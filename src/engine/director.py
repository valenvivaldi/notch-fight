"""The text director: how long a line stays up, how it breaks into lines, how big it can be in a box,
and a close-up template, so a theme says what's written and where, and the rest follows the rules:

- hold(txt): the frames a text needs on screen: 0.5 s + 0.2 s a word, never under 1 s.
- cue(f, start, txt): is it up at frame f (from start, for hold(txt) frames)?
- wrap(txt, width, scale): the text broken into lines that fit width pixels at that scale.
- text_block(im, txt, box): the text drawn as big as fits in box (x0, y0, x1, y1), centred, wrapped.
- ('caption', txt, {box, color, max_scale, shadow, outline}): text_block as an effect.
- closeup(t, f, ...): a close-up frame: a background, your drawing, the text in its box, zoom lines."""
import math
from .core import *
from .text import big_text, glyph
from .closeup import zoom_lines
from .fx import fx

FPS = 20
READ_BASE, READ_WORD, READ_MIN = 0.5, 0.2, 1.0                     # seconds: to read a line, a word more, at least

def hold(txt, fps=FPS):
    """The frames txt needs on screen to be read: 0.5 s + 0.2 s a word, and at least 1 s."""
    return int(math.ceil(max(READ_MIN, READ_BASE + READ_WORD * len(txt.split())) * fps))

def cue(f, start, txt, extra=0):
    """True while txt, shown from frame start, is up (hold(txt) frames, plus extra)."""
    return start <= f < start + hold(txt) + extra

def wrap(txt, width, scale=1):
    """txt broken at spaces into lines no wider than width pixels at this scale (a word too long for a
    line gets one to itself)."""
    per = max(1, (width + scale) // (4 * scale))                     # characters a line holds
    lines, cur = [], ''
    for word in txt.split():                                         # as few lines as fit...
        if cur and len(cur) + 1 + len(word) > per: lines.append(cur); cur = word
        else: cur = f'{cur} {word}' if cur else word
    if cur: lines.append(cur)
    return _balance(txt.split(), len(lines), per) or lines           # ...as even as they can be

def _cost(lines):
    """Shortest longest line first, then the most even."""
    m = max(map(len, lines)); return m, sum((m - len(l)) ** 2 for l in lines)

def _balance(words, k, per):
    """words in k lines, each within per characters, the longest as short as possible (None if none)."""
    best = None
    def go(i, left, acc):
        nonlocal best
        if left == 1:
            line = ' '.join(words[i:])
            if words[i:] and len(line) <= per:
                cand = acc + [line]
                if best is None or _cost(cand) < _cost(best): best = cand
            return
        for j in range(i + 1, len(words) - left + 2):
            line = ' '.join(words[i:j])
            if len(line) > per: break
            go(j, left - 1, acc + [line])
    if 1 < k <= len(words) <= 14: go(0, k, [])
    return best

def fit(txt, box, max_scale=3):
    """(scale, lines): the biggest scale (max_scale down to 1) at which txt, wrapped, fits in box."""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    for s in range(max_scale, 0, -1):
        lines = wrap(txt, w, s)
        tall = sum((7 + (2 if any(glyph(c)[1] for c in l) else 0)) * s for l in lines) - 2 * s
        if all(len(l) * 4 * s - s <= w for l in lines) and tall <= h: return s, lines
    return 1, wrap(txt, w, 1)

def text_block(im, txt, box, color=(255, 255, 255), max_scale=3, shadow=(0, 0, 0), outline=None):
    """txt as big as fits in box, wrapped and centred in it. Returns the scale used."""
    s, lines = fit(txt, box, max_scale)
    x0, y0, x1, y1 = box
    heights = [(7 + (2 if any(glyph(c)[1] for c in l) else 0)) * s for l in lines]
    y = y0 + max(0, (y1 - y0 - (sum(heights) - 2 * s)) // 2)
    for l, hgt in zip(lines, heights):
        acc = (2 * s) if any(glyph(c)[1] for c in l) else 0
        big_text(im, l, y + acc, color, scale=s, cx=(x0 + x1) // 2, shadow=shadow, outline=outline); y += hgt
    return s

@fx('caption')
def _fx_caption(d, im, e, f):
    """('caption', txt, {box, color, max_scale, shadow, outline}): text_block as an effect."""
    o = dict(box=(2, 2, W - 2, 22), color=(255, 255, 255), max_scale=2, shadow=(0, 0, 0), outline=None)
    if len(e) > 2: o.update(e[2])
    text_block(im, e[1], o['box'], o['color'], o['max_scale'], o['shadow'], o['outline'])

def closeup(t, f, bg=(0, 0, 0), draw=None, txt=None, box=(80, 2, W - 2, H - 2), text_from=0.1,
            color=(255, 255, 255), outline=(0, 0, 0), max_scale=3, zoom=(255, 255, 255)):
    """A close-up frame (t: 0..1 through it): the background (a colour or an image), then draw(im, d, t, f)
    (it may return a new image), then txt in its box from t >= text_from, and the zoom lines at the start."""
    im = Image.new('RGB', (W, H), bg) if isinstance(bg, tuple) else bg.copy()
    d = ImageDraw.Draw(im)
    if draw:
        out = draw(im, d, t, f)
        if out is not None: im = out; d = ImageDraw.Draw(im)
    if txt and t >= text_from: text_block(im, txt, box, color, max_scale, shadow=None if outline else (0, 0, 0), outline=outline)
    if zoom and t < 0.05: zoom_lines(ImageDraw.Draw(im), zoom)
    return im
