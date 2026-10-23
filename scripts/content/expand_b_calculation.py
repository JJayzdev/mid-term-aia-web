# -*- coding: utf-8 -*-
"""New calculator practice only; existing reviewed banks are never modified."""
from author_common import *

def calc(day,pages,prompt,options,why):
 doc=f'p2-t4-d{day:02}'
 add(doc,pages[0],'single_choice',prompt,'a',why,options)
 q=qs[-1];q['id']=f'{doc}-c{sum(x["topic"]==doc for x in qs):02}'
 q.update(author_id='question-engineer-b',calculation=True,cognitive_level='apply',difficulty='medium')
 for p in pages[1:]:extra_page(doc,p)

calc(1,[51],
 'Một batch hồi quy có dự đoán (4, 2, 2) và nhãn (2, 5, 1). Dùng MSE=(1/n)Σ(y_hat−y)², không có hệ số 1/2. MSE của batch bằng bao nhiêu? Làm tròn 3 chữ số thập phân.',
 ['4,667','14,000','2,333','2,000'],
 'Các sai số là 2, −3, 1; tổng bình phương=4+9+1=14. Lấy trung bình trên 3 mẫu: MSE=14/3≈4,667. Giá trị 2,333 xuất hiện nếu thêm nhầm hệ số 1/2.')
calc(1,[12,15],
 'Một lớp tính z=Wx+b rồi a=ReLU(z)=max(0,z) theo từng phần tử. Ma trận W có hàng thứ nhất (1; −2), hàng thứ hai (0,5; 1); x=(2; 3), b=(1; −1). Dấu phẩy trong 0,5 là dấu thập phân. Vector a là gì?',
 ['(0; 3)','(−3; 3)','(0; 4)','(0; 2)'],
 'Nơ-ron thứ nhất: z1=1×2−2×3+1=−3. Nơ-ron thứ hai: z2=0,5×2+1×3−1=3. ReLU chặn giá trị âm nên a=(0;3).')
calc(2,[7,9],
 'Convolution nhận ảnh 32×32, C_in=4, C_out=8, kernel k=3, stride s=2, padding p=1, dilation d=1. Dùng H_out=floor((H_in+2p−d(k−1)−1)/s)+1 và MAC=H_out×W_out×C_out×C_in×k²; bỏ chi phí bias. Kích thước output và số MAC là bao nhiêu?',
 ['16×16 và 73.728 MAC','17×17 và 83.232 MAC','16×16 và 18.432 MAC','16×16 và 296 MAC'],
 'H_out=W_out=floor((32+2−2−1)/2)+1=16. MAC=16×16×8×4×9=73.728. 296 là số tham số có bias, không phải số MAC.')
calc(2,[25],
 'Một ô LSTM vô hướng có c_prev=2, forget gate f=0,75, input gate i=0,4, ứng viên c_tilde=−0,5 và output gate o=0,6. Dùng c=f×c_prev+i×c_tilde, h=o×tanh(c). Giá trị (c,h) là gì? Làm tròn h đến 4 chữ số thập phân.',
 ['(1,3; 0,5170)','(1,7; 0,5612)','(1,3; 0,7800)'],
 'Ô nhớ mới c=0,75×2+0,4×(−0,5)=1,3. Sau đó h=0,6×tanh(1,3)≈0,5170. Bỏ tanh sẽ cho sai h=0,78; bỏ dấu âm của ứng viên sẽ cho c=1,7.')
calc(3,[45],
 'Tại ngưỡng confidence triển khai, detector có TP=72, FP=18 và FN=8. Dùng P=TP/(TP+FP), R=TP/(TP+FN), F1=2PR/(P+R). Bộ (P,R,F1) nào đúng? Làm tròn 4 chữ số thập phân.',
 ['(0,8000; 0,9000; 0,8471)','(0,9000; 0,8000; 0,8471)','(0,8000; 0,9000; 0,8500)'],
 'P=72/90=0,8; R=72/80=0,9. F1=2×0,8×0,9/1,7≈0,8471. Trung bình số học (0,8+0,9)/2=0,85 không phải F1.')
calc(3,[13],
 'Ảnh gốc 800×600 được letterbox thành 640×640: scale=0,8, padding trái=0 và padding trên=80 pixel. Box xyxy trên ảnh letterbox là (80,160,400,400). Trừ padding rồi chia scale cho từng tọa độ. Box xyxy trên ảnh gốc là gì?',
 ['(100,100,500,400)','(100,200,500,500)','(80,80,400,320)','(100,120,500,420)'],
 'x1=80/0,8=100; y1=(160−80)/0,8=100; x2=400/0,8=500; y2=(400−80)/0,8=400. Padding phải được trừ trong hệ tọa độ ảnh letterbox trước khi chia scale.')
calc(4,[8],
 'Hai camera RGB không nén, mỗi camera 1280×720 pixel, 24 bit/pixel, 30 frame/s, truyền chung một link 1,0 Gbit/s. Bỏ overhead và dùng 1 Gbit=10^9 bit. Với bitrate=N_camera×W×H×bits_per_pixel×FPS, tổng bitrate là bao nhiêu và link có đủ không? Làm tròn 4 chữ số thập phân.',
 ['1,3271 Gbit/s; không đủ','0,6636 Gbit/s; đủ','0,1659 Gbit/s; đủ'],
 'Mỗi camera cần 1280×720×24×30=663.552.000 bit/s. Hai camera cần 1.327.104.000 bit/s=1,327104 Gbit/s, vượt 1,0 Gbit/s ngay cả khi chưa tính overhead. Chia thêm 8 sẽ nhầm bit với byte.')
calc(4,[16],
 'Một frame 640×480 có 18.432 pixel bão hòa. Health policy cảnh báo khi saturated pixel ratio lớn hơn 5%. Tính ratio=100×số pixel bão hòa/(W×H). Ratio và quyết định nào đúng?',
 ['6%; có cảnh báo','0,06%; không cảnh báo','3%; không cảnh báo'],
 'Tổng pixel=640×480=307.200. Ratio=100×18.432/307.200=6%, lớn hơn ngưỡng 5% nên cảnh báo. 0,06 là tỷ lệ chưa đổi sang phần trăm.')
calc(5,[17],
 'Kalman update vô hướng có prediction x_pred=20 m, variance P=9 m², measurement z=26 m và variance R=3 m². Dùng K=P/(P+R), x_new=x_pred+K(z−x_pred). Bộ (K,x_new) là gì?',
 ['(0,75; 24,5 m)','(0,25; 21,5 m)','(0,75; 39,5 m)'],
 'K=9/(9+3)=0,75. Innovation=26−20=6 m; x_new=20+0,75×6=24,5 m. Dùng R ở tử số đảo mức tin measurement; dùng z thay innovation tạo 39,5 m.')
calc(5,[36],
 'Ba ước lượng vị trí Gaussian độc lập có variance lần lượt 4, 9 và 36 m². Theo dạng thông tin, I_total=Σ(1/P_i), P_fused=1/I_total, sigma_fused=sqrt(P_fused). Bộ (P_fused,sigma_fused) là gì? Làm tròn 4 chữ số thập phân.',
 ['(2,5714 m²; 1,6036 m)','(0,3889 m²; 0,6236 m)','(16,3333 m²; 4,0415 m)'],
 'I_total=1/4+1/9+1/36=14/36=7/18 m^−2. P_fused=18/7≈2,5714 m²; sigma=sqrt(18/7)≈1,6036 m. Lấy trung bình variance hoặc coi information là variance đều sai.')
calc(6,[9],
 'Một voxel grid phủ x∈[−20,20) m, y∈[−10,10) m, z∈[−2,2) m, với voxel size (0,2;0,2;0,4) m. Giả sử lưu dense một giá trị float32 4 byte cho mỗi ô, không metadata; 1 MB=10^6 byte. Tổng số ô có thể có và bộ nhớ dense là bao nhiêu?',
 ['200.000 ô; 0,8 MB','400.000 ô; 1,6 MB','20.000 ô; 0,08 MB'],
 'Số ô theo x,y,z lần lượt 40/0,2=200, 20/0,2=100, 4/0,4=10. Tổng=200×100×10=200.000; bộ nhớ=200.000×4=800.000 byte=0,8 MB. Đây là grid dense giả định, không phải số voxel không rỗng của sparse convolution.')
calc(6,[16],
 'Điểm LiDAR (1,2,8) m được đưa sang camera bằng x_cam=R×x_lidar+t, với R là identity và t=(1,−1,2) m. Camera pinhole không distortion có fx=400, fy=500, cx=320, cy=240 pixel; u=fx×X/Z+cx, v=fy×Y/Z+cy. Pixel (u,v) là gì?',
 ['(400; 290)','(370; 365)','(1120; 740)'],
 'Sau extrinsic: (X,Y,Z)=(2,1,10) m. Chiếu pinhole: u=400×2/10+320=400; v=500×1/10+240=290. Bỏ translation cho (370;365); quên chia depth cho (1120;740).')

calc(7,[20],
 'Ghép một-một ba tracks A,B,C với ba detections 1,2,3. Ma trận cost có các hàng A=(1;2;9), B=(2;9;9), C=(9;3;1). Không bỏ unmatched và tổng cost là tổng ba cặp. Phương án ghép tối ưu toàn cục cùng tổng cost là gì?',
 ['A→2, B→1, C→3; tổng 5','A→1, B→2, C→3; tổng 11','A→1, B→3, C→2; tổng 13'],
 'Ghép A→2,B→1,C→3 có cost 2+2+1=5. Sáu hoán vị có tổng lần lượt 11,13,5,20,14,27; nhỏ nhất là 5. Chọn cặp rẻ nhất A→1 trước có thể ép B vào cặp đắt.')
calc(7,[38],
 'Sau global identity matching, một tracker có IDTP=120, IDFP=30 và IDFN=50. Dùng IDF1=2×IDTP/(2×IDTP+IDFP+IDFN). IDF1 bằng bao nhiêu? Làm tròn 2 chữ số sau dấu phẩy theo phần trăm.',
 ['75,00%','80,00%','70,59%'],
 'Tử số=2×120=240; mẫu số=240+30+50=320. IDF1=240/320=75%. 80% là identity precision, còn 70,59% là identity recall; cả hai không thay IDF1.')
calc(8,[7],
 'Camera nhìn ngang trên mặt đường phẳng có độ cao h=1,5 m, focal length f=800 pixel. Chân vật cách đường chân trời Δv=40 pixel; Z=f×h/Δv. Nếu sai số Δv là ±2 pixel và các giả định khác đúng, khoảng Z nhỏ nhất/lớn nhất là gì? Làm tròn 3 chữ số thập phân.',
 ['28,571 m đến 31,579 m','28,500 m đến 31,500 m','31,579 m đến 28,571 m'],
 'Z danh định=800×1,5/40=30 m. Vì Z tỉ lệ nghịch Δv, Z_min=1200/42≈28,571 m và Z_max=1200/38≈31,579 m. Hai biên không đối xứng tuyến tính quanh 30 m.')
calc(8,[12],
 'Dùng NDS=[5×mAP+Σ(1−min(1,e_i))]/10 cho năm TP errors đã được quy về đúng thang của công thức. Cho mAP=0,6 và (e1,e2,e3,e4,e5)=(0,2;0,3;0,1;0,4;0,5). NDS là bao nhiêu? Làm tròn 3 chữ số thập phân.',
 ['0,650','0,450','0,683'],
 'Năm quality terms là 0,8;0,7;0,9;0,6;0,5, tổng 3,5. Phần detection=5×0,6=3. NDS=(3+3,5)/10=0,65. Cộng trực tiếp error thay 1−error cho 0,45; trung bình sáu thành phần không trọng số cho khoảng 0,683.')
calc(9,[24],
 'Video có FPS cố định 30, dài đúng 45 giây, gồm các frame index 0 đến 1349. Pipeline lấy frame 0 rồi mỗi frame thứ 9: 0,9,18,…; embedding batch size=16, batch cuối thiếu vẫn được chạy. Có bao nhiêu frame được chọn và bao nhiêu batch cần chạy?',
 ['150 frame; 10 batch','150 frame; 9 batch','151 frame; 10 batch','1.350 frame; 85 batch'],
 'Video có 30×45=1.350 frame; chọn các bội của 9 từ 0 đến 1341 được 150 frame. Số batch=ceil(150/16)=10, gồm 9 batch đủ và một batch 6 frame. Không có frame index1350.')
calc(9,[54],
 'Một batch 1.000 nhãn máy được route theo policy giả định: 600 nhãn confidence cao chỉ audit 10%, mỗi audit 5 giây; 300 nhãn trung bình đều review 8 giây/nhãn; 100 nhãn thấp đều vẽ lại 30 giây/nhãn. Bỏ overhead. So với vẽ thủ công cả 1.000 nhãn ở 30 giây/nhãn, tổng thời gian mới và phần trăm giảm là bao nhiêu?',
 ['95 phút; giảm 81%','140 phút; giảm 72%','90 phút; giảm 82%'],
 'Audit cao:600×10%×5=300 giây; review:300×8=2.400 giây; vẽ lại:100×30=3.000 giây. Tổng=5.700 giây=95 phút. Baseline=30.000 giây=500 phút; giảm=(30.000−5.700)/30.000=81%. Các ngưỡng và thời gian đều là giả định của bài.')
calc(10,[14],
 'Một VLM trả box xyxy chuẩn hóa theo thang 0–1000: (100;200;300;500), trên ảnh W=1920,H=1080 pixel. Dùng x_px=x_norm×W/1000, y_px=y_norm×H/1000; diện tích=(x2−x1)(y2−y1), không cộng 1. Kích thước box và diện tích pixel là gì?',
 ['384×324 pixel; 124.416 pixel²','384×576 pixel; 221.184 pixel²','200×300 pixel; 60.000 pixel²'],
 'x1=192,x2=576 nên width=384; y1=216,y2=540 nên height=324. Diện tích=384×324=124.416 pixel². Trục y phải nhân H thay W; các số chuẩn hóa không phải tọa độ pixel.')
calc(10,[16],
 'Một MoE giả định có tổng 24 tỉ tham số nhưng chỉ 3 tỉ active/token. Toàn bộ weights phải resident, mỗi weight 2 byte và shard đều lên 4 GPU. Bỏ KV cache, activations và overhead; 1 GB=10^9 byte. Dung lượng weights tổng và trên mỗi GPU là bao nhiêu?',
 ['48 GB tổng; 12 GB/GPU','6 GB tổng; 1,5 GB/GPU','48 GB tổng; 48 GB/GPU'],
 'Dung lượng weights theo tổng tham số:24×10^9×2=48×10^9 byte=48 GB. Shard đều bốn GPU cho 48/4=12 GB/GPU. Active/token liên quan phần compute, không thay tổng weights cần resident theo giả định.')
calc(11,[46],
 'Đo vị trí có nhiễu độc lập ở mỗi thời điểm với độ lệch chuẩn sigma_x=0,04 m. Với sai phân bậc hai, sigma_a=sqrt(6)×sigma_x/(Δt)². Tính sigma_a khi Δt=0,2 s và khi Δt=0,1 s. Làm tròn 3 chữ số thập phân.',
 ['2,449 và 9,798 m/s²','2,449 và 4,899 m/s²','0,490 và 0,980 m/s²'],
 'Với Δt=0,2: sqrt(6)×0,04/0,04≈2,449 m/s². Với Δt=0,1: sqrt(6)×0,04/0,01≈9,798 m/s². Giảm một nửa bước thời gian làm nhiễu gia tốc tăng bốn lần, không phải hai lần.')
calc(11,[49],
 'Một trajectory có tốc độ v=12 m/s và độ cong kappa=0,04 m^−1. Dùng gia tốc ngang a_lat=v²×kappa và giới hạn khả thi a_limit=mu×g với mu=0,5, g=9,81 m/s². Theo riêng cổng kiểm này, trajectory đạt không? Làm tròn 3 chữ số thập phân.',
 ['Không đạt: a_lat=5,760 lớn hơn giới hạn 4,905 m/s²','Đạt: a_lat=0,480 nhỏ hơn giới hạn 4,905 m/s²','Đạt: a_lat=5,760 nhỏ hơn giới hạn 9,810 m/s²'],
 'a_lat=12²×0,04=5,76 m/s²; a_limit=0,5×9,81=4,905 m/s². Vì 5,76>4,905 nên không đạt cổng này. Dùng v thay v² hoặc bỏ hệ số ma sát sẽ đánh giá sai.')
calc(12,[44],
 'Hai xe có tốc độ tiến gần tương đối 12 m/s, khoảng cách 18 m. Trong mô hình giảm tốc đều được cho bởi a_req=v_close²/(2d), dùng mốc phanh êm 3 m/s² và giới hạn minh họa 8 m/s². a_req và phân loại nào đúng?',
 ['4 m/s²; vượt mức êm nhưng chưa vượt giới hạn','0,333 m/s²; nằm dưới mức phanh êm','8 m/s²; đúng bằng giới hạn'],
 'a_req=12²/(2×18)=144/36=4 m/s². Giá trị nằm giữa 3 và 8 m/s². Quên bình phương cho 0,333; quên hệ số 2 ở mẫu cho 8. Đây là mô hình đơn giản và các mốc minh họa đã cho.')
calc(12,[68],
 'Một controller dự đoán độ đổi vận tốc tại 0,5 s là y5=−5,5 m/s. Quy tắc điều khiển là a_raw=y5/0,5 s, rồi clip a_raw vào [−9;+3] m/s². Bộ (a_raw,a_command) là gì?',
 ['(−11; −9) m/s²','(−2,75; −2,75) m/s²','(−11; +3) m/s²'],
 'a_raw=−5,5/0,5=−11 m/s². Vì thấp hơn biên dưới −9, lệnh sau clip là −9 m/s². Nhân 0,5 thay chia cho sai đơn vị; clip vào biên trên +3 làm sai chiều điều khiển.')

for q in qs:
 if q['id']=='p2-t4-d01-c02':q['revision']=2
save('expand-t4-calculation')
