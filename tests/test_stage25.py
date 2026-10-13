"""engine/stage25.py: the 2.5D floor (projection, depth, sizes, order, paths)."""
import os, sys, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from engine import Stage, arc, shrink  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

SPR = ['..aa..', '.aaaa.', 'aaaaaa', '.a..a.', '.a..a.']

class Projection(unittest.TestCase):
    def test_vanishing_point(self):
        st = Stage(far_y=33, near_y=62, vp_x=40, far_scale=0.62)
        self.assertEqual(st.proj(140, 1), (140, 62))                       # near: as is
        x, y = st.proj(140, 0)
        self.assertAlmostEqual(x, 40 + 100 * 0.62); self.assertEqual(y, 33)
        self.assertEqual(st.proj(40, 0.3)[0], 40)                          # the vanishing x never moves
        self.assertAlmostEqual(st.proj(100, 1, 10)[1], 52)                 # height, full size near
        self.assertAlmostEqual(st.proj(100, 0, 10)[1], 33 - 6.2)           # and smaller far

    def test_camera_and_parallax(self):
        st = Stage(far_y=46, near_y=58, parallax=0.1, round_feet=True)
        self.assertEqual(st.x(200, 1, cam=100), 100)
        self.assertAlmostEqual(st.x(200, 0, cam=100), 110)                 # the far side lags behind
        self.assertEqual(st.feet(0.5), 52); self.assertIsInstance(st.feet(0.37), int)

    def test_depth_is_the_inverse_of_feet(self):
        st = Stage(far_y=30, near_y=60)
        for z in (0, 0.25, 0.8, 1): self.assertAlmostEqual(st.depth(st.feet(z)), z)

class Figures(unittest.TestCase):
    def test_far_ones_are_smaller_and_faded(self):
        st = Stage(far_y=30, near_y=60, far_k=0.75, far_alpha=0.8)
        near, far = st.place(SPR, 50, 0.9), st.place(SPR, 50, 0.2, alpha=0.5)
        self.assertEqual(near['spr'], SPR); self.assertNotIn('alpha', near)
        self.assertEqual(far['spr'], shrink(SPR, 0.75)); self.assertAlmostEqual(far['alpha'], 0.4)

    def test_place_at_a_screen_point(self):
        st = Stage(far_y=30, near_y=60, far_k=0.75)
        a, b = st.place_at(SPR, 40, 35), st.place_at(SPR, 40, 55)
        self.assertEqual((a['x'], a['y'], a['spr']), (40, 35, shrink(SPR, 0.75)))
        self.assertEqual(b['spr'], SPR)

    def test_back_to_front_is_stable(self):
        self.assertEqual(Stage.back_to_front([(0.9, 'a'), (0.2, 'b'), (0.9, 'c'), (0.5, 'd')]), ['b', 'd', 'a', 'c'])

    def test_shadow_lands_on_the_floor(self):
        st = Stage(far_y=30, near_y=60); im = Image.new('RGB', (185, 64))
        st.shadow(im, 90, 1, 5, (200, 0, 0))
        self.assertGreater(im.getpixel((90, 60))[0], 0); self.assertEqual(im.getpixel((90, 50)), (0, 0, 0))

    def test_quad_and_line_draw_in_perspective(self):
        st = Stage(far_y=30, near_y=60, vp_x=92, far_scale=0.5); im = Image.new('RGB', (185, 64)); d = ImageDraw.Draw(im)
        st.quad(d, 20, 160, 0, 1, (255, 255, 255))
        self.assertEqual(im.getpixel((92, 45)), (255, 255, 255))
        self.assertEqual(im.getpixel((25, 31)), (0, 0, 0))                 # the far edge is narrower
        st.line(d, (0, 0.5, 10), (184, 0.5, 10), (255, 0, 0))

class Paths(unittest.TestCase):
    def test_arc(self):
        self.assertEqual(arc((0, 0, 0), (10, 1, 4), 5, 0), (0, 0, 0))
        self.assertEqual(arc((0, 0, 0), (10, 1, 4), 5, 1), (10, 1, 4))
        self.assertAlmostEqual(arc((0, 0, 0), (10, 1, 4), 5, 0.5)[2], 2 + 5)
        self.assertEqual(arc((0, 0, 0), (10, 1, 4), 5, 2), (10, 1, 4))     # clamped

    def test_ring(self):
        st = Stage(far_y=30, near_y=60)
        self.assertEqual(st.ring(90, 0.5, 40, 0.3, 0), (130, 0.5))
        wx, z = st.ring(90, 0.5, 40, 0.3, 3.14159 / 2)
        self.assertAlmostEqual(wx, 90, places=3); self.assertAlmostEqual(z, 0.8, places=3)   # the near half

if __name__ == '__main__':
    unittest.main()
