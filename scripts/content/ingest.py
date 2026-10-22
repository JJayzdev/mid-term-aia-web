"""Local, resumable source ingestion. Run with bundled Python; requires pypdf/pdfplumber.
Windows.Media.Ocr is used locally via Windows PowerShell 5; no source upload.
"""
import pathlib,json,re,hashlib,subprocess,concurrent.futures,shutil,time,argparse
ROOT=pathlib.Path(__file__).resolve().parents[2]
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def ingest(doc):
 import pdfplumber
 from pypdf import PdfReader
 source=ROOT/doc['relative_path'];digest=hashlib.sha256(source.read_bytes()).hexdigest()
 if digest!=doc['sha256']: raise ValueError('Source hash changed: '+str(source))
 cache=ROOT/'content/extracted'/f'{digest}.json'
 if cache.exists():
  old=json.loads(cache.read_text(encoding='utf-8'))
  if len(old['pages'])==doc['page_count'] and old.get('provenance',{}).get('pipeline_revision')==1 and old.get('provenance',{}).get('render_dpi')==115 and not any(p.get('error') for p in old['pages']):
   md=ROOT/'content/text'/f'{doc["document_id"]}.md';md.parent.mkdir(parents=True,exist_ok=True)
   if not md.exists():md.write_text('# '+doc['title']+'\n\n'+'\n\n'.join(f'## Physical PDF page {p["pdf_page"]} [{p["method"]}]\n\n{p["text"]}' for p in old['pages']),encoding='utf-8')
   return {'document_id':doc['document_id'],'cached':True,'pages':len(old['pages'])}
 work=ROOT/'tmp/content-tools/renders'/doc['document_id'];work.mkdir(parents=True,exist_ok=True)
 reader=PdfReader(source); pages=[];needs=[]
 with pdfplumber.open(source) as pdf:
  for num,page in enumerate(reader.pages,1):
   text=page.extract_text() or ''; private=sum(0xE000<=ord(c)<=0xF8FF for c in text)
   if len(re.sub(r'\s','',text))<40 or private or '\ufffd' in text:
    pdf.pages[num-1].to_image(resolution=115).save(work/f'{num:04}.png');needs.append(num)
    pages.append({'pdf_page':num,'text':'','method':'pending_ocr','error':None,'native_text_chars':len(text),'native_private_use_chars':private})
   else: pages.append({'pdf_page':num,'text':text,'method':'pypdf','error':None,'native_text_chars':len(text),'native_private_use_chars':private})
 if needs:
  result=work/'ocr.json';subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'scripts/content/ocr.ps1'),'-InputDirectory',str(work),'-OutputPath',str(result)],check=True,capture_output=True)
  ocr=json.loads(result.read_text(encoding='utf-8-sig'));ocr=ocr if isinstance(ocr,list) else [ocr]
  for entry in ocr:
   page=pages[entry['page']-1];page.update(text='\n'.join(entry.get('lines',[])) or entry['text'],method=entry['method'],error=entry['error']);page['ocr_language']='en-US';page['quality_warning']='Vietnamese diacritics, math and reading order require visual source review'
 for page in pages:page['status']='extracted_unverified'
 output={'schema_version':'1.0.0','document_id':doc['document_id'],'sha256':digest,'source_path':doc['relative_path'],'page_count':len(pages),'pages':pages,'provenance':{'ocr':'Windows.Media.Ocr installed en-US model','ocr_language':'en-US','render_dpi':115,'pipeline_revision':1,'source_mutated':False}}
 write(cache,output)
 md=ROOT/'content/text'/f'{doc["document_id"]}.md';md.parent.mkdir(parents=True,exist_ok=True)
 md.write_text('# '+doc['title']+'\n\n'+'\n\n'.join(f'## Physical PDF page {p["pdf_page"]} [{p["method"]}]\n\n{p["text"]}' for p in pages),encoding='utf-8')
 allowed=(ROOT/'tmp/content-tools/renders').resolve();resolved_work=work.resolve()
 if resolved_work==allowed or allowed not in resolved_work.parents:raise ValueError('Unsafe render cleanup path')
 shutil.rmtree(resolved_work)
 return {'document_id':doc['document_id'],'cached':False,'pages':len(pages),'ocr_pages':len(needs),'errors':sum(bool(p['error']) for p in pages),'empty_pages':sum(not p['text'].strip() for p in pages)}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=3);parser.add_argument('--limit',type=int);args=parser.parse_args()
 inventory=json.loads((ROOT/'docs/discovery/source-inventory.json').read_text(encoding='utf-8'));docs=[];topics=[]
 for f in inventory['files']:
  folder=pathlib.PurePosixPath(f['path']).parent.name;day=f['mapping']['day']['value'];track=None if folder=='phase1' else int(re.search(r'track(\d)',folder).group(1));phase=1 if track is None else 2;key=f'p1-d{day:02}' if phase==1 else f'p2-t{track}-d{day:02}'
  doc={'document_id':key,'title':f['cover_evidence']['title'],'relative_path':f['path'],'page_count':f['pages'],'sha256':f['sha256'],'bytes':f['bytes'],'phase':phase,'track':track,'day':key,'topic':key,'mapping_status':'verified_by_root_policy','mapping_policy':'Curricular folder defines phase/track; filename defines local day. This does not assert printed source labels match.','source_cover_evidence':f['cover_evidence'],'conflicts':f['errors'],'extracted_path':f'content/extracted/{f["sha256"]}.json'};docs.append(doc)
  topics.append({'id':key,'label':doc['title'],'phase':phase,'track':track,'day':key,'document_ids':[key],'question_count':0})
 write(ROOT/'content/catalog.json',{'schema_version':'1.0.0','catalog_version':'2026.10.22.1','documents':docs,'topics':topics})
 results=[];started=time.time()
 with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
  futures={pool.submit(ingest,d):d for d in docs[:args.limit]}
  for future in concurrent.futures.as_completed(futures):
   try: result=future.result()
   except Exception as e: result={'document_id':futures[future]['document_id'],'error':str(e)}
   results.append(result);print(json.dumps(result),flush=True)
   write(ROOT/'reports/ingestion/progress.json',{'elapsed_seconds':round(time.time()-started,1),'completed':len(results),'total':len(futures),'results':results})
 write(ROOT/'reports/ingestion/run.json',{'schema_version':'1.0.0','completed':len(results),'total':len(futures),'elapsed_seconds':round(time.time()-started,1),'results':results})
if __name__=='__main__':main()
