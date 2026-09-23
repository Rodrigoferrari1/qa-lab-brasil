import json
from pathlib import Path
p=Path(__file__).parent/'content/topics.json'
d=json.load(open(p,encoding='utf-8'))
lot6=['qa','testing','web','mobile','performance','security','ai','ai-testing','how-to-test','playground','bug-clinic','code-lab','glossary','learning-paths','interview-center','shorts','qa-shop','networking','auth','risk','accessibility','localization','ecommerce','payments','salesforce','erp','visual-regression','chatgpt','claude','gemini','deepseek','github-copilot','perplexity','microservices','event-driven']
# ChatGPT: PT/ES baseline has a safe-start block; EN had two generic legacy enrichment blocks instead.
en=d['chatgpt']['en']['sections']
en=[s for s in en if s[0] not in ('Using it in a real project','Adoption good practices')]
idx=next(i for i,s in enumerate(en) if s[0]=='First QA-oriented use')
en.insert(idx,['How to start safely','Start with non-sensitive examples and clearly defined QA tasks. Validate generated suggestions against requirements, evidence and trusted technical sources before using them in test assets or delivery decisions. Never expose secrets, production credentials or personal data in prompts.'])
d['chatgpt']['en']['sections']=en
# Architecture topics: EN missed the safe-start block present in PT/ES.
for key,body in {
 'microservices':'Start by mapping service boundaries, contracts, dependencies and observability before expanding the test strategy. Introduce contract, integration and end-to-end checks incrementally, and make failure handling, test data and environment ownership explicit.',
 'event-driven':'Start by mapping producers, consumers, event schemas, brokers and delivery guarantees. Define correlation IDs, observability and deterministic test data before automating asynchronous flows, and validate retries, duplication and ordering explicitly.'
}.items():
    en=d[key]['en']['sections']
    idx=next(i for i,s in enumerate(en) if s[0]=='First QA-oriented use')
    en.insert(idx,['How to start safely',body])
    d[key]['en']['sections']=en
# Validate structural parity and keep insight arrays aligned.
for key in lot6:
    n=len(d[key]['pt'].get('sections',[]))
    for lang in ['en','es']:
        m=len(d[key][lang].get('sections',[]))
        if m!=n: raise SystemExit(f'COUNT MISMATCH {key}: pt={n} {lang}={m}')
        if 'insights' in d[key]['pt']:
            cur=d[key][lang].get('insights',[])
            if len(cur)<n: cur += [{} for _ in range(n-len(cur))]
            elif len(cur)>n: cur=cur[:n]
            d[key][lang]['insights']=cur
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('LOT6 UPDATED',len(lot6))
