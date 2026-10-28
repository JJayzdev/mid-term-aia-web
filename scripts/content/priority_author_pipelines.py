from priority_author_common import *
order('p2-t4-d01','training-pipeline',[5,80],'Một bước SGD cơ bản đã lấy batch và đã xóa gradient cũ. Sắp xếp các thao tác sau.',[
 'Forward: tính dự đoán từ batch và weights hiện tại','Tính loss từ dự đoán và nhãn','Backward: tính gradient của loss theo weights','Optimizer update: cập nhật weights bằng gradient'],
 'Backward cần loss đã tính từ forward. Optimizer chỉ cập nhật sau khi gradient sẵn sàng; ở vòng tiếp theo cần quản lý/xóa gradient theo cấu hình, tránh cộng dồn ngoài ý muốn.')
order('p1-d07','rag-index',[43,50],'Trong pipeline dense RAG đơn giản đã chọn, sắp xếp quá trình tạo chỉ mục từ tài liệu chưa xử lý.',[
 'Nạp và xử lý văn bản tài liệu','Chia văn bản thành chunks cùng metadata nguồn','Tính embedding cho từng chunk','Lưu embeddings, chunks và metadata vào chỉ mục'],
 'Embedding được tính cho đơn vị chunk đã chọn; chỉ mục cần giữ liên kết vector với nội dung/nguồn. Đây là pipeline được mô tả, không áp cho mọi hệ thống tìm kiếm.')
order('p1-d08','rag-answer',[7,12,30,33],'Hệ thống RAG này có reranker. Sắp xếp đường trả lời từ lúc nhận câu hỏi.',[
 'Nhận và chuẩn bị query','Retrieval lấy các ứng viên phù hợp từ chỉ mục','Rerank các ứng viên đã truy xuất','Ghép context được chọn vào prompt cùng câu hỏi','Generation tạo câu trả lời từ context'],
 'Reranker cần tập ứng viên trước; generation cần context đã đóng gói. Rerank được nêu là thành phần của hệ thống này, không phải bước bắt buộc trong mọi RAG.')
order('p2-t4-d03','nms-pipeline',[28],'Sắp xếp greedy NMS cho các box cùng lớp. Giữ các box có confidence đạt ngưỡng; suppress khi IoU lớn hơn ngưỡng đã chọn.',[
 'Lọc box theo confidence','Sắp box còn lại theo confidence giảm dần','Giữ box có confidence lớn nhất còn lại','Loại các box còn lại có IoU với box vừa giữ lớn hơn ngưỡng','Lặp chọn–loại đến khi không còn ứng viên'],
 'NMS dùng box được giữ ở mỗi vòng để suppress các ứng viên còn lại. Confidence filtering xảy ra trước vòng; IoU đúng bằng ngưỡng không bị loại trong quy ước đề này.')
order('p2-t4-d07','tracking-pipeline',[10,11,14,21],'Trong tracking-by-detection, detection và predict track cũ có thể chạy độc lập. Sắp xếp các bước; hai thao tác độc lập đã gộp chung.',[
 'Tạo detections của frame mới và predict các track cũ','Tính cost/gating rồi association giữa track và detection','Update các track ghép được bằng detection tương ứng','Quản lý vòng đời: khởi tạo, giữ hoặc xóa các track theo policy'],
 'Association cần cả detections và vị trí track dự đoán. Không ép detection trước predict hay ngược lại khi độc lập; quản lý track mới/mất theo policy đã chọn.')
match('p2-t4-d01','activation-heads',[50,52,55,57],'Ghép một-một bài toán với dạng đầu ra/loss điển hình.',[
 ('Một nhãn nhị phân','Một sigmoid với binary cross-entropy','Sigmoid biểu diễn xác suất nhãn1, BCE xét nhãn0/1.'),('Nhiều nhãn có thể đồng thời đúng','Sigmoid độc lập mỗi nhãn với tổng hoặc trung bình BCE theo nhãn','Không buộc xác suất các nhãn cộng thành1.'),('Một lớp đúng trong C lớp loại trừ nhau','Softmax trên C logits với cross-entropy một nhãn','Chuẩn hóa tổng1 phù hợp giả định chọn một lớp.')],
 'Cần khớp giả định nhãn với head/loss. Một ảnh có cả chó và xe không phải bài toán chỉ được chọn một lớp nếu cả hai nhãn đều cần dự đoán.',focus='activations')
mc('p2-t4-d01','activation-tanh-gradient',[15,16,26],'Một neuron có a=tanh(x)=0,6 và upstream dL/da=3. Dùng da/dx=1−a². Gradient dL/dx bằng bao nhiêu?',
 '1,92','0,72','0,64',
 'Từ công thức tanh, đạo hàm là1−tanh²(x). Thay a=0,6:1−0,36=0,64. Chain rule nhân upstream3 cho1,92. Dùng a(1−a) là đạo hàm sigmoid, cho sai0,72.',focus='activations',calc=True,
 formula=('Đạo hàm tanh và chain rule','a=tanh(x); da/dx=1−a²; dL/dx=(dL/da)×(1−a²)','a: đầu ra tanh; dL/da: gradient truyền từ lớp sau.','Đạo hàm được suy ra từ công thức tanh bằng quy tắc đạo hàm thương; không dùng đạo hàm sigmoid thay thế.','a=0,6,upstream=3 →3×(1−0,36)=1,92.','Nhầm với a(1−a); bỏ gradient từ lớp sau.'))
save('pipelines')
