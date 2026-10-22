import json,pathlib
p=pathlib.Path('data/questions/drafts/track1.json');d=json.loads(p.read_text(encoding='utf-8'))
q=next(q for q in d['questions'] if q['id']=='p2-t1-d09-q01');q['revision']=3
next(o for o in q['options'] if o['id']=='b')['text']='Nếu D30 retention dưới ngưỡng X giả định trong hai cohort liên tiếp thì dừng acquisition để điều tra onboarding; không tăng quảng cáo để bù'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
