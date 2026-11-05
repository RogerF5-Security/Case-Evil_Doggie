"""Rebuild STL, 3MF layouts, fit coupons and mechanical validation. No G-code."""
from pathlib import Path
import sys,json,math,zipfile,hashlib,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DEV=ROOT.parents[1]/'work/cad_deps'
if DEV.exists():sys.path.insert(0,str(DEV))
import numpy as np
import trimesh
import manifold3d as md
from model import *


def mesh(s):
    # Remove sub-micron coplanar slivers before STL's float32 quantization.
    m=s.simplify(1e-6).to_mesh()
    t=trimesh.Trimesh(vertices=np.asarray(m.vert_properties)[:,:3],faces=np.asarray(m.tri_verts),process=True)
    t.update_faces(t.nondegenerate_faces(height=1e-6))
    t.remove_unreferenced_vertices()
    return t

def normalized(m):
    return m.copy().apply_translation(-m.bounds[0])

def print_pose(m,invert=False):
    m=m.copy()
    if invert: m.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]))
    return normalized(m)

def write_3mf(path,items):
    ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    ET.register_namespace('',ns)
    tag=lambda n:'{'+ns+'}'+n
    model=ET.Element(tag('model'),{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'es'})
    resources=ET.SubElement(model,tag('resources'));build=ET.SubElement(model,tag('build'))
    for i,(name,m,offset) in enumerate(items,1):
        obj=ET.SubElement(resources,tag('object'),{'id':str(i),'type':'model','name':name})
        me=ET.SubElement(obj,tag('mesh'));verts=ET.SubElement(me,tag('vertices'))
        tris=ET.SubElement(me,tag('triangles'))
        for v in m.vertices:
            ET.SubElement(verts,tag('vertex'),dict(zip(('x','y','z'),[f'{v[k]+offset[k]:.6f}' for k in range(3)])))
        for t in m.faces: ET.SubElement(tris,tag('triangle'),dict(zip(('v1','v2','v3'),map(str,t))))
        ET.SubElement(build,tag('item'),{'objectid':str(i)})
    ct='<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
    rel='<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',ct);z.writestr('_rels/.rels',rel)
        z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

def signature_section():
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp=TextPath((0,0),P['signature'],size=8,prop=FontProperties(family='DejaVu Sans',weight='bold'))
    cs=md.CrossSection([np.asarray(a) for a in tp.to_polygons()],md.FillRule.EvenOdd)
    a,b,c,d=cs.bounds();scale=P['signature_height']/(d-b)
    cs=cs.scale((scale,scale)).offset(.12,circular_segments=12)
    a,b,c,d=cs.bounds()
    # Mirror so the inscription reads normally looking INTO the open rear shell.
    return cs.translate((-(a+c)/2,-(b+d)/2)).mirror((1,0)).translate((35,32.5))

def finished():
    mark=extrude(signature_section(),ROOF_Z-.02,P['signature_depth']+.02)
    return front(),rear()-mark,rear(True)-mark

def build_all():
    target=ROOT/'models/stl';target.mkdir(parents=True,exist_ok=True)
    f,r,rd=finished()
    fp=print_pose(mesh(f));rp=print_pose(mesh(r),True)
    shaft=print_pose(mesh(plunger()))
    shafts=trimesh.util.concatenate([shaft,shaft.copy().apply_translation((12,0,0))])
    cf,cr=closure_coupon();uf,ur=usb_coupon()
    signature_patch=r^box(34,10,P['rear_thickness']+.2,18,27.5,ROOF_Z-.1)
    items=[('01_front_frame.stl',fp,1),('02_rear_cover.stl',rp,1),
      ('03_two_captive_buttons.stl',shafts,2),
      ('04_rear_direct_access_optional.stl',print_pose(mesh(rd),True),1),
      ('05_pcb_fit_template.stl',print_pose(mesh(fit_frame())),1),
      ('06_controls_template.stl',print_pose(mesh(controls_template())),1),
      ('07_clearance_coupon.stl',print_pose(mesh(tolerance_coupon())),1),
      ('08_snap_test_front.stl',print_pose(mesh(cf)),1),
      ('09_snap_test_rear.stl',print_pose(mesh(cr),True),1),
      ('10_usb_test_front.stl',print_pose(mesh(uf)),1),
      ('11_usb_test_rear.stl',print_pose(mesh(ur),True),1),
      ('12_signature_test.stl',print_pose(mesh(signature_patch),True),1)]
    validation=[]
    for name,t,count in items:
        assert t.is_watertight and t.is_winding_consistent and t.volume>0,name
        assert len(t.split())==count,(name,len(t.split()))
        assert abs(t.bounds[0,2])<1e-5
        t.export(target/name)
        again=trimesh.load(target/name)
        assert again.is_watertight and len(again.split())==count,name
        validation.append(dict(file=name,closed=True,solids=count,
          dimensions_mm=again.extents.round(3).tolist(),volume_cm3=round(float(again.volume)/1000,3)))
    overlaps={}
    pcb=pcb_reference()
    for name,a,b in [('frame_cover',f,r),('frame_pcb',f,pcb),('cover_pcb',r,pcb),('frame_window',f,pane())]:
        overlaps[name]=(a^b).volume();assert overlaps[name]<1e-5,(name,overlaps[name])
    for pos in (P['boot_center'],P['reset_center']):
        pl=plunger().translate((*pos,0))
        assert (pl^r).volume()<1e-5
    # Nominal USB keepout and lower clearance added in response to the prototype.
    uc=usb_center()
    usb=box(8,10,5,-6,uc-5,JOINT_Z-.1)
    lower=box(4.4,10,1.6,-4.9,uc-5,JOINT_Z-2.7)
    db9=box(30,12,15,20,98,JOINT_Z)
    for name,vol in [('usb_nominal',usb),('usb_lower_relief',lower),('db9_nominal',db9)]:
        assert ((f+r)^vol).volume()<1e-5,name
    # Four latch shoulders must encounter the catch ledges when the halves pull
    # 0.4 mm apart. This verifies engagement, NOT strength or fatigue life.
    retention_overlap=(f.translate((0,0,-.4))^r).volume()
    assert retention_overlap>1.0,retention_overlap
    # Check travel envelopes: the upper free end can deflect 0.95 mm inward.
    for side,y in LATCHES:
        tip=latch(side,y)^box(85,12,7,-7,y-6,10)
        translated=tip.translate((.95 if side<0 else -.95,0,0))
        assert (translated^r).volume()<1e-5
    layouts=[('doggie-house-standard.3mf',[
      ('Front frame',fp,(8,8,0)),('Rear cover',rp,(96,8,0)),
      ('Boot button',shaft,(188,16,0)),('Reset button',shaft,(200,16,0))],4),
      ('doggie-house-direct-access.3mf',[
      ('Front frame',fp,(8,8,0)),('Direct-access cover',print_pose(mesh(rd),True),(96,8,0))],2)]
    for name,layout,count in layouts:
        write_3mf(ROOT/'models'/name,layout)
        with zipfile.ZipFile(ROOT/'models'/name) as z:assert z.testzip() is None
        scene=trimesh.load(ROOT/'models'/name)
        assert len(scene.geometry)==count
        assert scene.extents[0]<230 and scene.extents[1]<230
    old_vent=5*rr(2.8,18,1.35,0,0).area()
    source_digest=hashlib.sha256(b''.join((HERE/n).read_text(encoding='utf-8').replace('\r\n','\n').encode('utf-8') for n in ['model.py','build.py','parameters.json'])).hexdigest()
    report=dict(version=P['version'],status='Digital checks passed; revised physical fit pending',
      source_sha256=source_digest,meshes=validation,
      dimensions_mm=[P['body_width'],P['body_length'],TOP_Z],
      derived=dict(pcb_dog_surface_z=PCB_Z,pcb_component_surface_z=JOINT_Z,
        roof_inside_z=ROOF_Z,usb_inner_bottom_z=usb_bottom_z(),
        usb_correction_z=P['usb_z_adjustment'],usb_center_y=uc,
        snap_clearance_z=.25,snap_beam_free_length=P['latch_tip_z']-P['front_thickness'],
        snap_beam_thickness=P['latch_thickness'],signature_roof_remaining=P['rear_thickness']-P['signature_depth']),
      ventilation=dict(roof_slots=14,side_slots=8,roof_open_area_mm2=round(roof_vents().area(),2),
        v1_roof_open_area_mm2=round(old_vent,2),roof_area_ratio=round(roof_vents().area()/old_vent,3),
        sides_open_area_mm2=round(2*side_vent_section().area(),2)),
      checks=dict(all_meshes_closed=True,stl_reimport=True,case_pcb_window_clear=True,
        plungers_clear=True,usb_lower_relief_clear=True,db9_clear=True,
        latch_free_tip_travel_clear=True,latch_retention_engagement=True,
        threemf_reimport=True,layout_within_230mm=True),
      overlap_volumes_mm3=overlaps,latch_retention_intersection_mm3=retention_overlap,
      not_verified=['Revised USB fit with real cable','PETG snap force and fatigue',
        'Signature legibility on actual printer','Button actuation/preload',
        'Thermal performance','Slicing and printing of v2'])
    (ROOT/'docs/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return f,r,rd

if __name__=='__main__':build_all()
