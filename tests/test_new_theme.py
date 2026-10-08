"""scripts/new_theme.py (nf new-theme): the skeleton it writes, for every flag combination, must import,
render every frame, loop (frame N is frame 0) and pass `nf check`; and the README gets its table row and
its place in the source tree. Everything runs on a temporary copy of the repo (src/, scripts/, README),
so the real src/ and README are never touched."""
import os, re, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import new_theme                                                    # noqa: E402

VARIANTS = {   # id: flags
    'nt-plain': {},
    'nt-people': dict(people=True),
    'nt-stage': dict(stage=True),
    'nt-both': dict(people=True, stage=True),
    'nt-calm': dict(fight=False),
    'nt-calm-both': dict(people=True, stage=True, fight=False),
    'arg-ntsalta': dict(people=True, stage=True),
    'dbz-ntcell': dict(parent='dbz', people=True),
}

# renders every frame of every clip of a theme in the temp copy and says whether frame N is frame 0
RENDER = '''
import random, sys, zlib
sys.path.insert(0, sys.argv[1] + '/src')
from themes import load_themes
items = load_themes()[sys.argv[2]]
assert items, 'no clips'
for name, n, fn, _ in items:
    assert n % 12 == 0, f'{name}: {n} is not a multiple of 12'
    random.seed(zlib.crc32(name.encode())); first = fn(0).convert('RGB').tobytes()
    for f in range(1, n): fn(f).convert('RGB')
    random.seed(zlib.crc32(name.encode()))
    assert fn(n).convert('RGB').tobytes() == first, f'{name}: frame {n} is not frame 0'
print('ok')
'''

def make_root():
    """A temporary copy of what the generator touches: src/, scripts/, the README, the check baseline."""
    tmp = tempfile.mkdtemp()
    for d in ('src', 'scripts'): shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d), ignore=shutil.ignore_patterns('__pycache__'))
    os.makedirs(os.path.join(tmp, 'tests'))
    shutil.copy(os.path.join(ROOT, 'tests', 'check_baseline.txt'), os.path.join(tmp, 'tests'))
    shutil.copy(os.path.join(ROOT, 'README.md'), tmp)
    return tmp

def read(path):
    with open(path) as fh: return fh.read()

def table_rows(text):
    """The rows of the themes table (the one headed | Theme |)."""
    lines = text.split('\n'); i = next(i for i, l in enumerate(lines) if l.startswith('| Theme |')) + 2
    rows = []
    while i < len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i += 1
    return rows

class NewTheme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_root(); cls.readme = os.path.join(cls.root, 'README.md')
        cls.before = read(cls.readme); cls.paths = {}
        for tid, flags in VARIANTS.items(): cls.paths[tid] = new_theme.create(tid, root=cls.root, **flags)
        cls.after = read(cls.readme)

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.root, ignore_errors=True)

    def test_every_variant_renders_every_frame_and_loops(self):
        for tid in VARIANTS:
            r = subprocess.run([sys.executable, '-c', RENDER, self.root, tid], capture_output=True, text=True)
            self.assertEqual((r.returncode, r.stdout.strip()), (0, 'ok'), f'{tid}: {r.stderr[-800:]}')

    def test_nf_check_finds_nothing(self):
        r = subprocess.run([sys.executable, os.path.join(self.root, 'scripts', 'check.py'), *VARIANTS],
                           cwd=self.root, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual([l for l in r.stdout.split('\n') if l.strip() and l.endswith(': ok') is False], [], r.stdout)

    def test_the_readme_gets_one_row_each_and_a_place_in_the_tree(self):
        old, new = table_rows(self.before), table_rows(self.after)
        self.assertEqual(len(new), len(old) + len(VARIANTS))
        self.assertEqual(new[:len(old)], old)                       # the others untouched
        for tid, flags in VARIANTS.items():
            mod = tid.replace('-', '_') + '.py'
            self.assertEqual(sum(l.startswith(f'| `{tid}` |') for l in new), 1, tid)
            self.assertEqual(len(re.findall(rf'\b{re.escape(mod)}\b', self.after)) - len(re.findall(rf'\b{re.escape(mod)}\b', self.before)), 1, mod)
            line = next(l for l in self.after.split('\n') if mod in l and '├──' in l)
            self.assertEqual('# sub-themes' in line, bool(flags.get('parent')), f'{mod} on the wrong tree line')
        row = next(l for l in new if l.startswith('| `nt-calm` |'))
        self.assertIn('no fight', row)

    def test_running_it_again_refuses(self):
        for tid, flags in VARIANTS.items():
            with self.assertRaises(new_theme.NewThemeError): new_theme.create(tid, root=self.root, **flags)
        self.assertEqual(read(self.readme), self.after)      # and the README is left alone
        r = new_theme.main(['nt-plain'], root=self.root)
        self.assertEqual(r, 1)

    def test_bad_ids_and_parents_are_refused(self):
        for bad in ('Nope', 'two words', 'under_score', '-x', 'x-', 'a--b', ''):
            with self.assertRaises(new_theme.NewThemeError, msg=bad): new_theme.create(bad, root=self.root)
        with self.assertRaises(new_theme.NewThemeError): new_theme.create('nt-orphan', parent='no-such-theme', root=self.root)
        self.assertFalse(os.path.exists(os.path.join(self.root, 'src', 'themes', 'nt_orphan.py')))
        with self.assertRaises(new_theme.NewThemeError): new_theme.create('ntcell', parent='dbz', root=self.root)   # not dbz-...
        self.assertFalse(os.path.exists(os.path.join(self.root, 'src', 'themes', 'ntcell.py')))

    def test_arg_themes_never_set_default_off_and_others_only_comment_it(self):
        self.assertNotIn('DEFAULT_OFF', read(self.paths['arg-ntsalta']))
        for tid, path in self.paths.items():
            if tid.startswith('arg'): continue
            lines = [l for l in read(path).split('\n') if 'DEFAULT_OFF' in l]
            self.assertTrue(lines and all(l.startswith('# ') for l in lines), tid)

    def test_effect_names_are_prefixed_and_new(self):
        taken = new_theme.fx_names(ROOT)                            # the real repo's names
        prefixes = {}
        for tid, path in self.paths.items():
            names = re.findall(r"@fx\('([^']+)'\)", read(path))
            self.assertTrue(names, tid)
            pre = {n.split('_')[0] for n in names}
            self.assertEqual(len(pre), 1, f'{tid}: {names}')
            self.assertTrue(all(n.startswith(next(iter(pre)) + '_') for n in names))
            self.assertFalse(set(names) & taken, f'{tid} reuses an effect name')
            prefixes[tid] = next(iter(pre))
        self.assertEqual(len(set(prefixes.values())), len(prefixes), prefixes)   # two new themes never share one

    def test_the_skeleton_has_what_it_promises(self):
        for tid, path in self.paths.items():
            text = read(path)
            for need in ('TODO', f"THEME = '{tid}'", 'N_ = 120', 'register_bg(', 'closeup(', 'cue(f,', 'hold(', 'fireflies'):
                self.assertIn(need, text, f'{tid}: {need}')
            self.assertEqual('Stage(' in text, 'both' in tid or 'stage' in tid or tid.startswith('arg'), tid)
            self.assertEqual('figure(' in text, tid in ('nt-people', 'nt-both', 'nt-calm-both', 'arg-ntsalta', 'dbz-ntcell'), tid)
        self.assertNotIn('RIVAL', read(self.paths['nt-calm']))
        self.assertIn('from themes.dbz import', read(self.paths['dbz-ntcell']))

class Readme(unittest.TestCase):
    def test_the_readme_path_can_be_given_by_the_environment(self):
        root = make_root(); mine = os.path.join(root, 'mine.md')
        shutil.copy(os.path.join(root, 'README.md'), mine)
        try:
            os.environ['NOTCH_FIGHT_README'] = mine
            new_theme.create('nt-env', root=root)
        finally: os.environ.pop('NOTCH_FIGHT_README', None)
        self.assertIn('| `nt-env` |', read(mine))
        self.assertNotIn('nt-env', read(os.path.join(root, 'README.md')))
        shutil.rmtree(root, ignore_errors=True)

if __name__ == '__main__':
    unittest.main()
