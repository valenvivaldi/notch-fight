"""Tres Acordes (Trukini's adult animated series, Rosario): Claude is in the flat with the three friends.
Drawn after the show: Jaique on the couch (the black block of hair, the long chin, the skull t-shirt, red
eyes), Eduard with his notebook (the long brown hair, the fringe over one eye), Adriel about to blow up (the
orange curls and sideburns, round glasses, red t-shirt, green shorts). Berna, Adriel's dad (black hair, the
glasses, a black vest), comes in from the left and shouts; Dios (bald and yellow, two black tufts, the
horseshoe moustache, a green vest, a cigarette) comes down on a cloud.
Clip `poema`: Eduard asks Claude to read his book of poems (nobody ever did); Claude reads one out, sober, no
frills, and likes it — close-up: the fringe, the tears, POR FIN ALGUIEN LO LEYO. Adriel wants his YouTube channel
seen too.
Clip `fristail`: Adriel raps (TODO CARO, TODO CARO), Claude makes the beat; Jaique: repetitive, Colorado. Claude
uploads it: 700 views and everyone laughs — close-up: the curls, the glasses, YO HAGO ARTE, NO COMEDIA. Berna
walks in: BUEN LABURAR NUNCA, NO? MEDIOCRE, and walks out again.
Clip `sentido`: Jaique, on the couch, asks Claude the meaning of life; Claude answers first (TENER BUENA
BANDA); Dios comes down on a cloud and answers too — close-up: the moustache, the smoke, NI IDEA, PREGUNTENLE A CLAUDE.
Jaique falls asleep (ZZZ) and wakes up. Every clip starts and ends on the same flat (the neutral pose)."""
from engine import *

THEME = 'tresacordes'
N1, N2 = 300, 240                                       # multiples of 12 (Claude's bob) and of 4 (the shake)
EX, CX, AX, JX = 28, 58, 88, 152                        # neutral: Eduard, Claude, Adriel, Jaique on the couch
WALL, FLOOR = (116, 150, 140), (118, 80, 52)

# ---- colours, as the show draws them: flat fills, a dark line, pale pink skin, big noses ------------------------
SKIN_P = ((206, 150, 152), (246, 206, 204), (255, 232, 228))         # Adriel, Eduard, Jaique: pale pink
SKIN_Y = ((204, 146, 54), (246, 200, 104), (255, 232, 156))          # Dios: yellow
GINGER = ((160, 66, 16), (228, 120, 38), (255, 176, 86))             # Adriel's curls and beard
HAIR_E = ((44, 26, 16), (96, 58, 34), (144, 96, 58))                 # Eduard's long hair
TUFT = ((8, 8, 10), (26, 26, 30), (72, 72, 82))                      # Dios's two tufts, the moustache
GLASS_F, LENS = (30, 26, 34), (176, 222, 246)
RED_L, RED, RED_D = (232, 78, 72), (198, 40, 42), (120, 20, 28)

# ---- people: body specs for figure() (facing right; flip to face left) ---------------------------------------
def _snout(g, at):                                      # the show's nose: big, out past the face
    o = at['sh'](at['hy']); put(g, at['c'] + 3 + o, at['hy'] + 2, 's'); put(g, at['c'] + 3 + o, at['hy'] + 3, 's')

def _rims(g, at):                                       # Jaique: red eye corners, a sleepy face
    o = at['sh'](at['hy']); y = at['hy'] + 2
    put(g, at['c'] - 1 + o, y, 'r'); put(g, at['c'] + 1 + o, y, 'r')

def _chin(g, at):                                       # Jaique: the long chin, pointing down and forward
    o = at['sh'](at['hy']); y = at['hy'] + 5
    put(g, at['c'] - 2 + o, y, '.'); put(g, at['c'] - 1 + o, y, '.'); put(g, at['c'] + 3 + o, at['hy'] + 3, 's')

def _skull(g, at):                                      # Jaique: the skull on his black t-shirt
    o = at['sh'](at['ty'] + 2)
    for x, y, ch in ((-1, 2, 'W'), (0, 2, 'W'), (-1, 3, 'w'), (0, 3, 'w')): put(g, at['c'] + x + o, at['ty'] + y, ch)

def _stubble(g, at):                                    # Eduard: a shadow of beard on the jaw
    o = at['sh'](at['hy']); put(g, at['c'] + 1 + o, at['hy'] + 4, 'b'); put(g, at['c'] + 2 + o, at['hy'] + 4, 'b')

def _book(g, at):                                       # Eduard: the notebook, held at the chest
    o = at['sh'](at['ty'] + 3)
    for y in range(at['ty'] + 3, at['ty'] + 6):
        for x in range(at['c'] - 2, at['c'] + 2): put(g, x + o, y, 'N')
        put(g, at['c'] - 2 + o, y, 'n')

def _specs(g, at):                                      # Adriel, Berna: round glasses, the lenses light blue
    o = at['sh'](at['hy']); y = at['hy'] + 2
    put(g, at['c'] - 1 + o, y, 'g'); put(g, at['c'] + 1 + o, y, 'g')
    put(g, at['c'] + o, y - 1, 'e'); put(g, at['c'] + 2 + o, y - 1, 'e')

def _brows(g, at):                                      # Adriel: the brows down over the glasses
    o = at['sh'](at['hy'])
    for x in (0, 1, 2): put(g, at['c'] + x + o, at['hy'], 'd')

def _ginger_beard(g, at):                               # Adriel: the curly sideburns down to the chin
    o = at['sh'](at['hy'])
    for x, y in ((-1, 3), (-1, 4), (0, 4), (1, 4)): put(g, at['c'] + x + o, at['hy'] + y, 'h')

def _stache(g, at):                                     # Dios: the horseshoe moustache, the cigarette
    o = at['sh'](at['hy'])
    for x, y in ((1, 3), (2, 3), (1, 4)): put(g, at['c'] + x + o, at['hy'] + y, 'm')
    put(g, at['c'] + 3 + o, at['hy'] + 4, 'W'); put(g, at['c'] + 4 + o, at['hy'] + 4, 'R')
    put(g, at['c'] - 1 + o, at['hy'], 'Y')                                       # the shine on the bald head

JAIQUE = dict(name='jaique', head=6, hair=["hhhhhhhhhhh", "hHhhhhhhHhh", ".hhhhhhhhh.", "..hhhhhhh..", "..hhhhhhh..",
                                           "..hh......."], hair_x=-5, hair_y=5,
              body=dict(color='j', top='J'), leg=dict(color='p', boot='k'), arm=dict(sleeve='j', hand='s'),
              paint=dict(head=[_rims, _snout], body=[_skull], face=[_chin]))
EDUARD = dict(name='eduard', hair=["..hhhh.", ".hhhhhh", "hhhhhhh", "hhhhH..", "hhh.hh.", "hhh....", "hhh....",
                                   "hh.....", "hh....."], hair_x=-3, hair_y=2,
              body=dict(color='j', top='J'), leg=dict(color='p', boot='k'), arm=dict(sleeve='j', hand='s'),
              paint=dict(head=[_snout, _stubble], body=[_book]))
ADRIEL = dict(name='adriel', hair=[".hHhHh.", "hHhhhHh", "hhhhhhh", "hhh....", "hh.....", "hh.....", ".h....."],
              hair_x=-3, hair_y=3, eye='E', shorts='q',
              body=dict(color='j', top='J'), leg=dict(color='s', boot='k'), arm=dict(sleeve='j', hand='s'),
              paint=dict(head=[_specs, _snout], face=[_brows, _ginger_beard]))
BERNA = dict(name='berna', hair=[".hhhhh.", "hhhhhhh", "hhh....", "hh....."], hair_x=-3, hair_y=2, eye='E',
             body=dict(color='j', top='J'), leg=dict(color='p', boot='k'), arm=dict(sleeve='s', hand='s'),
             paint=dict(head=[_specs, _snout]))
DIOS = dict(name='dios', hair=["hh.....", "hh....."], hair_x=-3, hair_y=-1, shorts='q', eye='L',
            body=dict(color='j', top='J'), leg=dict(color='s', boot='k'), arm=dict(sleeve='s', hand='s'),
            paint=dict(face=[_stache]))

PINK = SKIN_P[1]
JPAL = {'K': (24, 14, 12), 's': PINK, 'j': (34, 34, 38), 'J': (52, 52, 58), 'p': (66, 88, 132), 'k': (28, 24, 24),
        'h': (14, 12, 14), 'H': (52, 50, 58), 'r': (220, 90, 96), 'W': (240, 240, 236), 'w': (190, 190, 186)}
EPAL = {'K': (24, 14, 12), 's': PINK, 'j': (32, 32, 36), 'J': (50, 50, 56), 'p': (98, 132, 196), 'k': (30, 26, 24),
        'h': HAIR_E[1], 'H': HAIR_E[2], 'b': (200, 156, 146), 'N': (60, 100, 180), 'n': (240, 236, 220)}
APAL = {'K': (24, 14, 12), 's': PINK, 'j': (204, 44, 44), 'J': (166, 30, 34), 'q': (64, 126, 92),
        'k': (214, 48, 48), 'h': GINGER[1], 'H': GINGER[2], 'd': GINGER[0], 'E': (54, 116, 210), 'e': LENS,
        'g': GLASS_F}
BPAL = {'K': (24, 14, 12), 's': PINK, 'j': (28, 28, 32), 'J': (44, 44, 50), 'p': (92, 92, 102), 'k': (30, 26, 24),
        'h': (16, 14, 16), 'E': (54, 116, 210), 'e': LENS, 'g': GLASS_F}
DPAL_ = {'K': (24, 14, 12), 's': SKIN_Y[1], 'j': (150, 202, 44), 'J': (122, 172, 30), 'q': (58, 80, 160),
         'k': (60, 44, 36), 'h': TUFT[1], 'm': TUFT[0], 'W': (246, 246, 240), 'R': (255, 120, 40), 'Y': SKIN_Y[2],
         'L': (120, 78, 30)}

def man(spec, pose, x, pal, flip=False, y=GROUND, **flags):
    """A person (engine/people.py figure) in a pose, feet at y."""
    return actor(figure(spec, POSES[pose], **flags), x, y, flip=flip, pal=pal)

def claude(pose, x=CX):
    """Claude: the orange base sprite (CL) from claude.py, feet on the ground."""
    return actor(CL[pose], x, GROUND)

# ---- the flat -----------------------------------------------------------------------------------------------
def _flat(d):
    d.rectangle([0, 0, W, H], fill=WALL)
    for x in range(0, W, 12): d.line([x, 0, x, GROUND - 1], fill=(104, 136, 126))     # the wall's stripes
    d.rectangle([0, GROUND, W, H], fill=FLOOR)
    for y in range(GROUND + 2, H, 3): d.line([0, y, W, y], fill=(100, 66, 40))        # the planks
    d.rectangle([14, 6, 50, 34], fill=(40, 50, 96), outline=(200, 190, 170), width=2)  # the window, night
    d.line([32, 6, 32, 34], fill=(200, 190, 170)); d.line([14, 20, 50, 20], fill=(200, 190, 170))
    d.ellipse([38, 10, 44, 16], fill=(240, 236, 200))                                  # the moon
    for x, y in ((18, 12), (26, 28), (44, 27), (20, 26)): d.point((x, y), fill=(255, 255, 255))
    d.rectangle([0, 38, 9, GROUND - 1], fill=(96, 60, 40))                             # the bookshelf
    for i, c in enumerate(((180, 60, 60), (70, 120, 180), (230, 200, 90), (80, 160, 90), (200, 120, 60))):
        d.rectangle([1 + i * 2, 40 + (i % 2) * 4, 2 + i * 2, GROUND - 1], fill=c)
    d.rectangle([62, 8, 74, 24], fill=(214, 200, 170), outline=(120, 90, 60))           # a poster: a guitar
    d.ellipse([64, 14, 70, 22], fill=(150, 80, 40)); d.line([67, 8, 67, 14], fill=(60, 40, 30))
    d.line([178, 26, 178, GROUND], fill=(60, 60, 60)); d.polygon([(172, 26), (184, 26), (182, 34), (174, 34)], fill=(240, 210, 120))
register_bg(THEME, lambda v: (v + 60, v + 46, v + 30), decor=_flat)

# ---- effects ------------------------------------------------------------------------------------------------
@fx('ts_couch')
def _fx_couch(d, im, e, f):
    """The couch (drawn over the people's legs): a backrest, the seat with its seam, the arm."""
    back, hi, sh = (120, 74, 56), (150, 98, 74), (84, 50, 38)
    d.rounded_rectangle([124, 44, 184, 52], 3, fill=back, outline=OUT)
    d.line([126, 45, 182, 45], fill=hi)
    d.rectangle([124, 52, 184, GROUND], fill=back, outline=OUT)
    d.line([125, 53, 183, 53], fill=hi); d.line([154, 54, 154, GROUND - 1], fill=sh)
    d.rectangle([120, 46, 127, GROUND], fill=sh, outline=OUT)

@fx('ts_cloud')
def _fx_cloud(d, im, e, f):
    """A cloud Dios stands on: x, y its centre."""
    _, x, y = e
    for dx, dy, r in ((0, 0, 7), (-7, 2, 5), (7, 2, 6), (-2, -3, 5), (5, -3, 4)):
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(246, 246, 252), outline=(196, 204, 222))
    d.rectangle([x - 12, y + 3, x + 12, y + 6], fill=(246, 246, 252))

@fx('ts_mic')
def _fx_mic(d, im, e, f):
    """A microphone in a hand (x, y): the grey grille, the black handle down from it."""
    _, x, y = e
    d.line([x, y + 1, x, y + 4], fill=(30, 30, 34)); d.ellipse([x - 1, y - 2, x + 1, y], fill=(170, 170, 180), outline=OUT)

@fx('ts_notes')
def _fx_notes(d, im, e, f):
    """Notes floating up off a rapper (x, y): four, back where they started every 40 frames."""
    _, x, y = e
    for i in range(4):
        ph = (loop.phase(f, 40) + i / 4) % 1.0
        nx, ny = x + i * 5 - 6 + round(math.sin(ph * 6 + i) * 2), int(y - ph * 18)
        d.ellipse([nx - 1, ny, nx + 1, ny + 2], fill=(250, 250, 250)); d.line([nx + 1, ny + 1, nx + 1, ny - 3], fill=(250, 250, 250))

@fx('ts_beat')
def _fx_beat(d, im, e, f):
    """The beat Claude makes with his mouth, BUM and TSS by turns over him (x, y)."""
    _, x, y = e
    text(d, 'BUM' if (f // 6) % 2 == 0 else 'TSS', x - 6, y, (255, 214, 120) if (f // 6) % 2 == 0 else (190, 230, 255), shadow=OUT)

@fx('ts_book')
def _fx_book(d, im, e, f):
    """Eduard's book of poems, open in Claude's hands (x, y the middle of the spine)."""
    _, x, y = e
    d.rectangle([x - 5, y - 3, x + 5, y + 3], fill=(60, 100, 180), outline=OUT)
    d.rectangle([x - 4, y - 2, x - 1, y + 2], fill=(244, 240, 226)); d.rectangle([x + 1, y - 2, x + 4, y + 2], fill=(244, 240, 226))
    for k in range(2): d.line([x - 3, y - 1 + k * 2, x - 2, y - 1 + k * 2], fill=(140, 140, 150)); d.line([x + 2, y - 1 + k * 2, x + 3, y - 1 + k * 2], fill=(140, 140, 150))

@fx('ts_rage')
def _fx_rage(d, im, e, f):
    """Angry marks by a head (x, y), flicking on and off: the little cross of a vein."""
    _, x, y = e
    if (f // 3) % 2 == 0:
        for dx, dy in ((0, 0), (5, -2)):
            d.line([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=(255, 70, 60))
            d.line([x + dx - 2, y + dy + 2, x + dx + 2, y + dy - 2], fill=(255, 70, 60))

@fx('ts_zzz')
def _fx_zzz(d, im, e, f):
    """Z Z Z over a sleeper (x, y): three letters that rise and fade, back where they started every 40 frames."""
    _, x, y = e
    for k in range(3):
        p = (loop.phase(f, 40) + k / 3) % 1.0
        text(d, 'Z', x + k * 4 + int(p * 3), int(y - p * 12), (200, 220, 255), shadow=None)

# ---- the close-ups -----------------------------------------------------------------------------------------
def _nose(px, cx, cy, tones):
    """A nose: the lit bridge on the left, the shade down the right side, the wings and the nostrils, the tip."""
    for y in range(cy + 2, cy + 9): put_px(px, cx - 1, y, tones[2])
    for y in range(cy + 3, cy + 9): put_px(px, cx + 3, y, tones[0])
    put_px(px, cx + 4, cy + 9, tones[0]); put_px(px, cx + 2, cy + 9, tones[2])
    put_px(px, cx - 3, cy + 10, tones[0]); put_px(px, cx - 2, cy + 10, tones[0])     # the left wing
    put_px(px, cx + 2, cy + 10, tones[0]); put_px(px, cx + 3, cy + 10, tones[0])     # the right wing
    put_px(px, cx - 1, cy + 11, tones[0]); put_px(px, cx + 1, cy + 11, tones[0])     # the nostril shadows

def _cheeks(px, cx, cy, tones, k=0.45):
    """A flush of colour on the cheeks (k: how strong)."""
    for x0 in (cx - 15, cx + 11):
        for dx in range(5):
            for dy in range(2): put_px(px, x0 + dx, cy + 9 + dy, mix_rgb(tones[1], tones[2] if k < 0.5 else (240, 120, 120), k))

def _curl(px, x, y, r, tones):
    """One ringlet of hair: a shaded disc with a dark rim, the light on its upper left."""
    sphere(px, x, y, r, r, tones)

def _tee(d, cx, col, hi, neck):
    """The neck and the shoulders of a t-shirt at the bottom of a close-up, the collar lit."""
    d.rectangle([cx - 6, 52, cx + 6, 60], fill=neck[1]); d.line([cx + 4, 52, cx + 4, 60], fill=neck[0])
    d.polygon([(cx - 30, 64), (cx - 24, 57), (cx - 7, 56), (cx, 60), (cx + 7, 56), (cx + 24, 57), (cx + 30, 64)],
              fill=col, outline=OUT)
    d.line([(cx - 7, 57), (cx, 61), (cx + 7, 57)], fill=hi)

def _eduard(im, t, f):
    """Eduard's face, as the show draws him: the long brown hair down past his shoulders, the fringe swept over
    his right eye, the long pale face, a shadow of beard; the poem read back, his one eye fills with tears."""
    px = im.load(); d = ImageDraw.Draw(im)
    cx, cy = 40, 30
    locks(d, cx - 27, cx - 15, cy - 4, 63, HAIR_E, 1)                            # the hair down both sides, behind
    locks(d, cx + 15, cx + 27, cy - 4, 63, HAIR_E, 2)
    sphere(px, cx, cy - 8, 27, 24, HAIR_E)                                       # the crown
    _tee(d, cx, (32, 32, 36), (70, 70, 78), SKIN_P)
    sphere(px, cx, cy + 4, 19, 25, SKIN_P)                                       # the face, long
    _cheeks(px, cx, cy + 2, SKIN_P, 0.35)
    rr = random.Random(5)                                                         # the stubble on the jaw and lip
    for _ in range(46):
        a = rr.uniform(0.35, math.pi - 0.35); r = rr.uniform(0.8, 0.97)
        put_px(px, cx + math.cos(a) * 19 * r, cy + 4 + math.sin(a) * 25 * r, mix_rgb(SKIN_P[1], HAIR_E[1], 0.3))
    almond_eye(im, cx - 8, cy + 2, 5.5, 4.0, (0.4, 0.3), 0.0, (104, 70, 44), (46, 28, 18), SKIN_P)
    brow(d, (cx - 15, cy - 6), (cx - 3, cy - 9), HAIR_E[0], HAIR_E[2], 2)
    d.polygon([(cx - 22, cy - 18), (cx - 14, cy - 28), (cx, cy - 31), (cx + 14, cy - 29), (cx + 23, cy - 20), (cx + 22, cy + 10), (cx + 16, cy + 9), (cx + 8, cy + 2),
               (cx + 2, cy - 6), (cx - 6, cy - 11), (cx - 18, cy - 11), (cx - 22, cy - 6)], fill=HAIR_E[1])   # the fringe, swept right
    for k in range(11):
        x0 = cx - 18 + k * 4
        strand(d, x0, cy - 28 + abs(x0 - cx) // 3, x0 + 10, cy - 11 + k * 2, 1.6, HAIR_E[2] if k % 3 else HAIR_E[0])
    d.line([(cx - 16, cy - 11), (cx - 6, cy - 11), (cx + 2, cy - 6), (cx + 8, cy + 2), (cx + 16, cy + 9),
            (cx + 22, cy + 10)], fill=OUT)
    _nose(px, cx + 1, cy, SKIN_P)
    _mouth_open(d, cx, cy + 17, (110, 44, 52), (196, 120, 116), (250, 176, 170))
    if t > 0.3:                                                                   # the tears, one from under the fringe
        n = min(14, int((t - 0.3) * 44)); x = cx - 13
        d.line([x, cy + 6, x, cy + 6 + n], fill=(160, 206, 240)); d.point((x, cy + 6 + n), fill=(236, 248, 255))
        put_px(px, cx - 4, cy + 6, (200, 230, 250))
    if t > 0.5:
        n = min(10, int((t - 0.5) * 40)); x = cx + 10
        d.line([x, cy + 10, x, cy + 10 + n], fill=(160, 206, 240)); d.point((x, cy + 10 + n), fill=(236, 248, 255))
    if t > 0.55: spark(d, cx - 10, cy, 2)

def _mouth_open(d, cx, y, inside, upper, lower):
    """A mouth open in surprise: the dark inside, the upper lip in shade, the lower lip lit."""
    d.ellipse([cx - 3, y - 2, cx + 4, y + 3], fill=inside, outline=OUT)
    d.line([cx - 4, y - 3, cx + 5, y - 3], fill=upper)
    d.line([cx - 2, y + 3, cx + 3, y + 3], fill=lower)

def closeup_eduard(t, f):
    """Primer plano: Eduard, the fringe over one eye; someone read his book at last, the tears come."""
    def draw(im, d, t, f):
        soft_glow(im, 40, 26, 58, 52, (200, 140, 70), 0.5); _eduard(im, t, f)
    return closeup(t, f, (30, 22, 40), draw, txt='POR FIN ALGUIEN LO LEYO')

def _adriel(im, t, f):
    """Adriel's face, as the show draws him: the orange curls and the curly sideburns down to the chin, the round
    glasses over big blue eyes, the huge nose; with the rage the brows come down, the teeth bare, a vein beats on
    the temple and the pink goes red. He shakes."""
    px = im.load(); d = ImageDraw.Draw(im)
    sh = round(loop.wave(f, 4) * 1.0)
    cx, cy = 40 + sh, 31
    skin = tuple(tuple(min(255, int(c + (r - c) * min(1, t * 1.6) * 0.35)) for c, r in zip(tone, (255, 60, 60)))
                 for tone in SKIN_P)                                              # pale pink going red
    _tee(d, cx, RED, RED_L, skin)
    sphere(px, cx, cy - 10, 26, 18, GINGER)                                      # the mass of curls
    rr = random.Random(11)
    for k in range(22):                                                           # the ringlets round the top
        a = math.pi + k / 21 * math.pi
        _curl(px, cx + math.cos(a) * 25 + rr.randint(-1, 1), cy - 10 + math.sin(a) * 17 + rr.randint(-1, 1),
              rr.choice((3, 3.5, 4)), GINGER)
    sphere(px, cx, cy + 4, 21, 25, skin)                                         # the face
    for side in (-1, 1):                                                          # the sideburns, curling down the jaw
        for k in range(8):
            a = (0.05 + k / 7 * 0.85) * math.pi / 2
            _curl(px, cx + side * math.cos(a) * 19, cy + 4 + math.sin(a) * 23, 2.6, GINGER)
    for x in range(cx - 5, cx + 6, 3): _curl(px, x, cy + 27, 2.4, GINGER)        # the chin
    for k in range(6):                                                            # a fringe of curls on the forehead
        _curl(px, cx - 15 + k * 6, cy - 14 + (k % 2), 3, GINGER)
    for y in (cy - 7, cy - 5):                                                    # the creases between the brows
        d.line([cx - 3, y, cx + 3, y], fill=skin[0])
    for ex in (cx - 10, cx + 10):                                                 # the glasses: the lens, the eye, the frame
        for y in range(cy - 6, cy + 9):
            for x in range(ex - 8, ex + 9):
                if ((x - ex) / 8.0) ** 2 + ((y - cy - 1) / 7.0) ** 2 <= 1: px[x, y] = mix_rgb(skin[2], LENS, 0.5)
        almond_eye(im, ex, cy + 1, 6.0, 4.6, (0.8 if ex > cx else -0.8, 0.0), 0.3 * min(1, t * 2), (70, 140, 226),
             (24, 64, 140), skin, red=t > 0.4)
        d.ellipse([ex - 8, cy - 6, ex + 8, cy + 8], outline=GLASS_F)
        d.arc([ex - 7, cy - 5, ex + 7, cy + 7], 200, 280, fill=(255, 255, 255))   # the glint on the lens
    d.line([cx - 2, cy, cx + 2, cy], fill=GLASS_F)
    v = int(min(1, t * 2) * 4)                                                    # the brows, coming down into a V
    brow(d, (cx - 18, cy - 9 + v // 2), (cx - 4, cy - 9 + v), GINGER[0], GINGER[2], 3)
    brow(d, (cx + 4, cy - 9 + v), (cx + 18, cy - 9 + v // 2), GINGER[0], GINGER[2], 3)
    sphere(px, cx + 2, cy + 12, 8, 6, skin)                                      # the nose, big and round
    put_px(px, cx - 1, cy + 15, skin[0]); put_px(px, cx + 5, cy + 15, skin[0]); put_px(px, cx - 2, cy + 9, (255, 246, 244))
    d.rectangle([cx - 7, cy + 19, cx + 7, cy + 23], fill=(40, 10, 14), outline=(96, 30, 32))   # the mouth, bared
    d.rectangle([cx - 6, cy + 19, cx + 6, cy + 20], fill=(246, 242, 236))
    for x in range(cx - 4, cx + 6, 3): put_px(px, x, cy + 20, (176, 166, 166))
    d.line([cx - 6, cy + 23, cx + 6, cy + 23], fill=(232, 226, 220))
    if t > 0.25 and (f // 3) % 2 == 0:                                            # the vein, beating
        d.line([(cx - 21, cy - 10), (cx - 18, cy - 5), (cx - 20, cy - 1)], fill=(150, 40, 90))
        d.line([(cx - 18, cy - 5), (cx - 15, cy - 6)], fill=(150, 40, 90))
    if t > 0.5:                                                                   # sweat on the temple
        y = cy - 8 + int((t - 0.5) * 20)
        d.ellipse([cx + 19, y, cx + 21, y + 2], fill=(160, 210, 250)); put_px(px, cx + 19, y, (240, 250, 255))

def closeup_adriel(t, f):
    """Primer plano: Adriel, the curls, the glasses, the nose, the teeth: they laugh at his art."""
    def draw(im, d, t, f):
        soft_glow(im, 40, 30, 60, 56, (210, 60, 40), 0.6); _adriel(im, t, f)
    return closeup(t, f, (56, 18, 22), draw, txt='YO HAGO ARTE, NO COMEDIA!')

def _dios(im, t, f):
    """Dios, as the show draws him: the big bald yellow head with a shine, a black tuft over each ear, the eyes
    half shut, the black horseshoe moustache, the green vest, a cigarette whose smoke curls up."""
    px = im.load(); d = ImageDraw.Draw(im)
    cx, cy = 40, 27
    d.rectangle([cx - 7, 50, cx + 7, 60], fill=SKIN_Y[1]); d.line([cx + 5, 50, cx + 5, 60], fill=SKIN_Y[0])
    d.polygon([(cx - 30, 64), (cx - 26, 58), (cx - 18, 57), (cx - 16, 52), (cx - 12, 52), (cx - 9, 59), (cx + 9, 59),
               (cx + 12, 52), (cx + 16, 52), (cx + 18, 57), (cx + 26, 58), (cx + 30, 64)], fill=(150, 202, 44), outline=OUT)
    d.line([(cx - 9, 60), (cx + 9, 60)], fill=(196, 236, 96))                     # the vest, the collar lit
    for x, y in ((cx - 4, 61), (cx + 2, 62), (cx - 1, 63), (cx + 5, 61)): put_px(px, x, y, (60, 44, 30))   # chest hair
    for side in (-1, 1):                                                          # the tufts, bushy, over the ears
        tx = cx + side * 24
        d.ellipse([tx - 6, cy - 8, tx + 6, cy + 10], fill=TUFT[1], outline=OUT)
        for k in range(7):                                                        # tufts of hair sticking out
            y0 = cy - 6 + k * 2.5
            d.line([tx, y0, tx + side * (8 + (k % 3)), y0 + (k % 2) * 2 - 1], fill=TUFT[0], width=2)
            put_px(px, tx + side * (4 + k % 2), y0 - 1, TUFT[2])
    sphere(px, cx, cy, 25, 25, SKIN_Y)                                           # the head, bald
    d.ellipse([cx - 14, cy - 20, cx - 6, cy - 16], fill=mix_rgb(SKIN_Y[2], (255, 255, 255), 0.5))   # the shine
    put_px(px, cx - 4, cy - 19, (255, 255, 255))
    for side in (-1, 1):
        ex = cx + side * 10
        almond_eye(im, ex, cy, 6.0, 3.0, (0.5 * side, 0.6), 0.55, (90, 60, 36), (40, 24, 14), SKIN_Y, lash=False)
        d.line([ex - 7, cy - 1, ex + 7, cy - 1], fill=OUT)                        # the heavy lid
        d.line([ex - 6, cy - 5, ex + 6, cy - 6 if side < 0 else cy - 5], fill=SKIN_Y[0])   # the brow ridge
    d.line([(cx + 1, cy + 1), (cx - 4, cy + 10), (cx + 2, cy + 10)], fill=mix_rgb(SKIN_Y[0], OUT, 0.4))   # the nose
    d.line([(cx - 10, cy + 25), (cx - 10, cy + 17), (cx - 6, cy + 13), (cx + 6, cy + 13), (cx + 10, cy + 17),
            (cx + 10, cy + 25)], fill=TUFT[0], width=4)                           # the horseshoe moustache
    d.line([(cx - 5, cy + 12), (cx + 5, cy + 12)], fill=TUFT[2])
    d.line([(cx - 4, cy + 18), (cx + 4, cy + 18)], fill=mix_rgb(SKIN_Y[0], OUT, 0.3))   # the mouth, flat
    d.line([cx + 3, cy + 18, cx + 13, cy + 22], fill=(246, 246, 240), width=2)    # the cigarette
    ember = (255, 200, 80) if (f // 4) % 2 else (255, 110, 40)
    d.rectangle([cx + 13, cy + 21, cx + 14, cy + 23], fill=ember)
    for i in range(9):                                                            # the smoke, curling up
        y = cy + 20 - i * 3 - int(t * 6) % 3
        x = cx + 14 + round(math.sin(i * 0.9 + t * 6) * 2)
        put_px(px, x, y, mix_rgb((200, 200, 210), im.getpixel((x, y)), i / 10))

def closeup_dios(t, f):
    """Primer plano: Dios, asked the meaning of life, gives it a drag: NI IDEA. PREGUNTENLE A CLAUDE."""
    def draw(im, d, t, f):
        soft_glow(im, 40, 30, 60, 58, (240, 200, 100), 0.7); _dios(im, t, f)
    return closeup(t, f, (34, 26, 40), draw, txt='NI IDEA. PREGUNTENLE A CLAUDE')

# ---- the clips ------------------------------------------------------------------------------------------------
def _say(s, f, t0, t1, lines, cx, y, tail=None):
    """A speech bubble from frame t0 to t1 (engine/people.py's 'bubble' effect)."""
    if t0 <= f < t1: s['fx'].append(('bubble', lines, cx, y, tail))

def clip_poema(f):
    f = loop.frame(f)
    s = scene(f, THEME)
    if 176 <= f < 236: s['image'] = closeup_eduard((f - 176) / 60, f); return s
    reading = 50 <= f < 176
    cl = claude('armsup' if 150 <= f < 176 else 'guard' if reading else guard_pose(f))
    ed = 'reach' if 34 <= f < 50 else 'cheer' if 236 <= f < 250 else 'stand'
    s['actors'] = [cl, man(ADRIEL, 'cheer' if 250 <= f < 280 else 'guard', AX, APAL, flip=True),
                   man(EDUARD, ed, EX, EPAL), man(JAIQUE, 'stand', JX, JPAL, flip=True)]
    s['fx'].insert(0, ('ts_couch',))
    if reading and f < 150: s['fx'].append(('ts_book', CX + 7, 50))
    for i, line in enumerate(("EL MATE SE ENFRIA", "MIENTRAS TE ESPERO", "Y NO ME IMPORTA")):   # Claude reads it out
        t0 = 56 + i * 30
        if t0 <= f < t0 + 30: s['fx'].append(('caption', line))
    _say(s, f, 14, 50, ["CLAUDE, QUERES LEER", "MI LIBRO DE POEMAS?"], EX + 20, 4, EX)
    _say(s, f, 148, 176, ["SOBRIO, SIN PARAFERNALIA.", "ES MUY BUENO, EDU"], CX, 4, CX)
    _say(s, f, 248, 280, ["Y MI CANAL DE", "YOUTUBE, QUE?"], AX, 4, AX)
    return s

def clip_fristail(f):
    f = loop.frame(f)
    s = scene(f, THEME)
    if 140 <= f < 186: s['image'] = closeup_adriel((f - 140) / 46, f); return s
    rap = 16 <= f < 76
    ad_pose = 'cheer' if rap or 104 <= f < 140 else 'guard'
    s['actors'] = [claude(('armsup' if (f // 6) % 2 else 'guard') if rap else guard_pose(f) if f < 186 else 'guard', CX),
                   man(ADRIEL, ad_pose, AX, APAL, flip=True), man(EDUARD, 'stand', EX, EPAL),
                   man(JAIQUE, 'stand', JX, JPAL, flip=True)]
    if 186 <= f < 238:                                                           # Berna comes in from the left
        if f < 200: bx, pose, flip = ez(-14, 112, (f - 186) / 14), ('walk1' if (f // 4) % 2 else 'walk2'), False
        elif f < 226: bx, pose, flip = 112, 'point', True
        else: bx, pose, flip = ez(112, -14, (f - 226) / 12), ('walk1' if (f // 4) % 2 else 'walk2'), True
        s['actors'].append(man(BERNA, pose, bx, BPAL, flip=flip))
    s['fx'].insert(0, ('ts_couch',))
    if rap:                                                                      # the rap, the beat Claude makes for it
        hx, hy = figure_point(ADRIEL, POSES['cheer'], 'hand', AX, GROUND, flip=True)
        s['fx'] += [('ts_mic', hx, hy), ('ts_notes', AX, 30), ('ts_beat', CX, 32)]
        s['fx'].append(('caption', "TODO CARO, TODO CARO" if f < 46 else "HASTA EL CHINO ESTA CARO"))
    if 200 <= f < 226: s['fx'].append(('ts_rage', AX + 12, 30))
    _say(s, f, 76, 104, ["ES UN POCO", "REPETITIVO, COLORADO"], JX - 10, 4, JX)
    _say(s, f, 104, 140, ["LO SUBI: 700 VISITAS", "Y TODOS SE MATAN DE RISA"], CX + 10, 4, CX)
    _say(s, f, 200, 226, ["BUEN LABURAR NUNCA,", "NO? MEDIOCRE"], 112, 4, 112)
    return s

def clip_sentido(f):
    f = loop.frame(f)
    s = scene(f, THEME)
    if 160 <= f < 210: s['image'] = closeup_dios((f - 160) / 50, f); return s
    shut = 250 <= f < 290
    jq = man(JAIQUE, 'stand', JX, JPAL, flip=True, shut=shut)
    s['actors'] = [claude('armsup' if 62 <= f < 100 else guard_pose(f), CX), man(ADRIEL, 'guard', AX, APAL, flip=True),
                   man(EDUARD, 'stand', EX, EPAL), jq]
    if 100 <= f < 236:                                                           # Dios, on a cloud, down and up again
        if f < 120: dy = ez(-14, 36, (f - 100) / 20)
        elif f < 210: dy = 36
        else: dy = ez(36, -14, (f - 210) / 25)
        if dy > -10:
            s['actors'].append(man(DIOS, 'stand', 112, DPAL_, y=int(dy)))
            s['fx'].append(('ts_cloud', 112, int(dy) + 2))
    s['fx'].insert(0, ('ts_couch',))
    if 250 <= f < 290: s['fx'].append(('ts_zzz', JX + 10, 30))
    _say(s, f, 20, 60, ["CLAUDE, CHE...", "CUAL ES EL SENTIDO", "DE LA VIDA?"], JX, 2, JX)
    _say(s, f, 62, 100, ["TENER BUENA BANDA", "Y UN BUEN MATE"], CX, 4, CX)
    _say(s, f, 124, 160, ["JA! ESA ERA", "MI PREGUNTA, CHE"], 96, 2, 112)
    _say(s, f, 214, 250, ["ENTONCES ME VOY", "A DORMIR, CHE"], JX, 2, JX)
    return s

CLIPS = [clip('poema', N1, clip_poema),
         clip('fristail', N2, clip_fristail),
         clip('sentido', N1, clip_sentido)]
