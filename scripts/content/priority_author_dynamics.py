"""Source-grounded gap questions; independent review required before release."""
from priority_author_common import *

mc('p2-t4-d11','dynamics-offset',[46],
 'Ba vị trí một chiều đo cách đều 0,1 s là 0 m; 1,01 m; 2,04 m. Dùng a=(x_next−2x_now+x_prev)/(Δt)². Gia tốc tại mẫu giữa bằng bao nhiêu, và có đổi nếu cộng cùng sai lệch hiệu chuẩn +0,5 m vào cả ba vị trí không?',
 '2 m/s²; không đổi','2 m/s²; tăng thêm 50 m/s²','0,2 m/s²; không đổi',
 'Tử số 2,04−2×1,01+0=0,02 m; chia 0,01 s² được 2 m/s². Offset chung triệt tiêu vì 1−2+1=0. Điều này khác nhiễu độc lập từng mẫu: phương sai của tổ hợp là (1²+2²+1²)×sigma_x².',calc=True,
 formula=('Sai phân gia tốc và khuếch đại nhiễu',
 'a=(x_next−2x_now+x_prev)/(Δt)²; Var(a_noise)=6×sigma_x²/(Δt)^4; sigma_a=sqrt(6)×sigma_x/(Δt)²',
 'x: vị trí (m); Δt: bước thời gian (s); sigma_x: độ lệch chuẩn nhiễu vị trí; sigma_a: độ lệch chuẩn nhiễu gia tốc (m/s²).',
 'Các mẫu cách đều. Công thức phương sai cần nhiễu độc lập, cùng phương sai; không áp trực tiếp cho nhiễu tương quan. Làm mượt phải cân nhắc độ trễ và sai lệch.',
 'x=(0;1,01;2,04) m, Δt=0,1 s → a=2 m/s². Nếu sigma_x=0,01 m và nhiễu độc lập thì sigma_a≈2,449 m/s².',
 'Chia Δt thay vì (Δt)²; nhầm phương sai với độ lệch chuẩn; coi offset chung là nhiễu độc lập.'))

mc('p2-t4-d11','dynamics-gates',[49],
 'Sau làm mượt, gia tốc tăng từ 1,0 lên 2,2 m/s² trong 0,2 s. Một đoạn cua có v=10 m/s và độ cong κ=0,03 m⁻¹. Cổng chấp nhận |j|≤5 m/s³, κ≤0,04 m⁻¹, |a_lat|≤2,5 m/s², với j≈Δa/Δt và a_lat=v²κ. Những cổng nào bị vi phạm?',
 'Jerk và gia tốc ngang; độ cong đạt','Chỉ độ cong; hai cổng còn lại đạt','Chỉ jerk; độ cong và gia tốc ngang đạt',
 'j=(2,2−1,0)/0,2=6 m/s³ >5. Độ cong 0,03≤0,04 nên đạt riêng cổng độ cong, nhưng a_lat=10²×0,03=3 m/s² >2,5. Đạt giới hạn hình học không đồng nghĩa đi qua cua được ở mọi tốc độ.',calc=True,
 formula=('Jerk, độ cong và gia tốc ngang',
 'j=da/dt≈Δa/Δt; |κ|≤κ_max; |a_lat|=v²|κ|; v_max=sqrt(a_limit/|κ|)',
 'j: jerk (m/s³); κ: độ cong (m⁻¹); v: tốc độ (m/s); a_limit: giới hạn gia tốc ngang dương (m/s²).',
 'Quỹ đạo phẳng trơn, κ≠0 khi tính v_max; dùng độ lớn cho cổng hai chiều. Ngưỡng là giả định của bài, không thay cho mô hình đầy đủ của xe.',
 'v=10 m/s, κ=0,03 m⁻¹ → a_lat=3 m/s². Với a_limit=2,5 m/s², v_max≈9,129 m/s; j=1,2/0,2=6 m/s³.',
 'Nhầm jerk với gia tốc; bỏ bình phương tốc độ; coi cổng độ cong đạt là mọi cổng động học đều đạt.'))

mc('p2-t4-d11','scaling-floor',[71],
 'Mô hình pilot giả định err(D)=4D^(−0,5)+0,10 với D là số giờ dữ liệu dương. Cần bao nhiêu giờ để err≤0,30? Có D hữu hạn nào đạt err≤0,10 theo chính mô hình này không?',
 'Ít nhất 400 giờ; không có D hữu hạn','Ít nhất 400 giờ; 1.600 giờ đạt err≤0,10','Ít nhất 200 giờ; không có D hữu hạn',
 '4/sqrt(D)≤0,20 nên sqrt(D)≥20 và D≥400. Với mọi D hữu hạn dương, 4/sqrt(D)>0 nên err>0,10. Sàn 0,10 là giới hạn của mô hình giả định, không phải một mục tiêu đạt bằng cách thêm hữu hạn dữ liệu.',calc=True,
 formula=('Scaling dữ liệu có sàn lỗi',
 'err(D)=a×D^(−alpha)+c; D_target=(a/(epsilon−c))^(1/alpha); (err(2D)−c)/(err(D)−c)=2^(−alpha)',
 'D: lượng dữ liệu; a>0: hệ số; alpha>0: số mũ; c: sàn lỗi; epsilon: lỗi mục tiêu.',
 'Cần epsilon>c để tính lượng dữ liệu hữu hạn. Tham số phải được ước lượng từ pilot phù hợp; không tự ngoại suy qua thay đổi phân phối.',
 'a=4, alpha=0,5, c=0,10, epsilon=0,30 → D_target=(4/0,20)²=400 giờ. Nhân đôi D chỉ nhân phần lỗi trên sàn với 1/sqrt(2)≈0,7071.',
 'Bỏ sàn c; nghĩ nhân đôi dữ liệu chia đôi toàn bộ lỗi; thay epsilon≤c vào công thức như một nghiệm hữu hạn.'))

item=mc('p2-t4-d11','importance-weight',[89],
 'Lấy 4 kịch bản độc lập từ phân phối đề xuất q. Chỉ báo lỗi là (1;0;1;0), trọng số p(x)/q(x) tương ứng (0,1;1,9;0,1;1,9). Dùng ước lượng IS thường r_hat=(1/n)Σ w_i I_i. Ước lượng tỷ lệ lỗi của phân phối mục tiêu p là bao nhiêu?',
 '0,05 (5%)','0,50 (50%)','0,10 (10%)',
 'Tổng đóng góp có trọng số là 0,1+0+0,1+0=0,2; chia cho n=4 được 0,05. Đếm 2/4 chỉ mô tả mẫu đã được làm giàu theo q.',calc=True,
 formula=('Importance sampling: hiệu chỉnh phân phối lấy mẫu',
 'w_i=p(x_i)/q(x_i); r_hat=(1/n)×Σ_i(w_i×I_i)',
 'p: phân phối mục tiêu; q: phân phối lấy mẫu; I_i: chỉ báo lỗi 0/1; n: số mẫu.',
 'Mẫu độc lập từ q; biết tỷ số p/q; q dương trên vùng lỗi có xác suất dưới p. Đây là IS thường với mật độ chuẩn hóa.',
 'I=(1;0;1;0), w=(0,1;1,9;0,1;1,9) → r_hat=0,2/4=0,05.',
 'Dùng tỷ lệ lỗi thô dưới q; đảo p/q; bỏ vùng lỗi khỏi support của q.'))
item['supplemental_sources']=[dict(title='Owen, Maximov & Chertkov — Importance sampling, Eq. (4)',url='https://arxiv.org/html/1710.06965',accessed_at='2026-10-28',note='Bổ sung ngoài slide: estimator dùng tỷ số mật độ và chỉ báo sự kiện; D11 chỉ nêu IS trong mục tiêu lab. Bài tập dùng dạng IS thường.')]

item=mc('p2-t4-d12','zero-events-bound',[38],
 'Không có lỗi trong 3.000 lượt thử Bernoulli độc lập, cùng xác suất lỗi của phân phối mục tiêu đã xác định. Theo quy tắc 3/n, cận trên một phía xấp xỉ 95% là bao nhiêu, và có thể thay n bằng 3.000 frame tương quan của một lượt chạy không?',
 'Khoảng 0,1%; không thể thay như vậy','Bằng 0%; có thể thay vì mọi frame đều không lỗi','Khoảng 1%; không thể thay như vậy',
 '3/3000=0,001=0,1%. Đây là cận trên xấp xỉ, không phải xác suất lỗi bằng 0. Frame tương quan không phải 3.000 phép thử độc lập.',calc=True,
 formula=('Không quan sát lỗi: điều kiện của quy tắc 3/n',
 '(1−p_upper)^n=0,05; p_upper=1−0,05^(1/n)≈3/n',
 'n: số phép thử; p_upper: cận trên một phía 95% của xác suất lỗi.',
 'Không quan sát lỗi; phép thử Bernoulli độc lập, cùng xác suất, đại diện đúng phân phối cần suy luận. 3/n là xấp xỉ cho n đủ lớn; không dùng n frame tương quan hoặc mẫu IS như n phép thử này.',
 'n=3000 → 3/n=0,001=0,1%; nghiệm chính xác≈0,0009981.',
 'Kết luận rủi ro bằng 0; nhầm 0,001 với 1%; mở rộng kết luận sang phân phối khác.'))
item['supplemental_sources']=[dict(title='Hanley & Lippman-Hand (1983) — Interpreting Zero Numerators',url='https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf',accessed_at='2026-10-28',note='Bổ sung ngoài slide: PDF trang 2 dẫn xuất cận 95% và xấp xỉ 3/n; D12 trang 38 là nền về quy mô bằng chứng an toàn.')]

mc('p2-t4-d12','ttc-comparison',[43,44],
 'Hai ca tiến gần thẳng có (d,v_close): A=(10 m,5 m/s), B=(20 m,10 m/s). Dùng TTC=d/v_close và độ lớn giảm tốc tương đối đều cần thiết b=v_close²/(2d), bỏ qua độ trễ. Kết luận nào đúng?',
 'Cùng TTC=2 s; B cần giảm tốc gấp đôi A','Cùng TTC=2 s nên cùng mức giảm tốc cần thiết','TTC của B gấp đôi A; giảm tốc cần thiết bằng nhau',
 'TTC_A=10/5=2 s và TTC_B=20/10=2 s. Nhưng b_A=25/20=1,25 m/s², b_B=100/40=2,5 m/s². Cùng TTC không quyết định cùng nhu cầu phanh; hai độ đo trả lời hai câu khác nhau.',calc=True,focus='closed-loop',
 formula=('TTC và giảm tốc tương đối cần thiết',
 'TTC=d/v_close; b_req=v_close²/(2d)',
 'd>0: khoảng cách (m); v_close>0: tốc độ tiến gần (m/s); b_req: độ lớn giảm tốc tương đối (m/s²).',
 'TTC giả định tốc độ tiến gần giữ nguyên. b_req giả định giảm tốc tương đối đều đến khi hết tiến gần, không có trễ hay khoảng đệm. Không dùng TTC âm để kết luận va chạm; không coi mô hình là bảo đảm an toàn thực tế.',
 'A: d=10,v_close=5 → TTC=2 s,b_req=1,25 m/s². B: d=20,v_close=10 → TTC=2 s,b_req=2,5 m/s².',
 'Dùng tốc độ xe thay tốc độ tương đối; quên bình phương; suy cùng TTC thì cùng nhu cầu phanh.'))

mc('p2-t4-d12','clip-inverse',[68],
 'Bộ điều khiển dùng a_raw=y5/0,5 s rồi clip vào [−9;+3] m/s². Log chỉ lưu a_command=+3 m/s². Có thể suy ra điều gì về dự đoán y5 trước clipping?',
 'Chỉ suy ra y5≥1,5 m/s; không khôi phục duy nhất y5','Chắc chắn y5=1,5 m/s','Chỉ suy ra y5≥6 m/s; không khôi phục duy nhất y5',
 'a_command=3 khi a_raw≥3. Vì 0,5 s dương nên y5≥1,5 m/s. Nhiều đầu vào bão hòa cho cùng đầu ra; log lệnh đã clip không giữ đầy đủ dự đoán thô.',calc=True,focus='closed-loop',
 formula=('Từ dự đoán vận tốc đến lệnh gia tốc bão hòa',
 'a_raw=y_5/0,5; a_command=min(3,max(−9,a_raw))',
 'y_5: độ đổi vận tốc sau 0,5 s (m/s); a_raw và a_command: gia tốc (m/s²).',
 'Quy tắc controller trong bài; giới hạn [−9;+3] là cấu hình cho trước, không phải giới hạn phổ quát. y_5 là độ đổi, không phải vận tốc tuyệt đối.',
 'y_5=2 m/s → a_raw=4 m/s² → a_command=3 m/s². y_5=3 cũng cho lệnh3 nên không đảo ngược duy nhất.',
 'Nhân với0,5 thay vì chia; clip trước khi đổi sang gia tốc; cho rằng clipping có phép nghịch đảo duy nhất.'))

mc('p2-t4-d12','completion-aggregation',[35],
 'Chấm từng route bằng S=R×P, R là phần trăm hoàn thành và P là hệ số còn lại sau phạt. Lấy trung bình đều điểm hai route: A có R=100%,P=0,5; B có R=50%,P=1. Điểm tổng là bao nhiêu?',
 '50 điểm trên thang100','56,25 điểm trên thang100','75 điểm trên thang100',
 'S_A=100×0,5=50 và S_B=50×1=50, trung bình50. Nhân trung bình R với trung bình P cho75×0,75=56,25, là phép tổng hợp khác với quy tắc đã cho.',calc=True,focus='closed-loop',
 formula=('Điểm hoàn thành có phạt: nhân trước, tổng hợp sau',
 'S_i=R_i×P_i; S_mean=(Σ_i S_i)/N',
 'R_i: phần trăm hoàn thành route; P_i∈[0,1]: hệ số còn lại sau phạt; S_i: điểm route trên thang100; N: số route.',
 'Dùng trung bình đều route như đề quy định. Công thức từng route theo nguyên tắc hoàn thành nhân hệ số phạt; không ngầm thay bằng tích hai trung bình.',
 'Hai route (100;0,5) và (50;1) → điểm(50;50), trung bình50; tích hai trung bình là56,25 và không đúng quy tắc này.',
 'Cộng hệ số phạt vào hoàn thành; dùng P là phần bị trừ; nhầm trung bình tích với tích trung bình.'))

for item in BATCH:
 item['author_id']='priority-dynamics-author'
 item['review_notes'].append('Gap objective beyond existing T4 calculation items; source formulas visually checked where cited. Supplemental definitions explicitly labeled.')
save('d-dynamics')
