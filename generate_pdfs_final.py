import json, os, re, runpy
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
ROOT='/mnt/data/qa_rc4'
D=json.load(open(ROOT+'/content/topics.json',encoding='utf8'))
# Load the prior tool-specific recipes, but do not use its generated PDFs as final.
ns=runpy.run_path(ROOT+'/_oldgen.py')
TOOL=ns.get('TOOL',{})
recipes=ns.get('recipes',{})
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='QABody',parent=styles['BodyText'],fontSize=10,leading=15,textColor=colors.HexColor('#294b68'),spaceAfter=4))
styles.add(ParagraphStyle(name='QASmall',parent=styles['BodyText'],fontSize=8.3,leading=11,textColor=colors.HexColor('#617b91')))
styles.add(ParagraphStyle(name='QACode',parent=styles['BodyText'],fontName='Courier',fontSize=8.4,leading=12,backColor=colors.HexColor('#f2f8fc'),borderColor=colors.HexColor('#c8deed'),borderWidth=.5,borderPadding=6,spaceBefore=4,spaceAfter=6))
styles.add(ParagraphStyle(name='QAHeading2',parent=styles['Heading2'],fontSize=15,leading=19,textColor=colors.HexColor('#123f6d'),spaceBefore=10,spaceAfter=6))
styles.add(ParagraphStyle(name='QAHeading3',parent=styles['Heading3'],fontSize=12,leading=15,textColor=colors.HexColor('#17649a'),spaceBefore=8,spaceAfter=4))

def esc(s):
 return re.sub(r'&(?!(amp|lt|gt|quot|apos);)','&amp;',str(s)).replace('<','&lt;').replace('>','&gt;')

def header_footer(canvas,doc):
 canvas.saveState(); w,h=A4
 # brand badge - vector logo mark + name
 canvas.setFillColor(colors.HexColor('#1769aa')); canvas.roundRect(18*mm,h-16*mm,10*mm,10*mm,2.5*mm,fill=1,stroke=0)
 canvas.setFillColor(colors.white); canvas.setFont('Helvetica-Bold',8.5); canvas.drawCentredString(23*mm,h-12.5*mm,'QA')
 canvas.setFillColor(colors.HexColor('#123f6d')); canvas.setFont('Helvetica-Bold',9.5); canvas.drawString(31*mm,h-10.7*mm,'QA LAB BRASIL')
 canvas.setFillColor(colors.HexColor('#668096')); canvas.setFont('Helvetica',7); canvas.drawString(31*mm,h-14.1*mm,'Quality Engineering')
 canvas.setStrokeColor(colors.HexColor('#d4e5f1')); canvas.line(18*mm,h-18*mm,w-18*mm,h-18*mm)
 canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#7890a3')); canvas.drawRightString(w-18*mm,9*mm,f'QA Lab Brasil  |  {doc.page}')
 canvas.restoreState()

def build_pdf(path,title,subtitle,sections):
 os.makedirs(os.path.dirname(path),exist_ok=True)
 story=[Spacer(1,5*mm),Paragraph(esc(title),styles['Title']),Spacer(1,3),Paragraph(esc(subtitle or ''),styles['QABody']),Spacer(1,7)]
 for h,b in sections:
  story += [Paragraph(esc(h),styles['QAHeading2'])]
  if isinstance(b,list):
   story.append(ListFlowable([ListItem(Paragraph(esc(x),styles['QABody'])) for x in b],bulletType='bullet',leftIndent=16))
  else:
   for line in str(b).split('\n'):
    line=line.strip()
    if not line: continue
    if line.startswith('```') or line.endswith('```'): continue
    if re.match(r'^(python|py|pip|npm|npx|node|java|javac|robot|appium|adb|git|mvn|gradle|docker|kubectl|terraform|k6|jmeter|locust|code|echo|set |export |\.venv|mkdir|cd )',line,re.I):
     story.append(Paragraph(esc(line),styles['QACode']))
    elif re.match(r'^\d+[\.)]\s',line): story.append(Paragraph('<b>'+esc(line)+'</b>',styles['QABody']))
    elif re.match(r'^(CT|TC|CP)\d+',line): story.append(Paragraph('<b>'+esc(line)+'</b>',styles['QABody']))
    elif ':' in line and len(line.split(':',1)[0])<40:
     a,c=line.split(':',1); story.append(Paragraph('<b>'+esc(a)+':</b> '+esc(c),styles['QABody']))
    else: story.append(Paragraph(esc(line),styles['QABody']))
  story.append(Spacer(1,4))
 doc=SimpleDocTemplate(path,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=22*mm,bottomMargin=16*mm,title=title)
 doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)

# Rebuild all educational PDFs with branded header.
for k,v in D.items():
 for lang in ['pt','en','es']:
  if lang not in v: continue
  d=v[lang]; build_pdf(f'{ROOT}/pdf/{lang}/{k}.pdf',d.get('title',k),d.get('subtitle',''),d.get('sections',[]))

# Beginner-first manual content. Prior tool-specific notes are retained but wrapped in a much fuller tutorial.
LABELS={
'pt':{'suffix':'Instalação e Configuração','goal':'Objetivo deste manual','goalb':'Levar uma pessoa sem experiência prévia da máquina ainda não configurada até uma instalação validada e um primeiro uso funcional. Leia as etapas na ordem e só avance quando a validação da etapa atual funcionar.','before':'Antes de começar','terminal':'Onde executar os comandos','terminalb':'No Windows, abra o menu Iniciar e procure PowerShell ou Prompt de Comando. No macOS, abra Terminal. No Linux, abra o aplicativo Terminal da sua distribuição. Quando o manual pedir para fechar e reabrir o terminal, faça isso para que alterações de PATH/variáveis sejam recarregadas.','official':'Fonte oficial e versão','install':'Instalação passo a passo','path':'PATH e variáveis de ambiente','validate':'Como validar a instalação','first':'Primeiro uso funcional','trouble':'Problemas comuns e como resolver','done':'Critério de conclusão','doneb':'Considere a instalação concluída somente quando o comando de validação funcionar e o primeiro exemplo deste manual executar sem erro. Depois disso, avance para o guia educacional da ferramenta no QA Lab Brasil.'},
'en':{'suffix':'Installation & Setup','goal':'Goal of this manual','goalb':'Take a complete beginner from an unconfigured machine to a validated installation and a working first use. Follow the steps in order and do not continue until the current validation works.','before':'Before you start','terminal':'Where to run commands','terminalb':'On Windows, open Start and search for PowerShell or Command Prompt. On macOS, open Terminal. On Linux, open your distribution Terminal. When asked to close and reopen the terminal, do it so PATH/environment changes are reloaded.','official':'Official source and version','install':'Step-by-step installation','path':'PATH and environment variables','validate':'Validate the installation','first':'First working use','trouble':'Common problems and fixes','done':'Completion criteria','doneb':'Treat setup as complete only when the validation command works and the first example runs without errors. Then continue with the tool learning guide in QA Lab Brasil.'},
'es':{'suffix':'Instalación y Configuración','goal':'Objetivo de este manual','goalb':'Llevar a una persona sin experiencia desde una máquina sin configurar hasta una instalación validada y un primer uso funcional. Siga los pasos en orden y no avance hasta que la validación actual funcione.','before':'Antes de comenzar','terminal':'Dónde ejecutar los comandos','terminalb':'En Windows, abra Inicio y busque PowerShell o Símbolo del sistema. En macOS, abra Terminal. En Linux, abra la Terminal de su distribución. Cuando se indique cerrar y abrir la terminal, hágalo para recargar PATH/variables.','official':'Fuente oficial y versión','install':'Instalación paso a paso','path':'PATH y variables de entorno','validate':'Cómo validar la instalación','first':'Primer uso funcional','trouble':'Problemas comunes y soluciones','done':'Criterio de finalización','doneb':'Considere la instalación terminada solo cuando el comando de validación funcione y el primer ejemplo se ejecute sin errores. Después continúe con la guía educativa de la herramienta en QA Lab Brasil.'}}

SPECIAL={
'robot-framework':{
'pt':('Python 3.8 ou superior é requisito do Robot Framework atual. O próprio guia oficial recomenda Python e pip e explica PATH e ambientes virtuais.',
'''1. Instale Python primeiro usando a fonte oficial. No Windows, durante a instalação/gerenciador, permita que Python fique disponível no PATH quando essa opção for apresentada.\n2. Abra um NOVO PowerShell e execute: python --version\n3. Se python não funcionar, tente: py --version\n4. Verifique o pip: python -m pip --version\n5. Crie uma pasta de projeto: mkdir robot-lab\ncd robot-lab\n6. Crie um ambiente isolado: python -m venv .venv\n7. Windows PowerShell: .venv\\Scripts\\Activate.ps1\nWindows CMD: .venv\\Scripts\\activate.bat\nmacOS/Linux: source .venv/bin/activate\n8. Instale: python -m pip install robotframework\n9. Valide: robot --version''',
'''No Windows, se Python foi instalado mas python/robot não é reconhecido, primeiro feche e abra o terminal. Se continuar, procure “Editar as variáveis de ambiente para sua conta”, edite Path e inclua a pasta do Python e sua pasta Scripts. Em ambiente virtual, prefira ativar .venv em vez de alterar PATH global. Se o PowerShell bloquear Activate.ps1, use CMD com activate.bat ou siga a política de execução aprovada pela sua organização.''',
'''Crie primeiro_teste.robot com:\n*** Test Cases ***\nMeu primeiro teste\n    Log    QA Lab Brasil - Robot Framework funcionando\n\nExecute: robot primeiro_teste.robot\nO terminal deve mostrar PASS. Abra report.html e log.html gerados na mesma pasta; output.xml contém o resultado estruturado.'''),
'en':('Current Robot Framework requires Python 3.8 or newer. The official guide recommends Python/pip and documents PATH and virtual environments.','1. Install Python from the official source and make it available on PATH when offered.\n2. New terminal: python --version (or py --version on Windows).\n3. python -m pip --version\n4. mkdir robot-lab; cd robot-lab\n5. python -m venv .venv\n6. Activate .venv for your OS.\n7. python -m pip install robotframework\n8. robot --version','If python/robot is not found, reopen the terminal. On Windows add the Python install and Scripts directories to user Path if needed. Prefer an activated venv over global PATH changes.','Create first_test.robot with a minimal Test Cases/Log example, run robot first_test.robot, confirm PASS and inspect report.html/log.html.'),
'es':('Robot Framework actual requiere Python 3.8 o superior. La guía oficial recomienda Python/pip y documenta PATH y ambientes virtuales.','1. Instale Python desde la fuente oficial y agréguelo al PATH cuando se ofrezca.\n2. Nueva terminal: python --version (o py --version en Windows).\n3. python -m pip --version\n4. mkdir robot-lab; cd robot-lab\n5. python -m venv .venv\n6. Active .venv según su SO.\n7. python -m pip install robotframework\n8. robot --version','Si python/robot no se reconoce, reabra la terminal. En Windows agregue las carpetas de Python y Scripts al Path del usuario si es necesario. Prefiera un venv activo a cambios globales.','Cree primer_test.robot con un caso mínimo y Log, ejecute robot primer_test.robot, confirme PASS y abra report.html/log.html.')},
'playwright':{
'pt':('Node.js e npm instalados. Prefira uma versão LTS compatível com a versão atual do Playwright. Cada versão do Playwright requer binários específicos dos navegadores.',
'''1. Valide Node/npm: node -v e npm -v.\n2. Crie uma pasta: mkdir playwright-lab\ncd playwright-lab\n3. Inicialize um projeto Playwright conforme a documentação oficial (npm init playwright@latest) e responda às perguntas do assistente.\n4. Se necessário, instale os browsers: npx playwright install\n5. Valide: npx playwright --version\n6. Execute os testes de exemplo: npx playwright test\n7. Abra o relatório: npx playwright show-report''',
'''Normalmente não é necessário configurar PATH específico do Playwright; npx usa o pacote do projeto. Se node/npm não forem reconhecidos, corrija a instalação/PATH do Node.js. Em rede corporativa, downloads dos browsers podem exigir proxy/certificados; siga a documentação oficial de browsers do Playwright.''',
'''Abra tests/example.spec.* criado pelo instalador, execute npx playwright test e confirme testes aprovados. Depois execute npx playwright test --ui para explorar a interface de execução.'''),
'en':('Node.js and npm installed. Prefer a supported LTS release. Each Playwright version requires matching browser binaries.','1. node -v and npm -v.\n2. mkdir playwright-lab; cd playwright-lab\n3. npm init playwright@latest and answer the setup prompts.\n4. npx playwright install if browsers were not installed.\n5. npx playwright --version\n6. npx playwright test\n7. npx playwright show-report','Playwright normally needs no global PATH entry; npx uses the project package. Fix Node.js PATH if node/npm are missing. Corporate proxies may require the official proxy/certificate setup.','Run the generated example test, confirm it passes, then try npx playwright test --ui.'),
'es':('Node.js y npm instalados. Prefiera una versión LTS compatible. Cada versión de Playwright requiere binarios específicos de navegadores.','1. node -v y npm -v.\n2. mkdir playwright-lab; cd playwright-lab\n3. npm init playwright@latest y responda el asistente.\n4. npx playwright install si faltan navegadores.\n5. npx playwright --version\n6. npx playwright test\n7. npx playwright show-report','Playwright normalmente no requiere PATH global; npx usa el paquete del proyecto. Corrija PATH de Node.js si node/npm faltan.','Ejecute el test de ejemplo generado, confirme que pasa y pruebe npx playwright test --ui.')},
'python':{
'pt':('No Windows atual, a documentação oficial recomenda o Python Install Manager. Após a instalação, python, py e pymanager devem ficar disponíveis; o gerenciador pode solicitar inclusão de diretório no PATH.',
'''1. Acesse python.org/downloads e instale o Python Install Manager.\n2. Abra um novo PowerShell.\n3. Execute: python --version\n4. Execute: py --version\n5. Verifique pip: python -m pip --version\n6. Crie pasta: mkdir python-lab\ncd python-lab\n7. Crie ambiente virtual: python -m venv .venv\n8. Ative o ambiente conforme seu terminal.\n9. Crie hello.py com print("QA Lab Brasil - Python funcionando")\n10. Execute: python hello.py''',
'''Se python não for reconhecido mas py funcionar, o runtime existe. No Windows atual, procure “Editar as variáveis de ambiente para sua conta” e, quando necessário, adicione %LocalAppData%\\Python\\bin e o diretório Scripts do runtime conforme a documentação oficial. Feche e reabra o terminal. Evite misturar várias instalações antigas no PATH.''',
'''python hello.py deve imprimir a mensagem sem erro. Em seguida execute python -m pip --version dentro do .venv e confirme que o caminho mostrado pertence ao ambiente do projeto.'''),
'en':('Current Windows documentation recommends Python Install Manager. After setup, python, py and pymanager should be available; runtime setup may offer to add a directory to PATH.','1. Install Python Install Manager from python.org/downloads.\n2. New PowerShell.\n3. python --version\n4. py --version\n5. python -m pip --version\n6. mkdir python-lab; cd python-lab\n7. python -m venv .venv\n8. Activate it.\n9. Create hello.py and run python hello.py.','If py works but python does not, the runtime exists. Add the documented Python bin/Scripts locations to user PATH when required, then reopen the terminal. Avoid stale duplicate Python paths.','Run hello.py and verify pip inside the activated venv points to the project environment.'),
'es':('La documentación actual de Windows recomienda Python Install Manager. Después de instalar, python, py y pymanager deberían estar disponibles.','1. Instale Python Install Manager desde python.org/downloads.\n2. Abra PowerShell nuevo.\n3. python --version\n4. py --version\n5. python -m pip --version\n6. mkdir python-lab; cd python-lab\n7. python -m venv .venv\n8. Active el ambiente.\n9. Cree hello.py y ejecute python hello.py.','Si py funciona pero python no, agregue las rutas bin/Scripts documentadas al Path del usuario cuando sea necesario y reabra la terminal.','Ejecute hello.py y confirme que pip dentro del venv apunta al ambiente del proyecto.')},
'java':{
'pt':('Instale um JDK, não apenas uma JRE. A documentação Oracle atual instala o JDK em C:\\Program Files\\Java\\jdk-<versão> por padrão no Windows.',
'''1. Baixe o JDK para seu sistema no site oficial. Para projetos corporativos, confirme a versão exigida antes de escolher apenas “a mais nova”.\n2. Windows: execute o instalador oficial e conclua o assistente.\n3. Abra novo PowerShell: java -version\n4. Valide o compilador: javac -version\n5. Localize a pasta do JDK.\n6. Quando sua ferramenta exigir JAVA_HOME, crie JAVA_HOME apontando para a raiz do JDK, sem \\bin.\n7. Adicione %JAVA_HOME%\\bin ao Path quando necessário.\n8. Feche/reabra o terminal e repita java -version e javac -version.''',
'''Se java não for reconhecido, revise Path. Se java funciona mas mostra versão errada, procure entradas antigas do Java no Path e confirme JAVA_HOME. JAVA_HOME deve apontar para a pasta do JDK; Path aponta para o bin. Não configure várias entradas conflitantes.''',
'''Crie HelloWorld.java com uma classe HelloWorld e System.out.println. Execute javac HelloWorld.java e depois java HelloWorld. A mensagem deve aparecer no terminal.'''),
'en':('Install a JDK, not only a JRE. Current Oracle docs use C:\\Program Files\\Java\\jdk-<version> as the default Windows JDK location.','1. Download the required JDK from the official source.\n2. Run the Windows installer.\n3. New terminal: java -version\n4. javac -version\n5. Set JAVA_HOME to the JDK root when required.\n6. Add %JAVA_HOME%\\bin to Path when needed.\n7. Reopen terminal and validate again.','If Java is missing or the wrong version is shown, inspect old Path entries and JAVA_HOME. JAVA_HOME points to the JDK root, not bin.','Compile and run a minimal HelloWorld.java with javac and java.'),
'es':('Instale un JDK, no solo JRE. Oracle usa C:\\Program Files\\Java\\jdk-<versión> como ubicación predeterminada en Windows.','1. Descargue el JDK requerido desde la fuente oficial.\n2. Ejecute el instalador.\n3. Nueva terminal: java -version\n4. javac -version\n5. Configure JAVA_HOME a la raíz del JDK cuando se requiera.\n6. Agregue %JAVA_HOME%\\bin al Path cuando corresponda.\n7. Reabra terminal y valide.','Si aparece una versión incorrecta, revise entradas antiguas de Path y JAVA_HOME. JAVA_HOME apunta a la raíz, no a bin.','Compile y ejecute HelloWorld.java con javac y java.')}
}

# Existing installation set; cloud-only services are intentionally absent.
install_keys=sorted({os.path.basename(x).replace('-installation.pdf','') for x in __import__('glob').glob(ROOT+'/pdf/pt/*-installation.pdf')})
for k in install_keys:
 if k not in D: continue
 for lang in ['pt','en','es']:
  if lang not in D[k]: continue
  L=LABELS[lang]; d=D[k][lang]; meta=D[k].get('_meta',{}); url=meta.get('official') or meta.get('docs') or meta.get('download') or ''
  old=TOOL.get(k,('','','',''))
  pre,inst,val,pathnote=(list(old)+['','','',''])[:4]
  if k in SPECIAL:
   pre,inst,pathnote,first=SPECIAL[k][lang]
  else:
   first={'pt':'Faça o primeiro uso mínimo descrito no guia educacional da ferramenta. O objetivo é comprovar que a instalação abre/executa e consegue realizar uma operação simples em ambiente de teste.','en':'Perform the smallest working use described in the learning guide. Confirm the tool opens/runs and completes one simple operation in a test environment.','es':'Realice el primer uso mínimo descrito en la guía educativa. Confirme que la herramienta abre/ejecuta y completa una operación simple en un ambiente de prueba.'}[lang]
  # Add explicit beginner framing and realistic troubleshooting around the prior tool-specific content.
  trouble=pathnote or {'pt':'Se o comando não for reconhecido, feche e reabra o terminal e confirme a instalação. Só altere PATH quando a documentação oficial da ferramenta realmente exigir. Diferencie erro de instalação, permissão, rede, credenciais e configuração do projeto.','en':'If the command is not recognized, reopen the terminal and confirm installation. Change PATH only when the official tool docs require it. Distinguish installation, permissions, network, credentials and project configuration errors.','es':'Si el comando no se reconoce, reabra la terminal y confirme la instalación. Cambie PATH solo cuando la documentación oficial lo requiera. Distinga errores de instalación, permisos, red, credenciales y configuración.'}[lang]
  sections=[(L['goal'],L['goalb']),(L['before'],pre),(L['terminal'],L['terminalb']),(L['official'],(url+'\n'+({'pt':'Use sempre a documentação oficial para confirmar versões suportadas. Evite tutoriais antigos quando o instalador ou os pré-requisitos tiverem mudado.','en':'Always use official documentation to confirm supported versions. Avoid old tutorials when installers or prerequisites have changed.','es':'Use siempre la documentación oficial para confirmar versiones soportadas. Evite tutoriales antiguos cuando instaladores o requisitos hayan cambiado.'}[lang]))),(L['install'],inst),(L['path'],trouble),(L['validate'],val),(L['first'],first),(L['trouble'],trouble),(L['done'],L['doneb'])]
  build_pdf(f'{ROOT}/pdf/{lang}/{k}-installation.pdf',d['title']+' - '+L['suffix'],d.get('subtitle',''),sections)
print('educational',sum(1 for _ in __import__('glob').glob(ROOT+'/pdf/*/*.pdf')),'install keys',len(install_keys))
