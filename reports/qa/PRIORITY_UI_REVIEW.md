# Independent implementation review — 2026-10-28

Reviewer: practice_engine (not the UI author). Scope: `StructuredQuestion.tsx`, `QuizSession.tsx`, `FormulaLibrary.tsx`, `QuestionSources.tsx`, `practiceLabels.ts`, `App.tsx` changes and appended CSS. Read-only code review; browser behavior remains subject to root's integration tests.

## Findings sent to root

1. **P2 — Reset stale topic when changing its parent scope.** In the study filter, Track and day controls retain the previous selected `topic` while their option lists no longer contain it. Reproduce by choosing a topic in Track 1 and then choosing Track 4: selection remains in state, silently filtering the new track to zero questions. Reset topic on Track/day changes. Phase/mixed Phase and mode changes already reset it.
2. **Minor — Objective count wording.** Results count matching and ordering with all automatically graded questions, but the summary labels them “câu trắc nghiệm”. Use a label covering all objective formats, e.g. “câu chấm tự động”. No score discrepancy.
3. **Optional clarity — Formula library load/error state.** During content loading/failure it currently shows a zero-card library with no indication that loading failed. Pass the existing content status into this route if desired.

## Reviewed behavior

- Matching presents shuffled left and right snapshot orders, saves ID maps, allows incomplete answers, prevents repeated targets for one-to-one exercises, permits reuse when explicitly enabled, and displays per-pair result/explanation only after submission.
- Ordering requires explicit interaction or confirmation before recording an answer. Clearing resets to the persisted initial shuffle. Buttons provide keyboard/mobile interaction. Submission lists every accepted sequence; exact sequence grading is handled by the independently tested engine.
- Shared persistence retains failed answer payloads, reports failure, blocks navigation/submission and offers retry. Matching/ordering controls disable during pending writes and when submitted/read-only. Answer progress treats empty arrays/maps as blank.
- Formula cards use the shared renderer and reviewed bank fields; supplemental source links remain explicitly outside-slide sources. Link text is React-escaped; schema permits only HTTPS URLs and new-window links use noreferrer.
- No blocking new correctness issue identified beyond the stale topic filter finding. No UI source changes made by this reviewer.

## Fix verification

Re-read the integrated implementation on 2026-10-28: Track/day changes now reset `topic`; objective result counts use “câu khách quan”; the formula route passes loading/error state and suppresses a misleading empty-state message while loading or on failure. These resolve all three findings. The new browser suite includes the Track/day regression and formula-library coverage; runtime results are recorded separately after the released bank is available.

## Initial browser integration

The six tests in `scripts/qa/priority.spec.ts` passed against the 1,335-question integration bank on local preview port 5180 (12.7 seconds). They use released metadata and normal UI interactions, with read-only IndexedDB inspection; no draft bank injection. Coverage: fourteen-slot focus preset with seven groups/five practice kinds, partial matching grading and stable shuffled columns after reload, keyboard ordering and blank/confirm semantics, downloaded backup restore in a fresh browser context, formula search/filters and labeled supplemental source links, and stale-topic regression. Screenshots cover 360, 390 and 1440 pixels under `tmp/qa/priority-*.png`; formula capture was repeated with CSS animations disabled to avoid recording the sidebar's resize transition. Visual inspection of the 360-pixel matching and formula screens found readable, contained content. Final content build still requires the final bank run.

Read-only review of the cross-document provenance change: at least one reference remains anchored to the assigned topic, while all referenced documents retain catalog/hash/page/verification checks. Exam selection received an additional direct-call guard for every referenced document/hash/integer page; its regression verifies that valid supporting references preserve IDs/points and that corrupted references block selection.
