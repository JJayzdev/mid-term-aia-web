# Xác minh artifact Discovery của Root

Ngày 2026-10-22. Phạm vi chỉ là artifact Discovery; không phải nghiệm thu web/ngân hàng câu hỏi.

## Kiểm tra đã thực hiện

- Root tự liệt kê workspace trước khi agent ghi artifact: chỉ `slide/`; `rg --files` trả 63 PDF. `git status` báo không phải Git repository. Không có AGENTS.md trong workspace hoặc các đường dẫn cha đã kiểm tra.
- Đọc trực tiếp hai báo cáo A1/A2, inventory JSON, năm tài liệu chính, schema, script probe và báo cáo Reviewer.
- Tính lại SHA-256 và size của cả 63 nguồn sau công việc Discovery, so với inventory khảo sát: 63/63 khớp. Đối chiếu tập path nguồn với inventory, không thêm/mất file; 63 hash khác nhau.
- Tính lại 407.168.913 bytes, 3.589 trang, 3.142 trang không có text từ page statistics; kiểm tra mỗi file có dãy trang 1..N đầy đủ. Root không lặp lại toàn bộ trích xuất 3.589 trang; thống kê parser ban đầu do A1 chạy và có script khảo sát.
- Root tự render/nhìn 9 trang mẫu: 5 bìa đầu khóa của năm thư mục; hai bìa xung đột Phase/Track; Phase1 Day1 trang vật lý 12 và Track4 Day01 trang vật lý 8. Xác nhận hai xung đột đã báo và cần bảo toàn physical PDF page riêng printed slide label (hai trang nội dung mẫu lần lượt in 9/42 và 5/86).
- Đã render bằng pdfplumber/pypdfium2; Poppler `pdftoppm`/`pdfinfo` cũng có sẵn. `tesseract` không tìm thấy trên PATH; chưa kết luận máy không có mọi OCR engine. Một lần in text mẫu gặp lỗi encoding stdout cp1252; đã chạy lại với UTF-8. Không có lỗi đọc PDF do vấn đề stdout này.
- Đã đọc và chạy lại `python tmp/discovery/reviewer/schema_probe.py`: exit code 0, **28/28 probe cấu trúc** pass, bao gồm `Draft202012Validator.check_schema`, năm question_type và bảy tổ hợp type/format. Fixture tổng hợp chỉ nằm trong script kiểm tra, không phải câu hỏi học thuật/phát hành.

## Tái chạy kiểm tra

Tại root workspace:

```powershell
python tmp/discovery/root/verify_discovery.py
python tmp/discovery/reviewer/schema_probe.py
```

Script đầu kiểm tra file/hash/page statistics, năm tài liệu bắt buộc, JSON parse, link Markdown cục bộ và không có scaffold/Git. Script thứ hai dùng Python hệ thống có jsonschema; Python bundled không có package này. Không cài dependency mới cho kiểm tra Discovery. Log lần chạy cuối nằm ở [root-verification.log](root-verification.log) và [schema-probe.log](schema-probe.log).

## Điều chưa kiểm chứng

Chưa OCR toàn bộ, chưa xác minh mọi section/công thức/bảng, chưa duyệt taxonomy, chưa tạo câu hỏi. Schema probe không kiểm tra sự thật học thuật, không thay validator cross-field/catalog tương lai. Chưa chạy unit/integration/E2E hoặc production build vì chưa có ứng dụng. Không có Git diff để review vì workspace chưa là repository; nguồn được bảo toàn qua hash. Người dùng vẫn cần duyệt Gate 0 trước khi chuyển bước.
