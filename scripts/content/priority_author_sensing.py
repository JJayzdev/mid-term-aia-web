from priority_author_common import *
D='p2-t4-d04';F='sensors'
match(D,'sensor-strengths',[7,9,11,17,18],'Ghép một-một cảm biến với loại thông tin và giới hạn điển hình.',[
 ('Camera','Màu sắc/texture/ngữ nghĩa; nhạy với ánh sáng','Camera cung cấp hình ảnh giàu ngữ nghĩa nhưng chói/tối có thể giảm chất lượng.'),('LiDAR','Khoảng cách và hình học3D; point cloud có thể thưa hoặc suy giảm thời tiết','Đo range không bảo đảm point cloud sạch trong mọi điều kiện.'),('Radar','Range và vận tốc xuyên tâm qua Doppler; có thể có multipath/ghost','Vận tốc xuyên tâm không đồng nghĩa toàn bộ vector vận tốc3D.')],
 'Sensor fusion tận dụng tính bổ sung; không cảm biến nào luôn chính xác trong mọi điều kiện. Radar không trực tiếp cung cấp đủ mọi thành phần vận tốc chỉ từ một Doppler.',focus=F)
match(D,'sensor-calibration',[22,24],'Ghép một-một loại cấu hình với đại lượng nó mô tả.',[
 ('Intrinsic camera','Tiêu cự, tâm ảnh và mô hình distortion','Đây là tham số bên trong phép chiếu của camera.'),('Extrinsic giữa camera và LiDAR','Phép quay/tịnh tiến giữa hai hệ tọa độ','Sai extrinsic làm geometry không khớp dù thời gian đã đúng.'),('Time synchronization','Căn thời điểm ghi nhận giữa các luồng sensor','Đúng spatial transform vẫn không sửa được vật thể đã di chuyển giữa hai timestamp.')],
 'Ba lớp lỗi khác nhau nên cần chẩn đoán riêng. Không dùng chỉnh extrinsic để che một offset thời gian thay đổi theo chuyển động.',focus=F)
mc(D,'sensor-offset-calc',[24],'Hai sensor lệch timestamp40 ms. Một vật chuyển động ngang đều15 m/s trong hệ chung. Bỏ các nguồn sai số khác. Độ lệch vị trí chỉ do thời gian là bao nhiêu?',
 '0,60 m','600 m','0,0006 m',
 'Đổi40 ms=0,040 s. Với vận tốc không đổi, Δx=v×Δt=15×0,040=0,60 m. Dùng40 như giây sai1000lần; đổi ms hai lần cho0,0006 m.',focus=F,calc=True,
 formula=('Sai lệch do timestamp','Δx=v×Δt','v: vận tốc tương đối theo hướng xét; Δt: lệch thời gian tính bằng giây; Δx: sai lệch vị trí.','Xấp xỉ chuyển động đều trong khoảng ngắn, cùng hệ tọa độ; chưa tính quay,gia tốc hoặc rolling shutter.','15 m/s và40 ms →15×0,040=0,60 m.','Quên đổi ms sang s; dùng công thức1D cho cả quay phức tạp mà không nêu giả định.'))
mc(D,'sensor-direction-test',[22,24],'Kết quả kiểm tra nào giúp phân biệt lỗi thời gian với extrinsic cố định trong tình huống này nhất?','So sánh overlay lúc đứng yên và lúc chạy hai hướng, đồng thời kiểm timestamp','Chỉ tăng số layer của mạng fusion','Chỉ dùng một frame đẹp rồi kết luận calibration đúng',
 'Lệch do thời gian phụ thuộc chuyển động; kiểm đứng yên và đổi hướng kết hợp timestamp giúp tách giả thuyết. Extrinsic cố định thường tạo pattern sai hình học ngay cả khi đứng yên; không kết luận chỉ từ một frame.',focus=F,context='Overlay LiDAR–camera gần khớp khi xe đứng yên nhưng lệch rõ khi xe chuyển động; muốn chọn kiểm tra để phân biệt nguyên nhân.')
match('p2-t4-d06','fusion-levels',[19],'Ghép một-một kiến trúc với mức fusion được mô tả.',[
 ('Đưa dữ liệu các sensor đã căn chỉnh vào chung đầu vào','Early/data fusion','Thông tin được gộp trước backbone đặc trưng chính.'),('Mỗi sensor có encoder, sau đó kết hợp feature maps','Intermediate/feature fusion','Sự kết hợp diễn ra ở biểu diễn đặc trưng.'),('Mỗi sensor tạo detections rồi mới kết hợp quyết định','Late/decision fusion','Các dự đoán đã được tạo riêng trước khi ghép.')],
 'Phân loại theo vị trí gộp thông tin trong kiến trúc cụ thể, không theo tên sensor. Một hệ thống có thể kết hợp nhiều mức.',focus=F)
order('p2-t4-d06','fusion-pipeline',[19,20,21],'Một kiến trúc feature fusion được quy định: căn thời gian/hệ tọa độ trước, hai encoder độc lập, fusion feature rồi detection head. Sắp xếp pipeline.',[
 'Kiểm tra và căn thời gian/hệ tọa độ dữ liệu đầu vào','Chạy encoder camera và encoder LiDAR độc lập','Đưa feature về biểu diễn tương thích rồi gộp','Chạy detection head trên feature đã gộp'],
 'Đề chỉ mô tả một kiến trúc cụ thể. Hai encoder độc lập được gộp thành một bước để không ép thứ tự; late fusion lại tạo detections riêng trước khi gộp.',focus=F)
q(D,'sensor-weather-checks',[15,17,18,19],'Khi quality LiDAR giảm trong mưa và radar có ghost, những hành động nào cần thiết trước khi tin output fusion? Chọn tất cả đáp án đúng.',
 ['a','b'],'Cần quan sát quality từng sensor và đánh giá theo slice điều kiện thực. Fusion không tự làm input sai thành đúng, cũng không cho phép coi radar bất biến với môi trường.',[
 'Theo dõi health metrics riêng và dấu hiệu bất thường của từng sensor','Đánh giá lại output theo slice thời tiết và nguyên nhân ghost/multipath','Mặc định fusion luôn tốt hơn từng sensor nên bỏ theo dõi health','Coi radar đo chính xác toàn bộ vector vận tốc trong mọi điều kiện'],fmt='multiple_choice',focus=F,context='Hệ thống camera–LiDAR–radar được đưa từ thời tiết khô sang mưa; các luồng có dấu hiệu suy giảm khác nhau.')
save('sensors')
D='p2-t4-d12';F='closed-loop'
match(D,'loop-modes',[24,26,27],'Ghép một-một chế độ đánh giá với việc hành động có thay đổi đầu vào tiếp theo hay không.',[
 ('Open-loop trên log cố định','Dữ liệu tương lai vẫn theo log dù model đưa hành động khác','Hành động mới không thay diễn tiến đã ghi.'),('Closed-loop trong môi trường tương tác','Hành động thay trạng thái môi trường và quan sát tiếp theo','Vòng phản hồi giữ hệ quả các quyết định của model.'),('So chỉ số perception trên từng frame','Đo chất lượng nhận thức nhưng chưa trực tiếp đo hệ quả hành động','mAP không tự là xác suất va chạm của toàn hệ thống.')],
 'Trong ngữ cảnh xe/robot, khác biệt chính là phản hồi hành động vào môi trường. Một video dài phát lại vẫn có thể là open-loop.',focus=F)
order(D,'robot-feedback',[26,27],'Bắt đầu tại thời điểm robot nhận quan sát mới. Sắp xếp một chu kỳ closed-loop theo kiến trúc Sense–Perceive–Plan–Act đã cho.',[
 'Nhận quan sát từ sensor','Nhận thức/ước lượng trạng thái môi trường','Lập kế hoạch dựa trên trạng thái ước lượng','Phát lệnh điều khiển và hành động','Môi trường thay đổi; sensor tạo quan sát cho chu kỳ kế tiếp'],
 'Plan cần thông tin nhận thức, Act thực thi kế hoạch. Chu kỳ cuối tạo đầu vào cho chu kỳ mới; trong log open-loop cố định, nhánh phản hồi do hành động mới không tồn tại.',focus=F)
q(D,'loop-evidence',[27,28,31,34],'Những kết quả nào vẫn cần kiểm tra trước khi kết luận bản perception mới làm hệ thống lái tốt hơn? Chọn tất cả đáp án đúng.',
 ['a','b'],'mAP chỉ đo một khâu. Cần quan sát hệ quả ở closed-loop và lặp nhiều lượt vì sai lệch tích lũy/nhiễu có thể thay kết quả. Một log đẹp hoặc một seed không đủ chứng minh.',[
 'Kết quả toàn hệ thống ở closed-loop, như va chạm hoặc hoàn thành nhiệm vụ','Độ ổn định qua nhiều lượt và các tình huống có sai lệch tích lũy','Chỉ số mAP tăng là đủ, không cần thử hệ thống','Chỉ chọn lượt mô phỏng có kết quả tốt nhất rồi báo cáo'],fmt='multiple_choice',focus=F,context='Bản nhận thức B có mAP cao hơn A trên tập log; đội phát triển muốn thay A trong robot.')
mc(D,'loop-reset',[27,28],'Nếu reset robot về trạng thái trong log sau mỗi bước đánh giá, cơ chế lỗi nào có nguy cơ bị che?',
 'Sai lệch nhỏ tích lũy khiến quan sát tương lai khác dữ liệu log','Sai số của cảm biến ở frame hiện tại biến mất khỏi dữ liệu','Mọi lỗi phần mềm đều không thể phát hiện bằng replay',
 'Reset xóa hệ quả của hành động trước. Closed-loop giữ các sai lệch này nên robot có thể đến trạng thái lạ và mắc lỗi tiếp; replay vẫn hữu ích cho perception/phần mềm, không phải vô dụng.',focus=F,context='Bộ đánh giá chấm hành động trên từng trạng thái thật đã ghi, rồi chuyển sang trạng thái log kế tiếp bất kể hành động vừa đề xuất.')
essay(D,'loop-explain',[26,27,28,31],'Giải thích vì sao mAP cao hơn trên log chưa bảo đảm ít va chạm hơn khi robot chạy closed-loop.',
 'mAP đánh giá detection trên dữ liệu log cố định. Trong closed-loop, sai lệch perception ảnh hưởng plan/action, làm môi trường và quan sát tiếp theo thay đổi. Lỗi có thể tích lũy hoặc đưa robot tới trạng thái lạ; cần đo kết quả hệ thống trong closed-loop thay vì chỉ suy từ mAP.',
 'Cần nối được chuỗi perception → hành động → quan sát mới, không chỉ nói hai metric khác nhau. Lập luận không khẳng định mAP là vô ích; mAP vẫn giúp đánh giá một khâu.',[
 ('Giới hạn metric/log','Nêu mAP trên log không trực tiếp đo hậu quả hành động của toàn hệ thống','Chỉ nói mAP và va chạm khác nhau','Khẳng định mAP tăng luôn giảm va chạm'),
 ('Vòng phản hồi và hệ quả','Giải thích hành động đổi quan sát tiếp theo và sai lệch có thể tích lũy','Có nhắc phản hồi nhưng chưa nối với lỗi tích lũy/trạng thái lạ','Cho rằng closed-loop dùng tương lai log bất biến')],focus=F)
save('closed-loop')
