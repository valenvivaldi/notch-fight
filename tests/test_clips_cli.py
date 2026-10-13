"""./clips.sh end to end: the commands, and the checklist driven through a pseudo-terminal."""
import json, os, pty, select, subprocess, sys, tempfile, time, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SH = os.path.join(ROOT, 'clips.sh')
HAS_BUILD = os.path.isdir(os.path.join(ROOT, 'build', 'clips'))
BUILT = sorted(os.listdir(os.path.join(ROOT, 'build', 'clips'))) if HAS_BUILD else []
CLIP = BUILT[0] if BUILT else ''                              # any real clip and theme from the build
THEME = BUILT[-1].split('__')[0] if BUILT else ''

def config_file(cfg):
    path = os.path.join(tempfile.mkdtemp(), 'config.json')
    if cfg is not None: json.dump(cfg, open(path, 'w'))
    return path

def run(path, *args):
    env = dict(os.environ, NOTCH_FIGHT_CONFIG=path)
    return subprocess.run([SH, *args], env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL)

@unittest.skipUnless(HAS_BUILD, 'needs ./build.sh')
class Commands(unittest.TestCase):
    def test_disable_a_theme_then_list(self):
        path = config_file({'scale': 1.5})
        self.assertEqual(run(path, 'disable', THEME).returncode, 0)
        cfg = json.load(open(path))
        self.assertEqual((cfg['scale'], cfg['newClips']), (1.5, 'enabled'))
        self.assertIn(BUILT[-1], cfg['disabled'])
        self.assertIn(f'off  {BUILT[-1]}', run(path, 'list').stdout)

    def test_mode_switch_keeps_the_selection(self):
        path = config_file({'newClips': 'enabled', 'disabled': [CLIP]})
        before = run(path, 'list').stdout.splitlines()[1:]
        run(path, 'mode', 'disabled')
        self.assertEqual(json.load(open(path))['newClips'], 'disabled')
        self.assertEqual(run(path, 'list').stdout.splitlines()[1:], before)

    def themes(self, path):
        return dict(l.split('\t') for l in run(path, 'themes').stdout.splitlines())

    def test_only_all_and_defaults(self):
        path = config_file({})
        self.assertEqual(run(path, 'only', THEME).returncode, 0)
        st = self.themes(path)
        self.assertEqual({t for t, s in st.items() if s != 'off'}, {THEME})
        run(path, 'all', 'off'); self.assertEqual(set(self.themes(path).values()), {'off'})
        run(path, 'all', 'on'); self.assertEqual(set(self.themes(path).values()), {'on'})
        run(path, 'defaults')
        self.assertEqual(self.themes(path), self.themes(config_file({})))      # as with an empty config

    def test_themes_says_some_when_a_theme_is_half_on(self):
        mine = [c for c in BUILT if c.split('__')[0] == THEME]
        if len(mine) < 2: self.skipTest('needs a theme with two clips')
        path = config_file({'newClips': 'enabled', 'disabled': [mine[0]]})
        self.assertEqual(self.themes(path)[THEME], 'some')

    def test_a_typo_fails_and_suggests(self):
        r = run(config_file({}), 'disable', CLIP[:-1])
        self.assertEqual(r.returncode, 1)
        self.assertIn(f'did you mean: {CLIP}', r.stderr)

    def test_without_a_terminal_it_explains_instead_of_opening_the_checklist(self):
        r = run(config_file({}))
        self.assertEqual(r.returncode, 1)
        self.assertIn('needs a real terminal', r.stdout)

@unittest.skipUnless(HAS_BUILD, 'needs ./build.sh')
class ChecklistInATerminal(unittest.TestCase):
    def drive(self, path, keys):
        """Run ./clips.sh in a pty, type keys (with pauses), return the output."""
        pid, fd = pty.fork()
        if pid == 0:                                   # the child must never fall back into the test runner
            try:
                os.environ.update(NOTCH_FIGHT_CONFIG=path, TERM='xterm', LINES='60', COLUMNS='120')
                os.execv(SH, [SH])
            finally: os._exit(127)
        out = b''
        def read(t):
            nonlocal out
            end = time.time() + t
            while time.time() < end:
                r, _, _ = select.select([fd], [], [], 0.05)
                if r:
                    try: out += os.read(fd, 65536)
                    except OSError: return
        for _ in range(100):                           # wait for the checklist to draw, not a fixed time
            read(0.1)
            if b'Notch Fight: clips' in out: break
        for k in keys:
            try: os.write(fd, k)
            except OSError: break                      # the checklist already exited
            read(0.25)
        read(1.0)
        for _ in range(20):                            # never hang: kill it if it is still running
            if os.waitpid(pid, os.WNOHANG)[0]: break
            time.sleep(0.1)
        else: os.kill(pid, 9); os.waitpid(pid, 0)
        return out.decode(errors='replace')

    def test_space_on_the_first_theme_disables_it_and_enter_saves(self):
        path = config_file({'scale': 1.5})
        out = self.drive(path, [b' ', b'\r'])
        cfg = json.load(open(path))
        first_theme = sorted(os.listdir(os.path.join(ROOT, 'build', 'clips')))[0].split('__')[0]
        self.assertTrue(cfg['disabled'] and all(c.startswith(first_theme + '__') for c in cfg['disabled']))
        self.assertEqual(cfg['scale'], 1.5)
        self.assertIn('saved', out)

    def test_m_switches_the_mode_and_q_quits_without_saving(self):
        path = config_file({'scale': 1.5})
        self.drive(path, [b'm', b'q'])
        self.assertEqual(json.load(open(path)), {'scale': 1.5})

    def test_m_then_enter_saves_the_new_mode(self):
        path = config_file({})
        self.drive(path, [b'm', b'\r'])
        cfg = json.load(open(path))
        self.assertEqual(cfg['newClips'], 'disabled')
        shipped_off = [c for c in BUILT if os.path.exists(os.path.join(ROOT, 'build', 'clips', c, '.default-off'))]
        self.assertEqual(len(cfg['enabled']), len(BUILT) - len(shipped_off))   # what played before the switch

    def test_f_clears_the_forced_clips(self):
        path = config_file({'first': [CLIP]})
        self.drive(path, [b'f', b'\r'])
        self.assertEqual(json.load(open(path))['first'], [])

    def test_saving_nothing_asks_for_a_second_enter(self):
        path = config_file({'scale': 1.5})
        self.drive(path, [b'n', b'\r', b'x', b'q'])    # a key other than enter cancels the save; q quits
        self.assertEqual(json.load(open(path)), {'scale': 1.5})

if __name__ == '__main__':
    unittest.main()
