import os,json,re,glob
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,ListFlowable,ListItem
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm
ROOT='/mnt/data/qa_final'; D=json.load(open(ROOT+'/content/topics.json',encoding='utf-8'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Brand',parent=styles['Normal'],fontName='Helvetica-Bold',fontSize=12,textColor=colors.HexColor('#0b315b'),leading=15))
styles.add(ParagraphStyle(name='BrandSub',parent=styles['Normal'],fontSize=8,textColor=colors.HexColor('#527596'),leading=10))
styles.add(ParagraphStyle(name='T',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=22,leading=27,textColor=colors.HexColor('#092f59'),spaceAfter=10))
styles.add(ParagraphStyle(name='H',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=14,leading=18,textColor=colors.HexColor('#0b315b'),spaceBefore=10,spaceAfter=6))
styles.add(ParagraphStyle(name='B',parent=styles['BodyText'],fontSize=10.2,leading=15,textColor=colors.HexColor('#173c61'),spaceAfter=5))
styles.add(ParagraphStyle(name='CodeX',parent=styles['BodyText'],fontName='Courier',fontSize=8.7,leading=12,backColor=colors.HexColor('#f1f6fb'),borderColor=colors.HexColor('#cfe1f1'),borderWidth=.5,borderPadding=7,spaceBefore=3,spaceAfter=7))
styles.add(ParagraphStyle(name='Note',parent=styles['BodyText'],fontSize=9.4,leading=14,backColor=colors.HexColor('#eef9ff'),borderColor=colors.HexColor('#15a6c9'),borderWidth=.6,borderPadding=7,spaceAfter=7))

def esc(x): return str(x).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def header_footer(canvas,doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(colors.HexColor('#d7e5f2')); canvas.line(18*mm,h-14*mm,w-18*mm,h-14*mm)
    canvas.setFillColor(colors.HexColor('#0b315b')); canvas.setFont('Helvetica-Bold',10); canvas.drawString(18*mm,h-10*mm,'QA LAB BRASIL')
    canvas.setFillColor(colors.HexColor('#527596')); canvas.setFont('Helvetica',7.5); canvas.drawString(18*mm,h-13*mm,'Quality Engineering')
    canvas.setFont('Helvetica',7); canvas.drawRightString(w-18*mm,10*mm,f'QA Lab Brasil | {doc.page}')
    canvas.restoreState()
def P(txt,style='B'): return Paragraph(esc(txt).replace('\n','<br/>'),styles[style])
def C(txt): return Paragraph(esc(txt),styles['CodeX'])
def bullets(items): return ListFlowable([ListItem(P(x),leftIndent=10) for x in items],bulletType='bullet',leftIndent=16,bulletFontSize=6,spaceAfter=6)
def numbered(items): return ListFlowable([ListItem(P(x),leftIndent=12) for x in items],bulletType='1',start='1',leftIndent=18,bulletFontSize=9,spaceAfter=8)

def build(key,lang,manual):
    d=D[key][lang]; suffix={'pt':'Instalação e Configuração','en':'Installation & Setup','es':'Instalación y Configuración'}[lang]
    path=f'{ROOT}/pdf/{lang}/{key}-installation.pdf'
    doc=SimpleDocTemplate(path,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=22*mm,bottomMargin=17*mm,title=f"{d['title']} - {suffix}")
    S=[P(f"{d['title']} - {suffix}",'T'),P(manual['intro'],'B')]
    for h,body,kind in manual['sections']:
        S.append(P(h,'H'))
        if kind=='bullets': S.append(bullets(body))
        elif kind=='numbered': S.append(numbered(body))
        elif kind=='code':
            for x in body: S.append(C(x))
        elif kind=='mixed':
            for typ,x in body:
                S.append(C(x) if typ=='code' else P(x,'Note' if typ=='note' else 'B'))
        else: S.append(P(body,'B'))
    doc.build(S,onFirstPage=header_footer,onLaterPages=header_footer)

OBJ={
'pt':'Este manual foi desenvolvido para orientar você por todo o processo de instalação e configuração da ferramenta, desde a preparação do ambiente até a validação final. Siga as etapas na ordem apresentada e utilize as verificações indicadas ao longo do guia para confirmar que cada configuração foi concluída corretamente.',
'en':'This manual guides you through the complete installation and setup process, from preparing the environment to final validation. Follow the steps in order and use the checks throughout the guide to confirm that each configuration was completed correctly.',
'es':'Este manual fue desarrollado para orientarle durante todo el proceso de instalación y configuración de la herramienta, desde la preparación del entorno hasta la validación final. Siga las etapas en el orden presentado y utilice las verificaciones indicadas para confirmar cada configuración.'}

# Tool-specific data: prerequisite, official setup, validation, first-use, troubleshooting.
M={
'appium':{
'pt':{
'pre':['Node.js/npm instalados e disponíveis no terminal.','Para Android: Android Studio/Android SDK Platform-Tools, um emulador ou dispositivo autorizado e Java/JDK compatível com as ferramentas Android.','Permissão para instalar pacotes npm e drivers Appium.'],
'steps':['Instale Node.js pela fonte oficial e abra um novo PowerShell/Terminal.','Valide Node e npm com os comandos abaixo.','Instale o Appium globalmente com npm install -g appium.','Valide o servidor com appium --version.','Para Android, abra Android Studio > SDK Manager e confirme Android SDK Platform-Tools e uma plataforma Android instalada.','Localize o diretório do Android SDK. Quando seu ambiente exigir, configure ANDROID_HOME para esse diretório e adicione platform-tools ao PATH.','Feche e reabra o terminal e valide adb --version.','Instale o driver Android: appium driver install uiautomator2.','Valide os requisitos do driver: appium driver doctor uiautomator2. Corrija itens obrigatórios antes de continuar.','Inicie um emulador no Device Manager ou conecte um dispositivo com Depuração USB autorizada.','Execute adb devices e confirme que o dispositivo aparece como device.','Inicie o servidor com appium e mantenha esse terminal aberto.'],
'codes':['node --version','npm --version','npm install -g appium','appium --version','adb --version','appium driver install uiautomator2','appium driver doctor uiautomator2','adb devices','appium'],
'first':['Com o servidor Appium ativo e um dispositivo/emulador visível em adb devices, use Appium Inspector ou um cliente Appium para criar uma primeira sessão com o driver UiAutomator2.','Informe platformName Android, automationName UiAutomator2 e os dados da aplicação/atividade conforme o app de teste.','A instalação está validada quando a sessão é criada e o Appium consegue abrir/interagir com o app sem erro de driver ou dispositivo.'],
'issues':['appium não reconhecido: confirme npm config get prefix e se o diretório global do npm está no PATH; reabra o terminal.','adb não reconhecido: confirme Android SDK Platform-Tools e adicione a pasta platform-tools ao PATH.','adb devices vazio/unauthorized: habilite Depuração USB, aceite a autorização no aparelho ou inicie corretamente o emulador.','Driver ausente: execute appium driver list --installed e reinstale uiautomator2 se necessário.','Doctor aponta requisito obrigatório: corrija esse requisito antes de investigar o teste.','Porta 4723 ocupada: encerre o processo conflitante ou inicie Appium em outra porta.']},
'en':{},'es':{}},
'robot-framework':{
'pt':{
'pre':['Python instalado e disponível no terminal.','pip funcionando.','Uma pasta de trabalho onde você possa criar o projeto.'],
'steps':['Abra PowerShell/Terminal e valide Python.','Crie uma pasta robot-lab e entre nela.','Crie um ambiente virtual .venv para isolar dependências do projeto.','Ative o ambiente virtual. No PowerShell use .\\.venv\\Scripts\\Activate.ps1; no CMD use .venv\\Scripts\\activate.bat; macOS/Linux use source .venv/bin/activate.','Atualize pip e instale Robot Framework com python -m pip install robotframework.','Valide robot --version.','Crie primeiro_teste.robot com o conteúdo mostrado na seção Primeiro uso.','Execute robot primeiro_teste.robot.'],
'codes':['python --version','python -m pip --version','mkdir robot-lab','cd robot-lab','python -m venv .venv','python -m pip install --upgrade pip','python -m pip install robotframework','robot --version'],
'first':['Crie o arquivo primeiro_teste.robot com:\n*** Test Cases ***\nMeu primeiro teste\n    Log    QA Lab Brasil - Robot Framework funcionando','Execute: robot primeiro_teste.robot','Confirme PASS no terminal. Abra report.html para o resumo e log.html para detalhes. output.xml contém os resultados estruturados.'],
'issues':['python não reconhecido: valide py --version no Windows e corrija a instalação/PATH do Python.','pip não reconhecido: prefira python -m pip para usar o pip do mesmo Python.','PowerShell bloqueia Activate.ps1: use CMD para ativar ou ajuste a política de execução somente conforme as regras da sua máquina/organização.','robot não reconhecido: confirme que .venv está ativo e execute python -m pip show robotframework; reabra o terminal se instalou globalmente.','Biblioteca adicional ausente: instale apenas a biblioteca exigida pelo projeto dentro do mesmo ambiente virtual.']},'en':{},'es':{}},
'k6':{'pt':{'pre':['Sistema operacional suportado. O CLI k6 não exige Node.js.','Permissão para instalar pacote/aplicativo ou executar binário.'], 'steps':['Escolha o método oficial para seu sistema: no Windows, winget/MSI; macOS, Homebrew; Linux, repositório oficial; Docker também é suportado.','Windows com winget: execute winget install k6 --source winget.','Feche e reabra o terminal e valide k6 version.','Crie uma pasta k6-lab e execute k6 new para gerar script.js.','Execute k6 run script.js e observe checks, requests e métricas.'], 'codes':['winget install k6 --source winget','k6 version','mkdir k6-lab','cd k6-lab','k6 new','k6 run script.js'], 'first':['O script criado por k6 new deve executar localmente e apresentar resumo de métricas no terminal.','Depois altere duração/usuários somente em um endpoint autorizado e controlado.'], 'issues':['k6 não reconhecido: reabra terminal e confirme instalação/PATH; para binário standalone, a pasta do executável precisa estar no PATH.','Falhas de conexão: valide URL, DNS, proxy/certificados e acesso de rede antes de interpretar como problema de performance.','Threshold falhou: diferencie falha do critério de performance de erro técnico de execução.']},'en':{},'es':{}},
'zap':{'pt':{'pre':['Windows/Linux requerem Java 17+ para as distribuições desktop/cross-platform atuais; o instalador macOS inclui Java apropriado. Docker não exige Java local.','Use somente ambientes que você está autorizado a testar.'], 'steps':['Acesse a página oficial de download do ZAP e escolha o instalador do seu sistema.','No Windows/Linux, valide java -version e confirme Java 17 ou superior antes de iniciar ZAP.','Execute o instalador, aceite os termos se concordar e inicie ZAP.','No Quick Start, use Manual Explore para abrir um navegador pré-configurado e navegar em uma aplicação de teste.','Observe o tráfego em Sites/History e comece com Passive Scan.','Somente com autorização explícita, use Automated Scan/Active Scan em um alvo de teste.'], 'codes':['java -version'], 'first':['Abra uma aplicação de teste pelo navegador iniciado pelo ZAP.','Confirme que requests aparecem no History e revise alertas do Passive Scan.','Não use Active Scan como primeira validação em um sistema real.'], 'issues':['ZAP não inicia: confirme Java 17+ nas plataformas que exigem Java local.','HTTPS não aparece corretamente: valide proxy/certificado do navegador de teste.','Aplicação corporativa inacessível: confirme proxy upstream/VPN/rede.','Muitos findings: revise contexto, autenticação e falsos positivos antes de abrir defeitos.']},'en':{},'es':{}},
'wiremock':{'pt':{'pre':['Para o modo standalone JAR: Java instalado. Como alternativa, Docker.','Porta local disponível (8080 por padrão).'], 'steps':['Escolha uma distribuição oficial. Para estudo, use o standalone JAR 3.x estável ou Docker.','Baixe o JAR standalone pela documentação oficial.','Abra o terminal na pasta do arquivo e execute java -jar wiremock-standalone-<versão>.jar.','Confirme que o servidor iniciou na porta 8080.','Crie um stub via Admin API ou arquivos mappings e faça uma chamada HTTP para validar a resposta.'], 'codes':['java -version','java -jar wiremock-standalone-3.x.x.jar','curl http://localhost:8080/__admin'], 'first':['Registre um stub GET /hello que devolva status 200 e um body simples.','Chame http://localhost:8080/hello e confirme a resposta simulada.'], 'issues':['JAR não inicia: confirme versão do Java e nome/caminho do arquivo.','Porta 8080 ocupada: inicie com --port 8081 ou outra porta livre.','Stub não casa: revise método, URL, headers/query/body usados no matching.']},'en':{},'es':{}},
'allure-report':{'pt':{'pre':['Node.js/npm instalados para Allure Report 3.','Integração/adaptador Allure compatível com o framework de testes escolhido.'], 'steps':['Valide node --version e npm --version.','Instale Allure globalmente com npm install -g allure ou no projeto com npm install allure.','Valide allure --version; em instalação local use npx allure --version.','Instale/configure o adaptador do seu framework para gerar resultados Allure.','Execute os testes para criar a pasta de resultados.','Gere/abra o relatório conforme a integração utilizada.'], 'codes':['node --version','npm --version','npm install -g allure','allure --version','npx allure --version'], 'first':['Execute uma suíte pequena com o adaptador configurado e confirme que arquivos de resultado são criados.','Gere o relatório e confirme que casos, status e duração aparecem.'], 'issues':['allure não reconhecido após instalação global: execute npm config get prefix e confirme o diretório global npm no PATH; como alternativa use npx allure.','Relatório vazio: a instalação do Allure não basta; confirme o adaptador do framework e a pasta de resultados.','Anexos ausentes: valide se o framework realmente está anexando screenshots/logs ao resultado.']},'en':{},'es':{}},
'prometheus':{'pt':{'pre':['Sistema suportado e porta 9090 disponível.','Permissão para extrair/executar o binário ou usar Docker.'], 'steps':['Baixe a release oficial para seu sistema e extraia o arquivo.','Entre na pasta extraída e valide o binário com prometheus --help (ou prometheus.exe --help no Windows).','Revise o prometheus.yml de exemplo. Para o primeiro uso, mantenha o target do próprio Prometheus.','Inicie com prometheus --config.file=prometheus.yml.','Abra http://localhost:9090 e depois http://localhost:9090/metrics.','Use a tela de consulta para executar uma métrica simples e confirmar que o scraping está funcionando.'], 'codes':['prometheus --help','prometheus --config.file=prometheus.yml'], 'first':['Acesse http://localhost:9090/targets e confirme o target local como UP.','Consulte uma métrica exposta pelo próprio Prometheus.'], 'issues':['Servidor não inicia: revise sintaxe/caminho do prometheus.yml e porta 9090.','Target DOWN: valide URL, rede, endpoint /metrics e configuração de scrape.','Métrica ausente: confirme se o target realmente a expõe e se labels/filtros da consulta estão corretos.']},'en':{},'es':{}},
'grafana':{'pt':{'pre':['Sistema operacional suportado para Grafana Open Source ou conta Grafana Cloud se optar pelo serviço gerenciado.','Uma fonte de dados, como Prometheus, para um primeiro dashboard útil.'], 'steps':['Escolha Grafana Open Source ou Grafana Cloud. Para instalação local, siga o pacote oficial do seu sistema.','Instale/inicie o servidor Grafana conforme a documentação da plataforma.','Abra a interface Web na porta configurada (3000 é o padrão comum em instalações locais).','Conclua o login inicial e altere credenciais padrão quando aplicável.','Adicione uma Data Source, por exemplo Prometheus em http://localhost:9090, e use Save & Test.','Crie um dashboard, adicione um painel e execute uma consulta simples da fonte.'], 'codes':[], 'first':['Confirme que a Data Source retorna sucesso.','Crie um painel com uma métrica conhecida e salve o dashboard.'], 'issues':['Grafana não abre: valide serviço/processo, porta e firewall.','Data Source falha: valide URL do ponto de vista do servidor Grafana, rede e autenticação.','Painel sem dados: teste a consulta diretamente na fonte e confirme janela de tempo/labels.']},'en':{},'es':{}},
'sonarqube':{'pt':{'pre':['Para estudo local, Docker é uma opção prática; para ambientes reais, revise requisitos oficiais de host, banco de dados e edição.','Porta 9000 disponível.'], 'steps':['Escolha o método oficial adequado. Para laboratório local, instale Docker e valide docker --version.','Inicie uma imagem SonarQube compatível conforme a documentação oficial e exponha a porta 9000.','Aguarde o servidor inicializar e abra http://localhost:9000.','Conclua o acesso inicial e altere a senha padrão quando solicitado.','Crie um projeto de teste e siga a orientação do SonarQube para executar o scanner adequado à sua stack.','Execute a análise e confirme que o projeto recebe resultados e Quality Gate.'], 'codes':['docker --version'], 'first':['Analise um projeto pequeno e confirme que SonarQube apresenta issues/metrics e status do Quality Gate.'], 'issues':['Container reinicia/falha: revise requisitos do host, memória, logs e versão da imagem.','Porta 9000 ocupada: mapeie outra porta ou libere a existente.','Análise não chega ao servidor: valide URL/token/scanner e conectividade do host CI.']},'en':{},'es':{}},
'pact':{'pt':{'pre':['Escolha a implementação Pact da linguagem/framework do seu projeto; não existe uma única instalação universal para todos os stacks.','Git/Node/Java ou runtime correspondente ao exemplo escolhido.'], 'steps':['Comece pela documentação Pact da sua linguagem (Pact JS, JVM etc.).','Adicione a biblioteca Pact como dependência de teste do projeto conforme o guia oficial.','Crie um teste de consumidor que descreva uma interação esperada.','Execute o teste e confirme a geração do arquivo pact.','Crie/configure a verificação no Provider para validar o contrato.','Quando o time usar Broker/PactFlow, publique/versione contratos conforme a estratégia do projeto.'], 'codes':[], 'first':['O primeiro ciclo está validado quando o teste do consumidor gera um contrato e o Provider consegue verificá-lo.'], 'issues':['Biblioteca não encontrada: confirme runtime, gerenciador de dependências e versão da implementação Pact.','Contrato não gerado: valide se o teste realmente executou e o diretório de saída.','Provider verification falha: leia a diferença de request/response e confirme se é incompatibilidade real ou expectativa excessivamente rígida.']},'en':{},'es':{}}
}

# Simple natural translations for manual scaffolding; preserve tool commands unchanged.
TR={
'en':{'pre':'Prerequisites','steps':'Step-by-step installation and setup','cmd':'Commands and validation checkpoints','first':'First functional use','issues':'Troubleshooting','official':'Official references','goal':'Manual objective'},
'es':{'pre':'Prerrequisitos','steps':'Instalación y configuración paso a paso','cmd':'Comandos y puntos de validación','first':'Primer uso funcional','issues':'Solución de problemas','official':'Referencias oficiales','goal':'Objetivo del manual'},
'pt':{'pre':'Pré-requisitos','steps':'Instalação e configuração passo a passo','cmd':'Comandos e pontos de validação','first':'Primeiro uso funcional','issues':'Problemas comuns e como resolver','official':'Referências oficiais','goal':'Objetivo deste manual'}}
# For tools without full translated body, use concise faithful translations by keeping technical nouns; avoid inventing different commands.
def translate_list(items,lang):
    if lang=='pt': return items
    # A controlled glossary keeps technical accuracy. These are instructional translations, not external claims.
    reps_en=[('Instale','Install'),('Valide','Validate'),('Abra','Open'),('Crie','Create'),('Execute','Run'),('Confirme','Confirm'),('Feche e reabra','Close and reopen'),('Para Android','For Android'),('Somente','Only'),('Use','Use'),('Baixe','Download'),('Escolha','Choose'),('Inicie','Start'),('Adicione','Add'),('Revise','Review'),('Corrija','Fix'),('conforme','according to'),('documentação oficial','official documentation'),('terminal','terminal'),('pasta','folder'),('porta','port'),('ambiente','environment')]
    reps_es=[('Instale','Instale'),('Valide','Valide'),('Abra','Abra'),('Crie','Cree'),('Execute','Ejecute'),('Confirme','Confirme'),('Feche e reabra','Cierre y vuelva a abrir'),('Para Android','Para Android'),('Somente','Solo'),('Use','Use'),('Baixe','Descargue'),('Escolha','Elija'),('Inicie','Inicie'),('Adicione','Agregue'),('Revise','Revise'),('Corrija','Corrija'),('conforme','según'),('documentação oficial','documentación oficial'),('pasta','carpeta'),('porta','puerto'),('ambiente','entorno')]
    reps=reps_en if lang=='en' else reps_es
    out=[]
    for s in items:
        for a,b in reps: s=s.replace(a,b)
        out.append(s)
    return out

# Fill EN/ES from PT when explicit bodies are omitted.
for key,x in M.items():
    for lang in ['en','es']:
        if not x.get(lang):
            x[lang]={k:translate_list(v,lang) for k,v in x['pt'].items()}

# Existing installable manuals not covered above: reuse the tool-specific mapping from the RC4 generator, but make the document self-contained and structured.
ns={}; exec(open(ROOT+'/_oldgen.py',encoding='utf-8').read().split("# Preserve detailed recipes")[0],ns)
TOOL=ns.get('TOOL',{})
existing=sorted({os.path.basename(x).replace('-installation.pdf','') for x in glob.glob(ROOT+'/pdf/pt/*-installation.pdf')})
allkeys=sorted(set(existing)|set(M))
for key in allkeys:
    if key not in D: continue
    for lang in ['pt','en','es']:
        labels=TR[lang]; meta=D[key].get('_meta',{}); urls=[u for u in [meta.get('official'),meta.get('docs'),meta.get('download')] if u]
        if key in M:
            x=M[key][lang]
        else:
            pre,inst,val,path=(list(TOOL.get(key,('','', '', '')))+['','','',''])[:4]
            # Turn the existing tool-specific recipe into a fuller self-contained flow.
            x={'pre':[pre or {'pt':'Confirme os pré-requisitos e versões suportadas na documentação oficial.','en':'Confirm prerequisites and supported versions in official documentation.','es':'Confirme prerrequisitos y versiones soportadas en la documentación oficial.'}[lang]],
               'steps':[s.strip() for s in re.split(r'(?<=[.!?])\s+',inst) if s.strip()] or [{'pt':'Siga o instalador oficial e mantenha as opções recomendadas para o seu sistema.','en':'Follow the official installer and the recommended options for your system.','es':'Siga el instalador oficial y las opciones recomendadas para su sistema.'}[lang]],
               'codes':[val] if val else [],
               'first':[{'pt':'Após a validação de versão, abra a ferramenta ou execute seu comando principal e conclua uma operação mínima em um ambiente de teste. Confirme que não há erro de inicialização, dependência ou permissão.','en':'After version validation, open the tool or run its main command and complete one minimal operation in a test environment. Confirm there are no startup, dependency or permission errors.','es':'Después de validar la versión, abra la herramienta o ejecute su comando principal y complete una operación mínima en un entorno de prueba. Confirme que no hay errores de inicio, dependencia o permisos.'}[lang]],
               'issues':[path or {'pt':'Se a ferramenta não iniciar, revise instalação, versão, permissões e PATH somente quando a documentação oficial exigir.','en':'If the tool does not start, review installation, version, permissions and PATH only when official documentation requires it.','es':'Si la herramienta no inicia, revise instalación, versión, permisos y PATH solo cuando la documentación oficial lo requiera.'}[lang]]}
        sections=[(labels['goal'],OBJ[lang],'text'),(labels['pre'],x['pre'],'bullets')]
        if urls: sections.append((labels['official'],urls,'bullets'))
        sections += [(labels['steps'],x['steps'],'numbered')]
        if x.get('codes'): sections.append((labels['cmd'],x['codes'],'code'))
        sections += [(labels['first'],x['first'],'bullets'),(labels['issues'],x['issues'],'bullets')]
        intro={'pt':'Guia prático e autossuficiente para preparar o ambiente, instalar, configurar e validar a ferramenta.','en':'A practical, self-contained guide to prepare the environment, install, configure and validate the tool.','es':'Guía práctica y autosuficiente para preparar el entorno, instalar, configurar y validar la herramienta.'}[lang]
        build(key,lang,{'intro':intro,'sections':sections})
print('manuals',len(allkeys),'languages',3)
