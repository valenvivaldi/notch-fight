"""Close-up helpers shared by the themes' primer planos: the zoom lines, a fade, and the pieces of a detailed
face (a shaded ellipse for a head or a cap of hair, an almond eye, brows, locks of hair, a glow behind)."""
from .core import *
from PIL import ImageChops

PUPIL, LID = (18, 12, 12), (40, 22, 20)

def zoom_lines(d,c=(255,255,255)):
    """The 10 radial speed lines flashed at the start of a close-up (callers keep their own `if t<...`)."""
    for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=c)

def fade_to(im,c,a):
    """Return `im` blended towards the flat colour c by alpha a (no clamping: callers clamp).
    Close-ups reassign (`im=fade_to(...)`, then re-create `d`); fx paste it back (`im.paste(fade_to(...))`)."""
    return Image.blend(im,Image.new('RGB',im.size,c),a)

def soft_glow(im, cx, cy, rx, ry, col, k=0.5):
    """A soft light behind a head: concentric discs, the brightest in the middle, added onto im."""
    layer = Image.new('RGB', (W, H), (0, 0, 0)); ld = ImageDraw.Draw(layer)
    for i in range(6, 0, -1):
        s = i / 6
        ld.ellipse([cx - rx * s, cy - ry * s, cx + rx * s, cy + ry * s], fill=tuple(int(c * k * (1 - s)) for c in col))
    im.paste(ImageChops.add(im, layer))

def put_px(px, x, y, c):
    if 0 <= x < W and 0 <= y < H: px[int(x), int(y)] = c

def mix_rgb(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sphere(px, cx, cy, rx, ry, tones, light=(-0.55, -0.6, 0.58)):
    """A shaded ellipse (a head, a cap of hair, a beard): tones = (shade, base, light) by the light from the
    upper left, and a 1 px dark outline around it."""
    dark, base, lit = tones
    lx, ly, lz = light; n = math.sqrt(lx * lx + ly * ly + lz * lz); lx, ly, lz = lx / n, ly / n, lz / n
    ro = 1 + 1.0 / min(rx, ry)
    for y in range(max(0, int(cy - ry - 2)), min(H, int(cy + ry + 3))):
        for x in range(max(0, int(cx - rx - 2)), min(W, int(cx + rx + 3))):
            u = (x + 0.5 - cx) / rx; v = (y + 0.5 - cy) / ry; r2 = u * u + v * v
            if r2 <= 1:
                lam = u * lx + v * ly + math.sqrt(1 - r2) * lz
                px[x, y] = lit if lam > 0.42 else base if lam > -0.12 else dark
            elif r2 <= ro * ro: px[x, y] = OUT

def almond_eye(im, cx, cy, hw, hh, look, lid, iris, iris_dark, skin, red=False, lash=True):
    """An almond eye: sclera (shaded under the lid), iris in three tones with a dark rim, a pupil, two glints,
    the lid line with a lash at the outer corner, the crease above it. lid: 0 wide open .. 1 shut."""
    px = im.load(); d = ImageDraw.Draw(im)
    top = cy - hh + 2 * hh * lid
    white, shade = ((226, 146, 150), (170, 92, 100)) if red else ((242, 236, 234), (184, 172, 180))
    ix, iy, ir = cx + look[0], cy + look[1], hh * 0.8
    for y in range(int(cy - hh) - 1, int(cy + hh) + 2):
        for x in range(int(cx - hw) - 1, int(cx + hw) + 2):
            dx = (x + 0.5 - cx) / hw; dy = (y + 0.5 - cy) / hh
            if dx * dx + dy * dy > 1 or y + 0.5 < top: continue
            c = shade if y + 0.5 < top + 1.5 else white
            r = math.hypot(x + 0.5 - ix, y + 0.5 - iy)
            if r <= ir:
                c = PUPIL if r <= ir * 0.42 else iris_dark if r > ir * 0.8 else (iris if y + 0.5 < iy + ir * 0.3 else mix_rgb(iris, iris_dark, 0.35))
            px[x, y] = c
    put_px(px, ix - ir * 0.45, iy - ir * 0.5, (255, 255, 255))            # the two glints
    put_px(px, ix + ir * 0.35, iy + ir * 0.35, (236, 240, 246))
    d.line([cx - hw, top, cx + hw, top], fill=LID)                      # the lid
    d.line([cx - hw, top + 1, cx + hw, top + 1], fill=mix_rgb(shade, LID, 0.3)) if lid > 0.2 else None
    if lash:                                                            # the lashes, thicker at the outer corner
        out = 1 if look[0] >= 0 else -1
        d.line([cx + out * hw * 0.2, top, cx + out * hw * 1.05, top - 1], fill=LID)
        put_px(px, cx + out * hw * 1.1, top, LID)
    d.line([cx - hw * 0.7, top - 2, cx + hw * 0.7, top - 2], fill=mix_rgb(skin[0], skin[1], 0.5))   # the crease
    d.line([cx - hw * 0.8, cy + hh, cx + hw * 0.8, cy + hh], fill=mix_rgb(white, skin[2], 0.4))      # the lower lid

def brow(d, a, b, c, hi, w=2):
    """A brow: a thick line from a to b, a lighter hair line above it."""
    d.line([a, b], fill=c, width=w); d.line([(a[0], a[1] - 1), (b[0], b[1] - 1)], fill=hi)

def strand(d, x0, y0, x1, y1, bend, col):
    """A lock of hair: a curve from (x0,y0) to (x1,y1), bowed sideways by bend."""
    pts = [(x0 + (x1 - x0) * i / 8 + bend * math.sin(i / 8 * math.pi), y0 + (y1 - y0) * i / 8) for i in range(9)]
    d.line(pts, fill=col)

def locks(d, x0, x1, y0, y1, tones, seed):
    """Hair hanging straight down from y0 to y1 between x0 and x1: the base, a shade along the inner edge,
    lighter and darker strands every couple of pixels, a ragged end."""
    rr = random.Random(seed)
    d.rectangle([x0, y0, x1, y1], fill=tones[1])
    for x in range(x0, x1 + 1, 2):
        c = tones[2] if rr.random() < 0.35 else tones[0] if rr.random() < 0.5 else None
        if c: d.line([x, y0 + rr.randint(0, 4), x, y1 - rr.randint(0, 3)], fill=c)
    for x in range(x0, x1 + 1):
        if rr.random() < 0.5: d.point((x, y1), fill=OUT)
    d.line([x0 - 1, y0, x0 - 1, y1], fill=OUT); d.line([x1 + 1, y0, x1 + 1, y1], fill=OUT)
