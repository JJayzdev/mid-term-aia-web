# Mở rộng ngân hàng câu hỏi — Author A

Đã tạo **535 câu mới**, 11 batch, cho 32 PDF được phân công. Tất cả `pending_review`, `author_id=question-engineer-a`; không thay đổi approved hoặc tự duyệt.

| Batch | PDF | Câu mới | Trang vật lý khác nhau/PDF |
|---|---|---:|---|
| A001 | P1 Day1–3 | 50 | 14 / 16 / 16 |
| A002 | P1 Day4–6 | 51 | 17 / 16 / 15 |
| A003 | P1 Day7–9 | 51 | 15 / 16 / 16 |
| A004 | P1 Day10–12 | 50 | 17 / 16 / 17 |
| A005 | P1 Day13–15 | 50 | 16 / 16 / 14 |
| A006 | T1 Day1–3 | 51 | 15 / 16 / 15 |
| A007 | T1 Day4–6 | 51 | 17 / 14 / 16 |
| A008 | T1 Day7–9 | 51 | 16 / 14 / 17 |
| A009 | T1 Day10–11 | 34 | 16 / 16 |
| A010 | T4 Day7–9 | 48 | 15 / 15 / 16 |
| A011 | T4 Day10–12 | 48 | 16 / 16 / 16 |

Cộng baseline105 câu,32 PDF hiện có **640 ứng viên**, đúng20/PDF. P1:252mới+48cũ=300; T1:187+33=220; T4Day7–12:96+24=120. Đây là số ứng viên, chưa phải số reviewer thông qua.

Mỗi câu có documentID,SHA-256 và physical PDF page; curriculum theo chính sách folder/filename của root. Đã đọc section map và nội dung các trang trích dẫn; tránh số liệu thời sự, quy định pháp luật, benchmark chưa cân bằng và công thức OCR không rõ. Ví dụ tính toán nêu rõ hằng số. Không coi OCR là chứng nhận nguồn; reviewer cần mở PDF gốc.

Sau spot-check,145 câu có lựa chọn A001–003 được biên tập sang nhầm lẫn cùng khái niệm/workflow. Ưu tiên3 lựa chọn đáng tin thay vì thêm filler; MC có2/3,2/4,3/4 đáp án đúng. A001 sửa riêng standalone context,response schema,TF fragment và streaming ambiguity,tăng revision. Câu mới không hỏi đọc slide/nhớ lời giảng.

`python scripts/content/expand_a_validate.py` xác nhận535 câu qua schema,uniqueIDs,author/status,source hashes/page bounds,option/answerIDs và stem scan. Kiểm này không thay thế kiểm nguồn,distractor ambiguity và near-duplicates xuyên tác giả. Batches đã gửi root/reviewer từng đợt; phản hồi tiếp theo cần sửa có revision và kiểm lại trước tích hợp.
