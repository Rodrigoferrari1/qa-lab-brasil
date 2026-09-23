import json, os, re, runpy
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
ROOT='/mnt/data/lot7work'
D=json.load(open(ROOT+'/content/topics.json',encoding='utf8'))
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

