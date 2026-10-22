import json,pathlib
p=pathlib.Path('data/questions/drafts/track2.json');d=json.loads(p.read_text(encoding='utf-8'))
for q in d['questions']:
 if q['id']=='p2-t2-d03-q01':
  q.update(question='Một use case được chấm đa số tiêu chí Agentic Fit chỉ ở mức 1–2/5. Theo slide nên bắt đầu thế nào?',explanation='Lưu ý cuối trang 11 khuyên bắt đầu bằng chatbot hoặc workflow đơn giản khi đa số tiêu chí ở mức thấp.',revision=2)
  correct=q['correct_answer']
  for o,t in zip([o for o in q['options'] if o['id']!=correct],['Tăng số agent chuyên gia trước khi đo baseline','Tăng số vòng reasoning để bù điểm Agentic Fit thấp','Bắt buộc thêm long-term memory để biến bài toán thành agent']):o['text']=t
  next(o for o in q['options'] if o['id']==correct)['text']='Bắt đầu bằng chatbot hoặc workflow đơn giản'
 if q['id']=='p2-t2-d11-q01':
  old=next((o for o in q['options'] if o['text'].startswith('Inference không')),None)
  if old:old['text']='Chỉ so chi phí mỗi request mà không kiểm soát độ dài output hoặc workload'
  q['revision']=2
 if q['id']=='p2-t2-d13-q02':
  for o in q['options']:
   if o['text'].startswith('Team vận hành'):o['text']='Chỉ chụp schema hiện tại của provider và xem mọi thay đổi schema đều tương thích'
   if o['text'].startswith('Chỉ người dùng'):o['text']='Provider tự định nghĩa interface mới mà không đối chiếu kỳ vọng của consumer'
  q['revision']=2
words={'vectorDB':'vector DB','embeddingversion':'embedding version','point-in-time':'point-in-time','độtrễ':'độ trễ','outputlength':'output length','cost-sensitive':'cost-sensitive','vượt100M':'vượt 100M','hơn100':'hơn 100','phụthuộc':'phụ thuộc','top-k':'top-k','full-time':'full-time','least-privilege':'least-privilege','hay xóa':'hay xóa','Source':'Source','request/s':'request/s','requests/s':'requests/s','prefill':'prefill','batching':'batching','tailusage':'tail usage','data version':'data version','metrics/artifacts':'metrics/artifacts','lifecycle':'lifecycle','Registry quản lý':'Registry quản lý','contextbundle':'context bundle','systemprompt':'system prompt','modelversion':'model version','promptversion':'prompt version','guardrail/tool':'guardrail/tool','labelpointer':'label pointer','append-only':'append-only','toolname':'tool name','ởL7':'ở L7','JSONbody':'JSON body','bodyJSON':'body JSON','JSON body':'JSON body','rate-limit/tính':'rate-limit/tính','authz mỗi call':'authz mỗi call','per-call':'per-call','cachecatalog':'cache catalog','request cần':'request cần','$/1Mtoken':'$/1M token','1Mtoken':'1M token','checkpointstrategy':'checkpoint strategy','spottraining':'spot training','longtraining':'long training','long training':'long training','testtrước':'test trước','testresume':'test resume','flowtrước':'flow trước','$/GPU-hour':'$/GPU-hour','rowcount':'row count','knownproblems':'known problems','unknownpatterns':'unknown patterns','hardfail':'hard fail','deterministiclowrisk':'deterministic low-risk','risk low':'risk low','latencybreakdown':'latency breakdown','token cost':'token cost','modelversion':'model version','Token cost':'Token cost','input/outputhash':'input/output hash','schema/version':'schema/version','expectedinterface':'expected interface','blockmerge':'block merge','Goldenpath':'Golden path','goldenpath':'golden path','failurepath':'failure path','faultinjection':'fault injection','killpods':'kill pods','corruptdata':'corrupt data','verifygracefuldegradation':'verify graceful degradation','Inject latency/killpod':'Inject latency/kill pod','corruptinput':'corrupt input','errorhandling/timeout/retry':'error handling/timeout/retry','compiletime':'compile time','sau deployment':'sau deployment','modelA':'model A','modelB':'model B','embedding model':'embedding model','standby':'standby','RTO/RPO':'RTO/RPO','hai poolGPU':'hai pool GPU','trên5phút':'trên 5 phút','gần0':'gần 0','trongRAM':'trong RAM','taskallowlist':'task allowlist','checkpointstrategy':'checkpoint strategy','spot training':'spot training','consumer-driven':'consumer-driven','cost/job':'cost/job','history/replay':'history/replay','requestaudittrail':'request audit trail','trênSLA':'trên SLA','soSLA':'so SLA','schema vẫn':'schema vẫn','columnname':'column name','dataflow':'data flow','contracttesting':'contract testing','APIcontract':'API contract','runtime':'runtime'}
def clean(v):
 if isinstance(v,str):
  for old,new in sorted(words.items(),key=lambda x:-len(x[0])):v=v.replace(old,new)
  return v
 if isinstance(v,list):return [clean(x) for x in v]
 if isinstance(v,dict):return {k:(x if k in ['id','document_id','sha256','topic','day','author_id','question_type','answer_format','status','verification','taxonomy_status'] else clean(x)) for k,x in v.items()}
 return v
p.write_text(json.dumps(clean(d),ensure_ascii=False,indent=2),encoding='utf-8');print('Track2 revision/proofreading complete')
