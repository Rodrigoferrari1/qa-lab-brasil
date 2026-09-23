import json
from pathlib import Path
p=Path(__file__).parent/'content/topics.json'
d=json.load(open(p,encoding='utf-8'))
lot4=['data','devops','testability','cloud','docker','test-data','jenkins','kubernetes','terraform','grafana','prometheus','mysql','postgresql','sql-server','oracle','mongodb','data-pipeline','aws','azure','gcp','datadog','sonarqube','azure-devops','circleci','bitbucket-pipelines','kafka','azure-test-plans','data-quality','data-lake','data-warehouse','mysql-workbench','oracle-sql-developer','mongodb-compass']

# Common legacy enrichment added an extra generic EN adoption block not present in PT/ES.
remove_adoption=['jenkins','kubernetes','terraform','mysql','postgresql','sql-server','oracle','mongodb','data-pipeline','aws','azure','gcp','datadog','azure-devops','circleci','mysql-workbench','oracle-sql-developer','mongodb-compass']
for k in remove_adoption:
    d[k]['en']['sections']=[s for s in d[k]['en']['sections'] if s[0] != 'Adoption good practices']

# Docker PT contains safe-start where EN had a generic real-project block.
en=d['docker']['en']['sections']
for i,s in enumerate(en):
    if s[0]=='Using it in a real project':
        en[i]=['How to start safely','Start with the official Docker documentation. Confirm supported operating system, installation prerequisites and permissions. Validate Docker with a small image/container in a controlled environment before depending on it for a critical QA workflow.']
        break

# Bitbucket Pipelines / Azure Test Plans: remove extra generic adoption and map real-project slot to PT safe-start concept.
for k,label in [('bitbucket-pipelines','Bitbucket Pipelines'),('azure-test-plans','Azure Test Plans')]:
    en=d[k]['en']['sections']
    en=[s for s in en if s[0] != 'Adoption good practices']
    for i,s in enumerate(en):
        if s[0]=='Using it in a real project':
            en[i]=['How to start safely',f'Start with the official {label} documentation. Confirm access, permissions, prerequisites and the supported workflow. Perform the first configuration in a controlled project before applying it to a critical team process.']
            break
    d[k]['en']['sections']=en

# Kafka: PT has safe-start, EN had adoption; ES had an extra generic what-is block.
en=d['kafka']['en']['sections']
for i,s in enumerate(en):
    if s[0]=='Adoption good practices':
        en[i]=['How to start safely','Start with the official Apache Kafka documentation and a controlled local or non-production environment. Confirm broker/client compatibility, connectivity, topics and permissions before validating critical asynchronous flows.']
        # Move safe-start before first QA use, matching PT semantic order.
        item=en.pop(i)
        j=next(j for j,x in enumerate(en) if x[0]=='First QA-oriented use')
        en.insert(j,item)
        break
d['kafka']['en']['sections']=en
d['kafka']['es']['sections']=[s for s in d['kafka']['es']['sections'] if s[0] != 'Qué es y dónde encaja']

# Data Quality/Lake/Warehouse EN lacked the PT safe-start block.
for k,label in [('data-quality','Data Quality'),('data-lake','Data Lake'),('data-warehouse','Data Warehouse')]:
    en=d[k]['en']['sections']
    j=next(i for i,s in enumerate(en) if s[0]=='First QA-oriented use')
    en.insert(j,['How to start safely',f'Start with the official documentation and architecture used by your organization for {label}. Confirm access, data sources, permissions, environment and governance requirements. Practice with controlled non-production data before validating a critical data flow.'])

# Keep auxiliary insight arrays aligned with the baseline section count.
for key in lot4:
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
print('LOT4 UPDATED',len(lot4))
for k in lot4:
    print(k,len(d[k]['pt']['sections']),len(d[k]['en']['sections']),len(d[k]['es']['sections']))
