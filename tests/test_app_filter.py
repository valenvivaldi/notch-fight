"""The app honours the clip selection in config.json, pointed at temporary configs via NOTCH_FIGHT_CONFIG.

By default the built binary runs with --print-selection: it works out the selection exactly as at launch,
prints it and exits before the app starts — no panel, and the window you are typing in keeps focus.
NOTCH_FIGHT_TEST_PANEL=1 also runs real launches (through `open -g`: the panel shows, focus stays).
Skipped when there is no build or no Mac."""
import json, os, platform, subprocess, tempfile, time, unittest

ROOT = os.path.join(os.path.dirname(__file__), '..')
APP = os.path.join(ROOT, 'build', 'NotchFight.app')
BIN = os.path.join(APP, 'Contents', 'MacOS', 'NotchFight')
CLIPS = sorted(os.listdir(os.path.join(ROOT, 'build', 'clips'))) if os.path.isdir(os.path.join(ROOT, 'build', 'clips')) else []
SHIPPED_OFF = [c for c in CLIPS if os.path.exists(os.path.join(ROOT, 'build', 'clips', c, '.default-off'))]
ON = [c for c in CLIPS if c not in SHIPPED_OFF]      # the clips that play with an empty config
HAS_APP = platform.system() == 'Darwin' and os.path.exists(BIN)

def config_file(cfg):
    path = os.path.join(tempfile.mkdtemp(), 'config.json'); json.dump(cfg, open(path, 'w')); return path

def selection(cfg, binary=BIN):
    """Run the app with --print-selection against this config; return (output, seconds, exit code)."""
    env = dict(os.environ, NOTCH_FIGHT_CONFIG=config_file(cfg)); env.pop('NOTCH_FIGHT_FIRST', None)
    t0 = time.time()
    r = subprocess.run([binary, '--print-selection'], env=env, capture_output=True, text=True, timeout=90)   # a fresh copy's first launch is slow: macOS checks the whole bundle
    return r.stdout + r.stderr, time.time() - t0, r.returncode

@unittest.skipUnless(HAS_APP, 'needs macOS and ./build.sh')
class AppSelection(unittest.TestCase):
    def test_print_selection_exits_on_its_own_without_the_panel(self):
        out, secs, code = selection({})
        self.assertEqual(code, 0)
        self.assertIn('panel: shown', out)
        self.assertLess(secs, 10)

    def test_no_selection_keys_plays_everything_shipped_on(self):
        out, _, _ = selection({})
        self.assertIn(f'{len(ON)}/{len(CLIPS)} clips active', out)

    def test_new_disabled_plays_only_the_enabled_list(self):
        out, _, _ = selection({'newClips': 'disabled', 'enabled': [CLIPS[0]]})
        self.assertIn(f'1/{len(CLIPS)} clips active', out)

    def test_new_enabled_skips_the_disabled_list(self):
        out, _, _ = selection({'newClips': 'enabled', 'disabled': ON[:2]})
        self.assertIn(f'{len(ON) - 2}/{len(CLIPS)} clips active', out)

    def test_nothing_active_means_no_panel(self):
        out, _, _ = selection({'newClips': 'disabled', 'enabled': []})
        self.assertIn('no clips active', out)
        self.assertIn('panel: hidden', out)

    def test_a_forced_clip_plays_even_when_disabled(self):
        out, _, _ = selection({'newClips': 'disabled', 'enabled': [], 'first': [CLIPS[0]]})
        self.assertIn(f'0/{len(CLIPS)} clips active', out)
        self.assertIn(f'forced: {CLIPS[0]}', out)
        self.assertIn('panel: shown', out)

    def test_unknown_names_in_the_lists_are_logged(self):
        out, _, _ = selection({'newClips': 'enabled', 'disabled': ['nope__clip']})
        self.assertIn("unknown clip 'nope__clip'", out)

@unittest.skipUnless(HAS_APP, 'needs macOS and ./build.sh')
class AppRotation(unittest.TestCase):
    """The round outlives the app: state.json (next to the config) keeps what has played, so relaunches
    carry on with the round and no clip repeats until all have. --print-rotation N plays N clips, unseen."""
    def setUp(self):
        self.five = ON[:5]
        self.cfg = config_file({'newClips': 'disabled', 'enabled': self.five})
        self.state = os.path.join(os.path.dirname(self.cfg), 'state.json')

    def play(self, n):
        env = dict(os.environ, NOTCH_FIGHT_CONFIG=self.cfg); env.pop('NOTCH_FIGHT_FIRST', None)
        r = subprocess.run([BIN, '--print-rotation', str(n)], env=env, capture_output=True, text=True, timeout=90)
        return [l.split(': ', 1)[1] for l in r.stdout.splitlines() if l.startswith('played: ')]

    def test_a_round_spans_launches_without_repeats(self):
        first, second = self.play(2), self.play(3)
        self.assertEqual(sorted(first + second), sorted(self.five))
        third = self.play(5)                                         # a new round: all five again
        self.assertEqual(sorted(third), sorted(self.five))
        self.assertNotEqual(third[0], second[-1])                    # never the same clip twice in a row

    def test_it_counts_plays(self):
        self.play(3); self.play(4)
        state = json.load(open(self.state))
        self.assertEqual(sum(state['stats']['plays'].values()), 7)
        self.assertEqual(len(state['rotation']['played']), 2)       # 3 + 4 = one round of 5, then 2 of the next

    def test_clips_turned_off_leave_the_round_and_new_ones_join(self):
        self.play(3)
        state = json.load(open(self.state)); played = state['rotation']['played']
        json.dump({'newClips': 'disabled', 'enabled': self.five + [ON[5]]}, open(self.cfg, 'w'))
        rest = self.play(3)                                          # the 2 not played yet + the new one
        self.assertEqual(sorted(rest), sorted([c for c in self.five if c not in played] + [ON[5]]))

    def test_unknown_state_keys_are_kept(self):
        json.dump({'later': {'x': 1}}, open(self.state, 'w'))
        self.play(1)
        self.assertEqual(json.load(open(self.state))['later'], {'x': 1})

@unittest.skipUnless(HAS_APP, 'needs macOS and ./build.sh')
class AppDefaultOff(unittest.TestCase):
    """A clip whose build folder has a .default-off marker stays out of the rotation until enabled."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        app = os.path.join(cls.tmp, 'NotchFight.app')
        subprocess.run(['cp', '-cR', APP, app], check=True)          # APFS clone: fast
        cls.marked = ON[0]                                          # a clip that ships on, marked off in this copy
        open(os.path.join(app, 'Contents', 'Resources', 'clips', cls.marked, '.default-off'), 'w').close()
        cls.bin = os.path.join(app, 'Contents', 'MacOS', 'NotchFight')

    def test_a_default_off_clip_is_not_active(self):
        out, _, _ = selection({}, self.bin)
        self.assertIn(f'{len(ON) - 1}/{len(CLIPS)} clips active', out)

    def test_turning_it_on_in_enabled_mode(self):
        out, _, _ = selection({'newClips': 'enabled', 'enabled': [self.marked]}, self.bin)
        self.assertIn(f'{len(ON)}/{len(CLIPS)} clips active', out)

@unittest.skipUnless(HAS_APP and os.environ.get('NOTCH_FIGHT_TEST_PANEL') == '1',
                     'real launches show the panel: opt in with NOTCH_FIGHT_TEST_PANEL=1')
class AppPanel(unittest.TestCase):
    """Real launches, in the background (`open -g -n`): the panel shows, the focused window keeps focus."""
    def launch(self, cfg, wait=3.0):
        """Launch a new instance; return (its log, whether it quit on its own within `wait` s)."""
        log = os.path.join(tempfile.mkdtemp(), 'err.log')
        p = subprocess.Popen(['open', '-g', '-n', '-W', '--env', f'NOTCH_FIGHT_CONFIG={config_file(cfg)}',
                              '--stderr', log, APP])
        try: p.wait(timeout=wait); quit_alone = True
        except subprocess.TimeoutExpired:
            quit_alone = False
            subprocess.run(['pkill', '-nx', 'NotchFight'], capture_output=True)   # the newest instance: ours
            p.wait(timeout=5)
        return (open(log).read() if os.path.exists(log) else ''), quit_alone

    def test_nothing_active_quits_without_a_panel(self):
        log, quit_alone = self.launch({'newClips': 'disabled', 'enabled': []})
        self.assertIn('no clips active', log)
        self.assertTrue(quit_alone)

    def test_a_forced_clip_keeps_the_panel_up(self):
        log, quit_alone = self.launch({'newClips': 'disabled', 'enabled': [], 'first': [CLIPS[0]]})
        self.assertIn(f'0/{len(CLIPS)} clips active', log)
        self.assertFalse(quit_alone)

if __name__ == '__main__':
    unittest.main()
