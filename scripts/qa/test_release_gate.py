"""Negative release-gate fixtures in a temporary directory; never author approvals.

Run: python -m unittest discover -s scripts/qa -p test_release_gate.py -v
"""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('release_validator', PROJECT/'scripts/validate_release.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ReleaseGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = gate.read(PROJECT/'public/data/bank.json')
        cls.catalog = gate.read(PROJECT/'public/data/catalog.json')
        cls.schema = gate.read(PROJECT/'docs/schemas/question-bank.schema.json')
        cls.reports = {q['review']['report_id']: gate.read(PROJECT/q['review']['report_id'])
                       for q in cls.bank['questions']}

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='aia-gate-fixture-')
        self.root = Path(self.temporary.name).resolve()
        self.original_root = gate.ROOT
        gate.ROOT = self.root
        self.addCleanup(self.temporary.cleanup)
        self.addCleanup(setattr, gate, 'ROOT', self.original_root)
        self.data = copy.deepcopy(self.bank)
        self.write('docs/schemas/question-bank.schema.json', self.schema)
        self.write('catalog.json', self.catalog)
        for path, report in self.reports.items():
            self.write(path, report)

    def write(self, relative, value):
        target = self.root/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def validate(self, **kwargs):
        self.write('bank.json', self.data)
        return gate.validate(self.root/'bank.json', self.root/'catalog.json', **kwargs)

    def approval(self, question):
        path = question['review']['report_id']
        report = gate.read(self.root/path)
        item = next(r for r in report['results'] if (r['id'], r['revision']) ==
                    (question['id'], question['revision']))
        return path, report, item

    def test_valid_release_passes(self):
        errors, summary = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(summary['questions'], len(self.data['questions']))

    def test_later_rejection_revokes_old_exact_revision_approval(self):
        q = self.data['questions'][0]
        _, report, decision = self.approval(q)
        decision['decision'] = 'rejected'
        report['results'] = [decision]
        report['reviewed_at'] = '2099-01-01T00:00:00+00:00'
        self.write('reports/content/test-later-rejection.json', report)
        errors, _ = self.validate()
        self.assertTrue(any('latest exact-revision approval' in e for e in errors), errors)

    def test_approval_must_cover_every_cited_page(self):
        path, report, item = self.approval(self.data['questions'][0])
        item['source_pages'] = []
        self.write(path, report)
        errors, _ = self.validate()
        self.assertTrue(any('cover all referenced source pages' in e for e in errors), errors)

    def test_self_approval_is_rejected(self):
        q = self.data['questions'][0]
        q['author_id'] = q['review']['reviewer_id']
        errors, _ = self.validate()
        self.assertTrue(any('review must be independent' in e for e in errors), errors)

    def test_review_timestamp_must_match_artifact(self):
        self.data['questions'][0]['review']['reviewed_at'] = '2099-01-01T00:00:00+00:00'
        errors, _ = self.validate()
        self.assertTrue(any('review timestamp differs' in e for e in errors), errors)

    def test_document_minimum_cannot_be_satisfied_by_other_documents(self):
        _, baseline = self.validate()
        minimum = baseline['minimum_questions_per_document']
        doc = next(d for d, count in baseline['questions_per_document'].items() if count == minimum)
        item = next(q for q in self.data['questions'] if any(s['document_id'] == doc for s in q['source_reference']))
        self.data['questions'].remove(item)
        errors, summary = self.validate(min_per_document=minimum)
        self.assertEqual(summary['questions_per_document'][doc], minimum-1)
        self.assertTrue(any('Documents below minimum' in e for e in errors), errors)

    def test_multiple_pages_do_not_count_as_multiple_questions(self):
        _, baseline = self.validate()
        q = self.data['questions'][0]
        source = copy.deepcopy(q['source_reference'][0])
        source['pdf_page'] = source['pdf_page'] + 1
        q['source_reference'].append(source)
        path, report, decision = self.approval(q)
        decision['source_pages'].append({'document_id': source['document_id'], 'pdf_page': source['pdf_page']})
        self.write(path, report)
        errors, summary = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(summary['questions_per_document'], baseline['questions_per_document'])

    def test_track4_calculation_minimum_is_enforced(self):
        for q in self.data['questions']:
            q.pop('calculation', None)
        errors, _ = self.validate()
        self.assertTrue(any('Insufficient Track 4 calculation questions' in e for e in errors), errors)

    def test_percentage_rounding_is_not_source_dependent(self):
        self.data['questions'][0]['question'] = 'Làm tròn kết quả theo phần trăm.'
        errors, _ = self.validate(standalone_stems=True)
        self.assertEqual(errors, [])

    def test_source_dependent_stem_is_rejected(self):
        self.data['questions'][0]['question'] = 'Trong slide, khái niệm nào được trình bày?'
        errors, _ = self.validate(standalone_stems=True)
        self.assertTrue(any('source-dependent stem' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
