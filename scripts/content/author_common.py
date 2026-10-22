"""Load shared authoring definitions without executing any bank writes."""
from pathlib import Path
_source=Path(__file__).with_name('author_pilot.py').read_text(encoding='utf-8')
exec(compile(_source[:_source.index("add('p1-d01'")],str(Path(__file__)),'exec'))
def save(name):
 bank={'schema_version':'1.0.0','bank_version':'2026.10.22.'+name,'questions':qs}
 for q in qs:
  if 'options' in q:
   n=(int(q['id'].split('-d')[-1].split('-')[0])+int(q['id'][-2:]))%len(q['options'])
   options=q['options'];options=options[n:]+options[:n];mapping={o['id']:chr(97+i) for i,o in enumerate(options)}
   for i,o in enumerate(options):o['id']=chr(97+i)
   q['options']=options;q['correct_answer']=[mapping[x] for x in q['correct_answer']] if isinstance(q['correct_answer'],list) else mapping[q['correct_answer']]
 path=ROOT/'data/questions/drafts'/f'{name}.json';path.write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8');print(name,len(qs))
def rubric_scenario(doc,page,question,context,answer,explanation,criteria):
 add(doc,page,'scenario',question,answer,explanation,context=context,rubric=[x[0] for x in criteria])
 for c,(_,full,partial,no) in zip(qs[-1]['rubric'],criteria):c.update(full_credit=full,partial_credit=partial,no_credit=no)
def extra_page(doc,page):
 d=docs[doc];qs[-1]['source_reference'].append({'document_id':doc,'sha256':d['sha256'],'pdf_page':page,'title':d['title'],'locator':f'Physical PDF page {page}','verification':'needs_review'})
