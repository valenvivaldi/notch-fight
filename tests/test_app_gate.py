"""The app's gate (app/Gate.swift, run as `NotchFight --gate`) answers exactly like `nf gate` (scripts/nf.py):
same verdict, same reason, for pauses, quiet hours (past midnight, weekdays) and screen sharing.
"Now" is fixed on both sides (NOTCH_FIGHT_NOW for the app). Skipped when there is no build or no Mac."""
import datetime, json, os, platform, subprocess, sys, tempfile, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import nf  # noqa: E402

BIN = os.path.join(ROOT, 'build', 'NotchFight.app', 'Contents', 'MacOS', 'NotchFight')
HAS_APP = platform.system() == 'Darwin' and os.path.exists(BIN)
NO_SHARE = {'pauseOnShare': False}

def at(day, hh, mm=0): return datetime.datetime(2026, 9, day, hh, mm)   # 2026-09-28 is a Monday

@unittest.skipUnless(HAS_APP, 'needs macOS and ./build.sh')
class SameAnswer(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.saved = (nf.CONFIG, nf.STATE_DIR, nf.PAUSED)
        nf.CONFIG, nf.STATE_DIR, nf.PAUSED = os.path.join(self.dir, 'config.json'), self.dir, os.path.join(self.dir, 'paused')
    def tearDown(self): nf.CONFIG, nf.STATE_DIR, nf.PAUSED = self.saved

    def app(self, now):
        env = dict(os.environ, NOTCH_FIGHT_CONFIG=nf.CONFIG, NOTCH_FIGHT_NOW=str(now.timestamp()))
        r = subprocess.run([BIN, '--gate'], env=env, capture_output=True, text=True, timeout=30)
        return r.returncode == 0, r.stdout.strip()

    def same(self, cfg, now, paused=None):
        """Both sides from the same config and pause file (rewritten before each: an expired pause is removed)."""
        json.dump(cfg, open(nf.CONFIG, 'w'))
        def setup():
            if paused is not None: json.dump(paused, open(nf.PAUSED, 'w'))
        setup(); swift = self.app(now)
        setup(); python = nf.gate(cfg, now)
        self.assertEqual(swift, python, f'{cfg} {now} {paused}')
        return swift

    def test_nothing_set_shows(self):
        self.assertEqual(self.same(NO_SHARE, at(29, 12)), (True, 'showing'))

    def test_quiet_hours(self):
        windows = [{'from': '13:00', 'to': '14:00', 'days': 'all'}, {'from': '22:00', 'to': '08:00', 'days': 'all'},
                   {'from': '22:00', 'to': '08:00', 'days': 'weekdays'}, {'from': '09:00', 'to': '09:00', 'days': 'all'}]
        # Monday 29th .. Sunday 4th, around the edges of the windows
        times = [at(29, h, m) for h, m in ((7, 59), (8, 0), (12, 0), (13, 0), (13, 59), (14, 0), (21, 59), (22, 0), (23, 30))]
        times += [datetime.datetime(2026, 10, d, h) for d in (2, 3, 4, 5) for h in (3, 23)]   # Fri .. Mon
        for q in windows:
            for now in times: self.same(dict(NO_SHARE, quiet=q), now)
        self.assertFalse(self.same(dict(NO_SHARE, quiet=windows[1]), at(29, 23))[0])

    def test_pauses(self):
        now = at(29, 12)
        self.assertEqual(self.same(NO_SHARE, now, {'until': None}), (False, 'paused until resumed'))
        ok, why = self.same(NO_SHARE, now, {'until': now.timestamp() + 90 * 60})
        self.assertEqual((ok, why), (False, 'paused until 13:30'))
        self.assertEqual(self.same(NO_SHARE, now, {'until': now.timestamp() - 60}), (True, 'showing'))
        self.assertFalse(os.path.exists(nf.PAUSED))                       # an expired pause cleans itself up

    def test_a_pause_comes_before_quiet_hours(self):
        cfg = dict(NO_SHARE, quiet={'from': '00:00', 'to': '23:59', 'days': 'all'})
        self.assertEqual(self.same(cfg, at(29, 12), {'until': None}), (False, 'paused until resumed'))

    def test_screen_sharing(self):
        p = subprocess.Popen(['sleep', '30'])                             # stands in for Zoom's CptHost
        try:
            self.assertEqual(self.same({'shareProcesses': ['no-such-process', 'sleep']}, at(29, 12)),
                             (False, 'screen sharing (sleep)'))
            self.assertEqual(self.same({'shareProcesses': ['sleep'], 'pauseOnShare': False}, at(29, 12)), (True, 'showing'))
            self.assertEqual(self.same({'shareProcesses': ['no-such-process']}, at(29, 12)), (True, 'showing'))
        finally: p.kill(); p.wait()

if __name__ == '__main__':
    unittest.main()
