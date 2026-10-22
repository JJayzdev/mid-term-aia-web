# Independent code review — release gate

Reviewer: `reviewer`, 2026-10-22. Phạm vi bản tích hợp được Root xác nhận đóng băng tại `c307d6b`; không chỉnh sửa mã ứng dụng trong audit này.

**Kết luận: không còn lỗi major/critical mở trong phạm vi đã kiểm tra. Có thể chuyển gate phát hành cho ứng dụng tự học cục bộ.** Đây không phải cam kết không có lỗi hoặc chứng nhận hệ thống thi có giám sát.

## Phạm vi đã đọc

Đối chiếu `docs/ACCEPTANCE_CRITERIA.md` với `src/domain/quiz.ts`, `grading.ts`, `rational.ts`, `validation.ts`, `src/storage/database.ts`, `src/components/QuizSession.tsx` và các test tương ứng. Tập trung quota theo điểm, exact-set, rubric pending/rounding, deadline, hàng đợi lưu, writer ownership/CAS, nộp idempotent, snapshot và import/restore nguyên tử.

- Blueprint dùng bucket không giao nhau, approved đúng revision, seed/thứ tự ID ổn định; kiểm tra thiếu bucket trước tạo đề. Điểm 60/40, khách quan/rubric 90/10 và track weights có kiểm tra biểu diễn chính xác.
- Rubric tính bằng rational, half-up một lần mỗi câu; câu có nội dung chưa tự chấm không bị coi là sai. Snapshot giữ câu/đáp án/điểm của lịch sử.
- IndexedDB read-write transaction kiểm tra revision và writer token; deadline được kiểm tra trước lưu/nộp, auto-submit dùng deadline logic. Các thao tác nộp lặp trả kết quả hiện có.
- Import ngoài bị staging; restore kiểm tra snapshot, đáp án, điểm tính lại và xung đột trước ghi trong cùng transaction. Không tự kích hoạt ngân hàng do tệp lạ tự ghi approved.

## Finding và retest

| ID / mức | Đường dẫn và tái hiện | Sửa và trạng thái |
|---|---|---|
| QR-01 / major | `QuizSession.tsx`: gõ tự luận nhanh khi nhiều write đang xếp hàng; từng `finally(false)` cũ có thể hiện “Đã lưu” trước write cuối. | Đổi sang bộ đếm pending và ref, chỉ hết lưu khi hàng đợi cạn. Test giữ write thứ hai chưa resolve xác minh indicator. **Đóng sau retest.** |
| QR-02 / major | `QuizSession.tsx`: gây quota/save failure khi sửa tự luận, sau đó chuyển câu hoặc nộp. Catch cũ làm queue resolve; chuyển câu xóa draft, nộp có thể dùng phần đã commit cũ. Root cũng tái hiện trên production build trước sửa. | Giữ chính xác draft lỗi, nút thử lưu lại, chặn chuyển câu/thoát/nộp khi chưa lưu; báo lỗi trong phiên. Test failure→retry→submit và browser production do Root chạy đạt. **Đóng sau retest.** |
| QR-03 / major, Root phát hiện khi sửa | Với phiên thi đã hết hạn và đã nộp, kiểm tra deadline trước nhánh submitted từng chặn xem câu khác; write qua hạn có thể bị thông báo thành công dù giá trị bị loại. | Nhánh submitted review đặt trước deadline; kiểm tra đáp án thực trong kết quả write đã finalized, giữ draft bị loại và cảnh báo không tính. Đã đọc lại mã và test hai đường này. **Đóng sau retest.** |

Hiện tại các guard dùng ref để không phụ thuộc render state cũ; auto-submit vẫn hoạt động khi lỗi lưu và chỉ tính dữ liệu đã commit. Không có yêu cầu sửa mã còn chờ từ Reviewer.

## Bằng chứng thực chạy

Reviewer tự chạy tại workspace:

```text
npm test -- src/components/QuizSession.test.tsx src/storage/database.test.ts src/domain/quiz.test.ts src/domain/grading.test.ts src/domain/validation.test.ts
```

Exit code 0; 5 test files, **46/46 tests passed**, Vitest 5.0.5, thời điểm 14:45:22. Bao gồm failed-save/retry, queue indicator, review sau nộp, write qua hạn, CAS/two writers, submit race, backup conflict atomicity, exact quota trên nhiều seed và rubric rounding. Reviewer đọc lại các nhánh sửa cuối; không chạy lại toàn bộ browser suite riêng.

Đã mở `tmp/qa/production-browser-results.json`: **12 expected, 0 skipped, 0 unexpected, 0 flaky, errors=[]**, duration 35.289 giây; đây là kết quả production browser do **Root thực thi**, không gán là Reviewer tự chạy. Root báo full suite **48/48** và production build đạt; hai test ngoài lệnh focused của Reviewer là analytics/published-content. Báo cáo nghiệm thu tổng hợp thuộc `reports/qa/RELEASE_QA.md`.

## Giới hạn còn lại

Chưa có nghiệm thu đa trình duyệt/thiết bị thực toàn diện, kiểm thử migration lên DB version tương lai hoặc đo dung lượng dài hạn. Đồng hồ và dữ liệu phía client có thể bị người dùng sửa; không có server time, đồng bộ thiết bị hay tác vụ nộp khi trình duyệt đóng. Các giới hạn này phù hợp phạm vi tự học đã công bố. Test code không chứng minh nội dung học thuật đúng; nội dung có audit riêng từng batch trong `reports/content/`.
