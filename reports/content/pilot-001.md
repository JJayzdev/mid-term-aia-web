# Audit nội dung pilot-001

Kết quả revision1: **9 approved, 3 rejected**. Reviewer không phải tác giả, không chỉnh draft/bank. Đây là audit ngữ nghĩa theo nguồn, chưa phải nghiệm thu sản phẩm.

Đã tính lại SHA256 của p1-d01/p1-d11/p1-d14 và đối chiếu catalog; render110DPI, xem trực tiếp9 trang vật lý được dẫn. Ảnh nằm `tmp/reviewer/pilot/`. Trang vật lý luôn dùng làm chỉ số, không dùng số slide in (ví dụ p1-d01 p7 in4/42; p14 in11). Mapping chương trình theo policy thư mục/ngày của Root; không tuyên bố đó là nhãn in nguồn.

## Từng câu

- **p1-d01-q01 r1 — approved**: Trang vật lý 7 đối chiếu ba nhóm AI: b đúng vì Agentic tự lập kế hoạch/hành động; a,d thuộc discriminative, c chỉ một ví dụ generative. Explanation khớp; không phụ thuộc vị trí option.
- **p1-d01-q02 r1 — approved**: Trang vật lý14 liệt kê quản lý ngữ cảnh/compaction và quyền/sandbox: a,c đúng. Model weights và chỉ pretraining không thuộc phần non-model harness. Explanation có vòng lặp/bộ nhớ/quan sát đều có trên trang.
- **p1-d01-q03 r1 — approved**: Trang vật lý27 ghi hallucination: tự tin nhưng sai do tối ưu xác suất token, không phải đúng-sai. True và explanation được nguồn hỗ trợ trực tiếp.
- **p1-d01-q04 r1 — rejected**: Trang vật lý10 hỗ trợ chọn cascaded STT–LLM–TTS cho audit/transcript và thay provider, đổi lại độ trễ/mất ngữ điệu. Tình huống minh bạch, đáp án đúng. Major: partial_credit của cả hai tiêu chí không nêu biên 0.5 cụ thể, khó tự chấm nhất quán; cần định nghĩa phần ý thiếu nào cho từng tiêu chí.
- **p1-d11-q01 r1 — approved**: Trang vật lý5 phân biệt input injection detection/topic filter với output content filter/grounding check. c đúng; a là input, b,d không phải output pipeline nêu trên. Explanation khớp.
- **p1-d11-q02 r1 — approved**: Trang vật lý5 yêu cầu adversarial tests trước/sau và HITL flowchart: a,c đúng. b chỉ demo không đủ; d trái red-team report còn risk nào. Stem chọn thành phần trong các options, không đòi liệt kê toàn artifact pack.
- **p1-d11-q03 r1 — approved**: Trang vật lý4 yêu cầu escalation theo rủi ro×hoàn tác, cảnh báo confidence score đáng ngờ. Mệnh đề chỉ confidence là false; explanation đúng.
- **p1-d11-q04 r1 — rejected**: Trang vật lý4 có interrupt/resume, hàng đợi duyệt, timeout, audit trail; đáp án nêu hai cơ chế khác nhau là được hỗ trợ. Major: partial_credit không có biên cụ thể và yêu cầu liên hệ tình huống dù câu này không có tình huống; cần tiêu chí một cơ chế, cơ chế thứ hai khác nhau và cách chấm diễn đạt chưa đầy đủ.
- **p1-d14-q01 r1 — approved**: Trang vật lý6 nêu open-ended/stochastic và chất lượng đa chiều. a đúng; b,c,d trái hoặc không được hỗ trợ. Explanation đúng về nhiều đáp án và nhiều chiều.
- **p1-d14-q02 r1 — approved**: Trang vật lý7 nguyên tắc lặp lại, so sánh, tự động. a,b đúng; c,d trái scientific method/measure. Không yêu cầu option chứa mọi nguyên tắc để bộ đáp án đúng đầy đủ trong bốn lựa chọn.
- **p1-d14-q03 r1 — approved**: Trang vật lý9 offline=batch golden dataset, mỗi release/prompt change. True/explanation khớp, phân biệt online/human rõ.
- **p1-d14-q04 r1 — rejected**: Trang vật lý6 có ví dụ trả lời đúng nhưng dài gấp3 và chất lượng liên quan/đủ/mạch lạc. Tình huống/đáp án hợp nguồn; không mặc định dài hơn chắc chắn kém. Major: partial_credit chung chung ở hai tiêu chí không định nghĩa mức0.5 cụ thể; cần phân biệt chỉ nêu giới hạn accuracy với giải thích áp dụng, hoặc chỉ nêu chiều với mô tả cách dùng.

## Hành động và giới hạn

Ba câu rejected cần A1 sửa rubric với ranh giới 0/0.5/1 cụ thể theo từng tiêu chí, tăng revision rồi review lại. Chín câu approved chỉ được promote đúng revision1; nguồn cần được chuyển verified bởi release workflow dựa audit này. Một số distractor đơn giản nhưng không tạo đáp án đúng thứ hai. q14-q01/q04 cùng nguyên lý nhưng khác yêu cầu nhận biết/vận dụng nên không phải trùng nguyên câu. Không kiểm thử app, không khẳng định OCR toàn corpus đúng; scope chỉ12 câu trên9 trang đã xem.

## Retest revision2

Ba câu rubric p1-d01-q04, p1-d11-q04, p1-d14-q04 đã đọc lại phần sửa, ranh giới 0/0.5/1 cụ thể và nhất quán nguồn đã xem. **Approved revision2** cho ba câu; chín khách quan giữ approved revision1. Lịch sử rejected revision1 ở trên được giữ. Report JSON hiện chứa revision được duyệt mới nhất, tổng12 approved.
