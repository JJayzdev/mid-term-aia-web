# Câu hỏi trực tiếp — nghiệm thu 2026-10-22

Ngân hàng `2026.10.22-7b3dd4b2cc37`, vẫn204 câu, có87 câu cũ được chỉnh stem và reviewer độc lập duyệt lại đúngrevision (`reports/content/expand-wording.json`). Không phát hành câu mới chưa duyệt:440 draft expansion được loại khỏi lần build này. Đây là cập nhật diễn đạt, chưa hoàn thành mục tiêu20câu/PDF.

Root đã chạy validator với `--verify-sources --standalone-stems`: PASS; nguồn không đổi, không còn các mẫu stem phụ thuộc slide/bảng. Bằng chứng local `tmp/qa/wording-release-validation.json`.

Thêm lựa chọn luyện20/30/60 câu nếu ngân hàng đã duyệt đủ câu. Bộ E2E chọn toàn bộ ngày mẫu để luôn kiểm tra cả câu tự luận khi ngân hàng mở rộng. Điểm/snapshot/lưu dữ liệu không đổi.

Build mới phát hiện kiểu `number` suy rộng trong regression test lịch sử36câu vừa thêm; sửa literal `1 as const` để khớp `RubricMarks`. Không thay logic runtime. `npm run build` (TypeScript+Vite) sau sửa PASS, JS `index-vAmUaaut.js`. 51 unit tests đã chạy đạt trước sửa literal không đổi runtime; final expansion sẽ chạy lại toàn bộ.

Root chạy12E2E trên production preview:12/12 PASS,0skipped/flaky,21,4giây; `tmp/qa/wording-preview-browser-results.json`. Đề60câu và36/24quota vẫn đúng. Các bài cũ giữ nguyên nội dung snapshot trong lịch sử.

Deploy/live verification cập nhật sau publish.
