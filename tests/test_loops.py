"""Every clip loops: its frame N (one past the last) is its frame 0, the theme's neutral pose, so the
last frame flows back into the first, and into the theme's other clips, with no jump. Whatever moves in
the neutral pose (the guard pose's 12-frame bob, rain, fire, a swaying cloak) has to have a period that
divides the clip's length. Renders a few frames per clip."""
import os, random, sys, unittest, zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from themes import load_themes  # noqa: E402

THEMES = load_themes()

def frame(name, fn, f):
    random.seed(zlib.crc32(name.encode()))                          # as build.py seeds it
    return fn(f).convert('RGB').tobytes()

class Loops(unittest.TestCase):
    def test_every_clip_ends_where_it_starts(self):
        bad = []
        for theme, items in THEMES.items():
            for name, n, fn, _ in items:
                if frame(name, fn, 0) != frame(name, fn, n): bad.append(f'{theme}__{name}')
        self.assertEqual(bad, [], 'frame N differs from frame 0 (the loop jumps)')

    def test_a_themes_clips_share_the_neutral_pose(self):
        bad = []
        for theme, items in THEMES.items():
            first = {frame(name, fn, 0) for name, _, fn, _ in items}
            if len(first) > 1: bad.append(theme)
        self.assertEqual(bad, [], 'clips of the same theme start on different frames')

if __name__ == '__main__':
    unittest.main()
