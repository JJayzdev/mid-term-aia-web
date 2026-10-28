import { attemptResult } from '../domain/grading';
import { validAnswer, validateBank } from '../domain/validation';
import { DomainError } from '../domain/errors';
import type { AnswerValue, Attempt, AttemptQuestion, RubricMarks, StudyMode } from '../domain/types';

export const DB_NAME = 'aia-study-local';
export const DB_VERSION = 1;
export type Bookmark = { questionId: string; createdAt: number };
export type StagedImport = { id: string; createdAt: number; sourceVersion: string; questions: unknown[] };
export type AppBackup = { kind: 'aia-study-backup'; version: 1; exportedAt: string; attempts: Attempt[]; bookmarks: Bookmark[] };
let databasePromise: Promise<IDBDatabase> | null = null;

export function openDatabase(factory: IDBFactory = indexedDB): Promise<IDBDatabase> {
  if (factory === indexedDB && databasePromise) return databasePromise;
  const promise = new Promise<IDBDatabase>((resolve, reject) => {
    const request = factory.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('attempts')) db.createObjectStore('attempts', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('bookmarks')) db.createObjectStore('bookmarks', { keyPath: 'questionId' });
      if (!db.objectStoreNames.contains('imports')) db.createObjectStore('imports', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('settings')) db.createObjectStore('settings', { keyPath: 'key' });
    };
    request.onsuccess = () => { request.result.onversionchange = () => request.result.close(); resolve(request.result); };
    request.onerror = () => reject(request.error ?? new Error('Không thể mở IndexedDB.'));
    request.onblocked = () => reject(new Error('Cơ sở dữ liệu đang được dùng ở tab khác. Hãy tải lại sau khi đóng tab cũ.'));
  });
  if (factory === indexedDB) databasePromise = promise;
  return promise;
}

function requestValue<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => { request.onsuccess = () => resolve(request.result); request.onerror = () => reject(request.error); });
}
function txDone(tx: IDBTransaction): Promise<void> {
  return new Promise((resolve, reject) => { tx.oncomplete = () => resolve(); tx.onabort = tx.onerror = () => reject(tx.error ?? new Error('Giao dịch không thành công.')); });
}
function announce(id: string) { try { const channel = new BroadcastChannel('aia-study-attempts'); channel.postMessage({ id }); channel.close(); } catch { /* storage remains authoritative */ } }
function stableJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stableJson).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${stableJson((value as Record<string, unknown>)[key])}`).join(',')}}`;
  return JSON.stringify(value) ?? 'null';
}

export async function createAttempt(input: { mode: StudyMode; label: string; seed: string; bankVersion: string; questions: AttemptQuestion[]; writerToken?: string; now?: number; id?: string; durationMs?: number }): Promise<Attempt> {
  const db = await openDatabase();
  const now = input.now ?? Date.now();
  const attempt: Attempt = { id: input.id ?? crypto.randomUUID(), mode: input.mode, status: 'in_progress', label: input.label, startedAt: now, deadlineAt: input.mode === 'exam' ? now + (input.durationMs ?? 90 * 60_000) : null, submittedAt: null, finalizedAt: null, revision: 0, writerToken: input.writerToken ?? '', bankVersion: input.bankVersion, seed: input.seed, questions: structuredClone(input.questions), answers: {}, rubricMarks: {}, flags: [], score: null };
  const tx = db.transaction('attempts', 'readwrite');
  tx.objectStore('attempts').add(attempt);
  await txDone(tx);
  announce(attempt.id);
  return attempt;
}

export async function getAttempt(id: string): Promise<Attempt | undefined> {
  const db = await openDatabase(); return requestValue(db.transaction('attempts', 'readonly').objectStore('attempts').get(id));
}
export async function claimAttempt(id: string, writerToken: string): Promise<Attempt> {
  const db = await openDatabase(); const tx = db.transaction('attempts', 'readwrite'); const store = tx.objectStore('attempts');
  const current = await requestValue<Attempt | undefined>(store.get(id));
  if (!current) { tx.abort(); throw new DomainError('Phiên học không còn tồn tại.', 'missing_attempt'); }
  if (!['in_progress', 'submitted_pending_grading'].includes(current.status)) { await txDone(tx); return current; }
  const next: Attempt = { ...current, writerToken, revision: current.revision + 1 }; store.put(next);
  await txDone(tx); announce(id); return next;
}
export async function listAttempts(): Promise<Attempt[]> {
  const db = await openDatabase(); const rows = await requestValue<Attempt[]>(db.transaction('attempts', 'readonly').objectStore('attempts').getAll());
  return rows.sort((a, b) => (b.finalizedAt ?? b.startedAt) - (a.finalizedAt ?? a.startedAt));
}

async function finishInside(tx: IDBTransaction, attempt: Attempt, now: number, automatic: boolean): Promise<Attempt> {
  const result = attemptResult(attempt);
  const next = { ...attempt, status: result.pendingIds.length ? 'submitted_pending_grading' as const : 'graded' as const,
    submittedAt: automatic && attempt.deadlineAt !== null ? attempt.deadlineAt : now, finalizedAt: now, revision: attempt.revision + 1, score: result };
  tx.objectStore('attempts').put(next);
  return next;
}

export async function saveAnswer(id: string, questionId: string, answer: AnswerValue, expectedRevision: number, now = Date.now(), writerToken?: string): Promise<Attempt> {
  const db = await openDatabase(); const tx = db.transaction('attempts', 'readwrite'); const store = tx.objectStore('attempts');
  const current = await requestValue<Attempt | undefined>(store.get(id));
  if (!current) { tx.abort(); throw new DomainError('Phiên học không còn tồn tại.', 'missing_attempt'); }
  if (current.status !== 'in_progress') { tx.abort(); throw new DomainError('Bài đã nộp và không nhận thêm câu trả lời.', 'submitted'); }
  if (writerToken !== undefined && current.writerToken !== writerToken) { tx.abort(); throw new DomainError('Phiên này đang được chỉnh sửa ở tab khác. Tab hiện tại đã chuyển sang chỉ đọc.', 'writer_conflict'); }
  if (current.revision !== expectedRevision) { tx.abort(); throw new DomainError('Phiên đã thay đổi ở tab khác. Đang đồng bộ dữ liệu mới nhất.', 'revision_conflict'); }
  const item = current.questions.find(q => q.question.id === questionId);
  if (!item) { tx.abort(); throw new DomainError('Câu hỏi không thuộc phiên này.', 'unknown_attempt_question'); }
  const q = item.question;
  if (!validAnswer(q, answer)) { tx.abort(); throw new DomainError('Đáp án không hợp lệ cho câu hỏi này.', 'answer_shape'); }
  if (current.deadlineAt !== null && now >= current.deadlineAt) {
    const next = await finishInside(tx, current, now, true); await txDone(tx); announce(id); return next;
  }
  const next = { ...current, answers: { ...current.answers, [questionId]: structuredClone(answer) }, revision: current.revision + 1 };
  store.put(next); await txDone(tx); announce(id); return next;
}

export async function toggleFlag(id: string, questionId: string, expectedRevision: number, now = Date.now(), writerToken?: string): Promise<Attempt> {
  const db = await openDatabase(); const tx = db.transaction('attempts', 'readwrite'); const store = tx.objectStore('attempts');
  const current = await requestValue<Attempt | undefined>(store.get(id));
  if (!current) { tx.abort(); throw new DomainError('Phiên học không còn tồn tại.', 'missing_attempt'); }
  if (current.status !== 'in_progress') { tx.abort(); throw new DomainError('Bài đã nộp và không thể đánh dấu.', 'submitted'); }
  if (writerToken !== undefined && current.writerToken !== writerToken) { tx.abort(); throw new DomainError('Phiên này đang được chỉnh sửa ở tab khác. Tab hiện tại đã chuyển sang chỉ đọc.', 'writer_conflict'); }
  if (current.revision !== expectedRevision) { tx.abort(); throw new DomainError('Phiên đã thay đổi ở tab khác.', 'revision_conflict'); }
  if (!current.questions.some(q => q.question.id === questionId)) { tx.abort(); throw new DomainError('Câu hỏi không thuộc phiên này.', 'unknown_attempt_question'); }
  if (current.deadlineAt !== null && now >= current.deadlineAt) { const next = await finishInside(tx, current, now, true); await txDone(tx); announce(id); return next; }
  const flags = current.flags.includes(questionId) ? current.flags.filter(id => id !== questionId) : [...current.flags, questionId];
  const next = { ...current, flags, revision: current.revision + 1 }; store.put(next); await txDone(tx); announce(id); return next;
}

export async function submitAttempt(id: string, expectedRevision?: number, now = Date.now(), automatic = false, writerToken?: string): Promise<Attempt> {
  const db = await openDatabase(); const tx = db.transaction('attempts', 'readwrite'); const store = tx.objectStore('attempts');
  const current = await requestValue<Attempt | undefined>(store.get(id));
  if (!current) { tx.abort(); throw new DomainError('Phiên học không còn tồn tại.', 'missing_attempt'); }
  if (current.status !== 'in_progress') { await txDone(tx); return current; }
  if (!automatic && writerToken !== undefined && current.writerToken !== writerToken) { tx.abort(); throw new DomainError('Phiên này đang được chỉnh sửa ở tab khác. Tab hiện tại đã chuyển sang chỉ đọc.', 'writer_conflict'); }
  if (expectedRevision !== undefined && current.revision !== expectedRevision) { tx.abort(); throw new DomainError('Phiên đã thay đổi ở tab khác.', 'revision_conflict'); }
  if (automatic && (current.deadlineAt === null || now < current.deadlineAt)) { tx.abort(); throw new DomainError('Chưa đến thời gian tự nộp.', 'before_deadline'); }
  const expired = current.deadlineAt !== null && now >= current.deadlineAt;
  const next = await finishInside(tx, current, now, automatic || expired); await txDone(tx); announce(id); return next;
}

export async function gradeRubric(id: string, questionId: string, marks: RubricMarks, expectedRevision: number, writerToken?: string): Promise<Attempt> {
  const db = await openDatabase(); const tx = db.transaction('attempts', 'readwrite'); const store = tx.objectStore('attempts');
  const current = await requestValue<Attempt | undefined>(store.get(id));
  if (!current) { tx.abort(); throw new DomainError('Phiên học không còn tồn tại.', 'missing_attempt'); }
  if (current.status !== 'submitted_pending_grading') { tx.abort(); throw new DomainError('Phiên này không chờ tự chấm.', 'not_pending'); }
  if (writerToken !== undefined && current.writerToken !== writerToken) { tx.abort(); throw new DomainError('Phiên này đang được chỉnh sửa ở tab khác. Tab hiện tại đã chuyển sang chỉ đọc.', 'writer_conflict'); }
  if (current.revision !== expectedRevision) { tx.abort(); throw new DomainError('Phiên đã thay đổi ở tab khác.', 'revision_conflict'); }
  const item = current.questions.find(q => q.question.id === questionId);
  if (!item || item.question.answer_format !== 'rubric' || typeof current.answers[questionId] !== 'string' || !(current.answers[questionId] as string).trim()) { tx.abort(); throw new DomainError('Không thể chấm câu hỏi trống hoặc không có rubric.', 'rubric_unavailable'); }
  const allowed = new Set(item.question.rubric?.map(c => c.id) ?? []);
  if (Object.keys(marks).length !== allowed.size || Object.entries(marks).some(([criterionId, mark]) => !allowed.has(criterionId) || ![0, 0.5, 1].includes(mark))) { tx.abort(); throw new DomainError('Mỗi tiêu chí cần một mức 0, 0,5 hoặc 1.', 'rubric_marks'); }
  const rubricMarks = { ...current.rubricMarks, [questionId]: marks };
  const staged = { ...current, rubricMarks };
  const score = attemptResult(staged);
  const next: Attempt = { ...staged, status: score.pendingIds.length ? 'submitted_pending_grading' : 'graded', revision: current.revision + 1, score };
  store.put(next); await txDone(tx); announce(id); return next;
}

export async function toggleBookmark(questionId: string, now = Date.now()): Promise<boolean> {
  const db = await openDatabase(); const tx = db.transaction('bookmarks', 'readwrite'); const store = tx.objectStore('bookmarks');
  const old = await requestValue<Bookmark | undefined>(store.get(questionId));
  if (old) store.delete(questionId); else store.add({ questionId, createdAt: now });
  await txDone(tx); return !old;
}
export async function listBookmarks(): Promise<Bookmark[]> { const db = await openDatabase(); return requestValue(db.transaction('bookmarks', 'readonly').objectStore('bookmarks').getAll()); }

export async function stageImport(imported: StagedImport): Promise<void> {
  if (imported.questions.length > 5000) throw new DomainError('Tệp nhập vượt giới hạn 5.000 câu.', 'import_size');
  const db = await openDatabase(); const tx = db.transaction('imports', 'readwrite'); tx.objectStore('imports').put(structuredClone(imported)); await txDone(tx);
}
export async function listStagedImports(): Promise<StagedImport[]> { const db = await openDatabase(); return requestValue(db.transaction('imports', 'readonly').objectStore('imports').getAll()); }
export async function removeStagedImport(id: string): Promise<void> { const db = await openDatabase(); const tx = db.transaction('imports', 'readwrite'); tx.objectStore('imports').delete(id); await txDone(tx); }
export async function getSetting<T>(key: string, fallback: T): Promise<T> { const db = await openDatabase(); const row = await requestValue<{ key: string; value: T } | undefined>(db.transaction('settings', 'readonly').objectStore('settings').get(key)); return row?.value ?? fallback; }
export async function setSetting<T>(key: string, value: T): Promise<void> { const db = await openDatabase(); const tx = db.transaction('settings', 'readwrite'); tx.objectStore('settings').put({ key, value: structuredClone(value) }); await txDone(tx); }

export async function createBackup(): Promise<AppBackup> {
  const [attempts, bookmarks] = await Promise.all([listAttempts(), listBookmarks()]);
  return { kind: 'aia-study-backup', version: 1, exportedAt: new Date().toISOString(), attempts: attempts.filter(a => a.status !== 'in_progress'), bookmarks };
}
export function validateBackup(value: unknown): AppBackup {
  if (!value || typeof value !== 'object') throw new DomainError('Tệp sao lưu không hợp lệ.', 'backup_shape');
  const b = value as Partial<AppBackup>;
  if (b.kind !== 'aia-study-backup' || b.version !== 1 || !Array.isArray(b.attempts) || !Array.isArray(b.bookmarks)) throw new DomainError('Tệp sao lưu cần đúng định dạng AIA Study v1.', 'backup_version');
  if (typeof b.exportedAt !== 'string' || !Number.isFinite(Date.parse(b.exportedAt)) || b.attempts.length > 10_000 || b.bookmarks.length > 50_000) throw new DomainError('Sao lưu vượt giới hạn hoặc có thời điểm xuất không hợp lệ.', 'backup_size');
  const attemptIds = new Set<string>(); let questionTotal = 0;
  for (const a of b.attempts) {
    if (!a || typeof a.id !== 'string' || !a.id || attemptIds.has(a.id) || !['graded', 'submitted_pending_grading'].includes(a.status) || !Array.isArray(a.questions) || !a.questions.length || a.questions.length > 500 || !a.answers || typeof a.answers !== 'object' || !a.rubricMarks || typeof a.rubricMarks !== 'object' || !Array.isArray(a.flags) || typeof a.label !== 'string' || !a.label || !['daily', 'track', 'phase', 'mixed', 'wrong', 'bookmarked', 'focus', 'exam'].includes(a.mode) || typeof a.bankVersion !== 'string' || typeof a.seed !== 'string' || !Number.isFinite(a.startedAt) || !Number.isFinite(a.submittedAt) || !Number.isFinite(a.finalizedAt) || a.finalizedAt! < a.startedAt || a.submittedAt! < a.startedAt || !Number.isInteger(a.revision) || a.revision < 0) throw new DomainError('Sao lưu chứa phiên sai định dạng hoặc trùng ID.', 'backup_attempt');
    attemptIds.add(a.id); questionTotal += a.questions.length;
    if (questionTotal > 500_000 || a.questions.some(i => !i || !Number.isFinite(i.points) || i.points <= 0 || !Array.isArray(i.optionOrder))) throw new DomainError('Sao lưu vượt giới hạn hoặc có snapshot câu hỏi sai.', 'backup_size');
    const qids = a.questions.map(i => i.question?.id);
    if (qids.some(id => typeof id !== 'string' || !id) || new Set(qids).size !== qids.length || a.flags.some(id => !qids.includes(id)) || Object.keys(a.answers).some(id => !qids.includes(id)) || Object.keys(a.rubricMarks).some(id => !qids.includes(id))) throw new DomainError('Sao lưu có câu hỏi, đáp án, đánh dấu hoặc ID bị trùng/không khớp.', 'backup_snapshot');
    const docs = new Map<string, { document_id: string; title: string; relative_path: string; page_count: number; sha256: string }>();
    const topics = new Map<string, { id: string; label: string; phase: 1 | 2; track: 1 | 2 | 3 | 4 | null; day: string | null; document_ids: string[]; question_count: number }>();
    for (const item of a.questions) {
      const q = item.question;
      if (!q || !Array.isArray(q.source_reference) || !q.source_reference.length) throw new DomainError('Snapshot sao lưu thiếu nguồn câu hỏi.', 'backup_snapshot');
      for (const src of q.source_reference) {
        if (!src || typeof src.document_id !== 'string' || !/^[a-f0-9]{64}$/.test(src.sha256) || !Number.isInteger(src.pdf_page) || src.pdf_page < 1) throw new DomainError('Snapshot sao lưu có nguồn sai định dạng.', 'backup_snapshot');
        const old = docs.get(src.document_id);
        if (old && old.sha256 !== src.sha256) throw new DomainError('Snapshot sao lưu có hash tài liệu mâu thuẫn.', 'backup_snapshot');
        docs.set(src.document_id, { document_id: src.document_id, title: src.title, relative_path: 'backup-snapshot', page_count: Math.max(old?.page_count ?? 0, src.pdf_page), sha256: src.sha256 });
      }
      const oldTopic = topics.get(q.topic);
      if (oldTopic && (oldTopic.phase !== q.phase || oldTopic.track !== q.track || oldTopic.day !== q.day)) throw new DomainError('Snapshot sao lưu có taxonomy mâu thuẫn.', 'backup_snapshot');
      const refs = [...new Set([...(oldTopic?.document_ids ?? []), ...q.source_reference.map(s => s.document_id)])];
      topics.set(q.topic, { id: q.topic, label: q.topic, phase: q.phase as 1 | 2, track: q.track, day: q.day, document_ids: refs, question_count: (oldTopic?.question_count ?? 0) + 1 });
    }
    try { validateBank({ schema_version: '1.0.0', bank_version: a.bankVersion, questions: a.questions.map(i => i.question) }, { schema_version: '1.0.0', catalog_version: 'backup', documents: [...docs.values()], topics: [...topics.values()] }, false); }
    catch (e) { throw new DomainError(`Snapshot sao lưu không hợp lệ: ${e instanceof Error ? e.message : 'dữ liệu sai'}`, 'backup_snapshot'); }
    if (a.questions.some(i => i.optionOrder.length !== (i.question.options?.length ?? 0) || new Set(i.optionOrder).size !== i.optionOrder.length || i.optionOrder.some(id => !i.question.options?.some(o => o.id === id)))) throw new DomainError('Snapshot thứ tự lựa chọn không khớp options.', 'backup_snapshot');
    if (a.questions.some(i => i.question.answer_format === 'matching'
      ? !Array.isArray(i.matchingOrder) || i.matchingOrder.length !== i.question.matching_items?.length || new Set(i.matchingOrder).size !== i.matchingOrder.length || i.matchingOrder.some(id => !i.question.matching_items?.some(o => o.id === id))
      : i.matchingOrder !== undefined)) throw new DomainError('Snapshot thứ tự cột ghép không khớp nội dung.', 'backup_snapshot');
    const allowed = new Set(qids);
    for (const item of a.questions) {
      const answer = a.answers[item.question.id];
      if (answer !== undefined) {
        const q = item.question;
        if (!validAnswer(q, answer)) throw new DomainError('Snapshot sao lưu chứa đáp án sai định dạng.', 'backup_answer');
      }
      const marks = a.rubricMarks[item.question.id];
      if (marks) { const ids = item.question.rubric?.map(c => c.id) ?? []; if (Object.keys(marks).length !== ids.length || Object.entries(marks).some(([id, mark]) => !ids.includes(id) || ![0, 0.5, 1].includes(mark))) throw new DomainError('Sao lưu chứa mức tự chấm sai.', 'backup_marks'); }
    }
    const result = attemptResult(a);
    if (!a.score || stableJson(a.score) !== stableJson(result) || (a.status === 'submitted_pending_grading') !== (result.pendingIds.length > 0)) throw new DomainError('Điểm trong sao lưu không khớp đáp án và rubric.', 'backup_score');
    if (Object.keys(a.answers).some(id => !allowed.has(id))) throw new DomainError('Sao lưu tham chiếu câu hỏi không tồn tại.', 'backup_answer');
  }
  const bookmarkIds = new Set<string>();
  if (b.bookmarks.some(bm => !bm || typeof bm.questionId !== 'string' || !bm.questionId || !Number.isFinite(bm.createdAt) || bookmarkIds.has(bm.questionId) || (bookmarkIds.add(bm.questionId), false))) throw new DomainError('Sao lưu có bookmark sai định dạng hoặc trùng ID.', 'backup_bookmark');
  return b as AppBackup;
}
export async function restoreBackup(backup: AppBackup): Promise<void> {
  backup = validateBackup(backup);
  const db = await openDatabase(); const tx = db.transaction(['attempts', 'bookmarks'], 'readwrite');
  const attempts = tx.objectStore('attempts'), bookmarks = tx.objectStore('bookmarks');
  for (const incoming of backup.attempts) {
    const existing = await requestValue<Attempt | undefined>(attempts.get(incoming.id));
    if (existing && stableJson(existing) !== stableJson(incoming)) { tx.abort(); throw new DomainError(`Không thể khôi phục: phiên ${incoming.id} đã tồn tại với dữ liệu khác.`, 'backup_conflict'); }
  }
  for (const incoming of backup.bookmarks) {
    const existing = await requestValue<Bookmark | undefined>(bookmarks.get(incoming.questionId));
    if (existing && stableJson(existing) !== stableJson(incoming)) { tx.abort(); throw new DomainError(`Không thể khôi phục: bookmark ${incoming.questionId} đã tồn tại.`, 'backup_conflict'); }
  }
  for (const attempt of backup.attempts) {
    if (attempt.status === 'in_progress') { tx.abort(); throw new DomainError('Không khôi phục phiên đang làm dở từ tệp sao lưu.', 'backup_active_attempt'); }
    attempts.put(structuredClone(attempt));
  }
  for (const bookmark of backup.bookmarks) bookmarks.put(structuredClone(bookmark));
  await txDone(tx);
}

export function resetDatabaseForTests() { databasePromise?.then(db => db.close()); databasePromise = null; }
