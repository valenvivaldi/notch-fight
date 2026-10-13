"""Looney Tunes: Claude is Wile E. Coyote (brown-grey fur, the long snout, pointy ears, a big tail) in the
desert, next to his ACME crate. Clip `acme`: the package opens and the anvil on its rope drops on him, and
he's flattened for a moment. He lights an ACME rocket; it goes off without him and comes back for him. The
Road Runner zips past (BEEP BEEP, a dust trail) and he runs after it, overshoots the cliff, hangs in mid-air,
looks at us and holds up HELP?, then falls, a tiny puff of dust far below. Close-up: mouth open, the sign
YET AGAIN. Black, and back to the neutral pose by the crate."""
from engine import *

THEME = 'looney-coyote'
N_ = 360                                                            # 18 s, a multiple of 12: the guard bob loops
CX, CRATE_X, ANVIL_X = 50, 22, 52                                   # Wile E.; the ACME crate; the anvil over his head
CLIFF = 128                                                         # where the mesa ends: the canyon starts
INK = (16,14,22)
FUR, FUR_D, MUZZLE = (150,120,100), (96,70,56), (236,214,180)       # brown-grey fur, the pale muzzle
ORANGE, ORANGE_D = (217,119,87), (168,80,54)                        # Claude's orange: the ACME crate
DUST = (196,166,126)
SKY_TOP, SKY_BOT = (58,118,206), (170,206,240)

ACME, BEEP, HELP, AGAIN = 'ACME PACKAGE', 'BEEP BEEP', 'HELP?', 'YET AGAIN'

# ---- the timeline (frames at 20 fps) --------------------------------------------------------------------
T_LID = 20                                                          # the crate's lid pops open
T_RISE, T_HANG, T_DROP, T_HIT, T_POP = 22, 36, 48, 58, 66           # the anvil rises, hangs, drops, lands, he pops
T_ROCKET, T_LAUNCH, T_BACK, T_BOOM = 84, 98, 124, 142               # lit in his hand, off, back, boom
T_BEEP, T_RUN, T_CLIFF, T_SIGN = 164, 170, 192, 206
T_FALL = T_SIGN + hold(HELP)                                        # HELP? is up for its full hold, then he falls
T_PUFF = 236
CLOSE_AT, CLOSE_LEN = 254, 44                                       # YET AGAIN
T_BLACK, T_IN, T_NEUTRAL = 298, 304, 314                            # black, then the neutral pose fades in
HANG_X = CX + 4 * (T_CLIFF - T_RUN)                                 # where he hangs over the canyon

# ---- people -----------------------------------------------------------------------------------------------
def _snout(g, at):                                                  # the long snout, the nose, the chin
    c, hy = at['c'], at['hy']; o = at['sh'](hy)
    for x in range(c + 3, c + 7): put(g, x + o, hy + 2, 'f')
    for x in range(c + 2, c + 8): put(g, x + o, hy + 3, 'c')
    put(g, c + 7 + o, hy + 3, 'n')
    for x in range(c + 2, c + 5): put(g, x + o, hy + 4, 'c')

def _stare(g, at):                                                  # wide eyes, looking out at the viewer
    if not at['flags'].get('stare'): return
    c, hy = at['c'], at['hy']; o = at['sh'](hy)
    for ex in (0, 2):
        put(g, c + ex + o, hy + 1, 'w'); put(g, c + ex + o, hy + 2, 'K'); put(g, c + ex + o, hy + 3, 'w')

def _belly(g, at):                                                  # the cream belly down the front
    c, ty, hip, sh = at['c'], at['ty'], at['hip'], at['sh']
    for y in range(ty + 2, hip - 1):
        for x in range(c - 1 + sh(y), c + 2 + sh(y)): put(g, x, y, 'c')

def _tail(g, at):                                                   # a big bushy tail out behind, dark tip
    c, hip = at['c'], at['hip']
    seg(g, c - 3, hip - 3, c - 7, hip - 6, 'f'); seg(g, c - 3, hip - 2, c - 8, hip - 4, 'f')
    seg(g, c - 7, hip - 6, c - 10, hip - 5, 'f'); seg(g, c - 8, hip - 4, c - 10, hip - 3, 'f')
    seg(g, c - 10, hip - 5, c - 11, hip - 7, 'h')

_BODY = dict(w=24, h=24, c=11, legs=9, torso=7)
COYOTE = dict(_BODY, name='looney-coyote-wile', skin='f', hair=['.f...f.', '.fh.hf.'], hair_y=2,   # the pointy ears
              leg=dict(color='p', boot='k', toe=True),
              arm=dict(sleeve='j', fore='f', hand='f'),
              paint={'head': [_snout, _stare], 'body': [_belly], 'end': [_tail]})
CPAL = {'f': FUR, 'h': FUR_D, 'j': (120,96,80), 'p': (90,74,68), 'k': INK, 'K': INK, 'o': INK, 'c': MUZZLE,
        'n': INK, 'w': (246,246,240)}

_SQ = {}
def _squash(spr, kx, ky):                                           # a flattened copy (nearest sampling), cached
    key = (tuple(spr), kx, ky)
    if key not in _SQ:
        h, w = len(spr), len(spr[0]); nh, nw = max(1, round(h * ky)), max(1, round(w * kx))
        _SQ[key] = S([''.join(spr[min(h - 1, int(y / ky))][min(w - 1, int(x / kx))] for x in range(nw)) for y in range(nh)])
    return _SQ[key]

def _bird(legs):                                                    # the Road Runner, facing right: blue-purple, a crest, a beak
    g = blank(16, 10)
    for x, y in ((1, 5), (2, 4), (2, 5), (3, 5), (3, 6), (2, 6)): put(g, x, y, 'U')            # the tail
    for y in (4, 5, 6):
        for x in range(4, 11): put(g, x, y, 'u')
    for x in range(5, 10): put(g, x, 6, 'w')                         # the pale belly
    for y in (2, 3):
        for x in range(10, 13): put(g, x, y, 'u')
    put(g, 10, 1, 'U'); put(g, 11, 1, 'U'); put(g, 11, 0, 'U')       # the crest
    put(g, 12, 2, 'w'); put(g, 12, 3, 'u')
    for x in (13, 14, 15): put(g, x, 3, 'y')                         # the beak
    for x, y in legs: put(g, x, y, 'L')
    return to_sprite(g)
BIRD_A = _bird(((5, 7), (4, 8), (3, 9), (8, 7), (9, 8), (10, 9)))
BIRD_B = _bird(((6, 7), (6, 8), (5, 9), (9, 7), (10, 8), (11, 9)))
BIRDPAL = {'u': (96,84,210), 'U': (54,44,140), 'w': (240,240,250), 'K': INK, 'y': (250,170,40), 'L': (230,160,80)}

def _rocket():                                                      # the ACME rocket, nose to the right
    g = blank(14, 5)
    for x in range(2, 10):
        put(g, x, 1, 'w'); put(g, x, 2, 'r'); put(g, x, 3, 'w')
    for x in (10, 11, 12): put(g, x, 2, 'r')
    put(g, 1, 0, 'r'); put(g, 2, 0, 'r'); put(g, 1, 4, 'r'); put(g, 2, 4, 'r')
    return to_sprite(g)
ROCKET = _rocket()
ROCKETPAL = {'w': (240,240,246), 'r': (220,50,40), 'K': INK}

ANVIL = S([
"LLLLLLLLLLLLL",
"DDDDDDDDDDDDD",
".DDDDDDDDDDD.",
"..dDDDDDDDd..",
"...dDDDDDd...",
"...dDDDDDd...",
"..ddddddddd..",
".ddddddddddd.",
])
ANVILPAL = {'L': (206,210,220), 'D': (126,130,142), 'd': (70,72,86), 'K': INK}

# ---- the place --------------------------------------------------------------------------------------------
def _desert(d):
    for y in range(H):
        k = y / H; d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip(SKY_TOP, SKY_BOT)))
    d.ellipse([154, 4, 168, 18], fill=(255,236,170))                                  # the sun
    d.polygon([(40,40),(48,28),(78,26),(88,40)], fill=(176,84,58), outline=(120,50,36))   # the red mesas
    d.polygon([(108,42),(116,30),(150,28),(160,36),(166,42)], fill=(160,72,50), outline=(104,44,32))
    d.polygon([(0,42),(8,34),(26,34),(34,42)], fill=(190,96,64))
    d.polygon([(0,42),(CLIFF,42),(CLIFF,GROUND),(0,GROUND)], fill=(222,168,112))      # the desert floor
    for x, h in ((5, 14), (106, 10)):                                                 # two cacti
        d.rectangle([x, GROUND - h, x + 2, GROUND], fill=(74,128,70))
        d.rectangle([x - 3, GROUND - h // 2, x - 1, GROUND - h // 2 + 2], fill=(74,128,70))
    d.rectangle([0, GROUND, CLIFF - 1, H], fill=(64,60,68))                           # the road
    for x in range(0, CLIFF, 14): d.line([x, 61, x + 6, 61], fill=(236,230,200))
    d.rectangle([CLIFF, GROUND, W, H], fill=(120,56,40))                              # the canyon below the cliff
    d.line([CLIFF, GROUND, CLIFF, H], fill=(210,130,90))                              # the lip of the cliff
register_bg(THEME, lambda v: (v+30,v+24,v+44), decor=_desert)

# ---- effects ------------------------------------------------------------------------------------------------
@fx('lc_crate')
def _fx_crate(d, im, e, f):
    """The ACME crate: ('lc_crate', x, feet, lift): lift > 0 is the open crate, its lid up."""
    _, x0, bottom, lift = e
    L, R, T = int(x0) - 11, int(x0) + 11, int(bottom) - 12
    if lift > 0:
        d.rectangle([L, T - int(lift) - 2, R, T - int(lift)], fill=ORANGE_D, outline=INK)     # the lid, lifted
        d.rectangle([L + 1, T + 1, R - 1, T + 2], fill=(70,36,30))                           # the inside
    d.rectangle([L, T, R, bottom], fill=ORANGE, outline=INK)
    d.rectangle([L + 2, T + 4, R - 2, T + 9], fill=(240,236,226))                            # the ACME label
    text(d, 'ACME', L + 3, T + 5, INK, shadow=None)

@fx('lc_rope')
def _fx_rope(d, im, e, f):
    _, x, y1 = e; d.line([int(x), 0, int(x), int(y1)], fill=(200,184,150))

@fx('lc_flame')
def _fx_flame(d, im, e, f):
    """A rocket's flame: ('lc_flame', x, y, dirn), dirn +1 flying right (the flame behind it, to the left)."""
    _, x, y, dirn = e; tail = x - dirn * 6; n = 6 + (f % 3) * 2
    d.polygon([(tail, y - 2), (tail - dirn * n, y), (tail, y + 2)], fill=(255,170,40))
    d.polygon([(tail, y - 1), (tail - dirn * (n // 2), y), (tail, y + 1)], fill=(255,240,150))

@fx('lc_sign')
def _fx_sign(d, im, e, f):
    """A little sign on a stick: ('lc_sign', x0, y0, txt, hx, hy): the stick runs from (hx, hy) up to the board."""
    _, x0, y0, txt, hx, hy = e
    d.line([int(hx), int(hy), int(hx), int(y0) + 17], fill=(120,80,50))
    d.rectangle([x0, y0, x0 + 43, y0 + 17], fill=(250,248,240), outline=INK)
    text_block(im, txt, (x0 + 2, y0 + 1, x0 + 41, y0 + 16), color=INK, max_scale=2, shadow=None)

@fx('lc_dust')
def _fx_dust(d, im, e, f):
    """The Road Runner's dust trail behind it: ('lc_dust', x, feet)."""
    _, x, feet = e
    for k in range(5):
        r = 2 + (k % 2)
        cx_, cy_ = x - 8 - 5 * k, feet - 2 - (k % 2)
        d.ellipse([cx_ - r, cy_ - r, cx_ + r, cy_ + r], fill=DUST)

# ---- the close-up -------------------------------------------------------------------------------------------
def _again(im, d, t, f):                                            # his face, the mouth opening, the sign on its stick
    op = ease(min(1, t / 0.3))
    d.polygon([(20,16),(28,2),(38,14)], fill=FUR, outline=INK); d.polygon([(48,14),(60,2),(68,16)], fill=FUR, outline=INK)
    d.polygon([(24,12),(29,5),(34,11)], fill=FUR_D); d.polygon([(52,11),(59,5),(64,12)], fill=FUR_D)
    d.ellipse([14,10,76,58], fill=FUR, outline=INK)                                       # the head
    d.ellipse([34,30,92,50], fill=MUZZLE, outline=INK)                                    # the long muzzle
    d.ellipse([84,32,94,40], fill=INK)                                                    # the nose
    for ex in (26, 48):
        d.ellipse([ex, 16, ex + 14, 30], fill=(246,246,240), outline=INK); d.ellipse([ex + 5, 20, ex + 10, 27], fill=INK)
    bottom = 46 + int(12 * op)                                                            # the mouth, open wide
    d.ellipse([44, 40, 84, bottom], fill=(90,22,34), outline=INK)
    if op > 0.5: d.ellipse([58, bottom - 6, 76, bottom], fill=(226,90,100))              # the tongue
    d.line([88, 46, 100, 44], fill=(120,80,50))                                           # the stick
    d.rectangle([98, 12, 180, 44], fill=(250,248,240), outline=INK, width=2)              # the sign

# ---- the figure and the others -------------------------------------------------------------------------------
def ready(f):                                                       # the neutral pose: a guard bob every 12 frames
    return pose_cycle(f, 'guard', 'guard2')

def _coyote(f):
    """(sprite, x, feet): Wile E. through the clip."""
    pose, x, feet, flags, spr = ready(f), CX, GROUND, {}, None
    if T_HIT <= f < T_POP:
        spr = _squash(figure(COYOTE, POSES['guard']), 1.7, 0.3)                          # the pancake
    elif T_POP <= f < T_ROCKET:
        pose = 'cheer' if f < T_POP + 6 else ready(f)
        if f < T_POP + 3: feet = GROUND - 4                                              # he pops back up
    elif T_ROCKET <= f < T_BOOM:
        pose = 'point' if f < T_BACK - 2 else ready(f)                                   # he lit it, pointing
    elif T_BOOM <= f < T_BOOM + 10:
        pose = 'hurt'
    elif T_BEEP <= f < T_RUN:
        pose = 'point' if f >= T_BEEP + 4 else ready(f)                                  # he watches the bird pass
    elif T_RUN <= f < T_CLIFF:
        x, pose = CX + 4 * (f - T_RUN), pose_cycle(f, 'run1', 'run2', every=3)
    elif T_CLIFF <= f < T_FALL:
        x, feet = HANG_X, GROUND - 10 + round(loop.wave(f, 10))                          # hangs in mid-air
        pose, flags = ('reach' if f >= T_SIGN else 'jump'), {'stare': True}
    elif T_FALL <= f < T_BLACK:
        x, pose = HANG_X, 'jump'
        feet = GROUND - 10 + round(0.3 * (f - T_FALL) ** 2)                              # falls
    return (spr or figure(COYOTE, POSES[pose], **flags)), x, feet

def _rocket_at(f):
    """(x, feet, dirn) of the ACME rocket, or None: in his hand, off, and back."""
    hx, hy = figure_point(COYOTE, POSES['point'], 'hand', CX, GROUND)
    if T_ROCKET <= f < T_LAUNCH: return hx + 3, hy + 2, 0
    if T_LAUNCH <= f < T_BACK:
        t = f - T_LAUNCH; return hx + 3 + 0.6 * t * t, hy + 2, 1
    if T_BACK <= f < T_BOOM:
        return lerp(200, CX + 10, ease((f - T_BACK) / (T_BOOM - T_BACK))), hy + 2, -1
    return None

def _anvil_at(f):
    """(x, top) of the anvil, or None: rising out of the crate, hanging on its rope, falling, bouncing off."""
    if T_RISE <= f < T_HANG:
        t = ease((f - T_RISE) / (T_HANG - T_RISE))
        return lerp(CRATE_X, ANVIL_X, t), lerp(GROUND - 10, 6, t)
    if T_HANG <= f < T_DROP: return ANVIL_X + round(1.2 * loop.wave(f, 24)), 6
    if T_DROP <= f < T_HIT:
        t = f - T_DROP; return ANVIL_X, 6 + 0.25 * t * t
    if T_HIT <= f < T_POP: return ANVIL_X, 43                                            # on the pancake
    if T_POP <= f < T_POP + 18:
        t = f - T_POP; return ANVIL_X - 5 * t, 43 - 6 * t + 0.3 * t * t                  # bounces off, away
    return None

# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 --------------------------------
def clip_acme(f):
    s = scene(f, THEME)
    if T_BLACK <= f < T_IN:
        s['image'] = Image.new('RGB', (W, H), (0, 0, 0)); return s
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=SKY_TOP, draw=_again, txt=AGAIN,
                             box=(100, 16, 178, 40), text_from=0.0)
        return s
    open_lid = T_LID <= f < T_BLACK
    s['under'].append(('lc_crate', CRATE_X, GROUND, 8 * ease(min(1, (f - T_LID) / 6)) if open_lid else 0))
    if cue(f, 2, ACME): s['fx'].append(('caption', ACME, {'box': (2, 1, W - 2, 19)}))
    if cue(f, T_BEEP, BEEP): s['fx'].append(('caption', BEEP, {'box': (2, 1, W - 2, 19)}))

    cspr, cx, cfeet = _coyote(f)
    s['actors'].append(actor(cspr, cx, cfeet, pal=CPAL))
    if T_HIT <= f < T_HIT + 3: s['shake'] = (1, 0) if f % 2 else (-1, 0)

    rk = _rocket_at(f)
    if rk is not None:
        rx, ry, dirn = rk
        s['actors'].append(actor(ROCKET, rx, ry, flip=(dirn < 0), pal=ROCKETPAL))
        if dirn: s['fx'].append(('lc_flame', rx, ry, dirn))
        if dirn > 0:
            for k in range(3): s['fx'].append(('smoke', rx - dirn * (10 + 5 * k), ry, 3 - k // 2, (150,146,150)))
        if dirn == 0: s['fx'].append(('spark', rx - 7, ry, 2 + f % 2))

    if T_BEEP <= f < T_BEEP + 20:
        bird_x = -16 + 12 * (f - T_BEEP)
        s['actors'].append(actor(BIRD_A if (f // 2) % 2 == 0 else BIRD_B, bird_x, GROUND, pal=BIRDPAL))
        if bird_x > -8: s['fx'].append(('lc_dust', bird_x, GROUND))

    an = _anvil_at(f)
    if an is not None:
        ax, atop = an
        if T_RISE <= f < T_DROP: s['fx'].append(('lc_rope', ax, atop))
        s['actors'].append(actor(ANVIL, ax, atop + 8, pal=ANVILPAL))

    if T_HIT <= f < T_HIT + 3: s['fx'].append(('spark', CX, GROUND - 14, 4))
    if T_HIT <= f < T_HIT + 6:
        for dx in (-9, 9): s['fx'].append(('smoke', CX + dx, GROUND - 1, 3, DUST))
    if T_BOOM <= f < T_BOOM + 10: s['fx'].append(('boom', CX + 6, GROUND - 14, 3 + (f - T_BOOM) * 2))
    if T_BOOM <= f < T_BOOM + 22:
        s['fx'].append(('smoke', CX + 8, GROUND - 16 - (f - T_BOOM) // 3, max(1, 7 - (f - T_BOOM) // 3), (120,116,118)))
    if T_SIGN <= f < T_FALL and cue(f, T_SIGN, HELP):
        s['fx'].append(('lc_sign', cx - 20, 4, HELP, cx - 4, cfeet - 14))
    if T_PUFF <= f < T_PUFF + 16:                                       # a tiny puff of dust, far below
        s['fx'].append(('smoke', HANG_X, H - 2, 1 + (f - T_PUFF) // 5, DUST))
    if T_IN <= f < T_NEUTRAL: s['fx'].append(('dim', 1 - (f - T_IN) / (T_NEUTRAL - T_IN)))
    return s

CLIPS = [clip('acme', N_, clip_acme)]
