import { beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import QuizSession from './QuizSession';
import { makeQuestion } from '../test/fixtures';
import { createAttempt, DB_NAME, getAttempt, resetDatabaseForTests } from '../storage/database';
import * as database from '../storage/database';
import type { Attempt, Question } from '../domain/types';

beforeEach(async () => {
  resetDatabaseForTests();
  await new Promise<void>((resolve, reject) => { const req = indexedDB.deleteDatabase(DB_NAME); req.onsuccess = () => resolve(); req.onerror = () => reject(req.error); });
});

function matching(): Question {
  return { ...makeQuestion({ id: 'match-test' }), answer_format: 'matching', question_type: 'matching',
    matching_items: [{ id: 'left-a', text: 'Khái niệm A', explanation: 'Giải thích cặp A.' }, { id: 'left-b', text: 'Khái niệm B', explanation: 'Giải thích cặp B.' }],
    correct_answer: { 'left-a': 'a', 'left-b': 'b' } };
}
function mount(attempt: Attempt) {
  return render(<QuizSession initial={attempt} writerToken="tab" topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
}
describe('structured question sessions', () => {
  it('persists partial ID pairs and shuffled columns, then shows per-pair results', async () => {
    const user = userEvent.setup();
    const attempt = await createAttempt({ id: 'matching-session', mode: 'focus', label: 'Ôn trọng tâm', seed: 's', bankVersion: 'test', writerToken: 'tab', questions: [{ question: matching(), points: 100, optionOrder: ['b', 'a'], matchingOrder: ['left-b', 'left-a'] }] });
    const view = mount(attempt);
    await user.selectOptions(screen.getByRole('combobox', { name: 'Ghép: Khái niệm A' }), 'a');
    await waitFor(async () => expect((await getAttempt(attempt.id))?.answers['match-test']).toEqual({ 'left-a': 'a' }));
    expect(screen.getByRole('combobox', { name: 'Ghép: Khái niệm B' }).querySelector('option[value="a"]')).toBeDisabled();
    const saved = (await getAttempt(attempt.id))!;
    view.unmount(); mount(saved);
    expect(screen.getAllByRole('combobox')[0]).toHaveAccessibleName('Ghép: Khái niệm B');
    expect(screen.getByRole('combobox', { name: 'Ghép: Khái niệm A' })).toHaveValue('a');
    await user.selectOptions(screen.getByRole('combobox', { name: 'Ghép: Khái niệm B' }), 'b');
    await waitFor(() => expect(screen.getByRole('button', { name: /^Nộp bài/ })).toBeEnabled());
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    await user.click(screen.getByRole('button', { name: /^Nộp bài/ }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.score?.totalPoints).toBe(100));
    expect(screen.getByText('Giải thích cặp A.')).toBeInTheDocument();
    expect(screen.getByText('Giải thích cặp B.')).toBeInTheDocument();
    expect(screen.getAllByText('Đúng', { exact: true })).toHaveLength(2);
  });
  it('keeps an initially valid order unanswered until confirmed and accepts an alternative order', async () => {
    const user = userEvent.setup();
    const q: Question = { ...makeQuestion({ id: 'ordering-test' }), answer_format: 'ordering', question_type: 'ordering', options: [{ id: 'a', text: 'Bước A' }, { id: 'b', text: 'Bước B' }, { id: 'c', text: 'Bước C' }], correct_answer: ['a', 'b', 'c'], accepted_orders: [['b', 'a', 'c']] };
    const attempt = await createAttempt({ id: 'order-session', mode: 'focus', label: 'Ôn trọng tâm', seed: 's', bankVersion: 'test', writerToken: 'tab', questions: [{ question: q, points: 100, optionOrder: ['b', 'a', 'c'] }] });
    mount(attempt);
    expect((await getAttempt(attempt.id))?.answers).toEqual({});
    expect(screen.getByRole('button', { name: 'Đưa bước 1 lên' })).toBeDisabled();
    await user.click(screen.getByRole('button', { name: 'Đưa bước 1 xuống' }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.answers[q.id]).toEqual(['a', 'b', 'c']));
    await user.click(screen.getByRole('button', { name: 'Đưa bước 2 lên' }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.answers[q.id]).toEqual(['b', 'a', 'c']));
    await user.click(screen.getByRole('button', { name: 'Xác nhận thứ tự này' }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.answers[q.id]).toEqual(['b', 'a', 'c']));
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    await user.click(screen.getByRole('button', { name: /^Nộp bài/ }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.score?.totalPoints).toBe(100));
    expect(screen.getByText('Thứ tự đúng', { exact: true })).toBeInTheDocument();
    expect(screen.getByText('Thứ tự hợp lệ 2')).toBeInTheDocument();
  });
  it('retains a failed matching write for retry without pretending it was saved', async () => {
    const user = userEvent.setup();
    const attempt = await createAttempt({ id: 'match-retry', mode: 'focus', label: 'Ôn trọng tâm', seed: 's', bankVersion: 'test', writerToken: 'tab', questions: [{ question: matching(), points: 100, optionOrder: ['a', 'b'], matchingOrder: ['left-a', 'left-b'] }] });
    const realSave = database.saveAnswer;
    vi.spyOn(database, 'saveAnswer').mockRejectedValueOnce(new DOMException('Full', 'QuotaExceededError')).mockImplementation((...args) => realSave(...args));
    mount(attempt);
    await user.selectOptions(screen.getByRole('combobox', { name: 'Ghép: Khái niệm A' }), 'a');
    expect(await screen.findByRole('alert')).toHaveTextContent('Không đủ dung lượng');
    expect((await getAttempt(attempt.id))?.answers).toEqual({});
    await user.click(screen.getByRole('button', { name: 'Thử lưu lại' }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.answers['match-test']).toEqual({ 'left-a': 'a' }));
  });
});
