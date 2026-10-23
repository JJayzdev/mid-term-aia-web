# AIA Study

Ứng dụng ôn tập tiếng Việt từ bộ slide AIA, chạy hoàn toàn trong trình duyệt. React + TypeScript + Vite; dữ liệu học tập lưu bằng IndexedDB, không cần tài khoản hay backend.

**Dùng ngay:** [AIA Study trên GitHub Pages](https://jjayzdev.github.io/mid-term-aia-web/). [Mã nguồn](https://github.com/JJayzdev/mid-term-aia-web). Bản v1 được triển khai miễn phí ngày 2026-10-22.

## Chức năng

- Ôn theo ngày học, Phase, Track, chủ đề, độ khó; luyện tổng hợp, câu sai/bỏ trống và câu đã lưu.
- Lọc **Dạng bài → Chỉ câu tính toán** để luyện bài số bằng Casio. Mỗi đề thi thử có ít nhất hai câu tính trong phần Track 4; đây là cấu hình luyện tập, không phải tỷ lệ chính thức của đề thi.
- Thi thử 90 phút, **60 câu**, 100 điểm: Phase 1 = **36 câu / 60 điểm**; Phase 2 = **24 câu / 40 điểm** (6 câu mỗi Track). Có 54 câu khách quan và 6 câu tự luận; tự luận = 10 điểm. Bốn Track mặc định bằng nhau, có thể chỉnh trọng số điểm với bước 0,25%.
- Điểm được phân bổ theo nhóm để giữ đúng tỷ lệ; các câu trong một nhóm có thể lệch tối đa 0,01 điểm. Điểm từng câu hiển thị khi làm bài. Thay đổi cấu hình không làm đổi đề hoặc điểm trong lịch sử đã lưu.
- Đáp án khách quan chấm tự động; chọn nhiều dùng exact-set, không trừ điểm. Tự luận không trống chờ người học tự đánh giá từng tiêu chí 0 / 0,5 / 1; làm tròn half-up một lần ở cuối mỗi câu đến 0,01 điểm.
- Tự lưu câu trả lời, giữ đề và thứ tự lựa chọn khi tải lại, tự nộp khi hết hạn. Tab mới tiếp quản quyền sửa; tab cũ chỉ xem.
- Lịch sử giữ bản sao nội dung câu hỏi tại lúc làm bài, có điểm theo Phase/Track/chủ đề. Xuất/nhập sao lưu JSON; câu hỏi nhập ngoài chỉ vào vùng chờ duyệt.

## Chạy cục bộ

Yêu cầu Node.js 22.12+ (đã kiểm thử với 24.14.1), npm.

```sh
npm ci
npm run dev
npm run typecheck
npm test
npm run build
```

Vite in địa chỉ truy cập. Bản production nằm trong `dist/`; đường dẫn asset tương đối và hash routing hỗ trợ GitHub Pages dưới tên repository.

Kiểm thử trình duyệt dùng Chrome cài sẵn:

```sh
npx vite preview --host 127.0.0.1 --port 5175
npx playwright test --config scripts/qa/playwright.config.ts
```

Đặt `AIA_BASE_URL` nếu dùng cổng hoặc URL khác. Test dùng dữ liệu phát hành thực và browser context mới; kết quả/log/screenshot nằm trong `tmp/qa/`.

## Nguồn và mức độ bao phủ

Bộ đầu vào gồm **63 PDF / 3.589 trang**. Pipeline xử lý toàn bộ file, giữ hash SHA-256 và số trang vật lý (trang đầu PDF là 1). PDF gốc và cache OCR nằm cục bộ, không đưa lên website/repository. Ba trang không trích được chữ đã được xem ảnh: QR, trang gần trống/logo, và thẻ Q&A; không câu hỏi nào dựa trên ba trang đó.

Ngân hàng hiện có **1.284 câu đã duyệt độc lập**: Phase 1 có 300 câu; Track 1/2/3/4 có 220/240/260/264 câu. Mỗi PDF có ít nhất 20 câu; 12 PDF Track 4 có 22 câu/file, gồm **24 bài tính mới** với dữ kiện, đơn vị, quy tắc làm tròn và lời giải từng bước để luyện bằng Casio. Câu hỏi trực tiếp kiểm tra kiến thức/tình huống, không hỏi “trong slide…”. Nguồn trích dẫn gồm 1.079 trang khác nhau; điều này không đồng nghĩa mọi khái niệm trên 3.589 trang đều đã có câu hỏi. Kiểm duyệt theo câu/revision nằm trong `reports/content/`; thống kê trong `public/data/coverage.json`. Mỗi câu có tài liệu nguồn và trang vật lý trong phần giải thích. Độ khó là ước lượng biên soạn, chưa hiệu chuẩn bằng kết quả thi thực tế.

Phase/Track được tổ chức theo thư mục người dùng cung cấp, Day theo tên file với khóa riêng từng Phase/Track. Nhãn trên một số bìa không khớp tên thư mục; xung đột được giữ trong catalog và báo cáo. Không tạo thêm Day 9 của Track 2.

Pipeline nội dung dành cho người bảo trì:

```sh
python -m pip install -r requirements-content.txt
python scripts/content/ingest.py --help
python scripts/content/validate_drafts.py
python scripts/release_bank.py
python scripts/validate_release.py --verify-sources --min-per-document 20 --standalone-stems
python -m unittest discover -s scripts/qa -p test_release_gate.py -v
```

Ingestion cần thư mục `slide/` đúng bộ gốc và Windows OCR tiếng Anh. Xem `reports/ingestion/README.md` để tái chạy. Release chỉ nhận câu có quyết định duyệt độc lập đúng revision; tác giả không thể tự duyệt. Chạy validation/build/tests lại sau mỗi thay đổi ngân hàng. Không dùng JSON nhập trong UI để tự động nâng câu lên approved.

## Deploy miễn phí

GitHub Pages: publish mã nguồn ở `main`, bản `dist/` ở `gh-pages`, Pages chọn branch `gh-pages`, thư mục `/`. Không cần backend, biến bí mật hay dịch vụ AI trả phí.

Script dưới đây dùng đăng nhập Git Credential Manager hiện có, giữ credential trong bộ nhớ. Nó tạo repository public nếu chưa tồn tại, push nguồn đã commit và build đã kiểm tra, rồi bật Pages. Không ghi token vào file hay remote URL.

```sh
python scripts/deploy/github_pages.py --check
python scripts/deploy/github_pages.py --publish
python scripts/deploy/github_pages.py --status
```

Trước `--publish`, checkout `main` phải sạch, `dist/` phải là bản vừa qua kiểm thử. Lần sau script cập nhật branch mà không force-push. Có thể dùng Vercel: import repository, framework Vite, build `npm run build`, output `dist`; `vercel.json` đã sẵn sàng. Chỉ chọn gói miễn phí phù hợp mục đích sử dụng.

## Sao lưu và giới hạn

- Dữ liệu trên từng thiết bị/trình duyệt, không đồng bộ giữa thiết bị. Trong **Dữ liệu → Tải bản sao lưu**, lưu JSON trước khi xóa dữ liệu website hoặc đổi máy. Bản sao lưu chứa phiên đã nộp và bookmark, không chứa bài đang làm.
- Khôi phục cùng ID khác nội dung bị từ chối nguyên giao dịch. Ngân hàng nhập riêng không tác động ngân hàng phát hành.
- Tự luận là tự đánh giá của người học, không phải điểm được giảng viên/AI xác nhận.
- Đây là công cụ tự học. Đáp án là dữ liệu static nên có thể đọc qua DevTools; đồng hồ dựa trên thời gian thiết bị, không dùng cho thi có giám sát.
- Chưa có service worker/offline install; cần mạng để tải ứng dụng và ngân hàng. Lịch sử đã lưu được giữ cục bộ.
- Phiên bản v1 chỉ kiểm thử tự động trên Chrome; các trình duyệt khác cần hỗ trợ IndexedDB, BroadcastChannel và BigInt.

Quyết định triển khai: `docs/IMPLEMENTATION_DECISIONS.md`. Schema: `docs/schemas/question-bank.schema.json`. Tiêu chí nghiệm thu: `docs/ACCEPTANCE_CRITERIA.md`. Báo cáo QA phát hành: `reports/qa/`.
