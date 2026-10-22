# Independent review — đề thi 60 câu

Ngày 2026-10-22, Reviewer `reviewer`. Phạm vi chỉ thay đổi blueprint/UI đề thi; không duyệt thêm câu hỏi hoặc kết luận yêu cầu “20 câu/slide” đã được làm rõ.

**Gate: không có lỗi major/critical mở trong thay đổi đề 60 câu đã kiểm tra.** Có thể phát hành phần đề thi độc lập với kế hoạch mở rộng ngân hàng.

Đã đọc diff `src/domain/quiz.ts`, `types.ts`, `quiz.test.ts`, `src/test/fixtures.ts`, phần cấu hình/hiển thị trong `src/App.tsx`; đối chiếu grading, lưu snapshot và restore hiện hành.

- Số câu đúng: Phase 1 = 34 khách quan + 2 rubric = 36; Phase 2 = 4 × (5 khách quan + 1 rubric) = 24. Tổng 60, gồm 54 khách quan và 6 rubric.
- Điểm tối đa vẫn 100: Phase 1 = 54 + 6 = 60; Phase 2 = 36 + 4 = 40; khách quan 90, rubric 10. Deadline 90 phút không đổi.
- Phân chia centipoints dùng thương/phần dư nguyên. Phase 1 khách quan: 28 slot ×159 + 6×158 = 5.400 units; không làm tròn tổng quota. Mỗi track mặc định 5×180 +100 =1.000 units. Custom weights giữ đúng tổng bucket; cấu hình không biểu diễn được bị từ chối.
- Mỗi câu được lấy không hoàn lại, giữ points và optionOrder trong snapshot; không lấy bucket khác bù khi thiếu. Điểm dư một unit được gán ổn định theo thứ tự ID đã chọn rồi xáo thứ tự hiển thị; độ chênh trong bucket tối đa 0,01 điểm.
- Tương thích lịch sử: `AttemptQuestion` vẫn giữ trường `points`; `slotPoints` chỉ là kiểu blueprint lúc tạo đề, không thay định dạng persisted attempt. Grading/results/restore dùng danh sách câu và điểm snapshot, không bắt lịch sử phải có 60 câu. Vì vậy phiên 36 câu cũ không bị tái sinh theo blueprint mới. Kết luận này dựa kiểm tra mã và test snapshot hiện có; chưa chạy riêng fixture backup 36 câu thực từ người dùng.

Reviewer tự chạy:

```text
npm test -- src/domain/quiz.test.ts src/domain/grading.test.ts src/storage/database.test.ts
```

Exit 0, **34/34 tests**, 3 files, Vitest 5.0.5, bắt đầu 15:46:40. Bao gồm 100 seeds mặc định, 100 seeds custom weights, phân dư 159/158 và 175/174, counts/uniqueness/quota, thiếu bucket, snapshot stability, grading và backup transaction. Root/A2 báo full suite 50 tests và build đạt; Reviewer không ghi các lượt đó thành kiểm tra tự chạy. Browser đề 60 câu do Root phụ trách, chưa tính là bằng chứng tự thực thi trong báo cáo này.

Không review lại 204 câu đã audit; chưa phê duyệt ngân hàng mở rộng 20 câu/PDF hay 20 câu/trang. Mọi câu mới vẫn phải có ID/revision, nguồn/trang/hash và audit ngữ nghĩa độc lập trước phát hành.
