import json,pathlib
p=pathlib.Path('data/questions/drafts/expand-a-001.json');d=json.loads(p.read_text(encoding='utf-8'))
q=next(q for q in d['questions'] if q['id']=='p1-d01-x07');new='Những nội dung nào có thể nằm trong một Agent Skill? (Chọn tất cả đáp án đúng.)'
if q['question']!=new:q['question']=new;q['revision']+=1
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
q=next(q for q in d['questions'] if q['id']=='p1-d01-x04');new='Streaming từng khâu của voice pipeline giảm độ trễ cảm nhận bằng cơ chế nào?'
if q['question']!=new:
 q['question']=new;q['revision']+=1;q['explanation']='Khâu sau có thể bắt đầu xử lý các phần output mới xuất hiện, thay vì chờ LLM sinh xong toàn bộ câu rồi TTS mới đọc.'
 correct=q['correct_answer'];next(o for o in q['options'] if o['id']==correct)['text']='Chuyển phần output vừa sinh sang khâu sau trước khi toàn bộ câu hoàn thành'
 for o,t in zip([o for o in q['options'] if o['id']!=correct],['Đợi LLM hoàn tất toàn câu rồi chuyển nguyên câu cho TTS','Chỉ giảm max_tokens nhưng vẫn chờ toàn bộ output sinh xong mới bắt đầu đọc']):o['text']=t
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
