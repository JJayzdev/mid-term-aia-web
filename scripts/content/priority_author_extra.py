from priority_author_common import *
def sup(item,title,url,note):item['supplemental_sources']=[dict(title=title,url=url,accessed_at='2026-10-28',note=note)]
g=match('p2-t4-d01','activation-graphs',[15],'Ghép một-một mỗi đồ thị với hàm kích hoạt tương ứng. Mô tả hình dạng cũng được cung cấp để đọc không cần hình.',[
 ('Đồ thị I: đường cong chữ S, qua (0;0,5), tiệm cận 0 và 1','Sigmoid','Sigmoid có giá trị 0,5 tại x=0 và nằm trong (0,1).'),
 ('Đồ thị II: đường cong chữ S qua gốc tọa độ, tiệm cận −1 và 1','Tanh','Tanh là hàm lẻ, bằng 0 tại gốc và bị chặn giữa −1 và 1.'),
 ('Đồ thị III: bằng 0 khi x âm, là đường y=x khi x dương','ReLU','ReLU cắt phần âm về 0 và giữ nguyên phần dương.')],
 'Đồ thị I và II đều bão hòa nhưng khác miền đầu ra và giá trị tại gốc. Đồ thị III có góc gãy tại 0; đoạn dương không bão hòa.',focus='activations')
for item,kind in zip(g['matching_items'],['sigmoid','tanh','relu']):item['graph']=kind
q=mc('p2-t4-d02','norm-ln-eval',[17,34],'LayerNorm trên chiều D của từng token có gamma,beta cố định. Cùng một token đầu vào, chỉ thay các token khác trong batch và chuyển train sang eval. Bỏ mọi lớp khác. Đầu ra của token này thế nào?',
 'Không đổi: vẫn dùng thống kê D phần tử của chính token đó','Đổi vì eval dùng running statistics tích lũy từ batch trước','Đổi vì luôn gộp tất cả token trong batch để tính mean',
 'LayerNorm với normalized_shape=D tính thống kê từ D phần tử hiện tại của từng token ở cả train và eval. Gamma,beta và token đang xét không đổi nên kết quả không đổi; running statistics là cách hoạt động thông thường của BatchNorm, không phải LayerNorm.',focus='normalization',context='So sánh riêng lớp LayerNorm, không có dropout hoặc cập nhật tham số.')
sup(q,'PyTorch LayerNorm','https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html','Bổ sung ngoài slide: thống kê đầu vào hiện tại được dùng trong cả training và evaluation; normalized_shape xác định các chiều cuối.')
q=mc('p2-t4-d05','kalman-control',[28],'Trạng thái x=(vị trí;vận tốc)=(2 m;3 m/s), bước thời gian 1 s. Dùng F=[[1,1],[0,1]], B=(0,5;1), điều khiển gia tốc u=2 m/s². Với x_pred=F×x+B×u, prediction là gì?',
 '(6 m;5 m/s)','(5 m;3 m/s)','(7 m;5 m/s)',
 'F×x=(2+3;3)=(5;3). B×u=(1;2). Cộng hai vector được (6;5). Bỏ B×u là bỏ điều khiển; cộng trực tiếp u vào cả hai trạng thái sai vì B biểu diễn tác động theo đơn vị của từng thành phần.',focus='kalman',calc=True,
 formula=('Kalman tuyến tính có điều khiển','x_pred=F×x+B×u; P_pred=F×P×Fᵀ+Q; S=H×P_pred×Hᵀ+R; K=P_pred×Hᵀ×S⁻¹; x_new=x_pred+K×(z−H×x_pred)','F: chuyển trạng thái; B: ánh xạ điều khiển u; H: ánh xạ đo; P,Q,R: covariance; S: covariance innovation.','Mô hình tuyến tính; nhiễu quá trình và đo độc lập, S khả nghịch. B×u là điều khiển biết trước; nếu điều khiển có nhiễu phải mô hình hóa covariance phù hợp.','F×(2;3)=(5;3), B×2=(1;2) → x_pred=(6;5).','Bỏ điều khiển; cộng u vào mọi thành phần; đảo thứ tự nhân ma trận; lấy nghịch đảo từng phần tử.'))
sup(q,'FilterPy KalmanFilter','https://filterpy.readthedocs.io/en/latest/kalman/KalmanFilter.html','Bổ sung ngoài slide: control transition matrix B và predict có B×u; slide p28 là neo chương trình cho hệ phương trình Kalman ma trận.')
save('extra')
