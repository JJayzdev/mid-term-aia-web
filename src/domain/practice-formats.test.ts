import { describe, expect, it } from 'vitest';
import { makeExamBank, makeQuestion, testCatalog } from '../test/fixtures';
import { gradeAttempt, isBlankAnswer, isCorrect } from './grading';
import { practiceKind, practicePool, selectExam, selectPractice } from './quiz';
import { focusTopics, type Question, type QuestionBank } from './types';
import { validAnswer, validateBank } from './validation';

function matching(): Question {
  return { ...makeQuestion({ id: 'matching-fixture' }), question_type: 'matching', answer_format: 'matching',
    matching_items: [{ id: 'left-a', text: 'Term A', explanation: 'Because A.' }, { id: 'left-b', text: 'Term B' }],
    correct_answer: { 'left-a': 'b', 'left-b': 'a' } };
}
function ordering(): Question {
  return { ...makeQuestion({ id: 'ordering-fixture' }), question_type: 'ordering', answer_format: 'ordering',
    options: [{ id: 'a', text: 'Independent A' }, { id: 'b', text: 'Independent B' }, { id: 'c', text: 'After both' }],
    correct_answer: ['a', 'b', 'c'], accepted_orders: [['b', 'a', 'c']] };
}
const bankOf = (q: Question): QuestionBank => ({ schema_version: '1.0.0', bank_version: 'new-format-fixture', questions: [q] });
const itemOf = (q: Question) => ({ question: q, points: 100, optionOrder: q.options!.map(o => o.id) });

describe('matching and ordering contract', () => {
  it('allows verified supporting documents but requires a source anchored to the assigned topic', () => {
    const q = matching();
    const catalog = structuredClone(testCatalog);
    catalog.documents.push({ ...catalog.documents[0], document_id: 'support-doc' });
    const support = { ...q.source_reference[0], document_id: 'support-doc' };
    q.source_reference.push(support);
    expect(validateBank(bankOf(q), catalog).questions).toHaveLength(1);
    q.source_reference = [support];
    expect(() => validateBank(bankOf(q), catalog)).toThrow(/chủ đề chính/);
    q.source_reference.push({ ...support, document_id: 'doc-a', sha256: 'b'.repeat(64) });
    expect(() => validateBank(bankOf(q), catalog)).toThrow(/hash/);
  });
  it('validates both formats with reviewed optional focus and formula metadata', () => {
    const q = matching(); q.focus_topics = ['react'];
    q.formula_reference = { title: 'Formula', formula: 'x=1', symbols: 'x is state', conditions: 'Given model', example: 'x=1', common_mistakes: 'Wrong state' };
    expect(validateBank(bankOf(q), testCatalog).questions[0]).toEqual(q);
    expect(validateBank(bankOf(ordering()), testCatalog).questions).toHaveLength(1);
  });
  it('requires HTTPS supplemental URLs, valid access dates, and unique URLs', () => {
    const q = matching();
    const source = { title: 'Primary reference', url: 'https://example.org/reference', accessed_at: '2026-10-28', note: 'Outside-slide precision for this concept.' };
    q.supplemental_sources = [source];
    expect(validateBank(bankOf(q), testCatalog).questions).toHaveLength(1);
    for (const url of ['http://example.org', 'javascript:alert(1)', 'https:///no-host', 'not a URL']) {
      q.supplemental_sources = [{ ...source, url }];
      expect(() => validateBank(bankOf(q), testCatalog)).toThrow();
    }
    q.supplemental_sources = [{ ...source, accessed_at: '2026-02-31' }];
    expect(() => validateBank(bankOf(q), testCatalog)).toThrow();
    q.supplemental_sources = [source, { ...source, note: 'Same URL with a different note' }];
    expect(() => validateBank(bankOf(q), testCatalog)).toThrow(/lặp URL/);
  });
  it('rejects missing or unknown mapping keys, unknown targets and non-bijective one-to-one keys', () => {
    const keys: Record<string, string>[] = [{ 'left-a': 'b' }, { 'left-a': 'b', other: 'a' }, { 'left-a': 'b', 'left-b': 'unknown' }, { 'left-a': 'b', 'left-b': 'b' }];
    for (const key of keys) {
      const q = matching(); q.correct_answer = key;
      expect(() => validateBank(bankOf(q), testCatalog)).toThrow();
    }
    const q = matching(); q.matching_items![1].id = 'left-a';
    expect(() => validateBank(bankOf(q), testCatalog)).toThrow(/ID ghép cặp trùng/);
  });
  it('allows reusable targets only when explicitly declared', () => {
    const q = matching(); q.matching_reuse = true; q.correct_answer = { 'left-a': 'a', 'left-b': 'a' };
    expect(validateBank(bankOf(q), testCatalog).questions).toHaveLength(1);
    expect(isCorrect(itemOf(q), { 'left-b': 'a', 'left-a': 'a' })).toBe(true);
  });
  it('validates every accepted order as a distinct complete permutation', () => {
    for (const order of [['a', 'b'], ['a', 'a', 'c'], ['a', 'b', 'z'], ['a', 'b', 'c']]) {
      const q = ordering(); q.accepted_orders = [order];
      expect(() => validateBank(bankOf(q), testCatalog)).toThrow();
    }
  });
  it('grades matching by stable ID exact mapping and ordering by any listed complete sequence', () => {
    const m = itemOf(matching()), o = itemOf(ordering());
    for (const answer of [undefined, {}, { 'left-a': 'b' }, { 'left-a': 'a', 'left-b': 'b' }, { 'left-a': 'b', 'left-b': 'a', extra: 'a' }]) expect(isCorrect(m, answer)).toBe(false);
    expect(isCorrect(m, { 'left-b': 'a', 'left-a': 'b' })).toBe(true);
    for (const answer of [undefined, [], ['a', 'b'], ['a', 'c', 'b'], ['a', 'a', 'c']]) expect(isCorrect(o, answer)).toBe(false);
    expect(isCorrect(o, ['b', 'a', 'c'])).toBe(true);
    expect(gradeAttempt([m, o], { [m.question.id]: { 'left-a': 'b' }, [o.question.id]: ['b', 'a', 'c'] }, {})).toMatchObject({ totalPoints: 100, objectivePoints: 100, pendingIds: [], wrongIds: [m.question.id] });
  });
  it('distinguishes empty from partial work and validates partial saved answers', () => {
    for (const answer of [undefined, '', '  ', [], {}]) expect(isBlankAnswer(answer)).toBe(true);
    for (const answer of [false, { 'left-a': 'b' }, ['b']]) expect(isBlankAnswer(answer)).toBe(false);
    expect(validAnswer(matching(), {})).toBe(true);
    expect(validAnswer(matching(), { 'left-a': 'b' })).toBe(true);
    expect(validAnswer(matching(), { 'left-a': 'a', 'left-b': 'a' })).toBe(false);
    expect(validAnswer(matching(), JSON.parse('{"__proto__":"a"}'))).toBe(false);
    expect(validAnswer(ordering(), ['b'])).toBe(true);
    expect(validAnswer(ordering(), ['b', 'b'])).toBe(false);
  });
  it('persists independently shuffled matching columns in deterministic snapshots', () => {
    const q = matching();
    const first = selectPractice([q], 'mixed', { seed: 'pair-columns', count: 1 });
    expect(first).toEqual(selectPractice([q], 'mixed', { seed: 'pair-columns', count: 1 }));
    expect(new Set(first.items[0].matchingOrder)).toEqual(new Set(['left-a', 'left-b']));
    expect(new Set(first.items[0].optionOrder)).toEqual(new Set(['a', 'b']));
    expect(q.matching_items!.map(o => o.id)).toEqual(['left-a', 'left-b']);
  });
  it('keeps interactive practice out of the established exam blueprint', () => {
    const b = makeExamBank(); const before = selectExam(b.questions, testCatalog, undefined, 'same-exam');
    expect(selectExam([...b.questions, matching(), ordering()], testCatalog, undefined, 'same-exam')).toEqual(before);
  });
  it('accepts anchored cross-document exam sources while excluding any invalid supporting reference', () => {
    const bank = makeExamBank();
    const catalog = structuredClone(testCatalog);
    catalog.documents.push({ ...catalog.documents[0], document_id: 'support-doc' });
    const before = selectExam(bank.questions, catalog, undefined, 'cross-doc');
    const q = bank.questions[0];
    const source = { ...q.source_reference[0], document_id: 'support-doc' };
    q.source_reference.push(source);
    const supported = selectExam(bank.questions, catalog, undefined, 'cross-doc');
    expect(supported.items.map(i => [i.question.id, i.points])).toEqual(before.items.map(i => [i.question.id, i.points]));
    expect(supported.items.filter(i => i.question.phase === 1)).toHaveLength(36);
    for (const invalid of [
      { ...source, document_id: 'unknown-support' },
      { ...source, sha256: 'b'.repeat(64) },
      { ...source, pdf_page: 21 },
      { ...source, pdf_page: 0 },
      { ...source, pdf_page: 1.5 },
    ]) {
      q.source_reference = [q.source_reference[0], invalid];
      expect(() => selectExam(bank.questions, catalog, undefined, 'cross-doc')).toThrow(/Chưa đủ câu/);
    }
    q.source_reference = [source];
    expect(() => selectExam(bank.questions, catalog, undefined, 'cross-doc')).toThrow(/Chưa đủ câu/);
  });
  it('balances focus topic coverage and practice formats without repeats or unreviewed items', () => {
    const questions: Question[] = focusTopics.flatMap((topic, i) => ['matching', 'ordering', 'calculation', 'concept', 'scenario'].map((kind, j) => {
      const q = kind === 'matching' ? matching() : kind === 'ordering' ? ordering() : makeQuestion({ id: `base-${i}-${j}` });
      q.id = `${topic}-${kind}`; q.question = `Unique ${q.id}?`; q.focus_topics = [topic];
      if (kind === 'calculation') q.calculation = true;
      if (kind === 'scenario') { q.question_type = 'scenario'; q.context = 'Scenario input.'; }
      return q;
    }));
    const unreviewed = matching(); unreviewed.status = 'pending_review'; unreviewed.focus_topics = ['react']; questions.push(unreviewed);
    for (let seed = 0; seed < 20; seed++) {
      const result = selectPractice(questions, 'focus', { count: 14, seed: String(seed) });
      expect(result).toEqual(selectPractice(questions, 'focus', { count: 14, seed: String(seed) }));
      expect(new Set(result.items.map(i => i.question.id)).size).toBe(14);
      for (const topic of focusTopics) expect(result.items.filter(i => i.question.focus_topics?.includes(topic))).toHaveLength(2);
      expect(new Set(result.items.map(i => practiceKind(i.question))).size).toBe(5);
    }
    expect(practicePool(questions, 'focus', { focusTopic: 'kalman', practiceKind: 'matching' }).map(q => q.id)).toEqual(['kalman-matching']);
    expect(practicePool(questions, 'focus', { focusTopic: 'react', calculationOnly: true }).map(q => q.id)).toEqual(['react-calculation']);
    expect(practicePool(questions, 'focus', { phase: 2 })).toEqual([]);
  });
});
