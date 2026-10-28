from pathlib import Path
import json
p=Path('data/questions/drafts/priority-kalman.json');b=json.loads(p.read_text(encoding='utf-8'))
q=next(q for q in b['questions'] if q['id'].endswith('kalman-sensitivity'))
q.update(revision=2,question='Hai cấu hình vô hướng H=1 có (P_pred,R)=(9,3) và (3,1), đều đơn vị m². Gain và variance sau update thay đổi thế nào?',correct_answer='a',explanation='Cấu hình đầu K=9/12=0,75,P_new=0,25×9=2,25 m². Cấu hình sau K=3/4=0,75,P_new=0,25×3=0,75 m². Cả P_pred và R cùng giảm 3 lần nên tỷ số gain không đổi; không thể xét riêng việc R giảm khi P_pred cũng đổi.',calculation=True,cognitive_level='apply')
q.pop('context',None);q['question_type']='single_choice';q['options']=[{'id':'a','text':'K cùng bằng 0,75; P_new giảm từ 2,25 xuống 0,75 m²'},{'id':'b','text':'K tăng vì R giảm; P_new không đổi'},{'id':'c','text':'K giảm 3 lần; P_new tăng 3 lần'}]
q=next(q for q in b['questions'] if q['id'].endswith('kalman-ekf'));q.update(revision=2,question_type='matching',answer_format='matching',question='Ghép một-một họ bộ lọc với cách xử lý mô hình hoặc biểu diễn bất định.',correct_answer={'l1':'a','l2':'b','l3':'c','l4':'d'},explanation='Kalman tuyến tính dùng mô hình tuyến tính và Gaussian; EKF tuyến tính hóa cục bộ; UKF truyền sigma points; particle filter dùng tập hạt. Các phương pháp khác nhau về giả định và cách xấp xỉ, không phải chỉ khác tên.',matching_reuse=False,shuffle_options=True)
q.pop('context',None)
pairs=[('Kalman tuyến tính','Mô hình tuyến tính, bất định Gaussian qua mean/covariance','Bộ lọc chuẩn dùng các phép biến đổi tuyến tính.'),('EKF','Tuyến tính hóa cục bộ bằng Jacobian','EKF dùng đạo hàm tại ước lượng đang xét.'),('UKF','Truyền các sigma points qua hàm phi tuyến','UKF tránh phải tính Jacobian bằng cách chọn các điểm đại diện.'),('Particle filter','Biểu diễn phân phối bằng tập hạt có trọng số','Tập hạt có thể mô tả phân phối phức tạp hơn một Gaussian.')]
q['options']=[{'id':chr(97+i),'text':v[1]} for i,v in enumerate(pairs)];q['matching_items']=[{'id':f'l{i+1}','text':v[0],'explanation':v[2]} for i,v in enumerate(pairs)]
base=q['source_reference'][0];q['source_reference']=[dict(base,pdf_page=n,locator=f'Physical PDF page {n}') for n in [30,31,32,33]]
p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
