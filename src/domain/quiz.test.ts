import { describe, expect, it } from 'vitest';
import { DomainError } from './errors';
import { examNeeds, practicePool, selectExam, selectPractice, validateTrackWeights } from './quiz';
import { makeExamBank, testCatalog } from '../test/fixtures';
import { decimalSumEquals } from './rational';

describe('practice selection', () => {
  const bank = makeExamBank();
  it('filters by mode, day, topic, and difficulty without crossing boundaries', () => {
    const one = bank.questions[0]; one.difficulty = 'easy';
    expect(practicePool(bank.questions, 'phase', { phase: 1, difficulty: 'easy' })).toEqual([one]);
    expect(practicePool(bank.questions, 'daily', { phase: 1, day: 'p1-d01', topic: 'p1-topic' })).toHaveLength(36);
  });
  it('keeps Phase 1 in mixed study while limiting only selected Phase 2 tracks', () => {
    const pool = practicePool(bank.questions, 'mixed', { tracks: [2] });
    expect(pool.some(q => q.phase === 1)).toBe(true);
    expect(pool.filter(q => q.phase === 2).every(q => q.track === 2)).toBe(true);
  });
  it('returns stable seeded question and option order for the same inputs', () => {
    const a = selectPractice(bank.questions, 'mixed', { count: 10, seed: 'stable' });
    const b = selectPractice(bank.questions, 'mixed', { count: 10, seed: 'stable' });
    expect(a.items.map(i => i.question.id)).toEqual(b.items.map(i => i.question.id));
    expect(a.items.map(i => i.optionOrder)).toEqual(b.items.map(i => i.optionOrder));
  });
  it('uses only independently reviewed approved questions and does not repeat IDs', () => {
    const questions = bank.questions.map(q => structuredClone(q));
    questions[0].status = 'pending_review'; questions[1].review!.reviewed_revision = 0;
    const selected = selectPractice(questions, 'phase', { phase: 1, count: 18, seed: 'review-filter' });
    expect(selected.items).toHaveLength(18);
    expect(new Set(selected.items.map(i => i.question.id)).size).toBe(18);
    expect(selected.items.every(i => i.question.status === 'approved' && i.question.review?.reviewed_revision === i.question.revision)).toBe(true);
  });
  it('reports shortages rather than duplicating or falling back to another group', () => {
    const error = (() => { try { selectPractice(bank.questions, 'phase', { phase: 1, count: 37 }); } catch (e) { return e; } })();
    expect(error).toBeInstanceOf(DomainError);
    expect((error as DomainError).code).toBe('insufficient_practice');
    expect((error as DomainError).detail).toMatchObject({ required: 37, available: 36, missing: 1 });
    expect(() => selectExam(bank.questions.slice(1), testCatalog)).toThrow(/Không tạo đề/);
  });
  it('lets wrong and bookmarked review sessions use even a single matching question', () => {
    const q = bank.questions[0];
    expect(selectPractice([q], 'wrong', {}, [q.id]).items).toHaveLength(1);
    expect(selectPractice([q], 'bookmarked', {}, [q.id]).items).toHaveLength(1);
    expect(() => selectPractice([], 'bookmarked', {}, ['missing'])).toThrow(/Không đủ câu/);
  });
});

describe('exact decimal configuration', () => {
  it('does not accept rounded near-matches as exact sums', () => {
    expect(decimalSumEquals([0.33335, 0.33335, 0.3333], 1)).toBe(true);
    expect(decimalSumEquals([0.33334, 0.33334, 0.33334], 1)).toBe(false);
  });
});

describe('90-minute exam blueprint', () => {
  it('keeps the exam count, uniqueness, and 60/40, 90/10, and per-track points invariant across 100 seeds', () => {
    for (let seed = 0; seed < 100; seed++) {
      const exam = selectExam(makeExamBank().questions, testCatalog, [25, 25, 25, 25], `exam-fixture-${seed}`);
      expect(exam.items).toHaveLength(60);
      expect(new Set(exam.items.map(i => i.question.id)).size).toBe(60);
      expect(exam.items.reduce((s, i) => s + i.points, 0)).toBe(10000);
      expect(exam.items.filter(i => i.question.phase === 1).reduce((s, i) => s + i.points, 0)).toBe(6000);
      expect(exam.items.filter(i => i.question.phase === 2).reduce((s, i) => s + i.points, 0)).toBe(4000);
      expect(exam.items.filter(i => i.question.answer_format === 'rubric').reduce((s, i) => s + i.points, 0)).toBe(1000);
      expect(exam.items.filter(i => i.question.phase === 1)).toHaveLength(36);
      expect(exam.items.filter(i => i.question.phase === 2)).toHaveLength(24);
      expect(exam.items.filter(i => i.question.phase === 1 && i.question.answer_format !== 'rubric')).toHaveLength(34);
      expect(exam.items.filter(i => i.question.phase === 1 && i.question.answer_format === 'rubric')).toHaveLength(2);
      for (const track of [1, 2, 3, 4]) expect(exam.items.filter(i => i.question.phase === 2 && i.question.track === track).reduce((s, i) => s + i.points, 0)).toBe(1000);
      for (const track of [1, 2, 3, 4]) expect(exam.items.filter(i => i.question.phase === 2 && i.question.track === track)).toHaveLength(6);
    }
  });
  it('rejects nonpositive, non-100%, and unrepresentable track weights', () => {
    expect(() => validateTrackWeights([0, 25, 25, 50])).toThrow(/số dương/);
    expect(() => validateTrackWeights([25, 25, 25, 24])).toThrow(/tổng đúng 100/);
    expect(() => validateTrackWeights([24.1, 25.3, 25.3, 25.3])).toThrow(/bước 0,25%/);
    expect(examNeeds([24, 26, 25, 25]).reduce((sum, n) => sum + n.slotPoints.reduce((a, b) => a + b, 0), 0)).toBe(10000);
    expect(validateTrackWeights([24.25, 25.25, 25.25, 25.25])).toBeUndefined();
  });
  it('distributes centipoint remainders deterministically without changing bucket totals', () => {
    const needs = examNeeds([24.25, 25.25, 25.25, 25.25]);
    const p1Objective = needs.find(n => n.phase === 1 && n.format === 'objective')!;
    expect(p1Objective.count).toBe(34);
    expect(p1Objective.slotPoints.filter(points => points === 159)).toHaveLength(28);
    expect(p1Objective.slotPoints.filter(points => points === 158)).toHaveLength(6);
    const track1Objective = needs.find(n => n.phase === 2 && n.track === 1 && n.format === 'objective')!;
    expect(track1Objective.slotPoints).toEqual([175, 175, 175, 174, 174]);
    expect(needs.filter(n => n.phase === 2 && n.track === 1).flatMap(n => n.slotPoints).reduce((a, b) => a + b, 0)).toBe(970);
    expect(needs.filter(n => n.format === 'rubric').flatMap(n => n.slotPoints).reduce((a, b) => a + b, 0)).toBe(1000);
    for (const need of needs) expect(Math.max(...need.slotPoints) - Math.min(...need.slotPoints)).toBeLessThanOrEqual(1);
  });
  it('keeps custom positive quarter-step track totals exact across seeded exams', () => {
    const weights = [24.25, 25.25, 25.25, 25.25] as const;
    for (let seed = 0; seed < 100; seed++) {
      const exam = selectExam(makeExamBank().questions, testCatalog, [...weights], `custom-weight-${seed}`);
      expect(exam.items).toHaveLength(60);
      expect(exam.items.reduce((sum, item) => sum + item.points, 0)).toBe(10000);
      expect(exam.items.filter(item => item.question.answer_format === 'rubric').reduce((sum, item) => sum + item.points, 0)).toBe(1000);
      for (const [index, weight] of weights.entries()) {
        const track = (index + 1) as 1 | 2 | 3 | 4;
        expect(exam.items.filter(item => item.question.phase === 2 && item.question.track === track).reduce((sum, item) => sum + item.points, 0)).toBe(40 * weight);
      }
    }
  });
  it('fails on missing bucket even when other buckets have surplus', () => {
    const bank = makeExamBank().questions.filter(q => q.id !== 't3-r');
    expect(() => selectExam(bank, testCatalog)).toThrow(/Track 3.*rubric.*cần 1, hiện có 0/);
  });
  it('makes the same exam for the same bank, weights, and seed', () => {
    const bank = makeExamBank().questions;
    expect(selectExam(bank, testCatalog, [25, 25, 25, 25], 'x').items.map(i => i.question.id)).toEqual(selectExam(bank, testCatalog, [25, 25, 25, 25], 'x').items.map(i => i.question.id));
  });
});
