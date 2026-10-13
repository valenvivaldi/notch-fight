"""Scarface (1983): Claude as Tony Montana (the white suit, the dark shirt, the orange tie) in his mansion
foyer, by the desk with the white heap, the globe statue THE WORLD IS YOURS behind him and the staircase
rail at his side. Clip `littlefriend`: Sosa's hitmen in dark suits and shades break through the doors.
Tony grabs the M16 with the grenade launcher: SAY HELLO TO MY LITTLE FRIEND! Close-up: his wide eyes on the
line. One grenade blows the doors, then the full-auto spray: muzzle flashes, shell casings, the hitmen down.
The smoke comes down, Tony stands, the globe glints under THE WORLD IS YOURS, and the smoke rolls off back
to the empty foyer: the neutral pose."""
import math, random, zlib
from PIL import ImageFilter
from engine import *
from engine import loop

THEME = 'scarface'
N_ = 288                                                            # a multiple of 12 (the guard bob) and of 48 (the lamp)
CX = 92                                                             # Tony
LINE = "SAY HELLO TO MY LITTLE FRIEND!"
LINE2 = "THE WORLD IS YOURS"
CLOSE = LINE
CLOSE_AT, CLOSE_LEN = 68, 40                                        # the close-up on the line (ends at 108)
GLINT_AT, CAP2_AT = 196, 196                                        # the globe glints, THE WORLD IS YOURS
HITMEN = [(178, 116, 30), (162, 126, 33), (146, 134, 36), (130, 144, 39)]   # (x, death frame, frame it starts in)
INK = (16,14,22)
GOLD = (206,166,84)
WALL, WALL2, FLOOR = (84,56,70), (58,38,54), (118,92,96)
SKY, SKY2 = (60,40,56), (120,86,96)                                 # the close-up's background
ACCENT = (217,119,87)                                               # Claude's orange: the tie

# ---- people, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
GW, GH, C = 24, 24, 11
POSES = dict(POSES)
POSES.update({
 'hold':   ((1,4),(4,-2),(5,1),(10,0),0,'stance'),                 # the rifle at the hip
 'recoil': ((1,4),(4,-3),(5,1),(10,-1),-1,'stance'),               # the kick of the burst
 'reach':  ((1,4),(3,2),(5,3),(9,3),1,'lunge'),                    # for the rifle on the desk
 'lower':  ((-1,4),(0,7),(3,4),(6,6),0,'stand'),                   # the rifle down, after
})

def _jacket(g, at):                                                 # the open V: dark shirt, lapels, orange tie, shaded back
    c, ty = at['c'], at['ty']
    for y in range(ty, at['hip'] + 1): put(g, c - 3 + at['sh'](y), y, 'J')          # the back side, one shaded column
    for y in range(ty, ty + 5):                                                    # the lapels, a shaded edge each side of the V
        put(g, c - 2 + at['sh'](y), y, 'J'); put(g, c + 2 + at['sh'](y), y, 'J')
    for y in range(ty, ty + 4):                                                    # the dark shirt in a V under the collar
        for x in ((-1, 0, 1) if y < ty + 2 else (-1, 1)): put(g, c + x + at['sh'](y), y, 'b')
    for y in range(ty + 2, ty + 6): put(g, c + at['sh'](y), y, 'o')                # the tie, down the middle

def _slick(g, at):                                                 # slicked-back black hair hugging the skull
    c, hy = at['c'], at['hy']; o = at['sh'](hy)
    for x in range(c - 2, c + 3): put(g, x + o, hy, 'h')                           # the top of the skull
    put(g, c - 3 + o, hy, 'h'); put(g, c - 3 + o, hy + 1, 'h'); put(g, c - 2 + o, hy + 1, 'h')   # a bit of volume at the back
    put(g, c - 2 + o, hy + 3, 'h')                                                 # a short sideburn by the ear

def _shades(g, at):                                                 # sunglasses
    o = at['sh'](at['hy'])
    for x in range(-2, 3): put(g, at['c'] + x + o, at['hy'] + 2, 'G')

def _shirt(g, at):                                                 # a hitman's white shirt, a dark tie
    c, ty = at['c'], at['ty']
    for y in (ty, ty + 1):
        for x in (-1, 0, 1): put(g, c + x + at['sh'](y), y, 'w')
    for y in range(ty + 2, ty + 5): put(g, c + at['sh'](y), y, 'r')

def _moustache(g, at):                                             # a thin moustache over the mouth
    o = at['sh'](at['hy']); c, hy = at['c'], at['hy']
    for x in (c, c + 1, c + 2): put(g, x + o, hy + 3, 'h')

def _shine(g, at):                                                 # a bald head's shine
    o = at['sh'](at['hy']); put(g, at['c'] - 1 + o, at['hy'] + 1, 'w')

TONY = dict(name='scarface-tony', w=GW, h=GH, c=C, legs=9, torso=7, hair=[], hair_y=1,
            leg=dict(color='j', back='J', boot='k', boot_rows=2), body=dict(color='j', hip='J'),
            arm=dict(sleeve='j', back_sleeve='J', fore='j', back_fore='J', hand='s', hand_w=1),
            paint={'body': [_jacket], 'head': [_slick]})
HIT_A = dict(name='scarface-hitman-a', w=GW, h=GH, c=C, legs=9, torso=7, hair=['hhhhh'], hair_y=1,       # dark suit, moustache
             leg=dict(color='D', boot='k', boot_rows=2), body=dict(color='d'),
             arm=dict(sleeve='d', back_sleeve='D', fore='d', back_fore='D', hand='s', hand_w=1),
             paint={'body': [_shirt], 'head': [_shades, _moustache]})
HIT_B = dict(name='scarface-hitman-b', w=GW, h=GH, c=C, legs=9, torso=7, hair=['hhhhh'], hair_y=1,       # lighter grey suit
             leg=dict(color='A', boot='k', boot_rows=2), body=dict(color='a'),
             arm=dict(sleeve='a', back_sleeve='A', fore='a', back_fore='A', hand='s', hand_w=1),
             paint={'body': [_shirt], 'head': [_shades]})
HIT_C = dict(name='scarface-hitman-c', w=GW, h=GH, c=C, legs=9, torso=7, hair=[], hair_y=1,        # bald, shades
             leg=dict(color='D', boot='k', boot_rows=2), body=dict(color='d'),
             arm=dict(sleeve='d', back_sleeve='D', fore='d', back_fore='D', hand='s', hand_w=1),
             paint={'body': [_shirt], 'head': [_shades, _shine]})
HIT_D = dict(name='scarface-hitman-d', w=GW, h=GH, c=C, legs=9, torso=7, hair=['hhhhh'], hair_y=1,       # dark suit, shades
             leg=dict(color='D', boot='k', boot_rows=2), body=dict(color='d'),
             arm=dict(sleeve='d', back_sleeve='D', fore='d', back_fore='D', hand='s', hand_w=1),
             paint={'body': [_shirt], 'head': [_shades]})
HITS = [HIT_A, HIT_B, HIT_C, HIT_D]                                  # one per hitman, in HITMEN's order
TPAL = {'s':(226,184,150),'K':INK,'h':(34,26,24),'j':(240,236,226),'J':(204,200,190),'b':(30,28,34),'o':ACCENT,'k':INK}
HPAL = {'s':(214,170,134),'K':INK,'h':(18,14,12),'d':(44,44,58),'D':(30,30,40),'a':(150,150,164),'A':(104,104,120),
        'w':(236,236,244),'r':(120,18,30),'G':(8,8,12),'k':INK}
RIFLE = S([                                                          # the M16 with the M203 under the barrel; the grip at (5, 2)
 "...ggggg......",                                                   # the carry handle
 "wwwkkkkkkkkkkk",                                                   # the receiver and the barrel
 "wwwwkkkkkkkkkk",                                                   # the stock, the body
 "..wwmmkkLLLLLL",                                                   # the magazine, the grenade launcher's tube
 "....mm........"])                                                  # the magazine's end
RPAL = {'w':(84,62,40),'k':(26,26,30),'g':(74,74,84),'m':(40,40,46),'L':(126,126,134)}
RIFLE_GRIP = (5, 2)                                                  # the grip cell, where the front hand is
MUZZLE_DX = 9                                                        # the muzzle, past the barrel's end

def ready(f):                                                       # the neutral pose: it moves every 12 frames, which divides N_
    return pose_cycle(f, 'guard', 'guard2')

def tony_pose(f):
    if f < 56: return ready(f)
    if f < 66: return 'reach'
    if f < 150: return pose_cycle(f, 'hold', 'recoil', 2) if 118 <= f < 146 else 'hold'
    if f < 256: return 'lower'
    return ready(f)

def hand_of(pose, flip=False, x=CX):
    p = figure_point(TONY, POSES[pose], 'hand', x, GROUND, flip)
    return int(p[0]), int(p[1])

def door_open(f):
    """0 shut, 1 blown open: it bursts at 30, and shuts again after the fight (hidden under the smoke)."""
    if f < 30: return 0.0
    if f < 38: return ease((f - 30) / 8)
    if f < 236: return 1.0
    if f < 246: return 1 - ease((f - 236) / 10)
    return 0.0

def veil_alpha(f):
    """The smoke that rolls over the whole foyer and back off it: the clip's end is its start, clean."""
    if 246 <= f < 256: return (f - 246) / 10
    if 256 <= f < 264: return 1.0
    if 264 <= f < 276: return 1 - (f - 264) / 12
    return 0.0

# ---- the foyer --------------------------------------------------------------------------------------------
def _globe(d):                                                      # THE WORLD IS YOURS, on its plinth
    d.rectangle([17, 44, 27, GROUND], fill=(150,116,72))
    d.rectangle([14, 41, 30, 44], fill=GOLD)
    d.ellipse([12, 25, 32, 45], fill=(40,110,160), outline=(20,60,96))
    d.ellipse([16, 29, 22, 34], fill=(110,170,110)); d.ellipse([22, 36, 28, 41], fill=(110,170,110))
    d.line([12, 35, 32, 35], fill=(30,80,120))

def _set(d):
    for y in range(GROUND + 2):
        k = y / GROUND; d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip(WALL, WALL2)))
    d.rectangle([0, 50, W, 52], fill=GOLD)                          # the wainscot rail
    for i in range(7):                                              # the grand staircase, rising to the right
        x0, top = i * 7, 46 - 3 * i
        d.rectangle([x0, top, x0 + 7, GROUND], fill=(132,92,92), outline=(90,60,64))
        d.line([x0, top, x0, top - 8], fill=GOLD)
    d.line([0, 37, 49, 14], fill=GOLD)                              # the rail
    _globe(d)
    d.rectangle([54, 44, 78, 46], fill=(146,100,66))                # the desk
    d.rectangle([56, 46, 76, GROUND], fill=(96,60,44))
    d.polygon([(60, 44), (66, 37), (72, 44)], fill=(246,246,240))   # the white heap
    d.point((64, 42), fill=(255,255,255)); d.point((69, 40), fill=(255,255,255))
    d.rectangle([0, GROUND + 2, W, H], fill=FLOOR)
    for x in range(0, W, 24): d.line([x, GROUND + 2, x - 10, H], fill=(96,74,80))
register_bg(THEME, lambda v: (v+30,v+24,v+44), decor=_set)

@fx('sc_lamp')
def _fx_lamp(d, im, e, f):
    """The chandelier over the foyer, swaying on a cycle that fits the clip."""
    x = CX + round(2 * loop.wave(f, 48))
    d.line([CX, 0, x, 8], fill=(90,80,70))
    d.ellipse([x - 7, 7, x + 7, 12], outline=GOLD, fill=(120,90,50))
    for k in (-5, 0, 5): d.point((x + k, 13), fill=(255,240,190))

@fx('sc_door')
def _fx_door(d, im, e, f):
    """The double doors at the right: shut, or the panels thrown back (e[1] 0..1)."""
    o = e[1]; x0, x1 = 163, 184
    if o <= 0:
        d.rectangle([x0, 10, x1, GROUND], fill=(92,46,36), outline=GOLD)
        d.line([173, 10, 173, GROUND], fill=GOLD); d.point((169, 34), fill=GOLD); d.point((177, 34), fill=GOLD)
        return
    d.rectangle([x0, 10, x1, GROUND], fill=(22,14,20), outline=GOLD)
    ofs = int(30 * o)
    d.rectangle([x0 - ofs, 10, x0 + 9 - ofs, GROUND], fill=(92,46,36), outline=GOLD)
    d.rectangle([x1 - 9 + ofs, 10, x1 + ofs, GROUND], fill=(92,46,36), outline=GOLD)

# ---- the effects ----------------------------------------------------------------------------------------------
@fx('sc_m16')
def _fx_m16(d, im, e, f):
    """The M16 with the grenade launcher under the barrel. x, y: the grip (Tony's front hand)."""
    x, y = int(e[1]), int(e[2])
    x0, y0 = x - RIFLE_GRIP[0], y - RIFLE_GRIP[1]
    for cy, row in enumerate(RIFLE):
        for cx, ch in enumerate(row):
            if ch != '.': d.point((x0 + cx, y0 + cy), fill=RPAL[ch])

@fx('sc_muzzle')
def _fx_muzzle(d, im, e, f):
    spark(d, int(e[1]), int(e[2]), 2 + int(e[3]) % 2)

@fx('sc_tracer')
def _fx_tracer(d, im, e, f):
    d.line([int(e[1]), int(e[2]), int(e[3]), int(e[4])], fill=(255,230,140))

@fx('sc_nade')
def _fx_nade(d, im, e, f):
    """The grenade on its way: e = (x, y)."""
    d.rectangle([int(e[1]), int(e[2]), int(e[1]) + 1, int(e[2]) + 1], fill=(60,60,60))

@fx('sc_blast')
def _fx_blast(d, im, e, f):
    """The grenade going off at the doors: x, y, k frames in."""
    x, y, k = int(e[1]), int(e[2]), e[3]
    r = 3 + 1.6 * k
    d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], outline=(255,120,30), width=2)
    if k < 8: d.ellipse([x - r / 2, y - r / 4, x + r / 2, y + r / 4], fill=(255,236,160))

@fx('sc_debris')
def _fx_debris(d, im, e, f):
    """Bits of door flying out from the blast: x, y, k."""
    x, y, k = e[1], e[2], e[3]
    for i in range(8):
        rr = random.Random(i * 31 + 7)
        px = x + rr.uniform(-5, 1) * k * 0.6; py = y + rr.uniform(-6, 2) * k * 0.5 + 0.12 * k * k
        if py < GROUND: d.rectangle([int(px), int(py), int(px) + 1, int(py) + 1], fill=(150,110,80) if i % 2 else (90,70,60))

@fx('sc_casing')
def _fx_casing(d, im, e, f):
    """A brass shell case kicked out of the rifle: x, y, k frames since it left."""
    x, y, k = e[1], e[2], e[3]
    px, py = x + 0.9 * k, y - 2.5 * k + 0.18 * k * k
    if py < GROUND: d.point((int(px), int(py)), fill=(235,200,80))

@fx('sc_spurt')
def _fx_spurt(d, im, e, f):
    """Blood out of a hit: x, y, k frames in."""
    x, y, k = e[1], e[2], e[3]
    for i in range(6):
        rr = random.Random(zlib.crc32(f'{x},{y},{i}'.encode()))
        px = x + rr.uniform(-1.6, 1.6) * k; py = y + rr.uniform(-2.2, -0.4) * k + 0.12 * k * k
        if py < GROUND: d.point((int(px), int(py)), fill=(170,18,18))

@fx('sc_corpse')
def _fx_corpse(d, im, e, f):
    """A dead hitman lying flat on the marble: x, feet, k frames since he dropped (the pool grows)."""
    x, y, k = e[1], e[2], e[3]
    r = min(10, 4 + k * 0.6)
    d.ellipse([x - r, y - 2, x + r, y], fill=(150,14,14))              # the pool
    d.rectangle([x - 8, y - 4, x + 5, y - 1], fill=(70,70,92))          # the suit, flat
    d.rectangle([x + 1, y - 4, x + 3, y - 1], fill=(236,236,244))       # the white shirt, open at the neck
    d.point((x + 2, y - 2), fill=(120,18,30))                           # the dark tie
    d.rectangle([x + 5, y - 5, x + 9, y - 1], fill=(214,170,134))       # the head
    d.rectangle([x + 5, y - 5, x + 9, y - 4], fill=(18,14,12))          # the hair
    d.rectangle([x - 12, y - 4, x - 11, y - 3], fill=(214,170,134))     # a hand flung out
    d.rectangle([x - 10, y - 4, x - 9, y - 4], fill=(70,70,92))         # its sleeve
    d.rectangle([x - 10, y - 3, x - 8, y - 1], fill=INK)                 # the shoes

@fx('sc_pistol')
def _fx_pistol(d, im, e, f):
    """A hitman's pistol at his hand: x, y, dir (-1 when he faces left). A barrel and a grip, dark."""
    x, y, dr = int(e[1]), int(e[2]), e[3]
    xs = sorted([x, x + 3 * dr])
    d.rectangle([xs[0], y, xs[1], y], fill=(8,8,10))                    # the barrel and slide
    d.line([x + dr, y - 1, x + 3 * dr, y - 1], fill=(150,150,162))      # the slide's shine, so it reads on a dark suit
    d.point((x, y + 1), fill=(8,8,10))                                  # the grip

@fx('sc_puff')
def _fx_puff(d, im, e, f):
    """A smoke puff from the blast, drifting off: x, y, k frames old."""
    x, y, k = e[1], e[2], e[3]
    r = min(11, 3 + 0.25 * k)
    d.ellipse([x - 0.35 * k - r, y - 0.08 * k - r, x - 0.35 * k + r, y - 0.08 * k + r], fill=(112,106,112))

@fx('sc_glint')
def _fx_glint(d, im, e, f):
    """The globe catching the light: x, y, k."""
    x, y, k = int(e[1]), int(e[2]), e[3]
    if (k // 3) % 2 == 0: spark(d, x, y, 2, c=(255,250,220))
    else: d.point((x, y), fill=(255,255,255))

@fx('sc_bang')
def _fx_bang(d, im, e, f):
    text(d, '!', int(e[1]), int(e[2]), (255,230,90))

@fx('sc_veil')
def _fx_veil(d, im, e, f):
    """The smoke over the whole foyer: a (0..1)."""
    a = e[1]; rr = random.Random(7)
    m = Image.new('L', (W, H), int(200 * a))
    md = ImageDraw.Draw(m)
    for _ in range(18):
        x, y, r = rr.randint(0, W), rr.randint(0, H), rr.randint(14, 30)
        md.ellipse([x - r, y - r, x + r, y + r], fill=int(255 * a))
    m = m.filter(ImageFilter.GaussianBlur(4))
    im.paste((86,80,86), (0, 0), m)

# ---- the close-up --------------------------------------------------------------------------------------------
def _face(im, d, t, f):                                             # Tony's face: the scar, the brows, the eyes going wider
    x0 = int(lerp(14, 6, ease(t)))
    SK, SH, HAIR, WHITE = (226,184,150), (184,136,104), (14,12,16), (240,236,226)
    d.polygon([(x0 - 6, 64), (x0 + 8, 52), (x0 + 26, 50), (x0 + 26, 64)], fill=WHITE, outline=INK)       # lapels
    d.polygon([(x0 + 62, 64), (x0 + 48, 52), (x0 + 30, 50), (x0 + 30, 64)], fill=WHITE, outline=INK)
    d.polygon([(x0 + 26, 50), (x0 + 30, 50), (x0 + 30, 64), (x0 + 26, 64)], fill=(30,28,34))              # dark shirt
    d.polygon([(x0 + 27, 53), (x0 + 33, 53), (x0 + 34, 64), (x0 + 26, 64)], fill=ACCENT)                  # the orange tie
    d.rectangle([x0 + 18, 46, x0 + 38, 54], fill=SK)                                                     # neck
    d.ellipse([x0, 6, x0 + 56, 52], fill=SK, outline=INK)
    d.polygon([(x0 + 38, 10), (x0 + 50, 18), (x0 + 54, 34), (x0 + 48, 46), (x0 + 40, 44), (x0 + 44, 30)], fill=SH)  # the shaded side
    d.polygon([(x0 - 2, 22), (x0 + 4, 6), (x0 + 22, 2), (x0 + 28, 9), (x0 + 34, 2), (x0 + 52, 6), (x0 + 58, 22),
               (x0 + 54, 14), (x0 + 40, 10), (x0 + 28, 14), (x0 + 16, 10), (x0 + 2, 14)], fill=HAIR)         # slicked back, widow's peak
    d.line([x0 + 8, 8, x0 + 20, 5], fill=(70,66,74))                                                      # the sheen
    d.line([x0 + 10, 15, x0 + 24, 20], fill=INK, width=2); d.line([x0 + 46, 15, x0 + 32, 20], fill=INK, width=2)  # brows, down in the middle
    ew = int(lerp(7, 10, ease(t)))
    for cx, px in ((x0 + 18, 1), (x0 + 38, -1)):                                                          # wide eyes, whites showing
        d.ellipse([cx - ew // 2, 27 - ew // 3, cx + ew // 2, 27 + ew // 3], fill=(255,255,255), outline=INK)
        d.rectangle([cx + px - 1, 26, cx + px + 1, 28], fill=INK)
    d.line([x0 + 27, 30, x0 + 26, 38], fill=SH)                                                           # nose
    d.line([x0 + 9, 32, x0 + 20, 43], fill=(240,196,196))                                                 # the scar, across the cheek and lip
    for x, y in ((x0 + 12, 46), (x0 + 16, 50), (x0 + 30, 50), (x0 + 42, 46), (x0 + 36, 52)): d.point((x, y), fill=(60,46,44))  # stubble
    d.rectangle([x0 + 19, 40, x0 + 37, 50], fill=(60,10,14), outline=INK)                                  # the shout
    d.rectangle([x0 + 20, 40, x0 + 36, 43], fill=(246,242,230))                                            # teeth
    d.line([x0 + 28, 40, x0 + 28, 43], fill=INK)
    if t > 0.3: d.ellipse([x0 + 52, 18, x0 + 54, 21], fill=(150,200,240))                                 # sweat

# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 ---------------------------------
def clip_main(f):
    s = scene(f, THEME)
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=SKY, draw=_face, txt=CLOSE); return s
    if not cue(f, GLINT_AT, LINE2): s['under'].append(('sc_lamp',))   # the chandelier keeps out of the caption's way
    s['under'].append(('sc_door', door_open(f)))
    me = tony_pose(f)
    actors = [actor(figure(TONY, POSES[me]), CX, pal=TPAL)]
    if 52 <= f < 66: s['fx'].append(('sc_bang', CX - 3, 20))
    if 62 <= f < 256: s['fx'].append(('sc_m16', *hand_of(me)))
    mx, my = hand_of(me)[0] + MUZZLE_DX, hand_of(me)[1] - 1          # the muzzle

    for i, (tx, death, start) in enumerate(HITMEN):                 # the hitmen, through the doors
        walk_end = start + 18
        if f < start or f >= death + 4: continue
        if f >= death: pose = 'hurt'
        elif f < walk_end: pose = pose_cycle(f, 'walk1', 'walk2', 6)
        else: pose = 'point'
        x = tx if f >= walk_end else lerp(200, tx, (f - start) / 18)
        hit = HITS[i]
        actors.append(actor(figure(hit, POSES[pose]), int(round(x)), flip=True, pal=HPAL))
        if pose != 'hurt':                                          # the pistol in the hand, on the way in and at the shot
            hx, hy = figure_point(hit, POSES[pose], 'hand', int(round(x)), GROUND, True)
            s['fx'].append(('sc_pistol', hx, hy, -1))
        if death <= f < death + 8: s['fx'].append(('sc_spurt', tx, GROUND - 14, f - death))
    for tx, death, start in HITMEN:                                 # the dead
        if death + 4 <= f < 256: s['fx'].append(('sc_corpse', tx, GROUND, f - (death + 4)))

    if 108 <= f < 114:                                              # the grenade launcher
        t = (f - 108) / 6
        s['fx'].append(('sc_nade', lerp(mx, 172, t), lerp(my, 44, t) - 8 * math.sin(math.pi * t)))
    if 108 <= f < 111: s['fx'].append(('sc_muzzle', mx, my, f))
    if 114 <= f < 130:
        s['fx'].append(('sc_blast', 172, 44, f - 114)); s['fx'].append(('sc_debris', 172.0, 44.0, f - 114))
        s['flash'] = 0.9 if f < 116 else 0.35; s['fc'] = (172, 44)
    if 114 <= f < 120: s['shake'] = (1 if f % 2 else -1, 0)
    for j, s0 in enumerate(range(116, 150, 5)):                     # smoke rolling out of the doors
        if s0 <= f < s0 + 60: s['fx'].append(('sc_puff', 170 - 2 * j, 36 + 4 * (j % 3), f - s0))

    for tx, death, start in HITMEN:                                 # the spray: who it's aimed at, in turn
        win = {178: None, 162: (118, 126), 146: (126, 134), 130: (134, 144)}[tx]
        if win and win[0] <= f < win[1] and f % 2 == 0:
            s['fx'].append(('sc_muzzle', mx, my, f))
            s['fx'].append(('sc_tracer', mx, my, tx, GROUND - 14))
            s['shake'] = (1, 0) if f % 4 == 0 else (0, 0)
    if 118 <= f < 146 and f % 3 == 0:                               # the shell cases
        for k in range(0, 15):
            if f - k >= 118 and (f - k) % 3 == 0: s['fx'].append(('sc_casing', CX + 6, GROUND - 17, k))

    if cue(f, GLINT_AT, LINE2): s['fx'].append(('caption', LINE2))
    if GLINT_AT <= f < GLINT_AT + 44:
        s['fx'].append(('sc_glint', 34, 26, f - GLINT_AT)); s['fx'].append(('sc_glint', 12, 42, f - GLINT_AT + 3))
    va = veil_alpha(f)
    if va > 0: s['fx'].append(('sc_veil', va))
    s['actors'] = actors
    return s

CLIPS = [clip('littlefriend', N_, clip_main)]
