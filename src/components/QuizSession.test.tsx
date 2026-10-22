import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import QuizSession from './QuizSession';
import { makeQuestion } from '../test/fixtures';
import { createAttempt, DB_NAME, getAttempt, resetDatabaseForTests, submitAttempt } from '../storage/database';
import * as database from '../storage/database';

beforeEach(async () => {
  resetDatabaseForTests();
  await new Promise<void>((resolve, reject) => { const req = indexedDB.deleteDatabase(DB_NAME); req.onsuccess = () => resolve(); req.onerror = () => reject(req.error); req.onblocked = () => reject(new Error('delete blocked')); });
});

describe('essay answer navigation', () => {
  it('flushes rapid essay edits before navigating away', async () => {
    const user = userEvent.setup();
    const writerToken = 'test-tab';
    const questions = [
      { question: makeQuestion({ id: 'essay-first', format: 'rubric' }), points: 300, optionOrder: [] },
      { question: makeQuestion({ id: 'next-question' }), points: 300, optionOrder: ['a', 'b'] },
    ];
    const attempt = await createAttempt({ id: 'essay-navigation', mode: 'mixed', label: 'Ôn tập', seed: 's', bankVersion: 'test', questions, writerToken });
    render(<QuizSession initial={attempt} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
    const essay = screen.getByRole('textbox', { name: 'Câu trả lời tự luận' });
    await user.type(essay, 'Câu trả lời mới');
    await user.click(screen.getByRole('button', { name: 'Đi đến câu 2' }));
    await waitFor(async () => expect((await getAttempt(attempt.id))?.answers['essay-first']).toBe('Câu trả lời mới'));
    expect(screen.getByRole('heading', { name: 'Câu fixture next-question?' })).toBeInTheDocument();
  });
  it('shows a visible save failure and does not claim an answer was saved', async () => {
    const user = userEvent.setup();
    const writerToken = 'quota-tab';
    const attempt = await createAttempt({ id: 'visible-save-error', mode: 'mixed', label: 'Ôn tập', seed: 's', bankVersion: 'test', questions: [{ question: makeQuestion({ id: 'quota-question' }), points: 300, optionOrder: ['a', 'b'] }], writerToken });
    expect(await getAttempt(attempt.id)).toBeDefined();
    const read = vi.spyOn(database, 'getAttempt').mockResolvedValue(attempt);
    const write = vi.spyOn(database, 'saveAnswer').mockRejectedValue(new DOMException('Quota exceeded', 'QuotaExceededError'));
    try {
      render(<QuizSession initial={attempt} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
      await user.click(screen.getAllByRole('button', { name: /Phương án A/ })[0]);
      expect(await screen.findByRole('alert')).toHaveTextContent('Không đủ dung lượng để lưu câu trả lời');
      expect(screen.getByText(/Chưa lưu được/)).toBeInTheDocument();
      expect((await getAttempt(attempt.id))?.answers).toEqual({});
    } finally { write.mockRestore(); read.mockRestore(); }
  });
  it('keeps a failed essay draft, blocks navigation and submission, then retries the exact text', async () => {
    const user = userEvent.setup();
    const writerToken = 'retry-tab';
    const attempt = await createAttempt({ id: 'essay-retry', mode: 'exam', label: 'Thi thử', seed: 's', bankVersion: 'test', questions: [
      { question: makeQuestion({ id: 'retry-essay', format: 'rubric' }), points: 300, optionOrder: [] },
      { question: makeQuestion({ id: 'retry-next' }), points: 300, optionOrder: ['a', 'b'] },
    ], writerToken, durationMs: 90 * 60_000 });
    const realSave = database.saveAnswer;
    const write = vi.spyOn(database, 'saveAnswer')
      .mockRejectedValueOnce(new DOMException('Quota exceeded', 'QuotaExceededError'))
      .mockImplementation((...args) => realSave(...args));
    const confirm = vi.spyOn(window, 'confirm').mockReturnValue(true);
    try {
      render(<QuizSession initial={attempt} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
      const essay = screen.getByRole('textbox', { name: 'Câu trả lời tự luận' });
      fireEvent.change(essay, { target: { value: 'Bài luận cần được giữ nguyên khi lỗi lưu.' } });
      expect(await screen.findByRole('alert')).toHaveTextContent('Không đủ dung lượng');
      expect(screen.getByRole('textbox', { name: 'Câu trả lời tự luận' })).toHaveValue('Bài luận cần được giữ nguyên khi lỗi lưu.');
      expect(screen.getByRole('button', { name: /Tiếp/ })).toBeDisabled();
      expect(screen.getByRole('button', { name: /Nộp bài/ })).toBeDisabled();
      expect((await getAttempt(attempt.id))?.status).toBe('in_progress');
      await user.click(screen.getByRole('button', { name: /Thử lưu lại/ }));
      await waitFor(async () => expect((await getAttempt(attempt.id))?.answers['retry-essay']).toBe('Bài luận cần được giữ nguyên khi lỗi lưu.'));
      await user.click(screen.getByRole('button', { name: /Tiếp/ }));
      expect(await screen.findByRole('heading', { name: 'Câu fixture retry-next?' })).toBeInTheDocument();
      await user.click(screen.getAllByRole('button', { name: /Nộp bài/ })[0]);
      await waitFor(async () => expect((await getAttempt(attempt.id))?.status).toBe('submitted_pending_grading'));
      expect((await getAttempt(attempt.id))?.answers['retry-essay']).toBe('Bài luận cần được giữ nguyên khi lỗi lưu.');
      expect(confirm).toHaveBeenCalled();
    } finally { write.mockRestore(); confirm.mockRestore(); }
  });
  it('keeps the saving state until every queued essay edit finishes', async () => {
    const writerToken = 'queued-tab';
    const attempt = await createAttempt({ id: 'essay-queue-state', mode: 'mixed', label: 'Ôn tập', seed: 's', bankVersion: 'test', questions: [
      { question: makeQuestion({ id: 'queue-essay', format: 'rubric' }), points: 300, optionOrder: [] },
    ], writerToken });
    const resolvers: Array<(value: Awaited<ReturnType<typeof database.saveAnswer>>) => void> = [];
    const write = vi.spyOn(database, 'saveAnswer').mockImplementation(() => new Promise(resolve => resolvers.push(resolve)));
    try {
      render(<QuizSession initial={attempt} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
      const essay = screen.getByRole('textbox', { name: 'Câu trả lời tự luận' });
      fireEvent.change(essay, { target: { value: 'A' } });
      fireEvent.change(essay, { target: { value: 'AB' } });
      await waitFor(() => expect(resolvers).toHaveLength(1));
      expect(screen.getByText(/Đang lưu/)).toBeInTheDocument();
      resolvers[0](attempt);
      await waitFor(() => expect(resolvers).toHaveLength(2));
      expect(screen.getByText(/Đang lưu/)).toBeInTheDocument();
      resolvers[1](attempt);
      await waitFor(() => expect(screen.getByText(/Đã lưu/)).toBeInTheDocument());
      expect(screen.getByRole('textbox', { name: 'Câu trả lời tự luận' })).toHaveValue('AB');
    } finally { write.mockRestore(); }
  });
  it('allows question review after an expired attempt has auto-submitted', async () => {
    const user = userEvent.setup();
    const writerToken = 'expired-review-tab';
    const active = await createAttempt({ id: 'expired-review', mode: 'exam', label: 'Thi thử', seed: 's', bankVersion: 'test', questions: [
      { question: makeQuestion({ id: 'expired-first' }), points: 300, optionOrder: ['a', 'b'] },
      { question: makeQuestion({ id: 'expired-second' }), points: 300, optionOrder: ['a', 'b'] },
    ], writerToken, durationMs: 90 * 60_000 });
    const completed = await submitAttempt(active.id, active.revision, Date.now());
    render(<QuizSession initial={completed} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
    await user.click(screen.getByRole('button', { name: 'Đi đến câu 2' }));
    expect(await screen.findByRole('heading', { name: 'Câu fixture expired-second?' })).toBeInTheDocument();
    expect((await getAttempt(active.id))?.status).toBe('graded');
  });
  it('auto-submits saved answers when a queued essay write reaches storage after expiry', async () => {
    const writerToken = 'deadline-queue-tab';
    const created = await createAttempt({ id: 'deadline-queue', mode: 'exam', label: 'Thi thử', seed: 's', bankVersion: 'test', questions: [
      { question: makeQuestion({ id: 'deadline-essay', format: 'rubric' }), points: 300, optionOrder: [] },
      { question: makeQuestion({ id: 'deadline-objective' }), points: 300, optionOrder: ['a', 'b'] },
    ], writerToken, durationMs: 60_000 });
    const active = await database.saveAnswer(created.id, 'deadline-objective', 'a', created.revision, Date.now(), writerToken);
    const deadline = active.deadlineAt!;
    const realSave = database.saveAnswer;
    let release!: () => void;
    const write = vi.spyOn(database, 'saveAnswer').mockImplementation(async (...args) => {
      await new Promise<void>(resolve => { release = resolve; });
      const [id, questionId, answer, revision, , token] = args;
      return realSave(id, questionId, answer, revision, Date.now(), token);
    });
    const clock = vi.spyOn(Date, 'now').mockReturnValue(deadline - 1);
    try {
      render(<QuizSession initial={active} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
      fireEvent.change(screen.getByRole('textbox', { name: 'Câu trả lời tự luận' }), { target: { value: 'Bản nháp chưa được commit.' } });
      await waitFor(() => expect(release).toBeTypeOf('function'));
      clock.mockReturnValue(deadline + 1);
      release();
      await waitFor(async () => expect((await getAttempt(active.id))?.status).toBe('graded'));
      expect((await getAttempt(active.id))?.answers['deadline-essay']).toBeUndefined();
      expect((await getAttempt(active.id))?.answers['deadline-objective']).toBe('a');
      expect(screen.getByRole('textbox', { name: 'Câu trả lời tự luận' })).toHaveValue('Bản nháp chưa được commit.');
      expect(await screen.findByRole('alert')).toHaveTextContent('Thay đổi chưa lưu không được tính');
    } finally { write.mockRestore(); clock.mockRestore(); }
  });
  it('does not count a blank response as both wrong and blank', async () => {
    const writerToken = 'count-tab';
    const active = await createAttempt({ id: 'blank-count', mode: 'mixed', label: 'Ôn tập', seed: 's', bankVersion: 'test', questions: [{ question: makeQuestion({ id: 'blank-count-question' }), points: 300, optionOrder: ['a', 'b'] }], writerToken });
    const completed = await submitAttempt(active.id, active.revision, Date.now());
    render(<QuizSession initial={completed} writerToken={writerToken} topicLabels={new Map()} bookmarked={new Set()} onChange={() => {}} onExit={() => {}} onBookmarkChange={() => {}} onError={() => {}} />);
    expect(screen.getByText('sai hoặc chưa đạt').parentElement?.querySelector('b')).toHaveTextContent('0');
    expect(screen.getByText('bỏ trống').parentElement?.querySelector('b')).toHaveTextContent('1');
  });
});
