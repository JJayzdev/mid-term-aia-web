"""Promote only independently approved, exact draft revisions into public data.

This command consumes human/agent semantic review artifacts. It does not create
approvals and will leave rejected or unaudited questions out of the release.
"""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    schema = read(ROOT / 'docs/schemas/question-bank.schema.json')
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    catalog = read(ROOT / 'content/catalog.json')
    reviews = {}
    for path in sorted((ROOT / 'reports/content').glob('*.json')):
        report = read(path)
        for result in report.get('results', []):
            key = (result['id'], result['revision'])
            candidate = (report['reviewed_at'], result, report, path.relative_to(ROOT).as_posix())
            if key not in reviews or candidate[0] >= reviews[key][0]:
                reviews[key] = candidate
    seen, approved, omitted = set(), [], []
    for path in sorted((ROOT / 'data/questions/drafts').glob('*.json')):
        bank = read(path)
        validator.validate(bank)
        for draft in bank['questions']:
            if draft['id'] in seen:
                raise ValueError('Duplicate draft question ID: ' + draft['id'])
            seen.add(draft['id'])
            audit = reviews.get((draft['id'], draft['revision']))
            if not audit or audit[1]['decision'] != 'approved':
                omitted.append(draft['id'])
                continue
            _, decision, report, report_path = audit
            if report['reviewer_id'] == draft['author_id']:
                raise ValueError('Self-approval forbidden: ' + draft['id'])
            reviewed_pages = {(s['document_id'], s['pdf_page']) for s in decision.get('source_pages', [])}
            refs = {(s['document_id'], s['pdf_page']) for s in draft['source_reference']}
            if not refs <= reviewed_pages:
                raise ValueError('Review did not cover all referenced pages: ' + draft['id'])
            q = copy.deepcopy(draft)
            q['status'] = 'approved'
            q['review'] = {'reviewer_id': report['reviewer_id'], 'reviewed_at': report['reviewed_at'],
                           'reviewed_revision': q['revision'], 'report_id': report_path}
            for source in q['source_reference']:
                source['verification'] = 'verified'
            approved.append(q)
    approved.sort(key=lambda q: q['id'])
    digest = hashlib.sha256(json.dumps(approved, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]
    bank = {'schema_version': '1.0.0', 'bank_version': '2026.10.22-' + digest, 'questions': approved}
    validator.validate(bank)
    counts = Counter(q['topic'] for q in approved)
    public_catalog = {
        'schema_version': '1.0.0', 'catalog_version': catalog['catalog_version'],
        'documents': [{k: d[k] for k in ('document_id', 'title', 'relative_path', 'page_count', 'sha256', 'phase', 'track', 'day', 'mapping_status', 'mapping_policy', 'conflicts')} for d in catalog['documents']],
        'topics': [{**t, 'question_count': counts[t['id']]} for t in catalog['topics']],
    }
    coverage = {'bank_version': bank['bank_version'], 'approved_questions': len(approved),
                'documents_total': len(catalog['documents']), 'documents_represented': len(counts),
                'uncovered_documents': [d['document_id'] for d in catalog['documents'] if not counts[d['topic']]],
                'omitted_pending_or_rejected_ids': omitted,
                'note': 'Mỗi tài liệu được đại diện bằng một số câu từ các trang đã kiểm tra; không phải mọi khái niệm trên toàn bộ slide đều đã có câu hỏi.',
                'mapping_note': 'Phase/Track/Ngày ôn tập theo thư mục và tên file do người học cung cấp; nhãn in trên một số slide có thể khác.'}
    coverage['by_question_type'] = dict(Counter(q['question_type'] for q in approved))
    coverage['by_answer_format'] = dict(Counter(q['answer_format'] for q in approved))
    coverage['by_difficulty'] = dict(Counter(q['difficulty'] for q in approved))
    coverage['by_cognitive_level'] = dict(Counter(q['cognitive_level'] for q in approved))
    coverage['physical_pages_total'] = sum(d['page_count'] for d in catalog['documents'])
    coverage['distinct_cited_pages'] = len({(s['document_id'], s['pdf_page']) for q in approved for s in q['source_reference']})
    coverage['per_document'] = [{
        'document_id': d['document_id'], 'questions': sum(any(s['document_id'] == d['document_id'] for s in q['source_reference']) for q in approved),
        'cited_pages': sorted({s['pdf_page'] for q in approved for s in q['source_reference'] if s['document_id'] == d['document_id']}),
        'total_pages': d['page_count'],
    } for d in catalog['documents']]
    write(ROOT / 'data/questions/approved/bank.json', bank)
    write(ROOT / 'public/data/bank.json', bank)
    write(ROOT / 'public/data/catalog.json', public_catalog)
    write(ROOT / 'public/data/coverage.json', coverage)
    write(ROOT / 'reports/content/release-summary.json', coverage)
    print(json.dumps({'approved': len(approved), 'represented': len(counts), 'omitted': len(omitted), 'version': bank['bank_version']}))


if __name__ == '__main__':
    main()
