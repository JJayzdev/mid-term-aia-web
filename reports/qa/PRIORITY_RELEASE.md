# Priority practice release — 2026-10-28

Bank: `2026.10.28-04176e865b81`. All 1,373 questions pass release validation; 89 additions have independent approval at their current revision. No pending/rejected question was promoted. All 1,284 previously published question objects remain byte-equivalent after JSON parsing.

## Scope

- Matching: independently shuffled columns, stable IDs, one-to-one by default, opt-in target reuse, partial autosave, individual correct/incorrect feedback. Keyboard and mobile selects require no drag gesture.
- Ordering: shuffled steps, keyboard-accessible up/down buttons, explicit confirmation, reset to unanswered, and accepted alternative complete orders. Independent stages are grouped by the content author/reviewer.
- Both formats use all-or-nothing grading; partial or wrong work earns zero, with no negative score. Existing scoring policies remain unchanged.
- Seven focus groups, five practice-kind filters, balanced **Ôn trọng tâm** preset, and 37 searchable formula cards. Graph matching renders actual sigmoid, tanh and ReLU curves with equivalent text descriptions.
- Math rendering covers all question/option/explanation/rubric/matching/formula-card fields: powers, indices, Greek symbols, grouped sums, roots and floor/ceiling. Code spans, URLs and API fields such as `max_tokens` and `drop_last` remain literal.
- Additive schema and IndexedDB compatibility retain old attempts and backups. Submitted snapshots preserve their original content; updated question banks do not rewrite history.
- Exam configuration remains 60 questions, 90 minutes, 36 Phase 1 / 24 Phase 2, 60/40 points, 54 objective / 6 rubric, and at least two Track 4 calculations. Matching/ordering are practice formats and do not enter this blueprint.

## Content and provenance

89 additions: 58 single-choice, 17 matching, 10 ordering, two multiple-choice, two rubric. 49 additions are calculation questions; the complete bank has 73 calculations. Seven priority groups and all nine requested pipeline families are covered. The 14 expanded numerical groups reuse existing questions where appropriate and add distinct missing objectives plus grouped formula cards.

Every one of the 63 PDFs retains at least 20 questions. The bank cites 1,129 distinct physical pages. Source hashes, page ranges, curricular anchors, author/reviewer separation, exact revisions and independently verified supplemental URLs are enforced. Supporting references may come from other catalog documents, but at least one verified reference must belong to the assigned topic.

See `reports/content/PRIORITY_AUTHOR_COVERAGE.md`, `priority-review-summary.md`, per-batch review JSON, and `priority-duplicate-review.md`. The final duplicate screen checks 1,373 questions / 19 candidates; all nine pairs involving the additions were independently adjudicated. No unresolved content findings remain. Coverage does not imply a separate exercise for every equation or coverage of every concept in all 3,589 PDF pages.

## Verification

- Draft validation and release validation with source hashes, minimum 20 questions/PDF and standalone stems: passed, zero errors, zero omitted drafts.
- Vitest: **76/76 passed** across ten files. Includes grading, exact quotas, source provenance, persistence, restore, failed-write retry and rendering of every published text field.
- Python release-gate fixtures: **15/15 passed**. Rejects self-approval, stale/revoked revisions, incomplete page/external-source review, invalid mappings/orders and missing curricular anchors.
- TypeScript check and production Vite build: passed. JS `index-Bx7xb9gT.js`, CSS `index-Dz8Ovz_r.css`.
- Chrome browser on the final bank: **21/21 passed** (1.3 minutes). Covers real release data, focus balance, all nine pipeline families via reviewed content, matching/reordering interaction, stable shuffled IDs, partial reload, alternative NMS order, blank submission, downloaded-backup restore, expired exam recovery, two-tab ownership, write failures, topic filters, and responsive routes at 360/390/768/1440 px. Evidence: `tmp/qa/priority-final-browser.json`.
- Additional formula browser check: passed. All 37 expressions fit their containers at 360 px. Visually inspected the longest grouped optimizer card on a phone, activation graph matching at 390 px, and formula sources on desktop. Screenshots: `tmp/qa/priority-*.png`. No horizontal overflow or clipped formula found.

## Deployment

Published through the existing authorized free GitHub Pages process. Source commit `cc1fcbb2306f2efc63008139943e44d24586c4ad`; Pages commit `8842957c07e607f9bdcab9c658a9d9949feabde8`. GitHub reports `built`, no deployment error.

Production: https://jjayzdev.github.io/mid-term-aia-web/

The public bank was fetched and compared with the tested local JSON: exact equality, 1,373 questions, version `2026.10.28-04176e865b81`. The public HTML references the tested JS asset. All **21/21 browser cases also passed on the public URL** (1.3 minutes), including the strengthened check of every formula at 360 px. Live evidence: `tmp/qa/priority-live-browser.json`. This final documentation update does not change the deployed application.

## Limits

Supplemental knowledge is explicitly labeled in the UI and backed by primary references. Exam recollections only set practice priorities; no official question or frequency claim is made. Calculation answers use the existing choice-based format, with the stated units/rounding; free numeric input was not added. Original offline/local-storage limitations remain as documented in README.
