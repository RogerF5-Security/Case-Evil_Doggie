"""Build a standalone WebGL viewer of the REAL CAD, with reference PCB art.
Requires the CAD requirements only. No browser/library/CDN dependencies at runtime.
"""
from pathlib import Path
import sys,json,base64,io,copy
ROOT=Path(__file__).resolve().parents[1]
DEV=ROOT.parents[1]/'work/cad_deps'
if DEV.exists():sys.path.insert(0,str(DEV))
sys.path.insert(0,str(ROOT/'cad'))
import numpy as np
from build import mesh,finished
from model import *
parts=[]
def add(s,color,kind,explode=0,alpha=1):
    t=mesh(s)
    tri=t.triangles.reshape(-1,3);norm=np.repeat(t.face_normals,3,axis=0)
    values=np.c_[tri,norm,np.zeros((len(tri),2))].astype('<f4')
    parts.append(dict(kind=kind,explode=explode,alpha=alpha,color=color,
        geometry=base64.b64encode(values.tobytes()).decode()))
def artwork():
    # Original Faraday dog artwork, rendered on a reference PCB plane, not on CAD.
    z=PCB_Z-.02
    v=np.array([[0,0,z],[70,0,z],[70,100,z],[0,100,z]],float)
    f=np.array([[0,2,1],[0,3,2]])
    # The artwork is viewed from the opposite side of component-side XY.
    uv=np.array([[1,0],[0,0],[0,1],[1,1]])
    values=np.c_[v[f].reshape(-1,3),np.tile([0,0,-1],(6,1)),uv[f].reshape(-1,2)].astype('<f4')
    png=(ROOT/'assets/pcb-art.png').read_bytes()
    parts.append(dict(kind='photo',explode=0,alpha=1,color=[1,1,1],
        geometry=base64.b64encode(values.tobytes()).decode(),
        texture='data:image/png;base64,'+base64.b64encode(png).decode()))

f,r,_=finished()
add(f,[.925,.40,.16],'frame',-25)
add(r,[.22,.27,.33],'rear',35)
add(pcb_reference(),[.055,.19,.31],'pcb')
artwork()
add(box(30,14,11.5,20,94,JOINT_Z),[.08,.10,.13],'db9')
add(box(30,1.8,10.4,20,108,JOINT_Z+1.8),[.70,.75,.80],'db9')
d=md.CrossSection([np.asarray([[-8,-3],[8,-3],[7,3],[-7,3]],float)]).offset(.6,circular_segments=16)
add(d.extrude(2).rotate((90,0,0)).translate((35,112,JOINT_Z+7)),[.40,.45,.50],'db9')
for x in (22,48):add(md.Manifold.cylinder(4,2.8,2.8,6).rotate((-90,0,0)).translate((x,108,JOINT_Z+7)),[.78,.65,.36],'db9')
for x in (1.5,59):
    add(box(9.5,10.5,9.5,x,81.3,JOINT_Z),[.10,.52,.66],'hardware')
    for y in (84,89):add(cylinder(3.5,.6,x+4.7,y,JOINT_Z+9.5),[.65,.70,.74],'hardware')
add(box(7.5,10,3.6,-1,usb_center()-5,JOINT_Z),[.60,.65,.70],'hardware')
add(box(.3,8,2,-1.15,usb_center()-4,JOINT_Z+.8),[.04,.05,.06],'hardware')
add(box(20,24,3.2,45,41,JOINT_Z),[.76,.67,.40],'hardware')
add(box(12,12,8.5,3,65,JOINT_Z),[.23,.25,.27],'hardware')
add(box(7,14,10,31.5,7,JOINT_Z),[.78,.76,.64],'hardware')
add(box(4.5,7,2,32.75,12,JOINT_Z+10),[.07,.08,.09],'hardware')
for pos in (P['boot_center'],P['reset_center']):
    add(box(4.5,4.5,1.2,pos[0]-2.25,pos[1]-2.25,JOINT_Z),[.42,.45,.48],'hardware')
    add(plunger().translate((*pos,0)),[.925,.40,.16],'plunger',35)
add(pane(),[.72,.89,.95],'pane',-12,.16)
template=(ROOT/'viewer/template.html').read_text(encoding='utf-8')
scene=dict(parts=parts,version=P['version'],units='mm',
    source_sha256=json.loads((ROOT/'docs/validation.json').read_text(encoding='utf-8'))['source_sha256'])
(ROOT/'viewer/index.html').write_text(template.replace('__SCENE__',json.dumps(scene,separators=(',',':'))),encoding='utf-8')
print(json.dumps(dict(viewer=str(ROOT/'viewer/index.html'),parts=len(parts)),indent=2))
