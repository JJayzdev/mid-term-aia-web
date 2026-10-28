import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['browser.spec.ts', 'priority.spec.ts'], timeout: 45000,
  workers: 1, reporter: [['list'], ['json', { outputFile: '../../tmp/qa/browser-results.json' }]],
  outputDir: '../../tmp/qa/browser-artifacts',
  use: { baseURL: process.env.AIA_BASE_URL || 'http://127.0.0.1:5175/', channel: 'chrome', headless: true, viewport: { width: 1440, height: 1000 }, screenshot: 'only-on-failure', trace: 'retain-on-failure' },
});
