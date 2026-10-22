import { describe, expect, it } from 'vitest';
import { aggregateLearning } from './analytics';
import { gradeAttempt } from './grading';
import { makeQuestion } from '../test/fixtures';
import type { Attempt, AttemptQuestion } from './types';

function session(id: string, status: Attempt['status'], answer: string): Attempt {
  const question = makeQuestion({ id: `${id}-q` });
  const questions: AttemptQuestion[] = [{ question, points: 100, optionOrder: ['a', 'b'] }];
  const answers = { [question.id]: answer };
  return { id, mode: 'mixed', status, label: id, startedAt: 1, deadlineAt: null, submittedAt: 2, finalizedAt: 2, revision: 1, writerToken: 'tab', bankVersion: 'test', seed: id, questions, answers, rubricMarks: {}, flags: [], score: gradeAttempt(questions, answers, {}) };
}

describe('dashboard learning analytics', () => {
  it('aggregates completed scores by Phase, Track, and topic and excludes pending grading', () => {
    const right = session('right', 'graded', 'a');
    const wrong = session('wrong', 'graded', 'b');
    const pending = session('pending', 'submitted_pending_grading', 'b');
    const result = aggregateLearning([right, wrong, pending]);
    expect(result.byPhase['Phase 1']).toEqual({ earned: 100, max: 200 });
    expect(result.byTrack['—']).toEqual({ earned: 100, max: 200 });
    expect(result.byTopic['p1-topic']).toEqual({ earned: 100, max: 200 });
    expect(result.topicsToReview).toEqual([{ id: 'p1-topic', misses: 1, sessions: 1 }]);
  });
});
