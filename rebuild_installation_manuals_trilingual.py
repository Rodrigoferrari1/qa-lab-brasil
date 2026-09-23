import os, json, glob, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

ROOT=os.path.dirname(__file__)
D=json.load(open(ROOT+'/content/topics.json',encoding='utf8'))
langs=('pt','en','es')
install_keys=sorted(os.path.basename(x).replace('-installation.pdf','') for x in glob.glob(ROOT+'/pdf/pt/*-installation.pdf'))

labels={
'pt':{'title':'Instalação e Configuração','intro':'Guia completo para preparar o ambiente, instalar, configurar, validar e realizar o primeiro uso da ferramenta.','goal':'Objetivo deste manual','goaltext':'Este manual foi desenvolvido para orientar você por todo o processo de instalação e configuração da ferramenta, desde a preparação do ambiente até a validação final. Siga as etapas na ordem apresentada e utilize as verificações indicadas ao longo do guia para confirmar que cada configuração foi concluída corretamente.','refs':'Referências oficiais','note':'Observação','noteText':'As versões e requisitos podem evoluir. Antes de instalar em ambiente corporativo, confirme a documentação oficial e as políticas da sua organização.'},
'en':{'title':'Installation & Setup','intro':'A complete guide to prepare the environment, install, configure, validate and perform the first functional use of the tool.','goal':'Manual objective','goaltext':'This manual guides you through the complete installation and setup process, from preparing the environment to final validation. Follow the steps in order and use the checks throughout the guide to confirm that each configuration was completed correctly.','refs':'Official references','note':'Note','noteText':'Versions and requirements may evolve. Before installing in a corporate environment, confirm the current official documentation and your organization policies.'},
'es':{'title':'Instalación y Configuración','intro':'Guía completa para preparar el entorno, instalar, configurar, validar y realizar el primer uso funcional de la herramienta.','goal':'Objetivo del manual','goaltext':'Este manual fue desarrollado para orientarle durante todo el proceso de instalación y configuración de la herramienta, desde la preparación del entorno hasta la validación final. Siga las etapas en el orden presentado y utilice las verificaciones indicadas para confirmar que cada configuración fue concluida correctamente.','refs':'Referencias oficiales','note':'Observación','noteText':'Las versiones y requisitos pueden evolucionar. Antes de instalar en un entorno corporativo, confirme la documentación oficial actual y las políticas de su organización.'}}

# Select the same conceptual section indexes using Portuguese headings, then render corresponding EN/ES sections.
kw=['oficial','pré-requis','prerrequis','instala','configura','primeir','começar','comece','troubleshooting','problemas','path','variá','driver','sdk','valida','primeiros passos','fluxo prático','depend','ambiente','comandos','docker','java_home']
def selected_indices(topic):
    secs=topic['pt']['sections']; out=[]
    for i,s in enumerate(secs):
        h=str(s[0]).lower()
        if any(k in h for k in kw): out.append(i)
    # Always include official documentation if present and enough context.
    if len(out)<6:
        out=list(range(len(secs)))
    return out

styles=getSampleStyleSheet()
body=ParagraphStyle('body',parent=styles['BodyText'],fontName='Helvetica',fontSize=9.4,leading=13,spaceAfter=6)
h1=ParagraphStyle('h1',parent=styles['Heading1'],fontName='Helvetica-Bold',fontSize=17,leading=21,spaceAfter=8,textColor=colors.HexColor('#172554'))
h2=ParagraphStyle('h2',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=12,leading=15,spaceBefore=8,spaceAfter=5,textColor=colors.HexColor('#1e3a8a'))
small=ParagraphStyle('small',parent=body,fontSize=8.5,leading=11,textColor=colors.HexColor('#475569'))
urlstyle=ParagraphStyle('url',parent=body,fontSize=8.2,leading=10,textColor=colors.HexColor('#1d4ed8'))

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def header_footer(canvas,doc):
    canvas.saveState(); w,h=A4
    canvas.setFont('Helvetica-Bold',10); canvas.setFillColor(colors.HexColor('#172554')); canvas.drawString(42,h-30,'QA LAB BRASIL')
    canvas.setFont('Helvetica',7.5); canvas.setFillColor(colors.HexColor('#64748b')); canvas.drawString(42,h-41,'Quality Engineering')
    canvas.setStrokeColor(colors.HexColor('#dbeafe')); canvas.line(42,h-48,w-42,h-48)
    canvas.setFont('Helvetica',7); canvas.drawRightString(w-42,24,f'QA Lab Brasil | {doc.page}')
    canvas.restoreState()

def build(key,lang):
    topic=D[key]; d=topic[lang]; L=labels[lang]; meta=topic.get('_meta',{})
    out=ROOT+f'/pdf/{lang}/{key}-installation.pdf'
    doc=SimpleDocTemplate(out,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=62,bottomMargin=40,title=f"{d['title']} - {L['title']}")
    story=[Paragraph(esc(d['title'])+' - '+esc(L['title']),h1),Paragraph(esc(L['intro']),body),Paragraph(esc(L['goal']),h2),Paragraph(esc(L['goaltext']),body)]
    urls=[]
    for fld in ('official','docs','download'):
        u=meta.get(fld)
        if u and u not in urls: urls.append(u)
    if urls:
        story += [Paragraph(esc(L['refs']),h2)]
        for u in urls: story.append(Paragraph(esc(u),urlstyle))
    idx=selected_indices(topic)
    for i in idx:
        sec=d['sections'][i]
        story.append(Paragraph(esc(sec[0]),h2)); story.append(Paragraph(esc(sec[1]).replace('\n','<br/>'),body))
    doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)

for key in install_keys:
    if key not in D: continue
    for lang in langs: build(key,lang)
print('rebuilt',len(install_keys)*3,'installation PDFs')
