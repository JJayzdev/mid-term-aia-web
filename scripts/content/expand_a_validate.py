import json,pathlib,collections,re,hashlib
from jsonschema import Draft202012Validator
ROOT=pathlib.Path(__file__).resolve().parents[2];docs={d['document_id']:d for d in json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))['documents']};validator=Draft202012Validator(json.loads((ROOT/'docs/schemas/question-bank.schema.json').read_text(encoding='utf-8')));seen=set();summary=[];patterns=collections.Counter()
bad=re.compile(r'(trong (?:bài|slide|tài liệu|bảng|ví dụ)|theo (?:slide|tài liệu|bài giảng|bảng)|được minh họa|nguồn nêu|bài giảng cho biết)',re.I)
for path in sorted((ROOT/'data/questions/drafts').glob('expand-a-*.json')):
 bank=json.loads(path.read_text(encoding='utf-8'));validator.validate(bank);coverage=collections.defaultdict(set);counts=collections.Counter()
 for q in bank['questions']:
  assert q['id'] not in seen;seen.add(q['id']);assert q['author_id']=='question-engineer-a';assert '-x' in q['id'];assert q['status']=='pending_review';assert not bad.search(q['question']),(q['id'],q['question'])
  if 'options' in q:
   ids=[o['id'] for o in q['options']];assert len(ids)==len(set(ids));answers=q['correct_answer'] if isinstance(q['correct_answer'],list) else [q['correct_answer']];assert set(answers)<=set(ids)
   if q['answer_format']=='multiple_choice':patterns[f'{len(answers)}/{len(ids)}']+=1
  counts[q['topic']]+=1
  for ref in q['source_reference']:
   doc=docs[ref['document_id']];assert doc['sha256']==ref['sha256'];assert 1<=ref['pdf_page']<=doc['page_count'];coverage[doc['document_id']].add(ref['pdf_page'])
 summary.append({'batch':path.name,'questions':len(bank['questions']),'documents':dict(counts),'pages_per_document':{k:len(v) for k,v in coverage.items()}})
print(json.dumps({'questions':len(seen),'batches':summary,'multiple_choice_answer_patterns':dict(patterns)},ensure_ascii=True,indent=2))
