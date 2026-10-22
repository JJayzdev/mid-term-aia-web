"""Read-only quality/coverage checks. No script can approve question semantics."""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META_STEM = re.compile(r'\bslides?\b|theo (?:tài liệu|bài giảng|bảng|phần|sơ đồ|cây quyết định)|trong (?:bảng|sơ đồ)|được sơ đồ|của ví dụ|nguồn nêu|khớp bảng|phù hợp nguồn|được minh họa', re.I)

def normalized(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text).casefold()).strip()

def main():
    catalog = json.loads((ROOT / 'content/catalog.json').read_text(encoding='utf-8'))
    docs = {d['document_id']: d for d in catalog['documents']}
    questions = []
    batches = []
    for path in sorted((ROOT / 'data/questions/drafts').glob('*.json')):
        bank = json.loads(path.read_text(encoding='utf-8'))
        questions.extend(bank['questions'])
        batches.append({'file': path.name, 'questions': len(bank['questions'])})
    reviews = {}
    for path in sorted((ROOT / 'reports/content').glob('*.json')):
        report = json.loads(path.read_text(encoding='utf-8'))
        for result in report.get('results', []):
            key = (result['id'], result['revision'])
            existing = reviews.get(key)
            if not existing or report['reviewed_at'] >= existing[0]:
                reviews[key] = (report['reviewed_at'], result['decision'], report['reviewer_id'])
    per_doc = defaultdict(set)
    per_doc_approved = defaultdict(set)
    cited_pages = defaultdict(set)
    fingerprints = defaultdict(list)
    approved = []
    for q in questions:
        fingerprints[normalized(q.get('context', '') + ' ' + q['question'])].append(q['id'])
        decision = reviews.get((q['id'], q['revision']))
        independent = decision and decision[1] == 'approved' and decision[2] != q['author_id']
        if independent:
            approved.append(q['id'])
        for s in q['source_reference']:
            per_doc[s['document_id']].add(q['id'])
            cited_pages[s['document_id']].add(s['pdf_page'])
            if independent:
                per_doc_approved[s['document_id']].add(q['id'])
    report = {
        'note': 'Draft counts are not approval. Only exact-revision independent review counts as approved; semantic/source review remains mandatory.',
        'questions_total': len(questions), 'new_questions': sum(b['questions'] for b in batches if b['file'].startswith('expand-')),
        'independently_approved_current_revision': len(approved),
        'minimum_draft_per_document': min(len(per_doc[d]) for d in docs),
        'minimum_approved_per_document': min(len(per_doc_approved[d]) for d in docs),
        'documents_at_target_draft': sum(len(per_doc[d]) >= 20 for d in docs),
        'documents_at_target_approved': sum(len(per_doc_approved[d]) >= 20 for d in docs),
        'missing_to_target': sum(max(0, 20 - len(per_doc[d])) for d in docs),
        'exact_duplicate_groups': [ids for ids in fingerprints.values() if len(ids) > 1],
        'duplicate_ids': [qid for qid, n in Counter(q['id'] for q in questions).items() if n > 1],
        'source_dependent_stems': [{'id': q['id'], 'question': q['question']} for q in questions if META_STEM.search(q['question'])],
        'batches': batches,
        'documents': [{'document_id': d, 'draft_questions': len(per_doc[d]), 'approved_current_revision': len(per_doc_approved[d]), 'distinct_cited_pages': len(cited_pages[d])} for d in sorted(docs)],
    }
    target = ROOT / 'reports/expansion/structural-audit.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('documents', 'batches', 'source_dependent_stems')}, ensure_ascii=True))
    print('source_dependent_stems:', len(report['source_dependent_stems']))

if __name__ == '__main__':
    main()
