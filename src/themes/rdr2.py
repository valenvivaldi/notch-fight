"""Red Dead Redemption 2: Arthur Morgan's last sunrise on the mountain. Claude is Arthur (a hat, a worn coat, an
orange bandana, a satchel). Micah Bell (a cream hat, a moustache, a revolver) comes up the ridge; they fight,
Arthur lands a few punches and coughs, and Micah runs. Arthur sits down on the ridge and the sun comes up over
the peaks, the sky going from blue to gold. Close-up: his face lit orange, eyes half shut: THAT'S THE WAY IT IS.
Then the sun goes back down, Arthur gets up, his horse nudges him, and the clip is back on the neutral pose:
Arthur on the ridge with his horse under the pre-dawn stars."""
import math, random
from engine import *

THEME = 'rdr2'
register_bg(THEME, lambda v: (v+30,v+24,v+44))                       # the dotted ridge line
N_ = 360                                                            # a multiple of 12: the guard bounce loops
CLOSE = "THAT'S THE WAY IT IS."
CLOSE_AT, CLOSE_LEN = 252, 44                                       # the close-up (ends before the sun goes down)
CX, HX, MX, RX_IN = 50, 20, 68, W + 14                              # Arthur, his horse, where Micah stops, where he enters
INK = (16,14,22)
PALE, PALE_SHADE = (232,226,214), (170,160,150)
SKIN, SKIN_SHADE, BANDANA, BANDANA_SHADE = (236,150,100), (168,92,66), (217,119,87), (150,64,48)
HAT, HAT_SHADE = (92,58,34), (48,28,18)                              # the close-up's hat

# ---- the horse: a hand-drawn 34 x 24 sprite (rows of HPAL chars), facing right --------------------------
HPAL = {'w':PALE, 'g':PALE_SHADE, 'd':(58,42,44), 'h':(30,24,28), 'e':INK, 'n':(176,112,104),
        'x':(120,40,36), 'z':(92,56,30), 'b':(176,140,92), 'B':(126,94,60)}   # coat, grey shade, mane/tail, hooves,
                                                                              # eye, nostril, blanket, saddle, bedroll
HORSE = {
 'idle': S([
  ".........................w........",
  "........................www.......",
  "........................dwwww.....",
  "......................ddwwwewww...",
  ".....................ddwwwwwwwww..",
  "....................ddwwwwwgwwwww.",
  ".......bbbbb....z..ddwwwwww..wwwwn",
  ".......BBBBBzzzzzzddwwwwwww...gggw",
  "......wwwwwxxxxxxxddwwwwwww.......",
  "...ddwwwwwwxxxxxxxwwwwwwwww.......",
  "..ddwwwwwwwxxxxxxxwwwwwwwwww......",
  "..ddwwwwwwwwxxxxxwwwwwwwwwww......",
  ".dddwwwwwwwwwwwwwwwwwwwwwwww......",
  ".dddwwwwwwwwwwwwwwwwwwwww.........",
  ".dddwwwwwwwwwwwwwwwwwwwww.........",
  ".ddd..wwwwwgggggggggwww...........",
  ".dd..wwwww.gg.....gg.www..........",
  ".dd...www..gg.....gg.www..........",
  ".dd..www..gg......gg.ww...........",
  "..d..ww...gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  "....hhh...hh......hh.hhh..........",
  "....hhh...hh......hh.hhh..........",
 ]),
 'swish': S([                                                        # the tail flicks
  ".........................w........",
  "........................www.......",
  "........................dwwww.....",
  "......................ddwwwewww...",
  ".....................ddwwwwwwwww..",
  "....................ddwwwwwgwwwww.",
  ".......bbbbb....z..ddwwwwww..wwwwn",
  ".......BBBBBzzzzzzddwwwwwww...gggw",
  "......wwwwwxxxxxxxddwwwwwww.......",
  "...ddwwwwwwxxxxxxxwwwwwwwww.......",
  "..ddwwwwwwwxxxxxxxwwwwwwwwww......",
  ".dddwwwwwwwwxxxxxwwwwwwwwwww......",
  "ddd.wwwwwwwwwwwwwwwwwwwwwwww......",
  "ddd.wwwwwwwwwwwwwwwwwwwww.........",
  "ddd.wwwwwwwwwwwwwwwwwwwww.........",
  "dd....wwwwwgggggggggwww...........",
  "dd...wwwww.gg.....gg.www..........",
  ".d....www..gg.....gg.www..........",
  ".....www..gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  "....hhh...hh......hh.hhh..........",
  "....hhh...hh......hh.hhh..........",
 ]),
 'nuzzle': S([                                                       # the head lowered to nudge him
  "..................................",
  "..................................",
  "..................................",
  "..................................",
  "........................w.........",
  ".....................ddwww........",
  ".......bbbbb....z...ddwwww........",
  ".......BBBBBzzzzzz.ddwwwwwwww.....",
  "......wwwwwxxxxxxxddwwwwwwwewww...",
  "...ddwwwwwwxxxxxxxwwwwwwwwwwwwww..",
  "..ddwwwwwwwxxxxxxxwwwwwwwwwwwwwww.",
  "..ddwwwwwwwwxxxxxwwwwwwwwwwww.wwww",
  ".dddwwwwwwwwwwwwwwwwwwwwwwww...ggn",
  ".dddwwwwwwwwwwwwwwwwwwwww.........",
  ".dddwwwwwwwwwwwwwwwwwwwww.........",
  ".ddd..wwwwwgggggggggwww...........",
  ".dd..wwwww.gg.....gg.www..........",
  ".dd...www..gg.....gg.www..........",
  ".dd..www..gg......gg.ww...........",
  "..d..ww...gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  ".....ww...gg......gg.ww...........",
  "....hhh...hh......hh.hhh..........",
  "....hhh...hh......hh.hhh..........",
 ]),
}

# ---- people, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
GW, GH, C = 24, 24, 11                                              # the grid and its centre column (they face right)
POSES = dict(POSES)
POSES['cough'] = ((2, 4), (5, 0), (5, 3), (3, -2), 3, 'stance')    # doubled over, a hand up to the mouth
POSES['sit'] = ((-1, 3), (-3, 6), (6, 4), (4, 2), -1, 'stand')     # seated on the ground: a hand on the ground behind, the
                                                                    # forearm on the raised knee (the legs are _seated)
_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)

def _satchel(g, at):                                                # a satchel on his back (the left side)
    for y in (at['ty'] + 2, at['ty'] + 3, at['ty'] + 4): put(g, at['c'] - 4 + at['sh'](y), y, 'b')

def _moustache(g, at):                                              # a thick moustache under the eyes
    y, o = at['hy'] + 3, at['sh'](at['hy'])
    for x in (at['c'] - 1, at['c'], at['c'] + 1): put(g, x + o, y, 'm')

def _seated(g, at):                                                 # on the ground: one leg out flat, one knee up
    c, hip = at['c'], at['hip']
    for x in range(c - 2, c + 12): put(g, x, hip, '.')              # the standing boot row goes
    for x in range(c + 3, c + 9): put(g, x, hip - 1, 'p'); put(g, x, hip, 'p')   # the far leg, flat on the ground
    for x in range(c + 7, c + 11): put(g, x, hip, 'k')              # its boot
    seg(g, c, hip - 2, c + 4, hip - 6, 'p'); seg(g, c + 1, hip - 2, c + 5, hip - 6, 'p')   # the thigh, up to the knee
    seg(g, c + 4, hip - 6, c + 4, hip, 'p'); seg(g, c + 5, hip - 6, c + 5, hip, 'p')       # the shin, down to the ground
    for x in range(c + 3, c + 7): put(g, x, hip, 'k')               # its boot

def _coat(g, at):                                                   # the coat: a shaded back, an open front showing the
    c, ty, hip, sh = at['c'], at['ty'], at['hip'], at['sh']         # shirt, a gun belt and holster, the satchel strap,
    for y in range(ty + 1, hip - 1): put(g, c - 3 + sh(y), y, 'J')  # the bandana at the neck
    for y in range(ty + 1, hip - 2): put(g, c + 1 + sh(y), y, 'A')
    for x in range(c - 3, c + 3):                                                  # the gun belt, brass cartridges along it
        put(g, x + sh(hip - 1), hip - 1, 'Y' if (x - c) % 2 else 'z')
    put(g, c + sh(hip - 1), hip - 1, 'Y')                                          # the buckle
    for y in (hip, hip + 1, hip + 2):                                             # the holster, 2 x 3, tan leather on the hip
        put(g, c + 2 + sh(y), y, 'L'); put(g, c + 3 + sh(y), y, 'L')
    put(g, c + 3, hip - 2, 'G'); put(g, c + 4, hip - 2, 'G'); put(g, c + 3, hip - 1, 'G')   # the gun's grip, out of it
    seg(g, c - 3 + sh(ty + 1), ty + 1, c + 2 + sh(hip - 2), hip - 2, 'T')          # the satchel strap, across the chest
    put(g, c + 2 + sh(ty + 1), ty + 1, 'o')                                        # the bandana's knot
    put(g, c + 2, ty + 1, 'o')

def _vest(g, at):                                                   # Micah's grey-blue vest: a darker back, a white shirt
    c, ty, hip, sh = at['c'], at['ty'], at['hip'], at['sh']         # showing at the front
    for y in range(ty + 1, hip): put(g, c - 3 + sh(y), y, 'V')
    for y in range(ty + 1, hip - 1): put(g, c + 1 + sh(y), y, 'W')

def _hat(felt, band):
    """A cowboy hat over the head: a pinched crown with a dark band, a 10-px brim with curled-up ends. On a
    seated man (his hip on the ground line) it is tilted down a row."""
    def paint(g, at):
        c, hy, h = at['c'], at['hy'], at['h']
        o = at['sh'](hy)
        b = hy if at['hip'] == h - 1 else hy - 1                    # the brim's row
        for x in (c - 2, c - 1, c + 1, c + 2): put(g, x + o, b - 2, felt)     # the crown top, pinched in the middle
        for x in range(c - 2, c + 3): put(g, x + o, b - 1, band)              # the band
        for x in range(c - 5, c + 5): put(g, x + o, b, felt)                  # the brim
        put(g, c - 5 + o, b - 1, felt); put(g, c + 4 + o, b - 1, felt)        # its ends, curled up
    return paint

def _brim_shadow(colour):
    def paint(g, at):                                               # the brim's shadow across the eyes
        c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
        for x in range(c - 2, c + 3): put(g, x + o, hy + 1, colour)
    return paint

def _hair_long(g, at):                                              # Micah's blond hair, down the back under the hat
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for y in range(hy + 1, at['ty'] + 2): put(g, c - 3 + o, y, 'y')
    put(g, c - 2 + o, hy + 4, 'y')

CLAUDE = dict(_BODY, name='rdr2-arthur', hair=[], shut='K',
              body=dict(color='j', collar='o', hip='b'), leg=dict(color='p', boot='k'),
              paint=dict(body=[_satchel, _coat], head=[_brim_shadow('D')], end=[_hat('h', 'Q')]))
CLAUDE_SIT = dict(CLAUDE, name='rdr2-arthur-sit', legs=1, paint=dict(body=[_satchel, _coat], legs=[_seated],
                  head=[_brim_shadow('D')], end=[_hat('h', 'Q')]))
RIVAL = dict(_BODY, name='rdr2-micah', hair=[], shut='K', eyes=(0, 2),
             body=dict(color='j', collar='W', hip='p'), leg=dict(color='p', boot='k'),
             paint=dict(body=[_vest], head=[_brim_shadow('D'), _hair_long], face=[_moustache], end=[_hat('h', 'Q')]))
CPAL = {'s':(226,176,136), 'K':INK, 'h':(120,80,46), 'Q':(40,24,16), 'D':(52,34,22), 'j':(120,84,56),
        'J':(88,60,40), 'A':(214,206,190), 'p':(62,50,44), 'k':INK, 'o':BANDANA, 'b':(72,44,26), 'z':(38,24,16),
        'G':(176,176,186), 'T':(96,64,36), 'L':(160,112,64), 'Y':(214,176,84)}
RPAL = {'s':(206,164,130), 'K':INK, 'h':(236,232,222), 'Q':(52,40,32), 'D':(170,160,146), 'j':(110,128,150),
        'V':(88,104,124), 'W':(236,234,228), 'p':(44,40,60), 'k':INK, 'm':(64,44,34), 'y':(222,190,110)}

def build(who, pose):
    """Arthur or Micah in a pose (POSES): engine/people.py's figure()."""
    if who == 'claude': return figure(CLAUDE_SIT if pose == 'sit' else CLAUDE, POSES[pose])
    return figure(RIVAL, POSES[pose])

def put_on(spr, wx, flip=False, pal=None):
    """An actor standing at world x."""
    return actor(spr, int(wx), flip=flip, pal=pal)

def ready(f):                                                       # the neutral pose: it moves every 12 frames, which divides N_
    return pose_cycle(f, 'guard', 'guard2')

# ---- the sky, the peaks and the sun: one picture per frame, so the sunrise can be drawn ------------------
NIGHT_TOP, NIGHT_BOT = (10,12,34), (46,42,88)                      # pre-dawn
DAY_TOP, DAY_MID, DAY_BOT = (62,88,150), (214,122,92), (255,184,98)  # the sunrise: blue to orange gold
_rr = random.Random(9)
STARS = [(_rr.randint(0, W - 1), _rr.randint(0, 26), _rr.random()) for _ in range(22)]
PINES = (5, 13, 25, 98, 108, 150, 160, 176)

def _mix(a, b, t): return tuple(int(lerp(x, y, t)) for x, y in zip(a, b))

def far_y(x): return 30 + 7 * math.sin(x * 0.05 + 0.6) + 4 * math.sin(x * 0.14 + 2.2)
def mid_y(x): return 44 + 3 * math.sin(x * 0.08 + 1.4) + 1.5 * math.sin(x * 0.21)
def ridge_y(x): return 57 + 1.2 * math.sin(x * 0.04)

def _ridge_poly(fn):
    return [(x, fn(x)) for x in range(0, W + 3, 3)] + [(W + 3, H), (0, H)]

def k_of(f):
    """How far the sun has come up: 0 before dawn, 1 at full sunrise (the close-up), back to 0 by the end."""
    if f < 186: return 0.0
    if f < 250: return ease((f - 186) / 64)
    if f < 300: return 1.0
    if f < 350: return 1 - ease((f - 300) / 50)
    return 0.0

def kb(f, a, b):
    """A knockback: a hit pushes its target 2 px back for 4 frames, then 1 px until b, then none."""
    return 2 if a <= f < a + 4 else (1 if a + 4 <= f < b else 0)

def _paint_dawn(d, k, f):
    for y in range(H):
        t = min(1.0, y / 50)
        day = _mix(DAY_TOP, DAY_MID, t * 2) if t < 0.5 else _mix(DAY_MID, DAY_BOT, (t - 0.5) * 2)
        d.line([0, y, W, y], fill=_mix(_mix(NIGHT_TOP, NIGHT_BOT, t), day, k))
    for x, y, off in STARS:                                         # they twinkle, and go as the sky warms
        b = (0.55 + 0.45 * math.sin(2 * math.pi * ((loop.phase(f, 36) + off) % 1))) * (1 - k)
        if b > 0.1: d.point((x, y), fill=tuple(int(v * b) for v in (220, 226, 255)))
    if k > 0.02:                                                    # the sun, behind the far peaks until it clears them
        sx, sy = 124, lerp(74, 20, ease(k))
        d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=_mix((200,110,90), (250,170,90), k))
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(255,214,120))
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255,242,196))
    d.polygon(_ridge_poly(far_y), fill=_mix((26,24,54), (120,84,112), k))
    d.polygon(_ridge_poly(mid_y), fill=_mix((18,16,36), (70,46,74), k))
    for px in PINES:
        by = mid_y(px) + 1
        d.polygon([(px, by - 9), (px - 2, by), (px + 2, by)], fill=_mix((10,10,22), (40,28,44), k))
    d.polygon(_ridge_poly(ridge_y), fill=_mix((12,10,22), (44,30,40), k))

@fx('rd_dawn')
def _fx_dawn(d, im, e, f):
    """The whole sky, hills and sun for this frame: ('rd_dawn', {'k': 0..1})."""
    _paint_dawn(d, e[1]['k'], f)

@fx('rd_spark')
def _fx_spark(d, im, e, f):
    """A spark: (name, x, y, k), k the frames since it started."""
    _, x, y, k = e; spark(d, int(x), int(y), 3 + int(k) // 2)

@fx('rd_cough')
def _fx_cough(d, im, e, f):
    """A spray of red from the mouth: (name, x, y, k), k the frames since the cough. 2 px specks, 5 of them."""
    _, x, y, k = e
    for i in range(5):
        px = x + int((i - 2) * 1.6 + k * 0.5)
        py = y + int(abs(i - 2) * 0.8 + k * 0.7)
        col = (196, 26, 36) if i % 2 else (150, 18, 28)
        d.rectangle([px, py, px + 1, py + 1], fill=col)

def _face(im, d, t, f):                                             # his face in the sun, eyes half shut
    _paint_dawn(d, 1.0, f)
    ox = int(lerp(0, -3, ease(t)))                                  # a slow push in
    def R(x0, y0, x1, y1): return [x0 + ox, y0, x1 + ox, y1]
    d.polygon([(24 + ox, 50), (52 + ox, 50), (57 + ox, 64), (19 + ox, 64)], fill=SKIN_SHADE)    # neck
    d.polygon([(16 + ox, 49), (60 + ox, 49), (57 + ox, 58), (38 + ox, 63), (20 + ox, 58)], fill=BANDANA)  # bandana
    d.polygon([(44 + ox, 52), (54 + ox, 50), (50 + ox, 62)], fill=BANDANA_SHADE)                 # its knot
    d.ellipse(R(20, 22, 56, 50), fill=SKIN_SHADE, outline=INK)                                   # shade side (left)
    d.ellipse(R(27, 22, 57, 50), fill=SKIN, outline=INK)                                         # the sun side (right)
    d.ellipse(R(44, 32, 52, 46), fill=(246,176,122))                                             # the lit cheek
    d.polygon([(25 + ox, 18), (27 + ox, 7), (34 + ox, 4), (38 + ox, 8), (42 + ox, 4), (49 + ox, 7), (51 + ox, 18)],
              fill=HAT, outline=INK)                                                             # the crown, pinched on top
    d.rectangle(R(26, 14, 50, 17), fill=HAT_SHADE)                                               # its band
    d.polygon([(10 + ox, 14), (16 + ox, 18), (60 + ox, 18), (66 + ox, 14), (64 + ox, 20), (56 + ox, 22),
               (20 + ox, 22), (12 + ox, 20)], fill=HAT, outline=INK)                             # the brim, curled up at the ends
    d.rectangle(R(20, 22, 56, 26), fill=HAT_SHADE)                                               # the brim's shadow on the forehead
    d.rectangle(R(27, 31, 35, 32), fill=INK); d.rectangle(R(41, 31, 49, 32), fill=INK)           # lids, half shut
    d.rectangle(R(29, 33, 33, 33), fill=(240,232,220)); d.rectangle(R(43, 33, 47, 33), fill=(240,232,220))   # the eye under it
    d.line([38 + ox, 35, 36 + ox, 40], fill=SKIN_SHADE)                                          # the nose
    d.rectangle(R(33, 41, 43, 42), fill=(80,50,36))                                              # moustache
    d.line([35 + ox, 44, 41 + ox, 44], fill=(120,60,44))                                         # mouth
    rr = random.Random(5)                                                                        # stubble on the jaw
    for _ in range(46):
        x, y = rr.randint(24, 52), rr.randint(44, 52)
        if ((x - 38) / 15) ** 2 + ((y - 46) / 7) ** 2 <= 1:
            d.point((x + ox, y), fill=rr.choice([(110,78,58), (150,116,92), (96,68,52)]))

# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 --------------------------------
def nudge(f):                                                       # the horse steps in to nudge him, then back
    return 3 * math.sin(math.pi * (f - 330) / 18) if 330 <= f < 348 else 0.0

def horse_frame(f):
    """Idle: the tail flicks every 12 frames (a period of 24, which divides N_); he lowers his head to nudge him."""
    if 332 <= f < 346: return HORSE['nuzzle']
    return HORSE[pose_cycle(f, 'idle', 'swish', 12)]

def clip_main(f):
    s = scene(f, THEME)
    k = k_of(f)
    me, rival, rx, mx = ready(f), None, MX, CX
    if 16 <= f < 52: rival, rx = pose_cycle(f, 'walk1', 'walk2'), lerp(RX_IN, MX, ease((f - 16) / 36))   # Micah walks in
    if 52 <= f < 118: rival = ready(f)                              # the standoff
    if 64 <= f < 70: me = 'jab'                                     # Arthur lands a punch
    if 68 <= f < 80: rival, rx = 'hurt', MX + 4 - kb(f, 68, 80)     # Micah is knocked back
    if 78 <= f < 86: rival = 'hook'                                 # Micah hits back
    if 84 <= f < 94: me, mx = 'hurt', CX - kb(f, 84, 94)            # Arthur is knocked back
    if 94 <= f < 108: me = 'cough'                                  # the tuberculosis
    if 108 <= f < 114: me = 'jab'                                   # he still lands one
    if 112 <= f < 118: rival, rx = 'hurt', MX + 4 - kb(f, 112, 118)
    if 118 <= f < 152: rival, rx = pose_cycle(f, 'run1', 'run2', 3), lerp(MX, W + 30, (f - 118) / 34)   # Micah runs
    if 124 <= f < 146: me = 'crouch'                                # Arthur sinks down
    if 146 <= f < 304: me = 'sit'                                   # ...and sits on the ridge, watching the sun
    if 304 <= f < 314: me = 'crouch'                                # gets up
    if 68 <= f < 76: s['fx'].append(('rd_spark', 60, 40, f - 68))
    if 84 <= f < 92: s['fx'].append(('rd_spark', 58, 36, f - 84))
    if 112 <= f < 118: s['fx'].append(('rd_spark', 60, 40, f - 112))
    if 94 <= f < 106: s['fx'].append(('rd_cough', 53, 41, f - 94))
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=SKIN, draw=_face, txt=CLOSE); return s
    s['under'].append(('rd_dawn', {'k': k}))
    s['actors'] = [actor(horse_frame(f), int(HX + nudge(f)), pal=HPAL), put_on(build('claude', me), mx, pal=CPAL)]
    if rival: s['actors'].append(put_on(build('rival', rival), rx, flip=f < 118, pal=RPAL))
    return s

CLIPS = [clip('sunrise', N_, clip_main)]
