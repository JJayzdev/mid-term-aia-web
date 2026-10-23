# Tiêu chí nghiệm thu và bằng chứng

Tài liệu này xác định tiêu chí từ Discovery. Sau chỉ dẫn triển khai ngày 2026-10-22, kết quả thực tế được ghi riêng trong `reports/qa/RELEASE_QA.md` và `reports/qa/CODE_REVIEW.md`; bảng dưới đây là yêu cầu, không tự chứng minh PASS. Gate 0 nghiệm thu artifact Discovery riêng với gate sản phẩm.

| ID | Điều kiện / hành vi cần xác minh | Bằng chứng bắt buộc |
|---|---|---|
| D0 | Có đủ 5 tài liệu yêu cầu, kiểm kê toàn bộ file, codebase audit, giả định/quyết định chờ duyệt; nguồn không thay đổi | Danh sách file, count/size/hash trước–sau, kiểm tra liên kết nội bộ |
| I1 | Mọi PDF có manifest, mọi trang có trạng thái trích xuất hoặc issue rõ ràng | Manifest + số trang đối chiếu + issue report; không bỏ qua file lỗi |
| I2 | Phase/Track/Day/Topic có bằng chứng; ngày file và ngày nguồn không bị nhập nhằng | Mapping có explicit/inferred/confirmed, nguồn+trang, unresolved list |
| I3 | OCR/bảng/figure/công thức có đối chiếu hình ở phần dùng sinh câu hỏi | Mẫu trang gốc và kết quả xác minh, lỗi/confidence ghi riêng |
| C1 | Schema hợp lệ theo từng format, thiếu đáp án/nguồn/rubric hoặc options sai loại bị từ chối | Validator với fixture đúng/sai ở mọi nhánh, runtime cross-field tests |
| C2 | Không trùng ID/option, đáp án thuộc options, rubric tổng 1, trang/hash/catalog hợp lệ | Validator report và fixture lỗi |
| C3 | Tất cả câu phát hành được review độc lập đúng revision; không có lỗi chưa xử lý | Audit từng batch, phát hiện reviewer=author và approval cũ, retest câu sửa |
| C4 | Trùng exact bị chặn, gần trùng được audit | Báo cáo duplicate/near-duplicate cùng quyết định reviewer |
| C5 | Mỗi trong 63 PDF có ít nhất 20 câu đã duyệt; câu hỏi tự đủ dữ kiện, hỏi kiến thức/ứng dụng thay vì nhớ nội dung hay vị trí slide | Validator `--verify-sources --min-per-document 20 --standalone-stems`, đếm ID duy nhất mỗi PDF, semantic review từng câu |
| E1 | Đề mới đúng 60 câu, Phase1=36/Phase2=24 (6 mỗi Track); tổng 100 điểm, Phase1=60/Phase2=40; tự luận=10 (P1=6/P2=4), khách quan=90; mọi slot nguyên theo 0,01 điểm | Unit/invariant tests trên nhiều seed, weights, quotient/remainder; scenario rubric được tính là tự luận; đề cũ giữ snapshot |
| E2 | Track1–4 mặc định mỗi track 10 điểm; trọng số hợp lệ đổi được, không làm tròn âm thầm | Test equal/unequal weights, zero/negative/NaN/tổng sai/precision không khả thi |
| E6 | Đề mới có ít nhất 2 câu tính đã duyệt ở Track 4; bộ lọc tính toán kết hợp đúng phạm vi, không ảnh hưởng bài đã lưu | Seeded surplus-pool tests, thiếu/unaudited calculation fixtures, E2E lọc và reload |
| E3 | Chỉ approved đúng review revision được lấy; không lặp ID | Test trộn tất cả status, revision cũ; lặp seed/bank/config/version cho cùng đề |
| E4 | Ngân hàng thiếu phải dừng trước tạo phiên, không bù Phase/Track/format khác | Boundary fixture thiếu đúng một bucket, required/available/missing chính xác |
| E5 | Thứ tự câu/options thay đổi an toàn, đáp án không đổi ý nghĩa | Test ID options, multiple exact-set, câu khóa shuffle |
| S1 | Single/true-false đúng full, sai/bỏ trống 0; multiple exact-set, không partial/âm | Unit tests mọi tổ hợp, lựa chọn thừa/thiếu/ID lạ |
| S2 | Essay pending không bị coi là sai; rubric không vượt điểm max; blank=0; điểm cuối ghi self-graded | Unit + UI tests pending/partial/full/invalid rubric, mức 0/0,5/1 và half-up 0,01 ở cuối mỗi câu; tổng Phase/Track/Topic khớp tổng bài |
| T1 | 90 phút tính bằng deadline tuyệt đối, không theo số callback timer | Fake-clock tests tại start, trước hạn, đúng hạn, sau hạn và tab bị throttle |
| T2 | Reload/đóng tab/mở lại giữ thứ tự đề, options, đáp án, thời gian; quá hạn khóa và nộp khi resume | Integration + E2E test restart, change visibility, persisted expired attempt |
| T3 | Không chấp nhận câu trả lời sau deadline; nộp tay/tự động/retry/hai tab chỉ một kết quả | Transaction race tests; timestamp hợp lệ, một history record |
| P1 | Lưu sau mỗi thay đổi và trước điều hướng hoàn tất; lỗi/quota không giả báo thành công | Fault injection persistence, reload sau commit, lỗi giữa transaction |
| P2 | Import invalid/unknown version/duplicate không ghi một phần; backup round-trip giữ dữ liệu | Integration test atomic import/export/migration; external approved được staging |
| P3 | Sửa/xóa bank hiện hành không làm đổi điểm lịch sử | Snapshot test trên revision ngân hàng khác |
| U1 | Daily/Track/Phase/Mixed lọc đúng; câu sai và bookmark có luồng luyện lại | E2E mỗi chế độ + empty/filter combinations; có nhãn Day không mập mờ |
| U2 | Thi không lộ đáp án/explanation/rubric trước nộp trong UI; sau nộp hiển thị đầy đủ | E2E navigation + submit; pending score rõ ràng |
| U3 | Dashboard có lịch sử, thống kê và đề xuất ôn dựa trên sai/bỏ trống | E2E nhiều bài có điểm tự luận chưa chấm, mẫu số/empty state đúng |
| U4 | Mobile 360/390px, tablet 768px, desktop 1440px sử dụng được | Screenshot/kiểm tra thủ công, không tràn ngang, focus/keyboard/labels/contrast |
| R1 | Typecheck, unit, integration, E2E, production build chạy bản tích hợp cuối | Lệnh thật, exit code, phiên bản môi trường, log, screenshot; không thay bằng báo cáo agent |
| R2 | Không lỗi console/runtime ở luồng chính; không secrets/nguồn bị sửa | Log trình duyệt, Git diff nếu đã init, hash nguồn, release checklist |
| R3 | README hướng dẫn install/dev/test/build/deploy và backup; hạn chế/coverage công khai | README, QA report, coverage report, known-issues; không lỗi nghiêm trọng mở |

## Kế hoạch chạy test

Đề xuất Vitest cho domain và integration, Playwright cho E2E sau khi duyệt stack; validator schema có thể dùng Ajv 2020-12, phiên bản chốt lúc scaffold. Chỉ viết script package khi triển khai. Test cần tập trung quota theo điểm, slot feasibility, thời gian, transaction và grade; không chỉ kiểm tra snapshot cấu trúc implementation.

Unit/integration dùng fixture riêng, tuyệt đối không lẫn vào release học thuật. E2E triển khai dùng ngân hàng phát hành thực trong browser context mới để kiểm cả dữ liệu tích hợp và luồng UI; câu trả lời thử nằm trong context kiểm thử. Nội dung nguồn thật được kiểm định riêng, không dùng test code để “chứng minh” kiến thức đúng. Kiểm tra đáp án ẩn áp dụng UI, không phải bảo mật đáp án trước người có DevTools.

## Báo cáo QA bắt buộc

Mỗi lần chạy ghi run ID, commit hoặc hash artifact khi chưa có Git, môi trường, command, actual result/pass/fail/not-run, log/screenshot path. Mỗi lỗi có severity, steps to reproduce, expected/actual, module owner, fix revision và retest. `not-run` không tương đương pass. Root mở artifact/test output trên bản tích hợp cuối; chỉ gate được đáp ứng mới chuyển milestone.
