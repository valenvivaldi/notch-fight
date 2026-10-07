"""engine/loop.py and engine/ambient.py: time that loops, and ambient effects that come back to where they
started at frame N whatever the clip's length."""
import os, sys, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from engine import *          # noqa: E402,F403
from engine import loop       # noqa: E402

AMBIENT = ('rain', 'snow', 'ash', 'embers', 'fireflies', 'fog', 'torch', 'stars', 'flashes')
register_bg('test-ambient', lambda v: (v, v, v))

class Loop(unittest.TestCase):
    def tearDown(self): loop.at(None)

    def test_period_divides_the_clip_and_is_close(self):
        loop.at(300)
        for p in (7, 24, 48, 64, 100, 299):
            P = loop.period(p); self.assertEqual(300 % P, 0, p); self.assertLessEqual(abs(P - p), max(5, p // 3), p)

    def test_frame_n_is_frame_0_and_the_rest_are_themselves(self):
        loop.at(240)
        self.assertEqual([loop.frame(f) for f in (0, 1, 239, 240, 241)], [0, 1, 239, 0, 1])

    def test_wave_and_phase_close_the_loop(self):
        for n in (240, 288, 301):
            loop.at(n)
            self.assertAlmostEqual(loop.wave(n, 50, 0.3), loop.wave(0, 50, 0.3))
            self.assertEqual(loop.phase(n, 37), loop.phase(0, 37))

    def test_rng_repeats_with_the_clip(self):
        loop.at(120)
        self.assertEqual(loop.rng(120, 5).random(), loop.rng(0, 5).random())
        self.assertEqual(loop.rng(130, 5, p=10).random(), loop.rng(0, 5, p=10).random())

    def test_outside_a_clip_they_use_f_as_given(self):
        loop.at(None)
        self.assertEqual((loop.frame(500), loop.period(37)), (500, 37))

class Ambient(unittest.TestCase):
    def test_every_ambient_effect_loops_for_any_length(self):
        bad = []
        for name in AMBIENT:
            for n in (240, 300, 288, 301):
                def scn(f, name=name):
                    s = scene(f, 'test-ambient'); s['fx'].append((name, {})); return s
                _, _, frame, _ = clip(name, n, scn)
                if frame(0).tobytes() != frame(n).tobytes(): bad.append((name, n))
        self.assertEqual(bad, [])

    def test_every_ambient_effect_draws_something(self):
        loop.at(240)
        blank = scene(0, 'test-ambient')
        for name in AMBIENT:
            s = scene(37, 'test-ambient'); s['fx'].append((name, {}))
            self.assertNotEqual(render(s, 37).tobytes(), render(blank, 37).tobytes(), name)

    def test_the_engines_fire_loops_too(self):
        def scn(f):
            s = scene(f, 'test-ambient'); s['fx'].append(('fire', 90, GROUND, 3)); return s
        _, _, frame, _ = clip('fire', 250, scn)
        self.assertEqual(frame(0).tobytes(), frame(250).tobytes())

if __name__ == '__main__':
    unittest.main()
