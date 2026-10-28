# Priority practice: author coverage and handoff

Author: `priority-question-engineer`. Date: 2026-10-28. Scope: new `priority-*.json` only; existing banks are retained. Draft status remains `pending_review`; publication is controlled by independent exact-revision decisions, never by this report. The reviewer is `priority-independent-review`.

My contribution is **81 questions, 29 formula cards, 41 calculation questions**, all independently approved at their current revisions. Formats: 50 single-choice, 17 matching, 10 ordering, 2 multiple-choice, 2 rubric. Scenario is an additional question type, not an additional grading format. The separate `priority-dynamics-author` contribution adds **8 questions, 8 cards, 8 calculations**, bringing the authored update to **89 questions, 37 cards, 49 calculations**. Its final approval is tracked in the independent dynamics review artifact.

No slide-derived taxonomy was moved into Track 4 for preset convenience. Generation stays Phase 1 Day 1, ReAct Phase 1 Day 3, Plan–Act–Verify Phase 2 Track 3 Day 1, RAG Phase 1 Days 7/8. `focus_topics` adds cross-topic practice grouping without replacing those assignments.

## B: every requested priority area

IDs below are exact. A card uses the **same ID as its parent question**. Existing IDs without `priority` are retained, not reauthored. An item can cover a concept in its explanation/card as well as its stem; this table does not claim one new numerical exercise for every listed formula.

| Requirement | Questions / cards carrying coverage |
|---|---|
| ReAct expansion; Thought/Action/Observation roles; distinguish React UI library | `p1-d03-priority-react-stages` (matching and explanation) |
| Thought → Action → Observation → continue/Final; concrete tool result and failure | `p1-d03-priority-react-loop`, `p1-d03-priority-react-tool-error` |
| ReAct vs plan-then-execute vs function calling; FC is a mechanism usable inside ReAct | `p1-d03-priority-react-native`, `p1-d03-priority-react-explain`; retained `p1-d03-x09`, `p1-d03-x10` |
| Dependency order and termination; replan after wrong objective | `p1-d03-priority-react-dependent-tools`, `p1-d03-priority-react-stop`, `p2-t3-d01-priority-plan-react` |
| Temperature, top-k, top-p, output budget, context window and API differences | `p1-d01-priority-generation-parameters`, `p1-d01-priority-generation-budget`; parameter explanation explicitly rejects universal API behavior |
| A=.40/B=.30/C=.15/D=.10/E=.05 sampling and renormalization | `p1-d01-priority-generation-topk` card; `p1-d01-priority-generation-topp` |
| Smallest prefix mass ≥p including exact equality | `p1-d01-priority-generation-boundary` |
| softmax(z/T), T>0, do not substitute T=0 | `p1-d01-priority-generation-softmax-temperature` card |
| Sampling top-k vs retrieval top-k; low temperature not truth/reproducibility guarantee | `p1-d01-priority-generation-vs-retrieval`, `p1-d01-priority-generation-truth` |
| Scalar prediction before gain; state, innovation, covariance, standard deviation | `p2-t4-d05-priority-kalman-full-predict` card; `p2-t4-d05-priority-kalman-innovation`, `p2-t4-d05-priority-kalman-std` |
| Given check x_pred20,P9,z26,R3 → K.75,x24.5,P2.25,sigma1.5 | retained `p2-t4-d05-c01` for K/state; new `p2-t4-d05-priority-kalman-innovation` for residual/covariance/std |
| x/P/Q/R/K/F/H meanings | `p2-t4-d05-priority-kalman-symbols`, `p2-t4-d05-priority-kalman-matrix` |
| Full matrix F/B/u/P/Q/H/S/K/update | `p2-t4-d05-priority-kalman-control` full card and controlled prediction; `p2-t4-d05-priority-kalman-matrix-predict` covariance calculation |
| Gain sensitivity with other quantity fixed; equal scaling is a different case | retained `p2-t4-d05-x09`; scalar gain card; `p2-t4-d05-priority-kalman-sensitivity` tests joint scaling without false monotonic conclusion |
| Variance vs std; Gaussian independence/inverse variance | `p2-t4-d05-priority-kalman-std`, `p2-t4-d05-priority-kalman-gaussian-mean` card; retained `p2-t4-d05-c02`, `p2-t4-d05-x15` correlated-source caution |
| KF/EKF Jacobian/UKF/particle distinctions | `p2-t4-d05-priority-kalman-ekf`; retained `p2-t4-d05-q03`, `p2-t4-d05-q04` |
| Camera semantics/light, LiDAR geometry/weather/sparsity, radar range/radial Doppler/multipath | `p2-t4-d04-priority-sensor-strengths`, `p2-t4-d04-priority-sensor-weather-checks` |
| No sensor always reliable; radar not full 3D velocity | sensor-strengths per-pair explanations and weather checks; radial claim explicitly labeled NOAA supplement |
| Intrinsic/extrinsic/time sync; overlay diagnosis; timestamp arithmetic | `p2-t4-d04-priority-sensor-calibration`, `p2-t4-d04-priority-sensor-direction-test`, `p2-t4-d04-priority-sensor-offset-calc` card |
| Early/feature/late fusion and architecture-bound pipeline | `p2-t4-d06-priority-fusion-levels`, `p2-t4-d06-priority-fusion-pipeline` |
| Open-loop fixed log vs closed-loop action-dependent observations | `p2-t4-d12-priority-loop-modes`, `p2-t4-d12-priority-robot-feedback` |
| Why open-loop/mAP is insufficient; accumulating errors/off-distribution states | retained `p2-t4-d12-q04`; `p2-t4-d12-priority-loop-reset`, `p2-t4-d12-priority-loop-evidence` |
| Explain evidence and repeated closed-loop comparison | `p2-t4-d12-priority-loop-explain` rubric; uses all runs, common conditions and uncertainty |
| Sigmoid/tanh/ReLU/softmax formulas and output domains | `p2-t4-d01-priority-activation-formulas` card, `p2-t4-d01-priority-activation-ranges` |
| Graph matching with accessible descriptions | `p2-t4-d01-priority-activation-graphs`; graph enum drives actual scalar curves, not a false softmax scalar graph |
| Values for x=(-1,0,1) | `p2-t4-d01-priority-activation-sigmoid-value`, `p2-t4-d01-priority-activation-tanh-value`, `p2-t4-d01-priority-activation-softmax-value`; ReLU numerical skill retained in `p2-t4-d01-c02`, and example in activation formula card |
| Binary/multi-label sigmoid vs single-label multi-class softmax | `p2-t4-d01-priority-activation-heads`; multi-label explicitly marked PyTorch supplement |
| Saturation/vanishing vs dead ReLU | retained `p2-t4-d01-x04`; graph/formula/derivative cards show sigmoid/tanh limits; `p2-t4-d01-priority-activation-dead-relu` |
| Softmax !=argmax; additive invariance and subtract-max stability | `p2-t4-d01-priority-activation-formulas`, `p2-t4-d01-priority-activation-softmax-value`, `p2-t4-d01-priority-activation-stable` |
| Sigmoid/tanh/ReLU derivatives and upstream gradient | `p2-t4-d01-priority-activation-derivative` card, `p2-t4-d01-priority-activation-tanh-gradient` card |
| Softmax+CE gradient p−y and mean-batch factor | retained `p2-t4-d01-q01`; `p2-t4-d01-priority-activation-batch-gradient` card |
| Normalization formula, epsilon, affine gamma/beta vs statistics | `p2-t4-d01-priority-norm-symbols` card, `p2-t4-d01-priority-norm-epsilon` |
| B×D BN columns vs LN rows; CNN N,C,H,W; token B,T,D LN on D | `p2-t4-d02-priority-norm-axes`; normalized_shape explicit |
| BN batch train/running eval, LN current-input stats in both modes | `p2-t4-d02-priority-norm-inference`, `p2-t4-d02-priority-norm-ln-eval` (explicit PyTorch supplement) |
| X=[[1,3],[5,7]] worked BN/LN example; divisor/epsilon/gamma/beta assumptions | `p2-t4-d01-priority-norm-bn-value`, `p2-t4-d01-priority-norm-ln-value` |
| Affine output need not mean0/variance1 | `p2-t4-d01-priority-norm-affine` |

## C: nine required pipelines

| Pipeline | Ordering ID | Non-unique-order treatment |
|---|---|---|
| ReAct | `p1-d03-priority-react-loop` | Check loop/termination after observation |
| Kalman | `p2-t4-d05-priority-kalman-pipeline` | Independent calculations grouped |
| Training | `p2-t4-d01-priority-training-pipeline` | Batch and cleared old gradients fixed in premise |
| RAG indexing | `p1-d07-priority-rag-index` | Specified dense index architecture |
| RAG answering | `p1-d08-priority-rag-answer` | Rerank only required for the stated architecture |
| NMS | `p2-t4-d03-priority-nms-pipeline` | Both filter→sort and sort→filter accepted; strict IoU suppress policy given |
| Tracking | `p2-t4-d07-priority-tracking-pipeline` | Detect/predict grouped; final update/lifecycle grouped |
| Sensor fusion | `p2-t4-d06-priority-fusion-pipeline` | Specific feature-fusion architecture; encoders grouped |
| Robot feedback | `p2-t4-d12-priority-robot-feedback` | Cycle start fixed at new observation |

One additional ordering item `p1-d03-priority-react-dependent-tools` tests dependent tool use.

## D: retained numerical groups and formula lookup

Formula card IDs are parent IDs. Several coherent cards group related equations rather than creating duplicate cards/questions for every old exercise. Examples and conditions are reviewable content at that parent's revision.

| Requested group | Existing questions retained | New distinct objective and formula card IDs |
|---|---|---|
| Forward Wx+b, dense parameters, MSE/BCE/CE, backprop/GD | `p2-t4-d01-c01`, `p2-t4-d01-c02`, `p2-t4-d01-x02`, `p2-t4-d01-x08`, `p2-t4-d01-x12`, `p2-t4-d01-q01` | `p2-t4-d01-priority-d-forward-gradient`: simultaneous parameter updates; card contains all named base loss formulas; activation-batch-gradient card adds CE gradient |
| Smooth-L1, focal, L2, momentum, Adam/AdamW, clipping | `p2-t4-d01-x13`, `p2-t4-d01-x15`, `p2-t4-d01-q03`, `p2-t4-d01-q04` | `p2-t4-d01-priority-d-robust-loss`: marginal tail penalty; `p2-t4-d01-priority-d-clipped-momentum`: clipping before buffer update. Cards cover all seven techniques; corrected Adam moments are defined inputs, not a full from-zero optimizer derivation |
| CNN output/padding/stride/dilation/params/MAC/receptive field | `p2-t4-d02-c01` | `p2-t4-d02-priority-d-cnn-receptive`: cumulative jump; card includes output/parameter/MAC equations and scopes receptive formula to dilation1 |
| Residual/RNN/LSTM/attention/patch/token/cost | `p2-t4-d02-c02`, `p2-t4-d02-q01`, `p2-t4-d02-q02`, `p2-t4-d02-q03` | `p2-t4-d02-priority-d-rnn-shared`: parameters shared across time; `p2-t4-d02-priority-d-attention-memory`: CLS and quadratic matrix memory; cards include residual/RNN/LSTM/attention equations |
| IoU/GIoU/P/R/F1/AP/mAP/Dice/mIoU/OKS/PCK/letterbox | `p2-t4-d03-q01`, `p2-t4-d03-c01`, `p2-t4-d03-c02` | Five topics in four cards: `p2-t4-d03-priority-d-giou-disjoint`, `p2-t4-d03-priority-d-ap-unreached`, `p2-t4-d03-priority-d-seg-aggregate`, `p2-t4-d03-priority-d-pose-boundary`. F1 equation has explicit primary supplement |
| Camera bandwidth/bit-byte/video/saturation/timestamp | `p2-t4-d04-c01`, `p2-t4-d04-c02` | `p2-t4-d04-priority-d-video-budget` full sensor arithmetic card; `p2-t4-d04-priority-sensor-offset-calc` timestamp card |
| Voxel/dense memory/coordinate transform/LiDAR projection/back-projection | `p2-t4-d06-c01`, `p2-t4-d06-c02`, `p2-t4-d08-q03` | `p2-t4-d06-priority-d-voxel-resolution`: anisotropic resolution and channels; `p2-t4-d08-priority-d-backproject-depth`: optical depth vs Euclidean range; two cards cover named groups |
| Assignment/Mahalanobis/MOTA/IDF1/HOTA | `p2-t4-d07-c01`, `p2-t4-d07-c02`, `p2-t4-d07-q01` | `p2-t4-d07-priority-d-tracking-gate` full tracking card; HOTA at one alpha distinguished from average across alpha; no false AssA shortcut |
| Flat-ground depth/NDS | `p2-t4-d08-c01`, `p2-t4-d08-c02` | `p2-t4-d08-priority-d-nds-saturation`: clipping makes some error improvements invisible to score; card states level/rectified-camera assumption |
| Frame count/sampling/batches/annotation/savings | `p2-t4-d09-c01`, `p2-t4-d09-c02` | `p2-t4-d09-priority-d-batch-drop`: final partial-batch policy; card retains annotation/saving arithmetic |
| Normalized box/area/weights/MoE | `p2-t4-d10-c01`, `p2-t4-d10-c02` | `p2-t4-d10-priority-d-box-scale-mismatch`: wrong coordinate schema changes area anisotropically; card contains resident vs active parameter distinction |
| Acceleration/noise/jerk/curvature/lateral acceleration | `p2-t4-d11-c01`, `p2-t4-d11-c02` | `p2-t4-d11-priority-dynamics-offset`: constant calibration offset cancels in second difference, independent noise does not; `p2-t4-d11-priority-dynamics-gates`: multiple kinematic gates. Both have full cards |
| Data scaling/importance sampling/3-n applicability | Existing scaling/validation conceptual bank retained | `p2-t4-d11-priority-scaling-floor`: finite data cannot reach irreducible floor; `p2-t4-d11-priority-importance-weight`: ordinary IS p/q mean; `p2-t4-d12-priority-zero-events-bound`: exact/approximate 95% zero-event bound and independent trials vs correlated frames. Three cards; IS and 3/n use explicitly labeled primary supplements |
| TTC/deceleration/clipping/completion penalty | `p2-t4-d12-q03`, `p2-t4-d12-c01`, `p2-t4-d12-c02` | `p2-t4-d12-priority-ttc-comparison`: equal TTC can require different deceleration; `p2-t4-d12-priority-clip-inverse`: saturation loses information about raw prediction; `p2-t4-d12-priority-completion-aggregation`: per-route multiplication before averaging. All have cards |

## Source gaps resolved explicitly

Local slides anchor the curricular taxonomy and remain preferred. Some requested precision goes beyond them; supplements are labeled in the questions and independently opened by the reviewer:

- Hugging Face versioned GenerationConfig: exact top-k/top-p algorithms and output-token budget/API convention.
- PyTorch BCEWithLogitsLoss: multi-label independent sigmoid/BCE; LayerNorm: input statistics in both train/eval.
- FilterPy KalmanFilter: known control B×u in full matrix prediction.
- NOAA radar velocity: radial Doppler component; original LiDAR/radar slides alone did not establish the full velocity caveat.
- scikit-learn f1_score: explicit F1 harmonic-mean equation; PDF p42 anchors detection counts.
- Owen/Maximov/Chertkov importance-sampling paper: explicit ordinary density-ratio event estimator, beyond the D11 lab mention.
- Hanley/Lippman-Hand zero-numerator paper: exact one-sided zero-event bound and rule 3/n; D12 evidence-size discussion provides the curricular anchor.

The supplementary statements are narrow, not claims that the whole topic is absent from the slides. Source refs preserve catalog SHA256 and physical PDF page numbers. No anecdote about an exam is used as factual provenance or as an official exam guarantee.

## Revision and uniqueness handling

Independent review rejected near-duplicate first drafts of Plan–Act–Verify, Kalman sensitivity/EKF, and closed-loop explanation. Replacements now test replanning a wrong objective, joint uncertainty scaling, matching filter families, repeated evaluation, and quantitative accumulated bias. Old review decisions remain in audit artifacts. NMS now accepts both valid preprocessing orders; tracking groups independent stages. Other refinements added direct citations, specified divisibility/boundary conventions, and distinguished radial velocity from radial position uncertainty.

Historical author scripts reproduce their initial batches only. **Do not rerun them over the curated JSON**: reviewed corrections live in the JSON and targeted revision scripts. Root must use current JSON plus matching exact-revision reviewer artifacts for release.
