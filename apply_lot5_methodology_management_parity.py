import json
from pathlib import Path
p=Path(__file__).parent/'content/topics.json'
d=json.load(open(p,encoding='utf-8'))
lot5=['software','agile','scrum','kanban','xp','lean','waterfall','v-model','hybrid-methods','management','templates','release','incidents','jira-xray','zephyr','qtest','azure-test-plans','testrail','alm-quality-center','alm-octane','testlink','analytics','workspace','toolkit','setup-center']

# XP: EN missed the PT/ES safe-start section.
en=d['xp']['en']['sections']
j=next(i for i,s in enumerate(en) if s[0]=='First QA-oriented use')
en.insert(j,['How to start safely','Start with the official Extreme Programming references and introduce the practices incrementally in a controlled team context. Align roles, feedback loops, automated checks and the Definition of Done before increasing cadence or relying on a practice in a critical delivery.'])
d['xp']['en']['sections']=en

# Hybrid methods: PT baseline has safe-start but no generic "what it is" block.
for lang,title in [('en','What it is and where it fits'),('es','Qué es y dónde encaja')]:
    d['hybrid-methods'][lang]['sections']=[s for s in d['hybrid-methods'][lang]['sections'] if s[0]!=title]
for lang,heading,body,first in [
 ('en','How to start safely','Start by documenting which parts of the delivery flow follow agile practices and which parts follow staged or governance-driven controls. Make responsibilities, quality gates, evidence and handoffs explicit so the hybrid model is intentional rather than an accidental mixture of processes.','First QA-oriented use')]:
    secs=d['hybrid-methods'][lang]['sections']
    j=next(i for i,s in enumerate(secs) if s[0]==first)
    secs.insert(j,[heading,body])

# QA management tools: legacy enrichment added an EN adoption block absent from PT/ES.
for k in ['jira-xray','zephyr','qtest','alm-quality-center','alm-octane']:
    d[k]['en']['sections']=[s for s in d[k]['en']['sections'] if s[0] != 'Adoption good practices']

# Keep auxiliary insight arrays aligned with the baseline section count.
for key in lot5:
    n=len(d[key]['pt'].get('sections',[]))
    for lang in ['en','es']:
        m=len(d[key][lang].get('sections',[]))
        if m!=n:
            raise SystemExit(f'COUNT MISMATCH {key}: pt={n} {lang}={m}')
        if 'insights' in d[key]['pt']:
            cur=d[key][lang].get('insights',[])
            if len(cur)<n: cur=cur+[{} for _ in range(n-len(cur))]
            elif len(cur)>n: cur=cur[:n]
            d[key][lang]['insights']=cur

json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('LOT5 UPDATED',len(lot5))
for k in lot5:
    print(k,len(d[k]['pt']['sections']),len(d[k]['en']['sections']),len(d[k]['es']['sections']))
