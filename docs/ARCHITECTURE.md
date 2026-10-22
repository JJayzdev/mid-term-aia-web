# Kiến trúc đề xuất

Trạng thái: Discovery, chưa duyệt, chưa triển khai. Đường dẫn bên dưới là **đề xuất tương lai** trừ `slide/`, `docs/` và mẫu trong `tmp/discovery/`.

## Hiện trạng và lựa chọn

Không có codebase ứng dụng hay framework để giữ lại; chỉ có nguồn PDF. Đề xuất React + TypeScript + Vite, SPA tiếng Việt, static hosting, IndexedDB cho phiên thi/lịch sử/bookmark và dữ liệu người dùng. Cài đặt trực tiếp trong workspace hiện tại sau phê duyệt; chưa chốt phiên bản dependency trong Discovery.

Vite có mẫu React/TypeScript và build static assets ([tài liệu chính thức](https://vite.dev/guide/)). IndexedDB hỗ trợ dữ liệu có cấu trúc và transaction ở phía trình duyệt ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)); phù hợp hơn một JSON localStorage lớn cho nhiều phiên và migration. UI state cục bộ bằng React, logic nghiệp vụ là hàm thuần; chưa cần thư viện state toàn cục hoặc backend. Routing dùng hash để static host không cần rewrite; có thể đổi nếu môi trường triển khai yêu cầu.

## Ranh giới module và dữ liệu

```text
slide/ (nguồn, chỉ đọc)
  -> content/manifest.json + content/extracted/<document-id>/pages.jsonl
  -> content/catalog.json + content/mapping.json + extraction-issues.json
  -> data/questions/drafts/<batch-id>.json
  -> reports/content/<batch-id>.md (review độc lập)
  -> data/questions/approved/<release-id>.json
  -> public/data/bank.json (Root tạo bản phát hành)
  -> src/domain/ (lọc, blueprint, sinh đề, chấm điểm)
  -> src/storage/ (IndexedDB, transaction, migration, import/export)
  -> src/features/ (dashboard, practice, exam, results, data-management)
```

`src/domain/` không phụ thuộc DOM, timer hoặc IndexedDB; nhận clock/RNG/persistence qua interface khi cần. Không đóng gói toàn bộ PDF vào static bundle theo mặc định; lưu đường dẫn nguồn và trang để truy vết. Việc hiển thị PDF ngay trong web cần quyết định phân phối nguồn và dung lượng sau.

## Hợp đồng câu hỏi

Bản schema máy đọc đề xuất: [schemas/question-bank.schema.json](schemas/question-bank.schema.json), JSON Schema draft 2020-12, `schema_version=0.1.0-proposal`. Chưa phải schema được Root duyệt cho sản xuất. Mỗi package gồm `schema_version`, `bank_version`, `questions`.

| Trường | Quy tắc |
|---|---|
| id, revision, author_id | ID ổn định, revision tăng khi nội dung thay đổi; tác giả phục vụ kiểm tra reviewer độc lập |
| phase, track, day, topic | Phase 1/2 hoặc null ở bản nháp; Phase 1 track=null, Phase 2 track=1..4; day có thể null khi nguồn không cho ngày; topic là ID catalog |
| taxonomy_status | unresolved/inferred/verified; approved yêu cầu verified, kể cả khi verified bằng xác nhận người dùng có ghi nguồn |
| question_type | single_choice, multiple_choice, true_false, short_answer, scenario |
| answer_format | single_choice, multiple_choice, boolean, rubric; scenario phải chọn một hình thức phù hợp |
| difficulty, cognitive_level | easy/medium/hard; remember/understand/apply/analyze, có review độ khó sau pilot |
| question, context, options | Nội dung câu; context bắt buộc với scenario; options chỉ áp dụng hình thức lựa chọn, ID không phụ thuộc vị trí |
| correct_answer | ID option / tập ID / boolean / mẫu trả lời theo answer_format |
| rubric | Với rubric: tiêu chí có ID, mô tả, trọng số chuẩn hóa tổng 1; nhân với điểm slot khi chấm |
| explanation | Giải thích dựa nguồn, không chỉ nhắc lại đáp án |
| source_reference | Danh sách document ID, SHA256, trang vật lý PDF (1-based), số slide in trên trang nếu có, tiêu đề, trạng thái kiểm chứng |
| status, review, review_notes | draft/pending_review/approved/rejected; approved phải có review đúng revision và người khác author |

JSON Schema kiểm tra kiểu và điều kiện theo dạng câu. Validator nghiệp vụ phải kiểm tra ID duy nhất, đáp án nằm trong options, option ID duy nhất, multiple choice có ít nhất một nhiễu, rubric tổng 1, review đúng revision/người độc lập, nguồn/trang/hash thật, taxonomy tồn tại trong catalog, gần trùng và quota. Không tuyên bố JSON Schema đủ để chứng minh nội dung đúng.

## Manifest và catalog

Manifest chứa ID ổn định, đường dẫn tương đối, hash, byte, số trang, parser/version/config, thời điểm chạy, trạng thái lỗi. Mỗi trang giữ `pdf_page` làm khóa; `printed_slide_label` là chuỗi riêng để không nhầm số slide với chỉ số PDF. Text, bảng, công thức và figure có locator/page/bounding box; mỗi đối tượng có extraction_method, confidence nếu engine cung cấp, verification và issue_ids.

Mapping lưu riêng `day_in_filename`, `day_in_source`, `day_key`, `mapping_status`, `evidence`, `confirmed_by`. Day key dạng `p2-t2-local-01` chỉ được phát hành sau xác nhận hệ đánh số; UI có thể hiển thị “Ngày 1 trong Track · Ngày 16 trên slide”. Không gom track này với track khác chỉ vì cùng số ngày. Topic sơ bộ lấy tên file phải ghi inferred, chỉ verified sau đối chiếu trang liên quan.

## Blueprint và bộ tạo đề

Dùng đơn vị nguyên 0,01 điểm (100 điểm = 10.000 units). Blueprint bao gồm duration, totalUnits, tỷ trọng Phase/Track, tỷ lệ tự luận, danh sách slot theo phase/track/answer_format/độ khó, seed, algorithmVersion và bankVersion. Phase và tỷ lệ tự luận phải đúng trên tổng điểm; không làm tròn âm thầm.

Mặc định 100 điểm:

| Nhóm | Khách quan | Tự luận | Tổng |
|---|---:|---:|---:|
| Phase 1 | 54 | 6 | 60 |
| Phase 2 / Track 1 | 9 | 1 | 10 |
| Phase 2 / Track 2 | 9 | 1 | 10 |
| Phase 2 / Track 3 | 9 | 1 | 10 |
| Phase 2 / Track 4 | 9 | 1 | 10 |
| Tổng | 90 | 10 | 100 |

Ví dụ blueprint khả thi để làm fixture: Phase 1 gồm 18 câu khách quan ×3 điểm + 2 tự luận ngắn ×3; mỗi track Phase 2 gồm 3 khách quan ×3 + 1 tự luận ngắn ×1. Tổng 36 câu, 30 khách quan, 6 tự luận; **chưa chốt số câu thi mặc định**, cần pilot về thời gian/độ khó. Điểm thuộc slot, không gắn cứng trong ngân hàng; rubric chuẩn hóa cho phép dùng lại câu ở nhiều chế độ.

Với trọng số track w tổng bằng 1, mỗi track nhận `40w`, khách quan `36w`, tự luận `4w` điểm. Cấu hình nhập phải có đủ 4 trọng số dương, tổng đúng 1 theo biểu diễn rational/units; không normalize hay phân bổ phần dư âm thầm. Từ chối cấu hình không biểu diễn chính xác hoặc không đủ slot/câu cho từng nhóm.

Thuật toán: validate cấu hình → lọc approved + đúng revision review → phân bucket không giao nhau → kiểm tra số câu đủ cho từng bucket → lấy mẫu seeded không hoàn lại → gán điểm slot → xáo thứ tự câu/options an toàn → kiểm tra lại invariants → lưu snapshot trước khi mở bài. Nếu cấu hình tạo điều kiện chồng lấn, validator phải có phép ghép đầy đủ hoặc từ chối, không dùng greedy gây báo thiếu giả. Stable sort theo ID trước RNG, lưu phiên bản thuật toán và thứ tự option ID để seed tái tạo được với cùng bank/config/version. Không xáo các lựa chọn phụ thuộc thứ tự (ví dụ “cả A và B”); tốt hơn sửa câu tại content review.

Khi thiếu dữ liệu, trả lỗi cấu trúc gồm phase/track/format/difficulty, required/available/missing; không lấy nhóm khác bù. Giới hạn số câu vừa sức chốt sau pilot, không dùng việc tăng số câu để che thiếu coverage.

## Phiên thi, đồng hồ và chấm điểm

Lưu `attemptId`, `mode`, `status`, `startedAt`, `deadlineAt`, `submittedAt`, `finalizedAt`, config/seed/version, snapshot câu hỏi/rubric/điểm/options, đáp án, cờ đánh dấu và revision của phiên. Snapshot bảo đảm sửa ngân hàng không làm đổi điểm lịch sử.

Luồng trạng thái: prepared → in_progress → submitted_pending_grading hoặc graded. Nộp bài là transaction idempotent theo attemptId; viết answers, trạng thái, điểm khách quan và sự kiện lịch sử cùng transaction. Nộp lặp hoặc hai tab chỉ có một kết quả. Dùng revision/CAS trong transaction để chỉ một tab được ghi; tab còn lại chuyển read-only và tải trạng thái mới.

Thời gian hiển thị = max(0, deadlineAt − clock.now()); interval chỉ cập nhật UI. Trước mỗi thao tác ghi/trả lời/chuyển câu/nộp và lúc resume/visibilitychange phải kiểm tra deadline. Trình duyệt hạn chế timer ở tab nền ([MDN Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API)); do đó không trừ bộ đếm từng giây làm nguồn chân lý. Đáp án phải commit sau từng thay đổi, không đợi unload; hiển thị trạng thái lưu, không báo “đã lưu” khi transaction thất bại. Hết hạn khóa thay đổi; lấy bản đáp án commit hợp lệ cuối cùng. Khi đóng trình duyệt, nộp thực tế ở lần mở lại, `submittedAt=deadlineAt`, `finalizedAt=thời điểm xử lý` cho auto-submit.

Điểm mỗi câu khách quan là 0 hoặc điểm slot. Rubric tính tổng trọng số tiêu chí đạt nhân điểm slot, theo bước điểm cho phép, không vượt max. Bài tự luận không rỗng chưa chấm không phải câu sai; ghi pending và không đưa vào Wrong Review. Tổng cuối cùng = khách quan + rubric đã chấm; dashboard tách điểm tạm/chưa chấm/tự chấm. Topic chính duy nhất cho mỗi câu dùng phân rã điểm không đếm hai lần; tags phụ chỉ để lọc.

Đề xuất mỗi tiêu chí rubric có mức đạt 0 / 0,5 / 1 theo mô tả no_credit / partial_credit / full_credit. Dùng số thập phân chính xác hoặc rational để tính; làm tròn half-up một lần ở điểm cuối của mỗi câu tới 0,01 điểm, sau đó cộng các số nguyên units. Kiểm tra trọng số rubric tổng đúng 1 trước nhập. Đây là làm tròn điểm người học, không cho phép làm tròn quota blueprint.

## Lưu trữ và import/export

IndexedDB stores đề xuất: settings, installedBanks, importStaging, attempts, bookmarks, schemaMigrations. Lịch sử đã nộp bất biến trừ revision chấm rubric có audit; không giữ đáp án chỉ trong component state. Migration có version và transaction; lỗi/quota phải giữ bản dữ liệu trước và hiển thị cách export/khôi phục.

Import parse JSON → schema → kiểm tra nghiệp vụ → preview số câu/xung đột → commit nguyên tử. File sai không ghi một phần. Import câu hỏi từ bên ngoài đưa vào staging/pending_review kể cả tự ghi `approved`; chỉ release workflow có review được đối chiếu mới kích hoạt cho Mock Exam. Restore backup cá nhân là luồng riêng, có version và preview, không biến câu hỏi chưa duyệt thành approved. Giới hạn kích thước file/số câu trước khi parse sâu; không render HTML tùy ý từ question text.

Local-only không đồng bộ, không có server time, không chống người dùng sửa dữ liệu/đồng hồ; phù hợp tự học. Khi cần nhiều thiết bị hoặc thi chính thức, phải xem lại kiến trúc với backend thay vì gọi local-only là giải pháp đã đáp ứng.
