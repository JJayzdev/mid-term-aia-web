"""Curated misconception distractors; changes require fresh independent review."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REPAIRS={
'p2-t2-d01':[
['Chỉ chọn region có giá GPU thấp nhất','Chọn cloud có nhiều managed service nhất bất kể nơi lưu dữ liệu','Chỉ chọn cloud có latency inference thấp nhất'],
['Ít cần năng lực ops hơn vì toàn bộ dịch vụ được managed','Có sẵn nhiều availability zone và dịch vụ doanh nghiệp hơn mọi hyperscaler','Luôn phù hợp serving có SLA nghiêm ngặt hơn hyperscaler'],
['Chỉ khuyến nghị cấu hình mà không áp chính sách','Ghi lại hoạt động sau khi quyền đã được cấp','Phân quyền riêng cho từng request ở trong model'],
['Reserved dài hạn vì job có thể bị gián đoạn bất cứ lúc nào','On-demand cho mọi epoch dù đã có cơ chế resume đáng tin cậy','Chỉ dành Spot cho endpoint yêu cầu không gián đoạn'],
['Overcommit GPU giữa các pod mà không phân vùng memory','Tạo nhiều replica model nhưng mỗi replica giữ toàn GPU','Chỉ tăng batch size của một model thay vì cô lập các model'],
['State local trên laptop của một thành viên và không có lock','S3 backend nhưng không dùng cơ chế khóa khi cùng ghi','Mỗi thành viên giữ state riêng cho cùng tài nguyên production'],
['Copy cấu hình thủ công cho mỗi môi trường và sửa trực tiếp','Dùng workspace để tái sử dụng logic, chỉ dùng module để tách state','Dùng cùng workspace/state cho dev, staging và production'],
['Để mọi thay đổi source đều cài lại tất cả dependencies','Để pip cache chỉ tồn tại trong image trung gian bị xóa trước build sau','Để bỏ qua việc pin dependency vì source layer đã bảo vệ nó'],
['requests=1 nhưng limits=2 để scheduler chia sẻ nửa GPU','Chỉ đặt limits=1 và dành requests=0 cho mọi pod GPU','Đặt requests lớn hơn limits để ưu tiên scheduler'],
['Chỉ tạo tên khác nhưng dùng chung mọi RBAC và quota','Gộp serving vào experiments để không cần production isolation','Dùng namespace riêng chỉ để đổi tên pod mà không tách quyền'],
['Đưa mọi traffic dữ liệu ra public internet để giảm egress','Chỉ mã hóa TLS trên internet và xem như đã có private routing','Tạo public IP cho mỗi GPU để tránh mọi network cost'],
['Checkpoint cũ cần giữ lâu nhưng hầu như không được đọc','Compliance archive cần lưu nhiều năm với độ trễ đọc chấp nhận cao','Dataset ít dùng cần giá lưu thấp hơn độ trễ truy cập'],
['Supervisor luôn cần cùng loại GPU với specialist dù chỉ dispatch','Chạy mọi tool nhẹ và orchestrator trên GPU để giữ cấu hình đồng nhất','CPU chỉ được dùng cho storage, không dùng điều phối agent'],
['Redis Streams khi ưu tiên setup đơn giản và latency thấp hơn replay quy mô lớn','RabbitMQ khi trọng tâm là routing rules và dead-letter queue','In-process queue khi cần durability xuyên các instance'],
['L1 in-process cache chỉ giữ kết quả trong một instance','L2 Redis TTL nhưng không cache kết quả embedding theo nội dung query','Chỉ cache model weights thay vì kết quả embedding truy vấn'],
['Chỉ trùng độ dài token dù nội dung prefix khác nhau','Chỉ cùng suffix dù phần đầu prompt hoàn toàn khác','Chỉ cùng tenant dù token prefix khác nhau'],
['Đặt max_model_len luôn128K để tránh đo usage','Tăng GPU memory utilization sát100% để bù context dư','Tắt continuous batching trước khi điều chỉnh độ dài context'],
],
'p2-t2-d02':[
['Sửa trực tiếp Bronze theo logic mới rồi rebuild Silver','Dùng hiện trạng Postgres hôm nay như toàn bộ lịch sử hai tháng','Chỉ chỉnh Silver hiện tại mà không thể replay dữ liệu lịch sử'],
['Một hàng cho mỗi thay đổi kể cả khi cùng ticket_id','Ba hàng vì ba thay đổi tương đương ba thực thể','Một hàng cho mỗi lần retry ingestion thay vì theo khóa thực thể'],
['Chỉ INSERT sau mỗi lần chạy dù ticket_id đã tồn tại','Dùng khóa nullable và xem mọi NULL là cùng một thực thể','Dedupe theo thứ tự đến mà không có định danh thực thể'],
['Không cần giám sát slot vì WAL luôn tự giải phóng dù consumer đứng','CDC log-based phải full-scan bảng cho mỗi thay đổi','WAL không ghi DELETE nên chỉ cần theo dõi INSERT'],
['Fivetran khi bắt buộc tự host mã nguồn mở và ngân sách hạn chế','Tự viết từng connector dù đã có connector hỗ trợ và không muốn bảo trì','Debezium cho mọi SaaS bất kể nguồn có transaction log hay không'],
['JSON gzip vì đọc một cột luôn bỏ qua mọi cột khác không cần parse','Avro vì row format tối ưu hơn column format cho scan vài cột','Arrow vì là định dạng archive tối ưu cho mọi bảng lake trên object storage'],
['Chỉ tham chiếu tên bảng mà không tạo dependency graph','Bắt người dùng khai báo lại toàn bộ thứ tự chạy thủ công','Tự vật hóa mọi model thành table dù config là view'],
['Chỉ đọc dữ liệu mới ngay cả khi không có điều kiện incremental','Tự giữ cửa sổ lookback mà không cần khai báo SQL','Tự loại duplicate dù thiếu unique_key'],
['Tự tạo schema dev bằng copy toàn bộ data cho mỗi thay đổi nhỏ','Dùng chung bảng production để tiết kiệm chi phí dev','Bỏ phân tích tác động và backfill tất cả model sau mọi sửa đổi'],
['Append INSERT cho mọi bản sửa mà không merge theo khóa','Chỉ overwrite toàn bộ lịch sử mà không cần giữ trạng thái đúng','Dedupe bằng thời điểm chạy thay vì khóa thực thể'],
['Sửa âm thầm snapshot cũ để cùng version có nội dung mới','Ghi đè nhãn cũ mà không tạo dataset version','Loại mọi nhãn đến muộn khỏi mọi training version sau này'],
['Chỉ trạng thái mới nhất sau khi đã overwrite lịch sử','Số lần retry pipeline mà không lưu valid_from/valid_to','Giá trị tương lai mới nhất thay cho trạng thái tại thời điểm sự kiện'],
['Pydantic để thay mọi kiểm schema DataFrame bằng kiểm từng payload','dbt tests chạy SQL warehouse dù dữ liệu chỉ nằm trong tiến trình Python','Great Expectations chỉ vì nó không cần asset/suite hay bước validation'],
['Spark làm kho mới và bắt buộc copy mọi nguồn trước truy vấn','Ray Data vì batch inference đồng nghĩa truy vấn SQL liên kho','DuckDB chỉ vì single-process luôn thay thế mọi federated query'],
['Partition theo user_id cardinality cao để tạo thêm file nhỏ','Tăng task ghi cuối pipeline để mỗi file nhỏ hơn nữa','Chỉ tăng worker nhưng giữ nguyên số lần mở/đọc footer file nhỏ'],
['Consumer offset giữ bản sao message dù broker đã hết retention','Thêm partition tự khôi phục message đã bị xóa','Restart consumer từ offset cũ luôn replay được dữ liệu vô hạn'],
['Airflow chỉ như lịch batch và coi mọi chờ nhiều ngày là một task đang chạy','dbt để thay durable execution bằng các transform SQL','Trino làm nơi giữ workflow state và retry xuyên nhiều ngày'],
],
'p2-t2-d03':[
['Chỉ gọi một API theo flow cố định rồi trả lời','Chỉ thêm LLM tạo văn bản vào giao diện chat','Chỉ lưu lịch sử hội thoại mà không có quyết định/hành động'],
['Chỉ hallucination như chatbot, tool/loop không tạo rủi ro mới','Risk thấp hơn mặc định vì tool luôn trả dữ liệu đúng','Chỉ lỗi format, không cần eval các action'],
['Dùng model memory để tự suy đoán giá vé và thời tiết mới','Chỉ trả menu cố định thay vì kiểm tra điều kiện thực tế','Chỉ viết câu trả lời mượt mà mà không truy vấn hai nguồn'],
['Agent có nhớ preference qua nhiều cuộc hội thoại hay không','Bài toán có cần chia nhỏ thành các bước phụ thuộc hay không','Hệ thống có cần gọi API/search/database hay không'],
['Agent autonomy nhiều vòng dù chỉ retrieve một policy ổn định','Orchestrator-worker cho mọi FAQ đơn giản bất kể cost','Rule cứng không có retrieval dù policy thường xuyên được cập nhật'],
['Agent tự do quyết định lại mọi bước dù sequence đã biết','Routing khi không có lựa chọn path/specialist nào','Orchestrator-worker dù không có subtask độc lập để phân công'],
['Reasoning vì nhận dữ liệu đồng nghĩa đã chọn hành động','Action vì mọi tool output đều là tool call mới','Memory dài hạn vì mọi observation luôn phải lưu ngoài context'],
['Lưu mọi nội dung không có chiến lược retrieval/quyền','Tăng storage nhưng không định nghĩa đọc/ghi','Cho mọi agent truy cập toàn bộ memory để đơn giản hóa'],
['Chỉ tên tool và không mô tả kiểu tham số','Input rõ nhưng bỏ output/error contract','Chỉ happy-path output mà không nói failure mode'],
['Lời gọi tool với tên và args trước khi chạy','Kế hoạch chọn hành động trước khi có kết quả','Câu final answer đã tổng hợp xong cho user'],
['Final answer đủ để suy ra chính xác mọi action trước đó','Trace bảo đảm tool không bao giờ fail nên khỏi can thiệp','Chỉ lưu thought, bỏ tool args và observation vẫn debug đầy đủ'],
['Tăng loop ad-hoc vô hạn mà không mô hình hóa state','Chỉ thêm system prompt dài hơn để thay conditional routing','Bỏ persistence và gom mọi nhánh vào một chuỗi messages'],
['Bịa tool result có vẻ hợp lý để không gián đoạn task','Retry vô hạn cùng call bất kể loại lỗi','Im lặng bỏ tool rồi khẳng định đã có dữ liệu mới'],
['Tiếp tục gọi vì observation lặp là bằng chứng đã tiến triển','Tăng max iterations vô hạn thay vì kiểm điều kiện dừng','Chỉ tăng token budget mà không fallback'],
['Chỉ dùng prompt text để diễn tả mọi nhánh mà không có state','Chỉ lưu tool registry nhưng không edges/conditional routing','Chỉ xem final answer và bỏ luồng tool observations'],
['Chỉ sửa final answer mẫu mà không kiểm action thực tế','Chỉ tăng model size trước khi xem tool args','Chỉ chỉnh temperature dù tool description mơ hồ'],
['Mở agent loop cho mọi câu hỏi kể cả FAQ một bước','Dồn mọi request vào chatbot dù cần nhiều tool phụ thuộc','Chỉ dùng human fallback làm đường chính cho mọi yêu cầu'],
]}
bank=json.loads((ROOT/'data/questions/drafts/expand-b-01.json').read_text(encoding='utf-8'))
for q in bank['questions']:
    doc=q['topic'];ix=int(q['id'][-2:])-1
    correct=next(o['text'] for o in q['options'] if o['id']==q['correct_answer'])
    q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate([correct]+REPAIRS[doc][ix])]
    n=(int(doc[-2:])+ix+1)%4;q['options']=q['options'][n:]+q['options'][:n]
    for i,o in enumerate(q['options']):
        if o['text']==correct:q['correct_answer']=chr(97+i)
        o['id']=chr(97+i)
    q['revision']=2
    text=q['explanation']
    for phrase in ['Slide nêu ','Slide nhấn mạnh ','Slide mô tả ','Slide yêu cầu ','Nguồn nêu ','Nguồn mô tả ','Bảng mô tả ','Bảng nêu ','Slide liệt kê ','Tip Terraform nêu trực tiếp ','Networking slide liên hệ ','Bảng queue gắn ','Phần Docker optimization yêu cầu ','Production Setup liệt kê ']:text=text.replace(phrase,'')
    q['explanation']=text[0].upper()+text[1:]
EXPLAIN={
'p2-t2-d01-x01':'Data residency giới hạn vị trí lưu/xử lý; các lựa chọn cloud tại Việt Nam cần được xét cùng compliance và chi phí.',
'p2-t2-d01-x03':'SCPs áp guardrail ở cấp tổ chức/account để enforce security baseline trong Landing Zone.',
'p2-t2-d01-x04':'Spot phù hợp training có thể bị gián đoạn và resume; Reserved phù hợp serving cần ổn định.',
'p2-t2-d01-x06':'S3 giữ state từ xa và DynamoDB lock phối hợp truy cập state trong team.',
'p2-t2-d01-x07':'Module đóng gói logic tái sử dụng; workspace tách state cho các môi trường.',
'p2-t2-d01-x11':'PrivateLink giữ đường truy cập riêng thay internet và có thể tiết kiệm egress cost.',
'p2-t2-d01-x13':'Orchestrator chỉ dispatch không cần chạy LLM trên GPU; specialist thực hiện inference mới cần GPU.',
'p2-t2-d01-x14':'Kafka hỗ trợ throughput cao, lưu bền và replay, phù hợp agent fleet quy mô lớn.',
'p2-t2-d01-x17':'Context tối đa cần khớp phân bố request; cấp dư128K khi phần lớn dưới4K làm lãng phí tài nguyên.',
'p2-t2-d02-x10':'MERGE/upsert cập nhật hoặc thêm theo khóa thực thể, giữ kết quả ổn định khi CDC được xử lý lại.',
'p2-t2-d02-x13':'Pandera kiểm schema DataFrame trong Python; Pydantic kiểm từng payload/record ở biên hệ thống.',
'p2-t2-d03-x02':'Agent thêm hành động tool và vòng lặp nên có tool misuse/loop ngoài hallucination; nhiều calls cũng tăng cost.',
'p2-t2-d03-x05':'Intent ổn định và retrieve policy chủ yếu cần chatbot retrieval; chưa có nhu cầu quyết định tự chủ nhiều vòng.',
'p2-t2-d03-x09':'Input/output/error mode rõ giúp agent chọn tool đúng và xử lý failure của external dependency.',
'p2-t2-d03-x13':'Tool failure cần được phản ánh trung thực và thử fallback; bịa kết quả làm mất grounding.',
'p2-t2-d03-x14':'Tool call lặp mà observation không đổi là dấu hiệu không tiến triển, cần dừng và fallback.',
'p2-t2-d03-x17':'Triage dành chatbot cho câu đơn giản, agent cho nhiều bước và human escalation cho fallback.',
}
for q in bank['questions']:
    if q['id'] in EXPLAIN:q['explanation']=EXPLAIN[q['id']]
    if q['id']=='p2-t2-d03-x04':
        q['question']='Một tool tìm chuyến bay nhận origin, destination, date và max_price. Vì sao max_price cần nằm trong args thay vì chỉ ghi trong lời nhắc chung?'
        q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(['Để công cụ nhận ràng buộc ngân sách có cấu trúc khi truy vấn','Để công cụ tự quyết bỏ qua ngân sách nếu có nhiều kết quả','Để thay date bằng một khoảng giá mà không cần ngày bay','Để chỉ lọc ngân sách sau khi agent đã kết luận'])]
        q['correct_answer']='a';q['explanation']='Tool registry mô tả search_flights bằng route/date/budget args; truyền max_price đưa ràng buộc người dùng vào hành động truy vấn.'
        q['source_reference'][0]['pdf_page']=29;q['source_reference'][0]['locator']='Physical PDF page29; tool registry search_flights args'
    if q['id']=='p2-t2-d03-x11':
        q['question']='Trong một tác vụ nhiều bước, memory/state cần giữ bộ thông tin nào để agent không mất mạch?'
        q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(['Goal, facts và intermediate results của tác vụ','Chỉ final answer, bỏ mọi kết quả trung gian','Chỉ tool name cuối, bỏ goal và facts','Chỉ raw user text đầu tiên, không thêm observation'])]
        q['correct_answer']='a';q['explanation']='Memory giữ goal, facts và intermediate results, giúp các bước sau liên hệ được mục tiêu với kết quả đã quan sát.'
        q['revision']=3;q['source_reference'][0]['pdf_page']=17;q['source_reference'][0]['locator']='Physical PDF page 17; memory/state role in agent architecture'
    if q['id']=='p2-t2-d03-x10':
        q['question']='Sau khi thực thi một tool call, agent loop cần bổ sung những message nào trước lần gọi model kế tiếp?'
        q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(['Message của tool call do model sinh và tool message chứa result','Chỉ user message ban đầu, bỏ call và result vừa thực hiện','Chỉ final answer tự tạo dù model chưa kết luận','Chỉ tool name, bỏ args và result để giảm context'])]
        q['correct_answer']='a';q['explanation']='Loop nối output.as_message() cùng tool_message(output.name, result) vào messages, để model thấy hành động đã yêu cầu và kết quả tương ứng ở vòng sau.'
        q['revision']=3;q['source_reference'][0]['pdf_page']=27;q['source_reference'][0]['locator']='Physical PDF page 27; visually checked pseudocode messages += [output.as_message(), tool_message(output.name, result)]'
    changes={
    'p2-t2-d03-x12':(27,'Một agent loop nhận output.type="final_answer". Điều khiển đúng là gì trước khi gọi run_tool?','Trả output.content và kết thúc, không thực thi tool cho output đó','Luôn gọi run_tool với output.name kể cả khi đã là final answer','Chèn một tool result giả rồi mới trả final answer','Bỏ output và gọi model lại cho đến khi có tool call','Nhánh final_answer return ngay trước run_tool; chỉ output cần action mới đi vào thực thi công cụ.'),
    'p2-t2-d03-x14':(34,'Hàm outfit kiểm rain_probability>0.5 và return đồ mưa trước khi kiểm nhiệt độ. Với rain_probability=0.7 và temp_high=32, kết quả nào theo luồng if/return này?','Nhánh đồ mưa: áo mỏng, giày dễ khô, mang ô gấp','Nhánh trời nóng vì32>30, bỏ qua điều kiện mưa','Ghép cả hai chuỗi vì cả hai if đều phải chạy sau return','Nhánh mặc định có áo khoác vì nhiệt độ dưới33','Điều kiện mưa đúng nên return đầu kết thúc hàm; if nhiệt độ phía sau không được chạy.'),
    'p2-t2-d03-x17':(40,'Để so chatbot baseline với ReAct agent cho cùng use case, vì sao cần chạy cùng bộ test cases?','Giữ đầu vào so sánh nhất quán để nhận ra giá trị do cách xử lý khác nhau','Cho mỗi hệ câu khác nhau để hệ nào cũng có kết quả tốt','Chỉ chọn test agent đã trả đúng còn chatbot chưa được chạy','Thay test bằng một demo đẹp để không cần so từng case','Chạy cùng test cases trên hai hệ giúp so trực tiếp và ghi nhận nơi agent tạo thêm giá trị thay do khác bài toán.'),
    }
    if q['id'] in changes:
        page,prompt,correct,a,b,c,why=changes[q['id']];q.update(question=prompt,correct_answer='a',explanation=why,revision=3)
        q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate([correct,a,b,c])]
        q['source_reference'][0].update(pdf_page=page,locator=f'Physical PDF page {page}; original page visually checked for code questions')
for q in bank['questions']:
    changes={
      'p2-t2-d01-x01':('Một workload phải giữ dữ liệu trong lãnh thổ Việt Nam. Tiêu chí chọn cloud nào trực tiếp đáp ứng ràng buộc này?',['Xác minh region lưu trữ/xử lý tại Việt Nam cùng yêu cầu compliance','Chỉ chọn nhà cung cấp có tên thương hiệu Việt Nam mà không kiểm region','Chỉ chọn GPU rẻ nhất bất kể dữ liệu được xử lý ở đâu','Chỉ chọn latency thấp nhất mà không kiểm data residency'],'Data residency đòi kiểm vị trí lưu/xử lý thực tế; thương hiệu provider không tự chứng minh vị trí dữ liệu.'),
      'p2-t2-d01-x11':('VPC Endpoints/PrivateLink mang lại lợi ích nào?',['Tránh traffic qua internet và có thể giảm egress cost trong kiến trúc phù hợp','Đưa mọi traffic dữ liệu ra public internet để giảm egress','Chỉ mã hóa TLS trên internet là đã có private routing','Tạo public IP cho mỗi GPU để tránh mọi network cost'],'PrivateLink giữ đường truy cập riêng; tiết kiệm chi phí phụ thuộc kiến trúc và luồng dữ liệu.'),
      'p2-t2-d01-x15':('Đội muốn giảm việc embedding lại cùng truy vấn. Cơ chế cache nào nhắm đúng mục tiêu?',['Cache kết quả embedding theo nội dung query','Chỉ cache final answer mà không giữ query embedding','Chỉ cache model weights, vẫn embed mọi query lại từ đầu','Chỉ cache raw documents mà không ánh xạ query tới vector'],'Lưu vector embedding ứng với nội dung query cho phép tái sử dụng khi query lặp lại.'),
      'p2-t2-d03-x15':('Agent có giới hạn số vòng lặp nhưng một tool call bị treo chưa trả về. Guard nào trực tiếp giới hạn thời gian chờ call đó?',['Timeout cho từng tool call','Chỉ max iterations vì nó tự ngắt mọi call đang treo','Chỉ tăng context window để tool trả nhanh hơn','Retry không giới hạn trong cùng tool call'],'Giới hạn số vòng không thay thế timeout của dependency; timeout từng tool chặn một call treo giữ toàn bộ loop.')
    }
    if q['id'] in changes:
        prompt,opts,why=changes[q['id']];q.update(question=prompt,correct_answer='a',explanation=why,revision=3)
        q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(opts)]
        if q['id']=='p2-t2-d03-x15':q['source_reference'][0].update(pdf_page=30,locator='Physical PDF page 30; tool timeout distinct from max iterations')
for q in bank['questions']:
    if q['id']=='p2-t2-d03-x03':
        q['question']='Một reactive agent tìm vé rồi xét thời tiết tại điểm đến. Việc gọi các tool mang lại lợi ích nào cho câu trả lời?'
        q['explanation']='Các tool cung cấp dữ liệu vé và thời tiết mới; agent tổng hợp kết quả để xét đồng thời các điều kiện của tác vụ.'
        q['revision']=3
(ROOT/'data/questions/drafts/expand-b-01.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
print('b01 revision2 distractors curated')
