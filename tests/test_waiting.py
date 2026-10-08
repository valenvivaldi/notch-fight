"""Claude waiting for you: the hook marks the session ("<pid> waiting") on a permission prompt and takes it
off once a tool ran, keeping the marker's date (when the prompt started); the hook installer wires the
events; nf reads the new markers; the overlays the app draws loop and stay inside the panel.

The hook runs against a temporary HOME, with `python3` and `pkill` stubbed out on PATH: no app is
started or signalled."""
import json, os, stat, subprocess, sys, tempfile, time, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HOOK = os.path.join(ROOT, 'scripts', 'notch-hook.sh')
sys.path.insert(0, os.path.join(ROOT, 'scripts')); sys.path.insert(0, os.path.join(ROOT, 'src'))
import nf, hooks, overlays  # noqa: E402
from engine import W, H  # noqa: E402

SID = 'abc-123'

class Hook(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()
        self.dir = os.path.join(self.home, '.config', 'notch-fight', 'sessions'); os.makedirs(self.dir)
        self.marker = os.path.join(self.dir, SID)
        stubs = os.path.join(self.home, 'stubs'); os.makedirs(stubs)
        for name in ('python3', 'pkill'):
            p = os.path.join(stubs, name); open(p, 'w').write('#!/bin/sh\nexit 0\n'); os.chmod(p, stat.S_IRWXU)
        self.env = dict(os.environ, HOME=self.home, PATH=stubs + os.pathsep + os.environ['PATH'])

    def hook(self, *args):
        payload = json.dumps({'session_id': SID, 'hook_event_name': 'x', 'notification_type': 'permission_prompt'})
        t0 = time.time()
        subprocess.run(['bash', HOOK, *args], input=payload, env=self.env, capture_output=True, text=True, timeout=10, check=True)
        return time.time() - t0

    def mark(self, content, age=600):
        open(self.marker, 'w').write(content + '\n')
        t = time.time() - age; os.utime(self.marker, (t, t)); return t

    def read(self): return open(self.marker).read().split()

    def test_wait_marks_it_and_work_takes_it_off_keeping_the_date(self):
        t = self.mark('4242')
        self.hook('wait', '/nowhere/NotchFight.app')
        self.assertEqual(self.read(), ['4242', 'waiting'])
        self.assertAlmostEqual(os.path.getmtime(self.marker), t, delta=1)
        self.hook('work')
        self.assertEqual(self.read(), ['4242'])
        self.assertAlmostEqual(os.path.getmtime(self.marker), t, delta=1)
        self.assertEqual([f for f in os.listdir(self.dir) if f.startswith('.')], [])   # no temp file left

    def test_work_leaves_a_working_session_alone_and_is_quick(self):
        self.mark('4242'); before = os.stat(self.marker)
        secs = min(self.hook('work') for _ in range(3))
        after = os.stat(self.marker)
        self.assertEqual((before.st_ino, before.st_mtime), (after.st_ino, after.st_mtime))   # not even rewritten
        self.assertLess(secs, 0.25)

    def test_work_without_a_marker_does_nothing(self):
        self.hook('work')
        self.assertEqual(os.listdir(self.dir), [])

    def test_stop_reads_a_waiting_marker_of_another_live_session(self):
        other = os.path.join(self.dir, 'other')
        open(other, 'w').write(f'{os.getpid()} waiting\n')                  # this test runner: alive
        self.mark('4242'); self.hook('stop')
        self.assertFalse(os.path.exists(self.marker))
        self.assertTrue(os.path.exists(other))                                 # still working: kept

class Markers(unittest.TestCase):
    def test_read_marker(self):
        d = tempfile.mkdtemp()
        for content, want in (('123\n', (123, False)), ('123 waiting\n', (123, True)), ('', (0, False)), ('x', (0, False))):
            p = os.path.join(d, 'm'); open(p, 'w').write(content)
            self.assertEqual(nf.read_marker(p), want, content)

    def test_live_sessions_counts_the_waiting_ones(self):
        d = tempfile.mkdtemp(); saved = nf.SESSIONS; nf.SESSIONS = d
        try:
            open(os.path.join(d, 'a'), 'w').write(f'{os.getpid()}\n')
            open(os.path.join(d, 'b'), 'w').write(f'{os.getpid()} waiting\n')
            self.assertEqual(nf.live_sessions(waiting=True), (2, 1))
            self.assertEqual(nf.live_sessions(), 2)
        finally: nf.SESSIONS = saved

class Install(unittest.TestCase):
    def test_install_wires_the_events_and_uninstall_takes_them_all_off(self):
        d = tempfile.mkdtemp(); path = os.path.join(d, 'settings.json')
        json.dump({'hooks': {'PostToolUse': [{'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': 'mine'}]}]}}, open(path, 'w'))
        env = dict(os.environ, NOTCH_FIGHT_CLAUDE_DIRS=d)
        subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'hooks.py'), 'install', '/x/NotchFight.app'], env=env, check=True, capture_output=True)
        h = json.load(open(path))['hooks']
        cmds = lambda ev: [x['command'] for g in h.get(ev, []) for x in g['hooks']]
        self.assertTrue(any(' wait ' in c for c in cmds('Notification')))
        waits = [g for g in h['Notification'] if any(' wait ' in x['command'] for x in g['hooks'])]
        self.assertIn('permission_prompt', waits[0]['matcher'])
        for ev in ('PostToolUse', 'PostToolUseFailure', 'ElicitationResult'):
            self.assertTrue(any(c.endswith(' work') for c in cmds(ev)), ev)
        self.assertIn('mine', cmds('PostToolUse'))                             # the user's own hook stays
        subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'hooks.py'), 'install', '/x/NotchFight.app'], env=env, check=True, capture_output=True)
        h = json.load(open(path))['hooks']
        self.assertEqual(sum(c.endswith(' work') for c in cmds('PostToolUse')), 1)   # re-running doesn't duplicate
        subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'hooks.py'), 'uninstall'], env=env, check=True, capture_output=True)
        self.assertEqual(json.load(open(path))['hooks'], {'PostToolUse': [{'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': 'mine'}]}]})

class HookState(unittest.TestCase):
    """nf status tells per profile whether our hooks are current, old (no waiting alert), or another copy's."""
    def profile(self, cmds):
        d = tempfile.mkdtemp()
        json.dump({'hooks': {'X': [{'hooks': [{'type': 'command', 'command': c} for c in cmds]}]}}, open(os.path.join(d, 'settings.json'), 'w'))
        return d
    def test_states(self):
        mine = os.path.join(ROOT, 'scripts', 'notch-hook.sh')
        self.assertIsNone(nf.hook_state(self.profile(['echo hi'])))
        self.assertIsNone(nf.hook_state(tempfile.mkdtemp()))
        self.assertEqual(nf.hook_state(self.profile([f'{mine} start /a.app', f'{mine} stop'])), 'old: run ./install.sh')
        self.assertEqual(nf.hook_state(self.profile([f'{mine} start /a.app', f'{mine} work'])), 'current')
        self.assertTrue(nf.hook_state(self.profile(['/elsewhere/nf/scripts/notch-hook.sh stop'])).startswith('another copy: /elsewhere/nf'))

class Overlays(unittest.TestCase):
    def test_the_alert_loops(self):
        self.assertEqual(overlays.wait_frame(0).tobytes(), overlays.wait_frame(overlays.WAIT_N).tobytes())
    def test_frames_are_transparent_panels(self):
        for fr in overlays.wait_frames() + overlays.count_frames():
            self.assertEqual((fr.mode, fr.size), ('RGBA', (W, H)))
        self.assertEqual(overlays.count_frames()[0].getpixel((W // 2, H // 2))[3], 0)   # only the corner is drawn
        self.assertEqual(len(overlays.count_frames()), overlays.COUNT_MAX - 1)

if __name__ == '__main__':
    unittest.main()
