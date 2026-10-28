from priority_author_common import *
mc('p2-t4-d04','d-video-budget',[8,16,24],
 'Camera không nén ghi 640×480 pixel, 24 bit/pixel, 25 frame/s trong 60 s. Ngân sách lưu là 1,00 GB (10^9 byte), bỏ overhead. Để vừa ngân sách trong cùng thời lượng, hệ số giảm dung lượng tối thiểu V_raw/V_saved là bao nhiêu?',
 '1,3824 lần','11,0592 lần','0,7234 lần',
 'Mỗi frame=640×480×24/8=921.600 byte. Có 25×60=1.500 frame, tổng 1.382.400.000 byte=1,3824 GB. Tỷ số raw/budget=1,3824/1=1,3824 lần. Đây là yêu cầu dung lượng; không khẳng định codec thực tế đạt tỷ số này với chất lượng chấp nhận được.',calc=True,
 formula=('Camera: bandwidth, lưu video và health/time sync','bitrate=N_camera×W×H×bits_per_pixel×FPS; bytes=bitrate×seconds/8; saturation_ratio=100×N_saturated/(W×H); displacement=v×delta_t',
 'W,H: pixel; FPS: frame/s; bitrate: bit/s; v: vận tốc tương đối; delta_t: lệch timestamp tính bằng giây.','Ảnh thô không nén, bit depth đã tính đủ kênh, bỏ overhead. 1 byte=8 bit; GB=10^9 byte nếu đề quy định. Dịch chuyển v×delta_t giả định vận tốc không đổi; saturation threshold là policy riêng.','640×480×24 bit×25 FPS×60 s/8=1,3824 GB; v=15 m/s,delta_t=0,04 s →0,6 m.','Nhầm bit/byte; quên số camera/kênh; dùng mili giây như giây; coi tỷ lệ nén dự kiến là kết quả chất lượng đã kiểm chứng.'))
mc('p2-t4-d06','d-voxel-resolution',[9],
 'Grid dense giữ nguyên range. Cấu hình mới giảm voxel size một nửa theo x,y, giữ nguyên z, đồng thời tăng feature từ 8 lên 16 float32 mỗi ô. Không metadata. Bộ nhớ mới gấp mấy lần cũ?',
 '8 lần','4 lần','16 lần',
 'Số ô theo x tăng 2 lần, y tăng 2 lần, z không đổi nên số ô tổng tăng 4 lần. Feature/ô tăng 16/8=2 lần. Bộ nhớ dense tăng 4×2=8 lần. Không nhân thêm 2 cho z vì z giữ nguyên.',calc=True,
 formula=('Voxel grid và bộ nhớ dense','N_x=range_x/voxel_x; N_y=range_y/voxel_y; N_z=range_z/voxel_z; N_cells=N_x×N_y×N_z; bytes=N_cells×features_per_cell×bytes_per_feature',
 'range: chiều dài miền mỗi trục; voxel: độ dài cạnh; features_per_cell: số giá trị mỗi ô.','Range chia hết cho voxel; miền nửa kín tránh đếm biên hai lần. Đây là dense; sparse phụ thuộc ô có dữ liệu và overhead chỉ mục, không suy trực tiếp bằng công thức dense.','Giảm một nửa voxel x,y và nhân đôi số feature →2×2×1×2=8 lần bộ nhớ.','Nhầm giảm một nửa cạnh với giảm một nửa số ô; quên kênh feature; áp số ô đầy đủ cho sparse mà không xét occupancy.'))
mc('p2-t4-d08','d-backproject-depth',[9,('p2-t4-d06',16)],
 'Camera pinhole không distortion có fx=fy=400,cx=320,cy=240 pixel. Pixel (u,v)=(400,240), depth dọc trục camera Z=10 m. Điểm 3D (X,Y,Z) và khoảng cách Euclid từ tâm camera là gì? Làm tròn khoảng cách 3 chữ số thập phân.',
 '(2;0;10) m; khoảng cách 10,198 m','(2;0;10) m; khoảng cách 10,000 m','(0,2;0;10) m; khoảng cách 10,002 m',
 'Back-projection: X=(400−320)×10/400=2 m; Y=(240−240)×10/400=0; Z=10. Khoảng cách tâm=sqrt(2²+0²+10²)=sqrt(104)≈10,198 m. Depth dọc Z khác range Euclid khi điểm nằm ngoài trục quang.',calc=True,
 formula=('Đổi hệ tọa độ, chiếu và back-projection','x_camera=R×x_lidar+t; u=f_x×X/Z+c_x; v=f_y×Y/Z+c_y; X=(u−c_x)×Z/f_x; Y=(v−c_y)×Z/f_y; x_camera=Z×K⁻¹×[u;v;1]',
 'R,t: extrinsic LiDAR sang camera; K: intrinsic; X,Y,Z: tọa độ camera; u,v: pixel; Z: depth theo trục quang.','Pinhole không distortion hoặc ảnh đã undistort; Z>0; nguồn đã căn thời gian. Back-projection cần depth, pixel đơn lẻ không xác định duy nhất điểm 3D.','u=400,v=240,Z=10,fx=fy=400,cx=320,cy=240 →(X,Y,Z)=(2;0;10), range≈10,198 m.','Dùng sai chiều extrinsic; bỏ t; chia cho Z của hệ LiDAR; nhầm depth Z với range Euclid.'))
mc('p2-t4-d08','d-nds-saturation',[7,12],
 'Trong NDS=[5×mAP+Σ(1−min(1,e_i))]/10, mAP và bốn error khác giữ nguyên. Error còn lại giảm từ 1,4 xuống 1,1, rồi xuống 0,8. NDS tăng bao nhiêu ở từng lần?',
 'Lần 1 tăng 0; lần 2 tăng 0,02','Lần 1 tăng 0,03; lần 2 tăng 0,03','Lần 1 tăng 0; lần 2 tăng 0,2',
 'Error 1,4 và 1,1 đều bị min(1,e) chặn thành 1, nên đóng góp đều 0. Khi error=0,8, đóng góp thành 0,2. Chia cho 10 làm NDS tăng 0,02. Đây là error đã quy về đúng thang công thức, không cộng trực tiếp các đơn vị chưa chuẩn hóa.',calc=True,
 formula=('Depth mặt đường phẳng và NDS','Z=f×h/delta_v; NDS=[5×mAP+Σ(1−min(1,e_i))]/10',
 'h: độ cao camera; f: focal pixel; delta_v: độ lệch chân vật so với đường chân trời; e_i: năm TP errors theo định nghĩa NDS.','Depth giả định camera/mặt phẳng đường và đường chân trời đã biết, chân vật nằm trên đường; delta_v>0. NDS dùng đúng giao thức nuScenes, không tự gộp các error khác đơn vị ngoài quy ước.','f=800,h=1,5,delta_v=40 →Z=30 m. Một error giảm 1,1→0,8 làm NDS tăng (0,2−0)/10=0,02.','Áp mặt đường phẳng trên dốc mà không hiệu chỉnh; gần chân trời sai số pixel rất nhạy; quên chặn error ở 1 hoặc quên chia 10.'))
mc('p2-t4-d09','d-batch-drop',[24,54],
 'Video có 101 frame index 0…100. Chọn frame 0 rồi mỗi frame thứ 10. Batch size=4. So sánh giữ batch cuối thiếu với drop_last=true: mỗi cách chạy bao nhiêu batch và xử lý bao nhiêu frame?',
 'Giữ: 3 batch,11 frame; bỏ: 2 batch,8 frame','Giữ: 3 batch,12 frame; bỏ: 2 batch,8 frame','Giữ: 2 batch,8 frame; bỏ: 2 batch,8 frame',
 'Danh sách 0,10,…,100 gồm floor(100/10)+1=11 frame. Giữ batch thiếu: ceil(11/4)=3 batch, vẫn chỉ 11 frame thật. Drop_last: floor(11/4)=2 batch, xử lý 2×4=8 và bỏ 3 frame; không tự đệm thành 12 frame.',calc=True,
 formula=('Frame sampling, batch và công gán nhãn','N_frames=FPS×seconds; N_selected=floor((N_frames−1)/step)+1; batches_keep=ceil(N_selected/B); batches_drop=floor(N_selected/B); time=Σ(count_i×time_i); saving=100×(time_old−time_new)/time_old',
 'step: bước chỉ số; B: batch size; count_i: số nhãn thực sự audit/review/vẽ lại; time_i: thời gian một thao tác.','Video FPS cố định và N_frames nguyên đã biết, bắt đầu index0, không vượt N_frames−1. Nếu count audit theo tỷ lệ cần nêu làm tròn. Thời gian cộng theo giả định không overhead/song song.','101 frame,step10 →11 chọn; B4 giữ3 batch hoặc drop2 batch. 100 nhãn×30s so với 1.500s mới →tiết kiệm50%.','Nhầm số khoảng với số frame; tính frame đệm là dữ liệu thật; áp FPS cố định cho video VFR; quên chỉ audit một phần nhãn confidence cao.'))
mc('p2-t4-d10','d-box-scale-mismatch',[14,16],
 'Một box xyxy thực tế đã ở đơn vị pixel: (100,50,300,150) trên ảnh 2000×1000. Parser hiểu nhầm là thang 0–1000 và áp x_px=x_norm×W/1000,y_px=y_norm×H/1000. Diện tích sau parse sai gấp mấy lần diện tích đúng?',
 '2 lần','4 lần','1 lần',
 'Box đúng rộng 200,cao100 nên diện tích20.000 pixel². Parser sai nhân x với2000/1000=2,y với1000/1000=1: rộng400,cao100,diện tích40.000. Tỷ số2. Parser phải dựa đúng schema tọa độ của model, không đoán mọi box đều chuẩn hóa.',calc=True,
 formula=('Box chuẩn hóa và bộ nhớ weights MoE','x_pixel=x_norm×W/S; y_pixel=y_norm×H/S; area=(x2−x1)×(y2−y1); weight_bytes=N_total_parameters×bytes_per_weight; bytes_per_GPU=weight_bytes/number_of_shards',
 'S: thang chuẩn hóa, ví dụ1000; N_total_parameters: tổng weights resident; active_parameters: phần tham số được dùng cho token.','Box xyxy liên tục, không +1; không scale lại tọa độ đã ở pixel. Bộ nhớ weights giả định shard đều,bỏ activations/KV cache/overhead; MoE compute theo active nhưng resident weights theo tổng nếu nạp toàn bộ.','Ảnh2000×1000 mà scale nhầm box pixel theo S1000 →diện tích nhân2. MoE24 tỉ weights×2byte=48GB, shard4→12GB/GPU.','Tráo W/H; dùng thang0–1 cho box0–1000; chỉ đếm active weights khi tất cả experts phải resident; coi weights là toàn bộ VRAM.'))
save('d-geometry')
