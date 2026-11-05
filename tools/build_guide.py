"""Rebuild illustrated mechanical figures and the Spanish PDF assembly guide.
python -m pip install -r requirements-docs.txt
python tools/build_guide.py
"""
from pathlib import Path
import sys,math,json
ROOT=Path(__file__).resolve().parents[1]
DEV=ROOT.parents[1]/'work/cad_deps'
if DEV.exists():sys.path.insert(0,str(DEV))
sys.path.insert(0,str(ROOT/'cad'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from matplotlib.font_manager import findfont,FontProperties
from PIL import Image
from build import finished,signature_section
from model import *
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

IMG=ROOT/'docs/images';IMG.mkdir(exist_ok=True)
BG='#eef1f5';INK='#203247';ORANGE='#de682f';GRAY='#526373'
F,R,_=finished()
def patch(ax,cs,color,alpha=1):
    verts=[];codes=[]
    for poly in cs.to_polygons():
        verts.extend(poly.tolist()+[poly[0].tolist()])
        codes.extend([MPath.MOVETO]+[MPath.LINETO]*(len(poly)-1)+[MPath.CLOSEPOLY])
    ax.add_patch(PathPatch(MPath(verts,codes),facecolor=color,edgecolor=color,lw=.5,alpha=alpha))
def screenshot(name):return Image.open(IMG/name)

# Cover panel composed only of screenshots of the actual printable CAD.
fig=plt.figure(figsize=(13,8.1),facecolor=BG)
fig.text(.055,.934,'DOGGIE / HOUSE',fontsize=27,weight='bold',color=INK)
fig.text(.055,.886,'De la EKO a Guate. Una casita para cuidar al Doggie.',fontsize=13,color=GRAY)
for x,name in [(.04,'front.png'),(.52,'rear.png')]:
    ax=fig.add_axes([x,.14,.44,.70]);ax.imshow(screenshot(name));ax.axis('off')
fig.text(.07,.10,'EL PERRO A LA VISTA',fontsize=12,weight='bold',color=INK)
fig.text(.55,.10,'SIN TORNILLOS. MÁS VENTILACIÓN.',fontsize=12,weight='bold',color=INK)
fig.text(.07,.051,'RogerF5 · v2.0.0-rc1 · CAD revisado tras el prototipo; nueva impresión pendiente.',fontsize=10,color=GRAY)
fig.savefig(IMG/'cover.png',dpi=160);plt.close(fig)

# Exact cross-sections, not a redrawn approximate latch.
fig,axs=plt.subplots(1,2,figsize=(11,5.3),facecolor='white')
for ax in axs:
    patch(ax,R.rotate((-90,0,0)).slice(-P['latch_y'][0]),'#3a4856')
    patch(ax,F.rotate((-90,0,0)).slice(-P['latch_y'][0]),ORANGE)
    ax.set_xlim(-5.8,-.6);ax.set_ylim(11.8,18.2);ax.set_aspect('equal')
    ax.set_xlabel('X de la placa (mm)',fontsize=9,color=GRAY)
    ax.tick_params(labelsize=8);ax.spines[['top','right']].set_visible(False)
axs[0].set_title('1 / Cerrado',loc='left',fontsize=14,color=INK,pad=14)
axs[0].set_ylabel('Z desde el frente (mm)',fontsize=9,color=GRAY)
axs[0].annotate('Hombro del gancho',xy=(-4.65,15.03),xytext=(-3.4,13.0),
    fontsize=10,arrowprops=dict(arrowstyle='->',color=ORANGE),color=INK)
axs[1].set_title('2 / Presionar hacia dentro',loc='left',fontsize=14,color=INK,pad=14)
tip=latch(-1,P['latch_y'][0])^box(8,12,7,-6,P['latch_y'][0]-6,10)
cs=tip.translate((.95,0,0)).rotate((-90,0,0)).slice(-P['latch_y'][0])
for poly in cs.to_polygons():
    pts=np.vstack([poly,poly[0]])
    axs[1].plot(pts[:,0],pts[:,1],ls='--',color='#e8a970',lw=1.6)
axs[1].annotate('',xy=(-3.6,15.5),xytext=(-5.5,15.5),arrowprops=dict(arrowstyle='->',lw=2.2,color='#08a5ae'))
fig.text(.065,.02,'Naranja: marco y pestaña. Gris: tapa. Trazo discontinuo: desplazamiento del extremo, no simulación de esfuerzos.',fontsize=9,color=GRAY)
fig.tight_layout(rect=[0,.065,1,1]);fig.savefig(IMG/'snap-section.png',dpi=180);plt.close(fig)

# Side-wall YZ section exposes the measured 2 mm extension at the lower edge.
mat=np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0]],float)
fig,ax=plt.subplots(figsize=(9,4.8),facecolor='white')
patch(ax,F.transform(mat).slice(-3),ORANGE);patch(ax,R.transform(mat).slice(-3),'#3a4856')
ax.set_xlim(23,47);ax.set_ylim(0,20);ax.set_aspect('equal')
ax.hlines([7.4,5.4],28.7,41.3,colors=['#aa7080','#079ca5'],linestyles=['--','-'],linewidths=[1,1.6])
ax.annotate('2 mm',xy=(35,5.4),xytext=(35,7.4),ha='center',fontsize=11,
    arrowprops=dict(arrowstyle='<->',color='#079ca5'),color='#087d86')
ax.text(35,12,'Recorte USB-C',ha='center',fontsize=13,color=INK)
ax.set_xlabel('Y de la placa (mm)',fontsize=10);ax.set_ylabel('Z desde el frente (mm)',fontsize=10)
ax.spines[['top','right']].set_visible(False)
fig.text(.07,.965,'Borde inferior ampliado; borde superior conservado',fontsize=14,weight='bold',color=INK)
fig.text(.07,.025,'Punteado: límite de v1. Turquesa: nuevo límite de v2. La posición Y = 35 mm no cambia.',fontsize=10,color=GRAY)
fig.tight_layout(rect=[0,.07,1,.94]);fig.savefig(IMG/'usb-correction.png',dpi=175);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,2.25),facecolor='white')
sig=signature_section().mirror((1,0))
patch(ax,sig,INK)
bb=sig.bounds();ax.set_xlim(bb[0]-2,bb[2]+2);ax.set_ylim(bb[1]-1,bb[3]+1);ax.set_aspect('equal');ax.axis('off')
fig.savefig(IMG/'signature.png',dpi=180,bbox_inches='tight');plt.close(fig)

fonts=[('DV',FontProperties(family='DejaVu Sans')),('DVB',FontProperties(family='DejaVu Sans',weight='bold'))]
for name,prop in fonts:pdfmetrics.registerFont(TTFont(name,findfont(prop)))
WPDF,HPDF=A4
c=canvas.Canvas(str(ROOT/'docs/GUIA_MONTAJE_ES.pdf'),pagesize=A4)
c.setTitle('Doggie House - Guía de montaje v2');c.setAuthor('RogerF5 / Doggie House')
c.setSubject('Montaje y apertura de la carcasa comunitaria, cierre sin tornillos')

def text(x,y,s,size=10,bold=False,color=INK):
    c.setFillColor(colors.HexColor(color));c.setFont('DVB' if bold else 'DV',size);c.drawString(x,y,s)
def para(s,x,y,w,size=10,color=INK,leading=None):
    style=ParagraphStyle('p',fontName='DV',fontSize=size,leading=leading or size*1.5,textColor=colors.HexColor(color),spaceAfter=0)
    p=Paragraph(s,style);pw,ph=p.wrap(w,HPDF)
    assert y-ph>48,(s[:40],y,ph)
    p.drawOn(c,x,y-ph);return y-ph
def image(name,x,y,w,h):
    im=Image.open(IMG/name);iw,ih=im.size;scale=min(w/iw,h/ih)
    rw,rh=iw*scale,ih*scale;c.drawImage(ImageReader(im),x+(w-rw)/2,y+(h-rh)/2,rw,rh,mask='auto')
def page(n,tag,title,subtitle=''):
    c.setFillColor(colors.white);c.rect(0,0,WPDF,HPDF,fill=1,stroke=0)
    text(42,HPDF-42,'DOGGIE / HOUSE',10,True)
    text(WPDF-167,HPDF-42,tag.upper(),8,True,ORANGE)
    c.setStrokeColor(colors.HexColor('#dce2e8'));c.line(42,HPDF-58,WPDF-42,HPDF-58)
    text(42,HPDF-100,title,25,True)
    if subtitle:para(subtitle,42,HPDF-117,WPDF-84,9.3,GRAY)
    c.line(42,44,WPDF-42,44);text(42,28,'RogerF5 · v2.0.0-rc1 · 04.11.2026',8,color=GRAY)
    text(WPDF-89,28,f'{n} / 5',8,color=GRAY)
def step(n,title,s,x,y,w):
    text(x,y,str(n).zfill(2),11,True,ORANGE)
    text(x+27,y,title,11,True)
    return para(s,x+27,y-12,w-27,9.2)-19

page(1,'EKO → Guate','Una casita para el Doggie.','Carcasa comunitaria para EvilDoggie de Faraday / Kalpa. Sin tornillos y con el perro a la vista.')
image('cover.png',30,330,WPDF-60,360)
y=para('Durante un viaje a la EKO, el equipo de Faraday nos regaló un EvilDoggie. De regreso a Guate, le hicimos su casita para cuidarlo como se debe. Después de imprimir el primer prototipo, corregimos lo que se veía y lo que se sentía al montarlo.',42,310,WPDF-84,11)
y=para('<b>Esta revisión:</b> USB con más holgura, cuatro pestañas liberables, superficies sin letras exteriores, más ventilación y RogerF5 grabado por dentro.',42,y-18,WPDF-84,10.2)
para('El CAD pasa sus comprobaciones digitales. El cierre PETG, la corrección USB propuesta de 2 mm y el grabado necesitan comprobarse en una nueva impresión. Las fotos de v1 documentan el prototipo anterior.',42,y-20,WPDF-84,9,GRAY)
c.showPage()

page(2,'Preparar','Elegir piezas e imprimir.','Un conjunto estándar lleva marco, tapa y dos pulsadores. No lleva herrajes metálicos.')
rows=[['Cantidad','Pieza','Archivo / material'],['1','Marco con pestañas','01_front_frame.stl'],['1','Tapa de componentes','02_rear_cover.stl'],['2','Pulsadores cautivos','03_two_captive_buttons.stl'],['Opcional','Ventana transparente','PET / PC de 1 mm'],['Alternativa','Acceso directo a botones','01 + 04, sin pulsadores']]
t=Table(rows,colWidths=[62,176,273],rowHeights=[27]*6)
t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'DV'),('FONTNAME',(0,0),(-1,0),'DVB'),('FONTSIZE',(0,0),(-1,-1),8.5),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#233448')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f4f7'),colors.white]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),9)]));t.wrapOn(c,511,162);t.drawOn(c,42,HPDF-335)
y=para('<b>PETG sin fibras.</b> Boquilla 0,4 mm, capa 0,20 mm, 4 paredes y 20 % de relleno como punto de partida. Usar el perfil del filamento. No se entrega G-code ni un perfil ya ensayado de v2.',42,HPDF-361,511,10)
y=para('Marco y tapa: cara exterior sobre la cama. Las pestañas quedan de pie; el interior de la tapa queda hacia arriba. Pulsadores: de pie sobre su punta de 4 mm, con brim. Revisar los puentes y no dejar soportes en los canales.',42,y-16,511,9.8)
y=para('<b>Primero las muestras:</b> 08 + 09 para cerrar y abrir; 10 + 11 para presentar el recorte USB; 12 para leer la firma. Las muestras usan la misma geometría de la carcasa. El cupón USB prueba la abertura local, no registra toda la posición sobre la PCB.',42,y-18,511,9.8)
image('signature.png',70,103,455,82)
text(126,88,'Grabado interior: unos 5,4 mm de alto · 0,5 mm de profundidad',8.3,color=GRAY)
c.showPage()

page(3,'Montar','Del marco a la tapa.','Desconectar cables antes de presentar la placa o los pulsadores.')
image('exploded.png',100,405,395,275)
y1=360;y2=360
y1=step(1,'Ventana opcional','Cortar la lámina de 1 mm con la plantilla 1:1. Verificar la regla de 50 mm y fijarla al reborde con cinta fina.',42,y1,245)
y1=step(2,'Orientar el Doggie','Perro hacia la ventana; DB9 al extremo superior. Bajar la placa sobre los cuatro pines. No perforar ni presionar componentes.',42,y1,245)
y1=step(3,'Comprobar apoyos','Las cuatro esquinas deben descansar en sus bases. Mantener pines, canales y LED libres de cinta o rebabas.',42,y1,245)
y2=step(4,'Pulsadores','Para tapa 02, introducir las varillas desde dentro, punta estrecha hacia fuera. Comprobar que se deslizan. BOOT arriba; RESET abajo.',309,y2,245)
y2=step(5,'Alinear la junta','Presentar la tapa paralela, con USB, DB9 y borneras centrados. Alinear la lengua perimetral y los cuatro canales.',309,y2,245)
y2=step(6,'Encajar los ganchos','Presionar gradualmente en los bordes hasta que los cuatro ganchos entren en sus ventanas. No golpear ni presionar el centro.',309,y2,245)
c.showPage()

page(4,'Abrir y ajustar','Presionar. Liberar. Mantener.','Cuatro enganches accesibles. No usar los conectores como palanca.')
image('snap-section.png',30,386,WPDF-60,310)
y=para('<b>Para abrir:</b> desconectar cables. Presionar hacia dentro los dos ganchos de un lado, con la uña o una punta plástica. Separar apenas ese borde; liberar después los del otro lado y levantar la tapa recta. Practicar primero con 08 + 09.',42,370,511,10.3)
y=para('<b>Si el cierre está duro:</b> revisar rebabas, orientación y muestra de PETG. No forzar, pegar ni calentar las pestañas. La comprobación digital del recorrido no mide su fuerza ni su resistencia a ciclos.',42,y-15,511,9.8)
image('usb-correction.png',60,72,475,205)
c.showPage()

page(5,'Comprobar y compartir','Listo para la siguiente prueba.','Registrar el resultado real antes de marcar la revisión como físicamente validada.')
image('inside.png',50,405,230,275)
y=650
for title,s in [('Cierre','Cuatro ganchos asentados; la junta retiene y se abre sin grietas.'),('Conectores','USB a fondo sin mover la placa. DB9 y borneras accesibles.'),('Controles','GOOD / EVIL llega a ambos topes. BOOT y RESET regresan libres.'),('Interior','Sin placa doblada, LED tocados ni letras ilegibles. Ranuras despejadas.')]:
    text(306,y,title,11,True);y=para(s,306,y-12,247,9.7)-22
y=para('<b>Validación física pendiente:</b> anotar revisión de PCB, PETG, perfil, cable USB, ajuste de los 2 mm y ciclos de cierre probados en docs/RELEASE_CHECKLIST.md. No mezclar mitades v1 y v2.',42,365,511,10.2)
y=para('<b>Para compartir:</b> el paquete incluye STL, dos disposiciones 3MF, fuente paramétrica, visor offline, fotos de v1, guía ES/EN e informe geométrico. El README cuenta cómo nació la casita entre la EKO y Guate.',42,y-19,511,10)
y=para('Diseño de carcasa: RogerF5 y colaboradores. Hardware e ilustración originales: Faraday / Kalpa. Gracias al equipo de Faraday por el regalo y por querer compartir esta casita con la comunidad.',42,y-19,511,10)
para('Referencias: github.com/infobyte/doggie · especificaciones A1: store.bblcdn.com/8137fad1525a4454ac8a28502edbc919.pdf<br/>Las figuras muestran CAD de v2, no una impresión de v2. Sin ensayo térmico ni de fatiga.',42,y-20,511,8.2,GRAY)
c.showPage();c.save()
print('Guide:',ROOT/'docs/GUIA_MONTAJE_ES.pdf')
