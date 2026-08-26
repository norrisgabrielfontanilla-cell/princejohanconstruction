#!/usr/bin/env python3
"""Generate an isometric construction-site SVG scene."""
K, KZ = 30.0, 26.0

def iso(x, y, z=0.0):
    return ((x - y) * K, (x + y) * K * 0.5 - z * KZ)

def pts(seq):
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in seq)

OUT = []
def emit(s): OUT.append(s)

def shade(hex_color, factor):
    h = hex_color.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, min(255, int(c * factor))) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"

def box(x0, y0, x1, y1, zb, zt, color, stroke=None, op=1.0, cls=""):
    """Draw an isometric box. Faces: top, x1-face (right), y1-face (left)."""
    top = [iso(x0,y0,zt), iso(x1,y0,zt), iso(x1,y1,zt), iso(x0,y1,zt)]
    right = [iso(x1,y0,zt), iso(x1,y1,zt), iso(x1,y1,zb), iso(x1,y0,zb)]
    left = [iso(x0,y1,zt), iso(x1,y1,zt), iso(x1,y1,zb), iso(x0,y1,zb)]
    sw = f' stroke="{stroke}" stroke-width="1.1" stroke-linejoin="round"' if stroke else ''
    c = f' class="{cls}"' if cls else ''
    emit(f'<g{c} opacity="{op}">')
    emit(f'<polygon points="{pts(left)}"  fill="{shade(color,.70)}"{sw}/>')
    emit(f'<polygon points="{pts(right)}" fill="{shade(color,.86)}"{sw}/>')
    emit(f'<polygon points="{pts(top)}"   fill="{shade(color,1.06)}"{sw}/>')
    emit('</g>')

def panel_x(x1, y, dy, z, dz, fill, op=1.0):
    """Rect on the x1-facing face."""
    p = [iso(x1,y,z+dz), iso(x1,y+dy,z+dz), iso(x1,y+dy,z), iso(x1,y,z)]
    emit(f'<polygon points="{pts(p)}" fill="{fill}" opacity="{op}"/>')

def panel_y(y1, x, dx, z, dz, fill, op=1.0):
    """Rect on the y1-facing face."""
    p = [iso(x,y1,z+dz), iso(x+dx,y1,z+dz), iso(x+dx,y1,z), iso(x,y1,z)]
    emit(f'<polygon points="{pts(p)}" fill="{fill}" opacity="{op}"/>')

def slab(x0, y0, x1, y1, z, color, th=0.16):
    box(x0, y0, x1, y1, z - th, z, color)

def col(x, y, zb, zt, color, w=0.16):
    box(x, y, x + w, y + w, zb, zt, color)

def line3(a, b, stroke, w=2.4, cls="", extra=""):
    (x1,y1),(x2,y2) = iso(*a), iso(*b)
    c = f' class="{cls}"' if cls else ''
    emit(f'<line{c} x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
         f'stroke="{stroke}" stroke-width="{w}" stroke-linecap="round"{extra}/>')

# ---------------- palette ----------------
CONCRETE = "#ded9d1"
CONCRETE_D = "#b9b3a9"
DARKTOWER = "#59606a"
CREAM     = "#e0d6c4"
GLASS     = "#8fa6b8"
GLASS_LT  = "#b9cbd8"
TIMBER    = "#c2692b"
GROUND    = "#b4bac4"
STEEL     = "#8c93a0"
YELLOW    = "#e3bf39"
RED       = "#cf4433"
WHITE     = "#e9e9ea"

emit('<g id="scene">')

# ---------------- ground plate ----------------
box(-1, -1, 25, 15, -0.9, 0, GROUND)
# paving / road
panel_y(15, -1, 26, -0.9, 0.9, shade(GROUND, .62))
p = [iso(-1,-1,0), iso(25,-1,0), iso(25,15,0), iso(-1,15,0)]
emit(f'<polygon points="{pts(p)}" fill="{shade(GROUND,1.05)}"/>')
# road band across the front
p = [iso(-1,11.6,0.01), iso(25,11.6,0.01), iso(25,14.4,0.01), iso(-1,14.4,0.01)]
emit(f'<polygon points="{pts(p)}" fill="#9aa1ac"/>')
for i in range(0, 25, 3):
    p = [iso(i,12.95,0.02), iso(i+1.5,12.95,0.02), iso(i+1.5,13.05,0.02), iso(i,13.05,0.02)]
    emit(f'<polygon points="{pts(p)}" fill="#e6e8ea" opacity=".75"/>')
# site dirt patch
p = [iso(2,7.2,0.01), iso(9,7.2,0.01), iso(9,11.2,0.01), iso(2,11.2,0.01)]
emit(f'<polygon points="{pts(p)}" fill="#a99c88" opacity=".8"/>')

# ---------------- BACK-LEFT: skeleton frame building ----------------
# concrete frame, 7 floors, open (under construction)
FX0, FY0, FX1, FY1 = 1.2, 1.0, 7.2, 6.0
for f in range(7):
    z = f * 1.5
    slab(FX0, FY0, FX1, FY1, z + 1.5, CONCRETE)
    for cx in (FX0, FX0+3, FX1-0.16):
        for cy in (FY0, FY0+2.5, FY1-0.16):
            col(cx, cy, z, z + 1.5, CONCRETE_D)
# core wall
box(FX0+0.4, FY0+0.4, FX0+2.2, FY0+2.0, 0, 9.0, shade(CONCRETE,.92))
# a couple of clad floors at the bottom
for f in range(2):
    z = f * 1.5
    panel_x(FX1, FY0+0.2, FY1-FY0-0.4, z+0.35, 0.85, GLASS)
    panel_y(FY1, FX0+0.2, FX1-FX0-0.4, z+0.35, 0.85, GLASS)
# rooftop rail
for xa, ya, xb, yb in [(FX0,FY1,FX1,FY1), (FX1,FY0,FX1,FY1)]:
    line3((xa,ya,10.5),(xb,yb,10.5), "#8d949e", 2)

# ---------------- BACK-CENTRE: tall dark tower ----------------
TX0, TY0, TX1, TY1 = 8.6, 0.6, 13.0, 5.2
box(TX0, TY0, TX1, TY1, 0, 17.0, DARKTOWER)
# balcony bands + windows
for f in range(11):
    z = 1.2 + f * 1.4
    panel_x(TX1, TY0+0.3, TY1-TY0-0.6, z, 0.5, "#8e97a3", .95)
    panel_y(TY1, TX0+0.3, TX1-TX0-0.6, z, 0.5, "#79828e", .95)
    # slab lip
    box(TX0-0.1, TY0-0.1, TX1+0.1, TY1+0.1, z+0.5, z+0.6, "#aeb6c0")
# roof plant
box(TX0+0.6, TY0+0.6, TX0+2.0, TY0+2.0, 17.0, 17.9, "#7c838d")
box(TX1-1.8, TY1-1.8, TX1-0.5, TY1-0.5, 17.0, 17.6, "#6d747e")

# ---------------- RIGHT: cream apartment block ----------------
AX0, AY0, AX1, AY1 = 14.6, 2.4, 21.4, 8.6
box(AX0, AY0, AX1, AY1, 0, 9.6, CREAM)
for f in range(6):
    z = 0.9 + f * 1.45
    # recessed balconies on both visible faces
    panel_x(AX1, AY0+0.35, AY1-AY0-0.7, z, 0.8, shade(CREAM,.60))
    panel_y(AY1, AX0+0.35, AX1-AX0-0.7, z, 0.8, shade(CREAM,.60))
    box(AX0-0.1, AY0-0.1, AX1+0.1, AY1+0.1, z+0.8, z+0.95, shade(CREAM,1.08))
    # orange under-balcony accent every other floor
    if f % 2 == 1:
        panel_x(AX1+0.001, AY0+0.5, 1.6, z+0.15, 0.5, TIMBER, .95)
# roof parapet + units
box(AX0, AY0, AX1, AY1, 9.6, 10.0, shade(CREAM,1.1))
box(AX0+1.0, AY0+1.0, AX0+2.6, AY0+2.6, 10.0, 10.8, "#a49a8a")

# ---------------- FRONT-LEFT: glass podium ----------------
GX0, GY0, GX1, GY1 = 0.8, 7.0, 6.6, 11.4
box(GX0, GY0, GX1, GY1, 0, 5.6, GLASS)
for f in range(4):
    z = 0.5 + f * 1.3
    panel_x(GX1, GY0+0.25, GY1-GY0-0.5, z, 0.95, GLASS_LT, .85)
    panel_y(GY1, GX0+0.25, GX1-GX0-0.5, z, 0.95, GLASS_LT, .85)
    box(GX0-0.08, GY0-0.08, GX1+0.08, GY1+0.08, z+0.95, z+1.08, "#dfe3e7")
# mullions
for i in range(1, 6):
    line3((GX1, GY0+i*0.72, 0.4), (GX1, GY0+i*0.72, 5.4), "#e4e9ed", 1.3)
box(GX0, GY0, GX1, GY1, 5.6, 5.9, "#cfd5db")

# ---------------- FRONT-RIGHT: timber site office ----------------
OX0, OY0, OX1, OY1 = 13.4, 9.4, 18.6, 13.0
box(OX0, OY0, OX1, OY1, 0, 2.6, TIMBER)
for i in range(6):
    line3((OX1, OY0+0.2+i*0.55, 0.15), (OX1, OY0+0.2+i*0.55, 2.5), shade(TIMBER,.72), 1.6)
panel_y(OY1, OX0+0.5, 2.2, 0.4, 1.5, "#cfd9df", .9)
panel_y(OY1, OX0+3.2, 1.4, 0.4, 1.5, "#cfd9df", .9)
box(OX0-0.15, OY0-0.15, OX1+0.15, OY1+0.15, 2.6, 2.8, "#8d949e")

# ---------------- scaffolding on the frame building ----------------
emit('<g opacity=".95">')
for i in range(5):
    x = FX0 + i * 1.5
    line3((x, FY1+0.55, 0), (x, FY1+0.55, 10.6), STEEL, 2.2)
for f in range(8):
    z = f * 1.35
    line3((FX0, FY1+0.55, z), (FX1, FY1+0.55, z), STEEL, 1.8)
for f in range(0, 7, 2):
    z = f * 1.35
    line3((FX0, FY1+0.55, z), (FX0+1.5, FY1+0.55, z+1.35), STEEL, 1.3)
emit('</g>')

# ---------------- construction hoist (climbs the frame) ----------------
(_hx, _hy) = iso(FX1 + 0.75, FY1 - 1.2, 0.35)
emit(f'<line x1="{_hx:.1f}" y1="{_hy:.1f}" x2="{_hx:.1f}" y2="{_hy-268:.1f}" stroke="#9aa1ac" stroke-width="3"/>')
emit(f'<line x1="{_hx-5:.1f}" y1="{_hy:.1f}" x2="{_hx-5:.1f}" y2="{_hy-268:.1f}" stroke="#9aa1ac" stroke-width="2"/>')
emit('<g class="hoistCage">')
box(FX1+0.55, FY1-1.55, FX1+1.15, FY1-0.75, 0.35, 1.5, "#d8843a")
emit('</g>')

# ---------------- tower cranes ----------------
def crane(mx, my, height, jib_len, back_len, color, hook_cls, beacon_cls, dirn=1):
    """Lattice tower crane. dirn=+1 jib runs along +x, -1 along -x."""
    w = 0.55
    emit('<g>')
    # base block
    box(mx-0.5, my-0.5, mx+w+0.5, my+w+0.5, 0, 0.5, "#9aa1ac")
    # mast: 4 legs + lacing
    legs = [(mx,my),(mx+w,my),(mx+w,my+w),(mx,my+w)]
    for (lx,ly) in legs:
        line3((lx,ly,0),(lx,ly,height), color, 2.6)
    seg = height / 9.0
    for i in range(10):
        z = i*seg
        line3((mx,my,z),(mx+w,my,z), color, 1.5)
        line3((mx+w,my,z),(mx+w,my+w,z), color, 1.5)
        if i < 9:
            line3((mx,my,z),(mx+w,my,z+seg), color, 1.2)
            line3((mx+w,my,z),(mx+w,my+w,z+seg), color, 1.2)
    # slewing platform
    box(mx-0.35, my-0.35, mx+w+0.35, my+w+0.35, height, height+0.5, shade(color,.9))
    ztop = height + 0.5
    cx, cy = mx + w/2, my + w/2
    # A-frame cat head
    line3((cx,cy,ztop),(cx,cy,ztop+2.4), color, 2.4)
    # jib (top + bottom chord + lacing)
    jx = cx + dirn*jib_len
    line3((cx,cy,ztop+0.45),(jx,cy,ztop+0.45), color, 2.6)
    line3((cx,cy,ztop-0.15),(jx,cy,ztop-0.15), color, 2.0)
    n = int(jib_len)
    for i in range(n):
        xa = cx + dirn*i
        xb = cx + dirn*(i+1)
        line3((xa,cy,ztop-0.15),(xb,cy,ztop+0.45), color, 1.2)
    # counter jib + weight
    bx = cx - dirn*back_len
    line3((cx,cy,ztop+0.45),(bx,cy,ztop+0.45), color, 2.4)
    line3((cx,cy,ztop-0.15),(bx,cy,ztop-0.1), color, 1.6)
    box(bx-0.5, cy-0.5, bx+0.5, cy+0.5, ztop-0.55, ztop+0.55, "#7d838d")
    # tie bars
    line3((cx,cy,ztop+2.4),(jx-dirn*0.4,cy,ztop+0.45), "#cfd4da", 1.5)
    line3((cx,cy,ztop+2.4),(bx+dirn*0.3,cy,ztop+0.45), "#cfd4da", 1.5)
    # trolley (static) + rope (scaleY) + hook block (translateY) - synced animation
    tx = cx + dirn*(jib_len*0.62)
    (hx, hy) = iso(tx, cy, ztop-0.15)
    L = 150.0
    emit(f'<rect x="{hx-5:.1f}" y="{hy-4:.1f}" width="10" height="5" rx="1.5" fill="#7d838d"/>')
    emit(f'<line class="rope {hook_cls}-rope" x1="{hx:.1f}" y1="{hy:.1f}" '
         f'x2="{hx:.1f}" y2="{hy+L:.1f}" stroke="#b7bcc3" stroke-width="1.5" '
         f'style="transform-origin:{hx:.1f}px {hy:.1f}px"/>')
    emit(f'<g class="hook {hook_cls}-hook">')
    emit(f'<rect x="{hx-4:.1f}" y="{hy+L:.1f}" width="8" height="10" rx="1.5" fill="{RED}"/>')
    emit(f'<rect x="{hx-7:.1f}" y="{hy+L+10:.1f}" width="14" height="4" rx="1.5" fill="#7d838d"/>')
    emit('</g>')
    # beacon
    (bxp, byp) = iso(cx, cy, ztop+2.6)
    emit(f'<circle class="{beacon_cls}" cx="{bxp:.1f}" cy="{byp:.1f}" r="3.2" fill="#ff5a3c"/>')
    emit('</g>')

crane(2.0, 12.6, 15.0, 9.0, 3.2, YELLOW, "hookA", "beaconA", dirn=1)
crane(15.6, 0.2, 19.5, 9.5, 3.4, RED,    "hookB", "beaconB", dirn=-1)
crane(22.6, 10.4, 16.5, 8.5, 3.0, STEEL,  "hookC", "beaconC", dirn=-1)

# ---------------- vehicles ----------------
def truck(x, y, body, cls=""):
    c = f' class="{cls}"' if cls else ''
    emit(f'<g{c}>')
    box(x, y, x+1.9, y+0.95, 0, 0.85, body)
    box(x+1.9, y+0.06, x+2.8, y+0.9, 0, 0.62, shade(body,1.12))
    box(x+0.15, y+0.1, x+0.45, y+0.85, -0.12, 0.1, "#3a3f46")
    box(x+2.2, y+0.1, x+2.5, y+0.85, -0.12, 0.1, "#3a3f46")
    emit('</g>')

def car(x, y, body, cls=""):
    c = f' class="{cls}"' if cls else ''
    emit(f'<g{c}>')
    box(x, y, x+1.6, y+0.8, 0, 0.42, body)
    box(x+0.35, y+0.08, x+1.15, y+0.72, 0.42, 0.72, shade(body,.8))
    emit('</g>')

truck(3.2, 12.2, RED, "moveA")
truck(8.0, 12.2, "#d8843a", "moveB")
car(15.2, 12.3, WHITE, "moveC")
car(18.6, 12.3, "#cfd3d8", "moveD")

# material stacks
box(9.6, 9.2, 12.0, 10.4, 0, 0.45, "#a8a094")
box(9.7, 9.3, 11.9, 10.3, 0.45, 0.8, "#b6ada0")
box(6.4, 8.6, 7.8, 9.6, 0, 0.55, TIMBER)
# site fence
for i in range(14):
    x = 1.0 + i*1.3
    line3((x, 11.5, 0), (x, 11.5, 1.05), "#cfd4da", 1.6)
line3((1.0, 11.5, 1.0), (1.0+13*1.3, 11.5, 1.0), "#cfd4da", 1.4)
line3((1.0, 11.5, 0.45), (1.0+13*1.3, 11.5, 0.45), "#cfd4da", 1.2)

emit('</g>')

body = "\n".join(OUT)

# Write next to this script's repo root, or to a path given as argv[1].
import os, sys
default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hero-scene.svg.frag")
out_path = sys.argv[1] if len(sys.argv) > 1 else default
with open(out_path, "w") as f:
    f.write(body)

print(f"Wrote {len(OUT)} SVG elements to {out_path}")
print("Paste this inside the <svg> in the .hero-bg block of index.html,")
print('replacing the existing <g id="scene"> ... </g>.')
