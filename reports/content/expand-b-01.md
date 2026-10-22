# Kiểm định độc lập B01

Kết quả: **51/51 approved** tại đúng revision trong JSON. Đã đọc toàn bộ câu hỏi, phương án, đáp án và giải thích; đối chiếu trực quan 43 trang PDF vật lý đang được trích dẫn của T2 Days 1–3. Ảnh nguồn ở `tmp/reviewer/expand-b-01/`. Một ảnh p31 cũ được giữ làm lịch sử nhưng không dùng để xác nhận câu timeout mới p30.

Đã chạy lại JSON Schema bằng jsonschema và SHA256 của cả ba PDF so với catalog. Các kiểm tra này hỗ trợ cấu trúc/định danh; quyết định nội dung dựa trên đọc nguồn và đánh giá từng câu, không suy từ schema pass.

## Findings và retest

- Đã đóng bốn vấn đề r3: data residency không suy từ thương hiệu; PrivateLink không bảo đảm giảm cost vô điều kiện; embedding cache không phụ thuộc nhãn tầng tùy ý; timeout thay câu graph state trùng A001.
- Các câu d03 x04/x10/x11/x12/x14/x17 đã thay mục tiêu trùng hoặc quá gần A001 và được kiểm lại nguồn cụ thể. D02 x03 và x10 được giữ vì lần lượt kiểm vai trò khóa thực thể và lựa chọn kỹ thuật CDC.
- D03 x03: yêu cầu bỏ cách diễn đạt agent là bắt buộc; workflow cố định vẫn có thể gọi API. Artifact phản ánh chính revision được kiểm sau sửa.

## Giới hạn

Đây là gate nội dung batch B01; không phải xác nhận toàn bộ 1056 câu mới hoặc kiểm thử sản phẩm. Không dùng giá cloud, phiên bản hay nghĩa vụ pháp lý thay đổi theo thời gian làm đáp án số liệu hiện hành. Không sửa draft hoặc public bank.

## Bằng chứng từng câu

- **p2-t2-d01-x01 r3 approved**: p8: Tiêu chí VN data residency và compliance hỗ trợ a; không suy từ thương hiệu ra vị trí thực tế. r3 đóng phạm vi chọn provider. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x02 r2 approved**: p9: Specialized GPU cloud ít managed services và cần năng lực ops; b đúng, các lựa chọn SLA/AZ/managed tuyệt đối không phù hợp đánh đổi. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x03 r2 approved**: p12: SCP là guardrail enforce security baseline; a đúng. Audit và lời khuyến nghị không phải cơ chế cưỡng chế. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x04 r2 approved**: p15: Training có thể gián đoạn/resume phù hợp Spot/Preemptible; d đúng. Không dùng Spot để bảo đảm endpoint liên tục. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x05 r2 approved**: p17: MIG tạo instance cô lập cho nhiều model nhỏ; c đúng. Replica giữ toàn GPU hay overcommit không tạo phân vùng tương đương. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x06 r2 approved**: p19: S3 backend + DynamoDB lock là cặp quản lý state nhóm được trình bày; b đúng. Đây là cấu hình nguồn, không khẳng định lựa chọn duy nhất hay API mới nhất. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x07 r2 approved**: p19: Module để reuse, workspace tách state môi trường; a đúng. Hai distractor đảo vai trò hoặc dùng chung state. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x08 r2 approved**: p22: Đặt dependency layer trước COPY source giữ cache khi source đổi; d đúng. Không thay việc pin dependency. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x09 r2 approved**: p22: NVIDIA GPU requests=limits=1; c đúng. requests=0 hoặc requests>limits sai cấu hình yêu cầu. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x10 r2 approved**: p22: ml-serving tách RBAC và production isolation; b đúng. Chỉ đổi tên hoặc gộp experiments không đạt mục tiêu. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x11 r3 approved**: p24: PrivateLink tránh đường internet; a r3 chỉ nói có thể tiết kiệm egress trong kiến trúc phù hợp. Đã bỏ bảo đảm tiết kiệm vô điều kiện. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x12 r2 approved**: p25: Hot tier phục vụ active KV/embedding cache/session với độ trễ thấp; d đúng, archive/checkpoint ít đọc thuộc tầng khác. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x13 r2 approved**: p28: Supervisor chỉ dispatch dùng CPU, specialist inference LLM cục bộ dùng GPU; c đúng với điều kiện stem. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x14 r2 approved**: p28: Kafka nhắm throughput/durability/replay quy mô lớn; b đúng. Redis Streams và RabbitMQ được đặt ở ưu tiên khác, không phủ nhận chúng có khả năng lưu bền. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x15 r3 approved**: p28: Embedding cache tránh embed lại query; a r3 mô tả cơ chế thay vì buộc nhớ nhãn L3. Cache weights/raw documents không giữ query vector. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x16 r2 approved**: p31: RadixAttention tái sử dụng KV của prefix chung; d đúng. Cùng độ dài/suffix/tenant không bảo đảm token prefix chung. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d01-x17 r2 approved**: p31: max_model_len điều chỉnh theo usage thực tế; c đúng. Dư context hay sát 100% memory không phải giải pháp phù hợp. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x01 r2 approved**: p10: Bronze nguyên bản cho phép rebuild Silver khi logic cũ sai; b đúng. Postgres hiện trạng không thay lịch sử hai tháng. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x02 r2 approved**: p11: Silver hợp nhất một ticket thành một hàng thực thể; a đúng theo mô hình đã nêu. Ba events không phải ba thực thể. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x03 r2 approved**: p12: Khóa không null/không trùng giúp MERGE đúng thực thể qua retry; d đúng. Mục tiêu là ý nghĩa khóa, khác câu x10 chọn kỹ thuật CDC. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x04 r2 approved**: p14: Replication slot không được đọc giữ WAL và có thể đầy đĩa nguồn; c đúng. CDC không full-scan từng thay đổi và có DELETE. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x05 r2 approved**: p15: Airbyte phù hợp connector OSS nhiều SaaS/ngân sách hẹp; b đúng. Giải thích giữ đánh đổi chất lượng connector. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x06 r2 approved**: p16: Parquet đọc cột cần và predicate pushdown; a đúng. JSON gzip/Avro row/Arrow RAM không có cùng vai trò lake column scan. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x07 r2 approved**: p18: ref() tạo dependency graph và thứ tự chạy dbt; d đúng. Không ép materialization thành table. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x08 r2 approved**: p19: Thiếu bộ lọc is_incremental có thể quét lại lịch sử; c đúng, stem có điều kiện có thể. Không tự sinh lookback hoặc dedup. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x09 r2 approved**: p20: SQLMesh phân tích tác động thay đổi và virtual environment; b đúng với backfill/dev cost. Không dùng chung production để né môi trường. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x10 r2 approved**: p21: Bảng thực thể nhận CDC phù hợp MERGE/upsert theo khóa tin cậy; a đúng. Mục tiêu lựa chọn kỹ thuật idempotent, không chỉ định nghĩa khóa x03. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x11 r2 approved**: p22: Nhãn đến muộn tạo version mới, không sửa snapshot training cũ; d đúng. Các phương án ghi đè làm mất reproducibility. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x12 r2 approved**: p23: SCD2 giữ valid_from/valid_to để truy vấn trạng thái quá khứ; c đúng. Overwrite không trả lời được point-in-time. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x13 r2 approved**: p24: Pandera kiểm schema DataFrame trong Python; b đúng. Distractor Pydantic/dbt/GE mô tả sai phạm vi hoặc điều kiện vận hành. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x14 r2 approved**: p26: Trino truy vấn liên kho S3/Postgres/Kafka; a đúng. Các distractor không biến batch inference hoặc single-process thành federation. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x15 r2 approved**: p29: Compaction và giảm task ghi xử lý overhead mở/footer của file nhỏ; d đúng. Cardinality cao tạo thêm file nhỏ. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x16 r2 approved**: p32: Retention 24 giờ không đủ replay ba ngày; c đúng. Offset không giữ bản sao message đã bị xóa. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d02-x17 r2 approved**: p39: Temporal durable execution/retry runtime cho workflow nhiều ngày; b đúng. Không dùng SQL engine để thay orchestration state. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x01 r2 approved**: p7: Agent có chu trình quyết định-hành động-quan sát-lặp; a đúng. Thêm chat/history hoặc flow API cố định chưa đủ. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x02 r2 approved**: p8: Agent thêm tool misuse và loop ngoài hallucination; d đúng. Công cụ không bảo đảm đúng mặc định. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x03 r3 approved**: p9: Gọi tool lấy dữ liệu mới và tổng hợp điều kiện là lợi ích reactive agent; c đúng. Retest stem bỏ khẳng định agent bắt buộc. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x04 r2 approved**: p29: search_flights nhận max_price trong args để truyền ràng buộc ngân sách có cấu trúc; a đúng, không bỏ hoặc trì hoãn lọc ngân sách. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x05 r2 approved**: p14: FAQ intent ổn định/retrieve policy phù hợp chatbot retrieval; a đúng. Không cần autonomy nhiều vòng mặc định. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x06 r2 approved**: p15: Các bước nối tiếp đã rõ dùng prompt chaining; d đúng, không cần routing hoặc worker khi thiếu cấu trúc tương ứng. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x07 r2 approved**: p17: Perception nhận tool output; c đúng. Nhận dữ liệu không đồng nghĩa reasoning hoặc ghi long-term memory. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x08 r2 approved**: p18: Long-term memory cần retrieval strategy và permission model; b đúng. Storage tăng đơn thuần không định nghĩa đọc/ghi an toàn. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x09 r2 approved**: p19: Tool definitions cần input/output/error mode; a đúng. Bỏ output hay failure contract làm thiếu thông tin vận hành. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x10 r3 approved**: p27: Code thêm output.as_message và tool_message(name,result); a đúng. Đã thay câu Observation trùng A001 bằng mục tiêu message protocol. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x11 r3 approved**: p17: Memory giữ goal/facts/intermediate results; a đúng. Đã thay câu trace trùng A001, không giới hạn memory chỉ final answer. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x12 r3 approved**: p27: final_answer return trước run_tool; a đúng. Kiểm trực tiếp nhánh code, không bịa result hoặc ép gọi tool. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x13 r2 approved**: p28: System prompt yêu cầu giải thích tool failure và thử fallback; a đúng. Đây là xử lý trung thực khi lỗi, khác tình huống bounded retry đã thất bại của A001. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x14 r3 approved**: p34: rain=.7 thỏa nhánh đầu và return trước nhánh nhiệt độ; a đúng. Kiểm ảnh code thấy ngưỡng nhiệt độ 30, distractor 33 không làm thay đổi đáp án. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x15 r3 approved**: p30: Timeout từng tool chặn call treo dù có max iterations; a r3 đúng. Đã thay graph state trùng A001 bằng giới hạn thời gian dependency. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x16 r2 approved**: p35: Checklist debug kiểm tool selection/args/observation trong trace; b đúng. Final answer hợp lý không chứng minh action đúng. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
- **p2-t2-d03-x17 r3 approved**: p40: Cùng test cases trên chatbot và agent giữ đầu vào so sánh nhất quán; a đúng. Không chọn demo hoặc bộ test thiên lệch. Đã kiểm stem, options, answer và explanation với trang PDF vật lý.
