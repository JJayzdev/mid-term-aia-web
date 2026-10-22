"""Validate source-grounded release data. Requires Python + jsonschema.

Schema checks are structural. Content correctness requires separate reviewer
records; this program never approves authored questions by itself.
"""
import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from decimal import Decimal
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def normalize(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text).casefold()).strip()


def validate(bank_path, catalog_path, verify_sources=False, min_per_document=0, standalone_stems=False):
    bank, catalog = read(bank_path), read(catalog_path)
    schema = read(ROOT / 'docs/schemas/question-bank.schema.json')
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = ['schema %s: %s' % ('/'.join(map(str, e.path)), e.message) for e in validator.iter_errors(bank)]
    if errors:
        return errors, {}
    docs = {d['document_id']: d for d in catalog['documents']}
    topics = {t['id']: t for t in catalog['topics']}
    if len(docs) != len(catalog['documents']) or len(topics) != len(catalog['topics']):
        errors.append('Duplicate catalog document/topic IDs')
    ids = set()
    fingerprints = {}
    counts = Counter()
    per_doc = Counter()
    audit_entries = {}
    for path in (ROOT / 'reports/content').glob('*.json'):
        report = read(path)
        for result in report.get('results', []):
            if result.get('decision') == 'approved':
                audit_entries[(result['id'], result['revision'], path.relative_to(ROOT).as_posix())] = report
    for q in bank['questions']:
        qid = q['id']
        def fail(msg):
            errors.append(qid + ': ' + msg)
        if qid in ids:
            fail('duplicate question ID')
        ids.add(qid)
        fingerprint = normalize(q.get('context', '') + ' ' + q['question'])
        if standalone_stems and re.search(r'\bslides?\b|theo (?:tài liệu|bài giảng|bảng|phần)|trong bảng|nguồn nêu|khớp bảng|phù hợp nguồn|được minh họa', q['question'], re.I):
            fail('question must test knowledge directly; source-dependent stem')
        if fingerprint in fingerprints:
            fail('exact normalized duplicate of ' + fingerprints[fingerprint])
        fingerprints[fingerprint] = qid
        if q['status'] != 'approved':
            fail('non-approved question in release')
        review = q.get('review', {})
        if review.get('reviewer_id') == q['author_id'] or review.get('reviewed_revision') != q['revision']:
            fail('review must be independent and match revision')
        audit = audit_entries.get((qid, q['revision'], review.get('report_id')))
        if not audit or audit.get('reviewer_id') != review.get('reviewer_id'):
            fail('no matching independent approval artifact')
        topic = topics.get(q['topic'])
        if not topic or any(q[k] != topic[k] for k in ('phase', 'track', 'day')):
            fail('unknown topic or taxonomy differs from catalog')
        options = [o['id'] for o in q.get('options', [])]
        if len(options) != len(set(options)):
            fail('duplicate option IDs')
        if q['answer_format'] == 'single_choice' and q['correct_answer'] not in options:
            fail('answer not in options')
        if q['answer_format'] == 'multiple_choice':
            if not set(q['correct_answer']) < set(options):
                fail('multiple-choice answer must be proper subset of options')
        if q['answer_format'] == 'rubric':
            if sum(Decimal(str(c['weight'])) for c in q['rubric']) != 1:
                fail('rubric weights must sum exactly to 1')
            if len({c['id'] for c in q['rubric']}) != len(q['rubric']):
                fail('duplicate rubric criterion IDs')
        for source in q['source_reference']:
            doc = docs.get(source['document_id'])
            if not doc:
                fail('unknown source document')
                continue
            if source['sha256'] != doc.get('sha256') or not 1 <= source['pdf_page'] <= doc['page_count']:
                fail('source hash/page mismatch')
            if source['verification'] != 'verified':
                fail('unverified source')
        per_doc.update({s['document_id'] for s in q['source_reference'] if s['document_id'] in docs})
        kind = 'rubric' if q['answer_format'] == 'rubric' else 'objective'
        counts[(q['phase'], q['track'], kind)] += 1
    required = {(1, None, 'objective'): 34, (1, None, 'rubric'): 2}
    for track in (1, 2, 3, 4):
        required[(2, track, 'objective')] = 5
        required[(2, track, 'rubric')] = 1
    for bucket, count in required.items():
        if counts[bucket] < count:
            errors.append('Insufficient bucket %s: need %s, have %s' % (bucket, count, counts[bucket]))
    underfilled = {doc_id: per_doc[doc_id] for doc_id in docs if per_doc[doc_id] < min_per_document}
    if underfilled:
        errors.append('Documents below minimum %s questions: %s' % (min_per_document, underfilled))
    if verify_sources:
        for doc in docs.values():
            source = ROOT / doc['relative_path']
            if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != doc['sha256']:
                errors.append('Changed/missing source: ' + doc['relative_path'])
    summary = {'questions': len(bank['questions']), 'documents': len(docs),
               'documents_with_approved_questions': len(per_doc),
               'uncovered_documents': sorted(set(docs) - set(per_doc)),
               'minimum_questions_per_document': min((per_doc[d] for d in docs), default=0),
               'questions_per_document': {d: per_doc[d] for d in sorted(docs)},
               'by_bucket': {str(k): v for k, v in sorted(counts.items(), key=str)},
               'schema_version': bank['schema_version']}
    return errors, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', default=str(ROOT / 'public/data/bank.json'))
    parser.add_argument('--catalog', default=str(ROOT / 'public/data/catalog.json'))
    parser.add_argument('--verify-sources', action='store_true')
    parser.add_argument('--min-per-document', type=int, default=0)
    parser.add_argument('--standalone-stems', action='store_true')
    args = parser.parse_args()
    errors, summary = validate(args.bank, args.catalog, args.verify_sources, args.min_per_document, args.standalone_stems)
    print(json.dumps({'errors': errors, 'summary': summary}, ensure_ascii=True, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
