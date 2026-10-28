# Priority duplicate review

Reviewer: priority-independent-review. Date: 2026-10-28.

Scope: all 9 candidate pairs involving priority IDs in the final 1,373-question lexical screen (19 total candidates). Existing-only pairs were not reopened. Content read in full, including answers and learning objectives, rather than deciding by similarity threshold.

| Pair | Decision and rationale |
|---|---|
| activation-sigmoid-value / activation-tanh-value | Keep. Different functions, domains and numerical output; shared input is intentional comparison, explicitly requested in user verification examples. |
| norm-bn-value / norm-ln-value | Keep. Different normalization axes are the core distinction; shared matrix isolates the difference. Column result [[−1,−1],[1,1]] and row result [[−1,1],[−1,1]] independently verified. |
| generation-topk / generation-topp | Keep. Fixed cardinality vs cumulative-mass filtering retain different sets and require different normalization denominators. These are distinct requested concepts, not parameter-only variants. |
| p2-t4-d05-c01 / priority-kalman-innovation | Keep. Old asks gain and posterior mean; new asks innovation, posterior variance and standard deviation. Shared illustrative numbers deliberately extend the update through uncertainty conversion, not repeat its output. |
| generation-topp / generation-boundary | Keep. New boundary item specifically distinguishes ≥ from > and exact equality, which the first example crossing threshold cannot test. No additional number-only top-p variants accepted. |
| norm-ln-value / norm-epsilon | Keep. First tests row axis; second tests zero-variance stabilization and epsilon inside square root. No shared numerical procedure objective beyond normalization family. |
| p2-t4-d12-c02 / priority-clip-inverse | Keep. Old computes a forward command from negative raw velocity change. New infers the entire preimage of a saturated positive command and recognizes loss of information, requiring an inequality rather than a forward numeric result. |
| p2-t4-d06-c02 / p2-t4-d08-priority-d-backproject-depth | Keep. Old applies extrinsic translation and forward projection to a pixel; new inverts projection with known optical-axis depth and distinguishes that depth from Euclidean range. New distractors target depth/range and missing depth multiplication. These are different geometric operations and learning objectives. |
| activation-softmax-value / generation-softmax-temperature | Keep. First normalizes vector logits; second applies positive temperature division and distinguishes T=2 from T=1. Different mathematical control and explicit T>0 condition. |

Semantic duplicates found outside lexical screen were rejected before release: ReAct plan-vs-react r1 duplicated p2-t3-d01-x10; Kalman sensitivity r1 duplicated inverse R/gain relation; EKF r1 duplicated recognition via nonlinear radar/Jacobian; closed-loop reset and explanation r1 duplicated p2-t4-d12-q04. Replacements increase revision and add different objectives (replanning scenario; joint covariance scaling; four-filter matching; bias accumulation vs reset calculation; repeated A/B evaluation design). See corresponding exact-revision reports for decisions.

This report does not claim every conceivable conceptual overlap is absent. Matching/rubric/ordering items may revisit the same topic while testing additional relationships or an explicitly requested new response operation. Unnecessary paraphrases were not approved.
