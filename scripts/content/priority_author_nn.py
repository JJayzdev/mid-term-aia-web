from priority_author_common import *
D='p2-t4-d01';F='activations'
match(D,'activation-ranges',[15,53],'Ghép một-một hàm với miền đầu ra và đặc điểm chuẩn hóa.',[
 ('Sigmoid','Mỗi đầu ra nằm trong (0,1), không buộc nhiều đầu ra cộng thành 1','Sigmoid tác động độc lập lên từng logit.'),('Tanh','Đầu ra trong (−1,1), đối xứng quanh 0','Tanh cho cả giá trị âm và dương hữu hạn.'),('ReLU','Đầu ra trong [0,+∞), chặn phần âm','ReLU bằng0 khi đầu vào âm và bằng đầu vào khi dương.'),('Softmax','Vector dương có tổng các phần tử bằng1','Mẫu số dùng tổng exp của mọi logit nên các đầu ra phụ thuộc nhau.')],
 'Sigmoid và softmax đều có thể biểu diễn xác suất nhưng cấu trúc chuẩn hóa khác nhau. ReLU không bị chặn ở1.',focus=F)
match(D,'activation-formulas',[15,53],'Ghép một-một hàm kích hoạt với công thức; x là vô hướng và z là vector logit.',[
 ('Sigmoid','1/(1+exp(−x))','Mẫu số lớn khi x âm nên sigmoid gần0.'),('Tanh','(exp(x)−exp(−x))/(exp(x)+exp(−x))','Tử đổi dấu khi x đổi dấu, mẫu không đổi.'),('ReLU','max(0,x)','Phép max chặn giá trị âm.'),('Softmax tại phần tử i','exp(z_i)/Σ_j exp(z_j)','Tổng theo toàn bộ lớp tạo phân phối chuẩn hóa.')],
 'Không thay softmax bằng argmax: argmax chọn chỉ số, còn softmax trả cả vector xác suất.',focus=F,
 formula=('Sigmoid, tanh, ReLU và softmax','sigmoid(x)=1/(1+exp(−x)); tanh(x)=(exp(x)−exp(−x))/(exp(x)+exp(−x)); ReLU(x)=max(0,x); softmax(z)_i=exp(z_i)/Σ_j exp(z_j)','x: đầu vào vô hướng; z_i: logit lớp i; tổng j chạy qua mọi lớp.','Các logit hữu hạn; softmax áp trên trục lớp. Trừ max logit trước exp để ổn định số học.','Với (−1;0;1): sigmoid≈(0,269;0,500;0,731), tanh≈(−0,762;0;0,762), ReLU=(0;0;1), softmax≈(0,090;0,245;0,665).','Nhầm sigmoid riêng từng phần tử với softmax; coi argmax là vector xác suất; tính exp(logit lớn) trực tiếp gây tràn.'))
mc(D,'activation-sigmoid-value',[15],'Với x=(−1;0;1), áp sigmoid độc lập từng phần tử. Vector nào đúng? Làm tròn 3 chữ số thập phân.',
 '(0,269;0,500;0,731)','(0,090;0,245;0,665)','(−0,762;0;0,762)',
 'Thay số vào1/(1+exp(−x)): tại−1 là1/(1+e)≈0,269; tại0 là0,5; tại1 là1/(1+e⁻¹)≈0,731. Vector tổng1 thuộc softmax; vector có phần tử âm thuộc tanh.',focus=F,calc=True)
mc(D,'activation-tanh-value',[15],'Với x=(−1;0;1), áp tanh từng phần tử. Vector nào đúng? Làm tròn 3 chữ số thập phân.',
 '(−0,762;0;0,762)','(0,269;0,500;0,731)','(0;0;1)',
 'tanh(1)=(e−e⁻¹)/(e+e⁻¹)≈0,761594; tanh là hàm lẻ nên tanh(−1)≈−0,762; tanh(0)=0. Sigmoid luôn dương; ReLU chặn âm nhưng giữ1.',focus=F,calc=True)
mc(D,'activation-softmax-value',[53],'Một mẫu có logits z=(−1;0;1). Tính softmax trên ba lớp. Vector nào đúng? Làm tròn 3 chữ số thập phân.',
 '(0,090;0,245;0,665)','(0,269;0,500;0,731)','(0;0;1)',
 'Trừ max=1: z_shift=(−2;−1;0). exp≈(0,135335;0,367879;1), tổng≈1,503214. Chia từng phần tử cho tổng cho (0,090031;0,244728;0,665241). One-hot argmax chỉ chọn lớp cao nhất, không giữ phân phối.',focus=F,calc=True)
mc(D,'activation-derivative',[17,26],'Một neuron sigmoid đã có đầu ra s=0,8; upstream gradient dL/ds=2. Gradient dL/dz bằng bao nhiêu?',
 '0,32','1,6','0,16',
 'Đạo hàm sigmoid theo logit: ds/dz=s(1−s)=0,8×0,2=0,16. Chain rule: dL/dz=2×0,16=0,32. 0,16 bỏ upstream gradient;1,6 bỏ thừa số(1−s).',focus=F,calc=True,
 formula=('Đạo hàm sigmoid và ReLU','sigmoid′(z)=s×(1−s); ReLU′(z)=1 khi z>0, =0 khi z<0','s=sigmoid(z); upstream gradient nhân đạo hàm cục bộ theo chain rule.','ReLU không khả vi tại0; bài tính phải nêu quy ước nếu xét đúng0.','s=0,8, upstream=2 → gradient logit=2×0,8×0,2=0,32.','Quên upstream gradient; cho ReLU gradient1 ở miền âm; khẳng định đạo hàm toán học duy nhất tại0.'))
mc(D,'activation-stable',[53],'Softmax với logits (1000;1001;1002) dễ tràn exp. Cách nào giữ nguyên phân phối mà ổn định số học?',
 'Trừ1002 khỏi cả ba logits rồi tính softmax','Chia từng logit cho1002 rồi nói phân phối không đổi','Thay softmax bằng argmax vì cả hai luôn cùng vector',
 'Cộng/trừ cùng một hằng số làm tử và mẫu cùng nhân một hệ số nên triệt tiêu. Chia logits là thay nhiệt độ, thường đổi phân phối; argmax chỉ giữ chỉ số lớn nhất.',focus=F,context='Bạn triển khai softmax trên vector logit lớn và phát hiện exp trả giá trị vô hạn.')
mc(D,'activation-dead-relu',[15,26,45],'Một neuron ReLU nhận z<0 cho mọi mẫu trong nhiều bước. Gradient qua kích hoạt bằng0. Rủi ro nào phù hợp?',
 'Neuron có thể không nhận được tín hiệu gradient để cập nhật từ nhánh này','Đầu ra bắt buộc bão hòa tại1 như sigmoid','Gradient qua ReLU luôn bằng1 nên không có vấn đề',
 'ReLU chặn cả đầu ra và gradient khi z<0, tạo nguy cơ neuron chết nếu duy trì miền âm. Sigmoid bão hòa ở hai đầu theo cơ chế khác; ReLU không chặn trên tại1.',focus=F,context='Theo dõi activation cho thấy một kênh luôn bằng0 và pre-activation luôn âm; chưa xét các nhánh cập nhật khác.')
mc(D,'activation-batch-gradient',[56,69],'Batch hai mẫu có softmax p1=(0,8;0,2), y1=(1;0); p2=(0,3;0,7), y2=(0;1). Loss là trung bình CE hai mẫu. Gradient theo logits của mẫu thứ nhất là gì?',
 '(−0,1;0,1)','(−0,2;0,2)','(0,8;0,2)',
 'Gradient từng mẫu của CE là p−y. Với mẫu1: (−0,2;0,2). Loss lấy trung bình hai mẫu nên chia2, được (−0,1;0,1). Không cộng gradient logits của mẫu khác vào logits mẫu1.',focus=F,calc=True,
 formula=('Softmax + cross-entropy','L=−ln(p_true); dL/dz=p−y; nếu loss trung bình B mẫu, gradient mỗi mẫu=(p−y)/B','p: vector softmax; y: one-hot; B: số mẫu trong batch; ln: log tự nhiên.','Một nhãn đúng mỗi mẫu; cách reduction phải ghi rõ sum hay mean.','p=(0,8;0,2),y=(1;0),B=2 → gradient logits=(−0,1;0,1).','Quên chia B; dùng log10; hiểu gradient là p thay p−y.'))
save('activations')
F='normalization'
match(D,'norm-symbols',[77],'Ghép một-một ký hiệu trong x_hat=(x−mu)/sqrt(variance+epsilon), y=gamma×x_hat+beta.',[
 ('mu và variance','Thống kê của nhóm phần tử đang chuẩn hóa','Nhóm được xác định bởi trục của BatchNorm hoặc LayerNorm.'),('epsilon','Số dương nhỏ giúp tránh chia cho0','Epsilon nằm trong căn cùng variance, không phải hệ số học.'),('gamma','Hệ số co giãn học được','Gamma nhân giá trị đã chuẩn hóa.'),('beta','Hệ số dịch học được','Beta cộng sau phép co giãn.')],
 'Chuẩn hóa và affine là hai bước khác nhau. Sau gamma,beta, đầu ra không bắt buộc có mean0 và variance1.',focus=F,
 formula=('BatchNorm / LayerNorm — chuẩn hóa và affine','x_hat=(x−mu)/sqrt(variance+epsilon); y=gamma×x_hat+beta','mu: trung bình nhóm; variance: phương sai nhóm; epsilon: ổn định số; gamma,beta: tham số học được.','Phải xác định trục chuẩn hóa và quy ước variance. Trong các ví dụ B×D ở đây, BN theo cột qua B; LN theo hàng qua D.','X=[[1,3],[5,7]],gamma=1,beta=0,epsilon=0,variance chia n: BN=[[-1,-1],[1,1]],LN=[[-1,1],[-1,1]].','Nhầm trục; chia n−1 thay n khi đề quy định n; nhầm variance với sigma; bỏ affine.'))
match('p2-t4-d02','norm-axes',[17,34],'Ghép một-một trường hợp với nhóm phần tử dùng tính mean và variance. Các trục chuẩn hóa được chỉ rõ theo cấu hình trong đề.',[
 ('BatchNorm trên B×D, chuẩn hóa mỗi đặc trưng','Cố định d; lấy các mẫu trong B','Mỗi đặc trưng dùng thống kê qua batch.'),('LayerNorm trên B×D, normalized_shape=D','Cố định b; lấy các đặc trưng trong D','Mỗi mẫu được chuẩn hóa riêng.'),('BatchNorm2d trên N×C×H×W','Cố định c; lấy các phần tử trên N,H,W','Thống kê cùng kênh bao phủ batch và các vị trí không gian.'),('LayerNorm trên B×T×D, normalized_shape=D','Cố định b,t; lấy các phần tử trên D','Đề quy định trụcD nên mỗi token được chuẩn hóa riêng.')],
 'Tên phương pháp phải đi cùng hình dạng tensor và trục. Không lấy chung toàn bộ B,T,D nếu cấu hình LayerNorm chỉ chuẩn hóaD.',focus=F)
mc(D,'norm-bn-value',[77],'X=[[1,3],[5,7]] có hai mẫu (hàng), hai đặc trưng (cột). BatchNorm theo từng cột; gamma=1,beta=0,epsilon=0; variance chia số phần tử n. Output là gì?',
 '[[-1,-1],[1,1]]','[[-1,1],[-1,1]]','[[-2,-2],[2,2]]',
 'Mean hai cột=(3;5). Variance mỗi cột=((−2)²+2²)/2=4; sigma=2. Trừ mean rồi chia2 cho [[−1,−1],[1,1]]. Chuẩn hóa theo hàng là LayerNorm trong bài này, không phải BN.',focus=F,calc=True)
mc(D,'norm-ln-value',[77],'X=[[1,3],[5,7]] có hai mẫu. LayerNorm riêng từng hàng trên hai đặc trưng; gamma=1,beta=0,epsilon=0; variance chia n. Output là gì?',
 '[[-1,1],[-1,1]]','[[-1,-1],[1,1]]','[[0,1],[0,1]]',
 'Mean mỗi hàng lần lượt2 và6. Sai lệch mỗi hàng=(−1;1); variance=1; sigma=1. Vì vậy cả hai hàng chuẩn hóa thành(−1;1). Dịch offset chung của hàng không làm đổi kết quả này.',focus=F,calc=True)
mc(D,'norm-affine',[77],'Một nhóm có x_hat=(−1;1), mean0 và variance1. Dùng gamma=2,beta=3 cho cả nhóm. Output và mean/variance sau affine là gì?',
 'y=(1;5), mean=3, variance=4','y=(1;5), mean=0, variance=1','y=(−2;2), mean=0, variance=4',
 'y=2×x_hat+3=(1;5). Mean=(1+5)/2=3; variance=((1−3)²+(5−3)²)/2=4. Affine cho phép thay mean/scale; beta không được bỏ qua.',focus=F,calc=True)
mc(D,'norm-epsilon',[77],'Một nhóm chuẩn hóa có x=(2;2), gamma=1,beta=0,epsilon=0,01; variance chia n. Output là gì?',
 '(0;0)','Không xác định vì variance=0 dù epsilon dương','(20;20)',
 'Mean=2,variance=0. x−mu=(0;0); mẫu sqrt(0+0,01)=0,1. Output=(0;0). Epsilon làm mẫu khác0; quên trừ mean mới tạo20.',focus=F,calc=True)
mc('p2-t4-d02','norm-inference',[17],'Cần kiểm tra điều gì đầu tiên khi đầu ra CNN dùng BatchNorm thay đổi theo các ảnh khác cùng batch lúc suy luận?','Model đã chuyển sang eval và dùng running statistics hay chưa','Tăng temperature của softmax vì BatchNorm không dùng thống kê','Đổi mọi gamma thành0 để luôn nhận cùng đầu ra',
 'BatchNorm thông thường dùng running statistics khi inference, nên một ảnh không còn phụ thuộc batch hiện tại. Quên eval có thể khiến dùng batch statistics. Gamma=0 phá biểu diễn thay vì sửa chế độ.',focus=F,context='Cùng một ảnh và weights, kết quả thay đổi khi bạn ghép ảnh đó với các ảnh khác trong batch; chưa bật dropout hay tăng cường dữ liệu.')
save('normalization')
