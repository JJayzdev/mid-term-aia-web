# Kiểm toán codebase và đề xuất kỹ thuật

**Trạng thái:** discovery trước phê duyệt; chưa khởi tạo framework, cài package hoặc sửa mã ứng dụng.

## Bằng chứng khảo sát

Khảo sát tại `E:\VinAI\mid-term AIA web` ngày 2026-10-22:

- `Get-ChildItem -Force` chỉ thấy `docs/`, `slide/`, `tmp/`. Các thư mục slide hiện có là `phase1/`, `track1 k3/`, `track2 k3/`, `track3 k3/`, `track4/`; ở đây chỉ kiểm tra tên thư mục, không đọc hay xử lý bộ slide.
- Tại thời điểm khảo sát ban đầu, `rg --files -g '!slide/**' -g '!tmp/**'` không trả về tệp nào; `docs/discovery/` và `tmp/discovery/` cũng trống. Workspace có thể đã thay đổi sau snapshot này; ghi nhận đó không khẳng định trạng thái hiện tại của `tmp/`.
- `rg --files -g 'AGENTS.md' ...` với các mẫu ứng dụng/config đã dùng không tìm thấy AGENTS.md, package manifest/lockfile, cấu hình Vite/TypeScript/test, HTML entrypoint hay mã TS/JS/Python. Kiểm tra các vị trí cha `E:\AGENTS.md`, `E:\VinAI\AGENTS.md` và root workspace cũng không thấy AGENTS.md.
- `git rev-parse --show-toplevel` và `git status --short --branch` thất bại với `fatal: not a git repository (or any of the parent directories): .git`; workspace chưa được khởi tạo như Git repository.
- Công cụ có sẵn: Node `v24.14.1`, npm `11.11.0`, pnpm `11.25.0`, Python `3.9.13`, Git `2.51.0.windows.1`. Runtime kèm Codex cũng tồn tại: Node `v24.19.0`, Python `3.12.14`. `yarn` không có trên PATH.

Do chưa có ứng dụng, manifest, dependency hay script, chưa có lệnh build/dev/test/lint/typecheck nào có thể chạy. Hiện chỉ xác nhận khả năng chạy runtime và package manager; không cài đặt hay suy diễn phiên bản thư viện dự án.

## Kiến trúc tối thiểu đề xuất

Khởi đầu bằng ứng dụng đơn trang React + TypeScript + Vite, hoàn toàn chạy trên máy người học. Chỉ thiết lập scaffold và cài dependency sau khi được duyệt. Không thấy dấu hiệu yêu cầu tài khoản, đồng bộ nhiều thiết bị hoặc máy chủ; vì vậy chưa cần backend.

- Lưu câu hỏi đã duyệt, metadata, bookmark, lịch sử làm bài và câu trả lời bằng IndexedDB. Lưu tùy chọn nhỏ (ví dụ cấu hình trọng số) cùng nguồn dữ liệu cục bộ; xuất/nhập JSON là đường sao lưu và chuyển dữ liệu. Phiên bản schema và kiểm tra dữ liệu khi nhập giúp từ chối tệp lỗi hoặc sai định dạng mà không làm hỏng dữ liệu đang dùng.
- Tách ngân hàng câu hỏi đã duyệt khỏi luồng import/review. Bản seed ban đầu phải cố định và lặp lại được; không tự coi câu hỏi trích từ slide hoặc tệp import chưa duyệt là hợp lệ.
- Một bộ chọn phiên thống nhất phục vụ Daily, Track, Phase, Mixed, Wrong + Bookmarked Review và bài thi thử 90 phút. Lấy mẫu không lặp trong cùng phiên; nếu ngân hàng được duyệt không đủ câu, báo số lượng thiếu và dừng tạo phiên thay vì lặp câu hay lặng lẽ đổi chế độ.
- Lưu phiên, đáp án đã chọn và `deadline` tuyệt đối (timestamp) để khôi phục sau reload/đóng tab và tính thời gian còn lại dựa trên đồng hồ. Hỗ trợ nộp thủ công và tự nộp khi hết hạn; khi khôi phục phiên quá hạn phải hoàn tất nộp ngay.
- Tính điểm từ trọng số Phase 1 = 60%, Phase 2 = 40%; bốn trọng số track Phase 2 phải dương và tổng bằng 1. Từ chối cấu hình không hợp lệ hoặc không biểu diễn được thay vì tự chuẩn hóa âm thầm. Phần essay chiếm 10% theo yêu cầu; cần xác định trong tài liệu sản phẩm mẫu số và quan hệ giữa 10% essay với tỷ lệ 60/40 trước khi chốt công thức. Nếu chưa có người chấm hay rubric có thể máy chấm đáng tin cậy, essay chỉ nên lưu bài viết và cho người học tự đánh giá/rubric provisional, không trình bày như điểm khách quan.
- Màn hình kết quả giải thích điểm theo Phase, track và dạng câu; lưu kết quả để Wrong + Bookmarked Review lọc đúng câu sai/đã đánh dấu. Thiết kế responsive cho điện thoại và desktop, có trạng thái loading/empty/error và thao tác bàn phím cơ bản.

## Kiểm tra sau khi được duyệt triển khai

Khi scaffold tồn tại, thêm kiểm tra tự động tập trung vào hành vi có rủi ro: seed deterministic; không trùng và báo thiếu; quy tắc lọc review; biên 60/40, xác nhận bốn trọng số track dương có tổng 1 và từ chối cấu hình sai, cùng quy tắc essay; lưu/khôi phục phiên cùng deadline; auto-submit sau khi hết giờ; validation import/export và giữ dữ liệu cũ khi import lỗi. Chạy typecheck, unit tests và production build bằng scripts thực tế trong manifest. Hiện chưa thể chạy chúng vì chưa có mã hay scripts.

## Rủi ro và giới hạn cần tính đến

Local-only phù hợp với một người dùng trên một trình duyệt, nhưng dữ liệu có thể mất khi xóa site storage hoặc đổi thiết bị; trình duyệt có thể giới hạn/xóa dung lượng. JSON export là biện pháp khôi phục đơn giản, không phải đồng bộ hay sao lưu tự động. Timestamp deadline giúp khôi phục giữa reload nhưng ứng dụng client không thể ngăn sửa đồng hồ hệ thống, devtools hoặc chỉnh dữ liệu local; do đó bài thi không có tính giám sát hay chống gian lận. Điểm essay chỉ có ý nghĩa theo mức tự đánh giá nếu chưa có chấm độc lập. Cần chốt quy tắc điểm essay 10% trước khi hiển thị tổng điểm như một thước đo duy nhất. Trọng số track phải qua kiểm tra bốn giá trị dương và tổng bằng 1.

## Phân công và trạng thái tài liệu

- `docs/discovery/CODEBASE_AUDIT.md` — báo cáo kiểm toán và đề xuất này.
- `docs/ARCHITECTURE.md` và `docs/IMPLEMENTATION_PLAN.md` — Root phụ trách bản đề xuất kiến trúc và kế hoạch triển khai; cả hai vẫn chờ người dùng phê duyệt. Đây là cập nhật trạng thái so với đề xuất phân công ban đầu bên trên báo cáo.
- `src/` — phần triển khai giao diện và logic ứng dụng, chỉ tạo sau phê duyệt.
- `public/` hoặc thư mục dữ liệu có version — chỉ chứa seed câu hỏi đã duyệt; không tự nhập corpus slide vào ngân hàng.
- `tests/` (hoặc cạnh module theo convention được chọn) — kiểm tra selector, điểm, persistence và import; thêm sau khi có scaffold.
