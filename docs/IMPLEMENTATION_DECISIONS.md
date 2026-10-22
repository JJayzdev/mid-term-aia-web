# Quyết định triển khai sau Discovery

Ngày 2026-10-22. Người dùng đã chỉ dẫn: “đấy là tất cả data tôi có rồi, sử dụng nó. triển khai đến lúc có thể deploy, deploy free bằng vercel hoặc github”. Chỉ dẫn này thay trạng thái chờ duyệt Gate0 trong các tài liệu Discovery lịch sử; cho phép triển khai, kiểm thử và deploy miễn phí.

## Các mặc định được Root chốt

- React + TypeScript + Vite, giao diện tiếng Việt, IndexedDB, không tài khoản/backend. Triển khai ngay workspace hiện có.
- Schema `docs/schemas/question-bank.schema.json` được duyệt phiên bản 1.0.0 trước tạo batch câu hỏi.
- Bài thi 100 điểm/90 phút/36 câu theo blueprint đã đề xuất: Phase1 54 khách quan + 6 rubric, mỗi track Phase2 9 khách quan + 1 rubric; nhiều đáp án exact-set, tự luận tự chấm có nhãn.
- Tổ chức chương trình theo thư mục do người dùng cung cấp: phase1 là Phase1; bốn track là Phase2. Day theo tên file và có khóa riêng theo Phase/Track. Đây là **quyết định tổ chức nội dung của ứng dụng**, không phải tuyên bố nhãn trên bìa luôn khớp. Metadata ngày/Phase/Track gốc và cảnh báo xung đột được giữ nguyên.
- Không cần chờ thêm nguồn, không tạo Day9 Track2. Sử dụng toàn bộ 63 file, báo rõ trang/đối tượng không đọc được. Chỉ câu có căn cứ đã kiểm tra độc lập được phát hành.
- OCR chạy local; nguồn không upload lên OCR service. PDF gốc không đưa vào bundle/public repository; giữ manifest/provenance và câu hỏi đã review.
- Chuẩn bị Vercel Hobby và GitHub Pages. Chỉ dùng phương án miễn phí, không tạo tài nguyên tính phí. Bước publish cần tài khoản đã đăng nhập; nếu môi trường thiếu đăng nhập, vẫn hoàn tất artifact/build/deploy instructions và báo đúng bước còn cần người dùng.

## Phân công đang chạy

A1: pipeline ingestion/cache/manifest/catalog, câu nháp theo batch. A2: toàn bộ ứng dụng/test/package configuration. Reviewer: audit độc lập nguồn/câu hỏi và code/QA sau khi artifact sẵn sàng. Root: hợp đồng, tích hợp, validation/release, deployment configuration và xác minh cuối. Không hai agent sửa cùng file. Tài liệu Discovery giữ để truy vết; văn bản này là quyết định mới hơn.

## Điều chỉnh sau bản v1 — 2026-10-22

Người dùng yêu cầu đề khoảng 60 câu, tiếp tục Phase 1 60% / Phase 2 40%. Chốt đúng 60 câu: Phase 1 có 34 khách quan + 2 rubric; Phase 2 mỗi Track có 5 khách quan + 1 rubric. Như vậy tỷ lệ đúng cả theo số câu (36/24) lẫn điểm (60/40), giữ 90 phút và 10 điểm rubric như yêu cầu ban đầu.

Mỗi bucket có tổng điểm nguyên theo đơn vị 0,01; chia quotient/remainder cho các slot, chênh tối đa 1 đơn vị trong bucket. Phase 1 khách quan 5.400 đơn vị trên 34 câu, rubric 600 trên 2; mỗi Track khách quan 36×w, rubric 4×w khi w là phần trăm trong Phase 2. Trọng số là bội dương 0,25%, tổng đúng 100%. Lưu điểm theo snapshot nên đề cũ không bị tính lại theo blueprint mới.

Người dùng xác nhận tối thiểu 20 câu mỗi file PDF: 63 file, tối thiểu 1.260 câu. Từ 204 câu hiện tại cần bổ sung 1.056 câu, review độc lập theo batch. Câu hỏi phải hỏi trực tiếp về kiến thức hoặc tình huống trong PDF; không dẫn kiểu “trong slide”, “theo tài liệu”. Tham chiếu file/trang nằm riêng trong metadata nguồn.
