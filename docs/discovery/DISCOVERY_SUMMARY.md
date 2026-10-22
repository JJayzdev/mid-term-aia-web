# Báo cáo Discovery — chờ duyệt Gate 0

Ngày 2026-10-22, workspace `E:\VinAI\mid-term AIA web`. Chỉ hoàn tất khảo sát và đề xuất; chưa triển khai ứng dụng, OCR toàn bộ hoặc sinh câu hỏi.

## Hiện trạng

Ban đầu workspace chỉ có `slide/`. Chưa có framework, source ứng dụng, package manifest, build/test scripts hoặc Git repository. Chưa có chức năng quiz nào để kế thừa; Node/Python/Git có sẵn. [Codebase audit](CODEBASE_AUDIT.md) ghi rõ môi trường và các kiểm tra không thể chạy.

| Thư mục nguồn | PDF | Trang | Không có text |
|---|---:|---:|---:|
| phase1 | 15 | 1.128 | 1.128 |
| track1 k3 | 11 | 417 | 417 |
| track2 k3 | 12 | 564 | 564 |
| track3 k3 | 13 | 685 | 685 |
| track4 | 12 | 795 | 348 |
| Tổng | 63 | 3.589 | 3.142 |

Dung lượng 407.168.913 bytes (~388,31 MiB). Không PDF mã hóa hoặc lỗi mở/trích xuất; 87,55% trang không có text, cần OCR. 447 trang có text không đồng nghĩa chữ/công thức chính xác. [Kiểm kê chi tiết](CONTENT_INVENTORY.md) chứa toàn bộ 63 tiêu đề bìa và dẫn trang; [inventory JSON](source-inventory.json) chứa hash/size/page statistics và metadata nguồn.

Chủ đề bìa cho thấy Phase 1 gồm nền tảng AI/LLM, sản phẩm, agent, dữ liệu/RAG, triển khai, guardrails và đánh giá; Track 1 tập trung sản phẩm/kinh doanh, Track 2 hạ tầng/vận hành, Track 3 agent nâng cao, Track 4 thị giác máy tính/robotics. Đây là tóm lược phạm vi bìa, chưa phải taxonomy section đã duyệt.

## Vấn đề ảnh hưởng trực tiếp đến việc tạo câu hỏi

- `phase1/day 2 ai product.pdf`, trang 1 ghi Track 1.
- `track2 k3/day 3 tu chatbot den agentic agent.pdf`, trang 1 ghi Phase 1.
- Nhiều Day tên file khác Day in trên slide, có cả khoảng 20–21; không áp dụng offset chung.
- Track 2 không có Day9 trong tên file; chưa xác định thiếu tài liệu hay lịch học khác.
- Quan hệ Phase 2 của Track 1/4 và một số chủ đề cần người dùng hoặc nguồn xác nhận.
- OCR chưa được pilot. Bảng/công thức/sơ đồ cần kiểm tra trực quan; chưa được dùng text chưa xác minh để approve câu hỏi.

## Bộ artifact để duyệt

- [PRD](../PRD.md): phạm vi các chế độ học/thi, người dùng, quy tắc điểm và giới hạn.
- [ARCHITECTURE](../ARCHITECTURE.md): React/TypeScript/Vite, IndexedDB, engine/persistence/import, blueprint 60/40 và 10% tự luận.
- [CONTENT_RULES](../CONTENT_RULES.md): nguồn/provenance, OCR, taxonomy, batch, review độc lập.
- [ACCEPTANCE_CRITERIA](../ACCEPTANCE_CRITERIA.md): gate, invariants, test cần chạy và bằng chứng nghiệm thu.
- [IMPLEMENTATION_PLAN](../IMPLEMENTATION_PLAN.md): milestone 0–7, dependency, file ownership, quyết định chờ duyệt.
- [JSON Schema đề xuất](../schemas/question-bank.schema.json): 5 loại câu hỏi, điều kiện đáp án/rubric và approval metadata.
- [Review độc lập](DISCOVERY_REVIEW.md): kiểm tra thiết kế và 28 probe schema; không thay cho content/code QA tương lai.
- [Xác minh của Root](ROOT_VERIFICATION.md): nguồn không thay đổi, tài liệu/schema và giới hạn kiểm thử.

## Đề xuất cần duyệt

1. Phát triển ngay trong workspace hiện tại bằng React + TypeScript + Vite, lưu IndexedDB cho một người dùng, chưa backend; khởi tạo Git ở bước triển khai.
2. Dùng cấu hình 100 điểm, 90 phút; Phase 1/2 = 60/40; tự luận = 6+4 điểm; Track 1–4 mặc định mỗi track 10 điểm. Tự luận tự chấm theo rubric và hiển thị trạng thái điểm tạm/cuối; nhiều đáp án chấm exact-set.
3. Xác nhận mapping Phase/Track/Day và xử lý các tài liệu xung đột nêu trên. Giữ unresolved nếu chưa có quyết định; không di chuyển/sửa PDF.
4. Cho phép chuyển sang M1 với pilot OCR local rồi ingestion theo batch. Chưa cần cho triển khai web nếu muốn xem chất lượng ingestion trước.

Việc dừng tại đây là theo chỉ dẫn trực tiếp trong brief: “Dừng sau Discovery để báo cáo kết quả và chờ xác nhận trước khi bắt đầu triển khai.” Gate 1–7 chưa thực hiện, không được coi là đã pass.
