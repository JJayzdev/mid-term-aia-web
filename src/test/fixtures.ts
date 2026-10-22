import type { Catalog, Question, QuestionBank } from '../domain/types';

export const testCatalog: Catalog = {
  schema_version: '1.0.0', catalog_version: 'test-fixture',
  documents: [{ document_id: 'doc-a', title: 'Tài liệu fixture kiểm thử', relative_path: 'test-only.pdf', page_count: 20, sha256: 'a'.repeat(64) }],
  topics: [
    { id: 'p1-topic', label: 'Chủ đề fixture Phase 1', phase: 1, track: null, day: 'p1-d01', document_ids: ['doc-a'], question_count: 20 },
    ...([1, 2, 3, 4] as const).map(track => ({ id: `p2-t${track}-topic`, label: `Chủ đề fixture Track ${track}`, phase: 2 as const, track, day: `p2-t${track}-d01`, document_ids: ['doc-a'], question_count: 4 })),
  ],
};

export function makeQuestion(input: { id: string; phase?: 1 | 2; track?: 1 | 2 | 3 | 4 | null; format?: Question['answer_format']; difficulty?: Question['difficulty']; status?: Question['status']; author?: string; reviewer?: string; revision?: number } ): Question {
  const phase = input.phase ?? 1; const track = input.track === undefined ? (phase === 1 ? null : 1) : input.track;
  const topic = phase === 1 ? 'p1-topic' : `p2-t${track}-topic`;
  const format = input.format ?? 'single_choice';
  const base: Question = {
    id: input.id, revision: input.revision ?? 1, author_id: input.author ?? 'writer', phase, track,
    day: phase === 1 ? 'p1-d01' : `p2-t${track}-d01`, topic, taxonomy_status: 'verified',
    question_type: format === 'rubric' ? 'short_answer' : format === 'boolean' ? 'true_false' : format,
    answer_format: format, difficulty: input.difficulty ?? 'medium', cognitive_level: 'understand',
    question: `Câu fixture ${input.id}?`, correct_answer: '', explanation: 'Giải thích fixture chỉ phục vụ kiểm thử.',
    source_reference: [{ document_id: 'doc-a', sha256: 'a'.repeat(64), pdf_page: 1, title: 'Tài liệu fixture', verification: 'verified' }],
    status: input.status ?? 'approved',
  };
  if (format === 'single_choice') { base.options = [{ id: 'a', text: 'Phương án A' }, { id: 'b', text: 'Phương án B' }]; base.shuffle_options = true; base.correct_answer = 'a'; }
  if (format === 'multiple_choice') { base.options = [{ id: 'a', text: 'Phương án A' }, { id: 'b', text: 'Phương án B' }, { id: 'c', text: 'Phương án C' }]; base.shuffle_options = true; base.correct_answer = ['a', 'c']; }
  if (format === 'boolean') base.correct_answer = true;
  if (format === 'rubric') { base.correct_answer = 'Mẫu ý trả lời'; base.rubric = [{ id: 'c1', description: 'Tiêu chí một', weight: 0.5, full_credit: 'Đủ ý', partial_credit: 'Một phần', no_credit: 'Thiếu ý' }, { id: 'c2', description: 'Tiêu chí hai', weight: 0.5, full_credit: 'Đủ ý', partial_credit: 'Một phần', no_credit: 'Thiếu ý' }]; }
  if (base.status === 'approved') base.review = { reviewer_id: input.reviewer ?? 'reviewer', reviewed_at: '2026-10-20T12:00:00Z', reviewed_revision: base.revision, report_id: 'review-fixture' };
  return base;
}

export function makeExamBank(): QuestionBank {
  const questions: Question[] = [];
  for (let i = 0; i < 18; i++) questions.push(makeQuestion({ id: `p1-o-${String(i).padStart(2, '0')}`, phase: 1, format: 'single_choice' }));
  for (let i = 0; i < 2; i++) questions.push(makeQuestion({ id: `p1-r-${i}`, phase: 1, format: 'rubric' }));
  for (const track of [1, 2, 3, 4] as const) {
    for (let i = 0; i < 3; i++) questions.push(makeQuestion({ id: `t${track}-o-${i}`, phase: 2, track, format: 'single_choice' }));
    questions.push(makeQuestion({ id: `t${track}-r`, phase: 2, track, format: 'rubric' }));
  }
  return { schema_version: '1.0.0', bank_version: 'fixture-only-1', questions };
}
