# Đề 60 câu — nghiệm thu 2026-10-22

Thay đổi theo yêu cầu người dùng: đề mới 60 câu / 90 phút, 36 câu Phase 1 và 24 câu Phase 2 (6 mỗi Track), đồng thời giữ 60/40 điểm, tổng 100 điểm, tự luận 10 điểm. Ngân hàng 204 câu chưa đổi trong lần cập nhật blueprint này; mở rộng tối thiểu 20 câu/PDF là công việc nội dung tiếp theo.

- Root chạy `npm test -- --reporter=json --outputFile=tmp/qa/exam60-unit-results.json`: 51/51 PASS. Bao gồm regression giữ nguyên snapshot/điểm/đáp án khi resume và restore đề 36 câu cũ; 100 seed mặc định và 100 seed trọng số khác nhau.
- Root chạy `npm run build`: PASS, TypeScript và production build. JS `index-C_OHrUiH.js`.
- Root chạy `python scripts/validate_release.py --verify-sources`: PASS, 204 câu có audit đúng revision, nguồn PDF không đổi, đủ bucket mới 34/2 và 5/1 mỗi Track.
- Root chạy 12 E2E trên production preview: 12/12 PASS, 0 skipped/flaky, 23,4 giây. Có kiểm tra 60 ID duy nhất, 36/24 câu, 6 mỗi Track; điểm đúng 60/40, 90/10; trả lời đúng toàn bộ khách quan đạt 90 điểm; deadline/save/two-tab/import/mobile tiếp tục đạt. Bằng chứng local `tmp/qa/exam60-preview-browser-results.json`.
- Reviewer độc lập đã duyệt thay đổi, không có lỗi major/critical mở; xem `EXPANSION_CODE_REVIEW.md`.

Điểm từng bucket được chia theo đơn vị 0,01 bằng thương/phần dư; không thay đổi tổng quota. Lịch sử sử dụng snapshot nên không bị đổi sang 60 câu.

Deploy và kiểm thử live được cập nhật sau khi publish.
