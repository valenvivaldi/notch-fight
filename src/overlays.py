"""Overlays the app draws on top of whatever clip is playing (transparent W×H frames, packed like clips):

- overlays/wait:  Claude is waiting for you (a permission prompt, a question): the panel's edge pulses in
                  Claude's orange and a banner with the spinning asterisk says NEEDS YOU. It loops (WAIT_N
                  frames, 1 s) for as long as the session waits.
- overlays/count: how many sessions are working, when more than one: frame i is the badge for i+2 sessions
                  (the last one, COUNT_MAX, also stands for more), a small asterisk and the number in the
                  bottom right corner."""
from engine import *
from transitions import asterisk_thick

ORANGE = (217, 119, 87)
WAIT_N = 20                                                    # 1 s at 20 fps; every period divides it
COUNT_MAX = 9

def _pulse(f, lo, hi):
    """lo..hi and back once per WAIT_N frames (exact at f = 0 and f = WAIT_N: the loop closes)."""
    return round(lo + (hi - lo) * (1 - math.cos(2 * math.pi * f / WAIT_N)) / 2)

def wait_frame(f):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    a = _pulse(f, 90, 255)
    for i, alpha in ((0, a), (1, a * 2 // 3), (2, a // 3)):   # the edge, fading inwards
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=ORANGE + (alpha,))
    bw, bh = 118, 22; x0, y0 = (W - bw) // 2, (H - bh) // 2
    d.rectangle([x0, y0, x0 + bw - 1, y0 + bh - 1], fill=(0, 0, 0, 230), outline=ORANGE + (255,))
    # a quarter turn per loop (the asterisk looks the same every 90°): the angle is f'·0.25 rad
    asterisk_thick(d, x0 + 13, y0 + bh // 2, 7, 2 * math.pi * f / WAIT_N, ORANGE + (255,))
    label = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    big_text(label, 'NEEDS YOU', y0 + 5, (255, 255, 255, 255), scale=2, cx=x0 + 24 + (bw - 24) // 2, shadow=None)
    return Image.alpha_composite(im, label)

def count_frame(n):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    txt = str(n) if n < COUNT_MAX else f'{COUNT_MAX}+'
    w = 13 + len(txt) * 4; x0, y0 = W - w - 3, H - 11
    d.rounded_rectangle([x0, y0, x0 + w - 1, y0 + 8], radius=2, fill=(0, 0, 0, 200), outline=ORANGE + (255,))
    asterisk_thick(d, x0 + 5, y0 + 4, 3, 0, ORANGE + (255,))
    text(d, txt, x0 + 10, y0 + 2, (255, 255, 255, 255), shadow=None)
    return im

def wait_frames(): return [wait_frame(f) for f in range(WAIT_N)]
def count_frames(): return [count_frame(n) for n in range(2, COUNT_MAX + 1)]
