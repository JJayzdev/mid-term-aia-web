# -*- coding: utf-8 -*-
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
FIX={
'p2-t2-d10':[
['Thực thi lại mọi request bất kể side effect đã xảy ra','Chỉ đổi request ID là tự bảo đảm không lặp hành động','Chỉ tăng timeout mà không xét idempotency'],
['Chỉ parse JSON body ở mọi hop dù header đã có tên method','Chỉ route toàn endpoint mà không phân biệt tool name','Chỉ dựa IP nguồn để suy ra tool nào được gọi'],
['Không ảnh hưởng vì tên server giống nhau là đủ cache hit','Tool order ngẫu nhiên luôn tăng cache reuse','Chỉ nội dung user message ảnh hưởng prefix, tool schema không ảnh hưởng'],
['Chắc chắn agent không tồn tại dù chưa kiểm URI mới','Chắc chắn agent đã từ chối quyền chứ không phải discovery lỗi','Không cần theo dõi discovery failure vì chỉ là404'],
['Bảo đảm mọi dependency đã được audit bảo mật','Cho phép bỏ private registry approval gate','Bảo đảm tool definition không bao giờ đổi về sau'],
['FAILED ngay vì thiếu quyền luôn là lỗi không phục hồi','COMPLETED dù chưa được phép hoàn tất','REJECTED dù agent chưa từ chối yêu cầu'],
['Chứa private credential để mọi client tự đăng nhập','Thay mọi kiểm tra quyền ở runtime','Chỉ mô tả skill, security scheme luôn phải đoán ngoài card'],
['Cả hai chỉ chọn model rẻ nhất bất kể skill','Agent routing chỉ tối thiểu token mà không xét capability','Model routing chỉ so skill tag thay quality/cost'],
['SPIFFE identity tự cấp mọi resource permission','OAuth scope thay thế hoàn toàn chứng thực workload','API key dùng chung vẫn audit được toàn chuỗi agent'],
['Tool poisoning chỉ lúc đăng ký, không liên quan thay đổi sau approve','Tool squatting giả tên tool khác nhưng không đổi definition cũ','Một lỗi retry thông thường không cần pin/drift alert'],
['Chỉ ở lần login đầu tiên rồi tin mọi call sau','Chỉ khi server mới đăng ký dù policy đã thay đổi','Chỉ khi user đóng session thay vì trước action'],
['Ghi toàn bộ dữ liệu bảng trung gian vào messages sau mỗi bước','Nạp toàn tool schema và mọi tool result trước khi bắt đầu','Chỉ tăng context window mà không giảm dữ liệu transit'],
['Defer cả tool search cùng mọi tool khác','Ẩn tool search khỏi client và chờ model tự gọi tên','Chỉ giữ final answer tool mà không công cụ khám phá'],
['Mọi SDK harness luôn kèm managed deployment','Có SDK thì không còn cần sandbox/capacity planning','Không có managed deployment thì SDK không thể chạy loop'],
['Chỉ lịch sử conversation đủ để khôi phục file đã tạo','Chỉ tool-call name mà không cần artifact filesystem','Chỉ model response cuối cùng thay toàn sandbox state'],
['Chỉ RPS và CPU là đủ dù nhiều session đang chờ người','Chỉ đếm output token đang sinh, bỏ sandbox bị giữ','Chỉ độ sâu queue mà bỏ mọi phiên chờ duyệt'],
['Tin bản tóm tắt luôn giữ mọi policy bất kể độ dài','Chỉ lưu luật trong tool result cũ có thể bị loại','Bỏ guardrail ở lượt dài để tránh tăng context'],
],
'p2-t2-d11':[
['Chỉ GPU-hour, network/service fee không thuộc TCO','Chỉ storage, bỏ toàn bộ egress/NAT','Chỉ token bill, bỏ chi phí hạ tầng retrieval/orchestration'],
['Reserved discount tự triệt tiêu mọi phí idle ban đêm','Là capacity cần thiết vì job đã hoàn thành','Không tính phí khi GPU không có kernel dù VM bật'],
['Tối đa goodput bằng tăng mọi request dù vi phạm SLO','Chỉ tokens/s ở saturation không ràng buộc latency','Chỉ sốGPUbật mà không đo đầu ra'],
['Chỉ dùng peak FLOPs trên spec của chip','Chỉ dùng benchmark model khác precision khác của vendor','Bỏ lock-in vì custom silicon luôn portable giữa cloud'],
['Reserved dài hạn dù duty cycle thấp và biến động','Mua full cluster trước khi có nhu cầu ổn định','Giữ VM24/7để chờ workload thưa'],
['Discount luôn làm reserved rẻ hơn ở mọi utilization','Có commitment thì không còn cần đo idle','Capacity không dùng sẽ luôn được hoàn tiền tự động'],
['Đa AZ/type bảo đảm tuyệt đối không bị reclaim','Chỉ chọn một spot type/AZ để tránh mọi gián đoạn','Spot Fleet thay thế checkpoint/resume'],
['Chỉ lưu model weights, bỏ optimizer/scheduler state khi cần resume training','Chỉ save local disk của instance spot rồi coi là bền','Chỉ kiểm file checkpoint tồn tại mà không thử load/resume'],
['GPU-Util đo trực tiếp tỷ lệ peak FLOPs đạt được','Có kernel chạy đồng nghĩa Tensor Core đã bão hòa','100%time-activeđủ để quyết định mua thêmGPU'],
['Chỉ peak TFLOPs dù workload bandwidth-bound','Chỉ clockCPUorchestrator','Chỉ sốGPUkhông xét bandwidth mỗiGPU'],
['10request/svìmọirequestđềuđượctínhthroughput','7request/svìđó làsốvi phạmSLO','13request/svìcộngcảthroughputvàđạtSLO'],
['Cold start không bị tính phí vì chưa có output token','Scale-to-zero luôn rẻ hơn ở duty cycle100%','Keep-warm không bao giờ có năng lượng idle'],
['MIGchỉchia thời gian không phân vùng memory','Time-slicing luôn có isolation mạnh hơn hardware partition','MIGvàMPSđều bảo đảm memory riêng như nhau'],
['Chỉ giảm idle bên trong card bằng chia MIG','Chỉ tối ưu token prompt mà không thay node allocation','Chỉ tăng số node dự phòng dù nhiều node rỗng'],
['Mọi model luôn sinh cùng số reasoning token cho một task','Giá token thấp hơn luôn làm task rẻ hơn bất kể token usage','Thinking token ẩn không bị tính output cost'],
['Tự optimize model weights thay billing schema','Bảo đảm mọi provider có cùng giá token','Thay toàn tagging/ownership policy bằng một filebill'],
['Chargeback ngay dù tag coverage còn thiếu','Bỏ showback vì tổngbillđủ biếtteamgâychiphí','Chỉchiađềutổngbillmàkhôngđoxemteamnàodùng'],
],
'p2-t2-d12':[
['Job success bảo đảm semantics/đơn vị dữ liệu đúng','TăngCPUworkerđủ đểsửađơnvịprice','Chỉmodelupdate mới có thể làm business number sai'],
['Chỉ thời điểm raw ingest dù serving chưa publish','Chỉ timestamp job khởi động','Chỉ API uptime thay tuổi dữ liệu'],
['Chỉ HTTP status200làđủ','Chỉ process exit code0','Chỉ số retry job mà không đếm record'],
['Mọi drift đều chứng minh corruption phải hard-fail','Campaignkhôngthểlàmrationcategorythayđổi','Driftchỉcầnngưỡngcốđịnhkhôngcầnbusinesscontext'],
['Thêm cột optional không đổi field cũ','Thêm mô tả field mà không đổi dữ liệu','Thêm metadata lineage không đổi required schema'],
['Chỉ kiểu dữ liệu đủ, không cần semantics','ChỉownerlàđủkhôngcầnSLA','ChỉSLAthờigiankhôngcầnqualityrule'],
['Anomaly thay mọi constraint deterministic','Rules chỉ quan sát job status không kiểm data','Mọi anomaly luôn hard-fail dù chưa review'],
['Chỉ checkpoint với model registry','Chỉoutputdatasetvàalertchannel','ChỉschemafieldvàcloudIAMrole'],
['Info:logrồiluônpublish','Warningnhẹvàkhôngcóowner','Tắtschemacheckđểtránhstopdownstream'],
['Actual table sau build model như generic test','Chỉ availability endpoint SQL','Chỉ CPU memory database thay expected data'],
['Trộnweekdayvàweekendvàomộtbaselinekhôngseasonality','So vớingàysalelớnnhấtdùthứHai thường','Chỉdùngngàyhômquabấtkểchu kỳ tuần'],
['Chỉsốfilekhôngxemnộidungrỗng','Chỉrowcountmàkhôngđộdàitoken/ngônngữ','ChỉAPIstatuscủaparser'],
['Chỉanswertextkhôngrun/sourceversion','ChỉuserIDkhôngpipelineversion','Chỉmodelnamechungkhôngindex/chunker/parserversion'],
['Aiđangtrựcincidentnhưownershiplineage','Lầnchạynàotạoratablelỗinhưrunlineage','Chỉbảngnàonuôibảngnàyởcấpasset'],
['Run,PromptvàModel','Job,EndpointvàTenant','Dataset,AlertvàCredential'],
['Chỉtăngsốchartđẹpmàkhôngaction','Thaymetricbằngdanh sách owner','ChỉtargetSLOkhôngcurrentSLI/impact'],
['Nhiềualertluôntăngniềmtinbấtkểprecision','Precisionthấpchứngminhkhôngcófalsenegative','Chỉthêmthresholdnhạyhơnmàkhôngcontext/runbook'],
],
'p2-t2-d13':[
['LớpgovernancevìmọiMLtoolđềulàRBAC','Lớpcompute chỉ vì model chạyGPU','LớpdatachỉvìcótênStore'],
['Hardcodeconnectionstrings để tránh config race','Cho mọi service ghi cùng object khôngversion','Deploythủcôngđểkiểmsoátmỗilầnghi'],
['Gộptrainingvàinferencecùngquotađểchia sẻmọilỗi','Cho phép batch hút hếtresourcecriticalpath','ChỉretryliêntụckhitraininglàmservingđóiGPU'],
['Producerphảibiếtmọiimplementationconsumer','Mỗiconsumermớibuộcsửatoànbộproducer','Bỏeventcontractvìđãcóbroker'],
['Chỉlogtổnglatencykhôngspancomponent','ChỉGPU-UtilthaymọiE2Etrace','Chỉsốrequestthànhcôngkhôngduration'],
['Chỉ tênmodelchungkhôngversion','Chỉtimestampkhôngartifactidentity','ChỉgitSHAkhôngbiếtmodelđãload'],
['Lưutoànbộrawinputmặcđịnhvàgọilàprivacy-safe','Bỏhẳnđịnhdanhinputnênkhôngđốichiếuđược','Chỉghioutputhashvàkhẳngđịnhđủinputaudit'],
['ChỉproviderđịnhnghĩaAPIrồikhôngkiểmconsumer','Mỗiconsumerđoáninterfacekhôngcontracttest','ChỉkiểmHTTP200màkhôngexpectedinterface'],
['Chỉmockmọiexternalservicenênkhôngpháthiệnsaiintegration','Chỉunitfunctiontestthayrealdependencies','ChỉđặttênPostgrestrongfixturekhôngchạyDBthật'],
['Chỉsuccesspathđủđảmbảotimeout/retry','Chỉtestoutputđúngmàkhôngfailurehandling','Chỉloadtesthappypaththayinjectfailure'],
['JaegerđểbiếtđúngtừngPythonhotfunctionmàkhôngCPUprofiler','EXPLAINANALYZEđểprofilemọihàmPython','tracemallocchỉvìCPUhotspotđồngnghĩamemoryleak'],
['cProfilechỉđếmCPUtimekhôngmemoryallocation','tcđểxemallocationtừngdòngPython','EXPLAINANALYZEđểxemtấtcảPythonobject'],
['ChỉtăngCPUappmàkhôngxemplanSQL','Chỉpy-spyđểsuyraindexmissingtrongDB','ChỉgiảmLLMmax_tokensdùbottleneckquerySQL'],
['Mộtmeanđủđạidiệnmọitailrequest','ChỉP50đủvìp95/p99khôngảnhhưởngSLO','PercentiletheoservicethaytoànbộE2Etracing'],
['Chỉdựatrínhớngườirelease','Chỉkiểmmộtlầnlúcbắtđầudựán','Chỉđánhdấusaukhicósựcố'],
['Hủyngaymọirequestđangxửlýkhipodstop','Chỉnhậnrequestmớimàkhôngdrainrequestcũ','Chỉghihealthchecknhưngkhônghandlein-flight'],
['Chỉchạyđượctrênmáytácgiả','ChỉcodestyleđẹpnhưngkhôngAPIcontract','Chỉframeworkmớinhấtkhôngdocs/SLA'],
]}
FIX['p2-t2-d12']=[
['Job success bảo đảm semantics/đơn vị dữ liệu đúng','Tăng CPU worker đủ để sửa đơn vị price','Chỉ model update mới có thể làm business number sai'],
['Chỉ thời điểm raw ingest dù serving chưa publish','Chỉ timestamp job khởi động','Chỉ API uptime thay tuổi dữ liệu'],
['Chỉ HTTP status 200 là đủ','Chỉ process exit code 0','Chỉ số retry job mà không đếm record'],
['Mọi drift đều chứng minh corruption phải hard-fail','Campaign không thể làm ratio category thay đổi','Drift chỉ cần ngưỡng cố định không cần business context'],
['Thêm cột optional không đổi field cũ','Thêm mô tả field mà không đổi dữ liệu','Thêm metadata lineage không đổi required schema'],
['Chỉ kiểu dữ liệu đủ, không cần semantics','Chỉ owner là đủ không cần SLA','Chỉ SLA thời gian không cần quality rule'],
['Anomaly thay mọi constraint deterministic','Rules chỉ quan sát job status không kiểm data','Mọi anomaly luôn hard-fail dù chưa review'],
['Chỉ checkpoint với model registry','Chỉ output dataset và alert channel','Chỉ schema field và cloud IAM role'],
['Info: log rồi luôn publish','Warning nhẹ và không có owner','Tắt schema check để tránh stop downstream'],
['Actual table sau build model như generic test','Chỉ availability endpoint SQL','Chỉ CPU memory database thay expected data'],
['Trộn weekday và weekend vào một baseline không seasonality','So với ngày sale lớn nhất dù thứ Hai thường','Chỉ dùng ngày hôm qua bất kể chu kỳ tuần'],
['Chỉ số file không xem nội dung rỗng','Chỉ row count mà không độ dài token/ngôn ngữ','Chỉ API status của parser'],
['Chỉ answer text không run/source version','Chỉ user ID không pipeline version','Chỉ model name chung không index/chunker/parser version'],
['Ai đang trực incident như ownership lineage','Lần chạy nào tạo ra table lỗi như run lineage','Chỉ bảng nào nuôi bảng này ở cấp asset'],
['Run, Prompt và Model','Job, Endpoint và Tenant','Dataset, Alert và Credential'],
['Chỉ tăng số chart đẹp mà không action','Thay metric bằng danh sách owner','Chỉ target SLO không current SLI/impact'],
['Nhiều alert luôn tăng niềm tin bất kể precision','Precision thấp chứng minh không có false negative','Chỉ thêm threshold nhạy hơn mà không context/runbook'],
]
FIX['p2-t2-d13']=[
['Lớp governance vì mọi ML tool đều là RBAC','Lớp compute chỉ vì model chạy GPU','Lớp data chỉ vì có tên Store'],
['Hardcode connection strings để tránh config race','Cho mọi service ghi cùng object không version','Deploy thủ công để kiểm soát mỗi lần ghi'],
['Gộp training và inference cùng quota để chia sẻ mọi lỗi','Cho phép batch hút hết resource critical path','Chỉ retry liên tục khi training làm serving đói GPU'],
['Producer phải biết mọi implementation consumer','Mỗi consumer mới buộc sửa toàn bộ producer','Bỏ event contract vì đã có broker'],
['Chỉ log tổng latency không span component','Chỉ GPU-Util thay mọi E2E trace','Chỉ số request thành công không duration'],
['Chỉ tên model chung không version','Chỉ timestamp không artifact identity','Chỉ git SHA không biết model đã load'],
['Lưu toàn bộ raw input mặc định và gọi là privacy-safe','Bỏ hẳn định danh input nên không đối chiếu được','Chỉ ghi output hash và khẳng định đủ input audit'],
['Chỉ provider định nghĩa API rồi không kiểm consumer','Mỗi consumer đoán interface không contract test','Chỉ kiểm HTTP 200 mà không expected interface'],
['Chỉ mock mọi external service nên không phát hiện sai integration','Chỉ unit function test thay real dependencies','Chỉ đặt tên Postgres trong fixture không chạy DB thật'],
['Chỉ success path đủ đảm bảo timeout/retry','Chỉ test output đúng mà không failure handling','Chỉ load test happy path thay inject failure'],
['Jaeger để biết đúng từng Python hot function mà không CPU profiler','EXPLAIN ANALYZE để profile mọi hàm Python','tracemalloc chỉ vì CPU hotspot đồng nghĩa memory leak'],
['cProfile chỉ đếm CPU time không memory allocation','tc để xem allocation từng dòng Python','EXPLAIN ANALYZE để xem tất cả Python object'],
['Chỉ tăng CPU app mà không xem plan SQL','Chỉ py-spy để suy ra index missing trong DB','Chỉ giảm LLM max_tokens dù bottleneck query SQL'],
['Một mean đủ đại diện mọi tail request','Chỉ P50 đủ vì p95/p99 không ảnh hưởng SLO','Percentile theo service thay toàn bộ E2E tracing'],
['Chỉ dựa trí nhớ người release','Chỉ kiểm một lần lúc bắt đầu dự án','Chỉ đánh dấu sau khi có sự cố'],
['Hủy ngay mọi request đang xử lý khi pod stop','Chỉ nhận request mới mà không drain request cũ','Chỉ ghi health check nhưng không handle in-flight'],
['Chỉ chạy được trên máy tác giả','Chỉ code style đẹp nhưng không API contract','Chỉ framework mới nhất không docs/SLA'],
]
FIX['p2-t2-d11'][2]=['Tối đa goodput bằng tăng mọi request dù vi phạm SLO','Chỉ tokens/s ở saturation không ràng buộc latency','Chỉ số GPU bật mà không đo đầu ra']
FIX['p2-t2-d11'][4]=['Reserved dài hạn dù duty cycle thấp và biến động','Mua full cluster trước khi có nhu cầu ổn định','Giữ VM 24/7 để chờ workload thưa']
FIX['p2-t2-d11'][8]=['GPU-Util đo trực tiếp tỷ lệ peak FLOPs đạt được','Có kernel chạy đồng nghĩa Tensor Core đã bão hòa','100% time-active đủ để quyết định mua thêm GPU']
FIX['p2-t2-d11'][9]=['Chỉ peak TFLOPs dù workload bandwidth-bound','Chỉ clock CPU orchestrator','Chỉ số GPU không xét bandwidth mỗi GPU']
FIX['p2-t2-d11'][10]=['10 request/s vì mọi request đều được tính throughput','7 request/s vì đó là số vi phạm SLO','13 request/s vì cộng cả throughput và đạt SLO']
FIX['p2-t2-d11'][11]=['Cold start không bị tính phí vì chưa có output token','Scale-to-zero luôn rẻ hơn ở duty cycle 100%','Keep-warm không bao giờ có năng lượng idle']
FIX['p2-t2-d11'][12]=['MIG chỉ chia thời gian không phân vùng memory','Time-slicing luôn có isolation mạnh hơn hardware partition','MIG và MPS đều bảo đảm memory riêng như nhau']
FIX['p2-t2-d11'][15]=['Tự optimize model weights thay billing schema','Bảo đảm mọi provider có cùng giá token','Thay toàn tagging/ownership policy bằng một file bill']
FIX['p2-t2-d11'][16]=['Chargeback ngay dù tag coverage còn thiếu','Bỏ showback vì tổng bill đủ biết team gây chi phí','Chỉ chia đều tổng bill mà không đo xem team nào dùng']
b=json.loads((ROOT/'data/questions/drafts/expand-b-04.json').read_text(encoding='utf8'))
for q in b['questions']:
    correct=next(o['text'] for o in q['options'] if o['id']==q['correct_answer']);ix=int(q['id'][-2:])-1
    ts=[correct]+FIX[q['topic']][ix];n=(int(q['topic'][-2:])+ix+1)%4;ts=ts[n:]+ts[:n]
    q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(ts)];q['correct_answer']=chr(97+ts.index(correct));q['revision']=2
REPLACE={
'p2-t2-d10-x02':(47,'Context editing khác compaction ở cách tác động lịch sử thế nào?','Xóa khối cũ thay vì tóm tắt lịch sử','Cả hai chỉ tóm tắt mà không bao giờ xóa','Cả hai bảo đảm giữ nguyên mọi thông tin','Compaction chỉ đổi tool name còn editing đổi model','Context editing xóa tool/thinking block cũ; compaction tóm tắt nên có thể mất thông tin dù bản tóm tắt trông đầy đủ.'),
'p2-t2-d10-x11':(48,'Khi API trả nhiều content block gồm compaction, client nên lưu response thế nào cho lượt tiếp theo?','Giữ nguyên mọi content block cần thiết trong response.content','Chỉ rút text block rồi append chuỗi text','Chỉ lưu final answer string và bỏ block đặc biệt','Chỉ tăng max context để không cần lưu compaction block','Nếu client chỉ append text, compaction block bị mất âm thầm và request sau không dùng được trạng thái nén.'),
'p2-t2-d11-x03':(31,'Vì sao tách pool prefill/decode có thể giảm chi phí cho workload phù hợp?','Right-size riêng compute-bound prefill và memory-bound decode','Hai phase luôn có cùng bottleneck nên tách chỉ để đổi tên','KV transfer không bao giờ có overhead nên mọi deployment đều phải tách','Chỉ tăng số GPU mà không thay phân bổ tài nguyên','Prefill thiên compute, decode thiên bandwidth; pool riêng có thể right-size từng phase nhưng cần tính overhead chuyển KV.'),
'p2-t2-d11-x08':(33,'Một optimization tăng tốc decode có luôn làm chi phí/token giảm không?','Không; ROI phụ thuộc chế độ tải và phải đo trước/sau','Có; throughput tăng bất kỳ luôn làm total cost giảm cùng tỷ lệ','Có; speculative decoding không phụ thuộc acceptance rate','Không cần đo nếu optimization có benchmark peak tốt','Mỗi lever có vùng tải phù hợp; speculative decoding có thể hữu ích latency-bound nhưng làm cost tăng khi throughput đã bão hòa.'),
'p2-t2-d12-x07':(20,'Z-score đơn giản phù hợp nhất với loại metric nào?','Ổn định, lịch sử đủ dài và phân phối gần bình thường','Seasonality mạnh không cần baseline theo mùa','Nhiều outlier lịch sử và không cần robust statistic','Campaign đột biến mà không có annotation','Z-score là điểm bắt đầu cho metric ổn định; seasonality/outlier/campaign có thể làm baseline sai và alert cần review.'),
'p2-t2-d13-x06':(15,'Backup tồn tại nhưng chưa thử restore còn thiếu điều kiện production readiness nào?','Xác minh thực tế có thể phục hồi từ backup','Chỉ đổi tên bucket để chứng minh có bản sao','Chỉ kiểm file metadata tồn tại thay toàn bộ restore','Chỉ tăng số snapshot mà không thử dùng','Backup/restore tested nằm trong readiness; có backup chưa chứng minh artifact và quy trình phục hồi hoạt động.'),
'p2-t2-d13-x07':(15,'Log structured JSON giúp hệ observability xử lý log theo hướng nào?','Tách các field nhất quán để lọc và liên kết sự kiện','Chỉ lưu một chuỗi tự do không field nào','Thay toàn bộ trace và metric bằng log text','Bảo đảm mọi dữ liệu nhạy cảm tự bị xóa','Structured logging tạo record có field thay text tự do, hỗ trợ pipeline quan sát nhất quán; vẫn cần kiểm nội dung log riêng.'),
'p2-t2-d13-x08':(15,'Retry với exponential backoff khác retry liên tục ngay lập tức ở điểm nào?','Tăng khoảng chờ giữa các lần thử để tránh dồn tải khi dependency lỗi','Luôn retry không giới hạn và không có khoảng nghỉ','Bỏ qua mọi lỗi vĩnh viễn và luôn báo thành công','Chỉ thay thứ tự log không đổi nhịp gọi','Exponential backoff giãn các lần retry thay gọi dồn khi dependency chưa phục hồi; là mục reliability readiness.'),
'p2-t2-d13-x10':(13,'Synchronous DB calls trong hot path và thiếu connection pooling cần được xem là gì khi profiling?','Các ứng viên bottleneck tích hợp cần đo và tối ưu','Chỉ vấn đề code style không ảnh hưởng latency','Bằng chứng phải tăng model context trước tiên','Lý do bỏ database khỏi trace vì không phải LLM','Profiling checklist nêu synchronous DB call và missing connection pooling là nguồn bottleneck bên cạnh load model và vector search.'),
}
for q in b['questions']:
    if q['id'] in REPLACE:
        page,prompt,correct,d1,d2,d3,why=REPLACE[q['id']]
        q['question']=prompt;q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate([correct,d1,d2,d3])];q['correct_answer']='a';q['explanation']=why
        q['source_reference'][0]['pdf_page']=page;q['source_reference'][0]['locator']=f'Physical PDF page {page}'
curated={
'p2-t2-d10-x02':['Xóa khối cũ thay vì tóm tắt lịch sử','Cả hai đều tạo bản tóm tắt rồi giữ nguyên toàn bộ lịch sử gốc','Editing tóm tắt lịch sử còn compaction chỉ xóa tool block'],
'p2-t2-d11-x16':['Chuẩn hóa cost/usage billing về schema chung','Chỉ chuyển mọi bill sang cùng tiền tệ mà không chuẩn hóa field','Chỉ gộp tổng tiền mỗi provider và bỏ usage dimensions'],
'p2-t2-d12-x01':['Hoàn tất tiến trình không chứng minh dữ liệu đúng','Schema giữ nguyên kiểu số thì đơn vị tiền tệ cũng được bảo đảm đúng','Freshness đạt SLO là đủ để chứng minh mọi giá trị có nghĩa đúng'],
'p2-t2-d12-x08':['Data asset và expectation suite','Expectation suite với alert action, không chọn data asset','Checkpoint với alert channel, không gắn dữ liệu với rules'],
'p2-t2-d12-x10':['Logic SQL với mock input và expected output','Chỉ unique/not_null trên bảng thực tế sau build','Chỉ freshness của source trước khi chạy model SQL'],
'p2-t2-d13-x02':['Immutable events và event sourcing','Cho nhiều writer ghi đè trực tiếp cùng state không kiểm version','Đọc state một lần rồi cho mọi writer ghi lại snapshot cũ'],
'p2-t2-d13-x08':['Tăng khoảng chờ giữa các lần thử để tránh dồn tải khi dependency lỗi','Giữ khoảng nghỉ cố định bằng nhau giữa mọi lần thử','Giảm dần khoảng nghỉ sau mỗi lỗi để retry nhanh hơn'],
'p2-t2-d13-x10':['Các ứng viên bottleneck tích hợp cần đo và tối ưu','Chỉ đo thời gian query sau khi đã lấy connection, bỏ thời gian chờ pool','Chỉ đo CPU của app rồi suy ra mọi I/O database đều đủ nhanh'],
'p2-t2-d13-x13':['EXPLAIN ANALYZE','Chỉ xem tổng connection count mà không xem execution plan','Chỉ dùng CPU profiler của app để kết luận access path của database']}
for q in b['questions']:
 if q['id'] in curated:
  q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(curated[q['id']])];q['correct_answer']='a';q['revision']=3
 if q['id']=='p2-t2-d10-x03':
  q.update(question='Health check của MCP server cần xác minh version, capabilities và identity. Phản hồi nào cung cấp bằng chứng phù hợp hơn chỉ HTTP 200?',correct_answer='a',revision=3,explanation='server/discover trả version, capabilities và identity; mã HTTP thành công đơn thuần chưa xác minh tương thích giao thức và danh tính server.')
  q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(['Kết quả RPC server/discover','Trang HTTP tĩnh luôn trả 200 dù MCP handler chưa sẵn sàng','Chỉ TCP connection thành công tới cổng proxy'])]
  q['source_reference'][0].update(pdf_page=13,locator='Physical PDF page 13; protocol-aware health check server/discover')
 if q['id']=='p2-t2-d13-x14':
  q.update(question='Một request chạy song song Feature Store, vector search và LLM inference, rồi mới tổng hợp kết quả. Tối ưu một nhánh vốn kết thúc rất sớm có chắc giảm latency tổng không?',correct_answer='a',revision=3,explanation='Các lời gọi chạy song song; nhánh chậm nhất và các bước nối tiếp quyết định đường chờ, nên giảm nhánh không chi phối có thể không giảm thời gian trả kết quả.')
  q['options']=[{'id':chr(97+i),'text':t} for i,t in enumerate(['Không; cần xác định nhánh chi phối đường chờ của request','Có; latency tổng luôn là tổng thời gian mọi nhánh dù chạy song song','Có; nhánh nhanh nhất luôn quyết định lúc toàn bộ kết quả sẵn sàng'])]
  q['source_reference'][0].update(pdf_page=9,locator='Physical PDF page 9; parallel component calls before guardrails and response')
(ROOT/'data/questions/drafts/expand-b-04.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf8')
print('b04 curated')
