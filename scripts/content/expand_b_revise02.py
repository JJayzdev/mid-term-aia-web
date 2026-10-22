from expand_b_revise import ROOT
import json
FIX={
'p2-t2-d04':[
['Chỉ embed query bằng model mới còn giữ mọi vector corpus cũ','Chỉ thay metadata model_version mà không tính lại vector','Chỉ tăng top-k để bù khác biệt hai không gian'],
['Chỉ chọn model nhiều tham số nhất dù golden set thấp hơn','Chỉ dựa nhãn fine-tune tiếng Việt mà không đo miền hẹp','Dùng bảng tiếng Anh như bằng chứng đủ cho mọi domain Việt'],
['RAM cho toàn bộ corpus dù QPS thấp và budget hạn chế','SSD nóng cho mọi vector bất kể ít được truy cập','Không lưu vector và re-embed toàn corpus ở mỗi query'],
['Bắt BM25 và cosine có cùng raw score mới ghép được','Chỉ cộng raw score hai hệ mà không xét thang điểm','Bỏ kết quả sparse vì dense ranking luôn đủ cho exact term'],
['Post-filter luôn trả đủ100kết quả dù chỉ2%hợp filter','Tăng độ chặt filter luôn cải thiện recall của ANN','Chỉ test query không filter vì đủ đại diện tenant filter'],
['Mỗi document chỉ cần một vector như trước bất kể số token','Late interaction giảm storage bằng bỏ mọi vector chi tiết','Bất kỳ DB single-vector nào cũng tự thực hiện MaxSim'],
['Retrieve parent rồi chỉ trả child dù cần ngữ cảnh rộng','Cắt hoàn toàn theo byte và bỏ ranh giới đoạn','Embed mọi page cùng một vector corpus duy nhất'],
['Embed query/doc riêng để lấy candidate nhanh ở stage1','Chỉ tăng top-k mà không so relevance cặp query/doc','Chỉ lọc metadata và bỏ ranking candidate'],
['Chỉ lấy top-k chunk giống query mà không biểu diễn quan hệ','Chỉ tăng overlap để coi mọi quan hệ xuyên tài liệu tự hiện ra','Chỉ exact match tên entity mà không traverse cạnh'],
['Luôn embed query một lần và lấy top-k cố định','Chỉ mở loop nhiều vòng cho mọi query kể cả tra cứu đơn giản','Không cần phản tỉnh bằng chứng trước khi sinh answer'],
['Chỉ raw text không source locator','Chỉ score nhưng không xác định tài liệu/URL','Chỉ tên collection và bỏ citation của chunk'],
['Chỉ làm cache miss nhiều hơn nhưng không thể lộ data','Cosine cao tự bảo đảm hai query thuộc cùng tenant','TTL ngắn thay thế hoàn toàn tenant isolation'],
['Nâng top-k để cung cấp thêm nhiều instruction từ tài liệu','Cho retrieved text ghi đè policy system khi có từ khóa admin','Chỉ ẩn citation mà vẫn cho tài liệu điều khiển tool'],
['Chỉ giúp sắp xếp feature theo thời điểm ingest hiện tại','Thay entities để lookup không cần khóa','Cho phép lấy latest value làm feature cho mọi thời điểm quá khứ'],
['Precompute amount chưa tồn tại trước khi request đến','Chỉ dùng avg_amount_7d và bỏ amount hiện tại','Viết hai công thức riêng khác nhau cho training và serving'],
['Không có skew vì cùng tên feature đảm bảo cùng giá trị','Chỉ gây data drift của raw input nhưng không đổi feature','Sửa model weights mà không cần đồng nhất cách parse'],
['Cắt mọi hàm đúng cùng số ký tự dù mất signature','Bỏ imports/scope vì embedding luôn tự khôi phục','Chỉ giữ nửa hàm để mỗi chunk nhỏ hơn nhưng không có context'],
],
'p2-t2-d05':[
['Buộc mọi request chờ đến khi toàn batch kết thúc','Padding mọi request tới độ dài lớn nhất là cách duy nhất','Không nhận request mới khi batch đang generation'],
['NVFP4 như định dạng CPU generic không cần hardware support','Chỉ BF16 dù RAM không đủ để giữ weights','NF4 fine-tuning format thay mọi runtime CPU GGUF'],
['Dành contiguous block kích thước tối đa cho từng request','Xóa toàn bộ KV ở mỗi token để tránh fragmentation','Chỉ đặt batch cố định và không cấp phát động'],
['Nhân bản KV đầy đủ nhiều lần trên cùng VRAM','Tăng precision KV lên FP32 để tiết kiệm memory','Chỉ đổi scheduler mà giữ nguyên mọi biểu diễn KV'],
['Materialize toàn bộ ma trận attention vào HBM rồi đọc lại nhiều lần','Tăng số round-trip HBM để chia attention thành nhiều kernel','Chỉ nén weights mà không thay attention memory access'],
['Biên dịch lại mọi graph ở từng output token','Chỉ giảm thời gian tải weights ban đầu từ object storage','Tắt kernel fusion để tăng số launch nhỏ'],
['Dynamo như runtime CPU GGUF độc lập cho laptop','TensorRT-LLM dù môi trường chỉ có CPU không NVIDIA','vLLM GPU serving như lựa chọn duy nhất cho CPU local'],
['Trả ngay mọi output token mới mà không chạy decode','Tái sử dụng mọi prompt chỉ vì cùng độ dài','Skip mọi phần prompt dù prefix không trùng'],
['Bảo đảm mọi fact đúng dù không có grounding','Tự cấp quyền gọi tool khi JSON hợp lệ','Thay eval chất lượng bằng parse schema pass'],
['Tăng chunked-prefill-size để mỗi lượt dùng nhiều memory hơn','Tăng running requests không giới hạn dù đã OOM','Tăng context tối đa trước khi giảm prefill workload'],
['Mọi prompt ngắn unique đều có lợi bất kể KV transfer overhead','Classifier một-pass không decode vẫn cần pool decode riêng','Chỉ tải nhẹ ít concurrency vì transfer không bao giờ có chi phí'],
['Mỗi adapter kèm một bản base weights độc lập trên GPU riêng','Chỉ bỏ adapter và đổi system prompt cho mọi domain','Load đồng thời nhiều full model thay vì share base'],
['Chia requests vào các bản model replicated như DP','Chia layer liên tiếp thành stage như PP','Chia riêng MoE experts như EP'],
['Decode từng token và giữ KV cache tăng như chat generation','Continuous batching là bắt buộc thay mọi static batch','Không thể sort batch theo token length'],
['Chỉ khớp exact prefix rồi skip prefill thay vì trả response cũ','Chỉ cache KV nên không thể bắt query paraphrase','Chỉ hit khi toàn bộ input token giống từng byte'],
['Chạy model rẻ trước rồi mới quyết định defer lên model mạnh','Luôn gọi cả hai model và chọn sau khi sinh xong','Chỉ thay model sau khi user đã nhận câu trả lời'],
['Tăng timeout vô hạn và giữ mọi request trong queue','Chỉ retry cùng model quá tải không có circuit breaker','Đóng health check để load balancer không loại pod lỗi'],
],
'p2-t2-d06':[
['Tracking để thay mọi định dạng serialization model','Registry chỉ đổi stage nhưng tự thay packaging','Projects chỉ đóng environment mà không cần model flavor'],
['Params bất biến như learning_rate','Metrics scalar như accuracy ở từng epoch','Registry stage như Production'],
['Chỉ tối đa accuracy bất kể SLO latency','Chỉ chọn run ít token log nhất','Chỉ xem một metric cuối mà không so trade-off'],
['Chỉ một version được tồn tại nên xóa candidate trước test','Alias bất biến nên không thể dùng champion/challenger','Đổi alias làm ghi đè weights của version cũ'],
['Chỉ tên model chung mà không data/code version','Chỉ timestamp deploy không có eval lineage','Chỉ stageProduction mà không biết source run'],
['Mỗi request cùng user được random variant lại','Chỉ hash response nên user đổi variant theo câu trả lời','Luôn chuyển user sang variant tốt hơn sau một click'],
['Raw dataset lớn được Git copy đầy đủ ở mọi commit','Chỉ model artifact mà bỏ data pointer','Credential remote được commit cùng dataset'],
['Ghi credential cứng vào dvc.yaml được commit','Chia sẻ access key trong README để team tái lập','Đặt credential trong artifact model để CI đọc'],
['Luôn chạy mọi stage bất kể dependency không đổi','Chỉ chạy stage theo tên alphabet','Chỉ so output filename mà không xem deps'],
['DVC quản lý model registry còn MLflow quản lý raw data hash','Hai công cụ thay thế nhau hoàn toàn nên chỉ cần một','Cả hai chỉ dùng cho model serving và không track thí nghiệm'],
['Unit pass bảo đảm mọi distribution/data change không làm quality giảm','AI release chỉ phụ thuộc code, không phụ thuộc data','Weights luôn có hành vi xác định giống binary software'],
['Train tiếp dù dữ liệu critical fail rồi luôn deploy','Chỉ ghi warning nhưng không block training','Tăng epoch để bù schema/data quality lỗi'],
['Model signature input/output schema','File .dvc giữ content hash','Golden dataset version dùng eval'],
['Shuffle test khác nhau mỗi lần để baseline không bị ràng buộc','Train trên held-out set rồi so lại cùng set','Chỉ đo model mới mà không chạy production baseline'],
['Model mới trả response cho5%user như canary','V2thay từng pod production như rolling','Load balancer chuyển toàn traffic sang v2ngay như blue/green'],
['Xóa v1ngay khi deployv2để tiết kiệm nhưng vẫn gọi rollback instant','Trộn weightsv1v2để tránh giữ hai môi trường','Bỏ smoke/integration test vì đã có load balancer'],
['Spike test tăng tải đột ngột trong thời gian ngắn','Stress test tăng tới breaking point','Unit test một hàm preprocessing'],
]}
FIX['p2-t2-d06'][2]=['Chỉ tối đa accuracy bất kể SLO latency','Chỉ chọn latency thấp nhất dù accuracy dưới ngưỡng yêu cầu','Chỉ xem một metric cuối mà không so trade-off']
FIX['p2-t2-d06'][8]=['Luôn chạy mọi stage bất kể dependency không đổi','Chỉ kiểm code thay đổi, bỏ qua thay đổi data dependency','Chỉ so output filename mà không xem deps']
FIX['p2-t2-d06'][12]=['Static access key dài hạn được copy vào từng CI runner','Một service account key lưu thủ công và xoay theo lịch','Credential cá nhân được export thủ công trước mỗi lần chạy']
FIX['p2-t2-d04'][4][0]='Post-filter luôn trả đủ 100 kết quả dù chỉ 2% hợp filter'
FIX['p2-t2-d06'][14]=['Model mới trả response cho 5% user như canary','V2 thay từng pod production như rolling','Load balancer chuyển toàn traffic sang v2 ngay như blue/green']
FIX['p2-t2-d06'][15]=['Xóa v1 ngay khi deploy v2 để tiết kiệm nhưng vẫn gọi rollback instant','Trộn weights v1/v2 để tránh giữ hai môi trường','Bỏ smoke/integration test vì đã có load balancer']
bank=json.loads((ROOT/'data/questions/drafts/expand-b-02.json').read_text(encoding='utf8'))
for q in bank['questions']:
    correct=next(o['text'] for o in q['options'] if o['id']==q['correct_answer']);ix=int(q['id'][-2:])-1
    ts=[correct]+FIX[q['topic']][ix];n=(int(q['topic'][-2:])+ix+1)%4;ts=ts[n:]+ts[:n]
    q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(ts)];q['correct_answer']=chr(97+ts.index(correct));q['revision']=2
    for old,new in [('Bảng nêu ','') ,('Slide nêu ',''),('Nguồn nêu ',''),('Bảng mô tả ',''),('Slide yêu cầu ',''),('Bảng ',''),('được mô tả ','')]:q['explanation']=q['explanation'].replace(old,new)
    q['explanation']=q['explanation'][0].upper()+q['explanation'][1:]
    if q['id'] in ['p2-t2-d04-x05','p2-t2-d06-x03','p2-t2-d06-x09','p2-t2-d06-x13','p2-t2-d06-x15','p2-t2-d06-x16']:q['revision']=3
    if q['id']=='p2-t2-d06-x13':
        q['question']='OIDC federation cấp quyền cho CI/CD run bằng cơ chế nào thay việc lưu AWS key dài hạn?'
        q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(['Dùng identity của run để nhận credential ngắn hạn','Copy static access key vào mỗi runner','Xoay service-account key thủ công định kỳ rồi lưu vào runner','Export credential cá nhân trước mỗi lần chạy'])]
        q['correct_answer']='a';q['revision']=4
(ROOT/'data/questions/drafts/expand-b-02.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf8')
print('b02 revision2 curated')
