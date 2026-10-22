"""Explicit editorial revisions; preserve answers while varying option positions."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[2]
replacements={
'p1-d02-q01':['Chọn kiến trúc model trước rồi tìm nhóm khách phù hợp','Người dùng gặp khó khăn ở công đoạn nào?','Định nghĩa chatbot là outcome trước khi quan sát workflow','Ưu tiên tự động hóa mọi bước có dữ liệu sẵn'],
'p1-d02-q03':['Công việc lặp lại cần chuẩn hóa','Thời gian hao phí cho tìm kiếm/đọc hiểu/chờ đợi','Bắt đầu từ model mới nhất rồi tìm pain để khớp vào','Xem yêu cầu tính năng của stakeholder là bằng chứng pain đã được xác nhận'],
'p1-d04-q01':['Prompt engineering: viết lại lời nhắc trong message','Context engineering: chọn token của một lần gọi','Loop engineering: quy tắc lặp và điều kiện dừng','Harness engineering chỉ đổi danh sách tool mà không sửa quy tắc lặp'],
'p1-d04-q03':['Sandbox','Quyền và trace','Chọn những token model nhìn thấy trong một lần gọi là toàn bộ harness','Viết câu chữ của một message là toàn bộ harness'],
'p1-d10-q03':['Liên quan chủ đề','Không lỗi thời hoặc mâu thuẫn với bản mới hơn','Chỉ cần top-k similarity cao, bỏ qua phiên bản tài liệu','Chỉ cần job ingestion thành công, không xét nội dung retrieved'],
'p1-d12-q01':['Giữ state trong RAM và dùng sticky session để tránh external store','Externalize state ra bên ngoài instance','Đưa mọi phiên người dùng vào container image khi build','Khởi tạo lại toàn bộ lịch sử khi container restart'],
'p1-d12-q03':['Health check endpoint','Graceful shutdown','Đưa API key vào source để dev/prod giống nhau','Dùng local instance state thay cho lưu trữ bên ngoài'],
'p1-d13-q01':['Monitoring dựa trên các alert đã định nghĩa sẵn','Observability dựa trên telemetry đủ giàu','Chỉ kiểm tra endpoint còn phản hồi HTTP200','Chỉ tổng hợp một số uptime cho toàn hệ thống'],
'p1-d13-q03':['Metrics','Logs và traces','Chỉ alert rule biết trước, không cần telemetry chi tiết','Chỉ kiểm tra health endpoint thành công, bỏ qua trace của request'],
'p1-d15-q01':['Ollama như lựa chọn ưu tiên cho mọi tải production lớn','vLLM','Giữ mọi request chạy tuần tự để tránh batch','Chỉ so giá token API, không cần xét khả năng inference'],
'p1-d15-q03':['GPU','Ops và maintenance','Chỉ tiền token của cloud, không xét phí sở hữu GPU','Chỉ tiền mua GPU lần đầu, xem vận hành bằng không'],
'p1-d03-q01':['Long Horizon: giữ mục tiêu qua nhiều vòng/state','Dynamic Decision','Multi-step Reasoning: chia thành bước phụ thuộc','Tool Interaction: cần gọi công cụ bên ngoài'],
'p1-d03-q03':['Multi-step Reasoning','Long Horizon','Chỉ số lần trả lời đúng một FAQ cố định','Chỉ số lượng token tối đa, không xét workflow'],
'p1-d05-q01':['Functional job đã bao phủ cả nhu cầu cảm xúc nên không cần hỏi thêm','Sản phẩm có thể đúng chức năng nhưng không được dùng lại','Functional job chỉ là tính năng; chỉ cần đổi tên tính năng thành job','Social job chỉ liên quan đội bán hàng, không liên quan người dùng'],
'p1-d05-q03':['Người dùng muốn hoàn thành việc gì?','Người dùng muốn được nhìn nhận ra sao?','Model có thể tự động hóa tính năng nào, bất kể mục tiêu người dùng?','Tính năng đã được implement chưa, thay cho việc hỏi nhu cầu?'],
'p1-d06-q01':['Đã done nếu unit test của code pass dù chưa đo output','Chưa đủ điều kiện done','Đã done nếu demo một prompt thành công','Đã done nếu có feature nhưng chưa có tiêu chí chất lượng'],
'p1-d06-q03':['Citation coverage đủ','Escalation path rõ và test set đạt ngưỡng','Chỉ có endpoint trảHTTP200, không cần kiểm tra câu trả lời','Chỉ hoàn thành coding task, để eval sau khi release'],
'p1-d07-q01':['Fixed-size cắt mỗi Ntoken với overlap','Heading/structural','Recursive chỉ dừng khi vừa kích thước dù mất section metadata','Chia theo kích thước file lưu trữ thay vì nội dung'],
'p1-d07-q03':['Cố gắng tôn trọng ranh giới tự nhiên','Vẫn có thể phải cắt nếu một đoạn quá dài','Bảo đảm không bao giờ phải cắt đoạn vượt giới hạn','Bắt buộc tài liệu có heading chuẩn mới thực hiện được'],
'p1-d08-q01':['Brainstorm tự do không cần corpus/citation','Tra cứu policy nội bộ thay đổi và cần nguồn kiểm chứng','Một tác vụ kiến thức chung mà prompt đơn giản đã đủ','Không có corpus riêng nhưng muốn thêm vectorDB để gọi làRAG'],
'p1-d09-q01':['Cho mọi agent đồng thời ghi cùng báo cáo để tối đa song song','Song song việc đọc, tuần tự hóa việc ghi chung','Tuần tự hóa cả đọc độc lập vì mọi multi-agent đều có xung đột','Tách đọc nhưng bỏ bước điều phối lúc hợp nhất và ghi'],
'p2-t1-d01-q01':['Chỉ chốt prompt rồi đóng hoạt động eval sau release','Monitor, eval, fallback và iterate','Chỉ đo uptime vì output quality sẽ ổn định như phần mềm deterministic','Chỉ kiểm tra unit test lúc build, không xét model drift'],
'p2-t1-d01-q03':['Monitor','Eval và fallback','Xem model drift là việc riêng provider nên bỏ qua','Chỉ lặp lại build khi có lỗi compile'],
'p2-t1-d02-q03':['Hai bên tìm thấy nhau nhanh hơn','Tài xế chờ ít hơn','Notification đã được phát thành công là outcome cuối cùng','Số notification gửi được thay thế được việc đo thời gian chờ'],
'p2-t1-d03-q01':['Để giảm nhu cầu quan sát người dùng vì một test luôn đủ','Để biết phản ứng đến từ thay đổi nào','Để có thể ship cả sản phẩm sau một prototype','Để biến một pain đã thấy thành bằng chứng mọi solution đều đúng'],
'p2-t1-d04-q01':['Chỉ chọn các output demo thành công','Log và tương tác thực, gồm thumbs-down/usage','Chỉ dùng benchmark của provider thay cho application data','Tạo thật nhiều samples trước khi xác định failure mode'],
'p2-t1-d04-q03':['Curate targeted dataset','Score rồi inspect/review failures','Chỉ đổi prompt theo trực giác thay vì nhìn failure themes','Giữ dataset bất biến dù log thật xuất hiện failure mới'],
'p2-t1-d05-q01':['Chỉ xác định giá trị đạo đức mà không phân vai','Quy trình, vai trò và accountability','Chỉ đo benchmark và quyết định threshold','Chỉ thêm một content filter mà không xác định ownership'],
'p2-t1-d05-q03':['Fairness','Human rights và transparency','Threshold chặn launch là định nghĩa toàn bộ Ethics','Process và roles thay thế được mọi câu hỏi giá trị'],
'p2-t1-d06-q01':['CTR/reach','D1/D7/D30 return rate','Onboarding completion trong lần đầu','Trial-to-paid/LTV'],
'p2-t1-d07-q01':['Usage API là chi phí cố định không tăng theo người dùng','Power user tạo cost lớn hơn khoản phí cố định','Lợi nhuận của đa số user luôn bù mọi power user','Unlimited giúp tránh mọi nhu cầu đo cost/usage'],
'p2-t1-d07-q03':['Power user trả tương xứng cost tạo ra','Bảo vệ margin ở các mức sử dụng','Xóa quota nhưng vẫn không thu phí usage vượt','Chỉ tính average user và bỏ qua tailusage'],
'p2-t1-d08-q03':['API token/STT/TTS','Infra/server/telephony','Chỉ lấy API cost vì HITL và retry không thuộc cost hoàn thành job','Chỉ lấy server cost và xem sales overhead luôn bằng không'],
'p2-t1-d09-q01':['Nếu retention thấp thì xem xét lại','Nếu D30retention dưới ngưỡng Xgiả định trong hai cohort liên tiếp thì dừng acquisition để điều tra onboarding; không tăng quảng cáo để bù','Nếu một tuần xấu thì tự động tăng quảng cáo không cần xét cohort','Chỉ đặt ngưỡng nhưng không chỉ rõ thời gian và hành động'],
'p2-t1-d10-q03':['Họ có ảnh hưởng đến kết quả không?','Họ có quan tâm đến dự án không?','Họ có chức danh cao không, bất kể ảnh hưởng thực tế?','Họ đã sử dụng AI chưa, thay cho mức quan tâm dự án?'],
}
for filename in ['phase1-remaining.json','track1.json']:
 path=ROOT/'data/questions/drafts'/filename
 if not path.exists():continue
 bank=json.loads(path.read_text(encoding='utf-8'));changed=[]
 for q in bank['questions']:
  if q['id'] in replacements:
   texts=replacements[q['id']]
   assert len(texts)==len(q['options'])
   for o,t in zip(q['options'],texts):o['text']=t
   q['revision']=2;changed.append(q['id'])
  if 'options' in q:
   # Stable rotation preserves option IDs and therefore correct-answer semantics.
   n=(int(q['id'].split('-d')[-1].split('-')[0])+int(q['id'][-2:]))%len(q['options']);q['options']=q['options'][n:]+q['options'][:n]
 bank['bank_version']+='-curated';path.write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8');print(filename,','.join(changed))
