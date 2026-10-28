import { DomainError } from './errors';
import { decimalProductIsInteger, decimalSumEquals } from './rational';
import type { AttemptQuestion, BucketNeed, Catalog, ExamWeights, FocusTopic, PracticeKind, Question, StudyMode } from './types';

export type QuizFilter = { phase?: 1 | 2; track?: 1 | 2 | 3 | 4; tracks?: (1 | 2 | 3 | 4)[]; day?: string; topic?: string; difficulty?: Question['difficulty']; calculationOnly?: boolean; practiceKind?: PracticeKind; focusTopic?: FocusTopic; focusOnly?: boolean; count?: number; seed?: string };
export type CandidateResult = { items: AttemptQuestion[]; seed: string; label: string };

function hashSeed(seed: string): number {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) { h ^= seed.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function rng(seed: string): () => number {
  let a = hashSeed(seed);
  return () => { a += 0x6D2B79F5; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function shuffled<T>(items: T[], random: () => number): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [out[i], out[j]] = [out[j], out[i]]; }
  return out;
}
function approved(questions: Question[]): Question[] {
  return questions.filter(q => q.status === 'approved' && q.review?.reviewer_id !== q.author_id && q.review?.reviewed_revision === q.revision && q.taxonomy_status === 'verified' && q.phase !== null && q.source_reference.every(s => s.verification === 'verified'));
}
const formatClass = (q: Question) => q.answer_format === 'rubric' ? 'rubric' : 'objective';
function makeItem(question: Question, points: number, random: () => number): AttemptQuestion {
  const ids = question.options?.map(o => o.id) ?? [];
  return { question, points, optionOrder: question.shuffle_options ? shuffled(ids, random) : ids,
    ...(question.answer_format === 'matching' ? { matchingOrder: shuffled(question.matching_items?.map(o => o.id) ?? [], random) } : {}) };
}
export function stableSeed(parts: (string | number)[]): string { return parts.join('|'); }

export function practiceKind(question: Question): PracticeKind {
  if (question.answer_format === 'matching' || question.answer_format === 'ordering') return question.answer_format;
  if (question.calculation) return 'calculation';
  return question.question_type === 'scenario' ? 'scenario' : 'concept';
}

export function practicePool(questions: Question[], mode: Exclude<StudyMode, 'exam'>, filter: QuizFilter, reviewIds: string[] = [], today = new Date().toISOString().slice(0, 10)): Question[] {
  let pool = approved(questions);
  if (filter.calculationOnly) pool = pool.filter(q => q.calculation === true);
  if (filter.practiceKind) pool = pool.filter(q => practiceKind(q) === filter.practiceKind);
  if (mode === 'focus' || filter.focusOnly) pool = pool.filter(q => Boolean(q.focus_topics?.length));
  if (filter.focusTopic) pool = pool.filter(q => q.focus_topics?.includes(filter.focusTopic!));
  if (mode === 'track') pool = pool.filter(q => q.phase === 2 && q.track === filter.track);
  if (mode === 'phase') pool = pool.filter(q => q.phase === filter.phase);
  if (filter.phase) pool = pool.filter(q => q.phase === filter.phase);
  if (filter.track) pool = pool.filter(q => q.track === filter.track);
  if (filter.tracks?.length) pool = pool.filter(q => q.phase !== 2 || filter.tracks!.includes(q.track as 1 | 2 | 3 | 4));
  if (filter.topic) pool = pool.filter(q => q.topic === filter.topic);
  if (filter.difficulty) pool = pool.filter(q => q.difficulty === filter.difficulty);
  if (mode === 'daily') {
    if (filter.day) pool = pool.filter(q => q.day === filter.day);
    else {
      const days = [...new Set(pool.map(q => q.day).filter((d): d is string => Boolean(d)))].sort();
      if (days.length) { const day = days[hashSeed(today) % days.length]; pool = pool.filter(q => q.day === day); }
    }
  }
  if (mode !== 'daily' && filter.day) pool = pool.filter(q => q.day === filter.day);
  if (mode === 'wrong' || mode === 'bookmarked') {
    const wanted = new Set(reviewIds);
    pool = pool.filter(q => wanted.has(q.id));
  }
  return pool.sort((a, b) => a.id.localeCompare(b.id));
}

export function selectPractice(questions: Question[], mode: Exclude<StudyMode, 'exam'>, filter: QuizFilter, reviewIds: string[] = [], today = new Date().toISOString().slice(0, 10)): CandidateResult {
  const seed = filter.seed ?? stableSeed([mode, filter.phase ?? 'all', filter.track ?? 'all', filter.day ?? today, filter.difficulty ?? 'all']);
  const random = rng(seed);
  const pool = practicePool(questions, mode, filter, reviewIds, today);
  const count = Math.max(1, filter.count ?? (mode === 'wrong' || mode === 'bookmarked' ? pool.length : 10));
  if (pool.length < count) throw new DomainError(`Không đủ câu đã duyệt cho phiên này: cần ${count}, hiện có ${pool.length}. Không lặp câu hoặc chuyển sang nhóm khác.`, 'insufficient_practice', { required: count, available: pool.length, missing: count - pool.length, mode });
  const picked = mode === 'focus' ? balancedFocus(pool, count, random) : shuffled(pool, random).slice(0, count);
  if (!picked.length) throw new DomainError('Chưa có câu hỏi đã duyệt phù hợp với lựa chọn này.', 'empty_pool', { mode, filter });
  return { seed, label: modeLabel(mode, filter), items: picked.map(q => makeItem(q, 100, random)) };
}

function modeLabel(mode: StudyMode, filter: QuizFilter): string {
  const names: Record<StudyMode, string> = { daily: 'Ôn tập hôm nay', track: `Track ${filter.track ?? '—'}`, phase: `Phase ${filter.phase ?? '—'}`, mixed: 'Luyện tập tổng hợp', wrong: 'Ôn câu cần xem lại', bookmarked: 'Câu đã lưu', focus: 'Ôn trọng tâm', exam: 'Thi thử 90 phút' };
  return names[mode];
}

/** Round-robin topic coverage, then the least-used available kind within that topic. */
function balancedFocus(pool: Question[], count: number, random: () => number): Question[] {
  const remaining = shuffled(pool, random);
  const picked: Question[] = [];
  const topicCounts = new Map<string, number>();
  const kindCounts = new Map<PracticeKind, number>();
  const topicOrder = shuffled([...new Set(pool.flatMap(q => q.focus_topics ?? []))], random);
  while (picked.length < count && remaining.length) {
    const available = topicOrder.filter(topic => remaining.some(q => q.focus_topics?.includes(topic)));
    const topic = available.sort((a, b) => (topicCounts.get(a) ?? 0) - (topicCounts.get(b) ?? 0))[0];
    const candidates = remaining.filter(q => q.focus_topics?.includes(topic));
    candidates.sort((a, b) => (kindCounts.get(practiceKind(a)) ?? 0) - (kindCounts.get(practiceKind(b)) ?? 0));
    const question = candidates[0];
    if (!question) break;
    remaining.splice(remaining.indexOf(question), 1);
    picked.push(question);
    topicCounts.set(topic, (topicCounts.get(topic) ?? 0) + 1);
    const kind = practiceKind(question);
    kindCounts.set(kind, (kindCounts.get(kind) ?? 0) + 1);
  }
  return shuffled(picked, random);
}

export function validateTrackWeights(weights: ExamWeights): void {
  if (weights.length !== 4 || weights.some(w => !Number.isFinite(w) || w <= 0) || !decimalSumEquals(weights, 100)) {
    throw new DomainError('Bốn trọng số Track phải là số dương và có tổng đúng 100%.', 'weights_sum');
  }
  if (weights.some(w => !decimalProductIsInteger(w, 4) || !decimalProductIsInteger(w, 36))) throw new DomainError('Trọng số Track cần theo bước 0,25%.', 'weights_precision');
}

function distributeCentipoints(total: number, count: number): number[] {
  if (!Number.isSafeInteger(total) || !Number.isSafeInteger(count) || count < 1 || total < count) throw new DomainError('Không thể chia điểm chính xác cho số slot đã chọn.', 'weights_precision');
  const base = Math.floor(total / count);
  const remainder = total - base * count;
  return Array.from({ length: count }, (_, index) => base + (index < remainder ? 1 : 0));
}

export function examNeeds(weights: ExamWeights = [25, 25, 25, 25]): BucketNeed[] {
  validateTrackWeights(weights);
  const needs: BucketNeed[] = [
    { phase: 1, track: null, format: 'objective', count: 34, slotPoints: distributeCentipoints(5400, 34) },
    { phase: 1, track: null, format: 'rubric', count: 2, slotPoints: distributeCentipoints(600, 2) },
  ];
  weights.forEach((w, index) => {
    needs.push({ phase: 2, track: (index + 1) as 1 | 2 | 3 | 4, format: 'objective', count: 5, slotPoints: distributeCentipoints(36 * w, 5) });
    needs.push({ phase: 2, track: (index + 1) as 1 | 2 | 3 | 4, format: 'rubric', count: 1, slotPoints: distributeCentipoints(4 * w, 1) });
  });
  const total = needs.reduce((sum, item) => sum + item.slotPoints.reduce((bucketSum, points) => bucketSum + points, 0), 0);
  if (total !== 10000) throw new DomainError('Cấu hình điểm thi không cộng chính xác thành 100 điểm.', 'weights_total');
  return needs;
}

export function selectExam(questions: Question[], catalog: Catalog, weights: ExamWeights = [25, 25, 25, 25], seed = 'aia-exam-v1'): CandidateResult {
  const needs = examNeeds(weights);
  const validTopics = new Map(catalog.topics.map(topic => [topic.id, topic]));
  const documents = new Map(catalog.documents.map(document => [document.document_id, document]));
  const pool = approved(questions).filter(q => {
    if (q.answer_format === 'matching' || q.answer_format === 'ordering') return false;
    const t = validTopics.get(q.topic);
    return t && t.phase === q.phase && t.track === q.track && t.day === q.day && t.document_ids.length > 0
      && q.source_reference.some(s => t.document_ids.includes(s.document_id))
      && q.source_reference.every(source => {
        const document = documents.get(source.document_id);
        return document && source.sha256 === document.sha256 && Number.isInteger(source.pdf_page)
          && source.pdf_page >= 1 && source.pdf_page <= document.page_count;
      });
  });
  for (const need of needs) {
    const available = pool.filter(q => q.phase === need.phase && q.track === need.track && formatClass(q) === need.format).length;
    if (available < need.count) {
      const name = need.phase === 1 ? 'Phase 1' : `Phase 2 · Track ${need.track}`;
      throw new DomainError(`Chưa đủ câu đã duyệt ở ${name} (${need.format}): cần ${need.count}, hiện có ${available}. Không tạo đề để tránh lặp câu hoặc bù từ nhóm khác.`, 'insufficient_questions', { ...need, available, missing: need.count - available });
    }
  }
  const calculationCount = pool.filter(q => q.phase === 2 && q.track === 4 && formatClass(q) === 'objective' && q.calculation).length;
  if (calculationCount < 2) throw new DomainError(`Chưa đủ câu tính toán đã duyệt ở Track 4: cần 2, hiện có ${calculationCount}. Không tạo đề.`, 'insufficient_questions');
  const random = rng(seed);
  const result: AttemptQuestion[] = [];
  for (const need of needs) {
    const bucket = pool.filter(q => q.phase === need.phase && q.track === need.track && formatClass(q) === need.format).sort((a, b) => a.id.localeCompare(b.id));
    let chosen: Question[];
    if (need.phase === 2 && need.track === 4 && need.format === 'objective') {
      const calculations = shuffled(bucket.filter(q => q.calculation), random).slice(0, 2);
      const selectedIds = new Set(calculations.map(q => q.id));
      chosen = [...calculations, ...shuffled(bucket.filter(q => !selectedIds.has(q.id)), random).slice(0, need.count - 2)];
    } else chosen = shuffled(bucket, random).slice(0, need.count);
    chosen.sort((a, b) => a.id.localeCompare(b.id));
    if (need.slotPoints.length !== chosen.length) throw new DomainError('Số slot điểm không khớp với blueprint.', 'exam_invariant');
    chosen.forEach((question, index) => result.push(makeItem(question, need.slotPoints[index], random)));
  }
  if (new Set(result.map(i => i.question.id)).size !== 60 || result.reduce((sum, i) => sum + i.points, 0) !== 10000) throw new DomainError('Đề thi không đạt invariant số câu/điểm.', 'exam_invariant');
  return { seed, label: 'Thi thử 90 phút', items: shuffled(result, random) };
}
