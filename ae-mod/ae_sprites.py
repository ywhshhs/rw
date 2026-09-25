"""AE sprite kit — parametric pixel-art generator with centered 2.5D extrusion.
All ground units: light from top-left, dark side-walls down-right, whole shape
centered on the canvas so the game's unit-center == visual center."""
from PIL import Image

# ---- palette ----
TRACK=(17,17,0,255); TRACK_L=(45,45,12,255); TRACK_D=(10,10,0,255)
HULL=(69,74,84,255); HULL_L=(87,95,108,255); HULL_L2=(105,113,126,255)
HULL_D=(43,47,53,255); HULL_D2=(33,36,41,255); OUTLINE=(25,27,31,255)
SIDE=(32,35,40,255); WHEEL=(30,32,36,255); WHEEL_L=(70,74,82,255)
GREEN=(0,148,0,255); GREEN_L=(0,190,0,255)
ROCKET=(200,60,40,255); ROCKET_L=(255,130,70,255)
TAN=(122,112,82,255); TAN_L=(146,136,104,255); TAN_D=(92,84,58,255); TSIDE=(60,55,38,255)
OHULL=(96,98,66,255); OHULL_L=(116,118,84,255); OHULL_L2=(134,136,100,255)
OHULL_D=(70,72,46,255); OHULL_D2=(52,54,34,255); OSIDE=(40,42,26,255)
GOLD=(255,200,80,255); GOLD_D=(170,125,40,255)
CRANE=(160,120,50,255); CRANE_L=(195,155,80,255); CLAW=(90,86,60,255)
DISH=(125,133,145,255); DISH_L=(160,168,180,255)
WRECK=(30,33,38,255); WRECK_D=(12,12,12,255)

def px(im,x,y,c):
    if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y),c)

def outline_region(im, sil):
    for (x,y) in sil:
        for ddx,ddy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+ddx,y+ddy
            if (nx,ny) not in sil: px(im,nx,ny,OUTLINE)

def extrude(im, sil, top_fn, side, dx, dy, base=HULL):
    """Centered extrusion: canvas must be W+2dx x H+2dy. Top surface drawn at
    (dx,dy), walls at (2dx,2dy) -> whole shape centered on canvas center."""
    sil=set(sil)
    for (x,y) in sil: px(im, x+2*dx, y+2*dy, side)
    for (x,y) in sil:
        for ddx,ddy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+2*dx+ddx, y+2*dy+ddy
            if not (0<=nx<im.width and 0<=ny<im.height): continue
            if (nx-2*dx,ny-2*dy) not in sil and im.getpixel((nx,ny))[3]==0:
                px(im,nx,ny,OUTLINE)
    for (x,y) in sil: px(im, x+dx, y+dy, base)
    top_fn(im, sil, dx, dy)

def finish(sil, top_fn, side, dx, dy, base, w, h):
    im = Image.new('RGBA',(w+2*dx, h+2*dy),(0,0,0,0))
    extrude(im, sil, top_fn, side, dx, dy, base)
    return im

# ---- silhouette builders (top surface coordinates in local space 0..w, 0..h) ----
def tracked(w, h, tw=None, y0=0):
    tw = tw or max(3,int(w*0.2))
    s = {(x,y) for y in range(y0,h) for x in range(0,w)}
    return s, tw

def wheeled(w, h, ww=2):
    s = {(x,y) for y in range(0,h) for x in range(0,w)}
    return s, ww

def tracks_detail(im, sil, w, tw, shift, ox=0, oy=0):
    for (x,y) in sil:
        lx = x - ox; ly = y - oy
        if lx<tw or lx>=w-tw:
            px(im,x,y, TRACK_L if (ly+shift)%2==0 else TRACK)
    for (x,y) in sil:
        lx = x - ox
        if lx==0 or lx==tw-1 or lx==w-tw or lx==w-1:
            px(im,x,y,TRACK_D)

# ---- unit generators (local-space silhouettes; top_fn(im, sil, ox, oy)) ----
def wreck(sil, w, h, path):
    im = Image.new('RGBA',(w,h),(0,0,0,0))
    for (x,y) in sil: px(im,x,y, WRECK if (x+y)%4 else WRECK_D)
    im.save(path)

def grasshopper():
    w,h,dx,dy = 18,18,2,2
    sil = {(x,y) for y in range(4,14) for x in range(3,15)}                       # chassis
    sil |= {(x,y) for y in range(6,12) for x in list(range(1,3))+[0]} | {(x,y) for y in range(6,12) for x in range(15,17)}
    sil |= {(x,y) for x in range(6,12) for y in (1,2)} | {(x,y) for x in range(5,11) for y in range(15,17)}
    def top(im, s, ox, oy):
        for (x,y) in s:
            lx,ly = x-ox, y-oy
            if ly<4 or ly>13: px(im,x,y,WHEEL)                                     # 4 wheel clusters
            elif lx<2 or lx>13: px(im,x,y,WHEEL)
            else: px(im,x,y,TAN)
        for lx in range(3,13):
            px(im,ox+lx,oy+2,TAN_L); px(im,ox+lx,oy+3,TAN_L)                       # roll cage
        for lx in (4,11):
            for ly in (5,6,7): px(im,ox+lx,oy+ly,TAN_D)                            # seats
        for lx in (5,10):
            for ly in (9,10): px(im,ox+lx,oy+ly,GREEN)                             # team dots
        for ly in (12,13): px(im,ox+7,oy+ly,TAN_L); px(im,ox+8,oy+ly,TAN_L)
        px(im,ox+12,oy+1,GREEN_L)                                                  # antenna
    im = finish(sil, top, TSIDE, dx, dy, TAN, w, h)
    im.save('units/ae_grasshopper/aeGrasshopper.png')
    wreck(sil, w, h, 'units/ae_grasshopper/aeGrasshopper_dead.png')

def vulture():
    w,h,dx,dy = 18,20,3,3
    sil = {(x,y) for y in range(1,17) for x in range(3,15)}
    sil |= {(x,y) for y in range(2,16) for x in list(range(1,3))+[15,17]}
    def top(im, s, ox, oy):
        for (x,y) in s:
            lx,ly = x-ox,y-oy
            if lx<2 or lx>=14: px(im,x,y, WHEEL if ly%5 else WHEEL_L)
            elif ly<5: px(im,x,y,HULL_L)
            elif 7<=ly<13: px(im,x,y,TAN_D)                                        # cargo bed
            else: px(im,x,y,TAN)
        for lx in range(6,12):
            for ly in range(8,12):
                if (lx+ly)%3: px(im,ox+lx,oy+ly,CLAW)                              # scrap in bed
        for lx in (7,10): px(im,ox+lx,oy+9,GREEN)
        for ly in range(1,7): px(im,ox+13,oy+ly,CRANE); px(im,ox+14,oy+ly,CRANE)   # crane
        px(im,ox+14,oy+1,CRANE_L); px(im,ox+13,oy+1,CRANE_L)
        px(im,ox+13,oy+0,OUTLINE); px(im,ox+14,oy+0,OUTLINE)
    im = finish(sil, top, TSIDE, dx, dy, TAN, w, h)
    im.save('units/ae_vulture/aeVulture.png')
    wreck(sil, w, h, 'units/ae_vulture/aeVulture_dead.png')

def boar():
    w,h,dx,dy = 20,25,3,3
    sil = {(x,y) for y in range(0,h) for x in range(0,w)}
    def top(im, s, ox, oy):
        for (x,y) in s:
            lx,ly = x-ox,y-oy
            if lx<4 or lx>=16: px(im,x,y, TRACK_L if ly%2==0 else TRACK)
            else: px(im,x,y,HULL)
        for lx in (0,3,16,19):
            for ly in range(0,h): px(im,ox+lx,oy+ly,TRACK_D)
        for lx in range(4,16):
            for ly in (0,1,2,3): px(im,ox+lx,oy+ly,HULL_L)
        for ly in (0,1):
            for lx in range(6,14): px(im,ox+lx,oy+ly,HULL_L2)
        for ly in range(4,25): px(im,ox+4,oy+ly,OUTLINE); px(im,ox+15,oy+ly,OUTLINE)
        for ly in (5,6):
            for lx in range(7,13): px(im,ox+lx,oy+ly,GREEN)
        px(im,ox+9,oy+5,GREEN_L); px(im,ox+10,oy+5,GREEN_L)
        for ly in range(7,24,4): px(im,ox+5,oy+ly,HULL_D2); px(im,ox+14,oy+ly,HULL_D2)
        for ly in range(19,24):
            for lx in range(6,14):
                if lx not in (9,10): px(im,ox+lx,oy+ly,OUTLINE)
    im = finish(sil, top, SIDE, dx, dy, HULL, w, h)
    im.save('units/ae_boar/aeBoar.png')
    # turret: single long gun
    tw,th,tdx,tdy = 12,20,3,3
    tsil = {(x,y) for y in range(9,17) for x in range(3,9)} | {(x,y) for y in range(1,9) for x in range(5,7)}
    def ttop(im, s, ox, oy):
        for (x,y) in s: px(im,x,y,HULL)
        for (x,y) in s:
            if y<9: px(im,x,y,HULL_D)
        for lx in range(3,9): px(im,ox+lx,oy+9,HULL_L); px(im,ox+lx,oy+16,OUTLINE)
        for ly in range(9,17): px(im,ox+3,oy+ly,OUTLINE); px(im,ox+8,oy+ly,OUTLINE)
        px(im,ox+5,oy+1,OUTLINE); px(im,ox+6,oy+1,OUTLINE)
        px(im,ox+5,oy+2,HULL_L2); px(im,ox+6,oy+2,HULL_L2)
        for lx in (5,6):
            for ly in (12,13): px(im,ox+lx,oy+ly,GREEN)
    t = finish(tsil, ttop, SIDE, tdx, tdy, HULL, tw, th)
    t.save('units/ae_boar/aeBoar_turret.png')
    wreck(sil, w, h, 'units/ae_boar/aeBoar_dead.png')

def hornet():
    w,h,dx,dy = 16,20,2,2
    sil = {(x,y) for y in range(0,h) for x in range(0,w)}
    def top(im, s, ox, oy):
        for (x,y) in s:
            lx,ly = x-ox,y-oy
            if lx<3 or lx>=13: px(im,x,y, TRACK_L if ly%2==0 else TRACK)
            else: px(im,x,y,HULL_L)
        for lx in range(3,13):
            for ly in (0,1,2): px(im,ox+lx,oy+ly,HULL_L2)
        for ly in range(0,20): px(im,ox+3,oy+ly,OUTLINE); px(im,ox+12,oy+ly,OUTLINE)
        for lx in range(3,13): px(im,ox+lx,oy+0,OUTLINE); px(im,ox+lx,oy+19,OUTLINE)
        for ly in (5,6):
            for lx in range(5,11): px(im,ox+lx,oy+ly,GREEN)
    im = finish(sil, top, SIDE, dx, dy, HULL_L, w, h)
    im.save('units/ae_hornet/aeHornet.png')
    tw,th,tdx,tdy = 14,20,2,2
    tsil = {(x,y) for y in range(8,14) for x in range(3,11)} | {(x,y) for y in range(1,8) for x in range(4,10)}
    def ttop(im, s, ox, oy):
        for (x,y) in s: px(im,x,y,HULL_L)
        for (x,y) in s:
            if y<8: px(im,x,y,HULL_D)
        for lx in range(3,11): px(im,ox+lx,oy+8,HULL_L2); px(im,ox+lx,oy+13,OUTLINE)
        for ly in range(8,14): px(im,ox+3,oy+ly,OUTLINE); px(im,ox+10,oy+ly,OUTLINE)
        for lx in (4,5,8,9): px(im,ox+lx,oy+1,OUTLINE)
        for lx in (4,5,8,9): px(im,ox+lx,oy+2,HULL_L2)                     # twin muzzle highlights
        for lx in (6,7):
            for ly in (10,11): px(im,ox+lx,oy+ly,GREEN)
    t = finish(tsil, ttop, SIDE, tdx, tdy, HULL_L, tw, th)
    t.save('units/ae_hornet/aeHornet_turret.png')
    wreck(sil, w, h, 'units/ae_hornet/aeHornet_dead.png')

def thorn():
    w,h,dx,dy = 18,21,3,3
    sil = {(x,y) for y in range(1,18) for x in range(0,w)}
    def top(im, s, ox, oy):
        for (x,y) in s:
            lx,ly = x-ox,y-oy
            if ly>=13: px(im,x,y, TRACK_L if ly%2==0 else TRACK)
            elif lx<2 or lx>=16: px(im,x,y, WHEEL if ly%4 else WHEEL_L)
            else: px(im,x,y,HULL)
        for lx in range(2,16):
            for ly in (1,2,3): px(im,ox+lx,oy+ly,HULL_L)
        for ly in (5,6):
            for lx in range(6,12): px(im,ox+lx,oy+ly,GREEN)
        px(im,ox+8,oy+5,GREEN_L)
        for lx in (5,6,10,11):
            for ly in range(0,6): px(im,ox+lx,oy+ly,HULL_D2)
            px(im,ox+lx,oy+0,OUTLINE); px(im,ox+lx,oy+1,HULL_L2)           # thick MGs
        for dx2,dy2 in [(-1,0),(0,-1),(1,0),(0,1)]: px(im,ox+12+dx2,oy+8+dy2,HULL_D2)
        px(im,ox+12,oy+8,HULL_L2)
        for ly in (8,9): px(im,ox+5,oy+ly,HULL_D2)
    im = finish(sil, top, SIDE, dx, dy, HULL, w, h)
    im.save('units/ae_thorn/aeThorn.png')
    wreck(sil, w, h, 'units/ae_thorn/aeThorn_dead.png')

def beaver():
    w,h,dx,dy = 18,20,3,3
    sil = {(x,y) for y in range(3,17) for x in range(0,w)}
    sil |= {(x,y) for y in range(0,3) for x in range(1,17)}
    def top(im, s, ox, oy):
        for (x,y) in s:
            lx,ly = x-ox,y-oy
            if ly<3: px(im,x,y, (220,180,40,255) if (lx//2)%2 else HULL_D)   # dozer hazard
            elif lx<4 or lx>=14: px(im,x,y, TRACK_L if ly%2==0 else TRACK)
            else: px(im,x,y,HULL)
        for lx in range(4,14):
            for ly in (3,4,5): px(im,ox+lx,oy+ly,HULL_L)
        for ly in range(3,17): px(im,ox+4,oy+ly,OUTLINE); px(im,ox+13,oy+ly,OUTLINE)
        for ly in (7,8):
            for lx in range(6,12): px(im,ox+lx,oy+ly,GREEN)
        for ly in range(12,17): px(im,ox+11,oy+ly,HULL_D); px(im,ox+12,oy+ly,HULL_D)
        px(im,ox+12,oy+17,HULL_L2); px(im,ox+11,oy+17,HULL_L2)
    im = finish(sil, top, SIDE, dx, dy, HULL, w, h)
    im.save('units/ae_beaver/aeBeaver.png')
    wreck(sil, w, h, 'units/ae_beaver/aeBeaver_dead.png')

for f in (grasshopper, vulture, boar, hornet, thorn, beaver): f()
print("ALL 6 UNITS REGENERATED: centered 2.5D + min 16px")

# ============ EXTENDED CHASSIS + TURRET GENERATORS (batch 2-5) ============
ACCENTS = {
 "steel": (69,74,84,255), "olive": (96,98,66,255), "dark": (52,56,64,255),
 "purple": (86,72,110,255), "gold": (120,104,62,255), "red": (110,62,58,255),
 "tan": (122,112,82,255), "white": (150,152,158,255),
}
ACCENT_L = {k: tuple(min(255,c+34) for c in v[:3])+(255,) for k,v in ACCENTS.items()}

def chassis_silhouette(kind, w, h):
    """Returns (silhouette, accent_key_default) for a chassis type in local space."""
    if kind == "spider":
        s  = {(x,y) for y in range(4,h-4) for x in range(3,w-3)}                  # abdomen
        for cx,cy in [(2,2),(w-3,2),(2,h-3),(w-3,h-3)]:                            # 4 leg pods
            s |= {(cx+dx,cy+dy) for dx in (-1,0,1) for dy in (-1,0,1)}
        for i in range(1,4):
            s |= {(1+ (0 if i<2 else -1), int(h*0.2)+i*2)}
            s |= {(w-2+ (0 if i<2 else 1), int(h*0.2)+i*2)}
        return s
    if kind == "biped":
        s  = {(x,y) for y in range(3,h-3) for x in range(4,w-4)}                  # torso
        s |= {(x,y) for y in range(h-4,h) for x in list(range(2,4))+[w-4,w-2]}           # legs
        s |= {(x,y) for y in range(0,3) for x in range(5,w-5)}                      # head
        return s
    if kind == "hover":
        r = min(w,h)//2
        cx, cy = w//2, h//2
        s = {(x,y) for x in range(w) for y in range(h)
             if (x-cx)**2+(y-cy)**2 <= r*r}
        return s
    if kind in ("crawler","nuke_silo","titan","shield_anchor","aa_battery","factory"):
        s = {(x,y) for y in range(2,h-1) for x in range(0,w)}                       # wide flat
        s |= {(x,y) for y in range(0,2) for x in range(2,w-2)}                      # front plate
        return s
    if kind == "artillery":
        s  = {(x,y) for y in range(2,h-1) for x in range(2,w-2)}
        s |= {(x,y) for y in range(h-4,h) for x in range(1,w-1)}                     # baseplate
        return s
    if kind == "medic":
        return {(x,y) for y in range(1,h-1) for x in range(2,w-2)}
    # tracked / heavy_tracked / wheeled / halftrack default rect
    return {(x,y) for y in range(0,h) for x in range(0,w)}

def detail_common(im, s, ox, oy, w, h, accent, kind):
    A  = ACCENTS[accent]; AL = ACCENT_L[accent]
    for (x,y) in s:
        lx,ly = x-ox,y-oy
        if kind in ("tracked","heavy_tracked") and (lx<3 or lx>=w-3):
            px(im,x,y, TRACK_L if ly%2==0 else TRACK)
        elif kind=="wheeled" and (lx<2 or lx>=w-2):
            px(im,x,y, WHEEL if ly%4 else WHEEL_L)
        else:
            px(im,x,y,A)
    # glacis highlight + team stripe
    for (x,y) in s:
        lx,ly = x-ox,y-oy
        if ly<3 and 2<=lx<w-2: px(im,x,y,AL)
    sy = int(h*0.30)
    for (x,y) in s:
        lx,ly = x-ox,y-oy
        if ly in (sy,sy+1) and 3<=lx<w-3: px(im,x,y,GREEN)

def generate_body(kind, w, h, accent, dx=3, dy=3):
    sil = chassis_silhouette(kind, w, h)
    def top(im, s, ox, oy):
        detail_common(im, s, ox, oy, w, h, accent, kind)
    return finish(sil, top, (28,30,34,255), dx, dy, ACCENTS[accent], w, h)

def generate_turret(kind, accent, w=14, h=22, dx=3, dy=3):
    """kind: gun|mortar|missiles|beam|flame|dish|mgs|nuke|transport"""
    A  = ACCENTS[accent]; AL = ACCENT_L[accent]
    if kind == "gun":
        tsil = {(x,y) for y in range(h-10,h-4) for x in range(3,w-3)} | {(x,y) for y in range(3,h-10) for x in range(w//2-2,w//2+2)}
    elif kind == "mortar":
        tsil = {(x,y) for y in range(h-8,h-3) for x in range(3,w-3)}
        tsil |= {(x,y) for y in range(3,h-8) for x in range(w//2-3,w//2+3)}
    elif kind in ("missiles","aa_battery"):
        tsil = {(x,y) for y in range(h-8,h-3) for x in range(2,w-2)}
        tsil |= {(x,y) for y in range(2,h-8) for x in range(3,w-3)}
    elif kind == "beam":
        tsil = {(x,y) for y in range(h-9,h-3) for x in range(3,w-3)}
        tsil |= {(x,y) for y in range(2,h-9) for x in range(w//2-1,w//2+3)}
    elif kind == "flame":
        tsil = {(x,y) for y in range(h-8,h-3) for x in range(3,w-3)}
        tsil |= {(x,y) for y in range(3,h-8) for x in range(w//2-2,w//2+2)}
    elif kind == "dish":
        tsil = {(x,y) for y in range(h-6,h-2) for x in range(4,w-4)}
        tsil |= {(x,y) for y in range(3,h-6) for x in range(w//2-2,w//2+2)}
    elif kind == "transport":
        tsil = {(x,y) for y in range(h-6,h) for x in range(2,w-2)}
    elif kind == "nuke":
        tsil = {(x,y) for y in range(h-8,h) for x in range(2,w-2)}
        tsil |= {(x,y) for y in range(4,h-8) for x in range(5,w-5)}
    else:
        tsil = {(x,y) for y in range(h-9,h-3) for x in range(3,w-3)}
    def top(im, s, ox, oy):
        for (x,y) in s: px(im,x,y,A)
        for (x,y) in s:
            ly = y-oy
            if kind in ("gun","beam","flame","dish") and ly<10: px(im,x,y,HULL_D)
        # team light
        for lx in (w//2-1,w//2):
            for ly in (h-6,h-5): px(im,ox+lx,oy+ly,GREEN)
        if kind=="missiles":
            for lx in (4,7,w-6): px(im,ox+lx,oy+2,ROCKET); px(im,ox+lx,oy+3,ROCKET_L)
    return finish(tsil, top, (28,30,34,255), dx, dy, A, w, h)
