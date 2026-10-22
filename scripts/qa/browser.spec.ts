import { test, expect, type Page, type Dialog } from '@playwright/test';
import fs from 'node:fs';

async function rows(page: Page, store = 'attempts'): Promise<any[]> {
  return page.evaluate(async name => new Promise<any[]>((resolve, reject) => {
    const open = indexedDB.open('aia-study-local', 1);
    open.onerror = () => reject(open.error);
    open.onsuccess = () => { const db = open.result; const req = db.transaction(name).objectStore(name).getAll(); req.onsuccess = () => { resolve(req.result); db.close(); }; req.onerror = () => reject(req.error); };
  }), store);
}
async function startDaily(page: Page, day = 'p1-d01') {
  await page.goto('./#/study');
  await page.getByRole('combobox', { name: 'Ngày học', exact: true }).selectOption(day);
  await page.getByRole('button', { name: 'Bắt đầu lượt học' }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  return (await rows(page))[0];
}
async function submit(page: Page, a: any) {
  await page.getByRole('button', { name: `Đi đến câu ${a.questions.length}`, exact: true }).click();
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Nộp bài', exact: true }).last().click();
  await expect(page.locator('.result-summary')).toBeVisible();
}
test.beforeEach(async ({ page }) => {
  page.on('pageerror', error => { throw error; });
  page.on('console', message => { if (message.type() === 'error') throw new Error(message.text()); });
});

test('daily saves answer, order and bookmark across reload; wrong/bookmarked modes', async ({ page }) => {
  const a = await startDaily(page);
  const n = a.questions.findIndex((i: any) => i.question.answer_format === 'single_choice');
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  const q = a.questions[n].question;
  const wrong = q.options.find((o: any) => o.id !== q.correct_answer);
  await page.locator('.answer-option').nth(a.questions[n].optionOrder.indexOf(wrong.id)).click();
  await page.getByRole('button', { name: 'Lưu câu hỏi', exact: true }).click();
  await expect.poll(async () => (await rows(page))[0].answers[q.id]).toBe(wrong.id);
  await page.reload();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const resumed = (await rows(page))[0];
  expect(resumed.questions).toEqual(a.questions);
  expect(resumed.answers[q.id]).toBe(wrong.id);
  await expect(page.locator('.explanation')).toHaveCount(0);
  await submit(page, resumed);
  expect((await rows(page))[0].score.wrongIds).toContain(q.id);
  await page.getByRole('button', { name: 'Xem lịch sử', exact: true }).click();
  await page.goto('./#/study');
  await page.getByRole('button', { name: /^Đã lưu Quay lại/ }).click();
  await page.getByRole('button', { name: 'Bắt đầu lượt học' }).click();
  expect((await rows(page)).find(a => a.status === 'in_progress').questions.map((i: any) => i.question.id)).toEqual([q.id]);
  await submit(page, { questions: [q] });
  await page.getByRole('button', { name: 'Xem lịch sử', exact: true }).click();
  await page.goto('./#/study');
  await page.getByRole('button', { name: /^Câu cần xem lại Tập trung/ }).click();
  await page.getByRole('button', { name: 'Bắt đầu lượt học' }).click();
  expect((await rows(page)).find(a => a.status === 'in_progress').questions.some((i: any) => i.question.id === q.id)).toBe(true);
});

test('rapid essay input survives navigation and pending-grade reload', async ({ page }) => {
  const a = await startDaily(page);
  const n = a.questions.findIndex((i: any) => i.question.answer_format === 'rubric');
  expect(n).toBeGreaterThanOrEqual(0);
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  const answer = 'Mục tiêu rõ ràng, kiểm chứng nguồn và đánh giá kết quả theo rubric.';
  await page.getByLabel('Câu trả lời tự luận').pressSequentially(answer, { delay: 1 });
  await page.getByRole('button', { name: `Đi đến câu ${n === 0 ? 2 : 1}`, exact: true }).click();
  await expect(page.locator('.question-card h1')).toHaveText(a.questions[n === 0 ? 1 : 0].question.question);
  expect((await rows(page))[0].answers[a.questions[n].question.id]).toBe(answer);
  await submit(page, a);
  expect((await rows(page))[0].status).toBe('submitted_pending_grading');
  await page.reload();
  await page.goto('./#/history');
  await page.getByRole('button', { name: 'Tiếp tục tự chấm', exact: true }).first().click();
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  await expect(page.getByLabel('Câu trả lời tự luận')).toHaveValue(answer);
  for (const button of await page.getByRole('button', { name: 'Đạt', exact: true }).all()) await button.click();
  await page.getByRole('button', { name: 'Lưu tự đánh giá', exact: true }).click();
  await expect.poll(async () => (await rows(page))[0].status).toBe('graded');
  expect((await rows(page))[0].score.rubricPoints).toBe(100);
});

test('exam exact quotas, deadline autosubmit, reload and single result', async ({ page }) => {
  await page.clock.install();
  await page.goto('./#/exam');
  await page.getByRole('button', { name: 'Bắt đầu thi thử' }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const a = (await rows(page))[0];
  expect(a.questions).toHaveLength(60);
  expect(new Set(a.questions.map((i: any) => i.question.id)).size).toBe(60);
  expect(a.questions.filter((i: any) => i.question.phase === 1)).toHaveLength(36);
  expect(a.questions.filter((i: any) => i.question.phase === 2)).toHaveLength(24);
  for (const track of [1, 2, 3, 4]) expect(a.questions.filter((i: any) => i.question.track === track)).toHaveLength(6);
  expect(a.deadlineAt - a.startedAt).toBe(5400000);
  const points = (fn: (i: any) => boolean) => a.questions.filter(fn).reduce((s: number, i: any) => s + i.points, 0);
  expect(points(i => i.question.phase === 1)).toBe(6000);
  expect(points(i => i.question.phase === 2)).toBe(4000);
  expect(points(i => i.question.answer_format === 'rubric')).toBe(1000);
  for (const track of [1, 2, 3, 4]) expect(points(i => i.question.track === track)).toBe(1000);
  await expect(page.locator('.explanation, .self-grade')).toHaveCount(0);
  await page.clock.fastForward(5401000);
  await expect(page.locator('.result-summary')).toBeVisible();
  await page.getByRole('button', { name: 'Đi đến câu 2', exact: true }).click();
  await expect(page.locator('.question-card h1')).toHaveText(a.questions[1].question.question);
  await page.reload();
  const all = await rows(page);
  expect(all).toHaveLength(1); expect(all[0].status).toBe('graded');
  expect(all[0].submittedAt).toBe(a.deadlineAt);
  expect(all[0].score.totalPoints).toBe(0);
});

test('two tabs have one writer, preserving saved answer', async ({ page, context }) => {
  const a = await startDaily(page);
  const second = await context.newPage(); await second.goto('./');
  await expect(second.locator('.question-card h1')).toBeVisible();
  await expect(page.getByText('Phiên đang mở ở tab khác', { exact: true })).toBeVisible();
  const n = a.questions.findIndex((i: any) => i.question.answer_format === 'single_choice');
  await second.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  await second.locator('.answer-option').first().click();
  await expect.poll(async () => Object.keys((await rows(second))[0].answers).length).toBe(1);
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  await expect(page.locator('.answer-option').first()).toBeDisabled();
  expect(await rows(page)).toHaveLength(1);
});

test('closed exam resumes expired with its saved answers and no duplicate result', async ({ page, context }) => {
  await page.goto('./#/exam'); await page.getByRole('button', { name: 'Bắt đầu thi thử' }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const a = (await rows(page))[0];
  const n = a.questions.findIndex((i: any) => i.question.answer_format === 'single_choice');
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  await page.locator('.answer-option').first().click();
  await expect.poll(async () => Object.keys((await rows(page))[0].answers).length).toBe(1);
  const saved = (await rows(page))[0];
  const url = page.url(); await page.close();
  const resumed = await context.newPage(); await resumed.clock.install({ time: new Date(a.deadlineAt + 1000) });
  await resumed.goto(url); await expect(resumed.locator('.result-summary')).toBeVisible();
  const final = await rows(resumed); expect(final).toHaveLength(1);
  expect(final[0].questions).toEqual(a.questions); expect(final[0].answers).toEqual(saved.answers);
  expect(final[0].submittedAt).toBe(a.deadlineAt); expect(final[0].status).toBe('graded');
});

test('custom track weights and objective scoring follow stable option IDs', async ({ page }) => {
  await page.goto('./#/exam');
  await page.getByLabel('Trọng số Track 1', { exact: true }).fill('0');
  await expect(page.getByRole('button', { name: 'Bắt đầu thi thử' })).toBeDisabled();
  for (const [index, weight] of [10, 20, 30, 40].entries()) await page.getByLabel(`Trọng số Track ${index + 1}`, { exact: true }).fill(String(weight));
  await page.getByRole('button', { name: 'Bắt đầu thi thử' }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const a = (await rows(page))[0];
  for (const track of [1, 2, 3, 4]) expect(a.questions.filter((i: any) => i.question.track === track).reduce((sum: number, i: any) => sum + i.points, 0)).toBe(track * 400);
  expect(a.questions).toHaveLength(60);
  expect(a.questions.every((i: any) => Number.isInteger(i.points) && i.points > 0)).toBe(true);
  for (const [index, item] of a.questions.entries()) {
    const q = item.question; if (q.answer_format === 'rubric') continue;
    await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
    if (q.answer_format === 'boolean') await page.getByRole('button', { name: q.correct_answer ? 'Đúng' : 'Sai', exact: true }).click();
    else for (const id of Array.isArray(q.correct_answer) ? q.correct_answer : [q.correct_answer]) {
      const optionIndex = item.optionOrder.indexOf(id);
      expect(optionIndex).toBeGreaterThanOrEqual(0);
      await page.locator('.answer-option').nth(optionIndex).click();
      await expect.poll(async () => { const value = (await rows(page))[0].answers[q.id]; return Array.isArray(value) ? value.includes(id) : value === id; }).toBe(true);
    }
  }
  await submit(page, a);
  const final = (await rows(page))[0]; expect(final.status).toBe('graded');
  expect(final.score.totalPoints).toBe(9000); expect(final.score.pendingIds).toEqual([]);
  expect(final.score.wrongIds).toHaveLength(6);
});

test('export/restore roundtrip and external approved bank stays quarantined', async ({ page, browser }) => {
  const a = await startDaily(page); await submit(page, a);
  await page.getByRole('button', { name: 'Xem lịch sử', exact: true }).click();
  await page.goto('./#/data');
  const downloaded = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Tải bản sao lưu', exact: true }).click();
  const path = await (await downloaded).path(); expect(path).toBeTruthy();
  const backup = JSON.parse(fs.readFileSync(path!, 'utf8'));
  const context2 = await browser.newContext(); const restored = await context2.newPage();
  await restored.goto(new URL('./#/data', page.url()).href);
  await restored.locator('input[type=file]').setInputFiles(path!);
  await restored.getByRole('button', { name: 'Khôi phục dữ liệu', exact: true }).click();
  await expect.poll(async () => (await rows(restored)).length).toBe(1);
  expect((await rows(restored))[0].score).toEqual(backup.attempts[0].score);
  await page.locator('input[type=file]').setInputFiles({ name: 'invalid.json', mimeType: 'application/json', buffer: Buffer.from('{"schema_version":"999","questions":[]}') });
  await expect(page.getByRole('dialog')).toHaveCount(0);
  expect(await rows(page, 'imports')).toHaveLength(0);
  const bankResponse = await page.request.get(new URL('./data/bank.json', page.url()).href); const bank = await bankResponse.body();
  await page.locator('input[type=file]').setInputFiles({ name: 'bank.json', mimeType: 'application/json', buffer: bank });
  await page.getByRole('button', { name: 'Đưa vào vùng chờ', exact: true }).click();
  await expect.poll(async () => (await rows(page, 'imports')).length).toBe(1);
  expect((await rows(page, 'imports'))[0].questions.every((q: any) => q.status !== 'approved')).toBe(true);
  await context2.close();
});

test('filters restrict Phase, Track, topic and mixed scope', async ({ page }) => {
  for (const [mode, label, value, check] of [
    ['Theo Track Tập trung', 'Track', '4', (q: any) => q.phase === 2 && q.track === 4],
    ['Theo Phase Ôn theo', 'Phase', '1', (q: any) => q.phase === 1],
  ] as const) {
    await page.goto('./#/study');
    await page.getByRole('button', { name: new RegExp(`^${mode}`) }).click();
    await page.getByRole('combobox', { name: label, exact: true }).selectOption(value);
    await page.getByRole('button', { name: 'Bắt đầu lượt học' }).click();
    const a = (await rows(page)).find(a => a.status === 'in_progress'); expect(a.questions.every((i: any) => check(i.question))).toBe(true);
    await submit(page, a); await page.getByRole('button', { name: 'Xem lịch sử', exact: true }).click();
  }
  await page.goto('./#/study'); await page.getByRole('button', { name: /^Luyện tổng hợp Trộn/ }).click();
  await page.getByRole('combobox', { name: 'Chủ đề', exact: true }).selectOption('p1-d01');
  await page.getByRole('button', { name: 'Bắt đầu lượt học' }).click();
  const a = (await rows(page)).find(a => a.status === 'in_progress'); expect(a.questions.every((i: any) => i.question.day === 'p1-d01')).toBe(true);
});

test('failed answer write is visible and does not overwrite persisted data', async ({ page }) => {
  const a = await startDaily(page);
  const n = a.questions.findIndex((i: any) => i.question.answer_format === 'single_choice');
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  await page.evaluate(() => {
    const original = IDBObjectStore.prototype.put;
    (window as any).__qaOriginalPut = original;
    IDBObjectStore.prototype.put = function (...args: Parameters<IDBObjectStore['put']>) {
      if (this.name === 'attempts') throw new DOMException('QA simulated storage full', 'QuotaExceededError');
      return original.apply(this, args);
    };
  });
  await page.locator('.answer-option').first().click();
  await expect(page.getByRole('alert')).toContainText('Không đủ dung lượng để lưu câu trả lời');
  expect((await rows(page))[0].answers).toEqual({});
  await expect(page.locator('.session-progress')).not.toContainText('· Đã lưu');
  await page.evaluate(() => { IDBObjectStore.prototype.put = (window as any).__qaOriginalPut; });
  await page.locator('.answer-option').first().click();
  await expect.poll(async () => Object.keys((await rows(page))[0].answers).length).toBe(1);
  await page.getByRole('button', { name: `Đi đến câu ${n === 0 ? 2 : 1}`, exact: true }).click();
  await expect(page.locator('.question-card h1')).toHaveText(a.questions[n === 0 ? 1 : 0].question.question);
});

test('failed essay stays visible until retry succeeds; navigation and manual submit cannot discard it', async ({ page }) => {
  await page.goto('./#/exam'); await page.getByRole('button', { name: 'Bắt đầu thi thử' }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const a = (await rows(page))[0];
  const n = a.questions.findIndex((i: any) => i.question.answer_format === 'rubric');
  const q = a.questions[n].question;
  await page.getByRole('button', { name: `Đi đến câu ${n + 1}`, exact: true }).click();
  await page.getByLabel('Câu trả lời tự luận').fill('Bản đã ghi thành công.');
  await expect.poll(async () => (await rows(page))[0].answers[q.id]).toBe('Bản đã ghi thành công.');
  await page.evaluate(() => {
    (window as any).__qaOriginalPut = IDBObjectStore.prototype.put;
    IDBObjectStore.prototype.put = function (...args: Parameters<IDBObjectStore['put']>) {
      if (this.name === 'attempts') throw new DOMException('QA storage full', 'QuotaExceededError');
      return (window as any).__qaOriginalPut.apply(this, args);
    };
  });
  const draft = 'Bản chỉnh sửa mới phải được giữ lại để người học có thể thử lưu lại.';
  await page.getByLabel('Câu trả lời tự luận').fill(draft);
  await expect(page.getByRole('alert')).toContainText('Không đủ dung lượng');
  const next = page.getByRole('button', { name: `Đi đến câu ${n === 0 ? 2 : 1}`, exact: true });
  if (await next.isEnabled()) await next.click();
  await expect(page.getByLabel('Câu trả lời tự luận')).toHaveValue(draft);
  const exit = page.getByRole('button', { name: 'Tất cả chế độ', exact: true });
  if (await exit.isEnabled()) await exit.click();
  await expect(page.getByLabel('Câu trả lời tự luận')).toHaveValue(draft);
  const manual = page.getByRole('button', { name: 'Nộp bài', exact: true }).first();
  let prematureDialogs = 0;
  const acceptPrematureDialog = async (dialog: Dialog) => { prematureDialogs++; await dialog.accept(); };
  page.on('dialog', acceptPrematureDialog);
  if (await manual.isEnabled()) await manual.click();
  page.off('dialog', acceptPrematureDialog);
  expect(prematureDialogs).toBe(0);
  expect((await rows(page))[0].status).toBe('in_progress');
  expect((await rows(page))[0].answers[q.id]).toBe('Bản đã ghi thành công.');
  await page.evaluate(() => { IDBObjectStore.prototype.put = (window as any).__qaOriginalPut; });
  await page.getByRole('button', { name: 'Thử lưu lại', exact: true }).click();
  await expect.poll(async () => (await rows(page))[0].answers[q.id]).toBe(draft);
  await next.click();
  await expect(page.locator('.question-card h1')).toHaveText(a.questions[n === 0 ? 1 : 0].question.question);
  page.once('dialog', dialog => dialog.accept()); await manual.click();
  await expect(page.locator('.result-summary')).toBeVisible();
  expect((await rows(page))[0].answers[q.id]).toBe(draft);
});

test('responsive routes 360,390,768,1440 without horizontal overflow', async ({ page }) => {
  for (const width of [360, 390, 768, 1440]) {
    await page.setViewportSize({ width, height: 950 });
    for (const route of ['home', 'study', 'exam', 'history', 'data']) {
      await page.goto(`./#/${route}`); await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width}/${route}`).toBe(true);
    }
    await page.goto('./#/home'); await page.screenshot({ path: `tmp/qa/home-${width}.png`, fullPage: true });
  }
});

test('quiz navigation and results work at phone widths', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 850 });
  await page.goto('./#/home');
  await page.getByRole('button', { name: 'Mở điều hướng', exact: true }).click();
  await page.getByRole('link', { name: 'Ôn tập', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Chọn một chế độ ôn tập', exact: true })).toBeVisible();
  const a = await startDaily(page);
  for (const width of [360, 390]) {
    await page.setViewportSize({ width, height: 850 });
    await page.getByRole('button', { name: `Đi đến câu ${a.questions.length}`, exact: true }).click();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    await page.screenshot({ path: `tmp/qa/quiz-${width}.png`, fullPage: true });
  }
  await submit(page, a);
  await page.setViewportSize({ width: 360, height: 850 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  await expect(page.getByText('Theo Phase', { exact: true })).toBeVisible();
  await page.screenshot({ path: 'tmp/qa/result-360.png', fullPage: true });
});
