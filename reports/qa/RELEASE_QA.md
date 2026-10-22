# Release QA — AIA Study v1

Run ngày 2026-10-22. Root thực thi trên bản tích hợp thật; không chỉ dùng kết luận của tác giả. **Kiểm tra local đã đạt; code review độc lập và kiểm tra URL sau deploy được cập nhật ở phần trạng thái cuối.**

## Nội dung phát hành

- Bank `2026.10.22-cb4b0a35c49b`, schema `1.0.0`: **204 câu approved / 63 tài liệu có câu đại diện**, không có câu bị bỏ vì chưa duyệt.
- Phase 1: 48 câu; Track 1/2/3/4: 33/36/39/48 câu. 191 câu khách quan và 13 câu rubric; đủ mọi bucket của blueprint.
- 79 single-choice, 54 multiple-choice, 58 boolean, 13 rubric (phân loại answer format; câu scenario được tính theo hình thức chấm).
- 124 trang nguồn khác nhau được dẫn. Toàn corpus có 3.589 trang; câu hỏi không bao phủ toàn bộ khái niệm. Độ khó: 6 easy, 194 medium, 4 hard; mức nhận thức: 182 understand, 20 apply, 2 analyze. Đây không phải ngân hàng đã hiệu chỉnh độ khó bằng dữ liệu người học.
- Tất cả câu có audit độc lập đúng revision trong `reports/content/`. Hai cặp gần trùng và các distractor yếu đã được tác giả sửa, reviewer kiểm tra lại; lịch sử quyết định được giữ trong báo cáo batch.
- Ingestion đủ 63 PDF, 3.240 trang OCR + 349 trang native, 0 lỗi xử lý. Ba trang không text được xem ảnh và không dùng làm câu hỏi. `--verify-sources` xác nhận hash toàn bộ nguồn không đổi.

## Lệnh và kết quả thực tế

Môi trường: Windows, Node 24.14.1, npm 11.11.0, Python 3.9.13 + jsonschema; Chrome cài sẵn, Playwright 1.64.1, Vitest 5.0.5, Vite 7.3.7.

| Kiểm tra | Kết quả | Bằng chứng local |
|---|---|---|
| `python scripts/content/validate_drafts.py` | PASS, 204 câu/63 tài liệu | Draft schema/IDs/options/rubric/source bounds |
| `python scripts/release_bank.py` | PASS, 204 approved, 0 omitted | `reports/content/release-summary.json` |
| `python scripts/validate_release.py --verify-sources` | PASS, errors=[] | `tmp/qa/release-validation.txt` |
| `npm test -- --reporter=json --outputFile=tmp/qa/unit-results.json` | PASS, 48/48 tests, 7 files | `tmp/qa/unit-results.json` |
| `npm run build` (bao gồm TypeScript) | PASS | `tmp/qa/build.txt`, `dist/` |
| `npx playwright test --config scripts/qa/playwright.config.ts` | PASS, 12/12, 0 skipped/flaky, 35,3 giây | `tmp/qa/production-browser-results.json` |
| `npm audit --json` | PASS, 0 known vulnerabilities tại thời điểm chạy | `tmp/qa/npm-audit.json` |

Browser chạy **production preview**, không dùng Vite HMR cho lượt nghiệm thu. Test dùng ngân hàng phát hành thực; fixture chỉ nằm trong module tests và không vào public data. Bộ E2E bao gồm:

1. Daily: lưu/reload giữ đề, options và đáp án; bookmark và luyện câu sai.
2. Gõ tự luận nhanh, chuyển câu, nộp, reload, tiếp tục tự chấm.
3. Đề 36 câu, 100 điểm, 60/40 theo Phase, 90/10 theo dạng; mặc định mỗi Track 10 điểm; deadline đúng 90 phút, tự nộp, không lặp kết quả.
4. Hai tab chỉ một bên có quyền ghi.
5. Đóng tab khi thi, mở lại quá hạn: giữ đáp án trước hạn và tự nộp đúng deadline.
6. Trọng số 10/20/30/40; trả lời đúng toàn bộ khách quan qua UI cho điểm 90/100, tự luận bỏ trống = 0. Cấu hình trọng số bằng 0 bị chặn.
7. Export/restore sang browser context mới; JSON sai bị từ chối; ngân hàng imported approved vẫn vào vùng chờ.
8. Filter Phase/Track/topic/mixed giữ đúng phạm vi.
9. Inject QuotaExceededError: cảnh báo hiển thị, không ghi đáp án, không giả báo đã lưu.
10. Lỗi ghi tự luận giữ nguyên bản nháp, chặn chuyển câu/thoát/nộp tay; retry lưu đúng toàn bộ nội dung rồi tiếp tục được.
11. Năm route ở 360/390/768/1440 px không tràn ngang; screenshot được Root xem.
12. Menu, điều hướng quiz và kết quả ở màn hình điện thoại hoạt động; screenshot kết quả 360 px được Root xem.

Module tests thêm exact-set MC, rubric half-up bằng phân số chính xác, 100 seed quota/unique, thiếu bucket không bù nhóm khác, stale review/self-review bị chặn, CAS/submit race, backup collision atomic, snapshot bất biến và thống kê loại pending essays. Root E2E lắng nghe lỗi JavaScript và console.error; không có lỗi trong lượt đạt.

## Lỗi đã sửa và kiểm tra lại

- Phép tính rubric bằng floating point → số hữu tỷ BigInt, half-up một lần ở cuối câu.
- Mixed chọn cả hai Phase nhưng vô tình loại Phase 1 → chỉ lọc Track trên Phase 2.
- Reload bài pending không thể tự chấm do token cũ → nhận quyền sửa khi mở lại; tab cũ chỉ đọc.
- Shortcut Daily yêu cầu mặc định 10 câu khi ngày chỉ có 3–4 → mặc định giới hạn theo số khả dụng; cấu hình yêu cầu thiếu vẫn báo lỗi.
- Lỗi lưu bị ẩn và báo “đã lưu” sai → cảnh báo trong phiên + trạng thái lưu thất bại; inject quota test đạt.
- Root tái hiện mất bản nháp tự luận sau lỗi ghi (test trước sửa thất bại như dự kiến). Đã giữ bản nháp, thêm “Thử lưu lại”, chặn điều hướng/nộp tay khi chưa lưu thành công; bộ 12 E2E sau sửa đạt. Trạng thái đang lưu theo toàn bộ hàng đợi. Tự nộp hết giờ giữ đáp án đã commit và cảnh báo bản nháp bị loại; xem lại các câu sau hết giờ hoạt động.
- Blank bị đếm thêm vào wrong trong kết quả → hai bộ đếm riêng; danh sách luyện lại vẫn gồm blanks.
- Coverage note bị hero che trên điện thoại → layout tăng chiều cao theo nội dung, xem lại screenshot đạt.
- Vitest cũ có advisory → cập nhật 5.0.5, npm audit 0.
- Một số lần E2E ban đầu fail do selector nhãn đổi, assert trước khi điều hướng hoàn tất, và trace HTML kích hoạt Vite HMR. Đã sửa harness/chạy production; không tính các lần đó là PASS.

## Giới hạn và trạng thái cuối

- Chưa kiểm thử tự động Firefox/Safari, chưa có offline service worker hoặc đồng bộ đa thiết bị.
- Tự luận là self-grade, không phải chấm của giảng viên. Đáp án static và đồng hồ thiết bị phù hợp tự học, không phải thi có giám sát.
- Chỉ sample khái niệm từ 124 trang đã dẫn; toàn bộ OCR vẫn là `extracted_unverified`. Metadata theo thư mục/filename do Root chốt, bảo lưu xung đột nhãn bìa.
- Git source/PDF exclusion và scan token/private-key pattern đã kiểm tra; không phát hiện credential. Không đưa 407 MB PDF/cache lên repository hoặc website.
- **Đang chờ** kết luận `CODE_REVIEW.md` và URL production được xác minh trước tuyên bố release hoàn tất.
