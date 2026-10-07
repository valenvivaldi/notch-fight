"""Shared pieces for themes that build their people from a pose (haikyuu, fightclub, arcane, basterds,
arg-cordoba, hp): a character grid painted cell by cell, limbs as lines of cells, the lean of a body, the
far-away copy of a sprite, and the speech bubble they all talk in.

A pose-built figure is a list of rows of palette chars ('.' = clear): start from blank(w,h), paint it
with put/seg, finish with to_sprite(). Each theme keeps its own anatomy (legs, clothes, hair) on top."""
from .core import *
from .text import text
from .fx import fx

def blank(w,h):
    """An empty character grid, w x h."""
    return [['.']*w for _ in range(h)]

def to_sprite(g):
    """The grid as a sprite."""
    return S([''.join(r) for r in g])

def put(g,x,y,c):
    """One cell, if it falls inside the grid."""
    if 0<=y<len(g) and 0<=x<len(g[0]): g[y][x]=c

def seg(g,x0,y0,x1,y1,c,first=None):
    """A straight run of cells from (x0,y0) to (x1,y1), both ends included (an arm, a leg, a bat);
    first: a different char for the starting cell (a sleeve at the shoulder)."""
    n=max(abs(x1-x0),abs(y1-y0),1)
    for i in range(n+1): put(g,round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),first if (first and i==0) else c)

def leaner(lean,top,bottom):
    """How far each row shifts for a body leaning `lean` cells at the top row, nothing at the bottom one."""
    return lambda y: round(lean*(bottom-y)/(bottom-top))

_small={}
def shrink(spr,k=0.8):
    """A smaller copy of a sprite (nearest sampling), for the far side of a 2.5D scene; cached."""
    key=(tuple(spr),k)
    if key not in _small:
        h,w=len(spr),len(spr[0]); nh,nw=max(1,round(h*k)),max(1,round(w*k))
        _small[key]=S([''.join(spr[min(h-1,int(y/k))][min(w-1,int(x/k))] for x in range(nw)) for y in range(nh)])
    return _small[key]

def cell_xy(x,feet,w,h,cx,cy,flip=False):
    """Screen position of grid cell (cx,cy) of a w x h sprite drawn centred on x with its feet at feet."""
    return (x-w//2+(w-1-cx) if flip else x-w//2+cx), feet-h+cy

def speech_bubble(d,lines,cx,y,tail=None,fill=(250,250,250),ink=(30,30,30)):
    """A speech bubble: one line or a list of them, centred on cx (kept on screen), its top at y, the
    tail pointing down to x=tail (the speaker; default cx)."""
    lines=[lines] if isinstance(lines,str) else lines
    tail=cx if tail is None else tail
    w=max(len(l) for l in lines)*4+7; h=len(lines)*7+4; x=max(1,min(W-w-2,int(cx-w/2)))
    d.rectangle([x,y,x+w,y+h],fill=fill,outline=ink)
    tx=max(x+4,min(x+w-4,int(tail))); d.polygon([(tx-2,y+h),(tx+2,y+h),(int(tail),y+h+5)],fill=fill,outline=ink)
    d.line([tx-1,y+h,tx+1,y+h],fill=fill)
    for i,l in enumerate(lines): text(d,l,x+4,y+3+i*7,ink,shadow=None)

@fx('bubble')
def _fx_bubble(d,im,e,f):
    """('bubble', text or [lines], cx, y[, tail_x[, fill[, ink]]])."""
    speech_bubble(d,*e[1:])

# ---- figure(): a person from a body spec and a pose -------------------------------------------------------
# A body spec (a dict) says what someone is like; a pose says what they're doing. figure(spec, pose) paints
# them into a grid, facing right (draw them flipped to face left), feet on the bottom row:
#
#   spec  name (for the cache)   w, h, c: the grid and its centre column (26, 26, 12)
#         legs, torso, head: rows (9, 7, 5)          torso_cols: (from, to) round c (-3, 3)
#         hair: rows of chars over the head, at hair_x (-3) from c, hair_y (2) rows above its top
#         eyes: columns from c (0, 2); eye 'K'; shut 'o' (closed eyes); skin 's'
#         leg: color 'p', back (the far leg; same), boot 'k', boot_rows 1, pad (a knee pad char), stripe
#              (the near leg's every other row), toe True (the boot's tip), bend True (the knee in a lunge),
#              gap -1 (the far leg's column from c), stand ((-1, 1): how far apart the feet are when standing)
#         shorts: a char for two rows of shorts between the torso and the legs (drawn before the far arm)
#         body: color 'j', top (the whole top row), collar (its middle), belt (the row above the hip), hip
#         arm: sleeve 'j', back_sleeve (same), fore (the forearm; skin), back_fore (same), hand 's' (hand_w 1 wide;
#              back_hand: the far one's, same), mark (a char halfway up each upper arm: a tattoo),
#              fist 1 (1 a cell, 2 a 2x2 fist 'f', 5 a big gauntlet 'g' with core 'c'), shoulders ((-2,1), (2,1))
#         paint: {'legs', 'body', 'head', 'face', 'end': [callables (g, at)]} add the rest, after the legs,
#                the torso, the eyes, the hair and the near arm
#                (a tie, a number, stripes, a skirt, glasses, a scar...); at holds c, hip, ty (shoulder row),
#                hy (head top), sh (the lean at a row), L, T, pose, legs (its kind) and the flags
#   pose  (back elbow, back hand, front elbow, front hand, lean, legs), from (c, shoulder row): an elbow
#         None draws that arm straight; a row given as 'T' or 'T+1' means the torso's length (+1).
#         legs: stand, stance, lunge, reel, knock, bent, run1, run2, jump, kneel, crouch
#   flags (keyword arguments) reach the painters as at['flags'] (shut eyes, blood...).

def _row(v, T):
    return T + int(v[1:] or 0) if isinstance(v, str) else v

def _leg_offsets(kind, t, L, bend=True, stand=(-1, 1)):
    """Columns (from the leg's own column) of the far and the near leg, t rows below the hip."""
    fr = t / max(1, L - 1)
    if kind == 'bent':
        b = 1 if 0 < t < L - 1 else 0; return -b, b
    if kind == 'run1': return -round(3 * fr), round(3 * fr)
    if kind == 'run2': return -round(fr), round(2 * fr)
    if kind == 'jump': return -round(3 * fr), -round(3 * fr)
    spread = {'stand': stand, 'stance': (-3, 3), 'lunge': (-5, 5), 'reel': (-4, 2), 'knock': (0, 0)}.get(kind, stand)
    knee = 1 if bend and kind == 'lunge' and 3 < t < 7 else 0
    return round(spread[0] * fr), round(spread[1] * fr) + knee

def _legs(g, spec, kind, c, hip, h):
    lg = {'color': 'p', 'back': None, 'boot': 'k', 'boot_rows': 1, 'pad': None, 'stripe': None, 'toe': True, 'bend': True,
          'gap': -1, 'stand': (-1, 1), **spec.get('leg', {})}
    if kind in ('kneel', 'crouch'):                                   # down on a knee, or squatting
        for k, (kx, fx_) in enumerate((((-1, -6) if kind == 'kneel' else (2, -2)), (4, 4))):
            col = lg['back'] or lg['color'] if k == 0 else lg['color']
            ky = h - 1 if (kind == 'kneel' and k == 0) else hip + 2
            seg(g, c - 1 + k * 2, hip, c + kx, ky, col)
            if kind == 'crouch': seg(g, c + kx + 1, hip, c + kx + 1, ky, col)
            if kind == 'kneel' and k == 0: seg(g, c + kx, h - 1, c + fx_, h - 1, col); put(g, c + fx_ - 1, h - 1, lg['boot'])
            else:
                seg(g, c + kx, ky, c + fx_, h - 2, col); seg(g, c + kx + 1, ky, c + fx_ + 1, h - 2, col)
                for x in range(c + fx_, c + fx_ + 3): put(g, x, h - 1, lg['boot'])
        return
    L = h - hip
    for t in range(L):
        for k, off in enumerate(_leg_offsets(kind, t, L, lg['bend'], lg['stand'])):
            x = c + (lg['gap'] if k == 0 else 1) + off
            col = (lg['back'] or lg['color']) if k == 0 else (lg['stripe'] if lg['stripe'] and t % 2 else lg['color'])
            if t >= L - lg['boot_rows']: col = lg['boot']
            elif lg['pad'] and t == L // 2: col = lg['pad']
            put(g, x, hip + t, col); put(g, x + 1, hip + t, col)
            if t == L - 1 and lg['toe']: put(g, x + (-1 if kind == 'jump' else 2), hip + t, lg['boot'])

_figures = {}
def figure(spec, pose, **flags):
    """A person: spec (who) in pose (doing what), as a sprite facing right. Cached."""
    key = (spec['name'], pose, tuple(sorted(flags.items())))
    if key in _figures: return _figures[key]
    w, h, c = spec.get('w', 26), spec.get('h', 26), spec.get('c', 12)
    L, T, HD = spec.get('legs', 9), spec.get('torso', 7), spec.get('head', 5)
    be, bh, fe, fh, lean, kind = pose
    g = blank(w, h)
    down = kind in ('kneel', 'crouch')
    hip = h - 6 if down else h - L + (1 if kind == 'bent' else 0)
    ty = hip - 2 - T if spec.get('shorts') else hip - T; hy = ty - HD
    sh = leaner(lean, hy, hip)
    at = dict(c=c, hip=hip, ty=ty, hy=hy, sh=sh, L=L, T=T, pose=pose, legs=kind, flags=flags, w=w, h=h)
    _legs(g, spec, kind, c, hip, h)
    c0, c1 = spec.get('torso_cols', (-3, 3))
    if spec.get('shorts'):
        for y in (hip - 2, hip - 1):
            for x in range(c + c0 + sh(y), c + c1 + sh(y)): put(g, x, y, spec['shorts'])
    for p in spec.get('paint', {}).get('legs', ()): p(g, at)
    arm = {'sleeve': 'j', 'back_sleeve': None, 'fore': None, 'back_fore': None, 'hand': 's', 'back_hand': None,
           'hand_w': 1, 'fist': 1, 'mark': None,
           'shoulders': ((-2, 1), (2, 1)), **spec.get('arm', {})}
    skin = spec.get('skin', 's')
    def limb(e, hnd, front):
        (sx, sy) = arm['shoulders'][1 if front else 0]
        sx, sy = c + sx + sh(ty + sy), ty + sy
        hx, hy_ = c + hnd[0] + sh(ty), ty + _row(hnd[1], T)
        sleeve = arm['sleeve'] if front else (arm['back_sleeve'] or arm['sleeve'])
        fore = (arm['fore'] if front else (arm['back_fore'] or arm['fore'])) or skin
        if e is None: seg(g, sx, sy, hx, hy_, fore, sleeve)            # straight: the sleeve at the shoulder only
        else:
            ex, ey = c + e[0] + sh(ty), ty + _row(e[1], T)
            seg(g, sx, sy, ex, ey, sleeve); seg(g, ex, ey, hx, hy_, fore)
        if arm['fist'] == 2:
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)): put(g, hx + dx, hy_ + dy, 'f')
        elif arm['fist'] == 5:
            for dx in range(-2, 3):
                for dy in range(-2, 3): put(g, hx + dx, hy_ + dy, 'g')
            put(g, hx, hy_, 'c'); put(g, hx + 1, hy_, 'c'); put(g, hx - 1, hy_ - 1, 'G')
        else:
            hand = arm['hand'] if front else (arm['back_hand'] or arm['hand'])
            for dx in range(arm['hand_w']): put(g, hx + dx, hy_, hand)
        if arm['mark'] and e is not None: put(g, (sx + ex) // 2, (sy + ey) // 2, arm['mark'])
    limb(be, bh, False)                                                 # the far arm, behind the body
    bd = {'color': 'j', 'top': None, 'collar': None, 'belt': None, 'hip': None, **spec.get('body', {})}
    for y in range(ty, ty + T if spec.get('shorts') else hip + 1):
        o = sh(y)
        for x in range(c + c0 + o, c + c1 + o):
            col = bd['color']
            if y == hip and bd['hip']: col = bd['hip']
            elif y == hip - 1 and bd['belt']: col = bd['belt']
            elif y == ty and bd['top']: col = bd['top']
            put(g, x, y, col)
    if bd['collar']:
        for x in (c - 1, c, c + 1): put(g, x + sh(ty), ty, bd['collar'])
    for p in spec.get('paint', {}).get('body', ()): p(g, at)
    o = sh(hy)
    for y in range(hy, hy + HD):
        for x in range(c - 2 + o, c + 3 + o): put(g, x, y, skin)
    eye = spec.get('shut', 'o') if flags.get('shut') else spec.get('eye', 'K')
    for ex in spec.get('eyes', (0, 2)): put(g, c + ex + o, hy + 2, eye)
    for p in spec.get('paint', {}).get('head', ()): p(g, at)
    hx0, hy0 = spec.get('hair_x', -3), spec.get('hair_y', 2)
    for i, row in enumerate(spec.get('hair', ())):
        for j, ch in enumerate(row):
            if ch != '.': put(g, c + hx0 + o + j, hy - hy0 + i, ch)
    for p in spec.get('paint', {}).get('face', ()): p(g, at)
    limb(fe, fh, True)                                                  # the near arm, in front
    for p in spec.get('paint', {}).get('end', ()): p(g, at)
    _figures[key] = to_sprite(g); return _figures[key]

def figure_point(spec, pose, part, x, feet, flip=False):
    """Where part ('hand', 'back_hand', 'head', 'shoulder') of figure(spec, pose) is on screen, drawn
    centred on x with its feet at feet (flipped: facing left)."""
    w, h, c = spec.get('w', 26), spec.get('h', 26), spec.get('c', 12)
    L, T, HD = spec.get('legs', 9), spec.get('torso', 7), spec.get('head', 5)
    be, bh, fe, fh, lean, kind = pose
    hip = h - 6 if kind in ('kneel', 'crouch') else h - L + (1 if kind == 'bent' else 0)
    ty = hip - 2 - T if spec.get('shorts') else hip - T; hy = ty - HD; sh = leaner(lean, hy, hip)
    cx, cy = {'hand': (c + fh[0] + sh(ty), ty + _row(fh[1], T)), 'back_hand': (c + bh[0] + sh(ty), ty + _row(bh[1], T)),
              'head': (c - 2 + sh(hy), hy), 'shoulder': (c + 2 + sh(ty), ty + 1)}[part]
    return cell_xy(x, feet, w, h, cx, cy, flip)

# Poses most fighters share; a theme adds its own (same shape) for what only it does.
POSES = {
 'stand':  ((-1, 4), (-1, 7), (3, 4), (4, 6), 0, 'stand'),
 'guard':  ((1, 4), (4, -2), (3, 4), (6, -3), 0, 'stance'),
 'guard2': ((1, 4), (4, -1), (3, 4), (6, -2), 0, 'stance'),
 'jab':    ((1, 4), (4, -2), (6, 0), (11, -2), 1, 'lunge'),
 'hook':   ((4, -1), (10, -3), (3, 4), (5, -1), 2, 'lunge'),
 'hurt':   ((-3, 3), (-6, 1), (1, 5), (4, 6), -2, 'reel'),
 'cheer':  ((-3, -2), (-4, -7), (4, -2), (5, -7), 0, 'stand'),
 'point':  ((-1, 4), (-1, 7), (5, 1), (9, 0), 0, 'stance'),
 'reach':  ((-1, 4), (-1, 7), (5, 1), (9, 1), 0, 'stand'),
 'walk1':  ((-1, 4), (-2, 7), (3, 4), (4, 7), 0, 'stance'),
 'walk2':  ((-1, 4), (0, 7), (3, 4), (2, 7), 0, 'stand'),
 'run1':   ((-3, 2), (-5, 4), (3, 3), (6, 2), 1, 'run1'),
 'run2':   ((-1, 3), (1, 5), (3, 3), (2, 5), 1, 'run2'),
 'jump':   ((-3, -2), (-4, -7), (4, -2), (5, -7), 0, 'jump'),
 'kneel':  ((-1, 4), (1, 7), (3, 4), (5, 6), 0, 'kneel'),
 'crouch': ((-1, 4), (2, 6), (4, 2), (8, 1), 1, 'crouch'),
}

def pose_cycle(f, a, b, every=6):
    """Alternate between two poses every `every` frames (a walk, a bob)."""
    return a if (f // every) % 2 == 0 else b
