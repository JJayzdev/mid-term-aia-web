import json
from pathlib import Path
p=Path('data/questions/drafts/priority-d-geometry.json');b=json.loads(p.read_text(encoding='utf-8'))
for q in b['questions']:
 if q['id'].endswith('d-voxel-resolution'):
  q['revision']=2;q['question']=q['question'].replace('Grid dense giữ nguyên range.','Grid dense giữ nguyên range, mỗi chiều range chia hết cho voxel size ban đầu, không có ô biên một phần.')
 if q['id'].endswith('d-nds-saturation'):
  q['revision']=2;q['formula_reference']['conditions']='Depth giả định camera có trục quang song song mặt đường phẳng (hoặc ảnh đã rectified về mô hình đó), độ cao và đường chân trời đã biết, chân vật nằm trên đường; delta_v>0. NDS dùng đúng giao thức nuScenes, không tự gộp các error khác đơn vị ngoài quy ước.'
 if q['id'].endswith('d-batch-drop'):
  q['revision']=2;q['question']=q['question'].replace('drop_last=true:', 'drop_last=true (bỏ toàn bộ batch cuối nếu thiếu phần tử):')
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
