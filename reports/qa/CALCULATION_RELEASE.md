# Track 4 calculation release

Requested 2026-10-23 (Asia/Bangkok): numerical questions suitable for practice with a Casio calculator. The existing 1,260-question release and desktop reading scale are preserved.

## Behavior

- Optional `calculation` metadata identifies numerical practice without invalidating older question/attempt snapshots.
- The study page's “Dạng bài → Chỉ câu tính toán” filter combines with the selected Phase, Track, day, topic, difficulty and review list.
- Each new exam reserves two of its five Track 4 objective slots for approved calculations, then samples the remaining three without replacement. There can be more than two calculations. Count remains 60, Phase count 36/24, Phase points 60/40, and rubric points 10/100. A shortage is reported instead of silently substituting theory.
- This two-question minimum is an application practice setting, not a claim about the official exam blueprint.

## Content and validation

Bank `2026.10.22-28fda6d871f4` contains 1,284 approved questions, 24 newly tagged calculations, no omissions, and at least20 questions for every63 PDFs (22 for each Track4 PDF). The new24 were reviewed independently against26 physical pages across12 PDFs and every numerical answer was recomputed. See `reports/content/expand-root-calculation.json/.md`. Total released citations cover1,079 distinct physical pages, not all concepts in3,589 pages.

Root ran the final integrated revision:

- `python scripts/content/validate_drafts.py`: PASS. Five pre-existing A004 pending drafts had source verification incorrectly marked verified; their draft-only marker was restored to needs_review. No stem, answer, citation, revision or published content changed from that metadata repair.
- `python scripts/validate_release.py --verify-sources --min-per-document 20 --standalone-stems`: PASS, errors empty. Evidence `tmp/qa/calculation-release-validation.json`.
- `python -m unittest discover -s scripts/qa -p test_release_gate.py -v`:10/10 PASS. Added calculation-shortage fixture and valid percentage-rounding fixture. The latter exposed and fixed a lexical false positive: “theo phần trăm” is a unit instruction, while source-dependent “theo phần…” remains blocked. Evidence `tmp/qa/calculation-gate-tests.txt`.
- `npm test`:54/54 PASS, including filtering, shortage handling and100 surplus-pool seeds; `npm run build` includes TypeScript checking and Vite production build, PASS. Evidence `tmp/qa/calculation-unit-tests.txt`, `calculation-build.txt`. Artifacts `index-DBAX_54K.js`, `index-CW8pxNbG.css`.
- Production preview at127.0.0.1:5176:13/13 Playwright tests PASS in24.9s, no skipped/flaky cases. Includes numerical-only Track4 practice and reload, both exam paths with calculation minimum, exact quotas/points, deadlines, persistence/error recovery, backup and responsive routes. Evidence `tmp/qa/calculation-preview-browser-results.json`.
- Independent code/metadata reviews passed in `CALCULATION_CODE_REVIEW.md` and `CALCULATION_RELEASE_REVIEW.md`.

Deployment verification is pending and will be appended after the public site updates. Validation used Windows, Node24.14.1, npm11.11 and installed Chrome. Existing historical sessions retain their stored question snapshots.
