"""Build the community cover and PDF from existing CAD illustrations.
Does not import CAD code or regenerate any STL/3MF files.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage,
    Table, TableStyle, PageBreak, KeepTogether)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
IMAGES=ROOT/'docs/images'
PUB=json.loads((ROOT/'publication.json').read_text(encoding='utf-8'))
INK='#233446'; MUTED='#526273'; ORANGE='#bc481b'; BG='#eef1f5'

def font_file(bold=False):
    candidates=[
        Path('C:/Windows/Fonts')/('arialbd.ttf' if bold else 'arial.ttf'),
        Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'),
    ]
    for p in candidates:
        if p.exists(): return str(p)
    try:
        from matplotlib.font_manager import findfont, FontProperties
        return findfont(FontProperties(family='DejaVu Sans',weight='bold' if bold else 'normal'))
    except ImportError:
        raise RuntimeError('Install DejaVu Sans or provide Arial fonts to build the guide.')

for name,bold in [('DH',False),('DHB',True)]:
    pdfmetrics.registerFont(TTFont(name,font_file(bold)))

# A public-facing cover, composed from the existing CAD renders.
cover=Image.new('RGB',(1600,1000),BG)
draw=ImageDraw.Draw(cover)
draw.text((80,56),'DOGGIE / HOUSE',font=ImageFont.truetype(font_file(True),57),fill=INK)
draw.text((82,140),'Un hardware tan bonito merece estar protegido.',
    font=ImageFont.truetype(font_file(),29),fill=MUTED)
for name,x in [('front.png',55),('rear.png',825)]:
    im=Image.open(IMAGES/name).convert('RGB')
    im=ImageOps.contain(im,(720,610),Image.Resampling.LANCZOS)
    cover.paste(im,(x+(720-im.width)//2,205+(610-im.height)//2))
draw.text((82,866),'KRANKEN TRES D / PARA LA COMUNIDAD',
    font=ImageFont.truetype(font_file(True),23),fill=ORANGE)
draw.text((82,916),'Primera edición 1.0.0 · Ilustraciones CAD · Hardware original: Faraday / Kalpa',
    font=ImageFont.truetype(font_file(),21),fill=MUTED)
cover.save(IMAGES/'cover.png',optimize=True)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='DHBody',fontName='DH',fontSize=10.2,leading=15.5,
    textColor=colors.HexColor(INK),spaceAfter=11))
styles.add(ParagraphStyle(name='DHTitle',fontName='DHB',fontSize=28,leading=32,
    textColor=colors.HexColor(INK),spaceAfter=18))
styles.add(ParagraphStyle(name='DHHeading',fontName='DHB',fontSize=13,leading=17,
    textColor=colors.HexColor(INK),spaceBefore=10,spaceAfter=8))
styles.add(ParagraphStyle(name='DHKicker',fontName='DHB',fontSize=8.8,leading=13,
    textColor=colors.HexColor(ORANGE),spaceAfter=11))
styles.add(ParagraphStyle(name='DHSmall',fontName='DH',fontSize=8.3,leading=12,
    textColor=colors.HexColor(MUTED),spaceAfter=9))

story=[]
def para(s,style='DHBody'):
    story.append(Paragraph(s,styles[style]))
def image(name,w,h):
    im=Image.open(IMAGES/name);iw,ih=im.size
    scale=min(w/iw,h/ih)
    story.append(PDFImage(str(IMAGES/name),width=iw*scale,height=ih*scale))
def step(n,title,s):
    story.append(KeepTogether([
        Paragraph(f'{n:02d} / {title}',styles['DHHeading']),
        Paragraph(s,styles['DHBody'])]))
def page(kicker,title):
    para(kicker.upper(),'DHKicker');para(title,'DHTitle')

page('La historia / edición comunitaria 1.0.0','Una casa para EvilDoggie.')
image('cover.png',510,315)
story.append(Spacer(1,18))
para('En la <b>EKOparty 2026, en Argentina</b>, los amigos de <b>Faraday</b> nos regalaron un EvilDoggie. Al regresar a Guatemala, nos quedó una idea: un hardware tan bonito debía estar protegido.')
para('Lo trabajamos en el taller de <b>Kranken Tres D</b> y modelamos esta carcasa para cuidar la placa sin esconder al perro ni perder acceso a las conexiones. Compartimos los archivos para que cualquiera pueda imprimirla, ensamblarla y aportar mejoras.')
para('Gracias a los amigos de Faraday por el regalo que dio origen al proyecto y a la comunidad por seguir construyendo y compartiendo.')
para('Carcasa de 80 × 110 × 27,8 mm; PCB de referencia de 70 × 100 × 2 mm. Cuatro pestañas liberables, sin tornillos. Ventana transparente de 1 mm opcional.','DHSmall')
story.append(PageBreak())

page('01 / Preparar e imprimir','Elegí las piezas.')
rows=[
 ['Configuración','Piezas para imprimir'],
 ['Pulsadores cautivos','01_front_frame.stl\n02_rear_cover.stl\n03_two_captive_buttons.stl (2 varillas)'],
 ['Acceso directo','01_front_frame.stl\n04_rear_direct_access_optional.stl'],
 ['Muestra de cierre','08_snap_test_front.stl + 09_snap_test_rear.stl'],
 ['Muestra de USB','10_usb_test_front.stl + 11_usb_test_rear.stl'],
]
tab=Table(rows,colWidths=[130,380],hAlign='LEFT')
tab.setStyle(TableStyle([
 ('FONTNAME',(0,0),(-1,-1),'DH'),('FONTNAME',(0,0),(-1,0),'DHB'),
 ('FONTSIZE',(0,0),(-1,-1),9),('LEADING',(0,0),(-1,-1),14),
 ('BACKGROUND',(0,0),(-1,0),colors.HexColor(INK)),
 ('TEXTCOLOR',(0,0),(-1,0),colors.white),
 ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor(BG),colors.white]),
 ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),12),
 ('BOTTOMPADDING',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),10)]))
story.append(tab);story.append(Spacer(1,18))
para('Importar los STL en <b>milímetros a escala 100 %</b>. Los dos 3MF incluyen las piezas orientadas; seleccionar el perfil de la impresora y del filamento en el laminador. Elegir una sola tapa para cada conjunto.')
step(1,'Material y perfil','PETG sin fibras, boquilla 0,4 mm, capa 0,20 mm, 4 paredes y 20 % de relleno como punto de partida. Probar las muestras del cierre con el mismo material de la carcasa.')
step(2,'Orientación','Marco y tapa con su cara exterior sobre la cama e interior hacia arriba. Las pestañas del marco quedan de pie. Pulsadores sobre su extremo de 4 mm, con brim. Revisar puentes y retirar soportes que obstruyan canales o puertos.')
para('Ventana opcional: PET o policarbonato transparente de 1 mm. Usar docs/window-template-1to1.svg, imprimir al 100 % y verificar que la regla mida 50 mm.','DHSmall')
story.append(PageBreak())

page('02 / Ensamblar','Del marco a la tapa.')
image('exploded.png',490,220)
step(1,'Preparar','Desconectar los cables. Apoyar el marco sobre una superficie blanda, con la cara exterior hacia abajo. Retirar rebabas y comprobar que los canales estén libres.')
step(2,'Ventana y placa','Si se usa lámina, fijarla al reborde con cinta fina sin invadir apoyos ni pestañas. Orientar el perro hacia la ventana y DB9 hacia el extremo superior. Bajar la PCB sobre los cuatro pines; las cuatro esquinas deben apoyar sin forzar.')
step(3,'Pulsadores','Con tapa 02, introducir las dos varillas desde dentro, extremo estrecho hacia fuera y pestaña de retención hacia dentro. Comprobar que se deslicen libremente. BOOT arriba y RESET abajo, junto a la palanca. Omitir este paso con tapa 04.')
step(4,'Cerrar','Alinear conectores, junta perimetral y cuatro canales. Presentar la tapa paralela y presionar gradualmente junto a los bordes hasta encajar los cuatro ganchos. Comprobar la junta en todo el contorno; no golpear ni presionar componentes.')
story.append(PageBreak())

page('03 / Abrir y comprobar','Lista para acompañarte.')
image('snap-section.png',490,220)
para('<b>Para abrir:</b> desconectar los cables. Presionar hacia dentro los dos ganchos de un lateral a través de sus ventanas, con la uña o una punta plástica. Separar ligeramente ese borde, liberar el otro lado y levantar la tapa recta. Practicar con las muestras 08 + 09. No hacer palanca con los conectores.')
para('Comprobaciones antes de usarla','DHHeading')
for s in [
 'Los cuatro ganchos retienen la tapa y pueden liberarse sin grietas.',
 'USB-C entra a fondo sin mover la placa; DB9 y borneras son accesibles.',
 'GOOD / EVIL llega a ambos extremos. BOOT y RESET regresan libres.',
 'La PCB no se curva; la ventana no toca LED ni componentes; las ranuras están despejadas.',
]:
    para('• '+s)
para('Estado del diseño','DHHeading')
para('Primera publicación comunitaria 1.0.0. Los STL y 3MF conservan su geometría y su revisión interna de taller 2.0.0-rc1. Las comprobaciones digitales están documentadas; USB, cierre PETG y controles necesitan verificarse en la impresión y placa reales. No hay ensayos de impacto, temperatura o fatiga. Las fotos del prototipo corresponden a una etapa anterior.','DHSmall')
para('Modelado: Kranken Tres D y colaboradores. Hardware y arte originales: Faraday / Kalpa. Carcasa y documentación: MIT. Compartí fotos, material y ajuste en el repositorio.','DHSmall')
para('<link href="https://rogerf5-security.github.io/Case-Evil_Doggie/" color="#bc481b">Visor 3D, descargas y comunidad</link> · <link href="https://github.com/infobyte/doggie" color="#bc481b">Hardware original</link>','DHSmall')

def furniture(c,doc):
    w,h=A4;c.saveState()
    c.setStrokeColor(colors.HexColor('#d9dddf'))
    c.line(42,42,w-42,42);c.setFont('DH',8)
    c.setFillColor(colors.HexColor(MUTED))
    c.drawString(42,27,'DOGGIE HOUSE / Kranken Tres D / Edición comunitaria 1.0.0')
    c.drawRightString(w-42,27,str(doc.page));c.restoreState()

dest=ROOT/'docs/GUIA_MONTAJE_ES.pdf'
doc=SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=42,leftMargin=42,
    topMargin=42,bottomMargin=58,title='Doggie House - Guía de ensamblaje',
    author='Doggie House / Kranken Tres D',
    subject='Primera edición comunitaria: impresión, ensamblaje y mantenimiento')
doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
print('Guide:',dest)
