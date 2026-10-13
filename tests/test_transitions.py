"""Transition styles (src/transitions.py): every half starts or ends on the theme's keyframe and meets the
other half at black, so any theme's out goes with any theme's in; the iris is still the iris."""
import os, sys, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from engine import *  # noqa: E402,F403
import transitions as tr  # noqa: E402

def picture():
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 7): d.line([(x, 0), (x, H - 1)], fill=(40 + x % 200, 120, 200 - x % 150))
    return im

def black_but_center(im, room):
    """Black everywhere except within `room` px of the middle (the iris's asterisk, the CRT's dot)."""
    px = im.load()
    for y in range(H):
        for x in range(W):
            if px[x, y] != (0, 0, 0) and (abs(x - W // 2) > room or abs(y - H // 2) > room + 12): return False
    return True

class Styles(unittest.TestCase):
    def test_halves_open_and_close_on_the_picture(self):
        img = picture()
        for style in tr.STYLES:
            out, inn = tr.half_out(style, img), tr.half_in(style, img)
            self.assertEqual(len(out), tr.HALF); self.assertEqual(len(inn), tr.HALF)
            if style != 'iris':                                    # the iris already shows its asterisk
                self.assertEqual(out[0].tobytes(), img.tobytes(), style)
                self.assertEqual(inn[-1].tobytes(), img.tobytes(), style)
            self.assertTrue(black_but_center(out[-1], 20), f'{style}: the out half ends black')
            self.assertTrue(black_but_center(inn[0], 20), f'{style}: the in half starts black')

    def test_generic_styles_exist(self):
        self.assertEqual(tr.GENERIC[0], 'iris')
        self.assertTrue(set(tr.GENERIC) <= set(tr.STYLES))

    def test_the_iris_is_unchanged(self):
        img = picture()
        self.assertEqual([f.tobytes() for f in tr.iris_out(img) + tr.iris_in(img)],
                         [f.tobytes() for f in tr.transition(img, img)])

if __name__ == '__main__':
    unittest.main()
