# Quy tắc nội dung và trích xuất

Tài liệu ban đầu được lập trong Discovery; quyết định triển khai mới hơn ở `IMPLEMENTATION_DECISIONS.md` thay thế các trạng thái chờ duyệt lịch sử bên dưới.

## Yêu cầu bổ sung đã xác nhận — 2026-10-22

- Tối thiểu 20 câu cho mỗi file PDF trong 63 file, không phải mỗi trang. Mỗi câu có mục tiêu học tập riêng, khai thác nhiều phần nội dung; không tăng số lượng bằng các biến thể diễn đạt cùng một câu.
- Câu hỏi hỏi trực tiếp kiến thức, cơ chế, tính toán hoặc tình huống ứng dụng từ PDF. Không viết “trong slide”, “theo tài liệu”, “bài giảng nêu”, hoặc yêu cầu nhớ vị trí/cách diễn đạt của slide. File/trang nguồn nằm ở `source_reference`.
- Tài liệu là nguồn học thuật; không bổ sung đáp án bằng kiến thức ngoài để đạt số lượng. Reviewer kiểm tra tính đúng, phương án nhiễu, khả năng tự hiểu câu hỏi, trùng ý và chính xác trang/hash.
- Chỉnh sửa câu đã duyệt phải tăng revision và duyệt lại độc lập. Chỉ kết quả approved đúng revision mới được đưa vào website.
- Gate mở rộng: `python scripts/validate_release.py --verify-sources --min-per-document 20 --standalone-stems`. Bộ đếm mỗi PDF dùng ID câu duy nhất, không đếm nhiều lần khi một câu dẫn nhiều trang cùng file.

## Nguồn và provenance

`slide/` chỉ đọc, không rename, OCR ghi đè, nén hoặc sửa metadata. Mỗi tài liệu có document ID và SHA256. Tái chạy ingestion phải dùng manifest, phiên bản parser/OCR, cấu hình và hash để biết phần nào cần làm lại; artifact sinh ra nằm ngoài `slide/`.

Tham chiếu phải có đường dẫn nguồn trong manifest, trang vật lý PDF bắt đầu từ 1, tiêu đề và số slide in trên trang nếu có. Không dùng số trang OCR hay vị trí chunk thay số trang PDF. Không gộp trang làm mất provenance.

## Pipeline đề xuất sau Discovery

1. Kiểm kê lại toàn bộ nguồn và hash; so sánh baseline Discovery; PDF lỗi/mật khẩu được ghi issue thay vì bỏ qua.
2. Thử native text từng trang bằng pypdf/pdfplumber. Trang có text vẫn kiểm tra encoding, dấu tiếng Việt, reading order và công thức; text dài không tự có nghĩa là chính xác.
3. Trang không có text hoặc lỗi: render 150–300 DPI bằng Poppler/pdfplumber; OCR tiếng Việt + tiếng Anh. Chạy pilot ít trang trước; hiện chưa xác nhận OCR engine và language packs sẵn dùng. Không gửi toàn bộ nguồn lên dịch vụ bên ngoài chỉ vì cần OCR.
4. Bảng: giữ hàng/cột, header, đơn vị và chú thích; bảng ảnh cần đối chiếu ảnh gốc. Công thức: giữ ký hiệu, chỉ số, điều kiện và đơn vị; LaTeX chỉ được verified sau đối chiếu hình. Sơ đồ/figure: giữ crop/locator và diễn giải có xác minh, không xem OCR là hiểu quan hệ mũi tên.
5. Chấm trạng thái từng trang/đối tượng: extracted_unverified, verified, needs_ocr, needs_manual_review, unreadable; ghi lý do và confidence nếu engine có. Confidence không tự chuyển thành verified.
6. Tạo catalog/mapping có bằng chứng; tách vấn đề Day và Phase chưa chắc chắn. Báo lỗi gồm file, trang, loại lỗi, ảnh đối chiếu, ảnh hưởng, người phụ trách và bước xử lý.

Gate 1 yêu cầu kiểm kê đủ và không giấu trang lỗi; **không yêu cầu giả vờ mọi trang đều đọc được**. Trang chưa xác minh không được dùng để approve câu hỏi. Khi nguồn cần thiết chưa có, khóa phần đề phụ thuộc thay vì tạo câu hỏi thay thế.

## Taxonomy

- Phase 1 có thư mục riêng và bìa mẫu ghi Phase 1. Track 2/3 có bìa mẫu xác nhận Phase 2; không suy rộng mọi trang đã được kiểm tra.
- Track 1/4 được đề xuất thuộc Phase 2 theo brief/cấu trúc; phải giữ mức inferred cho tới bằng chứng hoặc xác nhận có lưu dấu.
- `day_in_filename` và `day_in_source` độc lập: Day1 của Track 1–3 có bìa ghi Day16. Không tạo quy tắc +15 cho toàn bộ bộ tài liệu chưa kiểm tra.
- Track 2 không có Day9 trong tên file: ghi missing_or_not_scheduled, chưa tự tạo ngày hoặc gộp bài.
- Topic lấy tiêu đề/section thực tế; tên file chỉ là gợi ý. Nhóm tự suy luận phải ghi inferred và không trình bày như lịch học gốc.
- Không đánh đồng `k3` với nội dung Phase hoặc tên track chính thức khi chưa có giải thích từ nguồn.
- Chặn phát hành taxonomy đang xung đột: `phase1/day 2 ai product.pdf` trang 1 có Track 1, và `track2 k3/day 3 tu chatbot den agentic agent.pdf` trang 1 có Phase 1. Không sửa/di chuyển nguồn để làm mất dấu xung đột; lưu quyết định xác minh trong mapping.

## Tạo câu hỏi theo batch

Chỉ sau Gate 1 và Root duyệt schema. Pilot 8–12 câu từ trang đã verified, gồm các dạng trả lời và ít nhất một tình huống/rubric khi nguồn hỗ trợ; không ép đủ loại bằng nội dung bịa. Batch tiếp theo đề xuất 15–25 câu trong một Day/Topic, điều chỉnh theo số lỗi sửa.

Mỗi batch có ID/revision, danh sách nguồn, thống kê Phase/Track/Day/Topic/type/format/difficulty, source coverage và câu bị chặn. Không lấy số câu làm thước đo duy nhất của coverage. Catalog phải phân biệt chưa trích xuất, chưa có câu, có câu nháp và có câu approved.

Câu hỏi kiểm tra hiểu/vận dụng/phân tích phải có đủ dữ kiện trong nguồn; có thể dựng tình huống giả định minh bạch dùng nguyên lý từ slide, nhưng không thêm khẳng định thực tế thiếu căn cứ. Giải thích chỉ rõ vì sao đáp án đúng; distractor hợp lý, không lộ đáp án bằng độ dài/diễn đạt hoặc phụ thuộc thứ tự option. Không dùng “tất cả đáp án trên” khi xáo lựa chọn.

## Dạng câu và chấm điểm

Single choice: ít nhất 2 option, một correct ID. Multiple choice: ít nhất 3 option, ít nhất 2 correct ID, ít nhất 1 distractor; chấm exact-set. True/false: correct boolean, không cần options. Short answer: đáp án mẫu + rubric với tiêu chí rõ và trọng số tổng 1. Scenario: context bắt buộc, chọn format single/multiple/rubric; không tạo engine chấm thứ năm.

Rubric phải nêu các ý thiết yếu, cách xử lý câu trả lời tương đương và điều kiện đạt từng tiêu chí. Không so khớp nguyên chuỗi câu tự luận. Câu bỏ trống 0; câu tự luận có nội dung chưa tự chấm ở trạng thái pending. Độ khó easy/medium/hard do nội dung quyết định và được hiệu chỉnh sau pilot; không tự suy ra từ số trang.

Mức đạt cho mỗi tiêu chí đề xuất 0 / 0,5 / 1; người viết phải nêu điều kiện không đạt/đạt một phần/đạt đầy đủ tương ứng. Điểm câu = điểm slot × tổng(weight × mức đạt), làm tròn half-up tới 0,01 điểm một lần ở cuối câu. Tổng bài cộng điểm câu bằng đơn vị nguyên; quy tắc này cần kiểm thử số lẻ và trường hợp đúng nửa đơn vị.

## Review độc lập và phát hành

Chu trình: draft → pending_review → approved hoặc rejected. Sau sửa nội dung/đáp án/nguồn/rubric/taxonomy, tăng revision, hủy approval cũ và quay pending_review. Reviewer không trực tiếp sửa dữ liệu do Question Engineer sở hữu.

Reviewer phải đọc trang gốc liên quan, kiểm tra đáp án/distractor/giải thích/phân loại/rubric và trùng lặp. Root kiểm tra artifact audit trước tích hợp; không dựa riêng vào báo cáo “đã xong”. Audit ghi question ID/revision, source/page, finding, severity, action, reviewer, thời gian, trạng thái retest.

Mức lỗi: critical = sai đáp án/nguồn bịa/lọt câu chưa duyệt; major = mơ hồ, thiếu rubric, sai taxonomy hoặc nguồn không đủ; minor = diễn đạt/format không đổi nghĩa. Mọi lỗi chưa giải quyết trong câu phát hành phải được xử lý; câu còn vấn đề chuyển ra khỏi release và không tính là approved khả dụng.

Script phát hiện trùng ID và trùng nội dung sau chuẩn hóa Unicode/whitespace; near-duplicate dùng similarity để gắn cờ, reviewer xác định hai câu có thật sự kiểm tra cùng ý. Không tự xóa câu bằng ngưỡng similarity. Reviewer khác tác giả, review đúng revision; một agent không tự approve toàn bộ batch mình tạo.

## Bài tính Track 4

Theo yêu cầu ngày 2026-10-23, bổ sung bài tính để luyện bằng máy tính Casio. Câu có `calculation: true` phải yêu cầu thao tác với dữ kiện số, nêu đơn vị/giả định cần thiết, quy tắc làm tròn khi kết quả không nguyên và lời giải thay số từng bước. Phương án nhiễu phản ánh lỗi tính hoặc dùng sai công thức. Công thức/khái niệm phải được đối chiếu PDF; dữ kiện giả định ghi trong đề, không biến thành tuyên bố thực nghiệm của nguồn.

Thuộc tính tùy chọn này giữ tương thích nội dung/lịch sử cũ. Lọc “Chỉ câu tính toán” vẫn tuân theo Phase/Track/ngày/chủ đề đã chọn. Đề mới đảm bảo ít nhất hai câu tính đã duyệt trong năm câu khách quan Track 4; không thêm slot, không đổi tổng 60 câu hoặc tỷ lệ điểm 60/40. Nếu thiếu hai câu tính, báo thiếu ngân hàng. Đây là cấu hình luyện tập của ứng dụng, không khẳng định tỷ lệ chính thức của đề thi.

## Các điều không được tuyên bố

PDF mở được không có nghĩa text đọc đúng; OCR thành công không có nghĩa công thức đúng; schema pass không có nghĩa đáp án đúng; đủ 63 file không có nghĩa đã đủ chương trình học. Discovery chỉ khảo sát và lập kế hoạch, chưa hoàn tất ingestion hoặc content audit.

## Mở rộng ôn trọng tâm — 2026-10-28

Yêu cầu mới cho phép kiến thức bổ sung ngoài slide nếu ghi rõ và dùng nguồn đáng tin cậy; phần này thay thế giới hạn chỉ dùng slide đối với nội dung mở rộng. Slide gốc vẫn được ưu tiên và xác định Phase/Track/Day. `supplemental_sources` ghi tiêu đề, HTTPS URL, ngày truy cập và phạm vi bổ sung. Reviewer độc lập phải đọc nguồn chính thống và ghi `supplemental_urls` trong quyết định đúng revision. Release chặn URL chưa được duyệt. Lời kể sau thi chỉ quyết định ưu tiên, không làm nguồn xác minh hoặc cơ sở quảng bá đề thật.

Hai dạng mới dùng ID ổn định. `matching` có `matching_items` và `options`, đáp án là ánh xạ ID trái → ID phải; mặc định một–một, `matching_reuse: true` cho phép dùng lại. Mỗi mục có thể kèm giải thích riêng. `ordering` có các bước trong `options`, đáp án là danh sách ID, `accepted_orders` chứa các thứ tự hợp lệ bổ sung. Không tạo thứ tự giả giữa các bước độc lập: gộp bước hoặc liệt kê các thứ tự hợp lệ. Cả hai dạng chấm đúng toàn bộ = đủ điểm, sai/thiếu/bỏ trống = 0, không trừ điểm. Không tự coi thứ tự xáo trộn ban đầu là câu trả lời.

`focus_topics` là nhóm ôn tập bổ sung, không thay taxonomy của tài liệu. Preset Ôn trọng tâm chọn cân bằng theo nhóm và dạng còn khả dụng; không thay cấu hình thi 60 câu hiện hành. Đề thi hiện hành không lấy hai dạng tương tác mới. `formula_reference` được duyệt cùng câu hỏi và revision, gồm công thức, ký hiệu, điều kiện, ví dụ và lỗi thường gặp. Không xuất bản công thức chưa được kiểm tra chỉ vì renderer hoặc schema chấp nhận.
