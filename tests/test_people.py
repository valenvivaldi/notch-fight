"""engine/people.py's figure(): a person from a body spec and a pose (the six themes that build people
from poses use it, and render the same as before; tests/test_snapshots.py holds them to that)."""
import os, sys, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from engine.people import figure, figure_point, POSES   # noqa: E402

SPEC = dict(name='test-person', hair=['.hhhhh.', 'hhhhhhh', 'hh.....'], body=dict(collar='w', belt='B'))

class Figure(unittest.TestCase):
    def test_every_shared_pose_builds_inside_its_grid(self):
        for name, pose in POSES.items():
            spr = figure(SPEC, pose)
            self.assertEqual((len(spr), len(spr[0])), (26, 26), name)
            self.assertTrue(any(ch != '.' for ch in spr[-1]), f'{name}: feet on the bottom row')
            self.assertTrue(any('h' in row for row in spr), f'{name}: the hair is there')

    def test_poses_differ_and_flags_matter(self):
        self.assertNotEqual(figure(SPEC, POSES['guard']), figure(SPEC, POSES['jab']))
        shut = dict(SPEC, name='test-shut')
        self.assertNotEqual(figure(shut, POSES['stand']), figure(shut, POSES['stand'], shut=True))

    def test_it_is_cached(self):
        self.assertIs(figure(SPEC, POSES['hook']), figure(SPEC, POSES['hook']))

    def test_painters_add_details_at_their_stage(self):
        def tie(g, at): g[at['ty'] + 2][at['c'] + 1] = 't'
        spr = figure(dict(SPEC, name='test-tie', paint={'body': [tie]}), POSES['stand'])
        self.assertIn('t', ''.join(spr))

    def test_figure_point_finds_the_hand(self):
        spr = figure(SPEC, POSES['point'])
        x, y = figure_point(SPEC, POSES['point'], 'hand', 50, 58)
        cx, cy = x - (50 - 26 // 2), y - (58 - 26)
        self.assertEqual(spr[cy][cx], 's')
        fx, _ = figure_point(SPEC, POSES['point'], 'hand', 50, 58, flip=True)
        self.assertEqual(fx - 50, -(x - 50) - 1)                      # mirrored round the centre column

if __name__ == '__main__':
    unittest.main()
