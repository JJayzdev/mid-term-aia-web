# Audit phase1-remaining

**Kết quả hiện hành sau retest: 36 approved (21 câu revision2, 15 câu revision1).** Đã hash12 PDF khớp catalog và render/xem trực tiếp12 trang vật lý được dẫn tại `tmp/reviewer/phase1/`. Xem từng đáp án/explanation/distractor và rubric scenario d09; không chỉ validate schema. Mapping theo policy Root, giữ source labels riêng.

## Giới hạn chất lượng/coverage

Đây là starter bank: mỗi tài liệu chỉ lấy một trang, không chứng minh bao phủ toàn bài. Nhiều distractor rất dễ loại (màu/logo/README), các multiple choice a+b và đa số single b; xáo option giúp giảm đoán vị trí nhưng không cải thiện độ sâu. Không nên trình bày đây là bộ thi đã hiệu chỉnh độ khó hoặc đánh giá toàn bộ curriculum. Có gần nhau trong một chủ đề; không thấy trùng nguyên câu, song nên mở rộng câu vận dụng và nguồn trang ở batch sau.

## Từng câu

- **p1-d02-q01 r1 rejected — MAJOR distractor**: p12: Bốn câu hỏi chẩn đoán ghi rõ công đoạn khó khăn; b đúng, các lựa chọn model/màu/bỏ quy trình không thuộc chẩn đoán. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d02-q02 r1 approved**: p12: Kết luận chưa hiểu điểm đau chưa đề xuất; false đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d02-q03 r1 approved**: p12: Lăng kính lặp lại và tốn thời gian có trong bảng; a,b đúng, model lớn/thay mọi quy trình không có. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d04-q01 r1 rejected — MAJOR distractor**: p9: Loop engineering ghi lặp thế nào/dừng khi nào; c đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d04-q02 r1 approved**: p9: Context engineering ghi một lần gọi model thấy gì; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d04-q03 r1 approved**: p9: Harness runtime có sandbox/quyền/trace; a,b đúng; một message là prompt, gói một lần gọi là context. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d10-q01 r1 approved**: p5: RAG stale có thể fail silently không exception; b đúng, các distractor tuyệt đối trái bảng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d10-q02 r1 approved**: p5: Hợp đồng retrieval vừa liên quan vừa không stale/bị bản mới mâu thuẫn; false đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d10-q03 r1 approved**: p5: Hai vế retrieval đúng là a,b; từ giống/file mở được không bảo đảm. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d12-q01 r1 rejected — MAJOR distractor**: p10: Chú thích stateless vẫn memory bằng externalize state; b đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d12-q02 r1 approved**: p10: Config in env ghi không hardcode API key; false đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d12-q03 r1 approved**: p10: Checklist có health endpoint/graceful shutdown; a,b đúng, xóa log/chỉ kiểm UI trái checklist. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d13-q01 r1 approved**: p9: Observability hỏi câu mới không deploy và unknown failure; b đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d13-q02 r1 approved**: p9: Monitoring theo dõi câu đã biết, dashboard/alert, known-knowns; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d13-q03 r1 approved**: p9: Telemetry metrics/logs/traces; a,b đúng, screenshot/browser list không là ba tín hiệu này. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d15-q01 r1 rejected — MAJOR distractor**: p11: vLLM production inference cho GPU/high throughput; b đúng, Ollama DNS không được hỗ trợ. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d15-q02 r1 approved**: p11: Ollama dùng dev/demo/edge, setup đơn giản; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d15-q03 r1 rejected — MAJOR distractor**: p11: Tổng chi phí gồm GPU/ops/maintenance; a,b đúng, màu/README không thuộc so sánh chi phí. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d03-q01 r1 rejected — MAJOR distractor**: p14: Dynamic Decision hỏi bước tiếp phụ thuộc quan sát; b đúng, Long Horizon nói giữ mục tiêu nhiều vòng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d03-q02 r1 approved**: p14: Tool Interaction liệt kê search/API/database và tools; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d03-q03 r1 rejected — MAJOR distractor**: p14: Multi-step Reasoning và Long Horizon trong bốn tiêu chí; a,b đúng; avatar/số slide không thuộc bộ tiêu chí. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d05-q01 r1 rejected — MAJOR distractor**: p9: Cảnh báo chỉ functional có thể đúng chức năng nhưng không dùng lại; b đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d05-q02 r1 approved**: p9: Ô cảm xúc nêu tự tin hơn/ít sợ sai; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d05-q03 r1 rejected — MAJOR distractor**: p9: JTBD hỏi việc cần làm và cách được nhìn nhận; a,b đúng, layers/GPU không có trong ba nhu cầu. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d06-q01 r1 rejected — MAJOR distractor**: p10: Done cần quality threshold/latency/fallback/monitoring; thiếu hai mục chưa done, b đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d06-q02 r1 approved**: p10: Backlog liệt kê feature/data/technical debt; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d06-q03 r1 approved**: p10: Ví dụ support yêu cầu citation/escalation/testset; a,b đúng, demo/public URL không đủ. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d07-q01 r1 rejected — MAJOR distractor**: p13: Hàng heading/structural nói chunk trọn ý/metadata section, cần cấu trúc tốt; b đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d07-q02 r1 approved**: p13: Fixed-size đơn giản/cost nhưng cắt giữa câu/bảng; true đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d07-q03 r1 approved**: p13: Recursive tôn trọng ranh giới tự nhiên nhưng cắt nếu đoạn dài; a,b đúng; c tuyệt đối sai,d ảnh không khớp bảng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d08-q01 r1 approved**: p14: Cần RAG khi nội bộ đổi và citation kiểm chứng; b đúng, ba distractor thuộc chưa cần. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d08-q02 r1 approved**: p14: Kiến thức chung LLM biết thuộc chưa cần; false đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d08-q03 r1 approved**: p14: Không corpus/prompt đủ thuộc chưa cần; a,b đúng, policy/corpus giảm hallucination thuộc cần. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d09-q01 r1 approved**: p11: Đọc độc lập song song, sản phẩm chung một luồng ghi; b đúng, các cách ghi không điều phối trái nguồn. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d09-q02 r1 approved**: p11: Mệnh đề ghi đồng thời không điều phối trái nguyên tắc, false đúng. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.
- **p1-d09-q03 r1 approved**: p11: Scenario vận dụng đúng nguyên tắc đọc song song/ghi tuần tự. Rubric c1 chia đọc độc lập/c2 ghi có điều phối; partial cụ thể, tổng1, không đòi nguyên chuỗi. Explanation khớp trang gốc; không thấy đáp án đúng thứ hai trong options.

Không kiểm thử app, không xác nhận OCR toàn corpus đúng. Quyết định approve chỉ áp dụng ID/revision và trang đã xem; sửa nội dung phải review lại.

## Điều chỉnh gate distractor

Review ban đầu coi đáp án unambiguous là đủ, đã được sửa trước release: CONTENT_RULES còn yêu cầu distractor hợp lý. 11 câu sau bị rejected major, đã gửi A1 sửa; lịch sử nguồn đúng ở trên vẫn giữ, không đồng nghĩa approve.

- p1-d02-q01: landing page color.
- p1-d03-q01: prompt length/user count instead of neighboring Agentic Fit criteria.
- p1-d03-q03: avatar color/slide count.
- p1-d04-q01: UI styling.
- p1-d05-q01: GPU cost in JTBD.
- p1-d05-q03: model layers/GPU brand.
- p1-d06-q01: logo.
- p1-d07-q01: random character/file size chunking.
- p1-d12-q01: disable healthcheck unrelated to memory.
- p1-d15-q01: Ollama DNS/spreadsheet/compress source.
- p1-d15-q03: color/README lines.

Cần revision2 và retest distractor; không promote revision1 của11 câu này.

## Retest distractor revision2

Đã đọc21 câu revision2 (bao gồm11 câu rejected và10 câu tác giả chủ động cải thiện), đối chiếu các trang gốc đã xem. Phương án mới là các nhầm lẫn về khái niệm/quy trình lân cận; không thấy đáp án đúng thứ hai. **21 approved revision2**,15 câu khác giữ approved revision1. Finding revision1 được đóng; lịch sử bên trên không bị xóa. Coverage vẫn giới hạn một trang mỗi tài liệu, chưa phải bộ đề hiệu chỉnh độ khó.
