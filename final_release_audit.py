import json,re,os,glob,unicodedata,collections,subprocess,sys
ROOT=os.path.dirname(__file__)
D=json.load(open(ROOT+'/content/topics.json',encoding='utf8'))
Q=json.load(open(ROOT+'/data/ctfl-questions.json',encoding='utf8'))
C=json.load(open(ROOT+'/data/pdf-catalog.json',encoding='utf8'))
issues=[]; stats={}
langs=('pt','en','es')
# topics structure
stats['topics']=len(D)
for slug,t in D.items():
    for l in langs:
        if l not in t: issues.append(f'{slug}: missing {l}')
    if all(l in t for l in langs):
        counts=[len(t[l].get('sections',[])) for l in langs]
        if len(set(counts))!=1: issues.append(f'{slug}: section counts {counts}')
        ic=[len(t[l].get('insights',[])) for l in langs]
        if len(set(ic))!=1: issues.append(f'{slug}: insight counts {ic}')
        for i in range(min(counts)):
            for l in langs:
                s=t[l]['sections'][i]
                if not isinstance(s,list) or len(s)<2 or not str(s[0]).strip() or not str(s[1]).strip(): issues.append(f'{slug}/{l}/section{i}: malformed')
# contamination heuristics
bad={'en':[r'\bnão\b',r'\bvocê\b',r'\btambém\b',r'\bferramenta\b',r'\binstalação\b',r'\bconfiguração\b',r'\bquando\b'],
     'es':[r'\bnão\b',r'\bvocê\b',r'\btambém\b',r'\bferramenta\b',r'\binstalação\b',r'\bconfiguração\b',r'\bquando\b'],
     'pt':[r'\bwhich\b',r'\bshould\b',r'\bprovides\b',r'\ballows\b']}
for slug,t in D.items():
    for l in langs:
        text=json.dumps(t[l],ensure_ascii=False).lower()
        for p in bad[l]:
            if re.search(p,text): issues.append(f'{slug}/{l}: possible language contamination {p}')
# duplicate slugs/titles
for l in langs:
    seen=collections.defaultdict(list)
    for slug,t in D.items(): seen[t[l]['title'].strip().casefold()].append(slug)
    for title,slugs in seen.items():
        if len(slugs)>1: issues.append(f'{l}: duplicate title {title}: {slugs}')
# CTFL
qs=Q['questions']; stats['ctfl_questions']=len(qs)
ids=[q['id'] for q in qs]
if len(ids)!=len(set(ids)): issues.append('CTFL duplicate IDs')
for q in qs:
    if not (0<=q.get('correct',-1)<4): issues.append(f"{q['id']}: invalid correct index")
    for l in langs:
        if not q['text'].get(l,'').strip(): issues.append(f"{q['id']}/{l}: missing text")
        if len(q['options'].get(l,[]))!=4: issues.append(f"{q['id']}/{l}: options != 4")
        if not q['explanation'].get(l,'').strip(): issues.append(f"{q['id']}/{l}: missing explanation")
# exact duplicate stems
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'\W+',' ',s).strip()
for l in langs:
    c=collections.defaultdict(list)
    for q in qs:c[norm(q['text'][l])].append(q['id'])
    for k,v in c.items():
        if len(v)>1: issues.append(f'CTFL {l}: duplicate question text {v}')
# family count supports unique 40-question exam
families={re.sub(r'-\d+$','',q['id']) for q in qs}
stats['ctfl_concepts']=len(families)
if len(families)<40: issues.append('CTFL has fewer than 40 unique concepts')
# verify selection implementation protects families
app=open(ROOT+'/assets/js/app.js',encoding='utf8').read()
for needle in ['ctflConceptId','ctflUniqueConcepts','usedConcepts','ctflBalancedSelect']:
    if needle not in app: issues.append('CTFL selection guard missing: '+needle)
# PDFs
for l in langs:
    edu=[]; inst=[]
    for f in glob.glob(ROOT+f'/pdf/{l}/*.pdf'):
        (inst if f.endswith('-installation.pdf') else edu).append(f)
    stats[f'pdf_{l}_edu']=len(edu); stats[f'pdf_{l}_install']=len(inst)
    if len(edu)!=len(D): issues.append(f'{l}: educational PDFs {len(edu)} != topics {len(D)}')
# catalog refs
entries=C if isinstance(C,list) else C.get('items',C)
# local href/src existence in HTML/CSS/JS
for f in [ROOT+'/index.html',ROOT+'/404.html']:
    txt=open(f,encoding='utf8').read()
    for ref in re.findall(r'(?:href|src)=["\'](/[^"\'?#]+)',txt):
        if ref=='/': continue
        path=ROOT+ref
        if not os.path.exists(path): issues.append(f'{os.path.basename(f)} missing asset {ref}')
# JS syntax
p=subprocess.run(['node','--check',ROOT+'/assets/js/app.js'],capture_output=True,text=True)
if p.returncode: issues.append('app.js syntax: '+p.stderr.strip())
# expected SEO files
for rel in ['robots.txt','sitemap.xml','index.html','404.html','data/ctfl-questions.json','data/pdf-catalog.json']:
    if not os.path.exists(ROOT+'/'+rel): issues.append('missing '+rel)
# known placeholder/bad typo scan in source content
badwords=re.compile(r'\b(testos|instalaçao|configuraçao|sujestão|corrijido|playwiright|playwrright)\b',re.I)
for path in [ROOT+'/content/topics.json',ROOT+'/assets/js/app.js',ROOT+'/index.html']:
    txt=open(path,encoding='utf8').read()
    m=badwords.search(txt)
    if m: issues.append(f'{os.path.basename(path)} suspicious typo: {m.group(0)}')
# output
stats['issues']=len(issues)
print(json.dumps(stats,ensure_ascii=False,indent=2))
if issues:
    print('\nISSUES')
    for x in issues[:300]: print('-',x)
    sys.exit(1)
print('PASS')
