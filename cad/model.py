"""Doggie House v2. Dimensions in mm, component-side XY coordinates.

Original PCB holes locate the board on loose pins. Four releasable PETG
cantilevers hold the joint independently; there are no metal fasteners.
Copyright (c) 2026 Doggie House contributors. MIT.
"""
import json, math
from pathlib import Path
import numpy as np
import manifold3d as md
P=json.loads((Path(__file__).parent/'parameters.json').read_text(encoding='utf-8'))
SEG=64
W=P['pcb_width'];L=P['pcb_length']
HO=P['hole_edge_gap']+P['pcb_hole_diameter']/2
HOLES=[(HO,HO),(W-HO,HO),(HO,L-HO),(W-HO,L-HO)]
LATCHES=[(side,y) for side in (-1,1) for y in P['latch_y']]
PCB_Z=P['front_thickness']+P['front_standoff_height']
JOINT_Z=PCB_Z+P['pcb_thickness']
ROOF_Z=JOINT_Z+P['max_component_height']+P['component_clearance']
TOP_Z=ROOF_Z+P['rear_thickness']
def empty():return md.Manifold()
def rr(w,l,r,x=W/2,y=L/2):
    return md.CrossSection.square((w-2*r,l-2*r),center=True).offset(r,circular_segments=32).translate((x,y))
def box(w,l,h,x,y,z):return md.Manifold.cube((w,l,h)).translate((x,y,z))
def cylinder(d,h,x,y,z,n=SEG):return md.Manifold.cylinder(h,d/2,d/2,n).translate((x,y,z))
def extrude(cs,z,h):return cs.extrude(h).translate((0,0,z))
def outer():
    return rr(P['body_width'],P['body_length'],P['body_radius'])
def cavity():
    c=P['pcb_clearance_per_side']
    return rr(W+2*c,L+2*c,1)
def aperture():
    a=1.8;c=9.2
    return md.CrossSection([np.array([[a+c,a],[W-a-c,a],[W-a,a+c],[W-a,L-a-c],
        [W-a-c,L-a],[a+c,L-a],[a,L-a-c],[a,a+c]],float)])
def pane_outline():
    cs=aperture().offset(1.15,circular_segments=32)
    for x,y in HOLES:cs=cs-md.CrossSection.circle(3.65,SEG).translate((x,y))
    return cs
def usb_center():return P['usb_bottom_y']+P['usb_measured_width']/2+P['usb_y_adjustment']
def usb_bottom_z():return JOINT_Z-1+P['usb_z_adjustment']
def port_cuts():
    uc=usb_center();z=usb_bottom_z()
    v=box(10.8,P['usb_cut_width'],P['usb_cut_height'],-10,uc-P['usb_cut_width']/2,z)
    v=v+box(7.5,P['usb_outer_width'],P['usb_outer_height'],-10,uc-P['usb_outer_width']/2,z-.8)
    v=v+box(P['db9_cut_width'],14,P['db9_cut_height'],W/2-P['db9_cut_width']/2,L-2,JOINT_Z)
    for x in (-10,W-1):v=v+box(11,14,13,x,80,JOINT_Z)
    return v
def roof_vents():
    cs=md.CrossSection()
    for y in P['vent_rows']:
        for x in P['vent_columns']:
            cs=cs+rr(P['vent_width'],P['vent_length'],1.5,0,0).rotate(-18).translate((x,y))
    return cs
def side_vent_section():
    cs=md.CrossSection()
    for y in P['side_vent_y']:
        cs=cs+rr(P['side_vent_width'],P['side_vent_height'],1.4,y,JOINT_Z+8)
    return cs
def side_vent_cuts():
    base=side_vent_section().extrude(12).transform(np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0]],float))
    return base.translate((-10,0,0))+base.translate((W-2,0,0))
def on_side(s,side):return s if side<0 else s.mirror((1,0,0)).translate((W,0,0))
def latch_bay(side,y,z0=None):
    z0=P['front_thickness'] if z0 is None else z0
    return on_side(box(2.7,P['latch_width']+1.2,P['latch_tip_z']+.4-z0,-4,y-(P['latch_width']+1.2)/2,z0),side)
def latch(side,y):
    t=P['latch_thickness'];w=P['latch_width'];z=P['front_thickness']
    s=box(t,w,P['latch_tip_z']-z+.2,-3.7,y-w/2,z-.2)
    # 45 degree lead-in cams the beam inward. Flat lower shoulder retains it.
    cs=md.CrossSection([np.array([[-3.6,P['latch_hook_z']],[-4.9,P['latch_hook_z']],
        [-4.9,P['latch_hook_z']+.7],[-3.6,P['latch_tip_z']]],float)],md.FillRule.EvenOdd)
    hook=cs.extrude(w).rotate((90,0,0)).translate((0,y+w/2,0))
    # Small root gusset reduces the abrupt section change at the bed plane.
    foot=md.CrossSection([np.array([[-2.5,z],[-1.9,z],[-2.5,z+.8]],float)]).extrude(w).rotate((90,0,0)).translate((0,y+w/2,0))
    return on_side(s+hook+foot,side)
def front():
    s=extrude(outer(),0,JOINT_Z)-extrude(cavity(),P['front_thickness'],JOINT_Z)
    s=s+extrude(rr(W+3,L+3,2)-cavity(),JOINT_Z,P['joint_lip_height'])
    for x,y in HOLES:
        s=s+cylinder(6.6,PCB_Z-P['front_thickness'],x,y,P['front_thickness'])
        s=s+cylinder(P['pcb_pin_diameter'],P['pcb_thickness']+.25,x,y,PCB_Z)
    s=s-extrude(aperture(),-1,P['front_thickness']+2)
    for side,y in LATCHES:s=s-latch_bay(side,y)
    for side,y in LATCHES:s=s+latch(side,y)
    return s-port_cuts()
def rear(direct_access=False):
    s=extrude(outer(),JOINT_Z,TOP_Z-JOINT_Z)-extrude(cavity(),JOINT_Z-.05,ROOF_Z-JOINT_Z+.05)
    s=s-extrude(rr(W+3.5,L+3.5,2.25),JOINT_Z-.02,P['joint_lip_height']+.27)
    for x,y in HOLES:
        s=s+cylinder(6,ROOF_Z-JOINT_Z-.1,x,y,JOINT_Z+.1)
        s=s-cylinder(3.2,.7,x,y,JOINT_Z-.05)
    s=s-port_cuts()-side_vent_cuts()
    for x in (7.25,62.75):s=s-extrude(rr(11,12.2,1.2,x,86.6),ROOF_Z-.1,P['rear_thickness']+1)
    s=s-extrude(roof_vents(),ROOF_Z-.1,P['rear_thickness']+1)
    tw=rr(P['toggle_width'],P['toggle_length'],1.8,P['toggle_center_x'],P['toggle_center_y'])
    s=s-extrude(tw,ROOF_Z-.1,P['rear_thickness']+1)
    s=s-extrude(tw.offset(.65,circular_segments=16),TOP_Z-.7,1)
    if direct_access:s=s-extrude(rr(11,23,2.2,63.5,18.2),ROOF_Z-.1,P['rear_thickness']+1)
    else:
        for x,y in (P['boot_center'],P['reset_center']):
            bottom=JOINT_Z+P['button_height_reference']+1.2
            s=s+cylinder(8,ROOF_Z-bottom+.2,x,y,bottom)
            s=s-cylinder(6.4,ROOF_Z-bottom+.3,x,y,bottom-.1)
            s=s-cylinder(4.6,P['rear_thickness']+.2,x,y,ROOF_Z-.05)
    for side,y in LATCHES:
        s=s-latch_bay(side,y,JOINT_Z-.1)
        opening=box(4.2,P['latch_width']+1.2,2.7,-5.5,y-(P['latch_width']+1.2)/2,P['latch_hook_z']-.25)
        s=s-on_side(opening,side)
    return s
def plunger(button_height=None):
    bh=P['button_height_reference'] if button_height is None else button_height
    tip=JOINT_Z+bh+P['plunger_tip_clearance']
    s=cylinder(4,TOP_Z+1.2-tip,0,0,tip)
    s=s+md.Manifold.cylinder(1,2,3,SEG).translate((0,0,ROOF_Z-2))
    return s+cylinder(6,1,0,0,ROOF_Z-1)
def pane():return extrude(pane_outline(),P['front_thickness'],P['window_sheet_thickness'])
def pcb_reference():
    s=box(W,L,P['pcb_thickness'],0,0,PCB_Z)
    for x,y in HOLES:s=s-cylinder(P['pcb_hole_diameter'],P['pcb_thickness']+2,x,y,PCB_Z-1)
    return s
def fit_frame():
    s=extrude(outer(),0,1.2)-extrude(aperture(),-.1,1.4)
    for x,y in HOLES:s=s-cylinder(3,1.5,x,y,-.1)
    return s
def controls_template():
    s=box(W,35,1.2,0,0,0)
    s=s-extrude(rr(P['toggle_width'],P['toggle_length'],1.8,P['toggle_center_x'],P['toggle_center_y']),-.1,1.5)
    for x,y in (P['boot_center'],P['reset_center']):s=s-cylinder(6,1.5,x,y,-.1)
    for x,y in HOLES[:2]:s=s-cylinder(3,1.5,x,y,-.1)
    return s
def closure_coupon():
    clip=box(10,16,TOP_Z+2,-6,P['latch_y'][0]-8,-1)
    return front()^clip,rear()^clip
def usb_coupon():
    clip=box(11,27,16.5,-6,21.5,0)
    return front()^clip,rear()^clip
def tolerance_coupon():
    s=box(45,15,3,0,0,0)
    for i,d in enumerate((2.5,2.7,3,4.6,6.4)):s=s-cylinder(d,4,5+i*8.5,7.5,-.1)
    return s
