"""scripts/check.py and engine/director.py: the rules a clip is checked against (loops, the font, how
long text stays up, text cut off by the edge), and the text director that helps follow them.

Every theme is checked; the problems already known are in tests/check_baseline.txt, and the test fails
only on new ones (fix one and drop its line, or rerun python3 scripts/check.py --baseline)."""
import os, sys, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src')); sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import check                                    # noqa: E402
from engine import W, H, hold, wrap, fit, cue   # noqa: E402

class Director(unittest.TestCase):
    def test_hold_follows_the_rule(self):
        self.assertEqual(hold('DON!'), 20)                              # never under 1 s
        self.assertEqual(hold('A B C D E F'), 34)                       # 0.5 s + 6 x 0.2 s = 1.7 s
        self.assertTrue(cue(10, 10, 'HEY') and cue(29, 10, 'HEY') and not cue(30, 10, 'HEY'))

    def test_wrap_fits_and_keeps_lines_even(self):
        lines = wrap('YOU WERE TRYING TO CROSS THE BORDER, RIGHT?', 100)
        self.assertEqual(lines, ['YOU WERE TRYING TO', 'CROSS THE BORDER, RIGHT?'])
        self.assertTrue(all(len(l) * 4 - 1 <= 100 for l in lines))

    def test_fit_picks_the_biggest_scale_that_fits(self):
        s, lines = fit('THE VIEW FROM THE TOP', (80, 2, 183, 62))
        self.assertEqual((s, lines), (3, ['THE VIEW', 'FROM', 'THE TOP']))
        self.assertEqual(fit('A VERY LONG LINE THAT CANNOT POSSIBLY BE BIG', (0, 0, 60, 10))[0], 1)

class Rules(unittest.TestCase):
    def problems(self, texts, n=60): return check.text_problems(texts, n, W, H, hold)

    def test_a_short_line_is_flagged_and_a_long_enough_one_is_not(self):
        texts = [[('SAY MY NAME', 10, 10, 50, 14)] if f < 10 else [] for f in range(60)]
        self.assertEqual([p[0] for p in self.problems(texts)], ['short'])
        texts = [[('SAY MY NAME', 10, 10, 50, 14)] if f < 25 else [] for f in range(60)]
        self.assertEqual(self.problems(texts), [])

    def test_a_blink_a_scoreboard_and_a_typed_line_count_as_one_showing(self):
        blink = [[('FIX THE LIGHTS', 10, 10, 60, 14)] if f < 40 and (f // 6) % 2 == 0 else [] for f in range(60)]
        score = [[(f'CAI {f // 10}-0 RAC', 10, 2, 50, 6)] for f in range(60)]
        typed = [[('THE IMPOSTOR.'[:3 + f // 3], 10, 10, 60, 14)] if f < 50 else [] for f in range(60)]
        for texts in (blink, score, typed): self.assertEqual(self.problems(texts), [], texts[0])

    def test_words_and_numbers_alone_are_not_lines(self):
        self.assertEqual(self.problems([[('POW!', 10, 10, 26, 14)] if f < 4 else [] for f in range(60)]), [])

    def test_text_left_off_the_edge_is_flagged_but_passing_through_is_not(self):
        stuck = [[('GAME OVER', 170, 10, 205, 14)] for f in range(60)]
        flying = [[('GAME OVER', 200 - f * 3, 10, 235 - f * 3, 14)] for f in range(60)]
        self.assertIn('cut off', [p[0] for p in self.problems(stuck)])
        self.assertNotIn('cut off', [p[0] for p in self.problems(flying)])

class Themes(unittest.TestCase):
    def test_no_new_problems_beyond_the_known_ones(self):
        known = check.baseline()
        new = [msg for ps in check.check().values() for k, msg in ps if k not in known]
        self.assertEqual(new, [], 'new problems (python3 scripts/check.py <theme> to see them in context)')

if __name__ == '__main__':
    unittest.main()
