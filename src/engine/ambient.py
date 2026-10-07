"""Ambient effects that loop on their own: rain, snow, ash, embers, fireflies, fog, a torch, twinkling
stars, camera flashes in a crowd. Each one keeps moving through the clip and is back where it started
at frame N, whatever the clip's length (they run on engine/loop.py), so a theme can leave them on in its
neutral pose. Add one like any effect, with its options in a dict (all optional):

    s['under'].append(('rain', {'dens': 0.7}))
    s['fx'].append(('torch', {'x': 40, 'y': 22}))
"""
import math, random
from .core import *
from .fx import fx
from . import loop

def _o(e, **default):
    """The options of an effect entry: its dict (if any) over the defaults."""
    o = dict(default)
    if len(e) > 1 and isinstance(e[1], dict): o.update(e[1])
    return o

def _fall(i, f, span, speed, salt):
    """How far drop i has fallen, 0..span, in a cycle that fits the clip; and its random draw."""
    rr = random.Random(salt * 7919 + i)
    C = loop.period(span / max(0.05, speed * rr.uniform(0.8, 1.2)))
    return ((loop.frame(f) % C) / C + rr.random()) % 1 * span, rr

@fx('rain')
def _fx_rain(d, im, e, f):
    """Slanted rain. dens 0..1, slant (px sideways per drop), length, color, top, bottom, speed (px/frame)."""
    o = _o(e, dens=1.0, slant=2, length=5, color=(150, 170, 205), top=0, bottom=GROUND, speed=6.0, n=60)
    span = o['bottom'] - o['top'] + o['length']
    for i in range(int(o['n'] * o['dens'])):
        y, rr = _fall(i, f, span, o['speed'], 11); y += o['top'] - o['length']
        x = rr.uniform(-10, W + 20) - (y - o['top']) * o['slant'] / o['length']
        d.line([x, y, x - o['slant'], y + o['length']], fill=o['color'])
        if y + o['length'] >= o['bottom'] - 1: d.point((x - o['slant'] - 1, o['bottom'] - 1), fill=o['color'])   # the splash

def _flakes(d, e, f, color, speed, size, sway, drift, salt, n):
    o = _o(e, dens=1.0, top=0, bottom=GROUND, color=color, speed=speed, n=n)
    span = o['bottom'] - o['top']
    for i in range(int(o['n'] * o['dens'])):
        y, rr = _fall(i, f, span, o['speed'], salt); y += o['top']
        x = (rr.uniform(0, W) + loop.wave(f, 64, i) * sway + drift * y / span) % W
        r = rr.choice(size)
        if r <= 1: d.point((int(x), int(y)), fill=o['color'])
        else: d.rectangle([int(x), int(y), int(x) + 1, int(y) + 1], fill=o['color'])

@fx('snow')
def _fx_snow(d, im, e, f):
    """Snow drifting down, swaying. dens 0..1, color, top, bottom, speed."""
    _flakes(d, e, f, (236, 240, 248), 0.5, (1, 1, 2), 2, 0, 23, 45)

@fx('ash')
def _fx_ash(d, im, e, f):
    """Ash falling, drifting to the right. dens 0..1, color, top, bottom, speed."""
    _flakes(d, e, f, (150, 144, 136), 0.4, (1, 1, 1, 2), 1.5, 14, 37, 30)

@fx('embers')
def _fx_embers(d, im, e, f):
    """Sparks rising from a fire and fading. x0, x1 (the fire's width), y (its base), height, n."""
    o = _o(e, x0=W // 2 - 10, x1=W // 2 + 10, y=GROUND, height=30, n=12)
    for i in range(o['n']):
        rise, rr = _fall(i, f, o['height'], o['height'] / 40, 41); t = rise / o['height']
        x = rr.uniform(o['x0'], o['x1']) + loop.wave(f, 24, i) * 2 * t
        c = (255, 220, 120) if t < 0.3 else ((255, 140, 40) if t < 0.7 else (150, 50, 20))
        d.point((int(x), int(o['y'] - rise)), fill=c)

@fx('fireflies')
def _fx_fireflies(d, im, e, f):
    """Fireflies wandering and blinking. n, area (x0, y0, x1, y1), color."""
    o = _o(e, n=8, area=(0, 10, W, GROUND - 4), color=(220, 255, 120))
    x0, y0, x1, y1 = o['area']; rr = random.Random(53)
    for i in range(o['n']):
        cx, cy = rr.uniform(x0, x1), rr.uniform(y0, y1); off = rr.random()
        x = cx + loop.wave(f, 120, i * 1.7) * 10; y = cy + loop.wave(f, 80, i * 2.3) * 5
        if (loop.phase(f, 40) + off) % 1 < 0.65:
            d.point((int(x), int(y)), fill=o['color'])
            if (loop.phase(f, 40) + off) % 1 < 0.3: d.point((int(x) + 1, int(y)), fill=tuple(v // 2 for v in o['color']))

@fx('fog')
def _fx_fog(d, im, e, f):
    """A bank of mist drifting sideways, once across per loop. dens 0..1, y0, y1, color."""
    o = _o(e, dens=0.6, y0=GROUND - 16, y1=GROUND + 4, color=(200, 206, 214))
    off = loop.phase(f, loop.N or 240) * W
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m); rr = random.Random(61)
    for i in range(14):
        x = (rr.uniform(0, W) + off) % (W + 40) - 20; y = rr.uniform(o['y0'], o['y1']); r = rr.uniform(10, 22)
        md.ellipse([x - r, y - r * 0.4, x + r, y + r * 0.4], fill=int(140 * o['dens']))
    im.paste(o['color'], (0, 0), m.filter(ImageFilter.GaussianBlur(3)))

@fx('torch')
def _fx_torch(d, im, e, f):
    """A flame on a wall or a stick, flickering, with its glow. x, y (the flame's base), size."""
    o = _o(e, x=W // 2, y=24, size=1.0)
    x, y, k = o['x'], o['y'], o['size']
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse([x - 20 * k, y - 22 * k, x + 20 * k, y + 14 * k], fill=55)
    im.paste((255, 170, 80), (0, 0), g.filter(ImageFilter.GaussianBlur(7))); d = ImageDraw.Draw(im)
    rr = loop.rng(loop.frame(f) // 2, salt=int(x) * 31 + int(y))  # changes every other frame
    for _ in range(3):
        h = rr.randint(4, 7) * k; dx = rr.randint(-1, 1)
        d.polygon([(x - 2 * k + dx, y), (x + dx, y - h), (x + 2 * k + dx, y)], fill=rr.choice([(255, 200, 70), (255, 120, 40)]))
    d.point((x, y - 1), fill=(255, 245, 200))

@fx('stars')
def _fx_stars(d, im, e, f):
    """A starry sky, the stars twinkling. n, area (x0, y0, x1, y1)."""
    o = _o(e, n=40, area=(0, 0, W, 30))
    x0, y0, x1, y1 = o['area']; rr = random.Random(71)
    for i in range(o['n']):
        x, y, off = rr.randint(x0, x1 - 1), rr.randint(y0, y1 - 1), rr.random()
        b = 0.55 + 0.45 * math.sin(2 * math.pi * ((loop.phase(f, 36) + off) % 1))
        d.point((x, y), fill=tuple(int(v * b) for v in (220, 226, 255)))

@fx('flashes')
def _fx_flashes(d, im, e, f):
    """Phones and cameras flashing in a crowd. area (x0, y0, x1, y1), n (at a time)."""
    o = _o(e, area=(0, 4, W, 26), n=4)
    x0, y0, x1, y1 = o['area']; rr = loop.rng(f, salt=83)
    for _ in range(rr.randint(0, o['n'])):
        x, y = rr.randint(x0, x1 - 1), rr.randint(y0, y1 - 1)
        d.point((x, y), fill=(255, 255, 255))
        if rr.random() < 0.3: d.point((x - 1, y), fill=(200, 200, 210)); d.point((x + 1, y), fill=(200, 200, 210))
