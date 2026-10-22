# Kiểm định độc lập A002

**51 approved** tại exact revisions trong JSON, gồm p1-d04-x04 r3 sau sửa. Đã đọc toàn bộ stem/options/answer/explanation của 51 câu; render và xem 48 trang PDF vật lý được trích dẫn, ảnh ở `tmp/reviewer/expand-a-002/`. SHA256 cả ba PDF khớp catalog; JSON Schema kiểm lại thành công bằng jsonschema.

Finding đã đóng: option b của p1-d04-x04 gọi “bản nháp mới nhất”, trong khi p18 yêu cầu “bản cập nhật mới nhất” bao gồm thay đổi ý định user. Đã đọc r3 và xác nhận sửa đúng, không đổi answer IDs.

Đã so mục tiêu với 9 câu legacy cùng ba PDF: giữ riêng context token selection, tool/runtime contract, loop verification, product requirements và PoC economics; không lặp nguyên các câu bốn lớp/JTBD/Definition of Done. Các ví dụ p95 hoặc kịch bản kinh doanh chỉ được dùng với điều kiện stem, không suy thành ngưỡng phổ quát.

Đây là gate nội dung A002, không phải kiểm thử app hoặc phê duyệt batch khác. Không sửa draft/public bank.

## Bằng chứng từng câu

- **p1-d04-x01 r2 approved**: PDF p13: Context engineering chọn lại tập token qua từng lượt; c đúng, không phải chỉ system prompt hay giữ nguyên mọi lịch sử. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x02 r2 approved**: PDF p14: Tool schema là contract sử dụng, tool result là dữ liệu mới; b đúng, hai distractor đánh tráo hướng dẫn và bằng chứng. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x03 r2 approved**: PDF p17: Write đẩy state ra file/DB ngoài context; a đúng, khác select kéo vào và compress nén trong context. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x04 r3 approved**: PDF p18: Compaction phải giữ quyết định/ràng buộc, nguồn/thời điểm, câu hỏi mở và cập nhật mới nhất; a,b đúng. r3 đã đổi đúng bản cập nhật thay bản nháp. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x05 r1 approved**: PDF p19: Giá vé live thiếu nguồn và expiry chưa đủ đáng tin; True đúng theo yêu cầu metadata. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x06 r2 approved**: PDF p22: Progressive disclosure nạp định nghĩa phù hợp lúc cần; a đúng, không nạp hết hoặc xóa mô tả tool. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x07 r2 approved**: PDF p25: Application thực thi tool rồi gửi result về model; c đúng. Model sinh request không tự chạy external API. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x08 r2 approved**: PDF p28: Tên read/write cụ thể tách risk và approval theo hành động; b đúng. Đổi tên mà bỏ contract hoặc dùng chung quyền không đạt mục tiêu. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x09 r2 approved**: PDF p29: Retry có thể lặp side effect nên cần idempotency; a đúng. Tên function/context size không giải quyết tác động lặp. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x10 r2 approved**: PDF p30: Tool quá nhỏ tăng calls, quá lớn khó hiểu boundary/debug/reuse; c đúng. Hai distractor đảo hoặc tuyệt đối hóa lợi ích. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x11 r2 approved**: PDF p31: Parallel calls vẫn cần rate limit và race-condition control; b,c đúng. Tăng concurrency vô hạn không giải quyết giới hạn. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x12 r2 approved**: PDF p32: Thiếu required args và quyền ghi phải hỏi bổ sung/xin quyền trước; a đúng. Quyền đọc không mặc nhiên bao gồm ghi. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x13 r2 approved**: PDF p37: Verify sau action kiểm tiêu chí và tạo tín hiệu phát hiện sai; c đúng. Chỉ self-report final_answer không xác minh công việc. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x14 r2 approved**: PDF p38: Success predicate cần kiểm tra chạy được như test/schema; b đúng, không coi budget cap hoặc tự nhận đã xong là thành công. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x15 r2 approved**: PDF p39: Verifier kiểm grounding phát hiện lazy hallucination dù rẻ và không lặp; a đúng. Hai detector khác kiểm tiêu chí khác. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x16 r2 approved**: PDF p48: Harness gate cưỡng chế bằng process trước action; c đúng. Prompt/hook chỉ thêm instruction hoặc gate sau write không có cùng bảo đảm. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d04-x17 r2 approved**: PDF p50: Approval gắn tool+exact args giới hạn đúng booking đã duyệt; b đúng. Duyệt tên tool không mở quyền cho mọi args. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x01 r2 approved**: PDF p7: Wrong thing là sai JTBD/persona/value, thing wrong là requirements/AC/risk thực thi; c đúng. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x02 r2 approved**: PDF p11: First-response resolution rate gần kết quả support hơn số câu trả lời hay token speed; b đúng. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x03 r2 approved**: PDF p15: Privacy chuyển thành minimization/masking và retention; a,b đúng. Thu thêm PII vô mục đích không đáp ứng privacy. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x04 r2 approved**: PDF p15: Transparency gồm AI disclosure, giới hạn và override/escalation; c đúng. Tên model hoặc confidence score đơn lẻ chưa đủ. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x05 r2 approved**: PDF p18: Người dùng có thể muốn decision support, giữ quyền từng bước; b đúng. Chấp nhận AI không đồng nghĩa full automation. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x06 r2 approved**: PDF p19: Persona AI thêm literacy/trust và error tolerance/explainability; c,d đúng. Hai distractor bỏ các chiều cần nghiên cứu. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x07 r2 approved**: PDF p20: Rephrase và abandon thuộc behavioral signal; c đúng. Rating là explicit, resolved/booked là outcome. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x08 r2 approved**: PDF p23: Requirement có p95, thời gian, nguồn và escalation kiểm thử được hơn mô tả chung; b đúng. 5 giây là ví dụ nguồn, không SLA mọi sản phẩm. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x09 r2 approved**: PDF p24: Latency SLA/uptime/cost budget là non-functional; a đúng, khác task chức năng và rủi ro AI-specific. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x10 r2 approved**: PDF p25: Không tìm thấy nguồn cần nêu giới hạn/fallback; c đúng. Happy-path answer hoặc retry vô hạn không phải failure handling. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x11 r2 approved**: PDF p26: Happy path đơn lẻ bỏ messy/edge/ambiguous/tool failures; b đúng. Không tự suy coverage từ một đường thành công. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x12 r2 approved**: PDF p28: PRD làm rõ quyết định/metric/risk/done; a đúng. Không để engineer tự suy hoặc hợp thức hóa giải pháp chốt trước. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x13 r2 approved**: PDF p29: Task completion/repeat usage là product metric, accuracy/citation là AI metric; c đúng theo hierarchy. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x14 r2 approved**: PDF p33: So that nêu business value gắn KPI/pain point; b đúng. Không thay bằng implementation tasks hoặc model name. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x15 r2 approved**: PDF p35: Tool timeout, thiếu nguồn và confidence thấp thuộc error states; a,b đúng. Chỉ request thuận lợi không bao phủ error. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x16 r2 approved**: PDF p38: Adoption thấp/workflow fit không rõ là business risk; c đúng, không phải lỗi kỹ thuật hay chất lượng dữ liệu. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d05-x17 r2 approved**: PDF p40: Privacy lớn chưa xử lý/no fallback/value chưa chứng minh là no-go; b đúng. Prototype chạy được không đủ go. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x01 r2 approved**: PDF p7: Unknowns từ data/prompt/tools/user behavior cần prototype/eval calibration; c đúng. Không phải chỉ implementation hoặc chỉnh threshold một lần. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x02 r2 approved**: PDF p8: Sprint phải học giả định nào bị bác bỏ và đầu tư/dừng ở đâu; b đúng. Đếm task không kiểm chứng giá trị. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x03 r2 approved**: PDF p9: Tool integration phải tính error handling và retries; a,b đúng. Chỉ happy-path connection bỏ effort vận hành. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x04 r2 approved**: PDF p9: Data/retrieval effort gồm cleaning/coverage/edge cases; c đúng. Setup index hoặc effort cố định bỏ unknowns. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x05 r2 approved**: PDF p12: MVE kiểm nhanh giả định user value; b đúng. MVP ship workflow dùng được, PoC phục vụ quyết định đầu tư. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x06 r2 approved**: PDF p12: MVP là phiên bản nhỏ dùng được để kiểm workflow; a đúng. Khác MVE test giả định giá trị trước tích hợp sâu. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x07 r2 approved**: PDF p13: Wizard of Oz kiểm value/workflow trước đầu tư model/integration; c đúng. Human backend không chứng minh performance production. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x08 r2 approved**: PDF p14: Experiment cần hypothesis/timebox/budget ceiling/stop criteria; b,c đúng. Deadline đơn lẻ thiếu kỷ luật quyết định. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x09 r2 approved**: PDF p16: Low-code hỗ trợ demo/PoC nhưng không thay discovery và production planning; a đúng. Flow trực quan không chứng minh đủ user value/architecture. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x10 r2 approved**: PDF p19: PoC canvas scope một workflow/user group/dataset hẹp; c đúng. Scope rộng hoặc chưa chốt success criteria không giảm bất định chính. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x11 r1 approved**: PDF p20: PoC không tự chứng minh production-ready mọi scale; False đúng. Nguồn explicitly loại lời hứa production readiness. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x12 r2 approved**: PDF p22: Human review/monitoring/maintenance thuộc Operate; a đúng. Build và Run chứa nhóm chi phí khác. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x13 r2 approved**: PDF p23: Ba scenario biểu diễn uncertainty adoption/cost/workflow fit; c đúng. Chỉ đổi tên trên cùng giả định không phải sensitivity. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x14 r2 approved**: PDF p24: Break-even phụ thuộc scenario và giả định đẩy mốc xa hơn; b đúng. Không cam kết optimistic case như chắc chắn. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x15 r2 approved**: PDF p25: ROI cần explicit adoption/review/API/error-handling cost; a,b đúng. Chỉ time saved lý thuyết bỏ điều kiện xảy ra giá trị. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x16 r2 approved**: PDF p27: Executive nhấn business value/scenario/decision ask; c đúng. Technical details không thay nội dung quyết định kinh doanh. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
- **p1-d06-x17 r2 approved**: PDF p28: Expectation setting nói capability/giới hạn/human review; b đúng. Chỉ demo thành công tạo scope thiếu thực tế. Đã đối chiếu stem, options, đáp án và giải thích với ảnh nguồn.
