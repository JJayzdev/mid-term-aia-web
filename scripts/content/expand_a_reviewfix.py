import json,pathlib
p=pathlib.Path('data/questions/drafts/expand-a-001.json')
d=json.loads(p.read_text(encoding='utf-8'))
for q in d['questions']:
 if q['id']=='p1-d02-x06':
  q['question']='Trường Boundary của Problem Card cho một trợ giảng AI có chức năng gì?'
  q['explanation']='Boundary xác định giới hạn hành động: trợ giảng AI không tự chấm điểm và chuyển câu hỏi chuyên sâu cho TA duyệt.'
 elif q['id']=='p1-d01-x16':
  q['question']='Với response schema có usage.input_tokens, usage.output_tokens và stop_reason, những trường nào giúp phân tích chi phí và nguyên nhân kết thúc lần gọi? (Chọn tất cả đáp án đúng.)'
 elif q['id']=='p1-d03-x10':
  q['question']='Có thể chọn cách tiếp cận Hybrid để kết hợp native structured tool calls với khả năng theo dõi reasoning/trace khi debug.'
  q['explanation']='Hybrid kết hợp native Function Calling với reasoning/trace, nhằm giữ cấu trúc gọi tool và khả năng quan sát quá trình xử lý.'
 else:continue
 q['revision']+=1
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
