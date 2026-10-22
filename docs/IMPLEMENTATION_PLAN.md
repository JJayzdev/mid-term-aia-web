# Kế hoạch milestone và các quyết định chờ duyệt

Ngày: 2026-10-22. **Đang dừng tại Gate 0 — Discovery.** Chưa được bắt đầu ingestion toàn bộ, tạo câu hỏi hoặc code ứng dụng.

## Kết quả Discovery

Đã đọc brief, kiểm tra workspace và nguồn; A1 khảo sát nội dung, A2 khảo sát codebase song song theo yêu cầu. A1 dùng GPT-6.1 Sol, A2 dùng GPT-6 Luna. Root là phiên đang chạy; không tuyên bố đã đổi model Root sang GPT-6 Astra vì công cụ hiện có không đổi model của phiên này. Reviewer dùng GPT-6.1 Sol cho lần kiểm tra hợp đồng Discovery; content/code audit chính thức vẫn ở milestone tương ứng.

Workspace ban đầu chỉ có `slide/`, không có Git. Vì vậy không tạo worktree giả; các agent dùng chung filesystem và chỉ ghi đường dẫn được giao. Chưa init repository, scaffold hoặc cài dependency. Hash nguồn được ghi để đối chiếu lại khi hoàn tất Discovery.

## Lộ trình và dependency

| Mốc | Công việc/đầu ra | Owner và gate |
|---|---|---|
| 0 | 5 tài liệu, inventory JSON/Markdown, codebase audit, schema đề xuất, unresolved decisions | Root kiểm tra artifact; người dùng duyệt trước M1 |
| 1 | Pilot OCR/text/bảng/công thức, rồi manifest/page catalog/mapping/errors toàn bộ; giữ source hash | A1 phụ trách pipeline; Root kiểm tra completeness, Reviewer mẫu rủi ro; unreadable báo rõ |
| 2 | Chốt JSON Schema, runtime validator, blueprint; pilot 8–12 câu verified rồi batch 15–25 | Root duyệt schema trước tạo hàng loạt; A1 sở hữu câu nháp |
| 3 | Audit từng câu/batch theo nguồn, sửa đúng batch, retest phần ảnh hưởng | Reviewer độc lập; Root phát hành chỉ approved không lỗi mở |
| 4 | Scaffold được duyệt trong workspace hiện tại, UI/modes/domain/persistence/import/export | A2 Web Engineer; code dùng fixture tách biệt nếu bank chưa sẵn; tích hợp approved bank sau Gate3 |
| 5 | Kiểm chứng quotas theo điểm, seeded generation, thiếu ngân hàng, scoring/timer/recovery | A2 chạy test module; Root kiểm tra output và invariants |
| 6 | Review diff + test/E2E trên bản tích hợp, responsive, runtime/build | Reviewer báo lỗi về owner; Root chạy lại các kiểm tra liên quan sau sửa |
| 7 | Hash nguồn/diff/secrets, validator/test/build cuối, README/QA/coverage/release notes | Root nghiệm thu bằng evidence; chưa tự publish/deploy trong Discovery |

Milestone 2–3 chạy theo batch nhỏ. Phần UI độc lập có thể chạy song song sau schema/kiến trúc được duyệt, nhưng không chuyển gate nội dung hay nghiệm thu web bằng fixture. Không khởi chạy nhiều agent chỉ để diễn đạt lại cùng một báo cáo.

## Ownership thực tế và dự kiến

| Agent | Được sửa | Không được sửa |
|---|---|---|
| Root | `docs/PRD.md`, `ARCHITECTURE.md`, `CONTENT_RULES.md`, `ACCEPTANCE_CRITERIA.md`, `IMPLEMENTATION_PLAN.md`, `docs/schemas/`; sau này release manifest và `public/data/bank.json` | Không chỉnh nguồn `slide/` |
| A1 Question Engineer | `docs/discovery/CONTENT_INVENTORY.md`, `source-inventory.json`, `tmp/discovery/a1/`; sau duyệt: `scripts/content/`, `content/`, `data/questions/drafts/` | Không tự approve batch mình tạo, không sửa UI |
| A2 Web Engineer | `docs/discovery/CODEBASE_AUDIT.md`; sau duyệt: `src/`, tests ứng dụng, package/config, `index.html`, asset UI | Không sửa câu học thuật approved hoặc schema không qua Root |
| Reviewer | `docs/discovery/DISCOVERY_REVIEW.md`; sau này `reports/content/`, `reports/qa/` | Không sửa ngân hàng, code của A2 hay nguồn |

Root promote bản đã review vào `data/questions/approved/` và artifact công khai; A1 chỉ nhận issue để sửa drafts. Nếu cần đổi ownership, bàn giao rõ đường dẫn trước; không hai agent sửa cùng file. Khi người dùng duyệt init Git, commit baseline nguồn/tài liệu theo dung lượng phù hợp, rồi mới cân nhắc branch/worktree cho công việc độc lập. Không có remote hay deploy target được cấu hình.

## Quyết định đề nghị phê duyệt

1. **Stack/phạm vi lưu trữ:** React + TypeScript + Vite ngay trong workspace hiện tại, IndexedDB cho một người dùng/trình duyệt; chưa backend/tài khoản/đồng bộ. Có cho khởi tạo Git để theo dõi thay đổi từ bước triển khai không?
2. **Cách chấm:** tự luận chia 6 điểm Phase 1 + 4 điểm Phase 2, tự chấm theo rubric với nhãn điểm tạm/cuối rõ ràng; multiple choice dùng exact-set. Track mặc định chia đều, cấu hình khác phải giữ đủ cả bốn track và tỷ lệ điểm chính xác. Số câu đề sẽ chốt sau pilot, không mặc định là 100 câu.
3. **Mapping nguồn:** xác nhận Track 1 và Track 4 thuộc Phase 2; dùng ngày cục bộ theo tên file để lọc và hiển thị ngày in trên slide riêng sau đối chiếu. Track 2 thiếu tên file Day9 là có chủ đích hay cần bổ sung? Nếu chưa trả lời, giữ mapping unresolved, không tự tạo nội dung.
4. **Bước kế tiếp:** duyệt Gate0 để làm M1; ưu tiên pilot OCR local tiếng Việt/Anh cho nguồn dạng ảnh, đo chất lượng trước chạy toàn bộ. Discovery chưa xác minh engine OCR/language packs hoạt động; lựa chọn/cài công cụ sẽ báo bằng chứng trong M1. Không cần upload nguồn ra ngoài để hoàn tất Discovery.

Ngoài ra cần xác nhận cách xếp hai tài liệu mâu thuẫn: `phase1/day 2 ai product.pdf` (bìa Track 1) và `track2 k3/day 3 tu chatbot den agentic agent.pdf` (bìa Phase 1). Cho phép bắt đầu OCR các file này không có nghĩa đã phê duyệt taxonomy; giữ trạng thái unresolved cho tới khi có quyết định.

Các mặc định này là đề xuất để duyệt, chưa coi im lặng là phê duyệt. Có thể duyệt M1 trước trong khi giữ quyết định app ở trạng thái pending; khi đó không scaffold web.

## Rủi ro và xử lý

- Khối lượng trang ảnh lớn: pilot có đo chất lượng, cache theo hash, xử lý batch; không hứa thời gian/coverage chưa đo.
- Bảng/công thức/diagram: OCR dễ sai cấu trúc, phải xem ảnh gốc trước approve câu.
- Day/Phase mâu thuẫn hoặc chưa rõ: bảo toàn hai nguồn metadata, issue theo document, không suy luận lịch học toàn khóa.
- Không đủ approved theo bucket: có preflight và báo thiếu; không giảm quota âm thầm.
- Lịch sử/timer local: transactional persistence, deadline tuyệt đối, giới hạn đồng hồ client và không nộp nền khi browser đóng được công bố.
- Không có ngân hàng/test hiện tại: không báo pass, coverage hay chức năng có sẵn khi chưa tạo và kiểm chứng.

## Điều kiện kết thúc lượt này

Root đọc kết quả A1/A2, kiểm tra schema JSON và các con số, đối chiếu mẫu trang gốc, rà báo cáo Reviewer, xác minh 63 nguồn giữ hash. Báo cáo Discovery ngắn gọn có link và các quyết định chờ duyệt; **dừng lại**, không tự chuyển M1.
