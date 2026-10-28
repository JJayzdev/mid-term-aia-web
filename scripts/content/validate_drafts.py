import pathlib,json,collections
from jsonschema import Draft202012Validator, FormatChecker
root=pathlib.Path(__file__).resolve().parents[2];catalog=json.loads((root/'content/catalog.json').read_text(encoding='utf-8'));docs={d['document_id']:d for d in catalog['documents']};validator=Draft202012Validator(json.loads((root/'docs/schemas/question-bank.schema.json').read_text(encoding='utf-8')), format_checker=FormatChecker())
topics={t['id']:t for t in catalog['topics']}
seen=set();counts=collections.Counter();types=collections.Counter();pages=collections.defaultdict(set);banks=[]
for p in sorted((root/'data/questions/drafts').glob('*.json')):
 bank=json.loads(p.read_text(encoding='utf-8'));validator.validate(bank);banks.append({'path':p.relative_to(root).as_posix(),'questions':len(bank['questions'])})
 for q in bank['questions']:
  assert q['id'] not in seen,q['id'];seen.add(q['id']);types[q['question_type']]+=1
  assert q['status']=='pending_review';assert q['taxonomy_status']=='verified'
  topic=topics[q['topic']];assert all(q[k]==topic[k] for k in ('phase','track','day')),q['id'];assert any(ref['document_id'] in topic['document_ids'] for ref in q['source_reference']),q['id']
  urls=[source['url'] for source in q.get('supplemental_sources',[])];assert len(set(urls))==len(urls),q['id']
  if 'options' in q:
   opts={o['id'] for o in q['options']};assert len(opts)==len(q['options']),q['id']
   if q['answer_format']=='matching':
    left=[o['id'] for o in q['matching_items']];mapping=q['correct_answer']
    assert len(left)==len(set(left)) and set(mapping)==set(left),q['id']
    assert set(mapping.values())<=opts,q['id']
    assert q.get('matching_reuse',False) or (len(left)==len(opts) and len(set(mapping.values()))==len(mapping)),q['id']
   elif q['answer_format']=='ordering':
    orders=[q['correct_answer']]+q.get('accepted_orders',[])
    assert all(len(order)==len(opts) and set(order)==opts for order in orders),q['id']
    assert len(set(tuple(order) for order in orders))==len(orders),q['id']
   else:
    answers=q['correct_answer'] if isinstance(q['correct_answer'],list) else [q['correct_answer']];assert set(answers)<=opts,q['id']
  if 'rubric' in q:assert abs(sum(c['weight'] for c in q['rubric'])-1)<1e-8
  for ref in q['source_reference']:
   d=docs[ref['document_id']];assert d['sha256']==ref['sha256'];assert 1<=ref['pdf_page']<=d['page_count'];assert ref['verification']=='needs_review';pages[d['document_id']].add(ref['pdf_page'])
  counts[q['source_reference'][0]['document_id']]+=1
report={'questions':len(seen),'documents_represented':len(counts),'question_types':dict(types),'banks':banks,'documents':[{'document_id':d['document_id'],'draft_question_count':counts[d['document_id']],'referenced_physical_pages':sorted(pages[d['document_id']]),'coverage_meaning':'Selected-page questions represent this document; not comprehensive concept coverage','approved_count':'Determined independently by reviewer/promote workflow; drafts never imply approval'} for d in catalog['documents']]}
(root/'reports/ingestion/draft-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='documents'}))
