import { describe, expect, it } from 'vitest';
import { gradeAttempt, isCorrect } from './grading';
import type { AttemptQuestion } from './types';
import { makeQuestion } from '../test/fixtures';

describe('objective and rubric grading', () => {
  it('uses exact-set grading for multiple choice and full-or-zero objective points', () => {
    const multi = makeQuestion({ id: 'multi', format: 'multiple_choice' });
    const item: AttemptQuestion = { question: multi, points: 375, optionOrder: ['c', 'a', 'b'] };
    expect(isCorrect(item, ['a', 'c'])).toBe(true);
    expect(isCorrect(item, ['a', 'c', 'b'])).toBe(false);
    expect(isCorrect(item, ['a'])).toBe(false);
    expect(isCorrect(item, ['a', 'a', 'c'])).toBe(false);
    const result = gradeAttempt([item], { multi: ['a', 'b'] }, {});
    expect(result.objectivePoints).toBe(0); expect(result.wrongIds).toEqual(['multi']);
  });
  it('grades single choice and boolean and keeps phase, track, and topic breakdowns additive', () => {
    const one = makeQuestion({ id: 'single', phase: 1 });
    const two = makeQuestion({ id: 'boolean', phase: 2, track: 2, format: 'boolean' });
    const items = [{ question: one, points: 300, optionOrder: ['a', 'b'] }, { question: two, points: 250, optionOrder: [] }];
    const result = gradeAttempt(items, { single: 'a', boolean: true }, {});
    expect(result.objectivePoints).toBe(550); expect(result.totalPoints).toBe(550);
    expect(result.byPhase['Phase 1']).toEqual({ earned: 300, max: 300 });
    expect(result.byTrack['Track 2']).toEqual({ earned: 250, max: 250 });
    expect(Object.values(result.byTopic).reduce((s, b) => s + b.earned, 0)).toBe(result.totalPoints);
  });
  it('keeps a nonblank essay pending without classifying it as wrong, while a blank is zero', () => {
    const essay = makeQuestion({ id: 'essay', format: 'rubric' });
    const item = { question: essay, points: 301, optionOrder: [] };
    const pending = gradeAttempt([item], { essay: 'Một câu trả lời có nội dung' }, {});
    expect(pending.pendingPoints).toBe(301); expect(pending.pendingIds).toEqual(['essay']); expect(pending.wrongIds).toEqual([]);
    const blank = gradeAttempt([item], { essay: '  ' }, {});
    expect(blank.pendingPoints).toBe(0); expect(blank.wrongIds).toEqual(['essay']);
  });
  it('rounds half up once at the end of each rubric question to one hundredth', () => {
    const essay = makeQuestion({ id: 'essay', format: 'rubric' });
    const item = { question: essay, points: 101, optionOrder: [] };
    const result = gradeAttempt([item], { essay: 'Response' }, { essay: { c1: 1, c2: 0 } });
    expect(result.rubricPoints).toBe(51);
    expect(result.pendingIds).toEqual([]); expect(result.wrongIds).toEqual([]);
    expect(result.byTopic[essay.topic]).toEqual({ earned: 51, max: 101 });
  });
  it('rounds an exact half-cent upward once after combining all rubric criteria', () => {
    const essay = makeQuestion({ id: 'half-cent', format: 'rubric' });
    const result = gradeAttempt([{ question: essay, points: 1, optionOrder: [] }], { 'half-cent': 'Response' }, { 'half-cent': { c1: 1, c2: 0 } });
    expect(result.rubricPoints).toBe(1);
  });
});
