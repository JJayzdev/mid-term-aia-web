# Priority practice engine — 2026-10-28

Owner: practice_engine. This report covers implementation checks, not semantic approval of learning content.

## Data and grading contract

- Additive schema 1.0.0 fields preserve older banks and saved snapshots. New answer formats/question types: `matching`, `ordering`. Both require shuffled options. Matching stores left items separately; learner answers are maps from left IDs to right IDs. Default is one-to-one; `matching_reuse: true` explicitly permits shared targets. Each left item may include its own explanation.
- Ordering stores an ordered ID array. `correct_answer` and every optional `accepted_orders` entry must be complete distinct permutations. An empty or partial learner sequence is permitted while working but earns zero on submission.
- Both formats earn the full question score only for a complete exact answer, otherwise zero. No negative or fractional score. Accepted alternative sequences are equally correct. Existing scoring policies are unchanged.
- `matchingOrder` snapshots the independently shuffled left column; `optionOrder` snapshots the right column or pipeline steps. Saved answers and both orders survive reload and backup/restore. Backup validation rejects missing/duplicate/foreign IDs, malformed answers and inconsistent scores.
- `focus_topics` uses seven agreed topic keys. `formula_reference` carries six reviewed text fields as part of the same question revision.
- Optional `supplemental_sources` declares primary references outside the slides: title, HTTPS URL, ISO access date and explanatory note. The schema permits 1–10 sources; runtime and Python checks reject duplicate URLs. Exact-revision decisions must list all external URLs in `supplemental_urls` before promotion/release. The curricular PDF anchor remains required.

## Selection and compatibility

`practicePool` accepts `practiceKind`, `focusTopic`, `focusOnly` and all prior filters, including `calculationOnly`. `practiceKind(question)` consistently classifies matching, ordering, calculation, scenario or concept. `selectPractice(..., 'focus', ...)` cycles through least-used eligible topics, then least-used kinds within the chosen topic. It is deterministic for a seed, uses only independently approved records, and does not repeat questions or fill from outside the filtered pool.

The existing exam selector explicitly excludes matching and ordering. Its 60-question quota, 36/24 Phase split, score allocation and minimum two Track 4 numerical questions remain unchanged. New metadata does not alter previously stored attempts.

## Validation evidence

- Vitest domain grading/selection/validation: 38 tests passed. Includes incomplete/wrong/extra mapping, reuse opt-in, valid alternate order, malformed answer keys, stable shuffled columns, unchanged exam selection, and 20-seed focus coverage/type balance.
- IndexedDB tests: 18 tests passed. New cases verify partial/cleared matching, fresh-connection persistence, independent column order, exact grading, focus backup round-trip and rejection of corrupted matching/order snapshots.
- Supplemental provenance extension: practice-format tests 10/10 passed, including invalid HTTP/script/malformed URLs, invalid dates and duplicate URL rejection. Python release-gate tests 14/14 passed, including independent external URL review coverage, complete mapping/permutation checks and explicit target reuse.
- Draft validator passed against the existing bank plus the first eight new ReAct drafts; this is structural validation only. Later authored batches still require root's integrated validation and independent review.
- Final TypeScript check passed after correcting a test-only inferred union type. Root will run the final integrated build and browser checks.

No commit or deployment performed by this agent.
