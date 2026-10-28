import { beforeEach, describe, expect, it, vi } from 'vitest';
import { makeExamBank, makeQuestion } from '../test/fixtures';
import { DomainError } from '../domain/errors';
import { claimAttempt, createAttempt, createBackup, DB_NAME, getAttempt, gradeRubric, listAttempts, openDatabase, resetDatabaseForTests, restoreBackup, saveAnswer, stageImport, submitAttempt, validateBackup } from './database';
import type { AttemptQuestion } from '../domain/types';
import { selectPractice } from '../domain/quiz';

beforeEach(async () => {
  resetDatabaseForTests();
  await new Promise<void>((resolve, reject) => { const req = indexedDB.deleteDatabase(DB_NAME); req.onsuccess = () => resolve(); req.onerror = () => reject(req.error); req.onblocked = () => reject(new Error('delete blocked')); });
});
const snapshot = (id = 'storage-q', format: 'single_choice' | 'rubric' = 'single_choice'): AttemptQuestion => ({ question: makeQuestion({ id, format }), points: 100, optionOrder: ['a', 'b'] });

describe('interactive practice persistence and backups', () => {
  it('retains partial matching, cleared answers and both column orders across connections', async () => {
    const q = makeQuestion({ id: 'persistent-pair' });
    q.question_type = q.answer_format = 'matching';
    q.matching_items = [{ id: 'left1', text: 'First term' }, { id: 'left2', text: 'Second term' }];
    q.correct_answer = { left1: 'b', left2: 'a' }; q.focus_topics = ['react'];
    const candidate = selectPractice([q], 'focus', { count: 1, seed: 'saved-columns' });
    const created = await createAttempt({ mode: 'focus', label: candidate.label, seed: candidate.seed, bankVersion: 'test', questions: candidate.items, now: 1000 });
    const partial = await saveAnswer(created.id, q.id, { left1: 'b' }, created.revision, 1100);
    resetDatabaseForTests();
    expect((await getAttempt(created.id))?.questions).toEqual(candidate.items);
    expect((await getAttempt(created.id))?.answers[q.id]).toEqual({ left1: 'b' });
    await expect(saveAnswer(created.id, q.id, { left1: 'b', left2: 'b' }, partial.revision, 1200)).rejects.toMatchObject({ code: 'answer_shape' });
    const clear = await saveAnswer(created.id, q.id, {}, partial.revision, 1200);
    expect(clear.answers[q.id]).toEqual({});
    const saved = await saveAnswer(created.id, q.id, { left2: 'a', left1: 'b' }, clear.revision, 1300);
    await submitAttempt(saved.id, saved.revision, 1400);
    const backup = await createBackup();
    expect(validateBackup(backup).attempts[0].score?.totalPoints).toBe(100);
    await restoreBackup(backup);
    expect((await listAttempts())).toHaveLength(1);
    const corrupted = structuredClone(backup);
    corrupted.attempts[0].questions[0].matchingOrder = ['left1', 'left1'];
    expect(() => validateBackup(corrupted)).toThrow(/thứ tự cột ghép/);
    const unknown = structuredClone(backup);
    unknown.attempts[0].answers[q.id] = { left1: 'b', extra: 'a' };
    expect(() => validateBackup(unknown)).toThrow(/đáp án sai định dạng/);
  });
  it('restores accepted alternative orders and rejects duplicate or unknown saved steps', async () => {
    const q = makeQuestion({ id: 'persistent-order' });
    q.question_type = q.answer_format = 'ordering';
    q.options!.push({ id: 'c', text: 'After first two' });
    q.correct_answer = ['a', 'b', 'c']; q.accepted_orders = [['b', 'a', 'c']];
    const candidate = selectPractice([q], 'mixed', { count: 1, seed: 'ordered' });
    const created = await createAttempt({ mode: 'mixed', label: candidate.label, seed: candidate.seed, bankVersion: 'test', questions: candidate.items, now: 1000 });
    const cleared = await saveAnswer(created.id, q.id, [], created.revision, 1100);
    const saved = await saveAnswer(created.id, q.id, ['b', 'a', 'c'], cleared.revision, 1200);
    await submitAttempt(saved.id, saved.revision, 1300);
    const backup = await createBackup();
    expect(validateBackup(backup).attempts[0].score?.totalPoints).toBe(100);
    for (const answer of [['a', 'a', 'c'], ['a', 'b', 'unknown']]) {
      const bad = structuredClone(backup); bad.attempts[0].answers[q.id] = answer;
      expect(() => validateBackup(bad)).toThrow(/đáp án sai định dạng/);
    }
    const partial = structuredClone(backup); partial.attempts[0].answers[q.id] = ['b', 'a'];
    expect(() => validateBackup(partial)).toThrow(/Điểm trong sao lưu/);
  });
});

describe('IndexedDB attempt persistence and concurrency', () => {
  it('persists each answer and restores it from a fresh database connection', async () => {
    const attempt = await createAttempt({ id: 'restore', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000 });
    await saveAnswer(attempt.id, 'storage-q', 'a', attempt.revision, 1100);
    resetDatabaseForTests();
    expect((await getAttempt(attempt.id))?.answers['storage-q']).toBe('a');
  });
  it('uses revision checks to prevent a second stale tab write', async () => {
    const attempt = await createAttempt({ id: 'cas', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000 });
    const outcomes = await Promise.allSettled([saveAnswer(attempt.id, 'storage-q', 'a', 0, 1100), saveAnswer(attempt.id, 'storage-q', 'b', 0, 1101)]);
    expect(outcomes.filter(o => o.status === 'fulfilled')).toHaveLength(1);
    expect(outcomes.filter(o => o.status === 'rejected')).toHaveLength(1);
    expect((await getAttempt(attempt.id))?.revision).toBe(1);
  });
  it('gives one tab write ownership and rejects the former tab after takeover', async () => {
    const attempt = await createAttempt({ id: 'owner', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], writerToken: 'tab-a', now: 1000 });
    const claimed = await claimAttempt(attempt.id, 'tab-b');
    await expect(saveAnswer(attempt.id, 'storage-q', 'a', claimed.revision, 1100, 'tab-a')).rejects.toMatchObject({ code: 'writer_conflict' });
    const saved = await saveAnswer(attempt.id, 'storage-q', 'b', claimed.revision, 1200, 'tab-b');
    expect(saved.answers['storage-q']).toBe('b');
  });
  it('rejects answer values outside the question option set', async () => {
    const attempt = await createAttempt({ id: 'bad-answer', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000 });
    await expect(saveAnswer(attempt.id, 'storage-q', 'forged-option', attempt.revision, 1100)).rejects.toMatchObject({ code: 'answer_shape' });
    expect((await getAttempt(attempt.id))?.answers).toEqual({});
  });
  it('keeps the prior answer when IndexedDB rejects a write and surfaces the quota error', async () => {
    const attempt = await createAttempt({ id: 'quota', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000 });
    const first = await saveAnswer(attempt.id, 'storage-q', 'a', attempt.revision, 1100);
    const write = vi.spyOn(IDBObjectStore.prototype, 'put').mockImplementation(() => { throw new DOMException('Quota exceeded', 'QuotaExceededError'); });
    try {
      await expect(saveAnswer(attempt.id, 'storage-q', 'b', first.revision, 1200)).rejects.toMatchObject({ name: 'QuotaExceededError' });
      expect((await getAttempt(attempt.id))?.answers['storage-q']).toBe('a');
    } finally { write.mockRestore(); }
  });
  it('grades the stored question snapshot after the source bank question changes', async () => {
    const sourceQuestion = makeQuestion({ id: 'snapshot-stability' });
    const attempt = await createAttempt({ id: 'snapshot-stability', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [{ question: sourceQuestion, points: 100, optionOrder: ['a', 'b'] }], now: 1000 });
    sourceQuestion.correct_answer = 'b';
    const saved = await saveAnswer(attempt.id, sourceQuestion.id, 'a', attempt.revision, 1100);
    const result = await submitAttempt(saved.id, saved.revision, 1200);
    expect(result.score?.objectivePoints).toBe(100);
    expect(result.score?.wrongIds).toEqual([]);
  });
  it('auto-submits atomically at the deadline and rejects post-expiry answers', async () => {
    const attempt = await createAttempt({ id: 'expiry', mode: 'exam', label: 'Mock', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000, durationMs: 5000 });
    const changed = await saveAnswer(attempt.id, 'storage-q', 'a', 0, 6000);
    expect(changed.status).toBe('graded'); expect(changed.submittedAt).toBe(attempt.deadlineAt); expect(changed.answers).toEqual({});
    await expect(saveAnswer(attempt.id, 'storage-q', 'b', changed.revision, 7000)).rejects.toMatchObject({ code: 'submitted' });
  });
  it('manual and automatic submit race has one idempotent final record', async () => {
    const attempt = await createAttempt({ id: 'race', mode: 'exam', label: 'Mock', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000, durationMs: 5000 });
    const first = await saveAnswer(attempt.id, 'storage-q', 'a', 0, 1200);
    const submitted = await Promise.all([submitAttempt(attempt.id, first.revision, 1300), submitAttempt(attempt.id, undefined, 7000, true)]);
    const final = await getAttempt(attempt.id);
    expect(final?.status).toBe('graded'); expect((await listAttempts()).filter(a => a.id === attempt.id)).toHaveLength(1);
    expect(submitted[0].id).toBe(submitted[1].id); expect(final?.submittedAt).toBeLessThanOrEqual(attempt.deadlineAt!);
  });
  it('keeps essay pending until every rubric level is selected, then stores self-grade', async () => {
    const attempt = await createAttempt({ id: 'rubric', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot('essay-storage', 'rubric')], now: 1000 });
    const saved = await saveAnswer(attempt.id, 'essay-storage', 'A nonblank answer', 0, 1100);
    const pending = await submitAttempt(attempt.id, saved.revision, 1200);
    expect(pending.status).toBe('submitted_pending_grading'); expect(pending.score?.pendingIds).toEqual(['essay-storage']);
    const graded = await gradeRubric(attempt.id, 'essay-storage', { c1: 1, c2: 0.5 }, pending.revision);
    expect(graded.status).toBe('graded'); expect(graded.score?.pendingIds).toEqual([]); expect(graded.score?.rubricPoints).toBe(75);
  });
  it('allows a resumed tab to finish pending self-grading and rejects the previous tab', async () => {
    const attempt = await createAttempt({ id: 'pending-owner', mode: 'exam', label: 'Mock', seed: 's', bankVersion: 'b1', questions: [snapshot('pending-essay', 'rubric')], writerToken: 'old-tab', now: 1000 });
    const answer = await saveAnswer(attempt.id, 'pending-essay', 'Response', 0, 1100, 'old-tab');
    const pending = await submitAttempt(answer.id, answer.revision, 1200, false, 'old-tab');
    const resumed = await claimAttempt(pending.id, 'new-tab');
    await expect(gradeRubric(resumed.id, 'pending-essay', { c1: 1, c2: 0.5 }, resumed.revision, 'old-tab')).rejects.toMatchObject({ code: 'writer_conflict' });
    const graded = await gradeRubric(resumed.id, 'pending-essay', { c1: 1, c2: 0.5 }, resumed.revision, 'new-tab');
    expect(graded.status).toBe('graded');
  });
  it('stages external content separately and never changes a staged question into approved', async () => {
    const batch = { id: 'batch', createdAt: 1, sourceVersion: 'foreign', questions: [{ status: 'pending_review' }] };
    await stageImport(batch);
    expect(await openDatabase()).toBeTruthy();
    const { listStagedImports } = await import('./database');
    expect((await listStagedImports())[0].questions).toEqual(batch.questions);
  });
});

describe('personal backup boundary', () => {
  it('rejects a backup containing an active exam attempt', () => {
    expect(() => validateBackup({ kind: 'aia-study-backup', version: 1, exportedAt: 'now', attempts: [{ id: 'x', status: 'in_progress' }], bookmarks: [] })).toThrow(DomainError);
  });
  it('rejects forged scores and conflicting restore IDs without overwriting local history', async () => {
    const attempt = await createAttempt({ id: 'safe', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000 });
    const saved = await saveAnswer(attempt.id, 'storage-q', 'a', 0, 1100);
    await submitAttempt(saved.id, saved.revision, 1200);
    const backup = await createBackup();
    const forged = structuredClone(backup) as typeof backup;
    forged.attempts[0].score!.totalPoints = 0;
    expect(() => validateBackup(forged)).toThrow(DomainError);
    const collision = structuredClone(backup); collision.attempts[0].label = 'Replacement';
    await expect(restoreBackup(collision)).rejects.toMatchObject({ code: 'backup_conflict' });
    expect((await getAttempt('safe'))?.label).toBe('Practice');
  });
  it('does not write earlier backup records when a later ID conflicts', async () => {
    const first = await createAttempt({ id: 'incoming-first', mode: 'mixed', label: 'First', seed: 's', bankVersion: 'b1', questions: [snapshot('first-q')], now: 1000 });
    const firstSaved = await saveAnswer(first.id, 'first-q', 'a', first.revision, 1100);
    await submitAttempt(firstSaved.id, firstSaved.revision, 1200);
    const second = await createAttempt({ id: 'incoming-second', mode: 'mixed', label: 'Second', seed: 's', bankVersion: 'b1', questions: [snapshot('second-q')], now: 1300 });
    const secondSaved = await saveAnswer(second.id, 'second-q', 'a', second.revision, 1400);
    await submitAttempt(secondSaved.id, secondSaved.revision, 1500);
    const backup = await createBackup();

    resetDatabaseForTests();
    await new Promise<void>((resolve, reject) => { const req = indexedDB.deleteDatabase(DB_NAME); req.onsuccess = () => resolve(); req.onerror = () => reject(req.error); req.onblocked = () => reject(new Error('delete blocked')); });
    const conflict = await createAttempt({ id: 'incoming-second', mode: 'mixed', label: 'Local version', seed: 's', bankVersion: 'b1', questions: [snapshot('local-q')], now: 1600 });
    const conflictSaved = await saveAnswer(conflict.id, 'local-q', 'a', conflict.revision, 1700);
    await submitAttempt(conflictSaved.id, conflictSaved.revision, 1800);

    await expect(restoreBackup(backup)).rejects.toMatchObject({ code: 'backup_conflict' });
    expect(await getAttempt('incoming-first')).toBeUndefined();
    expect((await getAttempt('incoming-second'))?.label).toBe('Local version');
  });
  it('round-trips completed sessions and restores them in one transaction', async () => {
    const attempt = await createAttempt({ id: 'backup', mode: 'mixed', label: 'Practice', seed: 's', bankVersion: 'b1', questions: [snapshot()], now: 1000 });
    const saved = await saveAnswer(attempt.id, 'storage-q', 'a', 0, 1100);
    await submitAttempt(saved.id, saved.revision, 1200);
    const backup = await createBackup();
    await restoreBackup(backup);
    expect((await getAttempt('backup'))?.status).toBe('graded'); expect(backup.attempts).toHaveLength(1);
  });
});

describe('legacy exam snapshot compatibility', () => {
  it('keeps the original 36-question points, answers, and grade when resumed and restored', async () => {
    const source = makeExamBank().questions;
    const selected = [
      ...source.filter(q => q.phase === 1 && q.answer_format !== 'rubric').sort((a, b) => a.id.localeCompare(b.id)).slice(0, 18),
      ...source.filter(q => q.phase === 1 && q.answer_format === 'rubric'),
      ...([1, 2, 3, 4] as const).flatMap(track => [
        ...source.filter(q => q.phase === 2 && q.track === track && q.answer_format !== 'rubric').sort((a, b) => a.id.localeCompare(b.id)).slice(0, 3),
        ...source.filter(q => q.phase === 2 && q.track === track && q.answer_format === 'rubric'),
      ]),
    ];
    const questions: AttemptQuestion[] = selected.map(question => ({
      question,
      points: question.phase === 1 ? 300 : question.answer_format === 'rubric' ? 100 : 300,
      optionOrder: question.options?.map(option => option.id) ?? [],
    }));
    expect(questions).toHaveLength(36);
    expect(questions.reduce((sum, item) => sum + item.points, 0)).toBe(10000);

    let attempt = await createAttempt({ id: 'legacy-36-exam', mode: 'exam', label: 'Thi thử 90 phút · bản cũ', seed: 'legacy-seed', bankVersion: 'legacy-bank-v1', questions, writerToken: 'legacy-tab', now: 1000 });
    for (let index = 0; index < questions.length; index++) {
      const item = questions[index];
      const answer = item.question.answer_format === 'rubric' ? `Bài tự luận ${item.question.id}` : item.question.correct_answer;
      attempt = await saveAnswer(attempt.id, item.question.id, answer, attempt.revision, 1100 + index, 'legacy-tab');
    }
    attempt = await submitAttempt(attempt.id, attempt.revision, 1200, false, 'legacy-tab');
    expect(attempt.status).toBe('submitted_pending_grading');
    expect(attempt.score).toMatchObject({ objectivePoints: 9000, pendingPoints: 1000, maxPoints: 10000 });

    const resumed = await claimAttempt(attempt.id, 'resume-tab');
    expect(resumed.questions).toEqual(questions);
    expect(resumed.answers).toEqual(attempt.answers);
    expect(resumed.score).toEqual(attempt.score);
    attempt = resumed;
    for (const item of questions.filter(part => part.question.answer_format === 'rubric')) {
      const marks = Object.fromEntries((item.question.rubric ?? []).map(criterion => [criterion.id, 1 as const]));
      attempt = await gradeRubric(attempt.id, item.question.id, marks, attempt.revision, 'resume-tab');
    }
    expect(attempt.status).toBe('graded');
    expect(attempt.score).toMatchObject({ objectivePoints: 9000, rubricPoints: 1000, totalPoints: 10000, maxPoints: 10000 });

    const backup = await createBackup();
    resetDatabaseForTests();
    await new Promise<void>((resolve, reject) => { const req = indexedDB.deleteDatabase(DB_NAME); req.onsuccess = () => resolve(); req.onerror = () => reject(req.error); req.onblocked = () => reject(new Error('delete blocked')); });
    await restoreBackup(backup);
    const restored = await getAttempt('legacy-36-exam');
    expect(restored?.questions).toEqual(questions);
    expect(restored?.questions.map(item => item.points)).toEqual(questions.map(item => item.points));
    expect(restored?.answers).toEqual(attempt.answers);
    expect(restored?.score).toEqual(attempt.score);
    expect(restored?.status).toBe('graded');
  });
});
