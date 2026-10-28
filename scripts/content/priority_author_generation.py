from priority_author_common import *
D='p1-d01';F='generation';SUP=dict(title='Hugging Face Transformers v4.50.0 — GenerationConfig',url='https://huggingface.co/docs/transformers/v4.50.0/main_classes/text_generation#transformers.GenerationConfig',accessed_at='2026-10-28',note='Bổ sung ngoài slide: định nghĩa top-k sampling, tập nucleus nhỏ nhất và phân biệt ngân sách token đầu ra. Slide được dẫn để xác định chủ đề học.')
match(D,'generation-parameters',[33,39,40],'Ghép một-một tham số/giới hạn với vai trò. Cách đặt tên và hỗ trợ cụ thể tùy API/model.',[
 ('Temperature','Điều chỉnh độ tập trung của phân phối token','Temperature thay hình dạng phân phối, không phải bộ kiểm chứng sự thật.'),('Top-k sampling','Giữ k token có xác suất cao nhất','k là số ứng viên token ở bước sinh tiếp theo.'),('Top-p sampling','Giữ tập đầu nhỏ nhất có xác suất tích lũy đạt ít nhất p','Số token được giữ có thể thay đổi theo phân phối.'),('Max output tokens','Giới hạn ngân sách token đầu ra theo API','Token không đồng nghĩa với từ; không phải kích thước toàn bộ ngữ cảnh.'),('Context window','Dung lượng ngữ cảnh model có thể xử lý','Ngữ cảnh có thể chứa prompt, lịch sử và phần sinh; quy tắc cụ thể tùy model/API.')],
 'Các khái niệm điều khiển các khía cạnh khác nhau. Không suy rằng mọi model đều hỗ trợ cùng tên tham số, cùng khoảng giá trị hoặc cùng giới hạn.',focus=F)
BATCH[-1]['supplemental_sources']=[SUP]
mc(D,'generation-topk',[40],'Phân phối token A=0,40; B=0,30; C=0,15; D=0,10; E=0,05. Chỉ áp top-k=2, rồi chuẩn hóa lại. Xác suất mới của A và B là gì? Làm tròn 3 chữ số thập phân.',
 '(0,571;0,429)','(0,400;0,300)','(0,500;0,500)',
 'Top-k=2 giữ A,B có tổng0,70. Chuẩn hóa: A=0,40/0,70≈0,571; B=0,30/0,70≈0,429. Không giữ nguyên xác suất cũ vì tổng phải là1; cũng không đổi thành phân phối đều.',focus=F,calc=True,
 formula=('Lọc top-k/top-p và chuẩn hóa','p_new(i)=p(i)/Σ_{j∈S}p(j) nếu i∈S; ngoài S là0','S: tập token được giữ; top-k chọn k xác suất lớn nhất; top-p chọn tập đầu nhỏ nhất có tổng≥p.','Bài này chỉ dùng một bộ lọc tại một thời điểm; nêu quy tắc xử lý hòa nếu xác suất bằng nhau.','A=0,40,B=0,30,C=0,15,D=0,10,E=0,05: top-k2 giữA,B; top-p0,80 giữA,B,C với tổng0,85.','Nhầm top-p0,80 là giữ80% số token; bỏ token vừa làm tổng vượt ngưỡng; quên chuẩn hóa lại.'))
BATCH[-1]['supplemental_sources']=[SUP]
mc(D,'generation-topp',[40],'Phân phối A=0,40; B=0,30; C=0,15; D=0,10; E=0,05. Chỉ áp top-p=0,80 theo tập đầu nhỏ nhất có tổng đạt ít nhất p. Tập giữ và xác suất mới của C là gì? Làm tròn 3 chữ số thập phân.',
 'Giữ A,B,C; p_new(C)=0,176','Giữ A,B; p_new(C)=0','Giữ A,B,C,D; p_new(C)=0,158',
 'Tổng tích lũy:0,40;0,70;0,85. Mốc đầu tiên đạt0,80 là sau C nên giữ A,B,C. Sau chuẩn hóa p_new(C)=0,15/0,85≈0,176. Không bỏ C chỉ vì nó làm tổng vượt0,80.',focus=F,calc=True)
BATCH[-1]['supplemental_sources']=[SUP]
mc(D,'generation-boundary',[40],'Phân phối A=0,50; B=0,30; C=0,20. Với top-p=0,80, tập đầu nhỏ nhất được giữ là gì?',
 'A,B vì tổng đúng bằng0,80','Chỉ A vì thêm B chạm ngưỡng','A,B,C vì phải lớn hơn0,80',
 'Quy tắc là đạt ít nhất p, bao gồm bằng. A chưa đủ; A+B=0,80 vừa đủ. Thêm C không còn là tập đầu nhỏ nhất.',focus=F,calc=True)
BATCH[-1]['supplemental_sources']=[SUP]
mc(D,'generation-softmax-temperature',[40,('p2-t4-d01',53),('p2-t4-d02',77)],'Logits z=(0;ln3), nhiệt độ T=2>0. Dùng softmax(z/T). Xác suất lớp thứ hai bằng bao nhiêu? Làm tròn 3 chữ số thập phân.',
 '0,634','0,750','0,900',
 'z/T=(0;ln3/2), exp=(1;sqrt(3)). Xác suất thứ hai=sqrt(3)/(1+sqrt(3))≈0,634. T=1 mới cho3/4=0,750. Không thay T=0 vào phép chia.',focus=F,calc=True,
 formula=('Softmax có nhiệt độ dương','p_i=exp(z_i/T)/Σ_j exp(z_j/T), T>0','z_i: logit; T: nhiệt độ dương; p_i: xác suất sau chuẩn hóa.','T>0; thứ tự logit không đổi. T thấp tập trung hơn nhưng không chứng minh thông tin đúng.','z=(0;ln3),T=2 → p≈(0,366;0,634).','Thế trực tiếp T=0; cho rằng temperature thấp chữa hallucination; nhầm sampling với retrieval.'))
BATCH[-1]['supplemental_sources']=[SUP]
match(D,'generation-vs-retrieval',[40,('p1-d07',51)],'Ghép một-một cách dùng k hoặc token với đơn vị mà nó kiểm soát.',[
 ('Top-k sampling ở bước sinh','Các token ứng viên cho token tiếp theo','Lọc phân phối từ vựng trước khi chọn token.'),('Top-k retrieval trong RAG','Các đoạn/tài liệu truy xuất được trả về','Đây là số kết quả tìm kiếm, không phải số ứng viên từ vựng.'),('Max tokens đầu ra','Ngân sách token model được phép sinh','Giới hạn độ dài đầu ra, không phải số đoạn tài liệu được lấy.')],
 'Cùng ký hiệu k nhưng sampling và retrieval tác động lên hai tập khác nhau. Thay k của retriever không trực tiếp biến thành thay top-k của generator.',focus=F)
BATCH[-1]['supplemental_sources']=[SUP]
mc(D,'generation-budget',[33,39],'API giả định có context window4096 token và giới hạn output1024 token; quy tắc là input+output≤4096. Input đã dùng3500 token. Output tối đa theo cả hai giới hạn là bao nhiêu?',
 '596 token','1024 token','4096 token',
 'Phần ngữ cảnh còn lại=4096−3500=596. Output không vượt min(1024,596)=596 token. Đây là quy tắc API giả định đã nêu, không khẳng định mọi dịch vụ tính context giống nhau.',focus=F,calc=True)
mc(D,'generation-truth',[25,40,('p2-t2-d07',8)],'Muốn tăng độ tin cậy của câu trả lời, lựa chọn nào hợp lý khi đã giảm temperature?',
 'Vẫn kiểm chứng bằng nguồn/đánh giá; không coi sampling thấp là bảo đảm đúng hay tái lập tuyệt đối','Bỏ kiểm chứng vì temperature thấp khiến model chỉ phát biểu sự thật','Yêu cầu mọi API hỗ trợ top-k và cho rằng cùng prompt luôn ra cùng chuỗi',
 'Temperature điều chỉnh phân phối token, không xác minh sự thật. Tái lập còn phụ thuộc model, runtime và hệ thống; hỗ trợ tham số tùy API/model. Cần đánh giá hành vi trên tác vụ thật.',focus=F,context='Một ứng dụng trả lời câu hỏi dựa trên tài liệu vẫn có câu sai dù cấu hình sinh ít ngẫu nhiên.')
save('generation')
