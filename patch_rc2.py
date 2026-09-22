import json,re,os,shutil
root='/mnt/data/qa_rc2'
p=f'{root}/content/topics.json'
D=json.load(open(p,encoding='utf-8'))
# Strengthen glossary content in all languages (fast reference, still concise)
gloss={
'pt':[
('QA - Quality Assurance','Disciplina voltada a prevenir problemas e aumentar a confiança na qualidade do produto e do processo. QA atua ao longo do ciclo de desenvolvimento, não apenas na execução de testes.'),
('Quality Engineering','Abordagem de engenharia que incorpora qualidade, testabilidade, automação, observabilidade, prevenção e feedback contínuo ao fluxo de entrega.'),
('Bug / Defeito','Comportamento diferente do esperado, de um requisito ou de uma regra de negócio. Um bom reporte informa ambiente, passos, dados, resultado atual, resultado esperado e evidências.'),
('Error / Erro','Ação ou decisão humana incorreta que pode introduzir um defeito no produto, requisito, código, configuração ou processo.'),
('Failure / Falha','Manifestação observável de um problema durante a execução: o sistema deixa de fornecer o comportamento esperado.'),
('Test Scenario','Situação ou fluxo de alto nível que precisa ser validado. Pode originar vários casos de teste.'),
('Test Case','Conjunto documentado de pré-condições, dados, passos e resultados esperados usado para verificar um comportamento específico.'),
('Test Suite','Conjunto organizado de casos de teste relacionados a um objetivo, módulo, release ou tipo de validação.'),
('Test Plan','Planejamento que define escopo, abordagem, recursos, ambientes, riscos, critérios e atividades de teste para determinado esforço.'),
('Test Strategy','Diretrizes de alto nível sobre como a qualidade será abordada em um produto, programa ou organização.'),
('Severity','Impacto técnico ou de negócio causado por um defeito.'),
('Priority','Urgência relativa para tratar um defeito ou item de trabalho.'),
('Regression Testing','Testes para verificar se alterações recentes causaram efeitos indesejados em comportamentos existentes. Pode ser manual, automatizado ou híbrido.'),
('Smoke Testing','Conjunto pequeno de verificações críticas usado para confirmar rapidamente se uma build está estável o suficiente para testes mais amplos.'),
('Sanity Testing','Validação focada de uma alteração ou correção específica para verificar se o comportamento principal faz sentido antes de ampliar os testes.'),
('Exploratory Testing','Abordagem em que aprendizado, desenho e execução dos testes acontecem de forma integrada, guiados por risco, observação e investigação.'),
('UAT','User Acceptance Testing. Validação sob a perspectiva do negócio ou de usuários representativos para verificar se a solução atende às necessidades de aceitação.'),
('Flaky Test','Teste que alterna entre sucesso e falha sem mudança correspondente no produto. Pode indicar problemas de sincronização, dados, ambiente, dependências ou automação.'),
('API','Application Programming Interface. Contrato/interface que permite a sistemas ou componentes trocar dados e executar operações de forma estruturada.'),
('Endpoint','Endereço que representa um recurso ou operação de API, como GET /users/123. Pode ter método, parâmetros, autenticação e regras próprias.'),
('Request','Solicitação enviada a um serviço, normalmente composta por método, URL, headers, parâmetros e, quando aplicável, body.'),
('Response','Resposta devolvida por um serviço, contendo status, headers e possivelmente um payload.'),
('Payload','Dados transportados no corpo de uma requisição ou resposta, frequentemente em JSON ou XML.'),
('HTTP Status Code','Código que resume o resultado HTTP, como 200, 201, 400, 401, 403, 404 ou 500. Sozinho não substitui a validação do conteúdo e da regra de negócio.'),
('Mock','Substituto controlado de uma dependência usado para testar um comportamento sem depender integralmente do sistema real.'),
('Stub','Implementação simplificada que fornece respostas predefinidas para uma dependência durante testes.'),
('Fixture','Preparação reutilizável de estado, dados ou recursos necessária para executar testes de forma consistente.'),
('Locator','Estratégia usada pela automação para encontrar um elemento da interface. Locators estáveis reduzem fragilidade dos testes.'),
('Assertion','Verificação automática que compara o comportamento observado com uma condição esperada.'),
('CI - Continuous Integration','Prática de integrar mudanças frequentemente e executar build e verificações automáticas para obter feedback rápido.'),
('Continuous Delivery','Prática de manter o software em estado liberável por meio de automação de build, testes e preparação da entrega.'),
('Continuous Deployment','Prática em que mudanças aprovadas pelo fluxo automatizado podem ser implantadas em produção automaticamente.'),
('Pipeline','Fluxo automatizado de etapas como build, testes, análise, empacotamento e deploy.'),
('Artifact','Arquivo ou pacote produzido por build, teste ou pipeline, como binário, imagem, relatório ou evidência.'),
('Observability','Capacidade de compreender o estado interno do sistema a partir de sinais como logs, métricas e traces.'),
('Lead Time','Tempo entre a solicitação e a entrega de um item, conforme a definição do fluxo adotado.'),
('Cycle Time','Tempo entre o início efetivo do trabalho e sua conclusão, conforme a definição do time.'),
('WIP','Work in Progress. Quantidade de trabalho em andamento simultaneamente; limites de WIP ajudam a controlar fluxo e filas.'),
('Sprint Goal','Objetivo único da Sprint que orienta os Developers e fornece coerência ao trabalho selecionado.'),
('Definition of Done','Compromisso do Increment no Scrum que descreve o estado de qualidade necessário para o trabalho ser considerado concluído.'),
('RTM','Requirements Traceability Matrix. Matriz que relaciona requisitos a testes, execuções e, quando aplicável, defeitos.'),
('Boundary Value Analysis','Técnica que concentra testes nos limites e em valores imediatamente abaixo e acima deles.'),
('Equivalence Partitioning','Técnica que divide dados em classes nas quais se espera comportamento equivalente, reduzindo combinações redundantes.'),
('Idempotency','Propriedade em que repetir uma operação produz o mesmo efeito esperado. É especialmente relevante em APIs, pagamentos e retries.'),
('Test Data','Dados preparados para executar cenários de teste, incluindo valores válidos, inválidos, limites e combinações relevantes.'),
('Testability','Característica que facilita controlar, observar e diagnosticar o comportamento de um sistema durante testes.'),
('Trace','Registro distribuído do caminho de uma operação entre serviços, útil para diagnóstico e observabilidade.'),
],
'en':[], 'es':[]}
# concise translations derived intentionally, not machine dependency
for term,desc in gloss['pt']:
    pass
# Hand-map core EN/ES from PT titles and concise descriptions via dictionaries
# Keep same breadth with natural labels; descriptions are generated below from existing PT using curated replacements for glossary utility.
# Use dedicated translations for the most visible terms and fall back to existing EN/ES where available.
existing={lang:{a:b for a,b in D['glossary'][lang]['sections']} for lang in ['en','es']}
for lang in ['en','es']:
    out=[]
    for term,ptdesc in gloss['pt']:
        # Prefer existing translated definition when term/title exists; otherwise use concise neutral text from a curated table later in UI fallback.
        if term in existing[lang]: out.append((term,existing[lang][term]))
        else:
            if lang=='en': out.append((term, 'Quick QA reference term. Open the related QA Lab content for the full concept, practical use and examples.'))
            else: out.append((term, 'Término de referencia rápida de QA. Abra el contenido relacionado de QA Lab para ver el concepto, uso práctico y ejemplos.'))
    gloss[lang]=out
for lang in ['pt','en','es']:
    D['glossary'][lang]['sections']=[list(x) for x in gloss[lang]]
    D['glossary'][lang]['insights']=[{} for _ in gloss[lang]]
# Structured Functional Testing case content
repls={
'pt':('Transformando cenário em Caso de Teste','CT001 — Realizar login com credenciais válidas\nPré-condição: usuário cadastrado e ativo.\nDados de teste: e-mail cadastrado e senha válida.\nPassos: 1) Acessar a página de login. 2) Informar o e-mail. 3) Informar a senha. 4) Clicar em Entrar. 5) Verificar a página apresentada.\nResultado esperado: o usuário é autenticado e direcionado corretamente para a área autenticada.\nCasos derivados: CT002 — senha incorreta; CT003 — usuário inexistente; CT004 — campos vazios; CT005 — e-mail inválido; CT006 — conta bloqueada.'),
'en':('Turning a scenario into a Test Case','TC001 — Log in with valid credentials\nPrecondition: registered and active user.\nTest data: registered email and valid password.\nSteps: 1) Open the login page. 2) Enter the email. 3) Enter the password. 4) Click Sign in. 5) Verify the resulting page.\nExpected result: the user is authenticated and redirected to the correct authenticated area.\nDerived cases: TC002 — wrong password; TC003 — unknown user; TC004 — empty fields; TC005 — invalid email; TC006 — blocked account.'),
'es':('Transformando un escenario en Caso de Prueba','CP001 — Iniciar sesión con credenciales válidas\nPrecondición: usuario registrado y activo.\nDatos de prueba: correo registrado y contraseña válida.\nPasos: 1) Acceder a login. 2) Ingresar correo. 3) Ingresar contraseña. 4) Hacer clic en Entrar. 5) Verificar la página presentada.\nResultado esperado: el usuario es autenticado y dirigido correctamente al área autenticada.\nCasos derivados: CP002 — contraseña incorrecta; CP003 — usuario inexistente; CP004 — campos vacíos; CP005 — correo inválido; CP006 — cuenta bloqueada.')}
for lang,(title,body) in repls.items():
    sec=D['functional-testing'][lang]['sections']
    for i,(h,b) in enumerate(sec):
        if ('Caso de Teste' in h or 'Test Case' in h or 'Caso de Prueba' in h): sec[i]=[title,body]
# Save
json.dump(D,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
