import json
p='/mnt/data/qa_rc3/content/topics.json';D=json.load(open(p,encoding='utf8'))
def seti(k,lang,i,**kw):
 d=D[k][lang]; ins=d.setdefault('insights',[{} for _ in d['sections']]);
 while len(ins)<=i: ins.append({})
 ins[i].update(kw)
# PT curated contextual cards
seti('mobile','pt',0,caution='Emuladores e simuladores aceleram a execução, mas não reproduzem perfeitamente câmera, biometria, sensores, bateria, desempenho, chamadas e condições reais de rede. Para fluxos críticos, combine-os com dispositivos físicos.')
seti('mobile','pt',1,good='Monte uma matriz mínima por risco: versões relevantes de Android/iOS, tamanhos de tela, fabricante quando houver impacto e pelo menos alguns dispositivos físicos para fluxos críticos.')
seti('mobile','pt',2,caution='Não valide apenas a permissão aceita. Teste negar, negar permanentemente, alterar a permissão nas configurações e retornar ao aplicativo.')
seti('mobile','pt',3,apply='Interrompa o fluxo com bloqueio de tela, troca de aplicativo, perda/retorno de rede, rotação e notificações. Verifique estado, dados e recuperação ao retornar.')
seti('functional-testing','pt',0,why='Grande parte dos defeitos percebidos pelo usuário está no comportamento das funcionalidades: login, cálculo, formulário, carrinho ou checkout. Teste funcional transforma requisitos e regras em evidências observáveis.')
seti('functional-testing','pt',1,apply='Comece pelo happy path e depois derive cenários negativos, alternativos e de limite. Para cada um, defina entrada, ação e resultado esperado sem duplicar casos desnecessariamente.')
seti('functional-testing','pt',8,good='Escreva passos reproduzíveis e resultados esperados objetivos. Evite frases como “o sistema deve funcionar corretamente”; descreva exatamente o que deve acontecer.')
seti('functional-testing','pt',8,caution='Um caso de teste não precisa validar tudo ao mesmo tempo. Casos excessivamente longos dificultam manutenção, diagnóstico e reutilização.')
seti('scrum','pt',0,caution='Scrum não é apenas um conjunto de reuniões e não deve ser tratado como uma metodologia prescritiva. É um framework leve baseado em empirismo e Lean Thinking.')
seti('scrum','pt',4,caution='A Daily Scrum não é reunião de status para o Scrum Master ou gestor. Seu objetivo é inspecionar o progresso em direção ao Sprint Goal e adaptar o Sprint Backlog.')
seti('devops','pt',0,caution='DevOps não é uma ferramenta, um cargo ou sinônimo de CI/CD. Ferramentas e pipelines apoiam práticas de colaboração, automação e feedback, mas não substituem a mudança de fluxo e responsabilidade compartilhada.')
seti('waterfall','pt',0,caution='Em fluxos muito sequenciais, problemas de requisito descobertos tarde podem gerar retrabalho elevado. Revisão antecipada de requisitos e testabilidade reduz esse risco.')
seti('kanban','pt',0,caution='Kanban não é apenas um quadro To Do / Doing / Done. Visualização sem políticas explícitas, gestão de WIP e melhoria do fluxo pode apenas tornar o acúmulo de trabalho mais visível.')
seti('lean','pt',0,caution='Lean não significa simplesmente cortar pessoas, documentação ou etapas. Remover uma atividade sem entender o valor e o risco pode aumentar defeitos e retrabalho.')
seti('testrail','pt',0,caution='TestRail organiza casos, execuções e resultados, mas não cria uma boa estratégia de testes sozinho. Repositórios sem manutenção podem acumular duplicações e casos obsoletos.')
seti('playwright','pt',0,good='Prefira locators orientados ao usuário, como getByRole e getByLabel, e assertions explícitas. Isso melhora legibilidade e reduz fragilidade.')
seti('java','pt',0,caution='Java, JDK, JRE e JVM não são sinônimos. Para compilar e desenvolver/testar ferramentas Java, normalmente você precisa de um JDK compatível com o projeto.')
seti('python','pt',0,caution='Evite instalar dependências de todos os projetos diretamente no Python global. Ambientes virtuais reduzem conflitos de versões e tornam a configuração reproduzível.')
# EN/ES contextual equivalents for core topics
pairs={
'mobile':{
'en':[(0,{'caution':'Emulators and simulators are fast, but they do not perfectly reproduce camera, biometrics, sensors, battery, performance, calls or real network conditions. Combine them with physical devices for critical flows.'}),(2,{'caution':'Do not test only permission granted. Cover deny, deny permanently, changing permission in system settings and returning to the app.'})],
'es':[(0,{'caution':'Emuladores y simuladores son rápidos, pero no reproducen perfectamente cámara, biometría, sensores, batería, rendimiento, llamadas o condiciones reales de red. Combine con dispositivos físicos en flujos críticos.'}),(2,{'caution':'No pruebe solo permiso aceptado. Cubra denegar, denegar permanentemente, cambiar el permiso en ajustes y volver a la aplicación.'})]},
'functional-testing':{
'en':[(0,{'why':'Many user-visible defects are functional: login, calculations, forms, carts or checkout. Functional testing turns requirements and rules into observable evidence.'}),(8,{'good':'Write reproducible steps and objective expected results. Avoid vague statements such as “the system should work correctly”.'})],
'es':[(0,{'why':'Muchos defectos visibles para el usuario son funcionales: login, cálculos, formularios, carrito o checkout. Las pruebas funcionales convierten requisitos y reglas en evidencia observable.'}),(8,{'good':'Escriba pasos reproducibles y resultados esperados objetivos. Evite frases vagas como “el sistema debe funcionar correctamente”.'})]},
'scrum':{'en':[(0,{'caution':'Scrum is not merely a set of meetings or a prescriptive methodology; it is a lightweight framework based on empiricism and Lean Thinking.'}),(4,{'caution':'Daily Scrum is not a status meeting for a manager or Scrum Master. Its purpose is to inspect progress toward the Sprint Goal and adapt the Sprint Backlog.'})], 'es':[(0,{'caution':'Scrum no es solo un conjunto de reuniones ni una metodología prescriptiva; es un framework ligero basado en empirismo y Lean Thinking.'}),(4,{'caution':'Daily Scrum no es una reunión de status para un gerente o Scrum Master. Su objetivo es inspeccionar el progreso hacia el Sprint Goal y adaptar el Sprint Backlog.'})]},
'devops':{'en':[(0,{'caution':'DevOps is not a tool, job title or synonym for CI/CD. Tools and pipelines support collaboration, automation and feedback but do not replace shared responsibility and flow improvement.'})], 'es':[(0,{'caution':'DevOps no es una herramienta, cargo ni sinónimo de CI/CD. Herramientas y pipelines apoyan colaboración, automatización y feedback, pero no sustituyen la responsabilidad compartida y la mejora del flujo.'})]},
'waterfall':{'en':[(0,{'caution':'In highly sequential flows, requirement problems found late can cause expensive rework. Early requirement and testability reviews reduce this risk.'})], 'es':[(0,{'caution':'En flujos muy secuenciales, problemas de requisitos descubiertos tarde pueden generar mucho retrabajo. Revisiones tempranas de requisitos y testabilidad reducen este riesgo.'})]},
'kanban':{'en':[(0,{'caution':'Kanban is not just a To Do / Doing / Done board. Visualization without explicit policies, WIP management and flow improvement may only make queues more visible.'})], 'es':[(0,{'caution':'Kanban no es solo un tablero To Do / Doing / Done. Visualización sin políticas explícitas, gestión de WIP y mejora del flujo puede solo hacer las colas más visibles.'})]},
'lean':{'en':[(0,{'caution':'Lean does not simply mean cutting people, documentation or steps. Removing work without understanding value and risk can increase defects and rework.'})], 'es':[(0,{'caution':'Lean no significa simplemente reducir personas, documentación o etapas. Eliminar trabajo sin entender valor y riesgo puede aumentar defectos y retrabajo.'})]},
'testrail':{'en':[(0,{'caution':'TestRail organizes cases, executions and results, but it does not create a good test strategy by itself. Unmaintained repositories can accumulate duplicate and obsolete cases.'})], 'es':[(0,{'caution':'TestRail organiza casos, ejecuciones y resultados, pero no crea por sí solo una buena estrategia de pruebas. Repositorios sin mantenimiento pueden acumular duplicados y casos obsoletos.'})]}}
for k,langs in pairs.items():
 for lang,rows in langs.items():
  for i,kw in rows:seti(k,lang,i,**kw)
json.dump(D,open(p,'w',encoding='utf8'),ensure_ascii=False,indent=2)
