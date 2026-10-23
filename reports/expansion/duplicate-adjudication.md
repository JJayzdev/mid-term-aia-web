# Rà soát câu gần trùng

Root đọc stem, lựa chọn, đáp án và giải thích của từng cặp trong `duplicate-candidates.json`. Điểm giống từ vựng chỉ tìm ứng viên; không tự quyết định trùng mục tiêu học tập. Báo cáo này bổ sung kiểm duyệt nguồn theo revision ở `reports/content/`.

Các cặp đã được tác giả thay nội dung và reviewer kiểm tra lại gồm IoU, ADKAR, Cohen's kappa, gradient checkpointing và một mục tiêu RAG quá gần câu cũ. Không giữ các biến thể chỉ đổi cách diễn đạt để đủ số lượng.

## Chín cặp còn lại sau lần quét 1.260 câu

Quét lại sau khi bổ sung 24 bài tính (1.284 câu): vẫn đúng chín cặp dưới đây, không xuất hiện cặp mới ở ngưỡng từ vựng 0,55. Các bài tính đã được kiểm riêng về mục tiêu, dữ kiện và đáp án trong `expand-root-calculation`.

| Cặp ID | Quyết định và lý do |
|---|---|
| `p2-t4-d09-x11` / `p2-t2-d12-x14` | Giữ: model lineage truy từ model về dataset/quy trình; column lineage truy nguồn ở cấp cột và phân biệt table/run/ownership lineage. |
| `p1-d13-x03` / `p2-t2-d05-q03` | Giữ: Phase 1 định nghĩa TTFT; Track 2 phân biệt TTFT với TPOT và lý do cần hai chỉ số. Có kiến thức nền chung nhưng mức phân biệt khác. |
| `p1-d13-x03` / `p2-t2-d08-x03` | Giữ: TTFT và RTO là hai đại lượng khác; chỉ giống cấu trúc câu “đo khoảng thời gian nào”. |
| `p2-t1-d07-q02` / `p2-t1-d07-q03` | Giữ: một câu nhận biết cấu trúc hybrid pricing; câu nhiều đáp án hỏi tác động đến cost của power user và margin. |
| `p2-t2-d05-x11` / `p2-t2-d11-x03` | Giữ: lựa chọn workload prefill-heavy phù hợp với disaggregation khác giải thích right-sizing hai pool theo compute/bandwidth. Cả hai đều nêu giới hạn KV-transfer overhead. |
| `p1-d13-x03` / `p2-t1-d06-x02` | Giữ: TTFT về inference, Time to Value về giá trị sản phẩm; chung cấu trúc câu hỏi thời gian. |
| `p2-t1-d06-x02` / `p2-t2-d08-x03` | Giữ: Time to Value và RTO thuộc hai mục tiêu khác nhau. |
| `p1-d08-q01` / `p1-d08-q03` | Giữ: tình huống cần truy xuất policy nội bộ có nguồn, so với nhận diện đồng thời các trường hợp giải pháp đơn giản đã đủ hoặc không có corpus riêng. Hai câu bổ sung ranh giới lựa chọn RAG; có phần kiến thức chung được chấp nhận. |
| `p2-t1-d06-x11` / `p2-t1-d09-x03` | Giữ: chọn core action gắn giá trị use case khác quy định inclusion/exclusion để người đọc không đếm “active” theo nhiều nghĩa. |

Không phát hiện ID trùng hoặc stem trùng hoàn toàn sau chuẩn hóa. Việc không xuất hiện trong danh sách giống từ vựng không chứng minh mọi câu đều độc nhất về ngữ nghĩa; đánh giá trong từng bài và đối chiếu câu cũ nằm trong review batch.
