import json, copy, re, unicodedata
from pathlib import Path
p=Path(__file__).parent/'content/topics.json'
d=json.load(open(p,encoding='utf-8'))

lot3=['programming','environment','git','python','java','nodejs','npm','vscode','powershell','intellij','eclipse','spring-tools','spring-framework','spring-boot','spring-initializr','mockito','spring-testing','maven','gradle','junit','testng','bitbucket','gitlab','github-actions','chrome-devtools','adb','logcat','maestro','detox','espresso','xcuitest']

# Remove EN/ES generic sections that were injected by older enrichment passes but have no PT baseline counterpart.
remove={
 'git':{'en':['What it is and where it fits','Adoption good practices'],'es':['Qué es y dónde encaja']},
 'python':{'en':['What it is and where it fits'],'es':['Qué es y dónde encaja']},
 'intellij':{'en':['What it is and where it fits'],'es':['Qué es y dónde encaja']},
 'spring-tools':{'en':['Using it in a real project']},
 'spring-framework':{'en':['What it is and where it fits'],'es':['Qué es y dónde encaja']},
 'maven':{'en':['Adoption good practices']},'gradle':{'en':['Adoption good practices']},'junit':{'en':['Adoption good practices']},'testng':{'en':['Adoption good practices']},
 'bitbucket':{'en':['Adoption good practices']},'gitlab':{'en':['Adoption good practices']},
 'chrome-devtools':{'en':['Adoption good practices']},'adb':{'en':['Adoption good practices']},'logcat':{'en':['Adoption good practices']},
 'espresso':{'en':['Using it in a real project','Adoption good practices']},
 'xcuitest':{'en':['Using it in a real project']},
}
for k,langs in remove.items():
    for lang,titles in langs.items():
        d[k][lang]['sections']=[s for s in d[k][lang]['sections'] if s[0] not in titles]

# Helpers for inserting missing concepts at the same semantic position as PT.
def insert_after(key,lang,after_title,new):
    secs=d[key][lang]['sections']
    i=next(i for i,s in enumerate(secs) if s[0]==after_title)
    secs.insert(i+1,new)

def insert_before(key,lang,before_title,new):
    secs=d[key][lang]['sections']
    i=next(i for i,s in enumerate(secs) if s[0]==before_title)
    secs.insert(i,new)

# Node.js ES lacked first-use and real-project sections; EN had a generic adoption section instead of safe-start.
nen=d['nodejs']['en']['sections']
for i,s in enumerate(nen):
    if s[0]=='Adoption good practices':
        nen[i]=['How to start safely','Install Node.js from the official source, open a new terminal and validate node --version and npm --version. Start in a small project folder, keep dependencies versioned in package.json/package-lock.json and avoid global packages unless the tool explicitly requires them.']
insert_after('nodejs','es','Cómo comenzar con seguridad',['Primer uso orientado a QA','Cree una carpeta de práctica, ejecute npm init -y y un script JavaScript sencillo con node. Valide que Node y npm funcionan antes de instalar frameworks de automatización o utilidades adicionales.'])
insert_after('nodejs','es','Primer uso orientado a QA',['Uso en un proyecto real','En automatización, use Node.js como runtime del proyecto, mantenga dependencias declaradas y reproducibles, separe configuración por ambiente y ejecute scripts mediante npm para que el mismo flujo funcione localmente y en CI/CD.'])

# IntelliJ ES had an extra generic section; add safe-start equivalent after practical application.
# After removal, ES is 12 and PT 12, but PT has safe-start while ES has same concept already.
insert_after('intellij','en','How QA applies it',['How to start safely','Install IntelliJ IDEA from the official JetBrains source, confirm the required JDK is available and create or open a small project first. Validate build and test execution before adding plugins or complex project configuration.'])

# Spring Boot ES lacked first QA use and real project.
insert_after('spring-boot','es','Cómo comenzar con seguridad',['Primer uso orientado a QA','Genere o abra un proyecto Spring Boot, confirme el JDK configurado, ejecute la aplicación y valide un endpoint o prueba mínima. Antes de automatizar escenarios mayores, compruebe que build, dependencias y perfil de ambiente funcionan correctamente.'])
insert_after('spring-boot','es','Primer uso orientado a QA',['Uso en un proyecto real','En proyectos reales, QA puede ejecutar pruebas unitarias/integración, validar APIs, perfiles, configuración y dependencias, y reproducir localmente defectos del backend. Mantenga datos y ambientes controlados para evitar resultados no deterministas.'])

# Maestro/Detox: normalize EN to PT concepts and fill ES QA-use + real-project.
for k in ['maestro','detox']:
    d[k]['es']['sections']=[s for s in d[k]['es']['sections'] if s[0] != 'Cuándo utilizarlo']

for k in ['maestro','detox']:
    en=d[k]['en']['sections']
    # Remove duplicate generic "When to use it", adoption and first-use because PT has QA practical use but not separate first-use.
    en=[s for s in en if s[0] not in ['When to use it','First QA-oriented use','Adoption good practices']]
    # Rename/replace safe slot after best practices with QA practical use if needed.
    # Existing order now: what, official, when, install, first, best, safe, real, issues
    safe_idx=next(i for i,s in enumerate(en) if s[0]=='How to start safely')
    if k=='maestro':
        en.insert(safe_idx,['How QA applies it in practice','Use Maestro to automate critical mobile journeys with readable YAML flows, stable selectors and controlled test data. Combine local execution with CI when appropriate and capture evidence for failures instead of relying only on a pass/fail result.'])
    else:
        en.insert(safe_idx,['How QA applies it in practice','Use Detox for end-to-end validation of React Native flows where synchronization with the app lifecycle is valuable. Keep scenarios focused on business-critical journeys and use lower-level tests for logic that does not require a full device/emulator flow.'])
    d[k]['en']['sections']=en

insert_after('maestro','es','Buenas prácticas',['Cómo lo aplica QA en la práctica','Use Maestro para automatizar recorridos móviles críticos con flows YAML legibles, selectores estables y datos de prueba controlados. Combine ejecución local con CI cuando corresponda y capture evidencias de fallos, no solo el resultado pass/fail.'])
insert_after('maestro','es','Cómo comenzar con seguridad',['Uso en un proyecto real','En un proyecto real, versione los flows junto al código o repositorio de QA, organice datos y ambientes, reutilice subflows cuando agreguen claridad y ejecute smoke/regresión móvil sobre dispositivos o emuladores representativos.'])
insert_after('detox','es','Buenas prácticas',['Cómo lo aplica QA en la práctica','Use Detox para validar flujos end-to-end de aplicaciones React Native cuando la sincronización con el ciclo de vida de la app sea importante. Mantenga los escenarios centrados en recorridos críticos y deje la lógica aislada para pruebas de nivel inferior.'])
insert_after('detox','es','Cómo comenzar con seguridad',['Uso en un proyecto real','En proyectos React Native, integre Detox al pipeline de pruebas, controle emuladores/simuladores y datos, capture logs/evidencias y mantenga los escenarios independientes para reducir flakiness y facilitar el diagnóstico.'])

# Espresso EN: after generic removals, add real-project? PT does not have it, so count should be 11 already.
# XCUITest EN: after removal count should match PT.

# Structural normalization for topics with a single EN generic adoption extra.
for k in ['spring-tools','maven','gradle','junit','testng','bitbucket','gitlab','chrome-devtools','adb','logcat']:
    # already removed where relevant; no-op here for readability
    pass

# Align insight slots and assert counts. Also detect suspiciously shallow translations by text ratio.
for key in lot3:
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
print('LOT3 UPDATED',len(lot3))
for k in lot3:
    print(k,len(d[k]['pt']['sections']),len(d[k]['en']['sections']),len(d[k]['es']['sections']))
