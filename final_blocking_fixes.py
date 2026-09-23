import json,re,unicodedata
from pathlib import Path
root=Path(__file__).parent
# 1) Pact semantic parity: PT is baseline, EN/ES are direct-equivalent translations.
p=root/'content/topics.json'; data=json.load(open(p,encoding='utf-8'))
pact=data['pact']
pact['en']['sections']=[
['What Contract Testing is','Contract Testing verifies whether the consumer and provider agree on the interface used in the integration. It does not replace functional or E2E testing; it reduces the risk of incompatibilities between services.'],
['How Pact works','In a consumer-driven flow, the consumer describes the interactions it expects from the provider. These interactions generate a Pact contract, which is then verified against the provider.'],
['Consumer and Provider','The Consumer makes the call; the Provider handles the call. A contract describes relevant requests and responses without requiring all systems to be available at the same time during consumer testing.'],
['Pact Broker/PactFlow','In distributed teams, contracts can be published and versioned in a broker so that consumers and providers can verify compatibility across versions.'],
['Where QA adds value','QA helps identify critical integrations, error scenarios, version compatibility and gaps that should not depend only on late E2E testing.'],
['Attention point','Do not turn Pact into a complete copy of the production payload. Overly strict contracts increase coupling and may break because of changes that are irrelevant to the consumer.']]
pact['en']['qa_tip']='Use Contract Testing to get fast feedback on compatibility between services, while keeping E2E for flows that truly require full integration.'
pact['es']['sections']=[
['Qué es Contract Testing','Contract Testing verifica si el consumidor y el proveedor están de acuerdo sobre la interfaz utilizada en la integración. No sustituye las pruebas funcionales ni E2E; reduce el riesgo de incompatibilidades entre servicios.'],
['Cómo funciona Pact','En un flujo consumer-driven, el consumidor describe las interacciones que espera del proveedor. Estas interacciones generan un contrato Pact, que después se verifica contra el proveedor.'],
['Consumer y Provider','Consumer es quien realiza la llamada; Provider es quien la atiende. Un contrato describe requests y responses relevantes sin exigir que todos los sistemas estén disponibles al mismo tiempo durante la prueba del consumidor.'],
['Pact Broker/PactFlow','En equipos distribuidos, los contratos pueden publicarse y versionarse en un broker para que consumidores y proveedores verifiquen la compatibilidad a lo largo de las versiones.'],
['Dónde QA agrega valor','QA ayuda a identificar integraciones críticas, escenarios de error, compatibilidad de versiones y brechas que no deben depender únicamente de pruebas E2E tardías.'],
['Punto de atención','No convierta Pact en una copia completa del payload de producción. Los contratos excesivamente rígidos aumentan el acoplamiento y pueden romperse por cambios irrelevantes para el consumidor.']]
pact['es']['qa_tip']='Use Contract Testing para obtener feedback rápido sobre compatibilidad entre servicios, manteniendo E2E para los flujos que realmente requieren integración completa.'
json.dump(data,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))

# 2) CTFL: translate term-only alternatives using the translated term embedded in explanations.
qpath=root/'data/ctfl-questions.json'; bank=json.load(open(qpath,encoding='utf-8'))
termmap={'pt':{},'es':{}}
for q in bank['questions']:
    en=q['explanation']['en'].split(':',1)[0].strip()
    for lang in ('pt','es'):
        loc=q['explanation'][lang].split(':',1)[0].strip()
        if en and loc: termmap[lang][en]=loc
# Curated ISTQB terminology for cases where legacy explanations retained English labels.
termmap['pt'].update({
'Test objective':'Objetivo de teste','Testing':'Teste','Quality assurance':'Garantia da qualidade','Defect':'Defeito','Failure':'Falha','Exhaustive testing':'Teste exaustivo','Error':'Erro','Test plan':'Plano de teste','Risk-based testing':'Teste baseado em risco','Test monitoring':'Monitoramento de teste','Defect report':'Relatório de defeito','Test strategy':'Estratégia de teste','Product risk':'Risco de produto','Confirmation testing':'Teste de confirmação','Component testing':'Teste de componente','Functional testing':'Teste funcional','Non-functional testing':'Teste não funcional','Static testing':'Teste estático','Test automation':'Automação de testes','Static analysis tool':'Ferramenta de análise estática','Automation benefit':'Benefício da automação','Tool metrics':'Métricas de ferramentas'})
termmap['es'].update({
'Test objective':'Objetivo de prueba','Testing':'Pruebas','Quality assurance':'Aseguramiento de la calidad','Defect':'Defecto','Failure':'Fallo','Exhaustive testing':'Pruebas exhaustivas','Error':'Error','Test plan':'Plan de pruebas','Risk-based testing':'Pruebas basadas en riesgos','Test monitoring':'Monitoreo de pruebas','Defect report':'Informe de defecto','Test strategy':'Estrategia de pruebas','Product risk':'Riesgo de producto','Confirmation testing':'Pruebas de confirmación','Component testing':'Pruebas de componentes','Functional testing':'Pruebas funcionales','Non-functional testing':'Pruebas no funcionales','Static testing':'Pruebas estáticas','Test automation':'Automatización de pruebas','Static analysis tool':'Herramienta de análisis estático','Automation benefit':'Beneficio de la automatización','Tool metrics':'Métricas de herramientas'})
changed={'pt':0,'es':0}
for q in bank['questions']:
    for lang in ('pt','es'):
        arr=q['options'][lang]
        out=[]
        for x in arr:
            y=termmap[lang].get(x,x)
            if y!=x: changed[lang]+=1
            out.append(y)
        q['options'][lang]=out
json.dump(bank,open(qpath,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))

# 3) Mobile back-to-top safe area.
css=root/'assets/css/site.css'; s=css.read_text(encoding='utf-8')
s += '''\n/* 3.1 final blocking fixes: mobile back-to-top safe area */\n@media(max-width:820px){\n  .back-to-top{width:40px;height:40px;left:14px;bottom:12px;border-radius:13px;font-size:19px}\n  .side{padding-bottom:76px}\n  .nav-tree{padding-bottom:64px}\n}\n'''
css.write_text(s,encoding='utf-8')

# audit
# structural parity + body length ratios to flag semantic-depth outliers
rows=[]; structural=[]; depth=[]
for slug,t in data.items():
    if not isinstance(t,dict) or not all(k in t for k in ('pt','en','es')): continue
    counts=[len(t[k].get('sections',[])) for k in ('pt','en','es')]
    if len(set(counts))>1: structural.append((slug,counts))
    for i in range(min(counts)):
        lens=[len(t[k]['sections'][i][1]) for k in ('pt','en','es')]
        if min(lens) and max(lens)/min(lens)>2.15: depth.append((slug,i+1,lens))
report=f'''# QA Lab Brasil 3.1 - Final Blocking Fixes Audit\n\n- Topics: {sum(1 for t in data.values() if isinstance(t,dict) and all(k in t for k in ('pt','en','es')))}\n- Structural section-count mismatches: {len(structural)}\n- Large section-depth outliers (>2.15x): {len(depth)}\n- CTFL option labels translated PT: {changed['pt']}\n- CTFL option labels translated ES: {changed['es']}\n- Pact semantic parity: corrected against PT baseline\n- Mobile back-to-top overlap: safe-area fix applied\n\nStructural mismatches: {structural[:20]}\nDepth outliers sample: {depth[:30]}\n'''
(root/'V3_1_FINAL_BLOCKING_FIXES_AUDIT.md').write_text(report,encoding='utf-8')
print(report)
