from priority_author_common import *
mc('p2-t4-d03','d-giou-disjoint',[13,14,45],
 'Hai box xyxy A=(0,0,2,2), B=(3,0,5,2), tọa độ liên tục không cộng 1. C là box nhỏ nhất bao cả hai. Với GIoU=IoU−(|C|−|A∪B|)/|C|, GIoU bằng bao nhiêu?',
 '−0,2','0','0,2',
 'Hai box không giao: intersection=0. Mỗi box diện tích 4 nên union=8. C rộng 5,cao 2 nên diện tích 10. IoU=0/8=0; GIoU=0−(10−8)/10=−0,2. GIoU có thể âm, không phải xác suất.',calc=True,
 formula=('Box overlap, Precision/Recall/F1 và letterbox','IoU=intersection/union; GIoU=IoU−(area_C−union)/area_C; P=TP/(TP+FP); R=TP/(TP+FN); F1=2×P×R/(P+R); x_original=(x_letterbox−pad_x)/scale; y_original=(y_letterbox−pad_y)/scale',
 'C: box bao nhỏ nhất; TP/FP/FN: đếm theo giao thức matching; pad_x,pad_y: padding trái/trên.','Box xyxy liên tục: diện tích=(x2−x1)×(y2−y1), không +1. Mẫu số phải khác 0; nêu quy ước metric nếu tập rỗng. Letterbox có cùng scale hai chiều.','A=(0,0,2,2),B=(3,0,5,2): union=8,C=10 → GIoU=−0,2.','Ép GIoU về [0,1]; chia scale trước khi trừ padding; dùng ngưỡng confidence khác nhau rồi so P/R như cùng giao thức.'))
mc('p2-t4-d03','d-ap-unreached',[43,44],
 'Precision envelope bằng 0,8 tại mọi mức recall từ 0 đến 0,50; recall lớn hơn 0,50 không đạt được nên precision bằng 0. AP dùng đúng 101 điểm 0;0,01;…;1. AP là bao nhiêu, làm tròn 4 chữ số thập phân?',
 '0,4040','0,8000','0,4000',
 'Các điểm 0;0,01;…;0,50 gồm 51 điểm, không phải 50. Tổng precision=51×0,8=40,8. Chia đủ 101 mức cho AP=40,8/101≈0,4040. Không chỉ lấy trung bình các mức recall đã đạt.',calc=True,
 formula=('AP nội suy 101 điểm và mAP','p_interp(r)=max precision(r′) với r′≥r; AP=(1/101)×Σ p_interp(r), r∈{0;0,01;…;1}; mAP=trung bình AP theo class và các ngưỡng đã quy định',
 'r: recall; precision envelope lấy giá trị lớn nhất ở bên phải; class/ngưỡng là các trục lấy trung bình.','Đây là quy ước 101 mức; recall không đạt cho precision 0. COCO box AP trung bình các ngưỡng IoU 0,50:0,05:0,95; không tráo với tích phân PR hoặc AP50.','Envelope 0,8 đến recall0,50 và 0 sau đó → AP=51×0,8/101≈0,4040.','Nhầm 101 điểm với 100 khoảng; chỉ tính vùng recall đạt được; gọi một ngưỡng IoU là AP@[.5:.95].'))
mc('p2-t4-d03','d-seg-aggregate',[54],
 'Một lớp foreground có (TP,FP,FN) ở ảnh A=(1,0,0), ảnh B=(9,10,0). IoU dataset được tính sau khi cộng các đếm; khác trung bình IoU từng ảnh. IoU dataset và trung bình từng ảnh là bao nhiêu, làm tròn 4 chữ số thập phân?',
 '0,5000 và 0,7368','0,7368 và 0,5000','0,5000 và 0,5000',
 'Cộng đếm: TP=10,FP=10,FN=0 → IoU dataset=10/20=0,5. IoU ảnh A=1, ảnh B=9/19≈0,4737; trung bình=(1+9/19)/2≈0,7368. Ảnh nhỏ được trọng số ngang ảnh lớn trong cách trung bình từng ảnh.',calc=True,
 formula=('Dice và mIoU segmentation','IoU_c=TP_c/(TP_c+FP_c+FN_c); mIoU=(1/C)×Σ IoU_c; Dice=2×TP/(2×TP+FP+FN); Dice_loss=1−Dice',
 'C: số lớp được chấm; TP,FP,FN cộng trên toàn dataset theo từng lớp.','Mask nhị phân rời rạc, không smoothing trong công thức này. Quy định cách xử lý lớp vắng/tập rỗng; không thay dataset IoU bằng trung bình IoU từng ảnh.','TP=10,FP=10,FN=0 → IoU=0,5; Dice=20/30≈0,6667.','Nhầm Dice với IoU; dùng pixel accuracy thay mIoU; trộn macro-average theo lớp với average theo ảnh.'))
mc('p2-t4-d03','d-pose-boundary',[74,75],
 'Bốn keypoint đều được chấm có sai số pixel (2;5;6;10), kích thước tham chiếu h=10 pixel. PCK quy định đúng khi d/h<0,5 (bất đẳng thức nghiêm). PCK bằng bao nhiêu?',
 '25%','50%','75%',
 'Ngưỡng pixel=0,5×10=5. Chỉ d=2 thỏa d<5; d=5 nằm trên biên nên không đúng theo quy ước đề. PCK=1/4=25%. Nếu dùng ≤ sẽ ra 50%, là giao thức khác.',calc=True,
 formula=('OKS và PCK cho keypoints','OKS=Σ[exp(−d_i²/(2×s²×k_i²))×I(v_i>0)]/ΣI(v_i>0); k_i=2×sigma_i; PCK=100×số điểm có d/h<alpha / số điểm được chấm',
 'd_i: sai số pixel; s²: diện tích object; k_i: tolerance từng keypoint; v_i: trạng thái được gán nhãn; h: chiều dài tham chiếu PCK.','Chỉ chấm keypoint hợp lệ; mẫu số >0. PCK phải nêu h và dấu < hay ≤. OKS-AP còn bao gồm detection/matching, không bằng PCK.','d=(2;5;6;10),h=10,alpha=0,5 và dấu < → PCK=25%. Một điểm d=0 hợp lệ có thành phần OKS=1.','Dùng diện tích s² như chiều dài s; nhầm k với sigma; tính điểm không được chấm vào mẫu số; đổi quy tắc biên.'))
mc('p2-t4-d07','d-tracking-gate',[18,20,37,38,39],
 'Innovation r=(3;2), covariance S=diag(9;1). Gating dùng d²=rᵀ×S⁻¹×r, chấp nhận d²≤4. Điểm này được ghép tiếp hay bị loại?',
 'd²=5 nên bị loại','d²=13 nên được ghép tiếp','d²=1 nên được ghép tiếp',
 'S⁻¹=diag(1/9;1). d²=3²/9+2²/1=1+4=5. Vì 5>4 nên cặp bị loại trước association. Đây là ngưỡng giả định của đề; không dùng khoảng cách Euclid bình phương=13.',calc=True,
 formula=('Assignment, Mahalanobis và metrics tracking','assignment: tối thiểu Σ cost(track,detection) với ràng buộc một–một; d²=rᵀ×S⁻¹×r; MOTA=1−(FN+FP+IDSW)/GT; IDF1=2×IDTP/(2×IDTP+IDFP+IDFN); HOTA_alpha=sqrt(DetA_alpha×AssA_alpha)',
 'S: covariance innovation; IDSW: đổi ID; IDTP/IDFP/IDFN: đếm sau identity matching toàn cục; alpha: ngưỡng localization.','Gating threshold phải phù hợp số chiều và policy. HOTA toàn bộ là trung bình HOTA_alpha qua các ngưỡng quy định; AssA lấy từ giao thức matching, không tự suy từ số ID switch.','r=(3;2),S=diag(9;1) → d²=5. DetA=0,8,AssA=0,45 → HOTA tại một ngưỡng=0,6.','Chọn greedy từng hàng thay assignment toàn cục; nhầm d với d²; ép MOTA không âm; lấy trung bình cộng DetA/AssA.'))
save('d-metrics')
