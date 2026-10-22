# Mở rộng ngân hàng — yêu cầu đã xác nhận

Ngày 2026-10-22. Người dùng xác nhận **20 câu mỗi file PDF**, không phải mỗi trang: tối thiểu 1.260 câu trong 63 file. Câu hỏi trực tiếp kiểm tra kiến thức/tình huống từ nội dung PDF; không hỏi cách trình bày hoặc điều gì được nêu trong slide. Nguồn file/trang đặt riêng trong metadata.

| Nhóm | PDF | Đã có ở v1 | Mục tiêu tối thiểu | Bổ sung cần thiết |
|---|---:|---:|---:|---:|
| Phase 1 | 15 | 48 | 300 | 252 |
| Track 1 | 11 | 33 | 220 | 187 |
| Track 2 | 12 | 36 | 240 | 204 |
| Track 3 | 13 | 39 | 260 | 221 |
| Track 4 | 12 | 48 | 240 | 192 |
| Tổng | 63 | 204 | 1.260 | 1.056 |

Author A: Phase 1, Track 1, Track 4 Days7–12 (535 câu mới). Author B: Track 2, Track 3, Track 4 Days1–6 (521 câu mới). Reviewer kiểm tra độc lập đúng revision, nguồn và từng phương án. Root chỉnh các câu cũ thành câu hỏi tự đủ ngữ cảnh, cũng phải duyệt lại; không tự duyệt chỉnh sửa của mình.

Các batch đầu phát hiện phương án nhiễu không đủ hợp lý, đã yêu cầu tác giả tạm dừng sinh hàng loạt để chỉnh các nhầm lẫn cùng khái niệm. Không nâng câu lên approved bằng schema test hoặc chỉ để đạt số lượng. Câu đã có source nhưng diễn đạt phụ thuộc bảng/slide phải được viết lại có đầy đủ giả định trong đề bài.

`structural-audit.json` là thống kê đang làm, phân biệt draft và review độc lập đúng revision. `wording-change-set.json` lưu thay đổi câu cũ. Hai file này không phải quyết định duyệt học thuật. Quyết định duyệt nằm trong `reports/content/expand-*.json`.

Gate trước phát hành: tất cả PDF có ít nhất20 ID câu đã duyệt; không trùng ID hoặc câu exact; không stem phụ thuộc nguồn; đáp án/rubric/schema hợp lệ; source hashes không đổi. Lệnh: `python scripts/validate_release.py --verify-sources --min-per-document 20 --standalone-stems`.

Phần đề thi 60 câu đã triển khai riêng: 36 câu Phase1/24 câu Phase2, giữ60/40điểm/90phút; xem `reports/qa/EXAM_60_RELEASE.md`. Ngân hàng live chưa được tăng số lượng cho tới khi hoàn thành gate nội dung.
