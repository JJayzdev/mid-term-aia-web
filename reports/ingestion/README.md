# Báo cáo ingest cục bộ

- 63/63 PDF, 3.589/3.589 trang vật lý đã được thử trích xuất.
- SHA-256 của toàn bộ PDF sau ingest khớp inventory; không sửa nguồn.
- Phương pháp: {'Windows.Media.Ocr/en-US': 3240, 'pypdf': 349}.
- Lỗi xử lý: 0; trang không có text sau xử lý: 3 (chi tiết trong audit.json).
- Cache theo SHA-256 tài liệu và trang; provenance lưu engine, ngôn ngữ, DPI, revision pipeline. Chạy lại `scripts/content/ingest.py` dùng cache hợp cấu hình; thiếu bản text Markdown sẽ được tái tạo.
- Pipeline render 115DPI, OCR Windows.Media.Ocr en-US trong bộ nhớ; không upload nguồn. Chạy tối đa3 process tài liệu. Render tạm được dọn tại đường dẫn đã kiểm tra nằm trong tmp/content-tools/renders.
- Mọi trang mang trạng thái extracted_unverified. Đủ 3.589 lượt trích xuất không có nghĩa đã hiểu/kiểm chứng đủ mọi khái niệm. OCR tiếng Việt, thứ tự đọc, công thức, code cần kiểm tra bằng trang PDF gốc.
- Mapping học tập theo policy root: thư mục phase1→Phase1, thư mục track→Phase2/track tương ứng; Day theo tên file. Bằng chứng bìa và xung đột vẫn giữ nguyên trong catalog. Không tạo Day9 Track2.
- Bản rawtext/cache chỉ dùng cục bộ. Website/Git public chỉ nhận catalog gọn và câu hỏi đã được reviewer độc lập duyệt.

## Tái lập

Bundled Python có pypdf/pdfplumber/pypdfium2: chạy `scripts/content/ingest.py --workers 3`, rồi `scripts/content/audit_ingestion.py`. Windows PowerShell5 (`powershell.exe`) và OCR en-US đã có sẵn. Chính sách script chỉ bỏ chặn trong process cục bộ qua `-ExecutionPolicy Bypass`, không sửa cấu hình máy. Validator schema chạy bằng system Python có jsonschema, vì bundled Python không có package này.
