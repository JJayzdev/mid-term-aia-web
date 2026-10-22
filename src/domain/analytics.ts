import type { Attempt } from './types';

export type Performance = { earned: number; max: number };
export type TopicReview = { id: string; misses: number; sessions: number };
export type LearningAnalytics = {
  byPhase: Record<string, Performance>;
  byTrack: Record<string, Performance>;
  byTopic: Record<string, Performance>;
  topicsToReview: TopicReview[];
};

export function aggregateLearning(attempts: Attempt[]): LearningAnalytics {
  const byPhase: LearningAnalytics['byPhase'] = {};
  const byTrack: LearningAnalytics['byTrack'] = {};
  const byTopic: LearningAnalytics['byTopic'] = {};
  const misses = new Map<string, { count: number; sessions: Set<string> }>();
  const add = (target: Record<string, Performance>, rows: Record<string, Performance>) => {
    for (const [key, row] of Object.entries(rows)) {
      const total = target[key] ??= { earned: 0, max: 0 };
      total.earned += row.earned; total.max += row.max;
    }
  };
  for (const attempt of attempts) {
    if (attempt.status !== 'graded' || !attempt.score) continue;
    add(byPhase, attempt.score.byPhase); add(byTrack, attempt.score.byTrack); add(byTopic, attempt.score.byTopic);
    const topicByQuestion = new Map(attempt.questions.map(item => [item.question.id, item.question.topic]));
    for (const id of attempt.score.wrongIds) {
      const topic = topicByQuestion.get(id); if (!topic) continue;
      const entry = misses.get(topic) ?? { count: 0, sessions: new Set<string>() };
      entry.count += 1; entry.sessions.add(attempt.id); misses.set(topic, entry);
    }
  }
  const topicsToReview = [...misses].map(([id, entry]) => ({ id, misses: entry.count, sessions: entry.sessions.size })).sort((a, b) => b.misses - a.misses || a.id.localeCompare(b.id));
  return { byPhase, byTrack, byTopic, topicsToReview };
}
