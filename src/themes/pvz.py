"""Plants vs. Zombies: Claude as Crazy Dave (a saucepan on his head, a scruffy beard) defends his front
lawn, by the porch and the lawn mower, with a sunflower and a peashooter; Codex is Dr. Zomboss.
Suns fall and Claude grabs them (the seed bank counts them); he plants a wall-nut. A HUGE WAVE OF
ZOMBIES IS APPROACHING!: a zombie loses its arm and then its head to the peas, a conehead its cone, a
buckethead keeps coming. They chew the wall-nut — close-up: CHOMP, the cracks, its scared eyes.
Claude lobs a cherry bomb: KABOOM, two piles of ash and a bucket. The ground shakes: DR. CODEX stomps
in on the Zombot and types > RM -RF LAWN; the Zombot hurls an imp over the plants and THE ZOMBIES ATE
YOUR BRAINS! starts to spell out — struck through: Claude jumps on the lawn mower, mows the imp and
rams the Zombot, which blows apart and flings Codex off the screen. Close-up: BECAUSE IM CRAAAZY!;
the reward card, YOU GOT A NEW PLANT! (the Claudeshooter); back to the lawn's neutral pose."""
from engine import *

THEME = 'pvz'
N_ = 420
CX = 26                                   # Claude by the porch in the neutral pose
MOWER_X = 9
SUNF_X, PEA_X, NUT_X, CHERRY_X = 44, 60, 96, 113
NUT_STOP = NUT_X+11                       # where the conehead stops to chew the wall-nut
ZB_X = 160                                # the Zombot once it has stomped in
HUD = (6, 5)                              # the sun counter in the seed bank

# ---- Claude as Crazy Dave: the saucepan (handle to the front) and a scruffy beard ---------------
POT = ["..111111....", ".11111111333", ".22222222..."]
DPAL = {'1':(200,204,214), '2':(128,132,146), '3':(70,72,84), '4':(96,64,44)}

def _dave(spr):
    s = overlay(spr, POT, -1, 0)
    return recolor_rows(s, lambda x,y,t,l,r,c: '4' if c=='O' and y in (t+4,t+5) and x>=l+3 and (x+y)%2==0 else None)
DAVE = variant(_dave)

# ---- the plants ----------------------------------------------------------------------------------
PPAL = {'a':(252,214,40), 'f':(252,170,60), 'G':(112,192,84), 'g':(52,118,44), 'L':(96,176,66),
        'l':(46,108,40), 'K':(24,14,12), 'W':(250,250,250), 'n':(198,150,92), 'N':(146,100,56),
        'c':(70,44,24), 'r':(222,40,40), 'R':(140,20,24)}
SUNFLOWER = S([
"...a.a.a...",
".aaaaaaaaa.",
"aaafffffaaa",
".afKfffKfa.",
"aafffffffaa",
".affKKKffa.",
"aaafffffaaa",
".aaaaaaaaa.",
"...a.l.a...",
".....l.....",
"LL...l..LL.",
".LLL.l.LLL.",
"..LLLlLLL..",
".....l....."])
SUNFLOWER2 = S([('.'+r[:-1]) if i < 9 else r for i, r in enumerate(SUNFLOWER)])   # the head sways
PEASHOOTER = S([
"..gGGGG........",
".gGGGGGGG..ggg.",
"gGGGGGKGGGGGgKg",
"gGGGGGKGGGGGgKg",
"gGGGGGGGGGGGgKg",
".gGGGGGGG..ggg.",
"..gGGGGg.......",
"....ll.........",
"....l..........",
"LL..l..LL......",
".LLLlLLL.......",
"..LLlLL........",
"....l.........."])
_NUT = [
"...nnnn...",
".nnnnnnnn.",
"nnnnnnnnnn",
"nnWWnnWWnn",
"nnWKnnWKnn",
"nnnnnnnnnn",
"nnnnnnnnnN",
"nnnnKKnnnN",
"nnnnnnnnNN",
"nnnnnnnnNN",
"NnnnnnnNNN",
".NNnnnNNN.",
"..NNNNNN.."]
_CRACKS = [[(2,1),(3,2),(3,3),(1,6),(2,7)], [(7,8),(8,9),(7,10),(5,1),(6,2),(1,9),(2,10)]]

def wallnut(stage):
    """The wall-nut, cracking: stage 0, 1, 2 (stage 2 also looks up, worried)."""
    g = [list(r) for r in _NUT]
    for k in range(stage):
        for x, y in _CRACKS[k]: g[y][x] = 'c'
    if stage >= 2: g[3][3], g[4][3], g[3][7], g[4][7] = 'K', 'W', 'K', 'W'
    return S([''.join(r) for r in g])
CHERRY = S([
".....l.....",
"....l.l....",
"...l...l...",
".rrr...rrr.",
"rrrrr.rrrrr",
"rKrKr.rKrKr",
"rrrrr.rrrrr",
"RrrrR.RrrrR",
".RRR...RRR."])
CLAUDESHOOTER = {'G':(217,119,87), 'g':(168,80,54)}                  # the reward: a peashooter in orange

# ---- the zombies (drawn facing right; they walk left, flipped) -----------------------------------
ZPAL = {'1':(160,178,140), '2':(120,138,104), '3':(112,86,62), '4':(80,60,44), '5':(236,232,220),
        '6':(200,30,40), '7':(70,80,110), '8':(240,240,230), '9':(40,30,30), 'c':(244,140,40),
        'C':(196,96,20), 'm':(176,178,188), 'M':(118,120,132)}
ZHEAD = [
"..1111111.....",
".111111111....",
".118911891....",
".111111111....",
".112999211....",
"..1111111....."]
ZBODY = [
"...3356533....",
"..33356533311.",
"..33356533311.",
"..3335653.....",
"..333363......",
"..3333333....."]
ZLEGS = {'w1':["...7777.......", "..77..77......", ".777...777...."],
         'w2':["...7777.......", "...77.77......", "..777.777....."]}
CONE = ["....cc........", "....cC........", "...ccCc.......", "...cCCc.......", "..ccccccc.....", ".CCCCCCCCC...."]
BUCKET = [".MmmmmmmM.....", ".MmmmmmmM.....", ".MmmmmmmM.....", "MMMMMMMMMM...."]

def zombie(legs, hat=None, arm=True, head=True):
    hat_rows = {'cone':CONE, 'bucket':BUCKET}.get(hat, [])
    body = [r for r in ZBODY]
    if not arm: body[1], body[2] = body[1][:9]+'.....', body[2][:9]+'.....'
    return S(list(hat_rows)+(ZHEAD if head else ['.'*14]*6)+body+ZLEGS[legs])
IMP = S([
"..11111..",
".1181811.",
".1111111.",
"..12921..",
"..355311.",
"..3553...",
"..7.7....",
".77.77..."])

# ---- Codex as Dr. Zomboss: the Codex head with red zombie eyes, a lab coat -----------------------
ZOMBOSS = S(ICONS['CODEX']+LOGO_BODY)
KPAL = {'y':(255,60,40), 'd':(228,228,234)}

MOWER = S([
"3..........",
".3.........",
"..3........",
"..3rrrrrr..",
".rrrrrrrrrr",
".rrRrrrrRrr",
"..KK....KK."])
MPAL = {'3':(150,150,160), 'r':(214,40,36), 'R':(150,24,24), 'K':(24,20,20)}

# ---- background: the front lawn ------------------------------------------------------------------
def _lawn(d):
    for y in range(0, 22):
        d.line([0, y, W, y], fill=(int(lerp(104,168,y/22)), int(lerp(164,214,y/22)), 240))
    for cx, cy in ((96,7), (150,11)):
        d.ellipse([cx-11, cy-3, cx+11, cy+3], fill=(240,246,255)); d.ellipse([cx-5, cy-6, cx+6, cy+1], fill=(240,246,255))
    d.rectangle([0, 21, W, 30], fill=(58,124,44))                         # the hedge at the back
    for x0 in range(0, W, 7): d.ellipse([x0-2, 17, x0+6, 25], fill=(58,124,44)); d.point((x0+2, 19), fill=(84,154,60))
    for row, (y0, y1) in enumerate(((30,38), (39,47), (48,GROUND))):      # the lawn tiles, three lanes deep
        for i, x0 in enumerate(range(14, W, 14)):
            d.rectangle([x0, y0, x0+13, y1], fill=(118,192,64) if (i+row) % 2 else (98,172,52))
        d.line([14, y1+1, W, y1+1], fill=(78,140,42))
    d.rectangle([0, GROUND+2, W, H], fill=(92,62,36))
    for x0 in range(0, W, 5): d.point((x0+(x0//5) % 3, GROUND+3+(x0//5) % 2), fill=(120,86,52))
    d.rectangle([0, 10, 13, GROUND+1], fill=(224,208,172))               # the house: siding, door, roof
    for y in range(12, GROUND, 3): d.line([0, y, 13, y], fill=(192,174,138))
    d.rectangle([3, 34, 11, GROUND+1], fill=(134,88,52), outline=(90,56,30)); d.point((10, 47), fill=(240,210,90))
    d.polygon([(0, 4), (19, 12), (0, 12)], fill=(152,62,50)); d.line([0, 12, 19, 12], fill=(110,40,34))
register_bg(THEME, lambda v: (v+30, v+70, v+10), decor=_lawn)

# ---- effects -------------------------------------------------------------------------------------
def _sun(d, x, y, r, f):
    for k in range(8):
        a = k*math.pi/4+f*math.pi/24; d.line([x, y, x+round(math.cos(a)*(r+2), 6), y+round(math.sin(a)*(r+2), 6)], fill=(255,236,120))   # (rounded: float noise)
    d.ellipse([x-r, y-r, x+r, y+r], fill=(255,214,40), outline=(232,150,20))
    d.point((x-1, y-1), fill=(255,250,210))

COSTS = [50, 100, 50, 150]                # sunflower, peashooter, wall-nut, cherry bomb

@fx('pvz_hud')
def _fx_hud(d, im, e, f):
    """The seed bank: sun counter and four seed packets (darkened when there are not enough suns;
    `pick` blinks the one being planted)."""
    _, sun, pick = e
    d.rectangle([0, 0, 63, 13], fill=(112,72,40), outline=(58,36,20))
    d.rectangle([1, 1, 13, 12], fill=(84,52,28)); _sun(d, 7, 4, 2, f)
    d.rectangle([1, 8, 13, 12], fill=(236,226,190)); t = str(sun); text(d, t, 7-len(t)*2+1, 8, (40,30,20), shadow=None)
    for i in range(4):
        x0 = 16+i*12; d.rectangle([x0, 1, x0+10, 12], fill=(236,226,170), outline=(70,150,50))
        cx = x0+5
        if i == 0: d.ellipse([cx-3, 3, cx+3, 9], fill=(252,214,40)); d.ellipse([cx-1, 5, cx+1, 7], fill=(160,90,30))
        if i == 1: d.ellipse([cx-3, 3, cx+2, 8], fill=(112,192,84)); d.rectangle([cx+2, 4, cx+4, 6], fill=(52,118,44))
        if i == 2: d.ellipse([cx-3, 3, cx+3, 10], fill=(198,150,92), outline=(146,100,56))
        if i == 3: d.ellipse([cx-4, 5, cx, 9], fill=(222,40,40)); d.ellipse([cx, 5, cx+4, 9], fill=(222,40,40)); d.line([cx-2, 5, cx, 2, cx+2, 5], fill=(46,108,40))
        if sun < COSTS[i]: im.paste(fade_to(im.crop((x0+1, 2, x0+10, 12)), (0,0,0), 0.55), (x0+1, 2))
        if pick == i and (f//2) % 2: d.rectangle([x0-1, 0, x0+11, 13], outline=(255,255,255))

@fx('pvz_sun')
def _fx_sun(d, im, e, f):
    _, x, y = e; _sun(d, int(x), int(y), 4, f)

@fx('pvz_pea')
def _fx_pea(d, im, e, f):
    _, x, y = e; x, y = int(x), int(y)
    d.ellipse([x-2, y-2, x+2, y+2], fill=(120,220,70), outline=(40,100,30)); d.point((x-1, y-1), fill=(220,255,200))

@fx('pvz_splat')
def _fx_splat(d, im, e, f):
    """A pea bursting on a zombie (green) or clanging off metal (yellow)."""
    _, x, y, metal = e; c = (255,230,90) if metal else (130,230,80)
    for dx, dy in ((-3,-2), (-3,2), (-1,-3), (-1,3), (-4,0)): d.point((x+dx, y+dy), fill=c)
    d.ellipse([x-2, y-1, x, y+1], fill=c)

@fx('pvz_ash')
def _fx_ash(d, im, e, f):
    """A charred zombie crumbling into a pile of ash (k 0..1)."""
    _, x, k = e; x = int(x); h = int(6*(1-k))+1; w = 7-int(2*k)
    d.ellipse([x-w, GROUND-h, x+w, GROUND+1], fill=(46,40,38)); d.point((x-2, GROUND-h+1), fill=(90,80,74))
    rr = random.Random(int(x)*7+int(k*10))
    for _ in range(4): d.point((x+rr.randint(-w, w), GROUND-h-rr.randint(1, 4)), fill=(70,64,60))

def zb_hand(x, arm):
    """Where the Zombot's hand is: arm 0 hangs forward, arm 1 is raised to throw."""
    return lerp(x-32, x-26, arm), lerp(44, 6, arm)

@fx('pvz_zombot')
def _fx_zombot(d, im, e, f):
    """The Zombot, Dr. Zomboss's giant robot zombie head on legs, facing left. arm: 0..1 (raised);
    jaw: px open; wreck: 0..1 (it sinks, scorched)."""
    _, x, arm, jaw, wreck = e; x = int(x); sink = int(wreck*14)
    dk = lambda c: tuple(int(v*(1-0.6*wreck)) for v in c)
    met, met2, met3 = dk((124,132,146)), dk((90,96,110)), dk((60,64,76))
    for lx in (x-14, x+6):
        d.rectangle([lx, 44+sink//2, lx+8, GROUND-2], fill=met2, outline=OUT)
        d.rectangle([lx-2, GROUND-3, lx+10, GROUND], fill=met3, outline=OUT)
    d.rounded_rectangle([x-23, 13+sink, x+23, 47+sink], 6, fill=met, outline=OUT)
    for y in (21, 40): d.line([x-21, y+sink, x+21, y+sink], fill=met2)
    for rx in range(x-19, x+20, 6): d.point((rx, 16+sink), fill=met3); d.point((rx, 44+sink), fill=met3)
    eye = (255,70,40) if wreck == 0 else (90,30,24)
    for ex in (x-17, x-5):
        d.rectangle([ex, 24+sink, ex+7, 28+sink], fill=(30,10,10)); d.rectangle([ex+1, 25+sink, ex+6, 27+sink], fill=eye)
        if wreck == 0: d.point((ex+3, 26+sink), fill=(255,230,120))
    d.rectangle([x-20, 32+sink, x+4, 34+sink+jaw], fill=(30,16,18), outline=OUT)
    for tx in range(x-19, x+4, 3):
        d.polygon([(tx, 32+sink), (tx+2, 32+sink), (tx+1, 34+sink)], fill=(236,232,210))
        d.polygon([(tx, 34+sink+jaw), (tx+2, 34+sink+jaw), (tx+1, 32+sink+jaw)], fill=(236,232,210))
    sx, sy = x-20, 30+sink; hx, hy = zb_hand(x, arm); hy += sink
    d.line([sx, sy, hx, hy], fill=OUT, width=7); d.line([sx, sy, hx, hy], fill=met2, width=5)
    d.rectangle([hx-3, hy-3, hx+3, hy+3], fill=met3, outline=OUT)

@fx('pvz_dome')
def _fx_dome(d, im, e, f):
    """The glass dome of the cockpit on top of the Zombot (drawn over Codex)."""
    _, x = e; x = int(x)
    d.arc([x-10, 1, x+10, 25], 180, 360, fill=(190,226,255)); d.point((x-5, 6), fill=(255,255,255))

@fx('pvz_debris')
def _fx_debris(d, im, e, f):
    """Plates and bolts of the Zombot flying off, t frames after the crash."""
    _, x, t = e; rr = random.Random(616)
    for _ in range(14):
        vx, vy, sz = rr.uniform(-3, 3), rr.uniform(-4.5, -1.5), rr.randint(1, 3)
        px, py = x+vx*t, 30+vy*t+0.3*t*t
        if py < GROUND: d.rectangle([px, py, px+sz, py+sz], fill=(124,132,146) if sz > 1 else (255,200,90), outline=OUT if sz > 1 else None)
    for k in range(5):
        r = 3+t//2+k; sx = x-12+k*6; sy = 30-t-k*2
        if sy > -r: d.ellipse([sx-r, sy-r, sx+r, sy+r], fill=(70,66,64) if k % 2 else (96,90,86))

@fx('pvz_fly')
def _fx_fly(d, im, e, f):
    """Codex flung off the screen by the explosion, spinning."""
    _, t = e
    sp = sprite_img(ZOMBOSS, KPAL).rotate(t*33, resample=Image.NEAREST, expand=True)
    x, y = ZB_X+2+2.6*t, 12-3.6*t+0.22*t*t
    im.paste(sp, (int(x-sp.width/2), int(y-sp.height/2)), sp)
    if t < 12: text(d, "NOOO!", int(x)-28, max(2, int(y)-4), (255,255,255))

@fx('pvz_term')
def _fx_term(d, im, e, f):
    """Codex's terminal: > RM -RF LAWN, typed n characters."""
    _, n = e; msg = "RM -RF LAWN"
    x0, x1 = 92, 144
    d.rectangle([x0, 1, x1, 10], fill=(14,16,20), outline=(90,96,110))
    d.polygon([(x1, 4), (x1+5, 6), (x1, 8)], fill=(90,96,110))
    d.line([x0+2, 3, x0+4, 5, x0+2, 7], fill=(90,230,110))
    text(d, msg[:n], x0+7, 3, (90,230,110), shadow=None)
    if n < len(msg) or (f//3) % 2: d.rectangle([x0+7+min(n, len(msg))*4, 7, x0+9+min(n, len(msg))*4, 7], fill=(90,230,110))

@fx('pvz_big')
def _fx_big(d, im, e, f):
    _, txt, y, c, ol, cx = e; big_text(im, txt, y, c, cx=cx, outline=ol)

@fx('pvz_eaten')
def _fx_eaten(d, im, e, f):
    """THE ZOMBIES / ATE YOUR BRAINS!, typed n characters; struck through once the mower roars."""
    _, n, strike = e; l1, l2 = "THE ZOMBIES", "ATE YOUR BRAINS!"
    g, ol = (110,210,60), (20,52,12)
    boxes = []
    if n > 0: boxes.append(big_text(im, l1[:n], 18, g, outline=ol))
    if n > len(l1): boxes.append(big_text(im, l2[:n-len(l1)], 33, g, outline=ol))
    if strike:
        for x, y, w, h in boxes: d.line([x-3, y+h//2+1, x+w+2, y+h//2-1], fill=(230,30,30), width=2)

# ---- the sun pickups -----------------------------------------------------------------------------
SUNS = [(10,'sky',80), (16,'flower',SUNF_X), (96,'flower',SUNF_X), (118,'sky',34), (130,'flower',SUNF_X),
        (142,'flower',SUNF_X)]
SPEND = [(56, 50), (184, 150)]            # the wall-nut, the cherry bomb

def sun_pos(t0, kind, x, f):
    """Where a sun is f frames into the clip (None: not there): it falls from the sky (or pops out of
    the sunflower), waits, then flies to the seed bank, arriving 26 frames after it appeared."""
    t = f-t0
    if t < 0 or t >= 26: return None
    if kind == 'sky': rest = (x, 34); start = lerp(-6, 34, t/14)
    else: rest = (x+7, GROUND-20); start = GROUND-14-math.sin(min(1, t/6)*math.pi*0.5)*6
    if t < 18: return (rest[0] if kind == 'sky' else lerp(x, rest[0], t/6)), (start if t < 14 or kind != 'sky' else 34)
    k = ease((t-18)/8); return lerp(rest[0], HUD[0], k), lerp(rest[1], HUD[1], k)

def sun_count(f):
    return 50+25*sum(1 for t0, _, _ in SUNS if f >= t0+26)-sum(c for t, c in SPEND if f >= t)

# ---- the zombies' walk ---------------------------------------------------------------------------
ZS = {1:(76, 1.4, None), 2:(86, 1.4, NUT_STOP), 3:(100, 1.3, NUT_STOP+12)}   # enter, speed, stop

def zx(i, f):
    enter, sp, stop = ZS[i]; x = 200-sp*(max(f, enter)-enter)
    return max(stop, x) if stop else x

def zb_x(f):
    """The Zombot stomps in, one step every 6 frames."""
    if f < 226: return 230
    st, p = divmod(f-226, 6)
    return ZB_X if st >= 4 else lerp(222-15.5*st, 222-15.5*(st+1), ease(p/4))

def front(t):
    """The left edge of the frontmost thing the peas can hit (None: nothing on screen)."""
    xs = []
    if 76 <= t < 112: xs.append(zx(1, min(t, 110))-6)
    if 86 <= t < 204: xs.append(zx(2, t)-6)
    if 226 <= t < 331: xs.append(zb_x(t)-23)
    xs = [x for x in xs if x < 184]
    return min(xs) if xs else None

PEAS = list(range(80, 204, 8))+list(range(240, 330, 8))
PEA_Y = GROUND-10

def peas(s, f):
    for t0 in PEAS:
        if t0 > f: break
        for t in range(t0, f+1):
            px = PEA_X+7+5*(t-t0); fr = front(t)
            if fr is not None and px >= fr:
                if f-t <= 1: s['fx'].append(('pvz_splat', int(fr), PEA_Y, t >= 226))
                break
        else:
            if px < W+4: s['fx'].append(('pvz_pea', px, PEA_Y))

def walk_pose(f): return 'w1' if (f//5) % 2 else 'w2'

# ---- close-up: the wall-nut being chewed ---------------------------------------------------------
NUT_C, NUT_SH, ZSKIN = (198,150,92), (160,112,64), (160,178,140)

def closeup_nut(fr, f):
    im = Image.new('RGB', (W, H), (64,128,40)); d = ImageDraw.Draw(im)
    for x0 in range(0, W, 20): d.rectangle([x0, 0, x0+9, H], fill=(74,142,48))
    j = (f % 2)*2-1 if fr >= 4 else 0
    cx, cy = 66+j, 40
    d.ellipse([cx-50, cy-46, cx+50, cy+46], fill=OUT)
    d.ellipse([cx-48, cy-44, cx+48, cy+44], fill=NUT_SH); d.ellipse([cx-48, cy-44, cx+40, cy+36], fill=NUT_C)
    for k in range(min(3, 1+fr//7)):                                    # bites out of the right edge
        by = cy-20+k*15; d.ellipse([cx+32, by-8, cx+60, by+8], fill=OUT); d.ellipse([cx+34, by-6, cx+60, by+6], fill=(238,218,164))
        for ty in range(by-5, by+6, 4): d.point((cx+34, ty), fill=OUT)                   # tooth marks
    cracks = [[(cx-12, cy-44), (cx-6, cy-32), (cx-13, cy-22), (cx-9, cy-16)],
              [(cx+28, cy-32), (cx+19, cy-23), (cx+24, cy-11)],
              [(cx-44, cy+6), (cx-30, cy+12), (cx-33, cy+25)]]
    for c in cracks[:1+fr//8]: d.line(c, fill=(70,44,24), width=2)
    for ex in (cx-22, cx+10):                                           # scared eyes, darting to the zombie
        d.ellipse([ex-9, cy-24, ex+9, cy-4], fill=OUT); d.ellipse([ex-8, cy-23, ex+8, cy-5], fill=(250,250,250))
        px = ex+3+(1 if (fr//4) % 2 else -1); d.ellipse([px-3, cy-18, px+3, cy-11], fill=OUT)
    d.line([cx-30, cy-31, cx-15, cy-27], fill=OUT, width=2); d.line([cx+3, cy-27, cx+18, cy-31], fill=OUT, width=2)
    d.line([cx-12, cy+12, cx-6, cy+9, cx, cy+12, cx+6, cy+9], fill=OUT, width=2)
    if fr >= 6:                                                         # a sweat drop
        sy = cy-34+(fr-6)*2; d.ellipse([cx+24, sy, cx+29, sy+6], fill=(150,210,255)); d.point((cx+25, sy+1), fill=(255,255,255))
    bite = (fr//3) % 2; zx_ = 146-ease(fr/5)*8+(3 if bite else 0)          # the zombie chomping in
    d.ellipse([zx_, 2, zx_+76, 74], fill=OUT); d.ellipse([zx_+2, 4, zx_+74, 72], fill=ZSKIN)
    d.ellipse([zx_+26, 18, zx_+40, 32], fill=OUT); d.ellipse([zx_+28, 20, zx_+38, 30], fill=(240,240,230)); d.ellipse([zx_+29, 23, zx_+33, 27], fill=OUT)
    m = 2 if bite else 12
    d.rectangle([zx_-1, 38-m, zx_+28, 40+m], fill=(40,24,24), outline=OUT)
    for tx in range(int(zx_), int(zx_)+27, 5):
        d.rectangle([tx, 38-m, tx+3, 41-m], fill=(236,232,210)); d.rectangle([tx+2, 37+m, tx+5, 40+m], fill=(236,232,210))
    if fr >= 4: big_text(im, "CHOMP", 3 if bite else 5, (255,255,255), cx=150, outline=OUT)
    if fr < 3: zoom_lines(d, (255,255,220))
    return im

# ---- close-up: Crazy Dave --------------------------------------------------------------------------
def closeup_dave(fr, f):
    im = Image.new('RGB', (W, H), (250,170,50)); d = ImageDraw.Draw(im)
    for i in range(18):
        a = i*0.349+fr*0.05
        d.polygon([(58, 40), (58+math.cos(a)*240, 40+math.sin(a)*240), (58+math.cos(a+0.17)*240, 40+math.sin(a+0.17)*240)], fill=(255,206,80))
    j = (f % 2)*2-1
    d.rectangle([16, 18, 100, H+4], fill=OUT); d.rectangle([18, 20, 98, H+4], fill=(217,119,87))
    d.rectangle([18, 20, 26, H+4], fill=(190,100,70))
    d.rectangle([10, 0, 106, 16], fill=OUT); d.rectangle([12, 0, 104, 14], fill=DPAL['1'])     # the saucepan
    for x0 in (22, 26): d.line([x0, 1, x0, 12], fill=(232,236,244))
    d.rectangle([8, 14, 108, 19], fill=OUT); d.rectangle([10, 15, 106, 18], fill=DPAL['2'])
    d.rectangle([106, 5, 160, 10], fill=OUT); d.rectangle([107, 6, 158, 9], fill=DPAL['3'])
    d.rectangle([44, 28+j, 51, 44+j], fill=OUT)                         # one eye small, one huge: CRAZY
    d.rectangle([66, 24-j, 78, 48-j], fill=OUT); d.rectangle([68, 27-j, 70, 30-j], fill=(255,255,255))
    rr = random.Random(77)
    for _ in range(70):                                                 # the scruffy beard
        x, y = rr.randint(24, 98), rr.randint(52, H)
        d.rectangle([x, y, x+1, y+2], fill=DPAL['4'])
    d.line([40, 54, 58, 58, 76, 54], fill=OUT, width=2)
    big_text(im, "BECAUSE IM", 20, (255,255,255), cx=143, outline=(120,60,10))
    if fr >= 4: big_text(im, "CRAAAZY!", 36+(j if fr >= 6 else 0), (255,255,255), cx=143+j, outline=(170,30,30))
    if fr < 3: zoom_lines(d, (255,255,220))
    return im

# ---- card: a new plant ---------------------------------------------------------------------------
def card_plant(fr, f):
    im = Image.new('RGB', (W, H), (60,40,24)); d = ImageDraw.Draw(im)
    for i in range(20):
        a = i*0.314+fr*0.04; c = (96,68,38) if i % 2 else (72,50,30)
        d.polygon([(40, 32), (40+math.cos(a)*240, 32+math.sin(a)*240), (40+math.cos(a+0.16)*240, 32+math.sin(a+0.16)*240)], fill=c)
    k = ease(fr/5); w, h = int(36*k), int(52*k)
    if w > 2:
        d.rectangle([40-w//2, 32-h//2, 40+w//2, 32+h//2], fill=(240,228,176), outline=(70,150,50), width=2)
        if k >= 1:
            sp = sprite_img(PEASHOOTER, dict(PPAL, **CLAUDESHOOTER), 2); paste_feet(im, sp, 40, 50)
            asterisk(d, 37, 9, 3, (217,119,87), f)
            text(d, "100", 34, 52, (40,30,20), shadow=None)
    if fr >= 4:
        big_text(im, "YOU GOT A", 9, (255,255,255), cx=126, outline=(90,50,20))
        big_text(im, "NEW PLANT!", 25, (255,255,255), cx=126, outline=(90,50,20))
    if fr >= 8: text(d, "CLAUDESHOOTER", 126-26, 46, (255,214,80))
    if fr < 3: im = fade_to(im, (255,255,255), 1-fr/3)
    if fr >= 18: im = fade_to(im, (0,0,0), (fr-17)/4)
    return im

# ---- the clip ------------------------------------------------------------------------------------
def clip_lastwave(f):
    s = scene(f, THEME)
    if 160 <= f < 184: s['image'] = closeup_nut(f-160, f); return s
    if 346 <= f < 362: s['image'] = closeup_dave(f-346, f); return s
    if 362 <= f < 384: s['image'] = card_plant(f-362, f); return s
    # --- the lawn: state defaults = the neutral pose ---
    cx, cpose, cflip, cy = CX, guard_pose(f), False, GROUND
    nut, pick, mower = None, None, MOWER_X
    # 1) suns: Claude grabs the first two; then he walks out and plants a wall-nut
    if 28 <= f < 40: cpose = 'armsup'
    if 44 <= f < 74:
        if f < 56: cx = ez(CX, 84, (f-44)/12)
        elif f < 60: cx, cpose = 84, 'charge'
        else: cx = ez(84, CX, (f-60)/14); cflip = True
        if f < 56 or f >= 60: cpose = 'guard' if (f//3) % 2 else 'guard2'; cy = GROUND-((f//3) % 2)
    if 50 <= f < 58: pick = 2
    if 58 <= f < 384: nut = 0 if f < 166 else (1 if f < 190 else 2)
    if 58 <= f < 64:
        for k in range(4): s['fx'].append(('smoke', NUT_X-6+k*4, GROUND-1-(f-58)//2, 2, (120,86,52)))
    # 2) the wave
    if 60 <= f < 76:
        s['fx'].append(('pvz_big', "A HUGE WAVE OF ZOMBIES", 17, (236,40,30), (60,0,0), W//2))
        s['fx'].append(('pvz_big', "IS APPROACHING!", 32, (236,40,30), (60,0,0), W//2))
    # the zombies: 1 basic (arm, head, down), 2 conehead (cone off, chews the nut), 3 buckethead
    zs = []
    if 76 <= f < 124:
        x = zx(1, min(f, 110)); arm, head = f < 98, f < 108
        if f < 110: zs.append(actor(zombie(walk_pose(f), arm=arm, head=head), x, flip=True, pal=ZPAL))
        else: zs.append(actor(rotate90(zombie('w2', arm=False, head=False), 3, trim=True), x+4, flip=True, pal=ZPAL, alpha=1-max(0, f-116)/8))
    if 108 <= f < 124:
        t = f-108; hx = zx(1, 108)+3+t*0.6; hy = GROUND-14+min(14, t*t*0.5)
        zs.append(actor(S(ZHEAD), hx, int(hy), flip=True, pal=ZPAL, alpha=1-max(0, f-116)/8))
    if 128 <= f < 150:
        t = f-128; zs.append(actor(S(CONE), zx(2, 128)+2+t*0.8, int(min(GROUND, GROUND-24+t*t*0.4)), flip=True, pal=ZPAL, alpha=1-max(0, f-142)/8))
    charred = 204 <= f < 216
    for i, hat in ((2, 'cone' if f < 128 else None), (3, 'bucket')):
        enter = ZS[i][0]
        if not (enter <= f < 216): continue
        x = zx(i, f); legs = walk_pose(f) if x > ZS[i][2] else 'w2'
        if x <= ZS[i][2] and i == 2 and f < 204 and (f//4) % 2: x -= 1              # chewing
        zs.append(actor(zombie(legs, hat), x, flip=True, pal=ZPAL, tint=(34,28,26) if charred else None))
    if 153 <= f < 204 and (f//6) % 2: s['fx'].append(('dmg', "CHOMP", NUT_X-8, GROUND-26, (255,255,255)))
    if 216 <= f < 228:
        for i in (2, 3): s['under'].append(('pvz_ash', zx(i, 204), (f-216)/12))
    if 216 <= f < 236: zs.append(actor(S(BUCKET), zx(3, 204)+3, GROUND, flip=True, pal=ZPAL, tint=(60,56,56), alpha=1-max(0, f-228)/8))
    # 3) the cherry bomb
    if 180 <= f < 186: pick = 3
    if 184 <= f < 190: cpose = 'punch'
    cherry = None
    if 186 <= f < 196:
        t = (f-186)/10; cherry = (lerp(CX+8, CHERRY_X, t), GROUND-10+t*10-math.sin(t*math.pi)*30, None)
    if 196 <= f < 204:
        j = (f % 2)*2-1 if f >= 199 else 0
        cherry = (CHERRY_X+j, GROUND, (255,255,255) if f >= 200 and f % 2 else None)
    if 204 <= f < 216:
        t = f-204
        if t < 8: s['fx'].append(('boom', CHERRY_X, GROUND-8, 4+t*4)); s['shake'] = rshake(2 if t < 4 else 1)
        if t < 6: s['flash'] = 1-t/6; s['fc'] = (CHERRY_X, GROUND-8); s['flashc'] = (255,200,120)
        s['fx'].append(('pvz_big', "KABOOM!", 20, (255,170,40), (120,20,10), CHERRY_X))
        cpose = 'armsup'
    # 4) Dr. Codex on the Zombot
    zbx, arm, jaw, wreck = None, 0.0, 0, 0.0
    if 226 <= f < 346:
        zbx = zb_x(f)
        if f < 250 and (f-226) % 6 == 5: s['shake'] = (0, 2)
        jaw = 3 if (f//8) % 2 else 0
    if 232 <= f < 250: s['fx'].append(('pvz_big', "DR. CODEX", 24, (150,236,110), (20,60,20), 78))
    if 250 <= f < 268: s['fx'].append(('pvz_term', min(11, (f-250)*2//3)))
    if 264 <= f < 276: arm = ease((f-264)/5) if f < 271 else 1-ease((f-271)/5)
    imp = None
    if 264 <= f < 271: hx, hy = zb_hand(zbx, arm); imp = (hx, hy+4)
    if 271 <= f < 283:
        t = (f-271)/12; imp = (lerp(ZB_X-26, 40, t), lerp(10, GROUND, t)-math.sin(t*math.pi)*14)
    if 283 <= f < 307: imp = (40-(f-283)*0.45, GROUND)
    if 307 <= f < 316:
        t = f-307; imp = (36+t*2, GROUND-t*4)
        if t < 6: s['fx'].append(('smoke', 34+t, GROUND-6-t, 3+t//2, (220,220,220)))
    if 283 <= f < 289: cpose = 'hurt'; cflip = False
    if 285 <= f < 312: s['fx'].append(('pvz_eaten', min(27, (f-285)*2), f >= 304))
    # 5) the lawn mower
    if 289 <= f < 298: cx = ez(CX, 20, (f-289)/9); cpose = 'guard'
    if 298 <= f < 304:
        t = (f-298)/6; cx = lerp(20, MOWER_X+1, t); cy = GROUND-4-math.sin(t*math.pi)*10; cpose = 'armsup'
    if 304 <= f < 331:
        mower = MOWER_X+(f-304)*4.6; cx, cy, cpose = mower+1, GROUND-4, 'dash'
        if (f//2) % 2: s['fx'].append(('dmg', "BRRRM", int(mower)-10, GROUND-24, (255,230,90)))
    if 331 <= f < 346:
        mower = None; t = f-331; wreck = min(1, t/10); jaw = 6
        if t < 8: s['fx'].append(('boom', zbx-20, GROUND-14, 4+t*5)); s['shake'] = rshake(2 if t < 5 else 1)
        if t < 6: s['flash'] = 1-t/6; s['fc'] = (zbx-20, GROUND-14); s['flashc'] = (255,210,140)
        s['fx'].append(('pvz_debris', zbx-10, t)); s['fx'].append(('pvz_fly', t))
        if t < 9: k = t/9; cx = lerp(MOWER_X+1+27*4.6, 112, k); cy = GROUND-4+4*k-math.sin(k*math.pi)*16; cpose = 'hurt'
        else: cx, cpose = 112, 'armsup'
        cflip = False
    # --- draw ---
    if zbx is not None: s['under'].append(('pvz_zombot', zbx, arm, jaw, wreck))
    s['actors'].append(actor(SUNFLOWER2 if (f//10) % 2 else SUNFLOWER, SUNF_X, pal=PPAL))
    s['actors'].append(actor(PEASHOOTER, PEA_X, GROUND-(1 if (f//7) % 2 else 0), pal=PPAL))
    if nut is not None: s['actors'].append(actor(wallnut(nut), NUT_X, pal=PPAL))
    s['actors'] += zs
    if cherry: s['actors'].append(actor(CHERRY, cherry[0], int(cherry[1]), pal=PPAL, tint=cherry[2]))
    if imp: s['actors'].append(actor(IMP, imp[0], int(imp[1]), flip=True, pal=ZPAL))
    if zbx is not None and f < 331: s['actors'].append(actor(ZOMBOSS, zbx+2, 19, pal=KPAL)); s['fx'].insert(0, ('pvz_dome', zbx+2))
    if mower is not None: s['actors'].append(actor(MOWER, mower, GROUND, pal=MPAL))
    s['actors'].append(actor(DAVE[cpose], cx, int(cy), flip=cflip, pal=DPAL))
    if f < 204: peas(s, f)
    elif 226 <= f < 331: peas(s, f)
    for t0, kind, x in SUNS:
        p = sun_pos(t0, kind, x, f)
        if p: s['fx'].append(('pvz_sun', p[0], p[1]))
    s['fx'].append(('pvz_hud', max(0, sun_count(f)) if f < 384 else 50, pick))
    if 384 <= f < 388: s['fx'].append(('dim', 1-(f-384)/4))
    return s

CLIPS = [clip('lastwave', N_, clip_lastwave)]
