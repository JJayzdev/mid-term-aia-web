# Expansion A001

50 câu hỏi mới, trạng thái `pending_review`, trong `data/questions/drafts/expand-a-001.json`. Script tái lập: `python scripts/content/expand_a_001.py` (system Python có jsonschema).

| PDF | Câu mới | Tổng sau khi được duyệt | Phạm vi khái niệm |
|---|---:|---:|---|
| p1-d01 | 16 | 20 | Foundation model, STT/TTS, barge-in/streaming, agent observation, skills/MCP, next-token, attention, tokenization, alignment, cutoff, API usage |
| p1-d02 | 17 | 20 | Actor/problem, PAIR, Double Diamond, discovery, Problem Card, metric/threshold/action, automate/augment, rule/workflow/agent, eval-optimizer, input/output metric, failure recovery |
| p1-d03 | 17 | 20 | Tool schema/errors, ReAct observation/trace, dependency/order, fallback, native function calling/hybrid, prompt constraints, loop controls, graph state, cost/accuracy, indirect injection, trace eval/triage |

Mỗi item có SHA-256 tài liệu và trang vật lý PDF. Dùng văn bản OCR đã ingest; các trang chứa công thức hoặc dữ kiện OCR không rõ không được dùng làm câu hỏi tính toán. Reviewer vẫn cần mở trang nguồn để xác minh độc lập. Đây là mở rộng các learning objective được chọn, không phải tuyên bố kiểm chứng toàn bộ 3.589 trang.

Đã kiểm tra JSON Schema và tránh trùng ID với bank approved. Không sửa bank approved hoặc 204 câu cũ; không tự duyệt. Stem hỏi trực tiếp kiến thức/tình huống, nguồn đặt tại `source_reference` và explanation.
