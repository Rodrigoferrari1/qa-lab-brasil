import json
from pathlib import Path
p=Path(__file__).parent/'content/topics.json'
d=json.load(open(p,encoding='utf-8'))
lot7=['jmeter','k6','etl','gatling','locust','loadrunner','opentelemetry','dynatrace','new-relic','sentry','owasp','zap','burp-suite','equivalence-partitioning','boundary-value-analysis','decision-table','state-transition','sauce-labs','lambdatest','dbeaver','pgadmin','charles-proxy','fiddler','proxyman','axe-core','wave','lighthouse','accessibility-insights','nvda','jaws','test-data-generator']

def rm(lang,key,titles):
    d[key][lang]['sections']=[s for s in d[key][lang]['sections'] if s[0] not in titles]
def insert_before(lang,key,before,section):
    a=d[key][lang]['sections']; i=next((i for i,s in enumerate(a) if s[0]==before),len(a)); a.insert(i,section)

def replace(lang,key,title,section):
    a=d[key][lang]['sections']; i=next(i for i,s in enumerate(a) if s[0]==title); a[i]=section

# Common legacy EN enrichment added one extra generic section that PT/ES do not have.
for key in ['jmeter','etl','gatling','locust','loadrunner','opentelemetry','dynatrace','new-relic','dbeaver','charles-proxy','fiddler','proxyman','axe-core','wave','lighthouse','accessibility-insights','nvda','jaws']:
    rm('en',key,{'Adoption good practices'})

# Sentry: remove generic legacy blocks, restore PT concepts in EN; remove duplicated generic ES block.
rm('en','sentry',{'What it is and where it fits','Adoption good practices'})
insert_before('en','sentry','First QA-oriented use',['How to start safely','Start with the official Sentry documentation and a controlled non-production project. Confirm SDK/platform support, data-scrubbing rules and access permissions before sending events. Generate a known test exception, verify that it reaches the expected project and only then expand instrumentation and release correlation.'])
rm('es','sentry',{'Qué es y dónde encaja'})

# OWASP: EN had adoption text instead of the safe-start block in PT/ES.
replace('en','owasp','Adoption good practices',['How to start safely','Start with OWASP official material such as the Web Security Testing Guide and select a small, authorized test scope. Map the application, authentication and sensitive flows, define evidence and stop conditions, and never perform intrusive security testing against systems without explicit authorization.'])
# Put it before First QA-oriented use to mirror PT.
a=d['owasp']['en']['sections']; s=next(x for x in a if x[0]=='How to start safely'); a.remove(s); insert_before('en','owasp','First QA-oriented use',s)

# Burp Suite: replace generic adoption with safe start; ES missed real-project block.
replace('en','burp-suite','Adoption good practices',['How to start safely','Use Burp Suite only in environments and targets for which you have authorization. Start by configuring the proxy and browser, validate interception with a harmless request, install/trust the CA certificate only where necessary, and prefer passive/manual analysis before any active or automated action.'])
a=d['burp-suite']['en']['sections']; s=next(x for x in a if x[0]=='How to start safely'); a.remove(s); insert_before('en','burp-suite','First QA-oriented use',s)
insert_before('es','burp-suite','Problemas comunes y troubleshooting',['Uso en un proyecto real','Defina qué flujos se analizarán con Burp Suite, quién puede interceptar tráfico, cómo se protegen credenciales y datos, qué evidencias se conservarán y qué acciones activas están autorizadas. Integre los hallazgos con el proceso de defectos y seguridad del equipo.'])

# Sauce Labs / LambdaTest: align to the 10 PT concepts and fix PT contamination in EN/ES.
cloud_data={
'sauce-labs':{
 'en_install':'Sauce Labs is a cloud platform; there is no local Sauce Labs server to install for normal use. Create an account, obtain the credentials required by the platform and integrate your test framework/driver with the remote endpoint. Install only the client libraries or tunnel component required by your chosen workflow.',
 'es_install':'Sauce Labs es una plataforma cloud; para el uso normal no se instala un servidor Sauce Labs local. Cree una cuenta, obtenga las credenciales requeridas e integre su framework/driver con el endpoint remoto. Instale solo las librerías cliente o el componente de túnel que requiera su flujo.',
 'en_qa':'Start with a small cross-browser/device scenario, choose the required platform/version, run it remotely and review video, logs and screenshots. Then expand the matrix based on product analytics, supported environments and risk instead of testing every combination.',
 'es_qa':'Comience con un escenario pequeño cross-browser/dispositivo, seleccione plataforma y versión, ejecútelo remotamente y revise video, logs y capturas. Después amplíe la matriz según analytics del producto, ambientes soportados y riesgo, evitando probar combinaciones sin criterio.',
 'en_real':'In a real project, define the supported browser/device matrix, concurrency limits, credential management, tunnel/network requirements, evidence retention and who owns failures caused by product, test or cloud environment.',
 'es_real':'En un proyecto real, defina la matriz soportada de navegadores/dispositivos, límites de concurrencia, gestión de credenciales, requisitos de túnel/red, retención de evidencias y responsables por fallos de producto, test o ambiente cloud.'},
'lambdatest':{
 'en_install':'LambdaTest is primarily a cloud testing platform. Create an account, obtain the access credentials and configure the remote grid/endpoint used by your framework. Install only the framework bindings, CLI or tunnel component required by the selected workflow; do not treat the cloud service itself as a local application.',
 'es_install':'LambdaTest es principalmente una plataforma cloud de pruebas. Cree una cuenta, obtenga las credenciales de acceso y configure el grid/endpoint remoto utilizado por su framework. Instale solo los bindings, CLI o túnel requeridos por el flujo elegido; no trate el servicio cloud como una aplicación local.',
 'en_qa':'Start with one representative browser/device scenario, execute it in the cloud and inspect logs, screenshots/video and network evidence. Expand the matrix from real user/browser data and product risk, not from an arbitrary list of combinations.',
 'es_qa':'Comience con un escenario representativo de navegador/dispositivo, ejecútelo en la nube y revise logs, capturas/video y evidencias de red. Amplíe la matriz a partir de datos reales de usuarios/navegadores y riesgo del producto, no de una lista arbitraria.',
 'en_real':'In a real project, define the supported matrix, concurrency, credential and secret handling, tunnel requirements, evidence retention and the triage process for failures across application, automation and cloud infrastructure.',
 'es_real':'En un proyecto real, defina matriz soportada, concurrencia, manejo de credenciales y secretos, requisitos de túnel, retención de evidencias y proceso de triage para fallos de aplicación, automatización e infraestructura cloud.'}}
for key,x in cloud_data.items():
    # remove legacy duplicate/generic sections in EN
    rm('en',key,{'When to use it','Adoption good practices','First QA-oriented use'})
    replace('en',key,'Installation and setup',['Installation and setup',x['en_install']])
    # after Best practices, add PT's "Como o QA aplica" concept
    insert_before('en',key,'How to start safely',['How QA applies it in practice',x['en_qa']])
    # existing Using real project becomes detailed
    replace('en',key,'Using it in a real project',['Using it in a real project',x['en_real']])
    # ES remove duplicate generic when-to-use, and add QA practical + real project
    rm('es',key,{'Cuándo utilizarlo'})
    replace('es',key,'Instalación y configuración',['Instalación y configuración',x['es_install']])
    insert_before('es',key,'Cómo comenzar con seguridad',['Cómo lo aplica QA en la práctica',x['es_qa']])
    insert_before('es',key,'Problemas comunes y troubleshooting',['Uso en un proyecto real',x['es_real']])

# k6: same structure already, but EN/ES were materially shallower than PT.
d['k6']['en']['sections']=[
['What k6 is','k6 is a Grafana tool for load and performance testing. Tests are defined as code and can evolve with the application, be versioned with the project and run locally or in CI/CD. For QA, it helps turn workload assumptions and performance expectations into repeatable checks instead of relying only on manual observation.'],
['What QA measures','Do not rely only on average response time. Review duration percentiles, failure rate, throughput, checks and application/infrastructure metrics. A test may have an acceptable average while a relevant portion of users experiences slow responses, so p90/p95/p99 and error behavior matter.'],
['Load scenarios','Model the workload according to the objective: a small performance smoke, expected average load, peak traffic, stress beyond normal capacity or a longer soak/endurance scenario. Define virtual users or arrival rate, ramp-up, duration and realistic test data based on expected usage rather than arbitrary numbers.'],
['Thresholds','Thresholds turn performance expectations into executable acceptance criteria. For example, define a maximum failure rate and a percentile target for request duration. A threshold should reflect a meaningful service expectation and make the test fail clearly when the agreed performance criterion is violated.'],
['First practical flow','Install k6 from the official source, validate with `k6 version`, create a small script with `k6 new` or your editor and run it with `k6 run`. Start with a controlled endpoint and low load, inspect checks and metrics, then increase complexity only after the basic script and environment are understood.'],
['CI/CD use','k6 can run in pipelines to detect performance regressions. Keep fast and deterministic checks in pull-request or deployment gates and schedule heavier load/stress/soak tests in appropriate environments and windows. Store results and compare trends so a pipeline does not become a source of noisy, unexplained failures.'],
['Attention point','Do not generate meaningful load against production systems or third-party services without explicit authorization, capacity planning and monitoring. Performance results depend on environment, data, network and backend conditions; document those conditions before comparing executions.']]
d['k6']['es']['sections']=[
['Qué es k6','k6 es una herramienta de Grafana para pruebas de carga y performance. Los tests se definen como código, pueden versionarse con el proyecto y ejecutarse localmente o en CI/CD. Para QA permite transformar supuestos de carga y expectativas de rendimiento en verificaciones repetibles, en lugar de depender solo de observación manual.'],
['Qué mide QA','No observe solamente el tiempo promedio. Revise percentiles de duración, tasa de fallos, throughput, checks y métricas de aplicación/infraestructura. Un promedio aceptable puede ocultar usuarios con respuestas lentas; por eso p90/p95/p99 y el comportamiento de errores son relevantes.'],
['Escenarios de carga','Modele la carga según el objetivo: smoke de performance, carga media esperada, pico, stress por encima de la capacidad normal o soak/endurance prolongado. Defina usuarios virtuales o arrival rate, ramp-up, duración y datos realistas basándose en el uso esperado, no en números arbitrarios.'],
['Thresholds','Los thresholds convierten expectativas de performance en criterios de aceptación ejecutables. Por ejemplo, defina una tasa máxima de fallos y un objetivo de percentil para la duración. El threshold debe representar una expectativa útil del servicio y hacer fallar el test cuando se incumpla el criterio acordado.'],
['Primer flujo práctico','Instale k6 desde la fuente oficial, valide con `k6 version`, cree un script pequeño con `k6 new` o su editor y ejecútelo con `k6 run`. Comience con un endpoint controlado y poca carga, revise checks y métricas y aumente la complejidad solo después de comprender el script y el ambiente.'],
['Uso en CI/CD','k6 puede ejecutarse en pipelines para detectar regresiones de performance. Mantenga checks rápidos y deterministas en gates de pull request/deploy y programe pruebas más pesadas de carga, stress o soak en ambientes y horarios adecuados. Conserve resultados y compare tendencias.'],
['Punto de atención','No genere carga relevante contra producción o servicios de terceros sin autorización explícita, planificación de capacidad y monitoreo. Los resultados dependen de ambiente, datos, red y backend; documente esas condiciones antes de comparar ejecuciones.']]

# ZAP: same structure but shallow EN/ES; align depth with PT.
d['zap']['en']['sections']=[
['What OWASP ZAP is','OWASP ZAP (Zed Attack Proxy) is an open-source web application security testing tool maintained within the OWASP ecosystem. It can work as an intercepting proxy and perform passive and active analysis, helping QA include DAST-oriented checks in authorized test environments.'],
['Passive Scan','Passive Scan analyzes traffic that passes through ZAP without actively attacking the target. It can highlight headers, cookie attributes, mixed content and other observable security signals, making it a useful starting point because it has lower risk of changing application state.'],
['Active Scan','Active Scan sends requests designed to probe potential vulnerabilities. It is intrusive and can change data or affect availability, so use it only against explicitly authorized targets and controlled environments, with scope, credentials and stop conditions agreed in advance.'],
['Quick Start and proxy','Use Quick Start for guided exploration or configure the browser/application to proxy traffic through ZAP. Confirm the target scope, HTTPS certificate handling and authentication before scanning. Start by navigating the application and reviewing passive findings before enabling more invasive actions.'],
['QA and DAST in CI','ZAP can support automated DAST checks in CI/CD, but the pipeline should define the target, authentication, baseline policy, accepted risk and failure criteria. Treat findings as inputs for triage rather than assuming every alert is a confirmed vulnerability; correlate with evidence and security review.'],
['Attention point','Security testing must be authorized. Never run active scans against production, third-party systems or environments outside the agreed scope. Protect credentials and captured traffic, avoid exposing sensitive data in reports and involve security specialists for high-impact findings.']]
d['zap']['es']['sections']=[
['Qué es OWASP ZAP','OWASP ZAP (Zed Attack Proxy) es una herramienta open source para pruebas de seguridad de aplicaciones web dentro del ecosistema OWASP. Puede funcionar como proxy de interceptación y realizar análisis pasivo y activo, ayudando a QA a incorporar verificaciones orientadas a DAST en ambientes autorizados.'],
['Passive Scan','Passive Scan analiza el tráfico que pasa por ZAP sin atacar activamente el objetivo. Puede señalar headers, atributos de cookies, mixed content y otras señales observables de seguridad. Es un buen punto de inicio porque tiene menor riesgo de modificar el estado de la aplicación.'],
['Active Scan','Active Scan envía requests diseñados para investigar posibles vulnerabilidades. Es intrusivo y puede modificar datos o afectar disponibilidad; úselo solo contra objetivos explícitamente autorizados y ambientes controlados, con alcance, credenciales y condiciones de parada acordadas.'],
['Quick Start y proxy','Use Quick Start para una exploración guiada o configure navegador/aplicación para enviar tráfico por ZAP. Confirme alcance, manejo de certificados HTTPS y autenticación antes de escanear. Comience navegando y revisando hallazgos pasivos antes de acciones más invasivas.'],
['QA y DAST en CI','ZAP puede apoyar checks DAST automatizados en CI/CD, pero el pipeline debe definir objetivo, autenticación, política baseline, riesgo aceptado y criterios de fallo. Trate los hallazgos como entradas para triage y no como vulnerabilidades confirmadas automáticamente; correlacione evidencia y revisión de seguridad.'],
['Punto de atención','Las pruebas de seguridad requieren autorización. Nunca ejecute scans activos contra producción, terceros o ambientes fuera del alcance acordado. Proteja credenciales y tráfico capturado, evite datos sensibles en reportes e involucre especialistas de seguridad en hallazgos de alto impacto.']]

# Ensure insights lengths and exact section-count parity for every final-lot topic.
for key in lot7:
    n=len(d[key]['pt'].get('sections',[]))
    for lang in ['en','es']:
        m=len(d[key][lang].get('sections',[]))
        if m!=n:
            raise SystemExit(f'COUNT MISMATCH {key}: pt={n} {lang}={m}')
        if 'insights' in d[key]['pt']:
            cur=d[key][lang].get('insights',[])
            if len(cur)<n: cur += [{} for _ in range(n-len(cur))]
            elif len(cur)>n: cur=cur[:n]
            d[key][lang]['insights']=cur
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('LOT7 UPDATED',len(lot7))
