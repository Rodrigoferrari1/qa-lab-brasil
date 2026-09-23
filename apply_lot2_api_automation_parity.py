import json, copy, unicodedata, re
from pathlib import Path
p=Path(__file__).parent/'content/topics.json'
d=json.load(open(p,encoding='utf-8'))

def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]+',' ',s).strip()

def set_sections(key, lang, secs):
    d[key][lang]['sections']=secs

# Exact structural corrections where EN/ES had extra/missing generic sections.
# Postman EN: remove extra generic section absent from PT baseline.
set_sections('postman','en',[s for s in d['postman']['en']['sections'] if s[0] != 'What it is and where it fits'])
# Bruno ES: add missing real-project section in the same position as PT.
bes=d['bruno']['es']['sections']
bes.insert(9,['Uso en un proyecto real','En un proyecto real, organice las colecciones por dominio o servicio, mantenga variables por ambiente y versione junto al código solo lo que pueda compartirse con seguridad. Use Bruno para reproducir requests, validar contratos y colaborar con desarrollo sin almacenar secretos en el repositorio.'])
set_sections('bruno','es',bes)
# Insomnia: PT is baseline with 10 sections. Remove EN-only generic adoption sections and keep same conceptual order.
ien=d['insomnia']['en']['sections']
keep=['QA use','Official site and documentation','Getting started','Good practices','When to use it','How QA applies it','Common mistakes','What it is and where it fits','First QA-oriented use','Common issues and troubleshooting']
set_sections('insomnia','en',[next(s for s in ien if s[0]==t) for t in keep])
# ES already 10 but replace generic 'Cómo comenzar' with first-use equivalent to PT position.
ies=d['insomnia']['es']['sections']
for i,s in enumerate(ies):
    if s[0]=='Cómo comenzar con seguridad':
        ies[i]=['Primer uso orientado a QA','Cree una request sencilla, configure URL, método, headers y body cuando corresponda, ejecútela y valide status, payload, headers y tiempo de respuesta. Guarde la request en el workspace para poder repetirla y compararla durante la investigación.']
set_sections('insomnia','es',ies)
# REST/GraphQL/OpenAPI/Cucumber/RestAssured/Karate: remove EN-only adoption generic section.
for key in ['rest','graphql','openapi','cucumber','rest-assured','karate']:
    set_sections(key,'en',[s for s in d[key]['en']['sections'] if s[0] != 'Adoption good practices'])
# Playwright: add the two PT concepts missing one each in EN/ES.
pen=d['playwright']['en']['sections']
# insert API/data after cross-browser
idx=next(i for i,s in enumerate(pen) if s[0]=='Cross-browser and parallel execution')+1
pen.insert(idx,['API and test-data preparation','Playwright can combine UI and API flows. Use APIRequestContext to prepare preconditions, create or clean test data and validate backend responses without forcing every setup step through the browser. Keep test data deterministic and avoid coupling tests to shared mutable records.'])
set_sections('playwright','en',pen)
pes=d['playwright']['es']['sections']
# add missing debug/evidence after locator section
idx=next(i for i,s in enumerate(pes) if s[0]=='Locators, auto-wait y assertions')+1
pes.insert(idx,['Debug, evidencias y Trace Viewer','Use screenshots, videos, logs y especialmente Trace Viewer para investigar fallos con contexto de acciones, DOM, red y snapshots. La evidencia debe ayudar a explicar por qué falló la prueba, no solo demostrar que falló.'])
set_sections('playwright','es',pes)

# For all lot2 topics, enforce section-count parity with PT and align insights array lengths.
lot2=['api','api-tools','api-lab','postman','bruno','insomnia','soapui','rest','graphql','openapi','pact','api-auth','http-status','wiremock',
      'automation','playwright','selenium','cypress','robot-framework','appium','webdriverio','cucumber','rest-assured','karate','allure-report','browserstack']

# Add depth to the shortest focused topics while preserving the exact PT concepts.
augment={
'pact':{
'en':{
'What Contract Testing is':'Contract Testing verifies the agreement between a consumer and a provider without requiring the entire integrated environment to be available. Instead of validating only isolated endpoints, it checks whether requests and responses still respect the expectations that one service has about another. This is especially useful in distributed systems and microservices, where interface changes can break consumers independently of the provider implementation.',
'How Pact works':'Pact records consumer expectations as contracts (pacts). The consumer test defines the interaction it needs; the provider later verifies those interactions against its implementation. This creates fast feedback when an API change would violate an agreed request, response, status, header or payload structure.',
'Consumer and Provider':'The Consumer is the application or service that uses an API. The Provider exposes the API. A good contract focuses on what the consumer really depends on, avoiding unnecessary fields that make the contract brittle. QA can help identify critical interactions and negative or compatibility scenarios.',
'Pact Broker/PactFlow':'A Pact Broker or PactFlow can publish, version and share contracts and verification results across teams and pipelines. This enables visibility of which consumer/provider versions are compatible and supports deployment decisions based on verified contracts.',
'QA value':'QA adds value by identifying risky integrations, reviewing meaningful consumer expectations, validating error contracts and ensuring that contract verification runs in CI/CD. Contract tests complement, rather than replace, integration and end-to-end testing.',
'Attention point':'Do not turn a contract into a copy of the entire provider response. Overly strict contracts create false failures and excessive maintenance. Model only behavior the consumer truly requires and keep versioning and verification results traceable.'},
'es':{
'Qué es Contract Testing':'Contract Testing verifica el acuerdo entre un consumidor y un proveedor sin exigir que todo el ambiente integrado esté disponible. En lugar de validar solamente endpoints aislados, comprueba si requests y responses siguen respetando las expectativas que un servicio tiene sobre otro. Es especialmente útil en sistemas distribuidos y microservicios, donde un cambio de interfaz puede romper consumidores independientemente de la implementación del proveedor.',
'Cómo funciona Pact':'Pact registra las expectativas del consumidor como contratos (pacts). La prueba del consumidor define la interacción que necesita y el proveedor verifica después esas interacciones contra su implementación. Esto genera feedback rápido cuando un cambio de API rompe un request, response, status, header o estructura de payload acordados.',
'Consumer y Provider':'Consumer es la aplicación o servicio que utiliza una API. Provider expone la API. Un buen contrato se concentra en lo que el consumidor realmente necesita y evita campos innecesarios que vuelven frágil el contrato. QA puede ayudar a identificar interacciones críticas y escenarios negativos o de compatibilidad.',
'Pact Broker/PactFlow':'Pact Broker o PactFlow permiten publicar, versionar y compartir contratos y resultados de verificación entre equipos y pipelines. Esto da visibilidad sobre qué versiones de consumer/provider son compatibles y apoya decisiones de despliegue basadas en contratos verificados.',
'Valor para QA':'QA agrega valor identificando integraciones de riesgo, revisando expectativas relevantes del consumidor, validando contratos de error y garantizando que la verificación se ejecute en CI/CD. Contract Testing complementa, no sustituye, pruebas de integración y end-to-end.',
'Punto de atención':'No convierta el contrato en una copia de toda la respuesta del provider. Contratos excesivamente estrictos generan falsos fallos y mantenimiento innecesario. Modele solo el comportamiento que el consumidor realmente necesita y mantenga trazabilidad de versiones y verificaciones.'}},
'wiremock':{
'en':{
'What WireMock is':'WireMock is a tool for simulating HTTP services. It allows a team to replace an unavailable, unstable, expensive or hard-to-control dependency with predictable responses, making tests more repeatable and enabling scenarios that would be difficult to reproduce against a real service.',
'Stubs and matching':'A stub defines which incoming request should match and which response WireMock should return. Matching can consider method, URL, query parameters, headers and body. Keep matchers specific enough to represent the contract, but not so strict that irrelevant details make tests fragile.',
'Failure scenarios':'Mocks are particularly useful for failures: timeouts, 4xx/5xx responses, malformed payloads, slow responses and specific business errors. This helps QA validate resilience and error handling without manipulating a real downstream system.',
'Standalone or embedded':'WireMock can run as a standalone process/container or be embedded in automated tests. Choose based on team architecture, test isolation and CI/CD needs. In either case, version mappings/configuration so scenarios are reproducible.',
'QA use':'QA can use WireMock to unblock integration testing, create deterministic preconditions and reproduce rare dependency behavior. Record which behavior is simulated so results are not mistaken for validation against the real provider.',
'Attention point':'A mock can drift from the real service. Keep stubs aligned with API contracts and periodically validate critical flows against a real integrated environment. Service virtualization complements integration testing; it does not prove the provider itself works.'},
'es':{
'Qué es WireMock':'WireMock es una herramienta para simular servicios HTTP. Permite sustituir una dependencia indisponible, inestable, costosa o difícil de controlar por respuestas previsibles, haciendo las pruebas más repetibles y habilitando escenarios difíciles de reproducir contra un servicio real.',
'Stubs y matching':'Un stub define qué request de entrada debe coincidir y qué response debe devolver WireMock. El matching puede considerar método, URL, query parameters, headers y body. Mantenga reglas suficientemente específicas para representar el contrato, sin volverlas frágiles por detalles irrelevantes.',
'Escenarios de error':'Los mocks son especialmente útiles para fallos: timeouts, respuestas 4xx/5xx, payloads inválidos, respuestas lentas y errores de negocio específicos. Esto permite validar resiliencia y tratamiento de errores sin manipular un sistema downstream real.',
'Standalone o integrado':'WireMock puede ejecutarse como proceso/contenedor standalone o integrarse en pruebas automatizadas. Elija según arquitectura, aislamiento y CI/CD. En ambos casos, versione mappings/configuración para que los escenarios sean reproducibles.',
'Uso en QA':'QA puede usar WireMock para desbloquear pruebas de integración, crear precondiciones deterministas y reproducir comportamientos raros de dependencias. Registre qué comportamiento está simulado para no confundirlo con una validación del proveedor real.',
'Punto de atención':'Un mock puede quedar desalineado del servicio real. Mantenga los stubs alineados con los contratos de API y valide periódicamente flujos críticos en un ambiente integrado real. La virtualización complementa las pruebas de integración; no demuestra que el provider funcione.'}}
}
for key,langs in augment.items():
    for lang,mp in langs.items():
        secs=d[key][lang]['sections']
        d[key][lang]['sections']=[[title,mp.get(title,text)] for title,text in secs]

for key in lot2:
    n=len(d[key]['pt'].get('sections',[]))
    for lang in ['en','es']:
        if len(d[key][lang].get('sections',[]))!=n:
            raise SystemExit(f'count mismatch {key} pt={n} {lang}={len(d[key][lang].get("sections",[]))}')
        # Keep insight slots structurally aligned where present.
        if 'insights' in d[key]['pt']:
            cur=d[key][lang].get('insights',[])
            if len(cur)<n: cur=cur+[{} for _ in range(n-len(cur))]
            elif len(cur)>n: cur=cur[:n]
            d[key][lang]['insights']=cur

json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('LOT2 UPDATED',len(lot2))
for k in lot2:
    print(k, len(d[k]['pt']['sections']),len(d[k]['en']['sections']),len(d[k]['es']['sections']))
