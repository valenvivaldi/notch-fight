"""Portal 2: Claude (the test subject: orange jumpsuit tied at the waist, white tank top, long-fall
boots, the Portal Gun) vs GLaDOS, hanging from the ceiling of an Aperture Science test chamber
(white panels, the CHAMBER 19 sign, the observation window). OH... IT'S YOU. Turrets pop up
(I SEE YOU, TARGET ACQUIRED) and neurotoxin creeps along the floor; Claude drops through a blue
portal and out of an orange one, then lines them up so the turret fire goes in one side and out
the other, straight into GLaDOS. Close-up: the yellow eye turns red — YOU MONSTER. Her personality
cores pop off (Wheatley babbles, the Space Core yells SPAAACE!), the ceiling cracks open; close-up:
Claude shoots a portal at the MOON, and the vacuum sucks cores, debris and GLaDOS out into space.
THIS WAS A TRIUMPH — the cake is a lie. GLaDOS is lowered back onto her arm, the toxin clears."""
from engine import *

THEME = 'portal'
N_ = 348
CX = 30                    # Claude's spot in the neutral pose
CEIL = 11                  # the black ceiling band ends here (the wall panels start below)
MOUNT = (156,8)            # where GLaDOS's body hangs from her arm (world)
LWALL, RWALL = 4, 178      # the wall faces that take a portal (left pillar, right pillar)
TUR = (106,122)            # turret x positions
GAP = (86,108)             # the crack in the ceiling (x span) the moon shows through
MOON = (98,5)
GSC = 1.25                 # GLaDOS's scale

BLUE = ((40,130,255),(170,220,255))       # portal rim, glow
ORANGE = ((255,130,20),(255,214,130))
YEL = (255,214,40); RED = (255,48,30)
TOX = (120,214,60)                          # neurotoxin
PANEL = (168,174,180); SEAM = (104,108,116)

# ---- Claude: the test subject ------------------------------------------------------------------
CHELL_PAL = {'1':(60,40,32),'2':(238,238,232),'3':(186,86,38),'4':(224,226,230),'5':(118,122,132)}

def _chell(spr):
    h0 = len(spr)
    spr = overlay(spr, ["..11111...", "111111111."], -1, 0)          # hair pulled back
    h = len(spr)
    def fn(x, y, t, l, r, c):
        if c == '.':
            if x == l-1 and t <= y <= t+2: return '1'                       # the ponytail
            return None
        inside = l <= x <= r
        if y >= h-2:                                                        # long-fall boots
            return '5' if (y == h-1 and (x == 0 or spr[y][x-1] == '.')) else '4'
        if inside and y in (t+5, t+6): return '2'                           # white tank top
        if inside and y == t+7: return '3'                                  # sleeves tied at the waist
        return None
    return recolor_rows(spr, fn)
CHELL = variant(_chell)
_HAND = {'guard':(13,4), 'guard2':(13,5), 'charge':(15,5), 'armsup':(12,0), 'punch':(16,5)}

def hand_of(pose, x, feet, flip=False):
    hx, hy = _HAND[pose]
    return hand_at(CHELL[pose], x, int(feet), flip, hx, hy, h=11)

# ---- text: the 3x5 font plus a wide M/W and the ' , . ! the font lacks or draws too wide ----------
_GL = {'M':["10001","11011","10101","10001","10001"], 'W':["10001","10001","10101","10101","01010"],
       "'":["1","1","0","0","0"], ',':["0","0","0","1","1"], '.':["0","0","0","0","1"], '!':["1","1","1","0","1"]}

def _txt_mask(txt):
    rows = [_GL[ch] if ch in _GL else [FONT.get(ch,FONT[' '])[i*3:i*3+3] for i in range(5)] for ch in txt]
    tw = sum(len(r[0])+1 for r in rows)
    m = Image.new('L', (max(1,tw), 5), 0); x = 0
    for r in rows:
        for j, row in enumerate(r):
            for i, b in enumerate(row):
                if b == '1': m.putpixel((x+i, j), 255)
        x += len(r[0])+1
    return m

def say(im, txt, y, c, scale=2, cx=W//2, outline=(0,0,0), left=None):
    """Scaled text centred at cx (or starting at x=left) with a dark outline. Returns its right edge."""
    m = _txt_mask(txt); m = m.resize((m.width*scale, m.height*scale), Image.NEAREST)
    x0 = int(cx-m.width//2) if left is None else left
    if outline:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1),(2,2)): im.paste(outline, (x0+dx, y+dy), m)
    im.paste(c, (x0, y), m)
    return x0+m.width

def small(im, txt, x, y, c, outline=(0,0,0), center=False):
    m = _txt_mask(txt); x = int(x-m.width//2) if center else int(x)
    if outline:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline, (x+dx, int(y)+dy), m)
    im.paste(c, (x, int(y)), m)

@fx('portal_say')
def _fx_say(d, im, e, f):
    _, txt, y, c, *rest = e; say(im, txt, y, c, cx=rest[0] if rest else W//2)

@fx('portal_small')
def _fx_small(d, im, e, f):
    _, txt, x, y, c = e; small(im, txt, x, y, c, center=True)

# ---- background: the test chamber --------------------------------------------------------------
def _aperture(d, cx, cy, r, c, bg):
    """The Aperture Science logo: a ring of 8 shutter blades around a hole."""
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    for k in range(8):
        a = k*math.pi/4
        d.line([cx+math.cos(a)*(r*0.35), cy+math.sin(a)*(r*0.35), cx+math.cos(a+0.9)*r, cy+math.sin(a+0.9)*r], fill=bg)
    d.ellipse([cx-r*0.3, cy-r*0.3, cx+r*0.3, cy+r*0.3], fill=bg)

def _chamber(d):
    d.rectangle([0, 0, W, GROUND], fill=(20,22,26))
    # white wall panels, a dark gap here and there
    rr = random.Random(19)
    for y0 in range(CEIL+1, GROUND, 12):
        for x0 in range(-4, W, 12):
            if rr.random() < 0.07 and 30 < x0 < 170: d.rectangle([x0, y0, x0+10, y0+10], fill=(34,36,40)); continue
            v = rr.randint(-6, 6)
            d.rectangle([x0, y0, x0+10, y0+10], fill=tuple(c+v for c in PANEL))
            d.line([x0, y0, x0+10, y0], fill=tuple(min(255,c+v+22) for c in PANEL))
            d.line([x0+10, y0+1, x0+10, y0+10], fill=tuple(c+v-24 for c in PANEL))
        d.line([0, y0+11, W, y0+11], fill=SEAM)
    for x0 in range(-4, W, 12): d.line([x0+11, CEIL+1, x0+11, GROUND], fill=SEAM)
    # the ceiling: black, a truss, the mount GLaDOS hangs from
    d.rectangle([0, 0, W, CEIL], fill=(12,12,15))
    for x in range(0, W, 9): d.line([x, 2, x+5, 8], fill=(30,32,36)); d.line([x+5, 2, x, 8], fill=(26,28,32))
    d.line([0, 2, W, 2], fill=(40,42,46)); d.line([0, 8, W, 8], fill=(40,42,46))
    d.line([0, CEIL, W, CEIL], fill=(70,74,80))
    d.rectangle([MOUNT[0]-7, 0, MOUNT[0]+7, 3], fill=(58,60,66)); d.line([MOUNT[0]-7, 3, MOUNT[0]+7, 3], fill=(96,100,108))
    # the observation window (lit office behind dark glass)
    x0, y0, x1, y1 = 44, 15, 76, 25
    d.rectangle([x0-1, y0-1, x1+1, y1+1], fill=(80,84,90))
    d.rectangle([x0, y0, x1, y1], fill=(28,40,46))
    d.rectangle([x0+3, y0+4, x0+9, y1], fill=(46,62,66)); d.rectangle([x0+18, y0+6, x0+22, y1], fill=(42,56,60))
    d.point((x0+6, y0+3), fill=(210,200,150)); d.point((x0+20, y0+5), fill=(210,200,150))
    for i in range(3): d.line([x0+10+i*4, y1, x0+16+i*4, y0], fill=(58,78,84))
    # the CHAMBER 19 sign
    d.rectangle([12, 14, 30, 38], fill=(226,224,210)); d.rectangle([12, 14, 30, 38], outline=(150,150,140))
    for j, (dx, bits) in enumerate(((14, FONT['1']), (22, FONT['9']))):
        for k, b in enumerate(bits):
            if b == '1': d.rectangle([dx+(k%3)*2, 16+(k//3)*2, dx+(k%3)*2+1, 16+(k//3)*2+1], fill=(30,30,30))
    d.line([14, 28, 28, 28], fill=(30,30,30))
    for i in range(4): d.rectangle([14+i*4, 31, 16+i*4, 33], fill=(30,30,30) if i != 2 else (220,100,30))
    for i in range(4): d.rectangle([14+i*4, 35, 16+i*4, 36], fill=(120,120,114))
    # the logo on a panel
    _aperture(d, 90, 31, 5, (70,74,80), tuple(PANEL))
    # left and right pillars (portal surfaces), the floor strip
    d.rectangle([0, CEIL+1, LWALL-1, GROUND], fill=(196,200,206)); d.line([LWALL-1, CEIL+1, LWALL-1, GROUND], fill=(120,124,132))
    d.rectangle([RWALL+1, CEIL+1, W, GROUND], fill=(196,200,206)); d.line([RWALL+1, CEIL+1, RWALL+1, GROUND], fill=(230,232,236))
    d.rectangle([0, GROUND-2, W, GROUND], fill=(86,90,96)); d.line([0, GROUND-2, W, GROUND-2], fill=(128,132,140))
    for x in range(0, W, 12): d.line([x, GROUND-1, x, GROUND], fill=(60,62,68))
register_bg(THEME, lambda v: (v, v+2, v+6), decor=_chamber, clip_ground=True)

def _bg(): return bg_for(THEME)

# ---- GLaDOS ------------------------------------------------------------------------------------
# Local coordinates relative to her mount point (the top of the body, where the arm grabs it).
_SPINE = [(-3,0),(3,0),(4,6),(2,12),(-1,16),(-5,15),(-3,9),(-4,4)]
_PLATE = [(3,0),(8,3),(9,9),(6,14),(2,12),(4,6)]
_HEAD = [(2,14),(-4,13),(-12,14),(-20,16),(-24,19),(-24,23),(-20,26),(-10,27),(-2,25),(3,21)]
_FACE = [(-24,19),(-24,23),(-20,26),(-16,25),(-15,20),(-19,17)]
_EYE = (-20,21)

def _tf(ax, ay, tilt, sx, sc):
    ca, sa = math.cos(tilt), math.sin(tilt)
    return lambda q: (ax+(q[0]*sx*ca-q[1]*sa)*sc, ay+(q[0]*sx*sa+q[1]*ca)*sc)

@fx('portal_arm')
def _fx_arm(d, im, e, f):
    """Her mechanical arm from the ceiling mount down to (x, y)."""
    _, x, y = e; mx = MOUNT[0]
    d.line([mx, 2, mx+1, 5, x, y], fill=(70,72,78), width=3)
    d.line([mx-1, 2, mx, 5], fill=(120,124,132))
    d.ellipse([mx-2, 3, mx+2, 7], fill=(90,92,98)); d.point((mx, 5), fill=(160,164,170))

@fx('portal_glados')
def _fx_glados(d, im, e, f):
    """GLaDOS: white body + long head shell, one glowing eye. (ax, ay) = mount point, tilt (rad,
    positive swings the head to the right), sx = horizontal stretch, sc = overall scale, eye colour
    (None = off), glow 0..1."""
    _, ax, ay, tilt, sx, sc, eye, glow = e
    if sc <= 0.05: return
    P = _tf(ax, ay, tilt, sx, sc); poly = lambda pts: [P(q) for q in pts]
    # cables dangling from the body
    for k, (a, b) in enumerate((((-3,4),(-9,14)), ((-2,9),(-6,20)), ((7,8),(11,18)))):
        sw = math.sin(2*math.pi*f/58+k)*1.2                           # a 58-frame sway: the clip loops
        d.line([P(a), P(((a[0]+b[0])/2+sw, (a[1]+b[1])/2+2)), P((b[0]+sw, b[1]))], fill=(30,30,36))
    d.polygon(poly(_SPINE), fill=(58,60,68))
    for y in (3, 7, 11): d.line(poly([(-3,y),(3,y)]), fill=(96,100,108))
    d.polygon(poly(_PLATE), fill=(214,218,224)); d.line(poly([(4,1),(8,4),(9,9)]), fill=(250,250,252))
    d.polygon(poly(_HEAD), fill=(232,234,238))
    d.line(poly([(-19,26),(-10,27),(-2,25),(3,21)]), fill=(150,154,162))
    d.line(poly([(-12,15),(-4,14),(2,15)]), fill=(252,252,255))
    d.line(poly([(-8,14),(-7,20),(-8,26)]), fill=(170,174,182))
    d.polygon(poly([(-4,17),(-1,18),(-1,22),(-4,23),(-6,20)]), fill=(186,190,198))      # the round side panel
    d.point(P((-3,20)), fill=(120,124,132))
    d.polygon(poly(_FACE), fill=(34,34,40))
    ex, ey = P(_EYE); r = max(1, 1.6*sc)
    if eye:
        px = im.load()
        for dx in range(-5, 6):
            for dy in range(-4, 5):
                k = 1-math.hypot(dx, dy)/5.5
                if k > 0: blend(px, int(ex+dx), int(ey+dy), eye, 0.5*k*glow)
        d.ellipse([ex-r, ey-r, ex+r, ey+r], fill=eye)
        d.point((ex, ey), fill=(255,255,220))
    else:
        d.ellipse([ex-r, ey-r, ex+r, ey+r], fill=(60,50,40))

# ---- the portal gun, portals, shots -------------------------------------------------------------
@fx('portal_gun')
def _fx_gun(d, im, e, f):
    """The Portal Gun held at a hand pivot, pointing at angle a; glows in the last shot's colour."""
    _, x, y, a, col = e; ca, sa = math.cos(a), math.sin(a)
    P = lambda u, v: (x+ca*u-sa*v, y+sa*u+ca*v)
    d.line([P(-3,0), P(3,0)], fill=(236,238,242)); d.line([P(-2,-1), P(2,-1)], fill=(236,238,242))
    d.line([P(-2,1), P(1,1)], fill=(150,154,162)); d.point(P(-3,1), fill=(40,40,44))
    d.line([P(3,-1), P(4,-1)], fill=(40,40,44)); d.line([P(3,1), P(4,1)], fill=(40,40,44))
    d.point(P(5,-1), fill=(90,94,100)); d.point(P(5,1), fill=(90,94,100))
    px = im.load(); tx, ty = P(5,0)
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            k = 1-math.hypot(dx, dy)/2.6
            if k > 0: blend(px, int(tx+dx), int(ty+dy), col[0], 0.5*k)
    d.point(P(4,0), fill=col[0]); d.point((tx, ty), fill=col[1])

def gun_tip(g):
    _, x, y, a, _ = g; return x+math.cos(a)*6, y+math.sin(a)*6

@fx('portal_portal')
def _fx_portal(d, im, e, f):
    """A portal: glowing oval opened to k (0..1), 'h' on a floor/ceiling or 'v' on a wall."""
    _, x, y, k, col, orient = e
    if k <= 0: return
    rim, glow = col
    a, b = (7*k+0.5, 2.2*k+0.5) if orient == 'h' else (2.2*k+0.5, 8*k+0.5)
    px = im.load()
    for dx in range(int(-a-4), int(a+5)):
        for dy in range(int(-b-4), int(b+5)):
            q = math.hypot(dx/(a+3), dy/(b+3))
            if q < 1: blend(px, x+dx, y+dy, rim, 0.35*(1-q)*k)
    d.ellipse([x-a, y-b, x+a, y+b], fill=rim)
    if a > 2 and b > 2:
        d.ellipse([x-a+1, y-b+1, x+a-1, y+b-1], fill=tuple(int(c*0.35) for c in rim), outline=glow)
    for j in range(8):                                       # sparkles swirling on the rim
        ang = f*0.35*(1 if j % 2 else -1)+j*0.785
        d.point((x+math.cos(ang)*a, y+math.sin(ang)*b), fill=(255,255,255) if j % 3 == 0 else glow)
    if k < 1:
        for j in range(6):
            ang = j*1.047+f; rr = (a+b)/2+4*(1-k)
            d.point((x+math.cos(ang)*rr, y+math.sin(ang)*rr*0.8), fill=glow)

@fx('portal_shot')
def _fx_shot(d, im, e, f):
    """A portal shot in flight at t (0..1) from (x0,y0) to (x1,y1), with a fading trail."""
    _, x0, y0, x1, y1, t, col = e
    for i in range(5):
        tt = max(0, t-i*0.07); x, y = lerp(x0, x1, tt), lerp(y0, y1, tt)
        if i == 0: d.ellipse([x-1.5, y-1.5, x+1.5, y+1.5], fill=col[1]); d.point((x, y), fill=(255,255,255))
        else: d.point((x, y), fill=col[0] if i < 3 else tuple(c//2 for c in col[0]))

@fx('portal_restore')
def _fx_restore(d, im, e, f):
    """Repaint the background over a box (hides what sticks out of a ceiling portal)."""
    _, x0, y0, x1, y1 = e; im.paste(_bg().crop((x0, y0, x1, y1)), (x0, y0))

@fx('portal_splat')
def _fx_splat(d, im, e, f):
    _, x, y, age, col = e
    for k in range(8):
        a = k*0.785+0.3; r0 = 1+age*2; r1 = r0+2
        d.line([x+math.cos(a)*r0, y+math.sin(a)*r0, x+math.cos(a)*r1, y+math.sin(a)*r1], fill=col[1] if k % 2 else col[0])

# ---- turrets, bullets, neurotoxin ---------------------------------------------------------------
@fx('portal_turret')
def _fx_turret(d, im, e, f):
    """An Aperture sentry turret facing left, risen r (0..1) out of the floor; `fire` opens its gun
    wings and flashes the muzzles, `eye` lights the red eye."""
    _, x, r, fire, eye = e
    if r <= 0: return
    tmp = Image.new('RGBA', (W, H), (0,0,0,0)); t = ImageDraw.Draw(tmp)
    y = GROUND+int((1-r)*14)
    for lx in (-3, 0, 3): t.line([x, y-4, x+lx, y], fill=(30,30,34,255))          # tripod legs
    t.ellipse([x-3, y-13, x+3, y-3], fill=(18,18,22,255))
    t.ellipse([x-2, y-12, x+3, y-4], fill=(236,238,242,255))
    t.line([x-1, y-11, x-1, y-5], fill=(50,50,56,255))                              # the front slit
    if fire:
        t.rectangle([x-5, y-10, x-2, y-8], fill=(200,204,210,255)); t.rectangle([x-5, y-7, x-2, y-6], fill=(170,174,180,255))
    ey = y-9
    t.point((x-1, ey), fill=(255,40,30,255) if eye else (90,20,20,255))
    tmp = tmp.crop((0, 0, W, GROUND+1)); im.paste(tmp, (0, 0), tmp)
    if fire and f % 2 == 0 and r >= 1:
        d.point((x-6, ey-1), fill=(255,240,160)); d.point((x-7, ey-1), fill=(255,190,80)); d.point((x-6, ey+2), fill=(255,240,160))

@fx('portal_laser')
def _fx_laser(d, im, e, f):
    """The turret's red aiming beam from (x0,y0) to (x1,y1)."""
    _, x0, y0, x1, y1 = e; px = im.load(); n = int(max(abs(x1-x0), abs(y1-y0))) or 1
    for i in range(n+1):
        if (i+f) % 3: blend(px, int(lerp(x0, x1, i/n)), int(lerp(y0, y1, i/n)), (255,30,30), 0.55)
    d.point((x1, y1), fill=(255,120,110))

@fx('portal_bullet')
def _fx_bullet(d, im, e, f):
    _, x, y = e; px = im.load()
    for i in range(-1, 7): blend(px, int(x+i), int(y-1), (255,170,60), 0.3); blend(px, int(x+i), int(y+1), (255,170,60), 0.3)
    d.line([x, y, x+5, y], fill=(255,190,70)); d.line([x, y, x+1, y], fill=(255,255,220))

@fx('portal_gas')
def _fx_gas(d, im, e, f):
    """Neurotoxin: a green cloud hugging the floor, `level` 0..1; `pull` drags it towards the right
    wall portal and thins it."""
    _, level, pull, *front = e
    if level <= 0.02: return
    if front: level *= 0.35
    px = im.load()
    for x in range(W):
        top = GROUND-level*12-2.2*math.sin(x*0.16+f*0.21)-1.4*math.sin(x*0.05-f*0.12)-2*level*math.sin(x*0.4+f*0.07)*pull
        top -= pull*8*max(0, (x-120)/60)
        for y in range(int(top), GROUND+1):
            k = min(1, (y-top)/4+0.25)
            puff = 0.1*math.sin(x*0.3+y*0.5+f*0.3)
            blend(px, x, y, TOX, max(0, (0.36+puff)*level*k*(1-0.5*pull)))

# ---- personality cores -------------------------------------------------------------------------
CORES = [dict(name='wheatley', eye=(80,170,255)), dict(name='space', eye=(255,220,60)),
         dict(name='morality', eye=(190,90,255))]

@fx('portal_core')
def _fx_core(d, im, e, f):
    """A personality core: a white sphere with dark handles and one coloured eye looking at `look`
    (radians, the direction the eye points); sc shrinks it (sucked into a portal)."""
    _, x, y, eye, look, sc = e
    if sc <= 0.1: return
    r = 4*sc
    d.ellipse([x-r, y-r, x+r, y+r], fill=(214,218,224)); d.arc([x-r, y-r, x+r, y+r], 30, 150, fill=(150,154,162))
    d.line([x-r, y-1*sc, x-r+1, y+1*sc], fill=(70,72,78)); d.line([x+r-1, y-1*sc, x+r, y+1*sc], fill=(70,72,78))
    ex, ey = x+math.cos(look)*1.6*sc, y+math.sin(look)*1.3*sc
    d.ellipse([ex-2*sc, ey-2*sc, ex+2*sc, ey+2*sc], fill=(40,40,46))
    d.ellipse([ex-1, ey-1, ex+1, ey+1], fill=eye); d.point((ex, ey), fill=(255,255,255))

# ---- the ceiling crack, the moon, the vacuum ---------------------------------------------------
@fx('portal_gap')
def _fx_gap(d, im, e, f):
    """The ceiling torn open over GAP: night sky, stars and the moon (with a blue portal on it once
    `mp` > 0)."""
    _, k, mp = e
    if k <= 0: return
    c = (GAP[0]+GAP[1])/2; hw = (GAP[1]-GAP[0])/2*k
    x0, x1 = int(c-hw), int(c+hw)
    d.rectangle([x0, 0, x1, CEIL+1], fill=(8,10,28))
    rr = random.Random(12)
    for _ in range(12):
        sx, sy = rr.randint(GAP[0], GAP[1]), rr.randint(0, CEIL)
        if x0 <= sx <= x1: d.point((sx, sy), fill=(200,200,230) if rr.random() < 0.5 else (110,110,150))
    mx, my = MOON
    if x0 <= mx+4 and mx-4 <= x1:
        tmp = Image.new('RGB', (W, H)); td = ImageDraw.Draw(tmp)
        td.ellipse([mx-4, my-4, mx+4, my+4], fill=(222,222,206)); td.point((mx-1, my-1), fill=(180,180,168))
        td.point((mx+2, my+1), fill=(180,180,168))
        if mp > 0: td.ellipse([mx-1-mp, my-1, mx+1+mp, my+1], fill=BLUE[0]); td.point((mx, my), fill=BLUE[1])
        im.paste(tmp.crop((x0, 0, x1+1, CEIL+2)), (x0, 0))
    for x in range(x0, x1+1, 2):                               # jagged broken edges
        d.point((x, CEIL+1+(x*7) % 3), fill=(12,12,15)); d.point((x, CEIL+2), fill=(70,74,80) if x % 4 else (12,12,15))
    d.line([x0, 0, x0, CEIL+1], fill=(60,62,66)); d.line([x1, 0, x1, CEIL+1], fill=(60,62,66))

@fx('portal_wind')
def _fx_wind(d, im, e, f):
    """Vacuum: streaks and bits of panel rushing into the right-wall portal at (tx, ty), strength k."""
    _, tx, ty, k = e; rr = random.Random(41); px = im.load()
    for i in range(int(40*k)):
        sx, sy = rr.randint(0, W-20), rr.randint(CEIL+2, GROUND)
        ph = ((f*rr.uniform(0.04, 0.08))+rr.random()) % 1
        x, y = lerp(sx, tx, ph**1.5), lerp(sy, ty, ph**1.5)
        dx, dy = tx-sx, ty-sy; L = math.hypot(dx, dy) or 1
        ln = 3+6*ph
        if i % 4 == 0:
            d.rectangle([x, y, x+1, y+1], fill=(200,204,210) if i % 8 else (120,124,132))
        else:
            for j in range(int(ln)): blend(px, int(x-dx/L*j), int(y-dy/L*j), (255,255,255), 0.6*(1-j/ln)*k)

# ---- close-up 1: the eye -----------------------------------------------------------------------
def closeup_eye(fr, f):
    """Primer plano: GLaDOS's head fills the left of the frame, the aperture eye turns yellow ->
    red, the shutter blades tighten — YOU MONSTER."""
    im = Image.new('RGB', (W, H), (10,10,13)); d = ImageDraw.Draw(im)
    for x in range(0, W, 7): d.line([x, 0, x+30, H], fill=(18,18,22))
    for k in range(4): d.line([(120+k*14, 0), (126+k*14, 20+k*3), (118+k*14, H)], fill=(30,30,36), width=2)   # cables
    shake = ((f % 2)*2-1) if 10 <= fr < 20 else 0
    ex, ey = 50+shake, 32
    d.polygon([(-10,-10),(110,-10),(140,8),(118,22),(92,42),(70,64),(-10,64)], fill=(226,228,232))
    d.polygon([(110,-10),(140,8),(118,22),(92,42),(86,30),(104,10)], fill=(176,180,188))
    d.line([(-10,6),(60,4),(100,-4)], fill=(150,154,162), width=2); d.line([(0,58),(40,52),(70,64)], fill=(170,174,182))
    d.ellipse([ex-20, ey-18, ex+20, ey+18], fill=(40,40,46)); d.ellipse([ex-17, ey-15, ex+17, ey+15], fill=(66,66,72))
    t = ease((fr-8)/8)
    col = tuple(int(lerp(a, b, t)) for a, b in zip(YEL, RED))
    if 8 <= fr < 16 and fr % 3 == 0: col = (80,60,40)                    # the flicker as it switches
    ri = 8-3*t                                                         # the iris narrows as she gets angry
    px = im.load()
    for dx in range(-20, 21):
        for dy in range(-18, 19):
            q = math.hypot(dx, dy)
            if ri < q < 16: blend(px, ex+dx, ey+dy, col, 0.35*(1-(q-ri)/(16-ri)))
    d.ellipse([ex-ri-2, ey-ri-2, ex+ri+2, ey+ri+2], fill=tuple(c//3 for c in col))
    d.ellipse([ex-ri, ey-ri, ex+ri, ey+ri], fill=col)
    for k in range(8):                                                  # shutter blades
        a = k*math.pi/4+fr*0.04
        d.line([ex+math.cos(a)*(ri+1), ey+math.sin(a)*(ri+1), ex+math.cos(a+0.7)*15, ey+math.sin(a+0.7)*15], fill=(30,30,34))
    d.ellipse([ex-2, ey-2, ex+2, ey+2], fill=(255,255,230) if t < 0.5 else (255,200,180))
    if fr < 3: zoom_lines(d, (255,240,180))
    if fr >= 14:
        k = min(1, (fr-14)/2)
        say(im, "YOU", 14, RED if (fr//2) % 4 else (255,160,140), cx=150)
        if fr >= 17: say(im, "MONSTER.", 32, RED if (fr//2) % 4 else (255,160,140), cx=150)
    if fr >= 27: im = fade_to(im, (0,0,0), (fr-26)/4)
    return im

# ---- close-up 2: a portal on the moon ----------------------------------------------------------
def closeup_moon(fr, f):
    """Primer plano, looking up through the crack: the moon; Claude's arm and the gun from the bottom
    left, the blue shot flies up and a portal opens on the moon's surface."""
    im = Image.new('RGB', (W, H), (6,8,24)); d = ImageDraw.Draw(im)
    rr = random.Random(8)
    for _ in range(50): d.point((rr.randint(0, W), rr.randint(0, H)), fill=(200,200,235) if rr.random() < 0.3 else (90,90,130))
    zoom = 1+0.25*ease((fr-12)/10)
    mx, my, mr = 132, 20, int(15*zoom)
    d.ellipse([mx-mr-2, my-mr-2, mx+mr+2, my+mr+2], fill=(30,32,50))
    d.ellipse([mx-mr, my-mr, mx+mr, my+mr], fill=(224,224,210))
    for cx, cy, cr in ((-5,-4,4), (6,3,3), (-2,7,2), (7,-7,2)):
        d.ellipse([mx+cx*zoom-cr, my+cy*zoom-cr, mx+cx*zoom+cr, my+cy*zoom+cr], fill=(186,186,174))
    # the broken ceiling framing the view
    d.polygon([(0,0),(70,0),(62,6),(66,12),(52,18),(40,14),(20,24),(0,20)], fill=(16,16,20))
    d.polygon([(185,40),(170,46),(160,58),(150,64),(185,64)], fill=(16,16,20))
    d.line([(70,0),(62,6),(66,12),(52,18),(40,14),(20,24),(0,20)], fill=(90,94,100))
    d.polygon([(0,40),(24,36),(40,44),(56,64),(0,64)], fill=(170,174,180)); d.line([(0,40),(24,36),(40,44),(56,64)], fill=(220,222,226))
    # Claude's arm + the gun, big, aimed at the moon
    gx, gy = 36, 58; a = math.atan2(my-gy, mx-gx); ca, sa = math.cos(a), math.sin(a)
    P = lambda u, v: (gx+ca*u-sa*v, gy+sa*u+ca*v)
    d.polygon([P(-40,-6), P(-4,-6), P(-4,6), P(-40,6)], fill=(217,119,87))                 # orange sleeve
    d.polygon([P(-4,-5), P(4,-5), P(4,5), P(-4,5)], fill=(168,80,54))
    d.polygon([P(-2,-7), P(16,-6), P(20,-3), P(20,4), P(14,6), P(-2,7)], fill=(236,238,242))
    d.polygon([P(4,5), P(14,6), P(20,4), P(20,1), P(8,3)], fill=(160,164,172))
    d.polygon([P(18,-5), P(26,-4), P(26,4), P(18,5)], fill=(34,34,38))
    d.line([P(26,-4), P(31,-3)], fill=(80,84,90), width=2); d.line([P(26,4), P(31,3)], fill=(80,84,90), width=2)
    tx, ty = P(30, 0); px = im.load()
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            k = 1-math.hypot(dx, dy)/7.5
            if k > 0: blend(px, int(tx+dx), int(ty+dy), BLUE[0], 0.6*k)
    d.ellipse([tx-2, ty-2, tx+2, ty+2], fill=BLUE[1])
    # the shot and the portal on the moon
    if 3 <= fr < 11:
        t = (fr-3)/8
        for i in range(6):
            tt = max(0, t-i*0.05); x, y = lerp(tx, mx+2, tt), lerp(ty, my+3, tt)
            r = 3-i*0.4
            d.ellipse([x-r, y-r, x+r, y+r], fill=BLUE[1] if i == 0 else BLUE[0])
    if fr < 5: zoom_lines(d, BLUE[1])
    if fr >= 11:
        k = ease((fr-11)/4); a2, b2 = 7*k*zoom, 5*k*zoom
        cx, cy = mx+2, my+3
        for dx in range(-14, 15):
            for dy in range(-12, 13):
                q = math.hypot(dx/(a2+5), dy/(b2+5))
                if q < 1: blend(px, cx+dx, cy+dy, BLUE[0], 0.5*(1-q))
        d.ellipse([cx-a2, cy-b2, cx+a2, cy+b2], fill=BLUE[0])
        if b2 > 2.5: d.ellipse([cx-a2+2, cy-b2+2, cx+a2-2, cy+b2-2], fill=(10,26,60))
        for j in range(10):
            ang = f*0.4+j*0.63; d.point((cx+math.cos(ang)*(a2+1), cy+math.sin(ang)*(b2+1)), fill=(255,255,255) if j % 2 else BLUE[1])
    if 11 <= fr < 13: im = fade_to(im, (200,230,255), 0.6); d = ImageDraw.Draw(im)
    if fr >= 21: im = fade_to(im, (0,0,0), (fr-20)/4)
    return im

# ---- the ending card ----------------------------------------------------------------------------
def _cake(d, x, y, f):
    """The Black Forest cake with one candle, flame flickering."""
    d.ellipse([x-16, y+5, x+16, y+11], fill=(90,90,96))                               # the plate
    d.rectangle([x-12, y-6, x+12, y+6], fill=(70,36,24))
    d.ellipse([x-12, y+2, x+12, y+9], fill=(70,36,24))
    d.line([x-12, y, x+12, y], fill=(236,224,200)); d.line([x-12, y+1, x+12, y+1], fill=(200,180,150))
    d.ellipse([x-12, y-10, x+12, y-3], fill=(244,240,230))                           # frosting on top
    for i in range(-11, 12, 3): d.line([x+i, y-6, x+i, y-4+(i % 2)], fill=(244,240,230))
    for cx in (-8, -3, 3, 8): d.ellipse([cx+x-1, y-9, cx+x+1, y-7], fill=(200,20,40))
    d.rectangle([x-1, y-18, x, y-8], fill=(236,236,236)); d.line([x-1, y-15, x, y-16], fill=(220,60,60))
    fl = f % 4
    d.ellipse([x-2, y-24+fl % 2, x+1, y-19], fill=(255,170,40)); d.point((x, y-21), fill=(255,250,210))

def card_triumph(fr, f):
    """THIS WAS A TRIUMPH. on an amber CRT, then the cake; THE CAKE IS A LIE scrawled beside it."""
    im = Image.new('RGB', (W, H), (14,10,4)); d = ImageDraw.Draw(im)
    amber = (255,176,40)
    line = "THIS WAS A TRIUMPH."
    n = min(len(line), fr)
    x0 = W//2-_txt_mask(line).width
    x1 = say(im, line[:n], 4, amber, outline=(60,34,0), left=x0) if n else x0
    if n < len(line) or (fr//4) % 2: d.rectangle([x1+1, 4, x1+4, 13], fill=amber)          # the cursor
    if fr >= 12:
        k = ease((fr-12)/6); _cake(d, 56, int(lerp(70, 44, k)), f)
    if fr >= 20 and (fr >= 24 or fr % 2):
        small(im, "THE CAKE", 128, 30, (210,60,40), outline=None, center=True)
        small(im, "IS A LIE", 128, 38, (210,60,40), outline=None, center=True)
        d.line([108, 45, 150, 45], fill=(150,40,30))
        if fr >= 28: small(im, "THE CAKE IS A LIE", 128, 50, (130,36,26), outline=None, center=True)
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    for y in range(0, H, 2): md.line([0, y, W, y], fill=60)
    im = Image.composite(Image.new('RGB', (W, H), (0,0,0)), im, m)
    if fr < 3: im = fade_to(im, (0,0,0), 1-fr/3)
    if fr >= 32: im = fade_to(im, (0,0,0), (fr-31)/4)
    return im

# ---- the clip ----------------------------------------------------------------------------------
def shot_timing(f, t0, dur=3):
    """-> t in (0..1) while a shot fired at t0 is in flight, else None."""
    return (f-t0)/dur if t0 <= f < t0+dur else None

def opening(f, t0, dur=4): return ease((f-t0)/dur) if f >= t0 else 0.0

# turret bursts: (fire frame, turret x) for each bullet
BURST_A = [(t, TUR[i % 2]) for i, t in enumerate(range(62, 72, 2))]
BURST_B = [(t, TUR[i % 2]) for i, t in enumerate(range(88, 100, 2))]
BUL_Y = GROUND-10
BSPD = 8
LPORT_OPEN = 83        # the blue portal on the left wall
RPORT_OPEN = 87        # the orange on the right wall

def bullets(s, f):
    hits = []
    for t0, tx in BURST_A+BURST_B:
        x = tx-7-BSPD*(f-t0); y = BUL_Y+(tx == TUR[1])
        if f < t0: continue
        if x > LWALL+2:
            s['fx'].append(('portal_bullet', x, y)); continue
        t_in = t0+(tx-7-LWALL-2)/BSPD                                  # the frame it reaches the wall
        if t_in >= LPORT_OPEN:
            x2 = RWALL-2-BSPD*(f-t_in)
            if x2 > 162: s['fx'].append(('portal_bullet', x2, 30+(y-BUL_Y)))
            elif x2 > 162-BSPD: hits.append(f)
        elif f-t_in < 3: s['fx'].append(('spark', LWALL+1, y, 2))
    return hits

def clip_triumph(f):
    s = scene(f, THEME)
    # --- state defaults (the neutral pose) ---
    cx, feet, pose, flip = CX, GROUND, guard_pose(f), False
    aim = 0.08; gcol = BLUE; show_gun = True
    g_ax, g_ay = MOUNT; g_tilt = round(0.05*math.sin(2*math.pi*f/116), 6); g_sx, g_sc = 1.0, GSC   # rounded: sin(2pi*k) is not
    eye = YEL; glow = round(0.8+0.2*math.sin(2*math.pi*f/29), 6); attached = True                     # quite 0, and it shows
    turret_r = 0.0; tfire = False; teye = False; lasers = []
    gas = 0.0; pull = 0.0; gap = 0.0; moonp = 0
    portals = []          # (x, y, k, col, orient, front)
    cores = []            # (x, y, eye, look, scale)
    restore = False
    # 1) OH... IT'S YOU.
    if 4 <= f < 40:
        txt = "OH... IT'S YOU."; n = min(len(txt), (f-4)//1+1)
        s['fx'].append(('portal_say', txt[:n], 15, YEL, 82))
    # 2) turrets, neurotoxin, the portal dodge, the portal trick
    if 40 <= f < 122:
        turret_r = ease((f-40)/8) if f < 110 else 1-ease((f-110)/8)
        teye = f < 108
        tfire = 62 <= f < 72 or 88 <= f < 100
        if 46 <= f < 58: s['fx'].append(('portal_small', "I SEE YOU", 100, 34, (255,90,70)))
        if 52 <= f < 64: s['fx'].append(('portal_small', "TARGET ACQUIRED", 94, 41, (255,90,70)))
        if 74 <= f < 86: s['fx'].append(('portal_small', "THERE YOU ARE", 108, 42, (255,90,70)))
        if 104 <= f < 116: s['fx'].append(('portal_small', "TARGET LOST", 100, 38, (255,160,140)))
    if f >= 48: gas = min(1.0, (f-48)/60)
    # Claude: shoot blue under his feet, orange onto the ceiling, drop through
    if 54 <= f < 58: aim = ez(0.08, math.pi/2-0.3, (f-54)/3); pose = 'guard'
    if 58 <= f < 64: aim = ez(math.pi/2-0.3, -1.0, (f-58)/3); pose = 'guard'
    if f >= 57: gcol = BLUE
    if f >= 60: gcol = ORANGE
    g = ('portal_gun',)+tuple(hand_of(pose, cx, feet))+(aim, gcol)
    t = shot_timing(f, 56, 2)
    if t is not None: s['fx'].append(('portal_shot',)+gun_tip(g)+(cx+2, GROUND, t, BLUE))
    t = shot_timing(f, 60, 3)
    if t is not None: s['fx'].append(('portal_shot',)+gun_tip(g)+(72, CEIL+1, t, ORANGE))
    if 58 <= f < 74: portals.append((CX, GROUND, opening(f, 58) if f < 70 else 1-ease((f-70)/4), BLUE, 'h', True))
    if 63 <= f < 90: portals.append((72, CEIL+1, opening(f, 63) if f < 86 else 1-ease((f-86)/3), ORANGE, 'h', True))
    if 58 <= f < 62: s['fx'].append(('portal_splat', CX, GROUND, f-58, BLUE))
    if 63 <= f < 67: s['fx'].append(('portal_splat', 72, CEIL+1, f-63, ORANGE))
    if 64 <= f < 70:                                                # sinking into the floor portal
        pose = 'armsup'; feet = GROUND+int(((f-64)/5)**1.5*14)
    if 70 <= f < 78:                                                # out of the ceiling, feet first
        pose = 'armsup'; cx = 72; tt = (f-70)
        feet = min(GROUND, CEIL+2+tt*3+tt*tt*0.6)
        restore = True
        if feet >= GROUND: pose = 'guard'
    if f == 78: s['fx'].append(('dust', 68, GROUND-1)); s['fx'].append(('dust', 76, GROUND-1))
    if f >= 70: cx = 72
    # the trick: blue on the left wall, orange on the right wall, jump the fire
    if 78 <= f < 88:
        pose = 'guard'
        if f < 84: flip = True; aim = math.pi+0.12
        else: aim = math.atan2(30-(GROUND-7), RWALL-cx)
    if f >= 80: gcol = BLUE
    if f >= 84: gcol = ORANGE
    if 86 <= f < 104:
        tt = (f-86)/18; pose = 'armsup'; feet = GROUND-int(15*4*tt*(1-tt)); aim = -0.3
    if 104 <= f < 108: pose = 'guard'; s['fx'].append(('dust', cx-3, GROUND-1)) if f == 104 else None
    g = ('portal_gun',)+tuple(hand_of(pose, cx, feet, flip))+(aim, gcol)
    t = shot_timing(f, 80, 3)
    if t is not None: s['fx'].append(('portal_shot',)+gun_tip(g)+(LWALL+1, 48, t, BLUE))
    t = shot_timing(f, 84, 3)
    if t is not None: s['fx'].append(('portal_shot',)+gun_tip(g)+(RWALL-1, 30, t, ORANGE))
    if f >= LPORT_OPEN and f < 212: portals.append((LWALL+1, 48, opening(f, LPORT_OPEN) if f < 208 else 1-ease((f-208)/4), BLUE, 'v', False))
    if f >= RPORT_OPEN and f < 272: portals.append((RWALL-1, 30, opening(f, RPORT_OPEN) if f < 266 else 1-ease((f-266)/6), ORANGE, 'v', False))
    if 72 <= f < 104 and turret_r >= 1:                                        # aiming beams
        tx = cx; ty = int(feet)-6
        for x in TUR: lasers.append((x-2, BUL_Y+1, tx, ty))
    elif 50 <= f < 62 and turret_r >= 1:
        for x in TUR: lasers.append((x-2, BUL_Y+1, CX, GROUND-6))
    hits = bullets(s, f) if 62 <= f < 124 else []
    if hits:
        s['shake'] = rshake(1); s['flash'] = 0.15; s['fc'] = (160, 30); s['flashc'] = (255,200,120)
        s['fx'].append(('spark', 162+random.randint(-2, 2), 28+random.randint(-3, 3), 3))
    if 102 <= f < 122:
        k = (f-102)
        g_tilt = 0.18*math.sin(k*0.9)*max(0, 1-k/20)
        if f % 4 < 2: eye = (255,120,40)
        if f % 3 == 0: s['fx'].append(('spark', 150+random.randint(-6, 6), 22+random.randint(-6, 10), 2))
    # 3) close-up: the eye
    if 122 <= f < 152: s['image'] = closeup_eye(f-122, f); return s
    # 4) the cores pop off; the ceiling cracks
    if 152 <= f < 200:
        eye = RED; g_tilt = 0.07*math.sin(f*0.6)
        if f % 5 == 0: s['fx'].append(('spark', 146+random.randint(-8, 8), 14+random.randint(0, 16), 2))
        for i, (c, t0, x0, vx) in enumerate(zip(CORES, (154, 162, 170), (146, 156, 150), (-2.2, -1.2, 0.8))):
            if f < t0:                                                 # still plugged into her body
                cores.append((x0, 22+i*2, c['eye'], 0.4, 0.8)); continue
            k = f-t0; x = x0+vx*min(k, 16)+(vx*0.25*(k-16) if k > 16 else 0)
            y = 22+k*1.2+k*k*0.3
            land = GROUND-5
            if y > land:
                kb = k-math.sqrt(max(0, (land-22)/0.3)); y = land-max(0, 6*math.sin(min(math.pi, kb*0.35)))*(1 if kb < 9 else 0)
            look = k*0.6*(1 if vx > 0 else -1) if y < land else (-1.9 if c['name'] == 'wheatley' else -1.3+0.4*math.sin(f*0.8))
            cores.append((x, y, c['eye'], look, 1.0))
            if k == 0: s['fx'].append(('spark', x, y, 3))
        if 172 <= f < 186: s['fx'].append(('portal_small', "HELLO? HELLO!", 60, 32, (140,200,255)))
        if 186 <= f < 200: s['fx'].append(('portal_small', "I'M NOT A MORON!", 64, 32, (140,200,255)))
        if 178 <= f < 200 and (f//2) % 3: s['fx'].append(('portal_small', "SPAAACE!", 140+random.randint(-1, 1), 42, YEL))
        if 184 <= f < 200:
            gap = ease((f-184)/6)
            if f < 190: s['shake'] = rshake(2)
            for i in range(6):                                    # chunks of ceiling falling
                k = f-184-i*0.7
                if 0 <= k < 12:
                    x = GAP[0]+3+i*3.5; y = CEIL+k*k*0.45
                    if y < GROUND-1: s['fx'].append(('dust', x, y)); s['fx'].append(('rock', x+1, y+1))
    if 190 <= f < 272: gap = 1.0
    # 5) close-up: a portal on the moon
    if 200 <= f < 224: s['image'] = closeup_moon(f-200, f); return s
    if 211 <= f < 272: moonp = 1
    if f >= 200: gcol = BLUE                                      # the moon shot was the last one
    # the vacuum
    if 224 <= f < 272:
        eye = RED; k = min(1, (f-224)/6)
        pull = k if f < 262 else max(0, 1-(f-262)/6)
        s['fx'].append(('portal_wind', RWALL-2, 30, pull))
        if f % 2 and f < 262: s['shake'] = (random.choice([-1, 0, 1]), 0)
        pose = 'hurt' if f < 262 else 'guard'; cx = 72+min(4, (f-224)*0.3) if f < 262 else ez(76, 72, (f-262)/8)
        show_gun = pose != 'hurt'
        # cores: dragged across the floor, then flung into the portal
        for i, (c, x0, t0) in enumerate(zip(CORES, (98, 146, 155), (228, 234, 240))):
            if f < t0:
                cores.append((x0+random.randint(0, 1), GROUND-5, c['eye'], -0.5, 1.0)); continue
            tt = min(1, (f-t0)/10); x = lerp(x0, RWALL-2, tt**1.6); y = lerp(GROUND-5, 30, tt**1.2)-math.sin(tt*math.pi)*8
            if tt < 1: cores.append((x, y, c['eye'], f*0.9, 1-tt*0.8))
            if c['name'] == 'space' and t0 <= f < t0+14:
                s['fx'].append(('portal_small', "SPAAACE!", min(150, x)+random.randint(-1, 1), max(14, y-12), YEL))
        # GLaDOS: stretches and tilts towards the portal, torn off the arm, sucked through
        if f < 246:
            tt = (f-224)/22; g_tilt = -0.9*ease(tt)+0.06*math.sin(f*1.3); g_sx = 1+0.35*ease(tt)
            g_ax = MOUNT[0]+random.randint(-1, 1)
        elif f < 262:
            attached = False; tt = (f-246)/16
            g_ax = lerp(MOUNT[0], RWALL-2, ease(tt)); g_ay = lerp(MOUNT[1], 22, ease(tt))
            g_tilt = -0.9-tt*2.2; g_sx = 1.35+tt*0.6; g_sc = GSC*(1-ease(tt))
            if f == 246: s['fx'].append(('spark', MOUNT[0], MOUNT[1], 4)); s['shake'] = rshake(2)
        else: attached = False; g_sc = 0
        if 260 <= f < 264: s['flash'] = 0.25; s['fc'] = (RWALL-2, 30); s['flashc'] = ORANGE[1]
    # 6) THIS WAS A TRIUMPH.
    if 272 <= f < 308: s['image'] = card_triumph(f-272, f); return s
    # back to the neutral pose: GLaDOS lowered onto her arm, the toxin clears
    if f >= 308:
        gas = max(0, 0.45*(1-(f-308)/22))
        if f < 330:
            tt = (f-308)/22; g_ay = lerp(MOUNT[1]-44, MOUNT[1], ease(tt)); attached = f >= 328
            eye = None if f < 326 else YEL
        elif f < 334: eye = YEL if f % 2 else None
        if f == 328: s['fx'].append(('spark', MOUNT[0], MOUNT[1], 3))
        cx = ez(72, CX, (f-308)/26); pose = guard_pose(f)
        if f < 334 and (f-308) % 6 == 0: s['fx'].append(('dust', int(cx)-4, GROUND-1))
    if 224 <= f < 272: gas = max(0, 1-(f-224)/40)
    # --- composition ---
    s['under'].append(('portal_arm', g_ax if attached else MOUNT[0]+1, g_ay if attached else 9))
    if gap > 0: s['under'].append(('portal_gap', gap, moonp))
    for x in TUR: s['under'].append(('portal_turret', x, turret_r, tfire, teye))
    s['under'].append(('portal_glados', g_ax, g_ay, g_tilt, g_sx, g_sc, eye, glow))
    if gas > 0: s['under'].append(('portal_gas', gas, pull))
    for p in portals:
        if not p[5]: s['under'].append(('portal_portal',)+p[:5])
    for l in lasers: s['under'].append(('portal_laser',)+l)
    cl = actor(CHELL[pose], cx, int(feet), flip=flip, pal=CHELL_PAL)
    s['actors'] = [cl]
    pre = [('portal_gas', gas, pull, True)] if gas > 0 else []
    pre += [('portal_core',)+c for c in cores]
    if show_gun and pose in _HAND: pre.append(('portal_gun',)+tuple(hand_of(pose, cx, feet, flip))+(aim, gcol))
    if restore: pre.append(('portal_restore', 60, 0, 85, CEIL+1))
    pre += [('portal_portal',)+p[:5] for p in portals if p[5]]
    s['fx'] = pre+s['fx']
    return s

CLIPS = [clip('triumph', N_, clip_triumph)]
