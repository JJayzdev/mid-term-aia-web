from priority_author_common import *
mc('p2-t4-d01','d-forward-gradient',[12,35,40,51,52,55],
 'Neuron hồi quy có y_hat=w×x+b, x=2,w=1,b=0, nhãn t=1. Loss L=(y_hat−t)²/2. Cập nhật đồng thời w,b bằng SGD với eta=0,1. Bộ (w_new,b_new) là gì?',
 '(0,8;−0,1)','(0,6;−0,2)','(0,8;−0,06)',
 'Forward: y_hat=1×2+0=2, sai số r=1. Vì có hệ số 1/2, dL/dy_hat=r=1. Chain rule: dL/dw=1×2=2, dL/db=1. SGD từ cùng trạng thái cũ: w_new=1−0,1×2=0,8; b_new=0−0,1×1=−0,1. Không tính lại gradient b từ w đã cập nhật.',calc=True,
 formula=('Forward, tham số, loss và gradient','z=W×x+b; số tham số dense=m×n+m; MSE=Σ(y_hat−t)²/N; BCE=−[t×ln(p)+(1−t)×ln(1−p)]; CE=−ln(p_lớp_đúng); w_new=w−eta×dL/dw',
 'W có m hàng,n cột; b có m phần tử; N là số phần tử lấy trung bình; t là nhãn; p là xác suất.','MSE ghi ở đây không có 1/2; nếu loss dùng 1/2 thì gradient giảm nửa. BCE nhãn nhị phân; CE một nhãn. Log tự nhiên; backprop nhân các đạo hàm theo chain rule.','x=2,w=1,b=0,t=1,L=(y_hat−t)²/2: dL/dw=2,dL/db=1; eta=0,1 cho (0,8;−0,1).','Nhầm tổng với trung bình; bỏ bias khi đếm tham số; nhầm hệ số 1/2; cập nhật tuần tự rồi tính lại gradient.'))
mc('p2-t4-d01','d-robust-loss',[58,60,63],
 'Hai residual là r=0,5 và r=2. Dùng smooth-L1(r)=r²/2 khi |r|<1, còn lại |r|−0,5. Nếu residual lớn tăng từ 2 lên 3, tổng loss tăng bao nhiêu?',
 '1','2,5','0,5',
 'Loss ban đầu=0,5²/2+(2−0,5)=0,125+1,5=1,625. Loss mới=0,125+(3−0,5)=2,625. Chênh lệch=1. Nhánh xa 0 tăng tuyến tính, không tăng như L2.',calc=True,
 formula=('Smooth-L1, focal loss và phạt L2','SmoothL1(r)=r²/2 nếu |r|<1, ngược lại |r|−1/2; FL(p)=−(1−p)^gamma×ln(p); J_reg=J+(lambda/2)×Σw_i²; dJ_reg/dw=dJ/dw+lambda×w',
 'r: sai số; p: xác suất lớp đúng; gamma: độ tập trung focal; lambda: hệ số phạt weights.','Smooth-L1 ở đây có ngưỡng beta=1. Focal không thêm trọng số alpha; gamma=0 cho CE. Phạt L2 có hệ số 1/2; không đồng nhất mọi dạng L2 với AdamW.','r=(0,5;2) cho tổng smooth-L1=1,625. p=0,9,gamma=2 cho FL≈0,001054. w=(3;4),lambda=0,2 cho penalty=2,5.','Dùng bình phương cho residual lớn; lấy p của lớp sai; bỏ hệ số 1/2; coi focal là phép lấy mẫu dữ liệu.'))
mc('p2-t4-d01','d-clipped-momentum',[71,73,74,79],
 'Gradient g=(6;8), clip theo L2-norm với ngưỡng c=5 trước momentum. Buffer cũ b=(1;−1), mu=0,9; dùng b_new=mu×b+g_clip. Buffer mới là gì?',
 '(3,9;3,1)','(6,9;7,1)','(5,9;4,1)',
 'Norm g=sqrt(36+64)=10, hệ số clip=min(1,5/10)=0,5 nên g_clip=(3;4). Buffer mới=(0,9;−0,9)+(3;4)=(3,9;3,1). Cắt từng tọa độ về 5 không phải norm clipping.',calc=True,
 formula=('Momentum, Adam/AdamW và norm clipping','g_clip=g×min(1,c/||g||); b_t=mu×b_prev+g_clip; w_new=w−eta×b_t; m_t=beta1×m_prev+(1−beta1)×g; v_t=beta2×v_prev+(1−beta2)×g²; Adam: w_new=w−eta×m_hat/(sqrt(v_hat)+epsilon); AdamW: w_new=w−eta×lambda×w−eta×m_hat/(sqrt(v_hat)+epsilon)',
 'b: buffer momentum; m,v: moments; m_hat,v_hat: moments đã hiệu chỉnh độ chệch; c: ngưỡng norm; eta: learning rate; lambda: decay.','Adam dùng phép toán từng phần tử; epsilon ở ngoài căn. Đề phải quy định clip trước hay sau tích lũy; AdamW tách decay khỏi moments. Gradient bằng 0 được giữ nguyên khi clip.','g=(6;8),c=5 → g_clip=(3;4); b_prev=(1;−1),mu=0,9 → b_new=(3,9;3,1).','Nhầm norm clipping với cắt từng tọa độ; bỏ hiệu chỉnh độ chệch; đưa decay AdamW vào moments; coi clipping chữa gradient nhỏ.'))
mc('p2-t4-d02','d-cnn-receptive',[7,9,13],
 'Chuỗi hai convolution không dilation: lớp 1 kernel=3,stride=2; lớp 2 kernel=3,stride=1. Với r0=j0=1, r_new=r_old+(k−1)×j_old và j_new=j_old×s, receptive field và bước nhảy sau lớp 2 là gì?',
 'r=7 pixel; j=2 pixel','r=5 pixel; j=2 pixel','r=7 pixel; j=1 pixel',
 'Lớp 1: r1=1+2×1=3,j1=1×2=2. Lớp 2: r2=3+2×2=7,j2=2×1=2. Phải dùng bước nhảy tích lũy trước lớp hiện tại; cộng mỗi kernel thêm 2 sẽ sai.',calc=True,
 formula=('CNN: kích thước, tham số, MAC và receptive field','H_out=floor((H_in+2p−d×(k−1)−1)/s)+1; parameters=C_out×(C_in×k²+1); MAC=H_out×W_out×C_out×C_in×k²; r_new=r_old+(k−1)×j_old; j_new=j_old×s',
 'p: padding mỗi phía; d: dilation; s: stride; k: kernel vuông; C: kênh; r: receptive field; j: bước trên ảnh gốc.','Conv thường groups=1, bias có tính trong parameters, MAC bỏ bias. Công thức receptive field ghi ở đây cho d=1; r0=j0=1. Tính W_out tương tự H_out.','Hai lớp k=3, strides=(2;1): (r1,j1)=(3;2), (r2,j2)=(7;2).','Làm tròn output lên; quên dilation; đếm parameters theo kích thước ảnh; dùng j_new thay j_old khi cập nhật r.'))
mc('p2-t4-d02','d-rnn-shared',[15,21,25],
 'RNN có input dimension d=3, hidden dimension h=4, một bias hidden, chưa tính output head. Số tham số hidden là h×(h+d)+h. Khi tăng độ dài chuỗi từ 10 lên 20, số tham số này đổi thế nào?',
 'Vẫn 32','Tăng từ 32 lên 64','Tăng từ 320 lên 640',
 'Hidden weights có h×h+h×d=16+12=28 phần tử, bias có 4, tổng 32. Các bước thời gian dùng chung weights, nên tăng chiều dài chuỗi không tạo thêm tham số; chi phí chạy có thể tăng.',calc=True,
 formula=('Residual, RNN và LSTM','Residual: H(x)=x+F(x); RNN: h_t=tanh(W_hh×h_prev+W_xh×x_t+b); parameters=h×(h+d)+h; LSTM: c_t=f_t×c_prev+i_t×c_tilde; h_t=o_t×tanh(c_t)',
 'h,d: kích thước hidden/input; f,i,o: cổng forget/input/output; c: ô nhớ; phép × giữa các cổng là nhân từng phần tử.','Residual cộng hai tensor tương thích; nếu khác kích thước cần projection. Đếm RNN ở đây dùng một bias, không output head; framework có thể dùng hai bias.','d=3,h=4 → 32 tham số hidden bất kể 10 hay 20 bước; LSTM c_prev=2,f=0,5,i=0,c_tilde bất kỳ → c_t=1.','Nhân số weights với độ dài chuỗi; nhầm hidden state với cell state; coi residual là ghép nối tensor.'))
mc('p2-t4-d02','d-attention-memory',[31,32,36,37],
 'Ảnh 256×256 chia patch 16×16, thêm một CLS token. Một head lưu ma trận attention đầy đủ N×N bằng float32 (4 byte/phần tử). Bỏ mọi bộ nhớ khác. Cần bao nhiêu byte?',
 '264.196 byte','262.144 byte','1.028 byte',
 'Số patch=(256/16)²=256; thêm CLS cho N=257. Ma trận có 257²=66.049 phần tử. Nhân 4 byte cho 264.196 byte. Quên CLS cho 262.144; chỉ nhân N×4 bỏ kích thước thứ hai.',calc=True,
 formula=('Attention, patch và bộ nhớ ma trận điểm','Attention(Q,K,V)=softmax(Q×Kᵀ/sqrt(d_k))×V; N_patch=(H/P)×(W/P); N=N_patch+N_extra; entries=N²; bytes=heads×N²×bytes_per_element; chi phí attention O(N²×D)',
 'P: cạnh patch; d_k: chiều key mỗi head; D: chiều embedding; N_extra: token đặc biệt như CLS.','H,W chia hết cho P; patch không chồng lấn. Công thức bộ nhớ chỉ cho ma trận attention được vật hóa, không toàn bộ model; kernel tiết kiệm bộ nhớ có thể không lưu toàn ma trận.','256×256,patch16,1 CLS → N=257; 1 head,float32 → 264.196 byte.','Quên token đặc biệt; nhầm byte/bit; dùng sqrt(N) thay sqrt(d_k); suy chi phí tổng model chỉ từ O(N²D).'))
save('d-neural')
