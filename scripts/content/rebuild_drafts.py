"""Recreate A1 drafts from explicit editorial source specs. Never promotes/approves.
Run only when intentionally rebuilding drafts: existing review records must be
revalidated against resulting question revision/content before promotion.
"""
import pathlib,subprocess,sys,json
from jsonschema import Draft202012Validator
root=pathlib.Path(__file__).resolve().parents[2]
steps=['author_pilot.py','author_phase1.py','author_track1.py','curate_distractors.py','fix_track1_rule.py','author_track2.py','proofread_track2.py','author_track3.py','finalize_track3.py']
for step in steps:subprocess.run([sys.executable,str(root/'scripts/content'/step)],cwd=root,check=True)
schema=json.loads((root/'docs/schemas/question-bank.schema.json').read_text(encoding='utf-8'));validator=Draft202012Validator(schema)
count=0
for name in ['pilot-001','phase1-remaining','track1','track2','track3']:
 bank=json.loads((root/'data/questions/drafts'/f'{name}.json').read_text(encoding='utf-8'));validator.validate(bank);assert all(q['status']=='pending_review' for q in bank['questions']);count+=len(bank['questions'])
print(f'{count} A1 pending_review questions rebuilt and schema valid; independent review required.')
