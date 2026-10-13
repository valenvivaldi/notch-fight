"""nf: pause, quiet hours, the gate the hook and the app ask, and the command line (no panel is shown)."""
import datetime, json, os, subprocess, sys, tempfile, time, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import nf  # noqa: E402

NO_SHARE = {'pauseOnShare': False}                                   # keep the process check out of it

class Temp(unittest.TestCase):
    def setUp(self):
        d = tempfile.mkdtemp()
        self.saved = (nf.CONFIG, nf.STATE_DIR, nf.PAUSED)
        nf.CONFIG, nf.STATE_DIR, nf.PAUSED = os.path.join(d, 'config.json'), d, os.path.join(d, 'paused')
    def tearDown(self): nf.CONFIG, nf.STATE_DIR, nf.PAUSED = self.saved

class Durations(unittest.TestCase):
    def test_the_forms(self):
        for s, m in (('15m', 15), ('1h', 60), ('90', 90), ('1h30m', 90), ('8h', 480), ('45min', 45)):
            self.assertEqual(nf.parse_duration(s), m, s)
        self.assertIsNone(nf.parse_duration('forever'))
    def test_nonsense_fails(self):
        for s in ('', 'soon', '1d', 'h'):
            with self.assertRaises(nf.NfError): nf.parse_duration(s)

class Seconds(unittest.TestCase):
    def test_the_forms(self):
        for s, n in (('10s', 10), ('30', 30), ('1m', 60), ('2min', 120), ('off', 0)):
            self.assertEqual(nf.parse_seconds(s), n, s)
        with self.assertRaises(nf.NfError): nf.parse_seconds('soon')

class Pause(Temp):
    def test_a_pause_closes_the_gate_until_it_ends(self):
        now = time.time()
        nf.set_pause(30, now=now)
        self.assertFalse(nf.gate(NO_SHARE, datetime.datetime.fromtimestamp(now + 60))[0])
        self.assertTrue(nf.gate(NO_SHARE, datetime.datetime.fromtimestamp(now + 31 * 60))[0])
        self.assertFalse(os.path.exists(nf.PAUSED))                   # an expired pause cleans itself up
    def test_forever_lasts_until_resumed(self):
        nf.set_pause(None)
        ok, why = nf.gate(NO_SHARE, datetime.datetime.now() + datetime.timedelta(days=30))
        self.assertEqual((ok, why), (False, 'paused until resumed'))
        os.remove(nf.PAUSED)
        self.assertTrue(nf.gate(NO_SHARE)[0])

class Quiet(unittest.TestCase):
    def at(self, day, hh, mm=0): return datetime.datetime(2026, 9, day, hh, mm)   # 2026-09-28 is a Monday
    def test_a_window_inside_one_day(self):
        q = {'from': '13:00', 'to': '14:00', 'days': 'all'}
        self.assertTrue(nf.in_quiet(q, self.at(28, 13, 30))); self.assertFalse(nf.in_quiet(q, self.at(28, 14, 0)))
    def test_a_window_past_midnight(self):
        q = {'from': '22:00', 'to': '08:00', 'days': 'all'}
        for h, inside in ((21, False), (22, True), (3, True), (8, False), (12, False)):
            self.assertEqual(nf.in_quiet(q, self.at(29, h)), inside, h)
    def test_weekdays_belong_to_the_night_they_start(self):
        q = {'from': '22:00', 'to': '08:00', 'days': 'weekdays'}
        self.assertTrue(nf.in_quiet(q, datetime.datetime(2026, 10, 2, 23)))    # Friday night
        self.assertTrue(nf.in_quiet(q, datetime.datetime(2026, 10, 3, 3)))     # ...into Saturday morning
        self.assertFalse(nf.in_quiet(q, datetime.datetime(2026, 10, 3, 23)))   # Saturday night
        self.assertFalse(nf.in_quiet(q, datetime.datetime(2026, 10, 5, 3)))    # Sunday night into Monday
    def test_the_gate_uses_it(self):
        cfg = dict(NO_SHARE, quiet={'from': '22:00', 'to': '08:00', 'days': 'all'})
        self.assertFalse(nf.gate(cfg, self.at(29, 23))[0]); self.assertTrue(nf.gate(cfg, self.at(29, 12))[0])
    def test_bad_spans_fail(self):
        for s in ('22-08', '25:00-08:00', '22:00'):
            with self.assertRaises(nf.NfError): nf.parse_quiet(s)

class Sharing(Temp):
    def test_a_running_process_from_the_list_closes_the_gate(self):
        p = subprocess.Popen(['sleep', '30'])                         # stands in for Zoom's CptHost
        try:
            cfg = {'shareProcesses': ['sleep']}
            self.assertEqual(nf.sharing(cfg), 'sleep')
            self.assertEqual(nf.gate(cfg), (False, 'screen sharing (sleep)'))
        finally: p.kill(); p.wait()
    def test_it_can_be_turned_off(self):
        self.assertIsNone(nf.sharing({'shareProcesses': ['no-such-process-here']}))

class CommandLine(unittest.TestCase):
    def run_nf(self, cfg_path, *args):
        env = dict(os.environ, NOTCH_FIGHT_CONFIG=cfg_path)
        return subprocess.run([os.path.join(ROOT, 'nf'), *args], env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    def test_quiet_and_share_write_the_config_and_gate_reads_it(self):
        d = tempfile.mkdtemp(); path = os.path.join(d, 'config.json'); json.dump({'scale': 1.5}, open(path, 'w'))
        r = self.run_nf(path, 'share', 'show'); self.assertEqual(r.returncode, 0); self.assertIn('keep showing', r.stdout)
        self.assertEqual(self.run_nf(path, 'quiet', '00:00-23:59').returncode, 0)
        cfg = json.load(open(path))
        self.assertEqual((cfg['scale'], cfg['pauseOnShare'], cfg['quiet']['from']), (1.5, False, '00:00'))
        r = self.run_nf(path, 'gate'); self.assertEqual(r.returncode, 1); self.assertIn('quiet hours', r.stdout)
        self.run_nf(path, 'quiet', 'off')
        self.assertEqual(self.run_nf(path, 'gate').returncode, 0)
    def test_delay_and_click_write_the_config(self):
        d = tempfile.mkdtemp(); path = os.path.join(d, 'config.json')
        self.assertEqual(self.run_nf(path, 'delay', '10s').returncode, 0)
        self.assertEqual(self.run_nf(path, 'click', 'next').returncode, 0)
        self.assertEqual({k: v for k, v in json.load(open(path)).items()}, {'delay': 10, 'click': 'next'})
        self.run_nf(path, 'delay', 'off'); self.run_nf(path, 'click', 'close')
        self.assertEqual(json.load(open(path)), {})
        self.assertEqual(self.run_nf(path, 'click', 'sideways').returncode, 1)
    def test_pause_needs_a_time_when_not_in_a_terminal(self):
        d = tempfile.mkdtemp(); path = os.path.join(d, 'config.json')
        r = self.run_nf(path, 'pause'); self.assertEqual(r.returncode, 1); self.assertIn('how long', r.stderr)
    def test_settings_never_kill_a_resident_app(self):
        """quiet / share used to `pkill` the app to hide it; a resident app only gets SIGUSR1 (look again).
        pkill is stubbed: it records its arguments instead (a real one would reach the real app)."""
        d = tempfile.mkdtemp(); path = os.path.join(d, 'config.json'); calls = os.path.join(d, 'calls')
        stubs = os.path.join(d, 'stubs'); os.makedirs(stubs)
        open(os.path.join(stubs, 'pkill'), 'w').write(f'#!/bin/sh\necho "$@" >> {calls}\n'); os.chmod(os.path.join(stubs, 'pkill'), 0o755)
        env = dict(os.environ, NOTCH_FIGHT_CONFIG=path, PATH=stubs + os.pathsep + os.environ['PATH'])
        for args in (('quiet', '00:00-23:59'), ('share', 'hide'), ('quiet', 'off')):
            subprocess.run([os.path.join(ROOT, 'nf'), *args], env=env, capture_output=True, stdin=subprocess.DEVNULL)
        sent = open(calls).read().splitlines() if os.path.exists(calls) else []
        self.assertTrue(sent)
        self.assertTrue(all(l.startswith('-USR1') for l in sent), sent)
    def test_unknown_commands_fail(self):
        self.assertEqual(self.run_nf(os.path.join(tempfile.mkdtemp(), 'c.json'), 'frobnicate').returncode, 2)

if __name__ == '__main__':
    unittest.main()
