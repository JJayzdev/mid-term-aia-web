# -*- coding: utf-8 -*-
"""Write explicit reviewer decisions after manual reading and visual inspection.
This helper validates provenance; it does not choose which questions to approve.
"""
import json,hashlib,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def report(batch,approved_ids,findings,evidence,summary):
 bank=json.loads((ROOT/'data/questions/drafts'/f'expand-a-{batch:03}.json').read_text(encoding='utf8'))
 docs={d['document_id']:d for d in json.loads((ROOT/'content/catalog.json').read_text(encoding='utf8'))['documents']}
 assert set(approved_ids)|set(findings)=={q['id'] for q in bank['questions']}
 assert not(set(approved_ids)&set(findings))
 for doc in {s['document_id'] for q in bank['questions'] for s in q['source_reference']}:
  assert hashlib.sha256((ROOT/docs[doc]['relative_path']).read_bytes()).hexdigest()==docs[doc]['sha256']
 results=[]
 for q in bank['questions']:
  for s in q['source_reference']:assert s['sha256']==docs[s['document_id']]['sha256'] and 1<=s['pdf_page']<=docs[s['document_id']]['page_count']
  approved=q['id'] in approved_ids
  result={'id':q['id'],'revision':q['revision'],'decision':'approved' if approved else 'rejected','source_pages':[{'document_id':s['document_id'],'pdf_page':s['pdf_page']} for s in q['source_reference']],'notes':(["Manually read complete stem, context, options, correct answer and explanation; verified support against cited original PDF render and extracted text.",evidence] if approved else findings[q['id']])}
  if not approved:result['severity']='major';result['action']='Author revise and increment revision; independent retest required.'
  results.append(result)
 artifact={'batch_file':f'data/questions/drafts/expand-a-{batch:03}.json','reviewer_id':'peer-reviewer-b','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'summary':summary}
 base=ROOT/'reports/content'/f'expand-peer-b-a{batch:03}'
 base.with_suffix('.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2),encoding='utf8')
 lines=[f'# Independent peer review A{batch:03}','','Reviewer: peer-reviewer-b.',summary,'',evidence,'','| ID | Revision | Decision | Notes |','|---|---:|---|---|']
 lines += [f"| {r['id']} | {r['revision']} | {r['decision']} | "+' '.join(r['notes']).replace('|','/')+' |' for r in results]
 base.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
 print(base,len(approved_ids),'approved',len(findings),'rejected')
if __name__=='__main__':
 findings={
 'p2-t1-d01-x04':['Same learning objective as d01-x03: platform absorbs capability supplied by a thin wrapper. Replace x04 with a distinct unused supported objective.'],
 'p2-t1-d01-x10':['Option b measures output token quantity, unrelated to the Evaluator role or quality measurement. Replace with a neighboring role/measurement misconception.'],
 'p2-t1-d02-x08':['Cited physical page15 is interview setup, not the leading interview wording. The actual leading positive introduction appears on physical page16; add/correct citation and verify.'],
 'p2-t1-d03-x02':['Physical page6 has generic solution options but not the specific Develop/micro-prototype mapping asserted. Add physical page5 which explicitly supports these elements.'],
 'p2-t1-d03-x13':['Repeats x10 learning objective: meaningful mechanism divergence versus cosmetic colors/chart placement. Retarget x13 to a distinct unused objective.']}
 approved={f'p2-t1-d{doc:02}-x{i:02}' for doc in [1,2,3] for i in range(1,18)}-set(findings)
 report(6,approved,findings,'Visually inspected all46 cited physical pages in tmp/root-review/expand-a-006/pages-01.png through pages-12.png. Actual PDF SHA256 verified for all3 documents.','Read all51 final revision1 questions and all options/answers/explanations. Compared all9 legacy questions for the same PDFs; broader related concepts were distinguished from duplicate objectives. Five major findings require retest. Other46 are approved at their exact recorded revisions.')
