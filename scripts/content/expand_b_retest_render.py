import json
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
D={d['document_id']:d for d in json.loads((R/'content/catalog.json').read_text(encoding='utf8'))['documents']}
pages=[('p2-t3-d09',31),('p2-t4-d01',30)]
out=R/'tmp/root-review/b-own-replacements';out.mkdir(exist_ok=True)
for k in range(0,len(pages),4):
 sheet=Image.new('RGB',(2400,1500),'white')
 for i,(doc,p) in enumerate(pages[k:k+4]):
  with pdfium.PdfDocument(R/D[doc]['relative_path']) as pdf:
   pg=pdf[p-1];im=pg.render(scale=1200/pg.get_width()).to_pil().convert('RGB')
  x=(i%2)*1200;y=(i//2)*750
  sheet.paste(im,(x,y+30));ImageDraw.Draw(sheet).text((x+10,y+8),f'{doc} PDF page {p}',fill='black')
 sheet.save(out/f'pages-{k//4+1}.png')
