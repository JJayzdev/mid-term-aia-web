# -*- coding: utf-8 -*-
"""Author-side structural checks only; does not perform or claim independent review."""
import json,re,collections
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[2]
schema=json.loads((ROOT/'docs/schemas/question-bank.schema.json').read_text(encoding='utf8'))
catalog={d['document_id']:d for d in json.loads((ROOT/'content/catalog.json').read_text(encoding='utf8'))['documents']}
batches=[];questions=[];counts=collections.Counter();pages=collections.defaultdict(set);errors=[]
for path in sorted((ROOT/'data/questions/drafts').glob('expand-b-*.json')):
 bank=json.loads(path.read_text(encoding='utf8'));jsonschema.validate(bank,schema)
 batches.append((path.stem,len(bank['questions'])));questions.extend(bank['questions'])
seen=set()
for q in questions:
 if q['id'] in seen:errors.append('duplicate id '+q['id'])
 seen.add(q['id']);counts[q['topic']]+=1
 if q['author_id']!='question-engineer-b' or q['status']!='pending_review':errors.append('author/status '+q['id'])
 if re.search(r'trong slide|theo tài liệu|slide nêu|bài giảng|theo phần|khớp bảng|nguồn nêu|trong bảng|theo bảng',q['question'],re.I):errors.append('meta wording '+q['id'])
 for ref in q['source_reference']:
  d=catalog[ref['document_id']]
  if ref['sha256']!=d['sha256'] or not 1<=ref['pdf_page']<=d['page_count']:errors.append('source '+q['id'])
  pages[q['topic']].add(ref['pdf_page'])
 if len({o['text'] for o in q.get('options',[])})!=len(q.get('options',[])):errors.append('duplicate option '+q['id'])
for doc,n in counts.items():
 if n!=(16 if doc.startswith('p2-t4-') else 17):errors.append('count '+doc)
assert len(questions)==521 and len(counts)==31
assert not errors,errors
lines=['# Author B expansion progress','','Author: question-engineer-b. The 521 original B expansion drafts retain pending_review status; independent approval decisions are stored separately. This author-side audit does not approve B questions.','','Assigned scope completed: Track 2 (12 documents), Track 3 (13 documents), Track 4 Days 1–6 (6 documents). Original bank questions unchanged.','','## Batches','','| Batch | New questions | Status |','|---|---:|---|']
lines += [f'| {name} | {n} | pending_review |' for name,n in batches]
lines += ['','## Author-side validation','','All 13 banks pass the question-bank JSON schema. IDs are unique within B, source SHA256 matches catalog, physical pages are in range, option text is unique per question, and no tested source-meta wording appears in question stems. Every question remains pending_review. These checks do not substitute for independent semantic/source review.','','## Citation coverage','','| Document | New questions | Distinct cited pages | Physical pages |','|---|---:|---:|---|']
lines += [f'| {doc} | {n} | {len(pages[doc])} | '+', '.join(map(str,sorted(pages[doc])))+' |' for doc,n in sorted(counts.items())]
lines += ['','Total distinct document/page pairs cited: '+str(sum(map(len,pages.values())))+'. Full extracted source texts were read before authoring. Clear prose mechanisms were used where OCR formulas were ambiguous; T2d03 code pages 27/34 were rendered and visually checked. Independent reviewers verify the exact question revisions.','','## Reproduction','','Current curated JSON is authoritative. Historical generation scripts must not be rerun over reviewed banks: later source fixes and reviewer edits may supersede their initial output. See scripts/content/README.md. Run only expand_b_audit.py to regenerate this read-only structural report.','','## Current revision distribution','']
revisions=collections.Counter(q['revision'] for q in questions)
lines += [f'- Revision {revision}: {n} questions.' for revision,n in sorted(revisions.items())]
lines += ['','Exact independent-review records govern approval; this report makes no approval claim. The separate 24-question calculator extension is outside these 521 original B drafts.','']
(ROOT/'reports/expansion/author-b-progress.md').write_text('\n'.join(lines),encoding='utf8')
print(f'PASS: {len(questions)} questions / {len(counts)} documents / {len(batches)} banks; {sum(map(len,pages.values()))} cited document-pages')
