import json,pathlib
R=pathlib.Path.cwd()
def change(batch,id,stem,choices,why,page):
 p=R/f'data/questions/drafts/expand-a-{batch:03}.json';b=json.loads(p.read_text(encoding='utf-8'));q=next(q for q in b['questions'] if q['id']==id)
 q.update(question=stem,question_type='single_choice',answer_format='single_choice',correct_answer='b',options=[{'id':'a','text':choices[1]},{'id':'b','text':choices[0]},{'id':'c','text':choices[2]}],explanation=why,revision=q['revision']+1)
 s=dict(q['source_reference'][0]);s.update(pdf_page=page,locator=f'Physical PDF page {page}');q['source_reference']=[s]
 p.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
def addpage(batch,id,page):
 p=R/f'data/questions/drafts/expand-a-{batch:03}.json';b=json.loads(p.read_text(encoding='utf-8'));q=next(q for q in b['questions'] if q['id']==id);s=dict(q['source_reference'][0]);s.update(pdf_page=page,locator=f'Physical PDF page {page}');q['source_reference'].append(s);q['revision']+=1;p.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
addpage(8,'p2-t1-d07-x02',7)
change(8,'p2-t1-d07-x03','Ba kịch bản optimistic, base và pessimistic phục vụ lập kế hoạch theo cách nào?', ['Base để budget khả thi; pessimistic để stress-test và chuẩn bị cắt scope','Chỉ dùng optimistic vì đó là mức tăng trưởng cần đạt','Gộp ba kịch bản thành một số trung bình rồi bỏ giả định riêng'],'Kịch bản giữ các giả định khác nhau hiển thị để đội hiểu khả năng sống sót khi điều kiện xấu.',27)
change(8,'p2-t1-d08-x02','Hybrid pricing có thể gây khó khăn nào dù giúp cân bằng rủi ro?', ['Cần giải thích cả phí nền lẫn phần usage để khách hiểu hóa đơn','Không thể đo usage khi có phí nền','Mặc nhiên quy mọi kết quả kinh doanh cho AI mà không cần attribution'],'Hybrid phối hợp đơn vị thu phí nên có thể phức tạp hơn khi giải thích, khác một khoản seat cố định.',7)
change(8,'p2-t1-d09-x06','Nếu evidence cho thấy giả định về nhóm khách ban đầu sai, lựa chọn nào phù hợp hơn tiếp tục sửa cùng tính năng?', ['Đổi hướng về nhóm khách, cách bán hoặc cách tính tiền phù hợp hơn','Giữ nguyên mọi giả định và coi mọi thất bại là thiếu quảng cáo','Lặp lại cùng sửa chữa dù chưa rõ vì sao chưa đạt mốc'],'Pivot phản ứng với giả định nền tảng sai, khác sửa một nguyên nhân đã hiểu trong hướng vẫn có cơ sở.',32)
change(8,'p2-t1-d09-x10','Một mốc kiểm tra 30 ngày đầu của sản phẩm mới nên ưu tiên bằng chứng nào?', ['Hiểu và đo được việc người dùng nhận giá trị ban đầu','Chỉ yêu cầu revenue lớn dù chưa có baseline hành vi','Chỉ đếm số tính năng hoàn tất mà không xác định core value'],'Mốc đầu phục vụ học và tạo số nền trước các mốc giữ chân, giá trị và mở rộng tiếp theo.',32)
change(8,'p2-t1-d09-x17','Trước khi bán theo outcome qua partner, hai bên cần thống nhất điều gì?', ['Cách quy công kết quả cho đóng góp của từng bên','Chỉ tổng số tài khoản partner sở hữu','Chỉ thời điểm ký hợp đồng mà chưa xác định thành công'],'Nếu cả hai cùng nhận công mà attribution chưa rõ, đơn vị thu tiền theo kết quả sẽ khó kiểm chứng và thương lượng.',25)
addpage(9,'p2-t1-d10-x02',10)
change(9,'p2-t1-d11-x06','Nhân viên chưa hiểu vì sao quy trình cần thay đổi. Can thiệp ADKAR nào phù hợp nhất?', ['Làm rõ vấn đề công việc và tác động của thay đổi','Chỉ thưởng theo số lần dùng AI trước khi giải thích mục đích','Chỉ tổ chức thực hành thao tác mà không nói nhu cầu thay đổi'],'Awareness giải quyết hiểu lý do thay đổi, khác Ability hoặc Reinforcement.',12)
change(9,'p2-t1-d11-x07','Nhân viên đã hiểu lý do đổi nhưng còn lo ngại và chưa muốn tham gia. Cần xử lý yếu tố nào?', ['Desire: giải quyết trở ngại và mối lo tạo động lực thay đổi','Chỉ Knowledge: bổ sung thêm hướng dẫn thao tác bất kể động lực','Chỉ Reinforcement: đo hành vi đã ổn định rồi thưởng'],'Desire là lý do muốn thay đổi; biết vì sao chưa đồng nghĩa muốn hoặc sẵn sàng thay đổi.',12)
change(9,'p2-t1-d11-x08','Trong trợ lý tra cứu nội bộ, phân công nào giữ đúng trách nhiệm kết quả?', ['AI tìm/tóm tắt; người kiểm chứng, phê duyệt và xử lý ngoại lệ','AI tóm tắt xong thì tự coi nội dung thành tài liệu chính thức','Người chỉ gửi prompt còn mọi câu hỏi nhạy cảm giao AI quyết cuối'],'Tăng tốc tìm thông tin không chuyển trách nhiệm phê duyệt cuối và xử lý ngoại lệ ra khỏi người.',22)
# Reviewer A002 vocabulary correction, preserve answer ID.
p=R/'data/questions/drafts/expand-a-002.json';b=json.loads(p.read_text(encoding='utf-8'));q=next(q for q in b['questions'] if q['id']=='p1-d04-x04')
for o in q['options']:
 if 'bản nháp mới nhất' in o['text']:o['text']=o['text'].replace('bản nháp mới nhất','bản cập nhật mới nhất')
q['revision']+=1;p.write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
