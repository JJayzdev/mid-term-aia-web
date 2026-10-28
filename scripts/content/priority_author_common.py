import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CAT={d['document_id']:d for d in json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))['documents']}
BATCH=[]
def q(doc,key,pages,stem,answer,explanation,options=None,fmt='single_choice',focus=None,calc=False,context=None,formula=None):
 d=CAT[doc]; sources=[]
 for ref in pages:
  dd,page=(doc,ref) if isinstance(ref,int) else ref
  sd=CAT[dd];sources.append(dict(document_id=dd,sha256=sd['sha256'],pdf_page=page,title=sd['title'],locator=f'Physical PDF page {page}',verification='needs_review'))
 item=dict(id=f'{doc}-priority-{key}',revision=1,author_id='priority-question-engineer',phase=d['phase'],track=d['track'],day=d['day'],topic=d['topic'],taxonomy_status='verified',question_type='scenario' if context else ('true_false' if fmt=='boolean' else 'short_answer' if fmt=='rubric' else fmt),answer_format=fmt,difficulty='medium',cognitive_level='apply' if calc or context or fmt=='ordering' else 'understand',question=stem,correct_answer=answer,explanation=explanation,source_reference=sources,status='pending_review',review_notes=['New priority practice; independently verify exact revision and source pages before release.'])
 if options: item['options']=[dict(id=chr(97+i),text=t) for i,t in enumerate(options)];item['shuffle_options']=True
 if focus:item['focus_topics']=[focus] if isinstance(focus,str) else focus
 if calc:item['calculation']=True
 if context:item['context']=context
 if formula:item['formula_reference']=dict(zip(['title','formula','symbols','conditions','example','common_mistakes'],formula))
 BATCH.append(item);return item

def mc(doc,key,pages,stem,correct,wrong1,wrong2,explanation,**kw):return q(doc,key,pages,stem,'a',explanation,[correct,wrong1,wrong2],**kw)
def match(doc,key,pages,stem,pairs,explanation,**kw):
 item=q(doc,key,pages,stem,{f'l{i+1}':chr(97+i) for i in range(len(pairs))},explanation,[x[1] for x in pairs],fmt='matching',**kw)
 item['matching_items']=[dict(id=f'l{i+1}',text=p[0],explanation=p[2]) for i,p in enumerate(pairs)];item['matching_reuse']=False;return item

def order(doc,key,pages,stem,steps,explanation,**kw):return q(doc,key,pages,stem,[chr(97+i) for i in range(len(steps))],explanation,steps,fmt='ordering',**kw)
def essay(doc,key,pages,stem,answer,explanation,criteria,**kw):
 item=q(doc,key,pages,stem,answer,explanation,fmt='rubric',**kw)
 item['rubric']=[dict(id=f'c{i+1}',description=c[0],weight=1/len(criteria),full_credit=c[1],partial_credit=c[2],no_credit=c[3]) for i,c in enumerate(criteria)];return item

def save(name):
 path=ROOT/f'data/questions/drafts/priority-{name}.json'
 path.write_text(json.dumps(dict(schema_version='1.0.0',bank_version='2026.10.28-priority-'+name,questions=BATCH),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(path,len(BATCH));BATCH.clear()
