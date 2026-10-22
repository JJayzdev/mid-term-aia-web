import { describe, expect, it } from 'vitest';
import { makeExamBank, makeQuestion, testCatalog } from '../test/fixtures';
import { validateBank } from './validation';

describe('question bank validation', () => {
  it('accepts a schema-valid release whose questions have independent current reviews', () => {
    expect(validateBank(makeExamBank(), testCatalog).questions).toHaveLength(60);
  });
  it('rejects duplicate question IDs and duplicate option IDs', () => {
    const duplicate = makeExamBank(); duplicate.questions.push(structuredClone(duplicate.questions[0]));
    expect(() => validateBank(duplicate, testCatalog)).toThrow(/ID câu hỏi bị trùng/);
    const badOption = makeQuestion({ id: 'bad-option' }); badOption.options![1].id = 'a';
    expect(() => validateBank({ schema_version: '1.0.0', bank_version: 'x', questions: [badOption] }, testCatalog)).toThrow(/option ID trùng/);
  });
  it.each([
    ['same reviewer', (q: ReturnType<typeof makeQuestion>) => { q.review!.reviewer_id = q.author_id; }],
    ['stale review revision', (q: ReturnType<typeof makeQuestion>) => { q.review!.reviewed_revision = 0; }],
    ['unverified source', (q: ReturnType<typeof makeQuestion>) => { q.source_reference[0].verification = 'needs_review'; }],
    ['unverified taxonomy', (q: ReturnType<typeof makeQuestion>) => { q.taxonomy_status = 'inferred'; }],
  ])('rejects an approved record with %s', (_label, mutate) => {
    const q = makeQuestion({ id: 'invalid' }); mutate(q);
    expect(() => validateBank({ schema_version: '1.0.0', bank_version: 'x', questions: [q] }, testCatalog)).toThrow();
  });
  it('rejects answer IDs outside the option set and a topic with mismatched taxonomy', () => {
    const q = makeQuestion({ id: 'bad-answer' }); q.correct_answer = 'missing';
    expect(() => validateBank({ schema_version: '1.0.0', bank_version: 'x', questions: [q] }, testCatalog)).toThrow(/đáp án không nằm trong options/);
    const wrongTopic = makeQuestion({ id: 'wrong-topic' }); wrongTopic.topic = 'p2-t1-topic';
    expect(() => validateBank({ schema_version: '1.0.0', bank_version: 'x', questions: [wrongTopic] }, testCatalog)).toThrow(/không khớp catalog/);
  });
  it('rejects a bank with an unknown schema version before business checks', () => {
    expect(() => validateBank({ schema_version: '9.0.0', bank_version: 'x', questions: [] }, testCatalog)).toThrow(/sai schema/);
  });
});
