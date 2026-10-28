import json
from pathlib import Path
def edit(name,fn):
 p=Path(f'data/questions/drafts/priority-{name}.json');b=json.loads(p.read_text(encoding='utf-8'));fn(b['questions']);p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sup(title,url,note):return dict(title=title,url=url,accessed_at='2026-10-28',note=note)
def pipelines(qs):
 q=next(q for q in qs if q['id'].endswith('activation-heads'));q['revision']=2;q['supplemental_sources']=[sup('PyTorch BCEWithLogitsLoss','https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html','Bổ sung ngoài slide: sigmoid riêng từng nhãn và binary cross-entropy cho multi-label; không buộc tổng xác suất các nhãn bằng 1.')]
 q=next(q for q in qs if q['id'].endswith('tracking-pipeline'));q['revision']=2
 q['options']=q['options'][:3];q['options'][2]['text']='Update track ghép được và quản lý vòng đời: tạo, giữ hoặc xóa track theo policy'
 q['correct_answer']=['a','b','c'];q['question']='Trong tracking-by-detection, detection và predict track cũ có thể chạy độc lập. Sắp xếp các nhóm thao tác; update và quản lý vòng đời cùng thuộc bước cuối.'
 q['explanation']='Association cần detections và track dự đoán. Sau association, cập nhật track có match và xử lý track không match/detection thừa theo policy. Các thao tác độc lập trong cùng nhóm không bị ép thứ tự.'
 for r in q['source_reference']:
  if r['pdf_page']==21:r['pdf_page']=12;r['locator']='Physical PDF page 12'
def sensors(qs):
 q=next(q for q in qs if q['id'].endswith('sensor-strengths'));q['revision']=3
 q['source_reference']=[r for r in q['source_reference'] if not(r['document_id']=='p2-t4-d05' and r['pdf_page']==35)]
 q['supplemental_sources']=[sup('NOAA JetStream — Radar Images: Velocity','https://www.noaa.gov/jetstream/velocity','Bổ sung ngoài slide: phép đo Doppler chỉ cho thành phần vận tốc tương đối theo tia nhìn, không trực tiếp cho toàn bộ vector vận tốc; nguyên lý xuyên tâm từ ví dụ radar khí tượng.')]
edit('pipelines',pipelines);edit('sensors',sensors)
