# Kiểm định 17 chỉnh sửa wording cuối

**17 approved** exact current revisions trong JSON. Đã đọc actual stem, options, answer, explanation của cả 17; render/xem lại 16 trang vật lý thuộc 13 PDF, gồm p17 cũ và p21 retest ORPO. Hashes 13 nguồn được tính độc lập và khớp catalog. Ảnh ở `tmp/reviewer/wording-final/`.

Finding đã đóng: p2-t3-d07-q03 r3 mở rộng mệnh đề thành kết hợp demonstration/preference nhưng chỉ cite section divider p17. r4 cite p21 và explanation ORPO combined SFT+preference objective, đã đọc lại đúng revision và đối chiếu ảnh. Mệnh đề dùng “có thể”, không khẳng định mọi alignment algorithm bỏ SFT riêng.

Các sửa khác giữ điều kiện kỹ thuật, cung cấp thuật ngữ/tình huống cần thiết và không buộc người học biết checklist/sơ đồ/timeline/lab chưa trình bày. Không thay báo cáo 87 historic hoặc 10 followup. Đây là gate nội dung wording, không kiểm thử app hoặc xác nhận batch chưa review.

## Bằng chứng từng câu

- **p1-d04-q03 r3 approved**: p9: Harness runtime gồm sandbox/quyền/trace, a,b đúng. Stem nêu mô hình bốn lớp; context-token selection và một-message wording không là toàn bộ harness.
- **p1-d11-q02 r2 approved**: p5: Adversarial tests trước/sau và HITL decision flow là evidence kiểm guardrails/human escalation; a,c đúng. Demo thuận lợi hoặc hứa loại mọi risk không đủ kiểm chứng.
- **p1-d14-q03 r2 approved**: p9: Offline batch golden dataset phù hợp release/prompt change; True đúng. Không suy offline đủ thay continuous/human evaluation.
- **p2-t4-d05-q01 r2 approved**: p18: Predict theo dynamics rồi update bằng phép đo mới; c đúng. Bỏ cả prediction hoặc measurement không là vòng lặp Kalman.
- **p2-t4-d07-q02 r2 approved**: p27: ByteTrack low-score vòng hai cứu existing track, không khởi tạo mới; False đúng. Stem gọi rõ ByteTrack, không còn phụ thuộc sơ đồ.
- **p2-t4-d11-q03 r2 approved**: p36: Quy trình giả định kiểm IoU giữa conditioning box và box detector tìm lại trong ảnh sinh; c đúng. Stem đã nêu quy trình có điều kiện, không gọi đây là chuẩn công bố.
- **p2-t1-d10-q02 r2 approved**: p9: Taxonomy Champions ở high influence/high interest; True đúng. Thuật ngữ nhóm xác định điều đang kiểm.
- **p2-t1-d10-q03 r3 approved**: p9: Hai trục hỏi ảnh hưởng đến kết quả và quan tâm dự án; a,b đúng. Title cao hoặc đã dùng AI không thay hai trục.
- **p2-t2-d12-q01 r2 approved**: p6: Freshness đo thời gian cập nhật/so SLA; d đúng. Schema/lineage/volume không trực tiếp kiểm độ trễ nguồn.
- **p2-t2-d13-q01 r2 approved**: p10: Audit trail giữ token cost per component và model version used; a,c đúng. Chỉ uptime/user count không trace request/model/cost.
- **p2-t3-d04-q01 r2 approved**: p13: Triple subject–predicate–object; d đúng. Embedding-score/chunk-overlap/prompt-token không là KG triple.
- **p2-t3-d04-q03 r2 approved**: p13: Graph retrieval có thể traverse entities/relations thay chỉ chunk search; True đúng với điều kiện hệ RAG dùng KG.
- **p2-t3-d07-q01 r2 approved**: p12: DPO train preference pairs trực tiếp, không cần Reward Model riêng; d đúng. Không loại dữ liệu preference hoặc trainable policy.
- **p2-t3-d07-q02 r2 approved**: p18: Human preference ghép RLHF/DPO, verifiable code/regex ghép RLVR; b,d đúng. Stem hỏi ghép nguồn tín hiệu, không bắt nhớ timeline.
- **p2-t3-d07-q03 r4 approved**: p21: ORPO kết hợp SFT loss + preference loss trong cùng objective; True đúng với từ có thể. Retest r4 đã thay citation p17 section divider bằng p21 support trực tiếp.
- **p2-t3-d08-q02 r2 approved**: p16: Node retry idempotent và return partial update; b,c đúng. Không mutate toàn state hoặc bỏ timeout dựa graph tự hết lỗi.
- **p2-t3-d11-q01 r2 approved**: p10: MCP Resources cung cấp read-only data qua URI làm context; d đúng. Tools callable, prompts templates, sampling completions là primitive khác.
