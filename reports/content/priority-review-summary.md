# Independent priority content review

Reviewer: `priority-independent-review`. Date: 2026-10-28.

All **89 current question revisions** in the 13 `priority-*.json` draft batches are approved. No current revision has an unresolved content finding. Earlier rejected revisions remain in the per-batch reports to preserve the author/reviewer/retest history.

The current content cites 130 distinct physical pages from 18 original PDF documents. Original formula and diagram pages were visually inspected, with source hashes checked against the catalog. Eight supplemental primary-source URLs were independently opened and recorded on the exact approved decisions; their slide references are curricular anchors where the slide does not supply the supplemental formula.

Review covered the question, all answer choices, explanation, source references, metadata, and complete formula cards. All numerical answers and card examples were recomputed independently. Conditions include normalization axes and inference statistics, variance versus standard deviation, token-filter boundary rules, matrix dimensions, geometric camera assumptions, explicit rounding, independent trials, and saturation. The 37 formula cards include connected formulas beyond each question's numerical objective; this does not mean every formula has a separate numerical exercise.

| Batch | Approved current revisions |
|---|---:|
| ReAct | 8 |
| Generation | 8 |
| Kalman | 10 |
| Activations | 9 |
| Normalization | 7 |
| Sensors | 7 |
| Closed loop | 5 |
| Pipelines | 7 |
| Extra graph / normalization / control | 3 |
| Neural calculations | 6 |
| Metrics calculations | 5 |
| Geometry calculations | 6 |
| Dynamics / scaling / evaluation calculations | 8 |
| **Total** | **89** |

The 89 additions contain 49 calculation questions, 17 matching questions, 10 ordering questions, 11 scenarios, and 2 rubric-scored short answers (calculation is a separate flag). Matching mappings were checked for complete, unique targets where reuse is disabled. Ordering review required grouping steps with no necessary internal order and accepting the valid filter/sort alternative in NMS. Activation graph equations and accessible descriptions match the intended functions; browser rendering validation belongs to the root implementation review.

Semantic duplicates were rejected and replaced before approval, including the initial ReAct distinction, inverse covariance sensitivity, EKF recognition, and closed-loop causality variants. The final lexical screen covers 1,373 questions with 19 candidate pairs. All nine pairs involving a priority question have documented distinct learning objectives in `priority-duplicate-review.md`. Existing-only pairs were not reopened.

Evidence is recorded in `priority-review-*.json`; arithmetic and original-page render evidence is under `tmp/priority-review/`. These approvals cover content at the recorded revisions, not a later author change or the deployed UI. The release process must continue enforcing revision and supplemental-URL matches.
