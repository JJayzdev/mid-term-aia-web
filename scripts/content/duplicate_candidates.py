"""Lexical candidates for human review; similarity is not a duplicate verdict."""
import json
import math
import re
import unicodedata
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STOP = set('một những nào khi cho của cần với đúng vì sao trong các được thể chọn tất cả đáp án phù hợp để và là có gì như thế thì phải nên giúp việc nhất hơn hoặc về này vào từ theo không chỉ muốn'.split())
questions = [q for path in sorted((ROOT / 'data/questions/drafts').glob('*.json')) for q in json.loads(path.read_text(encoding='utf-8'))['questions']]
tokens = [set(re.findall(r'\w+', unicodedata.normalize('NFKC', q.get('context', '') + ' ' + q['question']).casefold())) - STOP for q in questions]
inverted = defaultdict(list)
for i, words in enumerate(tokens):
    for word in words:
        inverted[word].append(i)
weights = {word: math.log((len(questions) + 1) / (len(ids) + 1)) + 1 for word, ids in inverted.items()}
norms = [math.sqrt(sum(weights[w] ** 2 for w in words)) for words in tokens]
scores = defaultdict(float)
for word, ids in inverted.items():
    if len(ids) > max(20, len(questions) // 5):
        continue
    for a, b in combinations(ids, 2):
        if norms[a] and norms[b]:
            scores[(a, b)] += weights[word] ** 2 / (norms[a] * norms[b])
candidates = []
for (a, b), score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    if score < 0.55:
        break
    candidates.append({'similarity': round(score, 3), 'first': questions[a]['id'], 'second': questions[b]['id'],
        'first_stem': questions[a]['question'], 'second_stem': questions[b]['question']})
out = ROOT / 'reports/expansion/duplicate-candidates.json'
out.write_text(json.dumps({'note': 'Lexical screening only. Reviewer must determine whether learning objectives are unnecessarily duplicated; absence does not prove semantic uniqueness.',
    'questions_checked': len(questions), 'candidates': candidates}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'questions_checked': len(questions), 'candidate_pairs': len(candidates)}))
