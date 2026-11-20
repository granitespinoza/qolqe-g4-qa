from pathlib import Path
from html.parser import HTMLParser
import html,re,json
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table,TableStyle,KeepInFrame,Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Rect,String
from reportlab.graphics import renderPDF
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
class E:
 def __init__(self,tag,attrs=()):self.tag=tag;self.attrs=dict(attrs);self.children=[]
 def text(self):return ''.join(c if isinstance(c,str)else c.text()for c in self.children)
 def find(self,tag):return[c for c in self.children if isinstance(c,E)and c.tag==tag]
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.root=E('root');self.stack=[self.root];self.slides=[]
 def handle_starttag(self,tag,attrs):
  e=E(tag,attrs);self.stack[-1].children.append(e)
  if tag=='section'and dict(attrs).get('class')=='slide':self.slides.append(e)
  if tag not in ['meta','link','br','img','input','hr']:self.stack.append(e)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):self.stack[-1].children.append(data)
p=Parser();p.feed((R/'apidoc/final/index.html').read_text(encoding='utf8'));assert len(p.slides)==18
for family,file in [('Body','segoeui.ttf'),('BodyBold','segoeuib.ttf'),('Mono','consola.ttf')]:pdfmetrics.registerFont(TTFont(family,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold')
styles={k:ParagraphStyle(k,fontName=font,fontSize=size,leading=leading,textColor=colors.HexColor('#19332b'),spaceAfter=after)for k,font,size,leading,after in [('body','Body',12,17,10),('title','BodyBold',25,30,18),('small','Body',10,14,7),('code','Mono',10,14,8)]}
def para(t,kind='body'):return Paragraph(html.escape(t).replace('\n','<br/>'),styles[kind])
def rows(e):
 result=[]
 for c in e.children:
  if isinstance(c,E):
   if c.tag=='tr':result.append(c)
   else:result+=rows(c)
 return result
def flows(e):
 if e.tag=='h1':return[para(e.text(),'title')]
 if e.tag=='p':return[para(e.text())]
 if e.tag=='pre':return[para(e.text(),'code')]
 if e.tag=='button':return[]
 if e.tag=='a':
  uri=e.attrs.get('href','')
  if uri.startswith('../../results/'):uri='https://github.com/granitespinoza/qolqe-g4-qa/actions/workflows/pruebas.yml'
  elif uri.startswith('../../'):uri='https://github.com/granitespinoza/qolqe-g4-qa/blob/main/'+uri[6:]
  return[Paragraph('<link href="'+html.escape(uri,quote=True)+'" color="#136b5b">'+html.escape(e.text())+'</link>',styles['small'])]
 if e.tag=='table':
  rr=rows(e);data=[[para(c.text(),'small')for c in row.children if isinstance(c,E)and c.tag in ('th','td')]for row in rr];n=max(map(len,data));t=Table(data,colWidths=[880/n]*n,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eee0ac')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8f2')]),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#cbd5c9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return[t,Spacer(1,12)]
 if e.tag=='svg':
  d=Drawing(880,293);d.scale(880/900,293/300)
  for c in e.children:
   if not isinstance(c,E):continue
   a=c.attrs
   if c.tag=='rect':d.add(Rect(float(a['x']),300-float(a['y'])-float(a['height']),float(a['width']),float(a['height']),fillColor=colors.HexColor(a['fill']),strokeColor=None))
   if c.tag=='text':d.add(String(float(a['x']),300-float(a['y']),c.text(),fontName='Body',fontSize=14,textAnchor=a.get('text-anchor','start'),fillColor=colors.HexColor('#19332b')))
  return[d]
 if e.attrs.get('class')=='cards':
  cells=[]
  for article in e.find('article'):cells.append([para(x.text())for x in article.children if isinstance(x,E)])
  t=Table([cells],colWidths=[880/len(cells)]*len(cells));t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#edf3e9')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#cbd5c9')),('LEFTPADDING',(0,0),(-1,-1),15),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15)]));return[t,Spacer(1,15)]
 if e.attrs.get('class')=='flow':return[para(' → '.join(x.text()for x in e.find('span')))]
 if e.attrs.get('class')=='eyebrow':return[]
 return[f for c in e.children if isinstance(c,E)for f in flows(c)]
out=R/'presentacion/Entrega_Final_Qolqe.pdf';out.parent.mkdir(exist_ok=True)
c=canvas.Canvas(str(out),pagesize=(960,540));c.setTitle('Qolqe · Entrega final · Franco');c.setAuthor('Franco')
heights=[]
for n,s in enumerate(p.slides,1):
 c.setFillColor(colors.HexColor('#f4f4ee'));c.rect(0,0,960,540,fill=1,stroke=0)
 c.setFillColor(colors.HexColor('#19332b'));c.setFont('BodyBold',10);c.drawString(40,514,'QOLQE · ENTREGA FINAL · FRANCO');c.setFont('Body',9);c.drawRightString(920,22,f'{n} / 18')
 content=flows(s);frame=KeepInFrame(880,454,content,mode='shrink');w,h=frame.wrapOn(c,880,454);frame.drawOn(c,40,490-h);heights.append(round(h,1));c.showPage()
c.save();reader=PdfReader(out);assert len(reader.pages)==18
for page,slide in zip(reader.pages,p.slides):assert slide.find('h1')[0].text()[:20]in(page.extract_text()or''),'Título ausente'
assert 'Granit y Franco'not in '\n'.join(x.extract_text()or''for x in reader.pages)
(R/'presentacion/Entrega_Final_Qolqe.verificacion.json').write_text(json.dumps({'pages':18,'source':'apidoc/final/index.html','author':'Franco','format_points':[960,540],'content_heights':heights},indent=2),encoding='utf8')
print('PDF exportado y verificado: 18 páginas',out)
