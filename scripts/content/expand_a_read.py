"""Read-only source section map and page text for expansion authoring."""
import json,sys,pathlib
sys.stdout.reconfigure(encoding='utf-8');root=pathlib.Path(__file__).resolve().parents[2];catalog=json.loads((root/'content/catalog.json').read_text(encoding='utf-8'))
for arg in sys.argv[1:]:
 doc_id,_,selection=arg.partition(':');doc=next(d for d in catalog['documents'] if d['document_id']==doc_id);data=json.loads((root/doc['extracted_path']).read_text(encoding='utf-8'));wanted={int(n) for n in selection.split(',') if n}
 print('\nDOCUMENT',doc_id,doc['title'])
 for p in data['pages']:
  if wanted and p['pdf_page'] not in wanted:continue
  text=p['text'] if wanted else ' | '.join(p['text'].splitlines()[:3])[:180]
  print(f'PAGE {p["pdf_page"]}\n{text}')
