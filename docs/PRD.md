# PRD — Mid-term AIA web

Ngày khảo sát: 2026-10-22. Trạng thái: **đề xuất, chờ duyệt Discovery**. Đây không phải báo cáo sản phẩm đã triển khai.

## Bối cảnh và bằng chứng

Workspace hiện có `slide/` với 63 PDF; chưa có ứng dụng, framework, dependency manifest, test, script build hay Git repository. Tài liệu kiểm kê: [CONTENT_INVENTORY.md](discovery/CONTENT_INVENTORY.md), [source-inventory.json](discovery/source-inventory.json), [CODEBASE_AUDIT.md](discovery/CODEBASE_AUDIT.md).

Giữ nguyên workspace và toàn bộ nguồn. Sau phê duyệt mới tạo ứng dụng ngay trong workspace này; không thay thế bằng project khác. Discovery chỉ tạo tài liệu và mẫu khảo sát trong `tmp/discovery/`.

## Người dùng và mục tiêu

Giả định để duyệt: một người học, sử dụng trên một trình duyệt/thiết bị, giao diện tiếng Việt; thuật ngữ chuyên môn giữ tiếng Anh khi cần. Mục tiêu là ôn đúng tài liệu đã cung cấp, biết điểm yếu theo chủ đề và luyện thi 90 phút. Chưa có yêu cầu tài khoản, đồng bộ thiết bị, phòng thi, giám sát hoặc thanh toán.

## Phạm vi chức năng

| Nhóm | Hành vi yêu cầu |
|---|---|
| Dashboard | Tiến độ, lịch sử, điểm gần nhất, thống kê Phase/Track/Topic, nội dung cần ôn |
| Daily / Topic | Chọn ngày hoặc chủ đề có căn cứ nguồn; lọc độ khó; giải thích sau trả lời hoặc cuối phiên |
| Track / Phase | Luyện riêng Track 1–4 thuộc Phase 2 hoặc riêng Phase 1/2 |
| Mixed Review | Trộn nhiều Phase/Track theo lựa chọn; vẫn báo thiếu khi không đủ câu |
| Wrong / Bookmarked Review | Luyện câu sai hoặc câu đánh dấu; ghi nhận kết quả mới nhưng giữ lịch sử |
| Mock Exam | 90 phút; 60/40 theo điểm; tự luận 10%; đủ bốn track; lưu câu trả lời, đánh dấu, nộp tay/tự động |
| Results | Tổng điểm, điểm Phase/Track/Topic, đúng/sai/bỏ trống/chờ tự chấm, đáp án, giải thích, rubric |
| Persistence | Khôi phục phiên đang thi và lịch sử sau reload; báo lỗi lưu; xuất dữ liệu để sao lưu |
| Import / Export | JSON có version/schema; preview lỗi; nhập nguyên tử; không mặc định tin trạng thái approved từ tệp lạ |
| Responsive | Dùng bàn phím, mobile và desktop; nhãn rõ ràng, không chỉ dùng màu báo đúng/sai |

Ngân hàng phát hành chỉ chứa câu `approved` đã được kiểm tra độc lập. Không dùng kiến thức ngoài nguồn để tự lấp phần OCR hoặc nguồn bị thiếu.

## Quy tắc thi đề xuất

- 100 điểm, 90 phút; Phase 1: 60, Phase 2: 40. Đây là tỷ lệ **điểm tối đa**, không phải số câu hoặc số điểm thí sinh đạt.
- Tự luận ngắn: 10 điểm, chia Phase 1 = 6, Phase 2 = 4. Phần khách quan: 54 và 36. Mặc định mỗi track Phase 2 nhận 10 điểm: 9 khách quan + 1 tự luận.
- Trọng số bốn track cấu hình được, tất cả phải lớn hơn 0. Cấu hình không thể biểu diễn chính xác bằng đơn vị điểm/slot hoặc thiếu ngân hàng phải bị từ chối trước khi bắt đầu.
- Một đáp án và đúng/sai: đúng toàn điểm, sai/bỏ trống 0. Nhiều đáp án: tập lựa chọn phải khớp hoàn toàn; không chấm từng phần, không trừ điểm.
- Tự luận: lưu bài viết, hiển thị rubric sau nộp; người học tự chấm từng tiêu chí. Chưa tự chấm thì hiển thị “điểm khách quan x/90; tự luận chờ chấm /10”, không quy đổi x/90 thành điểm cuối /100. Tự luận bỏ trống = 0. Điểm sau tự chấm ghi rõ nguồn chấm.
- Câu tình huống dùng hình thức trả lời khách quan hoặc rubric; tỷ lệ tự luận dựa trên `answer_format=rubric`, không dựa vào nhãn tình huống.
- Không lộ đáp án trong giao diện làm bài thi. Đây là web tự học chạy phía client, không cam kết chống xem dữ liệu bằng công cụ phát triển.
- Khi trình duyệt đóng, không thể chạy tác vụ nộp nền. Hết hạn sẽ khóa bài và hoàn tất nộp ngay lần mở lại; thời điểm hết hạn logic vẫn là deadline ban đầu.

## Nội dung và điều chưa rõ

Các thư mục thực tế: `phase1` (15 file), `track1 k3` (11), `track2 k3` (12), `track3 k3` (13), `track4` (12). Tổng 3.589 trang; 3.142 trang không có text, 447 trang có text chưa đồng nghĩa đọc đúng. Track 2 không có file mang tên Day 9; chưa kết luận đây là tài liệu bị thiếu hay lịch học bỏ qua ngày đó.

Hai xung đột cần xác minh: `phase1/day 2 ai product.pdf` trang 1 ghi Track 1; `track2 k3/day 3 tu chatbot den agentic agent.pdf` trang 1 ghi Phase 1. Không tự chuyển file hoặc coi vị trí thư mục là phân loại chính xác. Các ngày trên bìa còn có khoảng 20–21 và số ngày không tăng theo tên file; xem inventory để đối chiếu từng tài liệu.

Tên file Day 1 của Track 1–3 và số ngày 16 trên bìa là hai hệ đánh số. Phải lưu cả hai, chưa tự áp dụng phép cộng 15 cho toàn bộ tài liệu. Track 2/3 có Phase 2 ghi trên bìa mẫu; quan hệ Phase 2 của Track 1/4 cần nguồn bổ sung hoặc xác nhận. Tên chủ đề và mức độ bao phủ toàn khóa chỉ chốt sau ingestion.

## Ngoài phạm vi hiện tại

Không thêm hệ thống tài khoản/backend, chấm tự luận bằng AI, thi có giám sát, tự động cập nhật kiến thức từ Internet hay triển khai công khai. Chỉ đề xuất bổ sung khi có nhu cầu cụ thể.

## Thành công và điều kiện chuyển bước

Tiêu chí nghiệm thu chi tiết tại [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md). Mỗi gate phải có artifact và bằng chứng thực chạy. Chưa có test/build sản phẩm nào chạy trong Discovery vì chưa có ứng dụng. Dừng trước Milestone 1 để người dùng duyệt các quyết định trong [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).
