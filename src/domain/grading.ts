import type { Attempt, AttemptQuestion, GradeSummary, RubricMarks } from './types';
import { weightedDecimalRoundHalfUp } from './rational';

export function isCorrect(item: AttemptQuestion, answer: unknown): boolean {
  const expected = item.question.correct_answer;
  if (item.question.answer_format === 'multiple_choice') {
    if (!Array.isArray(answer) || !Array.isArray(expected)) return false;
    return answer.length === expected.length && new Set(answer).size === expected.length && [...answer].every(id => expected.includes(id));
  }
  if (item.question.answer_format === 'single_choice') return typeof answer === 'string' && answer === expected;
  return typeof answer === 'boolean' && answer === expected;
}

export function gradeAttempt(items: AttemptQuestion[], answers: Record<string, unknown>, marksByQuestion: Record<string, RubricMarks>): GradeSummary {
  let objectivePoints = 0, rubricPoints = 0, pendingPoints = 0;
  const byPhase: GradeSummary['byPhase'] = {}, byTrack: GradeSummary['byTrack'] = {}, byTopic: GradeSummary['byTopic'] = {};
  const wrongIds: string[] = [], pendingIds: string[] = [];
  for (const item of items) {
    const q = item.question;
    const phaseKey = `Phase ${q.phase ?? '—'}`;
    const trackKey = q.track === null ? '—' : `Track ${q.track}`;
    const add = (bucket: { earned: number; max: number }) => { bucket.max += item.points; };
    const p = byPhase[phaseKey] ??= { earned: 0, max: 0 }; add(p);
    const t = byTrack[trackKey] ??= { earned: 0, max: 0 }; add(t);
    const topic = byTopic[q.topic] ??= { earned: 0, max: 0 }; add(topic);
    const answer = answers[q.id];
    let earned = 0;
    if (q.answer_format !== 'rubric') {
      if (isCorrect(item, answer)) earned = item.points;
      else wrongIds.push(q.id);
      objectivePoints += earned;
    } else {
      const nonempty = typeof answer === 'string' && answer.trim().length > 0;
      if (!nonempty) wrongIds.push(q.id);
      else {
        const marks = marksByQuestion[q.id] ?? {};
        const criteria = q.rubric ?? [];
        if (!criteria.length || criteria.some(c => ![0, 0.5, 1].includes(marks[c.id]))) {
          pendingIds.push(q.id);
          pendingPoints += item.points;
        } else {
          earned = weightedDecimalRoundHalfUp(criteria.map(c => c.weight), criteria.map(c => marks[c.id] ?? 0), item.points);
          rubricPoints += earned;
          if (earned === 0) wrongIds.push(q.id);
        }
      }
    }
    p.earned += earned; t.earned += earned; topic.earned += earned;
  }
  return { objectivePoints, rubricPoints, pendingPoints, totalPoints: objectivePoints + rubricPoints, maxPoints: items.reduce((s, i) => s + i.points, 0), byPhase, byTrack, byTopic, wrongIds, pendingIds };
}

export function attemptResult(attempt: Attempt): GradeSummary {
  return gradeAttempt(attempt.questions, attempt.answers, attempt.rubricMarks);
}
