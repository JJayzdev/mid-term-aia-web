import json,pathlib
R=pathlib.Path.cwd()
def fix(batch,id,stem=None,correct=None,wrong=None,page=None,addpage=None,why=None):
 p=R/f'data/questions/drafts/expand-a-{batch:03}.json';b=json.loads(p.read_text(encoding='utf-8'));q=next(q for q in b['questions'] if q['id']==id)
 if stem:q['question']=stem
 if correct:next(o for o in q['options'] if o['id']==q['correct_answer'])['text']=correct
 if wrong:
  os=[o for o in q['options'] if o['id']!=q['correct_answer']]
  assert len(os)==len(wrong)
  for o,t in zip(os,wrong):o['text']=t
 if page:q['source_reference'][0].update(pdf_page=page,locator=f'Physical PDF page {page}')
 if addpage:
  s=dict(q['source_reference'][0]);s.update(pdf_page=addpage,locator=f'Physical PDF page {addpage}');q['source_reference'].append(s)
 if why:q['explanation']=why
 q['revision']+=1;p.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
fix(6,'p2-t1-d01-x04',stem='Product sense giúp PM đánh giá một giải pháp mới theo cách nào?',correct='Nhận diện pattern tương tự rồi xét mức phù hợp và tác động lên outcome đang cần',wrong=['Sao chép pattern thành công mà không xét khác biệt bối cảnh','Dựa vào mức quen thuộc của giao diện để suy ra outcome'],page=40,why='Product sense liên hệ kinh nghiệm thành công/thất bại với vấn đề hiện tại, nhưng phải đánh giá giống thật hay chỉ giống bề ngoài.')
fix(6,'p2-t1-d01-x10',wrong=['Tiếp tục tự sửa từng output mà không định nghĩa tiêu chí','Chỉ đo agreement giữa raters mà chưa thống nhất tiêu chí chất lượng'])
fix(6,'p2-t1-d02-x08',addpage=16)
fix(6,'p2-t1-d03-x02',addpage=5)
fix(6,'p2-t1-d03-x13',stem='Một thử nghiệm prototype khiến nhóm bỏ phương án đang ưu ái có thể được xem là thành công khi nào?',correct='Bằng chứng làm thay đổi quyết định thiết kế theo điều nhóm cần học',wrong=['Chỉ khi phần lớn người thử khen phương án ban đầu','Chỉ khi demo hoàn tất trơn tru dù không ảnh hưởng quyết định'],page=20,why='Thử nghiệm phục vụ học và quyết định; một kết quả làm đổi hướng có giá trị hơn lời khen không tạo hành động.')
