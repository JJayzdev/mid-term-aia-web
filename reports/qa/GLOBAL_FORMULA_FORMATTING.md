# Global formula formatting — 2026-10-23

The shared renderer now applies to every question, context, answer option, correct answer, explanation and rubric criterion, independent of the calculation flag. Saved snapshots receive the same presentation without modifying their content, grading keys or the published bank.

Supported notation found in the bank includes numeric/letter powers, negative unit exponents, Unicode powers/transposes, named/indexed subscripts (including h_(t-1)), hats/tildes, sigma/mu/kappa, square roots and balanced floor/ceil expressions. Whole identifiers, Vietnamese words, code spans and URLs are preserved. React escapes text instead of interpreting imported HTML.

Audit: all 1,284 questions and 6,992 nonempty question-content fields examined. A notation-pattern scan identified 120 fields in 58 questions, including 34 questions without the calculation flag. Regression tests render every field and verify that raw supported mathematical scripts/functions are gone and non-mathematical identifiers remain intact.

Validation: 58/58 unit tests, TypeScript and production build passed. All 14 existing browser scenarios passed. The added untagged-math/root scenario passed after correcting its test setup to select the new active attempt and reopen submitted results from history after reload. It checks pass^k in Phase 1, roots in Track 4, submitted explanations, saved history and widths 1440/390/360. Desktop and phone screenshots inspected: no horizontal overflow or clipped notation.
