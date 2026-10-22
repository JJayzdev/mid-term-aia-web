"""Produce read-only review packets/contact sheets; never writes approvals."""
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('batch')
    p.add_argument('--render', action='store_true')
    args = p.parse_args()
    bank = json.loads((ROOT / 'data/questions/drafts' / (args.batch + '.json')).read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'content/catalog.json').read_text(encoding='utf-8'))
    docs = {d['document_id']: d for d in catalog['documents']}
    out = ROOT / 'tmp/root-review' / args.batch
    out.mkdir(parents=True, exist_ok=True)
    pages = sorted({(s['document_id'], s['pdf_page']) for q in bank['questions'] for s in q['source_reference']})
    lines = []
    for q in bank['questions']:
        lines += [f"\n{q['id']} revision={q['revision']} [{q['question_type']}]", q.get('context', ''), q['question']]
        lines += [f"  {o['id']}: {o['text']}" for o in q.get('options', [])]
        lines += [f"ANSWER: {q['correct_answer']}", q['explanation'], f"SOURCE: {[(s['document_id'], s['pdf_page']) for s in q['source_reference']]}"]
    (out / 'questions.txt').write_text('\n'.join(lines), encoding='utf-8')
    if args.render:
        import pypdfium2 as pdfium
        from PIL import Image, ImageDraw
        images = []
        for doc_id, page in pages:
            with pdfium.PdfDocument(ROOT / docs[doc_id]['relative_path']) as pdf:
                pg = pdf[page - 1]
                img = pg.render(scale=1200 / pg.get_width()).to_pil().convert('RGB')
            canvas = Image.new('RGB', (1200, 750), 'white')
            canvas.paste(img, (0, 30))
            ImageDraw.Draw(canvas).text((10, 8), f'{doc_id} PDF page {page}', fill='black')
            images.append(canvas)
        for start in range(0, len(images), 4):
            sheet = Image.new('RGB', (2400, 1500), '#dddddd')
            for i, im in enumerate(images[start:start + 4]):
                sheet.paste(im, ((i % 2) * 1200, (i // 2) * 750))
            sheet.save(out / f'pages-{start // 4 + 1:02}.png')
    print(f'{args.batch}: {len(bank["questions"])} questions, {len(pages)} source pages; {out}')

if __name__ == '__main__':
    main()
