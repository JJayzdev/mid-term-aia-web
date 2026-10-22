import pathlib,json,collections,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
catalog=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));results=[];methods=collections.Counter();empty=[];errors=[]
for doc in catalog['documents']:
 p=ROOT/doc['extracted_path'];d=json.loads(p.read_text(encoding='utf-8'));assert d['sha256']==doc['sha256'];assert len(d['pages'])==doc['page_count'];assert hashlib.sha256((ROOT/doc['relative_path']).read_bytes()).hexdigest()==doc['sha256']
 for page in d['pages']:
  page['status']='extracted_unverified';methods[page['method']]+=1
  if not page['text'].strip():empty.append({'document_id':doc['document_id'],'pdf_page':page['pdf_page']})
  if page.get('error'):errors.append({'document_id':doc['document_id'],'pdf_page':page['pdf_page'],'error':page['error']})
 d['provenance']['ocr_language']='en-US';d['provenance']['ocr_model']='Windows installed OCR en-US; exact OS model version not exposed';d['provenance']['verification']='Text extraction/OCR never implies source-content verification'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 results.append({'document_id':doc['document_id'],'pages':doc['page_count'],'source_hash_matches':True})
report={'schema_version':'1.0.0','documents':len(results),'pages':sum(d['pages'] for d in results),'method_counts':dict(methods),'errors':errors,'empty_pages':empty,'all_source_hashes_unchanged':True,'all_pages_status':'extracted_unverified','coverage_meaning':'Complete technical extraction attempt for every physical PDF page; not complete semantic verification or question concept coverage.','quality_limitations':['en-US OCR degrades Vietnamese accents; OCR math, code and reading order may be wrong.','Native text with private-use/replacement glyphs or fewer than40nonwhitespace chars was rerendered/OCRed.','Independent question review must inspect rendered cited PDF pages.','Raw corpus remains local; never included in public web bundle.'],'results':results}
report['empty_page_visual_review']={'method':'A1 rendered and visually inspected three zero-text pages at80DPI; contact sheet tmp/content-tools/empty-audit/contact.png','observations':[{'document_id':'p1-d03','pdf_page':92,'observation':'QR-code image, no substantive lesson text visible'},{'document_id':'p2-t1-d04','pdf_page':46,'observation':'Essentially blank white page with logo/watermark; no substantive lesson text visible'},{'document_id':'p2-t3-d12','pdf_page':77,'observation':'Q&A title card; OCR missed visible Q&A text'}],'question_usage':'No drafted question cites these pages'}
(ROOT/'reports/ingestion/audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
text=f'''# Báo cáo ingest cục bộ

- 63/63 PDF, 3.589/3.589 trang vật lý đã được thử trích xuất.
- SHA-256 của toàn bộ PDF sau ingest khớp inventory; không sửa nguồn.
- Phương pháp: {dict(methods)}.
- Lỗi xử lý: {len(errors)}; trang không có text sau xử lý: {len(empty)} (chi tiết trong audit.json).
- Cache theo SHA-256 tài liệu và trang; provenance lưu engine, ngôn ngữ, DPI, revision pipeline. Chạy lại `scripts/content/ingest.py` dùng cache hợp cấu hình; thiếu bản text Markdown sẽ được tái tạo.
- Pipeline render 115DPI, OCR Windows.Media.Ocr en-US trong bộ nhớ; không upload nguồn. Chạy tối đa3 process tài liệu. Render tạm được dọn tại đường dẫn đã kiểm tra nằm trong tmp/content-tools/renders.
- Mọi trang mang trạng thái extracted_unverified. Đủ 3.589 lượt trích xuất không có nghĩa đã hiểu/kiểm chứng đủ mọi khái niệm. OCR tiếng Việt, thứ tự đọc, công thức, code cần kiểm tra bằng trang PDF gốc.
- Mapping học tập theo policy root: thư mục phase1→Phase1, thư mục track→Phase2/track tương ứng; Day theo tên file. Bằng chứng bìa và xung đột vẫn giữ nguyên trong catalog. Không tạo Day9 Track2.
- Bản rawtext/cache chỉ dùng cục bộ. Website/Git public chỉ nhận catalog gọn và câu hỏi đã được reviewer độc lập duyệt.

## Tái lập

Bundled Python có pypdf/pdfplumber/pypdfium2: chạy `scripts/content/ingest.py --workers 3`, rồi `scripts/content/audit_ingestion.py`. Windows PowerShell5 (`powershell.exe`) và OCR en-US đã có sẵn. Chính sách script chỉ bỏ chặn trong process cục bộ qua `-ExecutionPolicy Bypass`, không sửa cấu hình máy. Validator schema chạy bằng system Python có jsonschema, vì bundled Python không có package này.
'''
(ROOT/'reports/ingestion/README.md').write_text(text,encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=True))
