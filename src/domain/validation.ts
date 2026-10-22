import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import schema from '../../docs/schemas/question-bank.schema.json';
import { DomainError } from './errors';
import { decimalSumEquals } from './rational';
import type { Catalog, QuestionBank } from './types';

const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const validateShape = ajv.compile(schema);

export function validateCatalog(value: unknown): asserts value is Catalog {
  if (!value || typeof value !== 'object') throw new DomainError('Tệp danh mục không phải JSON object.', 'catalog_shape');
  const c = value as Partial<Catalog>;
  if (c.schema_version !== '1.0.0' || typeof c.catalog_version !== 'string' || !Array.isArray(c.documents) || !Array.isArray(c.topics)) {
    throw new DomainError('Danh mục cần schema_version 1.0.0, catalog_version, documents và topics.', 'catalog_shape');
  }
  const docs = new Set<string>();
  for (const doc of c.documents) {
    if (!doc || typeof doc.document_id !== 'string' || !doc.document_id || typeof doc.title !== 'string' || typeof doc.relative_path !== 'string' || !Number.isInteger(doc.page_count) || doc.page_count < 1 || !/^[a-f0-9]{64}$/.test(doc.sha256) || docs.has(doc.document_id)) {
      throw new DomainError('Danh mục có tài liệu thiếu trường hoặc trùng document_id.', 'catalog_document');
    }
    docs.add(doc.document_id);
  }
  const topics = new Set<string>();
  for (const topic of c.topics) {
    if (!topic || typeof topic.id !== 'string' || !topic.id || typeof topic.label !== 'string' || ![1, 2].includes(topic.phase) ||
      ![null, 1, 2, 3, 4].includes(topic.track) || !Array.isArray(topic.document_ids) || !Number.isInteger(topic.question_count) || topic.question_count < 0 || topics.has(topic.id)) {
      throw new DomainError('Danh mục có topic thiếu trường, sai giá trị hoặc trùng ID.', 'catalog_topic');
    }
    if (topic.phase === 1 && topic.track !== null) throw new DomainError(`Topic ${topic.id}: Phase 1 phải có track=null.`, 'catalog_taxonomy');
    if (topic.phase === 2 && ![1, 2, 3, 4].includes(topic.track as number)) throw new DomainError(`Topic ${topic.id}: Phase 2 cần track 1–4.`, 'catalog_taxonomy');
    if (topic.document_ids.some(id => !docs.has(id))) throw new DomainError(`Topic ${topic.id} tham chiếu tài liệu không có trong danh mục.`, 'catalog_source');
    topics.add(topic.id);
  }
}

export function validateBank(value: unknown, catalog: Catalog, approvedOnly = true): QuestionBank {
  if (!validateShape(value)) {
    const detail = validateShape.errors?.map(e => `${e.instancePath || '/'} ${e.message}`).join('; ');
    throw new DomainError(`Ngân hàng sai schema: ${detail ?? 'không hợp lệ'}`, 'bank_schema', validateShape.errors);
  }
  const bank = value as QuestionBank;
  const ids = new Set<string>();
  const topics = new Map(catalog.topics.map(t => [t.id, t]));
  const docs = new Map(catalog.documents.map(d => [d.document_id, d]));
  const normalizedContent = new Set<string>();
  for (const q of bank.questions) {
    if (ids.has(q.id)) throw new DomainError(`ID câu hỏi bị trùng: ${q.id}`, 'duplicate_question', q.id);
    ids.add(q.id);
    if (approvedOnly && (q.status !== 'approved' || !q.review || q.review.reviewer_id === q.author_id || q.review.reviewed_revision !== q.revision || q.taxonomy_status !== 'verified' || q.phase === null || q.source_reference.some(s => s.verification !== 'verified'))) {
      throw new DomainError(`Câu ${q.id} chưa được duyệt độc lập đúng revision hoặc taxonomy/nguồn chưa xác minh.`, 'unapproved_question', q.id);
    }
    const topic = topics.get(q.topic);
    if (!topic) throw new DomainError(`Câu ${q.id} tham chiếu topic không có trong catalog: ${q.topic}`, 'unknown_topic', q.id);
    if (q.phase !== topic.phase || q.track !== topic.track || q.day !== topic.day) throw new DomainError(`Taxonomy của câu ${q.id} không khớp catalog.`, 'taxonomy_mismatch', q.id);
    if (q.source_reference.some(s => { const doc = docs.get(s.document_id); return !doc || !topic.document_ids.includes(s.document_id) || s.sha256 !== doc.sha256 || s.pdf_page > doc.page_count; })) throw new DomainError(`Câu ${q.id} tham chiếu sai document, hash hoặc trang trong catalog.`, 'unknown_source', q.id);
    const normalized = [q.question, q.context ?? '', ...(q.options ?? []).map(o => o.text)].join('\n').normalize('NFKC').replace(/\s+/g, ' ').trim().toLocaleLowerCase('vi-VN');
    if (normalizedContent.has(normalized)) throw new DomainError(`Nội dung câu hỏi bị trùng chính xác: ${q.id}`, 'duplicate_content', q.id);
    normalizedContent.add(normalized);
    const optionIds = new Set(q.options?.map(o => o.id) ?? []);
    if (optionIds.size !== (q.options?.length ?? 0)) throw new DomainError(`Câu ${q.id} có option ID trùng.`, 'duplicate_option', q.id);
    if (q.answer_format === 'single_choice' && (typeof q.correct_answer !== 'string' || !optionIds.has(q.correct_answer))) throw new DomainError(`Câu ${q.id} có đáp án không nằm trong options.`, 'answer_option', q.id);
    if (q.answer_format === 'multiple_choice' && (!Array.isArray(q.correct_answer) || q.correct_answer.length < 2 || q.correct_answer.length >= optionIds.size || new Set(q.correct_answer).size !== q.correct_answer.length || q.correct_answer.some(id => typeof id !== 'string' || !optionIds.has(id)))) throw new DomainError(`Câu ${q.id} cần ít nhất hai đáp án đúng và một phương án nhiễu hợp lệ.`, 'answer_option', q.id);
    if (q.answer_format === 'rubric') {
      const marks = q.rubric ?? [];
      if (new Set(marks.map(m => m.id)).size !== marks.length || !decimalSumEquals(marks.map(m => m.weight), 1)) throw new DomainError(`Rubric của câu ${q.id} phải có ID duy nhất và tổng trọng số chính xác bằng 1.`, 'rubric_weight', q.id);
    }
  }
  return bank;
}

export function stageImportedBank(bank: QuestionBank): QuestionBank {
  return { ...bank, bank_version: `${bank.bank_version}-staged`, questions: bank.questions.map(q => ({ ...q, status: 'pending_review', review: undefined })) };
}
