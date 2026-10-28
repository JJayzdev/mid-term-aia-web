from pathlib import Path
import json
p=Path('data/questions/drafts/priority-normalization.json');b=json.loads(p.read_text(encoding='utf-8'))
q=next(q for q in b['questions'] if q['id'].endswith('norm-symbols'));q['revision']=2
q['options'][0]['text']='Mean/variance dùng để chuẩn hóa, từ nhóm hiện tại hoặc running statistics tùy chế độ'
q['matching_items'][0]['explanation']='Trục quyết định nhóm; BatchNorm thông thường dùng running statistics khi inference.'
q['formula_reference']['symbols']='mu: trung bình; variance: phương sai dùng để chuẩn hóa; epsilon: ổn định số; gamma,beta: tham số học được.'
q['formula_reference']['conditions']='Phải xác định trục, chế độ train/inference và quy ước variance. Trong các ví dụ B×D dùng thống kê hiện tại ở đây, BN theo cột qua B; LN theo hàng qua D. BatchNorm thông thường dùng running statistics khi inference.'
cat={d['document_id']:d for d in json.loads(Path('content/catalog.json').read_text(encoding='utf-8'))['documents']};d=cat['p2-t4-d02']
q['source_reference'].append(dict(document_id=d['document_id'],sha256=d['sha256'],pdf_page=17,title=d['title'],locator='Physical PDF page 17',verification='needs_review'))
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('data/questions/drafts/priority-generation.json');b=json.loads(p.read_text(encoding='utf-8'));q=next(q for q in b['questions'] if q['id'].endswith('generation-truth'));q['revision']=2
for s in q['source_reference']:
 if s['document_id']=='p2-t2-d07':s['pdf_page']=9;s['locator']='Physical PDF page 9'
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
