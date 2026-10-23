# Independent code gate — câu tính toán Track 4

**PASS cho code diff hiện tại**, không có finding major/critical mở. Phạm vi: optional `calculation` trong schema/types; `practicePool`/`selectExam`; bộ lọc Dạng bài và mô tả đề trong App; fixtures/domain/browser tests; release validator, coverage và negative fixture. Không sửa code hoặc bank.

- `calculation` không required nên câu/snapshot cũ thiếu flag vẫn hợp lệ. Backup validation không gọi selector mới; câu và điểm snapshot đã lưu tiếp tục được sử dụng. Đây là kiểm tra đường code, không tuyên bố đã import một backup người dùng thực.
- Calculation minimum xét pool đã approved, đúng revision, nguồn verified và taxonomy/catalog phù hợp, chỉ objective Phase2 Track4. Selector lấy hai calculation trước, loại IDs đã chọn khỏi ba slot còn lại; có thể lấy thêm calculation. Không bù Track khác, không lặp, thiếu hai câu thì báo lỗi trước tạo đề. Slot điểm/60 câu/36–24 và 60–40 điểm không đổi.
- Practice filter giữ giao với phase/track/topic/difficulty và review IDs; App dùng cùng pool để đếm và launch. Flag chỉ là metadata đã duyệt, không tự chứng minh câu có phép tính đúng.
- Python release gate yêu cầu ít nhất hai objective calculation Track4, đồng thời các gate approved/exact revision/source khác vẫn áp dụng. Coverage count mới không thay semantic approval.

Reviewer thực chạy `npm test -- src/domain/quiz.test.ts`: **16/16 pass**, gồm ba test mới về filter, shortage/unapproved và 100 seeds với pool dư + trọng số lẻ. Đã đọc browser test mới cho filter/reload và assertion ≥2 calculations ở hai đường exam; **chưa tự chạy browser/build hoặc negative Python fixture** trong gate code này. Root báo 54 unit/typecheck pass; ghi nhận riêng, không coi là kết quả tự chạy.

Release bank1284, nội dung 24 câu mới và browser trên production build cần kết quả riêng sau emit; PASS này không phê duyệt nội dung hay công bố đã kiểm bản live mới.
