import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import type { Attempt, AttemptQuestion, Question, QuestionBank } from '../../src/domain/types';

async function attempts(page: Page): Promise<Attempt[]> {
  return page.evaluate(() => new Promise((resolve, reject) => {
    const open = indexedDB.open('aia-study-local', 1);
    open.onerror = () => reject(open.error);
    open.onsuccess = () => {
      const db = open.result;
      const request = db.transaction('attempts').objectStore('attempts').getAll();
      request.onsuccess = () => { resolve(request.result); db.close(); };
      request.onerror = () => reject(request.error);
    };
  }));
}
async function current(page: Page, id?: string) {
  const rows = await attempts(page);
  const row = rows.find(a => id ? a.id === id : a.status === 'in_progress');
  expect(row).toBeTruthy();
  return row!;
}
async function bank(page: Page): Promise<QuestionBank> {
  await page.goto('./#/study');
  await expect(page.getByRole('heading', { name: 'Chọn một chế độ ôn tập', exact: true })).toBeVisible();
  const response = await page.request.get(new URL('./data/bank.json', page.url()).href);
  expect(response.ok()).toBe(true);
  return response.json();
}
async function launchQuestion(page: Page, q: Question) {
  await page.goto('./#/study');
  await page.getByRole('combobox', { name: 'Phase', exact: true }).selectOption(String(q.phase));
  await page.getByRole('combobox', { name: 'Ngày học', exact: true }).selectOption(q.day!);
  await page.getByRole('combobox', { name: 'Dạng bài', exact: true }).selectOption(q.answer_format);
  const count = page.getByRole('combobox', { name: 'Số câu mục tiêu', exact: true });
  const largest = await count.locator('option').last().getAttribute('value');
  if (largest) await count.selectOption(largest);
  await page.getByRole('button', { name: 'Bắt đầu lượt học', exact: true }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const attempt = await current(page);
  const index = attempt.questions.findIndex(item => item.question.id === q.id);
  expect(index, 'Narrow day/type pool must include the chosen published question').toBeGreaterThanOrEqual(0);
  await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
  return { attempt, index, item: attempt.questions[index] };
}
async function submit(page: Page, attempt: Attempt) {
  await page.getByRole('button', { name: `Đi đến câu ${attempt.questions.length}`, exact: true }).click();
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Nộp bài', exact: true }).last().click();
  await expect(page.locator('.result-summary')).toBeVisible();
}
async function finishMatching(page: Page, attempt: Attempt, item: AttemptQuestion) {
  const solution = item.question.correct_answer as Record<string, string>;
  for (const id of item.matchingOrder!) {
    await page.locator(`select[id="match-${item.question.id}-${id}"]`).selectOption(solution[id]);
    await expect.poll(async () => (await current(page, attempt.id)).answers[item.question.id]).toMatchObject({ [id]: solution[id] });
  }
}
async function arrange(page: Page, attempt: Attempt, item: AttemptQuestion, target: string[]) {
  const saved = (await current(page, attempt.id)).answers[item.question.id];
  const order = Array.isArray(saved) && saved.length ? [...saved] : [...item.optionOrder];
  for (let desired = 0; desired < target.length; desired++) {
    let index = order.indexOf(target[desired]);
    while (index > desired) {
      await page.getByRole('button', { name: `Đưa bước ${index + 1} lên`, exact: true }).click();
      [order[index - 1], order[index]] = [order[index], order[index - 1]];
      await expect.poll(async () => (await current(page, attempt.id)).answers[item.question.id]).toEqual(order);
      index--;
    }
  }
  await page.getByRole('button', { name: 'Xác nhận thứ tự này', exact: true }).click();
  await expect.poll(async () => (await current(page, attempt.id)).answers[item.question.id]).toEqual(target);
}
function kind(q: Question) {
  if (q.answer_format === 'matching' || q.answer_format === 'ordering') return q.answer_format;
  return q.calculation ? 'calculation' : q.question_type === 'scenario' ? 'scenario' : 'concept';
}
async function noOverflow(page: Page) {
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
}

test.beforeEach(async ({ page }) => {
  page.on('pageerror', error => { throw error; });
  page.on('console', message => { if (message.type() === 'error') throw new Error(message.text()); });
});

test('focus preset covers seven priority groups and varied types in fourteen stable slots', async ({ page }) => {
  const content = await bank(page);
  expect(new Set(content.questions.flatMap(q => q.focus_topics ?? [])).size).toBe(7);
  await page.getByRole('button', { name: /^Ôn trọng tâm Bảy nhóm/ }).click();
  await page.getByRole('combobox', { name: 'Số câu mục tiêu', exact: true }).selectOption('14');
  await expect(page.locator('.focus-note')).toContainText('không phải đề thi chính thức');
  await page.getByRole('button', { name: 'Bắt đầu lượt học', exact: true }).click();
  await expect(page.locator('.question-card h1')).toBeVisible();
  const attempt = await current(page);
  expect(attempt.mode).toBe('focus');
  expect(attempt.questions).toHaveLength(14);
  expect(new Set(attempt.questions.map(i => i.question.id)).size).toBe(14);
  expect(new Set(attempt.questions.flatMap(i => i.question.focus_topics ?? [])).size).toBe(7);
  expect(new Set(attempt.questions.map(i => kind(i.question))).size).toBe(5);
  expect(attempt.questions.every(i => i.question.status === 'approved')).toBe(true);
  await page.reload();
  await expect(page.locator('.question-card h1')).toBeVisible();
  expect((await current(page)).questions).toEqual(attempt.questions);
});

test('matching uses stable IDs, preserves partial maps and column order, then explains each pair', async ({ page }) => {
  const content = await bank(page);
  const candidates = content.questions.filter(q => q.answer_format === 'matching' && !q.matching_reuse && (q.matching_items?.length ?? 0) >= 3);
  const q = candidates.find(q => q.matching_items?.some(row => row.graph)) ?? candidates[0];
  expect(q).toBeTruthy();
  const { attempt, index, item } = await launchQuestion(page, q);
  const left = item.matchingOrder![0];
  const right = (q.correct_answer as Record<string, string>)[left];
  await expect(page.locator('.pair-feedback')).toHaveCount(0);
  await expect(page.locator('.activation-plot')).toHaveCount(q.matching_items!.filter(row => row.graph).length);
  await page.locator(`select[id="match-${q.id}-${left}"]`).selectOption(right);
  await expect.poll(async () => (await current(page)).answers[q.id]).toEqual({ [left]: right });
  const other = item.matchingOrder![1];
  await expect(page.locator(`select[id="match-${q.id}-${other}"] option[value="${right}"]`)).toBeDisabled();
  for (const width of [1440, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await noOverflow(page);
    await page.screenshot({ path: `tmp/qa/priority-matching-${width}.png`, fullPage: true, animations: 'disabled' });
  }
  await page.reload();
  await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
  const restored = await current(page);
  expect(restored.questions).toEqual(attempt.questions);
  expect(restored.answers[q.id]).toEqual({ [left]: right });
  expect(await page.locator('.matching-row select').evaluateAll(elements => elements.map(el => (el as HTMLSelectElement).value))).toEqual(item.matchingOrder!.map(id => id === left ? right : ''));
  await submit(page, attempt);
  await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
  await expect(page.locator('.pair-correct')).toHaveCount(1);
  await expect(page.locator('.pair-wrong')).toHaveCount(q.matching_items!.length - 1);
  await expect(page.locator('.pair-feedback')).toHaveCount(q.matching_items!.length);
  expect((await current(page, attempt.id)).score?.totalPoints).toBe(0);
  for (const row of q.matching_items!.filter(row => row.explanation)) {
    const feedback = page.locator('.matching-row').filter({ has: page.locator(`select[id="match-${q.id}-${row.id}"]`) }).locator('.pair-feedback p');
    await expect(feedback).toHaveCount(2);
    await expect(feedback.last()).not.toHaveText('');
  }
});

test('ordering remains blank until confirmed, supports keyboard moves and valid alternative sequences', async ({ page }) => {
  const content = await bank(page);
  const q = content.questions.find(q => q.answer_format === 'ordering' && q.accepted_orders?.length) ?? content.questions.find(q => q.answer_format === 'ordering');
  expect(q).toBeTruthy();
  const { attempt, item, index } = await launchQuestion(page, q!);
  expect((await current(page)).answers[q!.id]).toBeUndefined();
  await expect(page.locator('.ordering-confirm')).toContainText('Chưa trả lời');
  await expect(page.locator('.order-feedback')).toHaveCount(0);
  const down = page.getByRole('button', { name: 'Đưa bước 1 xuống', exact: true });
  await down.focus(); await expect(down).toBeFocused(); await page.keyboard.press('Enter');
  const moved = [...item.optionOrder]; [moved[0], moved[1]] = [moved[1], moved[0]];
  await expect.poll(async () => (await current(page)).answers[q!.id]).toEqual(moved);
  await page.getByRole('button', { name: 'Xóa trả lời', exact: true }).click();
  await expect.poll(async () => (await current(page)).answers[q!.id]).toEqual([]);
  await expect(page.locator('.session-progress')).toContainText('0 đã trả lời');
  const target = q!.accepted_orders?.[0] ?? q!.correct_answer as string[];
  await arrange(page, attempt, item, target);
  await page.reload();
  await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
  expect((await current(page)).answers[q!.id]).toEqual(target);
  for (const width of [1440, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 }); await noOverflow(page);
    await page.screenshot({ path: `tmp/qa/priority-ordering-${width}.png`, fullPage: true, animations: 'disabled' });
  }
  await submit(page, attempt);
  await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
  await expect(page.locator('.order-feedback>b')).toHaveText('Thứ tự đúng');
  await expect(page.locator('.order-feedback h3')).toHaveCount(1 + (q!.accepted_orders?.length ?? 0));
  expect((await current(page, attempt.id)).score?.totalPoints).toBe(item.points);
});

test('submitted matching and ordering round-trip through an actual downloaded backup', async ({ page, browser }) => {
  const content = await bank(page);
  for (const format of ['matching', 'ordering'] as const) {
    const q = content.questions.find(q => q.answer_format === format)!;
    expect(q).toBeTruthy();
    const { attempt, item } = await launchQuestion(page, q);
    if (format === 'matching') await finishMatching(page, attempt, item);
    else await arrange(page, attempt, item, q.accepted_orders?.[0] ?? q.correct_answer as string[]);
    await submit(page, attempt);
    await page.getByRole('button', { name: 'Xem lịch sử', exact: true }).click();
  }
  const before = await attempts(page);
  await page.goto('./#/data');
  const downloading = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Tải bản sao lưu', exact: true }).click();
  const path = await (await downloading).path(); expect(path).toBeTruthy();
  const backup = JSON.parse(fs.readFileSync(path!, 'utf8'));
  expect(backup.attempts).toHaveLength(2);
  const other = await browser.newContext();
  try {
    const restored = await other.newPage();
    await restored.goto(new URL('./#/data', page.url()).href);
    await restored.locator('input[type=file]').setInputFiles(path!);
    await restored.getByRole('button', { name: 'Khôi phục dữ liệu', exact: true }).click();
    await expect.poll(async () => (await attempts(restored)).length).toBe(2);
    const after = await attempts(restored);
    for (const old of before) {
      const saved = after.find(a => a.id === old.id)!;
      expect(saved.questions).toEqual(old.questions);
      expect(saved.answers).toEqual(old.answers);
      expect(saved.score).toEqual(old.score);
    }
    await restored.goto(new URL('./#/history', page.url()).href);
    await restored.getByRole('button', { name: 'Xem lại', exact: true }).first().click();
    await expect(restored.locator('.result-summary')).toBeVisible();
  } finally { await other.close(); }
});

test('formula library filters reviewed cards, shows external provenance and fits phone screens', async ({ page }) => {
  const content = await bank(page);
  const cards = content.questions.filter(q => q.formula_reference);
  expect(cards.length).toBeGreaterThan(0);
  await page.goto('./#/formulas');
  await expect(page.locator('.formula-card')).toHaveCount(cards.length);
  // Inspect every formula, including long grouped equations, at phone width.
  await page.setViewportSize({ width: 360, height: 1000 });
  await noOverflow(page);
  expect(await page.locator('.formula-expression').evaluateAll(nodes => nodes.filter(node => node.scrollWidth > node.clientWidth + 1).map(node => node.textContent))).toEqual([]);
  const longest = [...cards].sort((a, b) => b.formula_reference!.formula.length - a.formula_reference!.formula.length)[0];
  await page.getByRole('searchbox', { name: 'Tìm công thức', exact: true }).fill(longest.id);
  await expect(page.locator('.formula-card')).toHaveCount(1);
  await page.screenshot({ path: 'tmp/qa/priority-formulas-long-360.png', fullPage: true, animations: 'disabled' });
  const q = cards.find(q => q.supplemental_sources?.length) ?? cards[0];
  await page.getByRole('searchbox', { name: 'Tìm công thức', exact: true }).fill(q.id);
  await expect(page.locator('.formula-card')).toHaveCount(1);
  await expect(page.locator('.formula-card h2')).toHaveText(q.formula_reference!.title);
  await expect(page.locator('.formula-card dt')).toHaveText(['Ký hiệu', 'Điều kiện áp dụng', 'Ví dụ thay số', 'Lỗi thường gặp']);
  if (q.supplemental_sources?.length) {
    await expect(page.locator('.question-sources')).toContainText('Bổ sung ngoài slide:');
    for (const source of q.supplemental_sources) await expect(page.getByRole('link', { name: source.title, exact: true })).toHaveAttribute('href', source.url);
  }
  for (const width of [1440, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 }); await noOverflow(page);
    await page.screenshot({ path: `tmp/qa/priority-formulas-${width}.png`, fullPage: true, animations: 'disabled' });
  }
  await page.getByRole('searchbox', { name: 'Tìm công thức', exact: true }).fill('');
  await page.getByRole('combobox', { name: 'Nhóm trọng tâm', exact: true }).selectOption('kalman');
  await expect(page.locator('.formula-card')).toHaveCount(cards.filter(q => q.focus_topics?.includes('kalman')).length);
  await page.getByRole('combobox', { name: 'Phạm vi tài liệu', exact: true }).selectOption('p1');
  await expect(page.locator('.formula-card')).toHaveCount(cards.filter(q => q.focus_topics?.includes('kalman') && q.phase === 1).length);
  if (!q.supplemental_sources?.length) {
    const supplemented = content.questions.find(q => q.supplemental_sources?.length)!;
    expect(supplemented, 'New bank must explicitly label supplemental primary references').toBeTruthy();
    // Source display shares the same component as formula cards; visit this source's quiz below via all-type daily study.
    await page.goto('./#/study');
    await page.getByRole('combobox', { name: 'Phase', exact: true }).selectOption(String(supplemented.phase));
    await page.getByRole('combobox', { name: 'Ngày học', exact: true }).selectOption(supplemented.day!);
    await page.getByRole('combobox', { name: 'Nhóm trọng tâm', exact: true }).selectOption(supplemented.focus_topics![0]);
    const count = page.getByRole('combobox', { name: 'Số câu mục tiêu', exact: true });
    const largest = await count.locator('option').last().getAttribute('value');
    if (largest) await count.selectOption(largest);
    await page.getByRole('button', { name: 'Bắt đầu lượt học', exact: true }).click();
    const attempt = await current(page);
    const index = attempt.questions.findIndex(i => i.question.supplemental_sources?.length);
    expect(index).toBeGreaterThanOrEqual(0);
    await submit(page, attempt);
    await page.getByRole('button', { name: `Đi đến câu ${index + 1}`, exact: true }).click();
    await expect(page.locator('.question-sources')).toContainText('Bổ sung ngoài slide:');
  }
});

test('changing Track or day resets a previously selected topic', async ({ page }) => {
  const content = await bank(page);
  const t1 = content.questions.find(q => q.track === 1)!;
  await page.getByRole('button', { name: /^Theo Track Tập trung/ }).click();
  await page.getByRole('combobox', { name: 'Chủ đề', exact: true }).selectOption(t1.topic);
  await page.getByRole('combobox', { name: 'Track', exact: true }).selectOption('4');
  await expect(page.getByRole('combobox', { name: 'Chủ đề', exact: true })).toHaveValue('');
  await expect(page.getByRole('button', { name: 'Bắt đầu lượt học', exact: true })).toBeEnabled();
  await page.getByRole('button', { name: /^Ôn tập hôm nay Một lượt/ }).click();
  const first = content.questions.find(q => q.phase === 1)!;
  const second = content.questions.find(q => q.phase === 1 && q.day !== first.day)!;
  await page.getByRole('combobox', { name: 'Ngày học', exact: true }).selectOption(first.day!);
  await page.getByRole('combobox', { name: 'Chủ đề', exact: true }).selectOption(first.topic);
  await page.getByRole('combobox', { name: 'Ngày học', exact: true }).selectOption(second.day!);
  await expect(page.getByRole('combobox', { name: 'Chủ đề', exact: true })).toHaveValue('');
  await expect(page.getByRole('button', { name: 'Bắt đầu lượt học', exact: true })).toBeEnabled();
});
