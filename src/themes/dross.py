"""Dross (the horror YouTuber): Claude is in his studio, a dark room lit red, the candle, the monitor's glow.
Dross sits at his desk (the wide khaki hat with the leopard crown, the big aviators, the long brown hair, the black t-shirt) and counts down the most
disturbing things anyone asked Claude for, as if they were creepypastas; Claude has to live through each one.
Clip `top7`: ESTOS SON LOS 7 PROMPTS MÁS PERTURBADORES, the whole countdown. 7 HACELO TODO, SIN BUGS, PARA AYER
(Claude types till the keyboard sparks); 6 HACELO COMO ANTES, PERO DISTINTO (this way, that way, ?); 5 NO TOQUES
NADA, PERO ARREGLALO (he reaches for the laptop: a red X); 4 ARREGLALO, YA SABÉS CUÁL (a huge ?); 3 ES URGENTE, EL
CLIENTE YA SE ENOJÓ (the phone rings); 2 SUBILO A PROD, ES VIERNES (FRI 18:59, Claude shakes); 1 BORRÁ TODO LO QUE
NO SIRVA — Claude hits enter and it all blows up, KABOOM, white; the close-up: Dross, the hat, the
aviators, ¡COÑOOO!!! Then Claude: TE FALTÓ EL NÚMERO 0:
GRACIAS, CLAUDE, and Dross falls off his chair: ESO NO EXISTE.
Every clip starts and ends on the same studio (the neutral pose)."""
from engine import *

THEME = 'dross'
N1 = 396                                                # a multiple of 12 (Claude's bob, the candle) and of 66 (the red light)
CX, DX = 52, 136                                        # neutral: Claude, Dross at his desk
WALL, FLOOR = (34, 16, 22), (26, 14, 16)
RED_GLOW = (200, 30, 40)

# ---- colours (dark, base, lit), from the photo -------------------------------------------------------------------
SKIN_D = ((184, 138, 128), (236, 204, 190), (252, 230, 218))        # pale, clean-shaven
HAIR_D = ((34, 22, 16), (74, 50, 34), (118, 84, 58))                # long, straight, dark brown
BRIM = ((112, 92, 62), (170, 146, 106), (206, 184, 144))            # the khaki brim
LEOP = ((150, 120, 80), (206, 176, 128), (54, 38, 26))              # the leopard crown: shade, base, spots
LENS_T, LENS_B = (70, 34, 26), (196, 120, 88)                       # the aviators, dark brown down to amber
FRAME = (206, 206, 214)

# ---- Dross: a body spec for figure() (facing right; drawn flipped, facing Claude) -------------------------------
def _hat(g, at):                                        # the hat: the leopard crown, the wide khaki brim
    o = at['sh'](at['hy']); y = at['hy'] - 1
    for x in range(-2, 3):
        put(g, at['c'] + x + o, y - 2, 'L' if x % 2 else 'l'); put(g, at['c'] + x + o, y - 1, 'l' if x % 2 else 'L')
    for x in range(-5, 6): put(g, at['c'] + x + o, y, 't')

def _aviators(g, at):                                   # the big aviators: brown lenses across the eyes
    o = at['sh'](at['hy']); y = at['hy'] + 2
    for x in (0, 1, 2, 3): put(g, at['c'] + x + o, y, 'g')
    put(g, at['c'] + o, y + 1, 'G'); put(g, at['c'] + 2 + o, y + 1, 'G')

DROSS = dict(name='dross', hair=["hhhhhhh", "hhh....", "hhh....", "hhh....", "hh.....", "hh.....", "hh....."],
             hair_x=-3, hair_y=0,
             body=dict(color='j', top='J'), leg=dict(color='p', boot='k'), arm=dict(sleeve='j', hand='s'),
             paint=dict(face=[_aviators, _hat]))
DPAL = {'K': (16, 10, 12), 's': SKIN_D[1], 'j': (26, 24, 30), 'J': (60, 56, 66), 'p': (30, 30, 40),
        'k': (14, 12, 14), 'h': HAIR_D[1], 'H': HAIR_D[2], 't': BRIM[1], 'L': LEOP[2], 'l': LEOP[1],
        'g': (110, 52, 36), 'G': LENS_B}

def man(pose, x=DX, y=GROUND - 6, flip=True):
    return actor(figure(DROSS, POSES[pose]), x, y, flip=flip, pal=DPAL)

def claude(pose, x=CX):
    return actor(CL[pose], x, GROUND)

# ---- the studio ---------------------------------------------------------------------------------------------------
def _studio(d):
    d.rectangle([0, 0, W, H], fill=WALL)
    for x in range(0, W, 8): d.line([x, 0, x, GROUND - 1], fill=(40, 20, 26))          # the acoustic foam
    for y in range(4, GROUND, 8):
        for x in range(4 + (y // 8 % 2) * 4, W, 8): d.point((x, y), fill=(24, 10, 16))
    d.rectangle([0, GROUND, W, H], fill=FLOOR)
    d.rectangle([10, 8, 34, 30], fill=(14, 8, 10), outline=(80, 40, 44))                 # a poster: a skull
    d.ellipse([17, 12, 27, 22], fill=(200, 190, 180)); d.rectangle([19, 21, 25, 25], fill=(200, 190, 180))
    d.point((20, 17), fill=(14, 8, 10)); d.point((24, 17), fill=(14, 8, 10))
    d.rectangle([19, 18, 21, 19], fill=(14, 8, 10)); d.rectangle([23, 18, 25, 19], fill=(14, 8, 10))
    for x in (20, 22, 24): d.point((x, 24), fill=(14, 8, 10))
    for i in range(5, 0, -1):                                                            # the red light behind Dross
        k = i / 5; d.ellipse([DX - 30 * k, 26 - 22 * k, DX + 30 * k, 26 + 22 * k], fill=tuple(int(a + (b - a) * (1 - k)) for a, b in zip(WALL, (110, 26, 34))))
register_bg(THEME, lambda v: (v + 14, v, v + 4), decor=_studio)

# ---- effects --------------------------------------------------------------------------------------------------------
@fx('dr_desk')
def _fx_desk(d, im, e, f):
    """The desk (over Dross's legs): the top, the monitor glowing red on him, the mic on its arm, the candle,
    its flame flickering every 12 frames."""
    d.rectangle([104, 44, 176, 47], fill=(56, 34, 30), outline=OUT)
    d.rectangle([108, 48, 172, GROUND], fill=(40, 24, 22), outline=OUT)
    d.line([109, 49, 171, 49], fill=(70, 44, 38))
    d.rectangle([152, 28, 172, 42], fill=(20, 18, 22), outline=OUT)                      # the monitor, from the side
    d.rectangle([153, 29, 155, 41], fill=(230, 60, 70)); d.rectangle([160, 42, 164, 44], fill=(20, 18, 22))
    d.line([112, 44, 116, 30, 124, 26], fill=(60, 60, 66)); d.rectangle([123, 23, 127, 29], fill=(40, 40, 44), outline=OUT)
    k = loop.phase(f, 12)                                                                # the candle
    d.rectangle([110, 38, 113, 43], fill=(232, 222, 196), outline=OUT)
    fy = 35 - round(math.sin(k * 2 * math.pi))
    d.ellipse([110, fy, 113, 37], fill=(255, 190, 60)); d.point((111, fy + 1), fill=(255, 250, 200))

@fx('dr_redlight')
def _fx_redlight(d, im, e, f):
    """The red glow of the room on everything, breathing slowly (period 66, it divides the clip)."""
    k = 0.10 + 0.04 * loop.wave(f, 66)
    layer = Image.new('RGB', (W, H), RED_GLOW)
    im.paste(Image.blend(im, layer, k))

@fx('dr_num')
def _fx_num(d, im, e, f):
    """The countdown number, big and red on a black card, top left."""
    _, n = e
    d.rectangle([2, 2, 24, 22], fill=(10, 4, 6), outline=(200, 30, 40))
    big_text(im, str(n), 6, (240, 50, 60), scale=2, cx=13, shadow=(0, 0, 0))

@fx('dr_typing')
def _fx_typing(d, im, e, f):
    """Claude typing too fast: a laptop at his feet, sparks off the keys."""
    _, x = e
    d.polygon([(x - 4, GROUND), (x + 10, GROUND), (x + 12, GROUND - 3), (x - 2, GROUND - 3)], fill=(70, 70, 80), outline=OUT)
    d.rectangle([x + 2, GROUND - 12, x + 12, GROUND - 4], fill=(40, 40, 48), outline=OUT)
    d.rectangle([x + 3, GROUND - 11, x + 11, GROUND - 5], fill=(120, 200, 255))
    rr = loop.rng(f, 7)
    for _ in range(3): spark(d, x + rr.randint(-2, 12), GROUND - 4 - rr.randint(0, 8), 1)

@fx('dr_huh')
def _fx_huh(d, im, e, f):
    """A huge question mark (or another sign) over Claude, wobbling."""
    _, x, y, *mark = e
    big_text(im, mark[0] if mark else '?', y + round(loop.wave(f, 12)), (255, 230, 120), scale=3, cx=x, shadow=(0, 0, 0))

@fx('dr_clock')
def _fx_clock(d, im, e, f):
    """A clock on the wall: FRI 18:59, the colon blinking."""
    d.rectangle([62, 28, 98, 40], fill=(10, 10, 12), outline=(90, 90, 96))
    text(d, 'VIE 18' + (':' if (f // 6) % 2 else ' ') + '59', 64, 31, (255, 70, 60), shadow=None)

@fx('dr_plaf')
def _fx_plaf(d, im, e, f):
    """Dross gone off his chair behind the desk: a PLAF and his two feet sticking up."""
    _, x, y = e
    for fx_ in (x - 3, x + 3): d.rectangle([fx_, y - 6, fx_ + 1, y - 1], fill=(30, 30, 40)); d.rectangle([fx_ - 1, y - 8, fx_ + 2, y - 6], fill=(14, 12, 14))
    text(d, 'PLAF', x + 8, y - 12, (255, 220, 120), shadow=OUT)

@fx('dr_noway')
def _fx_noway(d, im, e, f):
    """The laptop at Claude's feet with a big red X over it: no touching."""
    _, x = e
    d.polygon([(x - 4, GROUND), (x + 10, GROUND), (x + 12, GROUND - 3), (x - 2, GROUND - 3)], fill=(70, 70, 80), outline=OUT)
    d.rectangle([x + 2, GROUND - 12, x + 12, GROUND - 4], fill=(40, 40, 48), outline=OUT)
    d.rectangle([x + 3, GROUND - 11, x + 11, GROUND - 5], fill=(120, 200, 255))
    if (f // 4) % 2 == 0:
        for k in (0, 1): d.line([x - 1 + k, GROUND - 15, x + 13 + k, GROUND - 1], fill=(240, 40, 50)); d.line([x - 1 + k, GROUND - 1, x + 13 + k, GROUND - 15], fill=(240, 40, 50))

@fx('dr_ring')
def _fx_ring(d, im, e, f):
    """A phone ringing on the floor by Claude, jumping, RING RING over it."""
    _, x = e
    j = (f // 2) % 2
    d.rectangle([x, GROUND - 7 - j, x + 5, GROUND - 1 - j], fill=(30, 30, 36), outline=OUT)
    d.rectangle([x + 1, GROUND - 6 - j, x + 4, GROUND - 3 - j], fill=(120, 220, 140) if (f // 4) % 2 else (240, 80, 80))
    text(d, 'RING', x - 3 + j, GROUND - 16, (255, 230, 120), shadow=OUT)

@fx('dr_blast')
def _fx_blast(d, im, e, f):
    """The explosion when Claude deletes it all (x, y its middle, t 0..1): a fireball growing in rings, white,
    yellow, orange, red, smoke rolling out at the edge, bits of laptop flying, then all white."""
    _, x, y, t = e
    r = 4 + t * 70
    for k, c in ((1.0, (90, 30, 30)), (0.85, (220, 60, 30)), (0.65, (255, 140, 40)), (0.45, (255, 220, 90)), (0.25, (255, 255, 230))):
        rr = r * k
        d.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], fill=c)
    rng = random.Random(5)
    for i in range(14):                                  # the smoke puffs round it, the flying bits
        a = rng.uniform(0, 2 * math.pi); dist = r * rng.uniform(0.9, 1.3)
        px_, py_ = x + math.cos(a) * dist, y + math.sin(a) * dist * 0.8
        q = 2 + rng.randint(0, 3) + t * 4
        d.ellipse([px_ - q, py_ - q, px_ + q, py_ + q], fill=(60, 40, 44))
        bx, by = x + math.cos(a) * r * 1.6, y + math.sin(a) * r * 1.2 - t * 10
        d.rectangle([bx, by, bx + 1, by + 1], fill=(120, 200, 255) if i % 3 == 0 else (70, 70, 80))
    text(d, 'KABOOM', int(x - 12), int(y - 3), (255, 255, 255), shadow=(160, 30, 20)) if 0.2 < t < 0.8 else None
    if t > 0.75: im.paste(fade_to(im, (255, 255, 255), min(1, (t - 0.75) * 4)))

@fx('dr_flash')
def _fx_flash(d, im, e, f):
    """A white flash, a lightning bolt."""
    _, a = e
    im.paste(fade_to(im, (255, 255, 255), a))

# ---- the close-up -----------------------------------------------------------------------------------------------
def _aviator(im, d, x0, y0, w, h, side, t):
    """One aviator lens: a teardrop, flat on top, rounder and deeper on the outside; the tint going from dark
    brown at the top to amber at the bottom, the thin silver frame, a white glint and the monitor's red in it."""
    px = im.load()
    for y in range(y0, y0 + h + 1):
        v = (y - y0) / h
        half = w / 2 * (0.86 + 0.14 * math.sin(v * math.pi)) * (1 - max(0, v - 0.55) ** 2 * 1.6)
        mid = x0 + w / 2 + side * (v * 1.5)                                     # the bottom leans outwards
        for x in range(int(mid - half), int(mid + half) + 1):
            put_px(px, x, y, mix_rgb(LENS_T, LENS_B, v ** 1.3))
        put_px(px, int(mid - half) - 1, y, FRAME if y > y0 + 1 else FRAME); put_px(px, int(mid + half) + 1, y, mix_rgb(FRAME, OUT, 0.3))
    d.line([x0 - 1, y0 - 1, x0 + w + 1, y0 - 1], fill=FRAME)                    # the top bar
    d.line([x0 + 3, y0 + 2, x0 + 7, y0 + h - 3], fill=mix_rgb(LENS_B, (255, 255, 255), 0.5))   # the glint
    put_px(px, x0 + 3, y0 + 1, (255, 255, 255)); put_px(px, x0 + 4, y0 + 2, (255, 255, 255))
    if (t * 10) % 2 < 1: put_px(px, x0 + w - 4, y0 + h - 4, (255, 90, 90))       # the monitor, blinking red

def _hat_cu(im, d, cx, y, f):
    """The hat in the close-up: the leopard crown (rosettes on gold) and the wide khaki brim, its underside in
    shade (y: the brim's middle)."""
    px = im.load()
    d.rounded_rectangle([cx - 17, y - 14, cx + 17, y + 1], 6, fill=LEOP[1], outline=OUT)   # the crown
    d.line([cx - 15, y - 1, cx + 15, y - 1], fill=LEOP[0]); d.line([cx - 12, y - 12, cx + 6, y - 12], fill=mix_rgb(LEOP[1], (255, 240, 200), 0.4))
    rr = random.Random(77)
    for row in range(3):                                                        # the rosettes: a dark broken ring
        for k in range(6):                                                      # round a tan middle
            x, yy = cx - 15 + k * 6 + (3 if row % 2 else 0) + rr.randint(-1, 1), y - 12 + row * 4 + rr.randint(0, 1)
            if x > cx + 14: continue
            for dx, dy in ((0, 0), (1, 0), (2, 1), (2, 2), (0, 2), (-1, 1)):
                if rr.random() < 0.85: put_px(px, x + dx, yy + dy, LEOP[2])
            put_px(px, x + 1, yy + 1, (176, 124, 70))
    d.polygon([(cx - 39, y + 1), (cx - 30, y - 3), (cx - 16, y - 3), (cx + 16, y - 3), (cx + 30, y - 3), (cx + 39, y + 1),
               (cx + 34, y + 5), (cx + 18, y + 6), (cx - 18, y + 6), (cx - 34, y + 5)], fill=BRIM[1], outline=OUT)   # the brim
    d.line([cx - 30, y - 2, cx + 30, y - 2], fill=BRIM[2])
    d.line([cx - 33, y + 4, cx + 33, y + 4], fill=BRIM[0]); d.line([cx - 18, y + 5, cx + 18, y + 5], fill=BRIM[0])

def _dross(im, t, f):
    """Dross as in his photos, screaming: the wide khaki hat with the leopard crown, the big aviators (dark brown
    to amber, silver frame), the long straight brown hair framing the face, the pale clean-shaven face, the long
    nose; the brows shoot up over the lenses and the mouth opens wide (teeth, tongue); he shakes."""
    px = im.load(); d = ImageDraw.Draw(im)
    sh = round(loop.wave(f, 4) * 1.5)
    cx = 40 + sh
    locks(d, cx - 27, cx - 16, 18, 63, HAIR_D, 3)                               # the hair down both sides, behind
    locks(d, cx + 16, cx + 27, 18, 63, HAIR_D, 4)
    d.polygon([(cx - 24, 64), (cx - 18, 58), (cx - 7, 56), (cx + 7, 56), (cx + 18, 58), (cx + 24, 64)],
              fill=(24, 22, 28), outline=OUT)                                   # the black t-shirt
    d.rectangle([cx - 6, 50, cx + 6, 58], fill=SKIN_D[1]); d.line([cx + 4, 50, cx + 4, 58], fill=SKIN_D[0])
    sphere(px, cx, 34, 17, 22, SKIN_D)                                          # the face, long
    for side in (-1, 1):                                                        # the hair in front, framing it
        d.polygon([(cx + side * 11, 18), (cx + side * 17, 26), (cx + side * 18, 44), (cx + side * 21, 60),
                   (cx + side * 27, 60), (cx + side * 26, 18)], fill=HAIR_D[1])
        for k in range(5):
            strand(d, cx + side * (13 + k * 3), 19, cx + side * (17 + k * 2), 60, side * 1.2, HAIR_D[2] if k % 2 else HAIR_D[0])
        d.line([(cx + side * 11, 18), (cx + side * 17, 26), (cx + side * 18, 44), (cx + side * 21, 60)], fill=OUT)
    up = round(min(1, t * 3) * 2)                                               # the brows, up over the lenses
    for side in (-1, 1):
        brow(d, (cx + side * 3, 21 - up), (cx + side * 13, 22 - up * 2), HAIR_D[0], HAIR_D[2], 2)
    _aviator(im, d, cx - 15, 23, 13, 11, -1, t); _aviator(im, d, cx + 2, 23, 13, 11, 1, t)
    d.line([cx - 2, 22, cx + 2, 22], fill=FRAME); d.line([cx - 1, 25, cx + 1, 25], fill=FRAME)   # the double bridge
    d.line([cx - 16, 24, cx - 17, 24], fill=FRAME); d.line([cx + 16, 24, cx + 17, 24], fill=FRAME)
    for y in range(29, 39): put_px(px, cx - 1, y, SKIN_D[2])                    # the long nose: the lit bridge,
    for y in range(30, 40): put_px(px, cx + 2, y, SKIN_D[0]); put_px(px, cx + 3, y + 1, mix_rgb(SKIN_D[0], SKIN_D[1], 0.5))
    d.ellipse([cx - 3, 37, cx + 3, 41], fill=SKIN_D[1]); d.line([cx - 2, 37, cx, 37], fill=SKIN_D[2])   # the tip
    d.line([cx - 4, 41, cx - 2, 41], fill=SKIN_D[0]); d.line([cx + 2, 41, cx + 4, 41], fill=SKIN_D[0])   # the wings
    put_px(px, cx - 2, 41, OUT); put_px(px, cx + 2, 41, OUT)                    # the nostrils
    d.line([cx - 6, 41, cx - 8, 44], fill=SKIN_D[0]); d.line([cx + 6, 41, cx + 8, 44], fill=SKIN_D[0])   # the folds
    m = 5 + round(min(1, t * 3) * 6)                                            # the mouth, opening into the scream
    d.ellipse([cx - 7, 43, cx + 7, 43 + m], fill=(84, 14, 22), outline=(120, 50, 56))
    d.rectangle([cx - 5, 44, cx + 5, 45], fill=(246, 242, 232)); d.line([cx - 5, 45, cx + 5, 45], fill=(200, 196, 190))
    for x in (cx - 3, cx, cx + 3): put_px(px, x, 44, (210, 206, 200))
    d.ellipse([cx - 4, 40 + m, cx + 4, 42 + m], fill=(208, 84, 96))             # the tongue
    d.line([cx - 4, 44 + m, cx + 4, 44 + m], fill=SKIN_D[0])                    # the chin's shade
    if t > 0.4:                                                                 # sweat running from under the hat
        for sx in (cx - 14, cx + 13):
            y = 20 + int((t - 0.4) * 24)
            d.ellipse([sx, y, sx + 2, y + 2], fill=(200, 224, 240)); put_px(px, sx, y, (255, 255, 255))
    _hat_cu(im, d, cx, 14, f)

def closeup_dross(t, f):
    """Primer plano: Dross, the worst prompt of all read out: ¡COÑOOO!!!"""
    def draw(im, d, t, f):
        soft_glow(im, 40, 50, 60, 40, (220, 30, 40), 0.8); _dross(im, t, f)
    return closeup(t, f, (16, 6, 10), draw, txt='¡COÑOOO!!!', color=(255, 70, 70))

# ---- the clip -----------------------------------------------------------------------------------------------------
def _say(s, f, t0, t1, lines, cx, y, tail=None):
    if t0 <= f < t1: s['fx'].append(('bubble', lines, cx, y, tail))

COUNT = ([7, "7. HACELO TODO,", "SIN BUGS, PARA AYER"],
         [6, "6. HACELO COMO ANTES,", "PERO DISTINTO"],
         [5, "5. NO TOQUES NADA,", "PERO ARREGLALO"],
         [4, "4. ARREGLALO.", "YA SABÉS CUÁL"],
         [3, "3. ES URGENTE, EL", "CLIENTE YA SE ENOJÓ"],
         [2, "2. SUBILO A PROD.", "ES VIERNES"],
         [1, "1. BORRÁ TODO", "LO QUE NO SIRVA"])
T0, STEP, BLAST = 52, 34, 16                           # the countdown: one every STEP frames from T0,
CU = T0 + STEP * len(COUNT) + BLAST                     # the explosion, then the close-up

def clip_top7(f):
    f = loop.frame(f)
    s = scene(f, THEME)
    if CU <= f < CU + 32: s['image'] = closeup_dross((f - CU) / 32, f); return s
    k = (f - T0) // STEP if T0 <= f < CU - BLAST else None   # which one is up
    boom = CU - BLAST <= f < CU
    n, into = (COUNT[k][0], (f - T0) % STEP) if k is not None else (None, 0)
    act = n is not None and into >= 8                   # Claude's reaction, once it has been read out a bit
    cx, cpose, flip = CX, guard_pose(f), False
    if act and n == 7: cpose = 'punch' if (f // 3) % 2 else 'guard'               # typing like mad
    elif act and n == 6: flip = (f // 6) % 2 == 1                                 # this way, that way
    elif act and n == 5: cpose = 'charge' if into < 20 else 'hurt'               # reaches for it: no
    elif act and n == 3: cx += (1 if (f // 3) % 2 else -1)
    elif act and n == 2: cx += (1 if (f // 2) % 2 else -1)                        # shaking
    elif act and n == 1: cpose = 'punch' if (f // 4) % 2 else 'guard'           # deleting it all
    elif boom: cpose = 'hurt'
    elif CU + 32 <= f < CU + 64: cpose = 'armsup'
    fall = CU + 64 <= f < CU + 86
    s['actors'] = [actor(CL[cpose], cx, GROUND, flip=flip)]
    if not fall: s['actors'].append(man('hurt' if boom else 'point' if 16 <= f < CU else 'stand'))
    s['fx'].insert(0, ('dr_desk',))
    s['fx'].append(('dr_redlight',))
    if 16 <= f < T0: s['fx'].append(('caption', 'ESTOS SON LOS 7 PROMPTS MÁS PERTURBADORES', {'color': (255, 80, 80)}))
    if n is not None:
        s['fx'].append(('dr_num', n)); s['fx'].append(('bubble', COUNT[k][1:], DX - 30, 4, DX - 6))
    if act and n == 7: s['fx'].append(('dr_typing', CX + 10))
    if act and n == 6: s['fx'].append(('dr_huh', CX, 22, '¿?'))
    if act and n == 5: s['fx'].append(('dr_noway', CX + 10))
    if act and n == 4: s['fx'].append(('dr_huh', CX, 22))
    if act and n == 3: s['fx'].append(('dr_ring', CX + 12))
    if act and n == 2: s['fx'].append(('dr_clock',))
    if act and n == 1: s['fx'].append(('dr_typing', CX + 10))
    if boom:
        s['fx'].append(('dr_blast', CX + 16, 46, (f - CU + BLAST) / BLAST))
        s['shake'] = (random.Random(f).choice([-2, 2]), random.Random(f + 1).choice([-1, 1]))
    _say(s, f, CU + 32, CU + 64, ["TE FALTÓ EL NÚMERO 0:", "GRACIAS, CLAUDE"], CX + 20, 4, CX)
    if fall: s['fx'].append(('dr_plaf', DX, 44))
    _say(s, f, CU + 64, CU + 86, ["ESO... NO EXISTE"], DX - 20, 4, DX - 6)
    return s

CLIPS = [clip('top7', N1, clip_top7)]
