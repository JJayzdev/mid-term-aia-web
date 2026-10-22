# Kiểm tra độc lập artifact Discovery

Ngày: 2026-10-22. Người thực hiện: Reviewer độc lập với tác giả 5 tài liệu và schema. Phạm vi là hợp đồng/thiết kế Discovery; **không phải phê duyệt nội dung học thuật, nghiệm thu mã hoặc cho phép chuyển milestone**. Các đề xuất vẫn cần người dùng duyệt theo Gate 0.

## Kết quả

Không phát hiện lỗi critical/major còn mở trong phạm vi đã đọc. Có đủ 5 tài liệu `PRD.md`, `ARCHITECTURE.md`, `CONTENT_RULES.md`, `ACCEPTANCE_CRITERIA.md`, `IMPLEMENTATION_PLAN.md`; có schema đề xuất, inventory và codebase audit. Các tài liệu phân biệt rõ hiện trạng, đề xuất, quyết định chưa duyệt và kiểm thử tương lai. Không có khẳng định sản phẩm/test/build đã PASS.

- Schema bao phủ 5 question types: single choice, multiple choice, true/false, short answer, scenario. Scenario cho phép single/multiple/rubric và bắt buộc context; các dạng còn lại ràng buộc answer format tương ứng. Rubric bắt buộc cho short answer/scenario rubric; boolean/rubric không nhận options. Approved yêu cầu review, taxonomy verified và provenance verified về cấu trúc.
- Schema không chứng minh tác giả khác reviewer, revision khớp, đáp án thuộc options, tổng rubric bằng 1, nguồn/hash/trang thật hoặc quota khả thi. `ARCHITECTURE.md` và tiêu chí C2/C3 giao rõ các điều kiện này cho validator nghiệp vụ và review; đây là phần hoãn có chủ đích, không phải kiểm tra đã hoàn tất.
- Ví dụ quota đúng: Phase 1 = 54 khách quan + 6 rubric = 60; mỗi track Phase 2 = 9 + 1 = 10, bốn track = 40; tổng = 100, rubric = 10. Fixture 18+12 = 30 câu khách quan, 2+4 = 6 rubric, tổng 36. Tài liệu ghi đây là ví dụ, chưa chốt số câu mặc định. Scenario rubric được tính theo format.
- Timer dùng deadline tuyệt đối, kiểm tra hạn khi ghi/resume; trình duyệt đóng chỉ hoàn tất nộp khi mở lại. Persistence nêu transaction, CAS, idempotency, lưu sau mỗi thay đổi, lỗi lưu, snapshot và import nguyên tử. Scoring tách essay pending khỏi sai; điểm tự chấm có nhãn và không quy đổi điểm khách quan /90 thành kết quả /100. Các yêu cầu có test tương lai tương ứng.
- Inventory và 5 tài liệu nhất quán về 63 PDF, 3.589 trang, 3.142 trang không text, 447 trang có text; không đánh đồng text có sẵn với chất lượng đọc. Hai xung đột bìa Phase/Track được giữ unresolved; ngày file/ngày in tách riêng, không suy diễn +15; Day9 Track2 chưa được gọi là tài liệu chắc chắn bị thiếu.
- Không có app/Git hiện hữu theo codebase audit; kế hoạch không tuyên bố worktree/scaffold/cài package đã thực hiện. Gate 0 dừng trước ingestion toàn bộ, tạo câu hỏi và code ứng dụng. Chỉ trạng thái hợp đồng được khảo sát; các giới hạn OCR và quyết định mapping vẫn công khai.

## Finding và retest

| ID / mức độ | Đường dẫn, cách tái hiện | Expected / actual ban đầu | Xử lý và retest |
|---|---|---|---|
| DR-01 / minor | `docs/discovery/CODEBASE_AUDIT.md`: đối chiếu đề xuất trọng số và ownership với `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_PLAN.md` | Audit ban đầu có chữ chuẩn hóa trọng số và đề xuất `docs/architecture/`, dễ nhầm với hợp đồng mới cấm normalize âm thầm và Root sở hữu `docs/ARCHITECTURE.md` | Đã báo Root; A2 sửa audit, Reviewer đọc lại. Hiện yêu cầu bốn trọng số dương/tổng 1, từ chối sai thay vì sửa ngầm; ownership và trạng thái proposal được cập nhật. **Đóng sau retest tài liệu.** |

## Kiểm tra thực chạy

- Đọc trực tiếp 5 tài liệu, schema, `CONTENT_INVENTORY.md` và `CODEBASE_AUDIT.md`; đối chiếu điều kiện schema và tính quota bằng phép tính độc lập.
- Lệnh tái hiện: `python tmp/discovery/reviewer/schema_probe.py`, tại root workspace. Python 3.9.13, jsonschema 4.25.1; exit code 0. `Draft202012Validator.check_schema` không lỗi; **28/28 probe hợp đồng tổng hợp đạt kết quả mong đợi**, gồm 7 tổ hợp type/format hợp lệ, đáp án sai kiểu, thiếu rubric/context/nguồn/đáp án, type/format không khớp, Phase2 thiếu track và approved thiếu review. Fixture synthetic chỉ tồn tại trong bộ nhớ, không phát hành ngân hàng học thuật.
- Thử ban đầu bằng Python 3.12.14 kèm runtime thất bại vì `ModuleNotFoundError: jsonschema`; sau đó dùng thư viện đã có ở system Python. Không cài dependency.

Các probe này là kiểm tra cấu trúc artifact Discovery, không phải toàn bộ test validator tương lai. Bộ probe chưa phủ mọi biên min/max/format và chưa kiểm tra nghiệp vụ; không suy ra chất lượng kiến thức từ schema pass.

## Chưa chạy và giới hạn

Reviewer chưa hash lại 63 PDF, chưa trích xuất lại toàn bộ trang hoặc tự nhìn từng bìa; phần đối chiếu nguồn ở trên dựa inventory đã đọc. Root chịu trách nhiệm kiểm tra hash/bằng chứng nguồn riêng. Chưa có OCR pilot, content audit từng câu, code review ứng dụng, unit/integration/E2E, browser runtime, responsive, typecheck hay production build để chạy. Không có kết quả PASS sản phẩm. Các gate M1–M7 và phê duyệt của người dùng còn nguyên.

## Rà bổ sung quy tắc rubric

Đã đọc lại phần sửa tại `ARCHITECTURE.md`, `CONTENT_RULES.md` và AC S2: ba mức 0 / 0,5 / 1 ánh xạ nhất quán no_credit / partial_credit / full_credit; tính thập phân chính xác/rational, half-up một lần ở điểm cuối mỗi câu tới 0,01 rồi cộng integer units. Trọng số rubric phải tổng đúng 1; làm tròn điểm đạt không được dùng để làm tròn quota blueprint. S2 yêu cầu kiểm thử mức chấm, số lẻ và quy tắc rounding tương ứng. Không phát hiện mâu thuẫn mới; schema không đổi nên không chạy lại probe. Đây là rà đặc tả, chưa kiểm thử implementation rounding.

Root báo đã đối chiếu hash toàn bộ nguồn và nhìn hai bìa xung đột cùng chín trang mẫu, trong đó có ví dụ số slide in khác trang vật lý. Các kiểm tra đó do Root thực hiện riêng; không tính vào kiểm tra độc lập đã chạy của Reviewer.
