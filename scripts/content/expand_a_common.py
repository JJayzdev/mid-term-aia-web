"""Expansion authoring helpers. Only creates new pending-review draft banks."""
import json,pathlib,collections
from jsonschema import Draft202012Validator
ROOT=pathlib.Path(__file__).resolve().parents[2]
CAT=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));DOC={d['document_id']:d for d in CAT['documents']};QUESTIONS=[]
def item(doc,page,stem,choices,answer,why,kind='single_choice',context=None,level='understand'):
 if isinstance(answer,list) and kind=='single_choice':kind='multiple_choice'
 for phrase in [' trong taxonomy của bài',' theo slide',' theo bài',' được bài nêu',' trong bài',' theo ví dụ trợ giảng',' theo lộ trình trong bài',' theo khung lợi thế AI gợi ý',' được bài gợi ý']:
  stem=stem.replace(phrase,'')
 stem=stem.replace('theo nguyên tắc PAIR trong bài','theo nguyên tắc PAIR').replace('Theo phần tokenization, ','').replace(' theo phần scale','').replace(' theo ví dụ trợ giảng','').replace('Trong định nghĩa LLM của bài, ','Đối với LLM, ').replace('được bài giải thích theo thứ tự nào','có vai trò tương ứng theo thứ tự nào').replace('Hướng nào được khung lợi thế AI gợi ý','Hướng nào phù hợp nhất')
 replacements={'Mã màu của giao diện tool':'Ràng buộc số lượng token input của riêng model','Số lần release của provider':'Chỉ tên provider nhưng không mô tả kết quả/error của tool','Chỉ số dòng của file Python':'Chỉ độ dài chuỗi content, bỏ qua usage và nguyên nhân dừng','Chỉ tên biến client trong source code':'Chỉ tên model, bỏ qua token usage và stop reason','Chỉ độ dài system prompt bất kể output':'Chỉ giảm input tokens, không xét quality hoặc latency','Chỉ số lượng provider có trong code':'Chỉ tối đa số model được hỗ trợ, không xét kết quả từng call'}
 replacements.update({'Chỉ thay logo provider':'Chỉ cấu hình happy-path connection, bỏ qua lỗi và retry','Chỉ tên model cho deck executive':'Chỉ latency của một lần gọi thành công, không xét lỗi','Sai ngôn ngữ lập trình so với sai font chữ':'Sai model architecture so với sai tokenizer, bất kể nhu cầu người dùng','Chỉ tên hãng GPU chạy model':'Chỉ công bố tên model mà không giải thích giới hạn hoặc quyền override','Chỉ số lượng slide pitch':'Chỉ tốc độ dựng prototype mà không xét dòng chi phí/giá trị','Chỉ kích thước file model':'Chỉ số phiên bản model, không xét trust và khả năng chấp nhận sai','Chỉ số phiên bản SDK mà engineer dùng':'Chỉ ngân sách GPU, bỏ qua mức hiểu AI của người dùng'})
 replacements.update({'Chỉ đổi màu giao diện citation':'Chỉ tăng top-k nhưng vẫn inject các mảnh rời không có ngữ cảnh cha','Số dòng của tài liệu nguồn':'Dot product của vector chưa chuẩn hóa, để norm vẫn chi phối','Chỉ độ dài chuỗi văn bản':'Tổng norm của hai vector, không xét hướng tương đối','Chỉ DNS routing error':'Chỉ tốc độ thực thi riêng lẻ của từng tool','Chỉ data serialization':'Chỉ định dạng payload truyền giữa các tool','Chỉ model quantization':'Chỉ precision của weights bất kể role và context','Không thể đặt tên model provider':'Không thể tính usage của từng query vì thiếu token count','Không thể biết có bao nhiêu câu trong question':'Không thể chọn BM25 hay dense chỉ từ việc thiếu ngày tài liệu','Chỉ số dòng của file Python':'Chỉ độ dài content, bỏ qua usage và stop reason'})
 replacements.update({'Chỉ số container image tags đã phát hành':'Số replica cố định theo cấu hình ban đầu, không xét request đang chờ','Chỉ lỗi availability của hệ thống':'Không có harm nếu output chưa thay đổi việc phân bổ cơ hội hay nguồn lực'})
 replacements.update({'Chỉ đo output nào có độ dài giống nhau':'Chỉ đo tỷ lệ agreement thô, không điều chỉnh phần có thể do chance','Chỉ model knowledge cutoff':'Verbosity bias do một answer dài hơn answer còn lại','Chỉ việc ground-truth label bị thiếu':'Self-preference bias khi một answer do model cùng family tạo ra','Chỉ giá/token của judge để suy ra độ chính xác':'Chỉ so với một LLM judge khác, không có human labels làm đối chiếu','Chỉ cần cộng thêm tên provider vào estimate':'Cộng lại token cost của call chính đã được tính đầy đủ để tăng tổng budget','Chỉ giảm output length là đã tính đủ hidden cost':'Chỉ tính happy-path call rồi xem retry/guardrail là đã nằm sẵn trong token estimate'})
 if choices:choices=[replacements.get(s,s) for s in choices]
 stem=stem.replace(' được minh họa','').replace(' ?','?')
 d=DOC[doc];n=sum(q['topic']==doc for q in QUESTIONS)+1;fmt={'true_false':'boolean','scenario':'single_choice'}.get(kind,kind)
 q={'id':f'{doc}-x{n:02}','revision':1,'author_id':'question-engineer-a','phase':d['phase'],'track':d['track'],'day':doc,'topic':doc,'taxonomy_status':'verified','question_type':kind,'answer_format':fmt,'difficulty':'medium','cognitive_level':level,'question':stem,'correct_answer':answer,'explanation':why,'source_reference':[{'document_id':doc,'sha256':d['sha256'],'pdf_page':page,'title':d['title'],'locator':f'Physical PDF page {page}','verification':'needs_review'}],'status':'pending_review','review_notes':['New expansion item; requires independent review against cited original PDF page. Curricular grouping follows root folder/filename policy.']}
 if choices:
  options=[{'id':chr(97+i),'text':s} for i,s in enumerate(choices)];shift=n%len(options);options=options[shift:]+options[:shift];mapping={o['id']:chr(97+i) for i,o in enumerate(options)}
  for i,o in enumerate(options):o['id']=chr(97+i)
  q.update(options=options,shuffle_options=True,correct_answer=[mapping[x] for x in answer] if isinstance(answer,list) else mapping[answer])
 if context:q['context']=context;q['cognitive_level']='apply'
 overrides={'p1-d01-x10':'Trong câu “Con mèo ngồi trên bàn. Nó rất đáng yêu.”, self-attention giúp model xử lý từ “Nó” như thế nào?','p1-d02-x06':'Trường Boundary của Problem Card có chức năng gì?','p1-d03-x07':'Tool tìm vé timeout hai lần. Cách phản hồi nào phù hợp để hệ thống suy giảm chức năng an toàn?'}
 if q['id'] in overrides:q['question']=overrides[q['id']];q['revision']=2
 if q['id']=='p1-d01-x04':
  q['question']='Streaming từng khâu của voice pipeline giảm độ trễ cảm nhận bằng cơ chế nào?';q['revision']=2
  next(o for o in q['options'] if o['id']==q['correct_answer'])['text']='Chuyển phần output vừa sinh sang khâu sau trước khi toàn bộ câu hoàn thành'
 QUESTIONS.append(q)
def save(name):
 bank={'schema_version':'1.0.0','bank_version':'2026.10.22.expansion-a-'+name,'questions':QUESTIONS};Draft202012Validator(json.loads((ROOT/'docs/schemas/question-bank.schema.json').read_text(encoding='utf-8'))).validate(bank)
 old=json.loads((ROOT/'data/questions/approved/bank.json').read_text(encoding='utf-8'));assert not {q['id'] for q in old['questions']} & {q['id'] for q in QUESTIONS}
 p=ROOT/'data/questions/drafts'/f'expand-a-{name}.json';p.write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8');print(p,len(QUESTIONS))
