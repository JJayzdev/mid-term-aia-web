"""Source-grounded Track4 drafts, authored by Root; requires independent review."""
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
catalog = json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
docs = {d['document_id']: d for d in catalog['documents']}
questions = []

def add(day, page, stem, answers, correct, explanation, kind='single_choice', difficulty='medium', context=None, rubric=None, cognitive='understand'):
    key = f'p2-t4-d{day:02d}'
    index = 1 + sum(q['day'] == key for q in questions)
    doc = docs[key]
    fmt = 'rubric' if rubric else ('boolean' if kind == 'true_false' else ('multiple_choice' if isinstance(correct, list) else 'single_choice'))
    q = dict(id=f'{key}-q{index:02d}', revision=1, author_id='root-content', phase=2, track=4,
             day=key, topic=key, taxonomy_status='verified', question_type=kind, answer_format=fmt,
             difficulty=difficulty, cognitive_level=cognitive, question=stem, correct_answer=correct,
             explanation=explanation, source_reference=[dict(document_id=key,sha256=doc['sha256'],pdf_page=n,title=doc['title'],verification='needs_review') for n in ([page] if isinstance(page,int) else page)],status='pending_review')
    if context: q['context'] = context
    if rubric: q['rubric'] = rubric
    elif answers:
        shift = (day + index) % len(answers)
        order = list(range(len(answers)))[shift:] + list(range(len(answers)))[:shift]
        q['options'] = [dict(id=chr(97+i),text=answers[old]) for i,old in enumerate(order)]
        q['correct_answer'] = [chr(97+order.index(n)) for n in correct] if isinstance(correct,list) else chr(97+order.index(correct))
        q['shuffle_options'] = True
    questions.append(q)

def criterion(id, description, full, partial, none):
    return dict(id=id,description=description,weight=0.5,full_credit=full,partial_credit=partial,no_credit=none)

add(1,56,'Với softmax + cross-entropy, p=(0,659; 0,242; 0,099) và nhãn one-hot y=(1; 0; 0), gradient theo logits là gì?',
    ['(-0,341; 0,242; 0,099)','(0,341; -0,242; -0,099)','(0,659; 0; 0)','(1; 0; 0)'],0,
    'Slide cho công thức gradient theo logits là p − y. Trừ theo từng thành phần cho kết quả (-0,341; 0,242; 0,099).',difficulty='hard',cognitive='apply')
add(1,66,'Tại sao tăng learning rate quá lớn có thể làm loss tăng dù cập nhật đi ngược gradient?',
    ['Gradient mô tả độ dốc cục bộ; bước quá dài có thể vượt vùng mà hướng đó còn phù hợp.','Gradient ở một điểm bảo đảm giảm loss với mọi độ dài bước; loss tăng chỉ có thể do nhãn sai.','Learning rate chỉ đổi hướng gradient, không đổi độ dài bước cập nhật.','Loss phải giảm ở mỗi bước dù learning rate lớn; dao động chỉ có thể do thiếu tham số.'],0,
    'Gradient cho hướng giảm cục bộ, còn learning rate quyết định độ dài bước. Slide lưu ý gradient không cho biết bước dài bao nhiêu là an toàn.')
add(1,45,'Theo slide, kỹ thuật nào phù hợp để xử lý gradient bùng nổ?',
    ['Cắt gradient (gradient clipping).','Thay mọi skip connection bằng lớp sigmoid.','Chỉ tăng số lớp sigmoid để nhân thêm các đạo hàm nhỏ.','Chỉ giảm độ rộng hidden layer mà không kiểm soát chuẩn gradient.'],0,
    'Slide phân biệt gradient biến mất và bùng nổ; gradient clipping được nêu cho trường hợp bùng nổ.',difficulty='easy')
add(1,81,'Theo phần tổng kết, AdamW tách weight decay khỏi gradient thay vì gộp L2 trực tiếp vào gradient như Adam(weight_decay) trong ví dụ PyTorch.',None,True,
    'Đây là điểm khác biệt được ghi trong tổng kết Chương 4 của tài liệu.',kind='true_false')

add(2,15,'Trong residual learning, nếu ánh xạ mong muốn là H(x), nhánh residual F(x) được định nghĩa thế nào?',
    ['F(x)=H(x)−x','F(x)=H(x)+x','F(x)=x/H(x)','F(x)=H(x)²'],0,
    'Khối residual học phần dư H(x)−x, rồi cộng đường tắt x để tạo F(x)+x.')
add(2,36,'Giữ nguyên chiều embedding d, khi số token n tăng gấp đôi thì chi phí self-attention O(n²d) tăng khoảng bao nhiêu?',
    ['4 lần','2 lần','8 lần','Không đổi'],0,
    'Thay n bởi 2n: (2n)²d=4n²d. Đây là chi phí theo số token, không phải khẳng định mọi thời gian chạy đo được đều đúng gấp bốn.',cognitive='apply')
add(2,32,'Chọn các mô tả đúng về multi-head attention trong slide.',
    ['Mỗi head có bộ chiếu Q, K, V riêng.','Kết quả các head được ghép lại rồi chiếu thêm một lần.','Mọi head bắt buộc dùng chung cùng một Q, K, V.','Các head chạy nối tiếp và mỗi head chỉ nhận đầu ra của head trước.'],[0,1],
    'Slide mô tả h phép attention song song, từng head có các phép chiếu riêng; các kết quả được concatenate rồi chiếu đầu ra.',kind='multiple_choice')
add(2,15,'Mạng thường 56 lớp có sai số huấn luyện cao hơn mạng 20 lớp; chỉ dấu đó đủ để kết luận nguyên nhân là overfitting.',None,False,
    'Slide gọi đây là degradation và nhấn mạnh sai số ngay trên tập huấn luyện đã cao hơn, nên không thể giải thích đơn thuần là overfitting.',kind='true_false')

add(3,14,'Hai bounding box có diện tích phần giao bằng 4 và phần hợp bằng 10. IoU bằng bao nhiêu?',
    ['0,4','2,5','0,6','4'],0,
    'IoU là diện tích giao chia diện tích hợp: 4/10=0,4.',cognitive='apply')
add(3,28,'Trong greedy NMS, sau khi lọc confidence, bước nào được thực hiện trước khi loại các box chồng lấn?',
    ['Sắp score giảm dần và giữ box có score cao nhất.','Giữ box có diện tích lớn nhất bất kể score.','Lấy trung bình tọa độ mọi box rồi xóa tất cả box ban đầu.','Sắp score tăng dần và giữ box thấp nhất.'],0,
    'NMS giữ box điểm cao nhất, rồi loại box còn lại có IoU vượt ngưỡng với box vừa giữ; sau đó lặp lại.')
add(3,14,'Slide nêu những vai trò nào của IoU? Chọn tất cả đáp án đúng.',
    ['Assignment khi huấn luyện.','Ngưỡng trong NMS.','Tiêu chí TP/FP khi đánh giá.','Đo trực tiếp xác suất thuộc lớp của vật thể từ logits phân loại.'],[0,1,2],
    'Ba vai trò được liệt kê trực tiếp: assignment, NMS, đánh giá TP/FP. IoU đo mức chồng lấn hình học, không phải xác suất lớp từ logits.',kind='multiple_choice')
add(3,24,'Trong kiến trúc YOLO26 minh họa trên slide, head one-to-one có thể suy luận không cần NMS.',None,True,
    'Sơ đồ phân biệt head one-to-many đi qua NMS và head one-to-one không NMS. Câu hỏi bám cấu hình minh họa của tài liệu, không khái quát cho mọi detector.',kind='true_false')

add(4,22,'Những đại lượng nào thuộc camera intrinsics?',
    ['Focal length và principal point.','Distortion của ống kính.','Rigid transform từ LiDAR sang camera.','Timestamp offset giữa camera và radar.'],[0,1],
    'Intrinsics mô tả tiêu cự, tâm ảnh và méo ảnh; biến đổi giữa cảm biến là extrinsics, lệch timestamp là temporal calibration.',kind='multiple_choice')
add(4,22,'Nên ưu tiên kiểm tra nhóm nguyên nhân nào?',
    ['Temporal calibration/time sync.','Intrinsics: tiêu cự và méo ống kính, không xét thời gian.','Extrinsics: chỉ một biến đổi cứng cố định, không xét timestamp.','Chỉ giới hạn range của LiDAR, bỏ qua độ trễ.'],0,
    'Slide gợi ý object lệch theo vận tốc là dấu hiệu của lỗi time sync; cần kiểm tra timestamp offset, latency hoặc rolling-shutter timing.',kind='scenario',context='Hợp nhất camera–LiDAR trông gần đúng khi xe đứng yên, nhưng vật thể lệch ngày càng nhiều khi xe chạy nhanh.',cognitive='apply')
add(4,23,'Online calibration cần đủ robust trước các vật thể chuyển động trong cảnh.',None,True,
    'Slide ghi ước lượng khi xe/robot đang chạy phải robust với dynamic objects.',kind='true_false',difficulty='easy')
add(4,[22,23],'Nêu hai bước kiểm tra có căn cứ để xử lý độ lệch sau khi tháo lắp cảm biến: một bước chẩn đoán và một bước đánh giá sau hiệu chỉnh.',None,
    'Kiểm tra extrinsics/rigid transform và dấu hiệu projection drift sau tháo lắp; hiệu chỉnh rồi đo reprojection error, so sánh ảnh hưởng đến mAP hoặc association.',
    'Slide phân biệt extrinsics với intrinsics/time sync; phần re-calibration nêu rung, tháo lắp, va chạm là trigger và đề xuất đo reprojection error cùng mAP/association drop.',kind='scenario',difficulty='hard',cognitive='analyze',context='Sau khi tháo lắp LiDAR, phép chiếu lên camera bị lệch cố định. Nhóm muốn xác định nguyên nhân và chứng minh hiệu chỉnh có ích.',rubric=[
        criterion('diagnosis','Chẩn đoán hình học sau tháo lắp','Nêu kiểm tra extrinsics/rigid transform và liên hệ với độ lệch cố định hoặc projection drift sau tháo lắp.','Nêu đúng extrinsics/rigid transform nhưng chưa liên hệ với triệu chứng.','Không nêu kiểm tra extrinsics hoặc chỉ quy lỗi cho nhãn/loss.'),
        criterion('measurement','Đánh giá sau hiệu chỉnh','Nêu đo reprojection error trước–sau và thêm ít nhất một chỉ số mAP hoặc association để kiểm tra ảnh hưởng.','Chỉ nêu một trong hai: reprojection error hoặc mAP/association trước–sau.','Không nêu phép đo liên quan, chỉ đánh giá bằng cảm giác.')])

add(5,18,'Thứ tự hai bước lặp của Kalman filter được mô tả thế nào?',
    ['Dự đoán trạng thái, rồi cập nhật bằng phép đo mới.','Gán phép đo làm trạng thái và bỏ hoàn toàn dự đoán.','Chỉ dự đoán, không sử dụng phép đo.','Huấn luyện lại mạng neural từ đầu ở mỗi bước.'],0,
    'Predict đưa ước lượng tiến theo mô hình; update kết hợp phép đo đến với trọng số phù hợp.',difficulty='easy')
add(5,18,'Bộ lọc Kalman cần giữ hai đại lượng cốt lõi nào giữa các bước?',
    ['Ước lượng trạng thái x và độ bất định P.','Ước lượng trạng thái x và ma trận nhiễu đo R, không cần P.','Ma trận chuyển trạng thái F và nhiễu quá trình Q, không cần x.','Phép đo gần nhất z và ma trận đo H, không cần trạng thái ước lượng.'],0,
    'Slide nói bộ lọc nhớ phỏng đoán tốt nhất x và độ bất định P, không bắt buộc giữ toàn bộ lịch sử.',difficulty='easy')
add(5,31,'EKF xử lý mô hình đo phi tuyến theo cách nào?',
    ['Tuyến tính hóa cục bộ bằng Jacobian quanh ước lượng hiện tại.','Giả định mọi hàm đo đều tuyến tính trên toàn miền.','Thay hàm đo bằng trung bình các phép đo mà không tuyến tính hóa quanh ước lượng.','Tính Jacobian một lần tại gốc tọa độ rồi giữ cố định cho mọi trạng thái tiếp theo.'],0,
    'EKF dùng hàm thật để dự đoán, tính đạo hàm/Jacobian tại điểm đang tin và dùng xấp xỉ đó cho cập nhật.')
add(5,31,'Theo slide, khi hàm cong mạnh hoặc độ bất định lớn, xấp xỉ của EKF có thể lệch cả trung bình lẫn độ rộng phân phối.',None,True,
    'Slide minh họa sự khác biệt của phân phối thật và xấp xỉ EKF, đồng thời nêu các điều kiện làm xấp xỉ kém.',kind='true_false')

add(6,9,'Vì sao voxel kết hợp sparse convolution giúp tiết kiệm tính toán trên point cloud?',
    ['Chỉ tính convolution tại các voxel có dữ liệu.','Tính dense convolution trên mọi voxel rỗng và không rỗng với chi phí như nhau.','Chỉ tính tại voxel rỗng và bỏ qua voxel có điểm đo.','Nội suy lấp mọi voxel rỗng rồi luôn chạy dense convolution trên toàn lưới.'],0,
    'Sparse convolution tận dụng không gian thưa: tránh tính tại các voxel rỗng.')
add(6,7,'Chọn các mô tả đúng về biểu diễn point cloud.',
    ['Point-based học trực tiếp trên tập điểm.','Pillar/BEV nén theo trục thẳng đứng.','Range-view chiếu sang ảnh theo góc quét.','Voxel-based luôn giữ nguyên liên tục mọi tọa độ và không rời rạc hóa.'],[0,1,2],
    'Slide so sánh point, voxel, pillar và range-view; voxel-based rời rạc hóa không gian 3D, nên mô tả giữ liên tục mọi tọa độ là sai.',kind='multiple_choice')
add(6,5,'Mật độ điểm LiDAR thường giảm theo khoảng cách, nên vật thể xa có ít điểm hơn.',None,True,
    'Đây là một đặc tính point cloud được nêu trong slide, ảnh hưởng khả năng nhận biết vật thể xa.',kind='true_false',difficulty='easy')
add(6,4,'Việc nào cần được ưu tiên trước khi tăng độ phức tạp model?',
    ['Đối chiếu frame, quy ước yaw, deskew và metadata giữa train và inference.','Chỉ tăng số lớp backbone để hấp thụ sai lệch tọa độ.','Bỏ timestamp để pipeline đơn giản hơn.','Chỉ thay NMS threshold mà không kiểm tra preprocessing.'],0,
    'Slide chỉ rõ sai frame/yaw, khác deskew và thiếu timestamp/calibration metadata có thể làm hỏng pipeline; cần ổn định dữ liệu và hình học trước.',kind='scenario',context='Detector 3D chạy tốt trên dữ liệu train nhưng suy luận thực tế cho box quay sai hướng. Pipeline train và inference do hai nhóm cấu hình riêng.',cognitive='apply')

add(7,20,'Hungarian giải bài toán association khác greedy ở điểm chính nào?',
    ['Tìm phép ghép có tổng cost nhỏ nhất cho toàn bộ ma trận.','Luôn chọn cặp có cost nhỏ nhất đầu tiên rồi khóa hàng/cột, không xét toàn cục.','Chỉ ghép theo thứ tự ID tăng dần.','Tối đa hóa số box mới bất kể cost.'],0,
    'Slide đối chiếu greedy chọn cặp rẻ nhất trước với Hungarian tối ưu tổng chi phí toàn cục.')
add(7,27,'Trong ByteTrack được mô tả, box score thấp được dùng để tạo track mới ngay lập tức.',None,False,
    'Box score thấp dùng ở vòng hai để cứu track chưa ghép; slide ghi không sinh track mới từ nhóm box này.',kind='true_false')
add(7,26,'DeepSORT bổ sung thông tin nào so với SORT để giữ ID qua che khuất?',
    ['Embedding ngoại hình/Re-ID.','Chỉ giảm ngưỡng confidence của detector mà không thêm đặc trưng ngoại hình.','Chỉ tăng ngưỡng NMS trên từng frame độc lập.','Chỉ ghép bằng IoU, không dùng embedding.'],0,
    'Slide tóm tắt SORT dựa motion+hình học, DeepSORT thêm trí nhớ ngoại hình để hỗ trợ association.')
add(7,26,'Vì sao matching cascade ưu tiên track mới mất trước track đã mất lâu?',
    ['Dự đoán của track mất lâu kém tin cậy hơn, dễ ghép nhầm nếu xét ngang hàng.','Track mất lâu luôn chắc chắn đã ra khỏi cảnh nên không cần bất kỳ logic vòng đời nào.','Track mới mất đã được gán ID mới và phải xóa ID cũ.','Ngoại hình của track mới mất không thể được lưu lại.'],0,
    'Slide liên hệ thời gian không ghép với độ tin cậy của dự đoán Kalman và nguy cơ ghép nhầm.')

add(8,16,'Hướng bottom-up kiểu LSS đưa ảnh lên BEV dựa vào thành phần nào?',
    ['Ước lượng depth theo pixel rồi nâng/chiếu đặc trưng lên BEV.','Chỉ phép NMS trên box 2D, không có bước dùng depth.','NMS loại toàn bộ điểm nằm ngoài ảnh mà không dùng hình học.','Bỏ camera intrinsics và coi tọa độ pixel là tọa độ mét.'],0,
    'Bottom-up dùng depth để nâng đặc trưng ảnh lên biểu diễn không gian/BEV; chất lượng depth ảnh hưởng kết quả.')
add(8,16,'Chọn mô tả phù hợp với nhánh top-down/query attention trên slide.',
    ['BEVFormer chiếu các điểm 3D của ô BEV vào ảnh để lấy đặc trưng qua attention.','DETR3D dùng object query dự đoán tọa độ 3D rồi lấy đặc trưng ảnh.','Mọi mô hình top-down bắt buộc trước tiên dựng một depth map dense chính xác tuyệt đối.','Top-down không bao giờ sử dụng nhiều frame.'],[0,1],
    'Mô tả về BEVFormer và DETR3D đúng với slide; BEVFormer còn dùng attention với BEV của frame trước, nên phủ định temporal information là sai.',kind='multiple_choice')
add(8,9,'Với tọa độ ảnh (u,v), depth z và ma trận nội tại K, công thức giải mã tọa độ camera trên slide là gì?',
    ['[x,y,z]ᵀ = z·K⁻¹·[u,v,1]ᵀ','[x,y,z]ᵀ = K·[u,v,1]ᵀ / z²','[x,y,z]ᵀ = [u,v,z]ᵀ không cần K','[x,y,z]ᵀ = z·[1,1,1]ᵀ'],0,
    'Slide nêu phép đi ngược từ pixel cùng depth sang tọa độ 3D bằng nghịch đảo camera intrinsics.',difficulty='hard',cognitive='apply')
add(8,19,'Có thể coi biểu đồ NDS camera/LiDAR trên slide là bảng xếp hạng công bằng tuyệt đối giữa mọi model dù backbone và dữ liệu bổ sung khác nhau.',None,False,
    'Slide yêu cầu đọc như xu hướng vì backbone và dữ liệu bổ sung khác nhau, không coi là xếp hạng công bằng.',kind='true_false')

add(9,33,'Để hạn chế leakage khi chia dữ liệu video, nên làm gì?',
    ['Chia theo cảnh/scene, tránh để frame gần trùng của cùng cảnh vào cả train và test.','Chia ngẫu nhiên từng frame rồi tin rằng file khác tên là độc lập.','Cho mọi frame test vào train để giảm variance.','Chỉ đổi tên thư mục sau khi chia ngẫu nhiên từng frame.'],0,
    'Các frame gần nhau rất giống; chia theo cảnh hạn chế việc test có frame gần trùng trong train.')
add(9,16,'Khi đồng bộ camera, LiDAR và IMU trong pipeline, nên join theo loại thời gian nào?',
    ['Event time: lúc sự kiện xảy ra, có xử lý dữ liệu đến muộn.','Ingestion time: lúc pipeline nhận dữ liệu, bất kể độ trễ.','Processing time của từng worker xử lý, không theo thời điểm đo.','Timestamp của lúc ghi Parquet sau khi đã trộn các luồng.'],0,
    'Slide phân biệt event time và ingestion time, yêu cầu join theo thời điểm sự kiện thay vì thứ tự đến.')
add(9,51,'Mask do Grounding DINO + SAM tạo ra trong luồng pre-label đã mặc nhiên là ground truth và không cần người kiểm tra.',None,False,
    'Slide ghi pre-label chưa phải đáp án chuẩn; người vẫn cần kiểm tra/chỉnh nhãn.',kind='true_false')
add(9,30,'Một dataset chỉ được gọi là “v3” chưa đủ để tái tạo thí nghiệm. Cần lưu những thông tin nào để định danh phiên bản và split?',None,
    'Lưu commit/snapshot của dữ liệu, danh sách hoặc quy tắc split tái tạo được (gồm seed nếu dùng) và revision mã xử lý. Tên v3 chỉ là nhãn, không mô tả đầy đủ đầu vào.',
    'Slide định nghĩa version bằng commit dữ liệu + danh sách split + mã xử lý; ví dụ manifest có data commit, split by_scene(seed) và git revision của code.',kind='short_answer',difficulty='medium',cognitive='apply',rubric=[
        criterion('data-code','Định danh dữ liệu và mã xử lý','Nêu cả commit/snapshot dữ liệu và revision mã xử lý.','Chỉ nêu đúng một trong hai: commit dữ liệu hoặc revision code.','Chỉ nêu tên v3/thời gian tùy ý mà không định danh dữ liệu hay code.'),
        criterion('split','Tái tạo tập train/validation/test','Nêu danh sách split cố định hoặc quy tắc tái tạo đầy đủ kèm seed khi ngẫu nhiên; không chỉ phần trăm chia.','Có nêu cần lưu split nhưng chỉ nói tỷ lệ chia, chưa có danh sách/quy tắc tái tạo.','Không đề cập split hoặc đề xuất chia lại ngẫu nhiên mà không lưu thông tin.')])

add(10,39,'Đầu ra đặc trưng của VLA cho robot trong sơ đồ slide là gì?',
    ['Chuỗi hành động như dịch chuyển, xoay và kẹp.','Chỉ caption ảnh mà không có đầu ra hành động.','Chỉ bounding box và class của vật thể.','Chỉ bản đồ độ sâu, chưa sinh lệnh tác động lên robot.'],0,
    'VLA được minh họa là VLM đã pretrain được bổ sung đầu ra hành động, phục vụ điều khiển robot.')
add(10,19,'Ở giai đoạn alignment Qwen3-VL được minh họa, thành phần nào được cập nhật trong khi ViT và LLM đóng băng?',
    ['Projector/merger.','Toàn bộ LLM nhưng không có projector.','Chỉ tokenizer dạng chuỗi, không có tham số học.','Toàn bộ ViT và LLM, projector đóng băng.'],0,
    'Câu hỏi chỉ áp dụng ví dụ Qwen3-VL trong slide: giai đoạn đầu chỉ cập nhật projector/merger. Slide cũng chỉ ra mô hình khác có thể cập nhật khác.')
add(10,8,'Theo slide, những yếu tố nào quyết định số token ảnh?',
    ['Độ phân giải ảnh.','Số tile.','Hệ số gộp các patch/token.','Temperature dùng khi lấy mẫu token văn bản đầu ra.'],[0,1,2],
    'Slide nêu độ phân giải, số tile và hệ số gộp đặt ngân sách token ảnh; số token liên quan chi phí và độ chi tiết.',kind='multiple_choice')
add(10,7,'CLIP được slide mô tả là học tương phản trên cặp ảnh–văn bản.',None,True,
    'Phần lịch sử vision encoder ghi rõ CLIP dùng contrastive learning trên cặp ảnh và văn bản.',kind='true_false',difficulty='easy')

add(11,15,'Slide tách sim2real gap thành những nhóm nào?',
    ['Ngoại hình: ánh sáng, texture, vật liệu.','Nội dung/hành vi: bố cục cảnh, ai đi đâu và khi nào.','Mô hình cảm biến: nhiễu, raydrop, rolling shutter.','Chỉ số lượng epoch; các sai khác của cảnh/cảm biến không liên quan.'],[0,1,2],
    'Ba nhóm giúp chẩn đoán nguyên nhân và chọn cách sửa khác nhau; tăng epoch không thay thế mô hình hóa gap.',kind='multiple_choice')
add(11,23,'Nhận xét nào đúng về phạm vi domain randomization theo phần tổng kết?',
    ['Quá hẹp thì không phủ thế giới thật; quá rộng có thể lãng phí mẫu.','Càng rộng vô hạn càng luôn tốt, không có chi phí nào.','Chỉ cần ngẫu nhiên seed, không cần thay đổi thuộc tính cảnh.','Không nên kiểm tra gap cảm biến vì chỉ appearance ảnh hưởng.'],0,
    'Slide nhấn mạnh cân bằng coverage và hiệu quả lấy mẫu, đồng thời ưu tiên randomization có cấu trúc.')
add(11,36,'Trong cổng tin cậy nhãn được đề xuất cho bài lab, IoU được dùng để đối chiếu gì?',
    ['Box điều kiện đầu vào với box của vật được detector tìm lại trong ảnh sinh.','Box sinh của hai scene không liên quan, bỏ qua box điều kiện.','Hai embedding ảnh–văn bản bằng cosine similarity thay vì đối chiếu vị trí box.','Confidence phân loại của một detector mà không so vị trí box điều kiện.'],0,
    'Slide minh họa kiểm tra vật sinh có nằm đúng chỗ box điều kiện hay không. Đây là thiết kế đề xuất cho lab, không được trình bày như một cổng chuẩn đã được công bố.')
add(11,38,'Để quy lợi ích cho dữ liệu tổng hợp một cách công bằng, cần đối chiếu baseline có cùng số bước huấn luyện, batch và kiến trúc.',None,True,
    'Slide cảnh báo pretrain rồi fine-tune có thể tăng ngân sách huấn luyện; phải kiểm soát số bước/batch/kiến trúc trước khi gán mức tăng cho dữ liệu sinh.',kind='true_false')

add(12,17,'Những thông tin nào được nêu trong thẻ lần chạy để tái tạo log replay?',
    ['Nhật ký và revision mã phần mềm.','Phiên bản model nhận thức và calibration.','Seed và cấu hình.','Chỉ trọng số model cuối cùng; calibration và seed có thể bỏ.'],[0,1,2],
    'Thẻ gồm log, mã phần mềm, model, calibration, seed và config để xác định đầu vào cùng điều kiện chạy.',kind='multiple_choice')
add(12,21,'So sánh hai lần replay cần dung sai cho khác biệt số nhỏ thay vì luôn yêu cầu mọi bit đầu ra giống nhau.',None,True,
    'Slide minh họa ngưỡng khác biệt chấp nhận được; các khác biệt số học và thực thi phải được đánh giá bằng tolerance phù hợp.',kind='true_false')
add(12,43,'Theo ví dụ TTC của slide, khoảng cách 12 m và tốc độ tiến gần 5 m/s cho TTC bằng bao nhiêu?',
    ['2,4 giây','0,417 giây','60 giây','7 giây'],0,
    'TTC = khoảng cách / tốc độ tiến gần = 12/5 = 2,4 giây. Đây là độ đo đơn giản trong ví dụ, không đủ một mình để kết luận an toàn của toàn hệ thống.',cognitive='apply')
add(12,[26,27],'Giải thích vì sao một bộ điều khiển có điểm vòng hở tốt vẫn có thể gây va chạm khi chạy vòng kín.',None,
    'Vòng hở đánh giá trên trạng thái/log đã ghi và không để hành động làm thay đổi thế giới tiếp theo. Vòng kín cho xe đi theo đầu ra của chính nó, nên sai lệch nhỏ tích lũy, dẫn đến trạng thái chưa gặp và có thể va chạm.',
    'Hai slide đối chiếu feedback và việc reset về log: vòng hở xóa tác động sai lệch qua bước, vòng kín giữ tác động và cho sai lệch tích lũy.',kind='short_answer',difficulty='hard',cognitive='analyze',rubric=[
        criterion('feedback','Khác biệt feedback giữa hai kiểu đánh giá','Nêu vòng hở không cho hành động thay đổi trạng thái/log tiếp theo, còn vòng kín có feedback hành động tới thế giới.','Chỉ nêu đúng một phía (vòng hở không feedback hoặc vòng kín có feedback).','Đảo ngược hoặc không nêu được khác biệt feedback.'),
        criterion('accumulation','Giải thích cơ chế thất bại','Liên hệ sai lệch nhỏ tích lũy qua các bước với trạng thái lệch khỏi log và nguy cơ va chạm.','Nêu sai số có thể tích lũy nhưng chưa liên hệ với trạng thái/hậu quả trong vòng kín.','Khẳng định điểm vòng hở cao bảo đảm an toàn hoặc không nêu cơ chế tích lũy.')])

for q in questions:
    if q['id'] in {'p2-t4-d01-q02','p2-t4-d05-q03','p2-t4-d06-q01','p2-t4-d03-q03','p2-t4-d08-q02','p2-t4-d06-q02'}: q['revision']=2

bank = dict(schema_version='1.0.0',bank_version='track4-draft-001',questions=questions)
schema=json.loads((ROOT/'docs/schemas/question-bank.schema.json').read_text(encoding='utf-8'))
jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(bank)
out=ROOT/'data/questions/drafts/root-track4.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote {len(questions)} pending-review questions across 12 documents; schema valid. No approval assigned.')
