"""src/build.py partial builds (ONLY=<theme|theme__clip>[,...]): only the named clips and their themes'
transition halves (<theme>__out, <theme>__in, and __out__<style> / __in__<style> for the other styles)
are rendered; everything else in build/ is left as it is.
Runs on a temporary copy of src/ with two tiny synthetic themes, so it takes seconds."""
import os, shutil, subprocess, sys, tempfile, time, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

THEME = '''from engine import *
THEME = '{id}'
register_bg(THEME, lambda v: (v, v, v))
def clip_{clip}(f):
    s = scene(f, THEME); s['actors'] = [actor(CL['guard'], 30 + f * {speed})]; return s
CLIPS = [clip('{clip}', 4, clip_{clip})]
'''

def make_src(themes):
    """A copy of src/ whose only themes are the given synthetic ones: {id: (clip, speed)}."""
    tmp = tempfile.mkdtemp(); src = os.path.join(tmp, 'src')
    shutil.copytree(os.path.join(ROOT, 'src'), src)
    tdir = os.path.join(src, 'themes')
    for fn in os.listdir(tdir):
        if fn.endswith('.py') and fn != '__init__.py': os.remove(os.path.join(tdir, fn))
    for tid, (clip, speed) in themes.items(): add_theme(src, tid, clip, speed)
    out = os.path.join(tmp, 'build'); os.makedirs(out)
    return src, out

def add_theme(src, tid, clip, speed=1):
    open(os.path.join(src, 'themes', f'{tid}.py'), 'w').write(THEME.format(id=tid, clip=clip, speed=speed))

def build(src, out, only=None):
    env = dict(os.environ); env.pop('ONLY', None)
    if only is not None: env['ONLY'] = only
    return subprocess.run([sys.executable, os.path.join(src, 'build.py')], cwd=out, env=env, capture_output=True, text=True)

def mtimes(out):
    """Every file under clips/ and transitions/ with its modification time."""
    res = {}
    for top in ('clips', 'transitions'):
        for dp, _, fs in os.walk(os.path.join(out, top)):
            for fn in fs: res[os.path.relpath(os.path.join(dp, fn), out)] = os.stat(os.path.join(dp, fn)).st_mtime_ns
    return res

class PartialBuild(unittest.TestCase):
    def setUp(self):
        self.src, self.out = make_src({'ta': ('one', 1), 'tb': ('two', 2)})
        r = build(self.src, self.out); self.assertEqual(r.returncode, 0, r.stderr)

    def built(self): return open(os.path.join(self.out, '.built')).read().split()

    def test_a_full_build_lists_every_clip_as_built(self):
        self.assertEqual(sorted(self.built()), ['ta__one', 'tb__two'])
        for d in ('ta__out', 'ta__in', 'tb__out', 'tb__in'):            # two halves per theme, none per pair
            self.assertTrue(os.path.isdir(os.path.join(self.out, 'transitions', d)), d)
        styles = ['', '__crt', '__dissolve', '__wipe']                  # the first style (iris) has no suffix
        self.assertEqual(sorted(os.listdir(os.path.join(self.out, 'transitions'))),
                         sorted(f'{t}__{h}{s}' for t in ('ta', 'tb') for h in ('in', 'out') for s in styles))

    def test_a_theme_with_its_own_transition_has_only_that(self):
        path = os.path.join(self.src, 'themes', 'tc.py'); add_theme(self.src, 'tc', 'three')
        open(path, 'a').write("TRANSITION = 'curtain'\n")
        r = build(self.src, self.out, 'tc'); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(sorted(d for d in os.listdir(os.path.join(self.out, 'transitions')) if d.startswith('tc__')), ['tc__in', 'tc__out'])

    def test_clips_have_a_glow_colour_per_frame(self):
        lines = open(os.path.join(self.out, 'clips', 'ta__one', 'glow')).read().split()
        self.assertEqual(len(lines), 4)
        self.assertTrue(all(len(l) == 6 and int(l, 16) >= 0 for l in lines))

    def test_only_a_theme_rebuilds_just_it_and_its_transitions(self):
        before = mtimes(self.out); time.sleep(0.05)
        r = build(self.src, self.out, 'tb'); self.assertEqual(r.returncode, 0, r.stderr)
        after = mtimes(self.out)
        self.assertEqual(set(before), set(after))                       # nothing removed, nothing extra
        changed = {p for p in after if after[p] != before[p]}
        self.assertTrue(all(p.startswith(('clips/tb__', 'transitions/tb__')) for p in changed))
        self.assertTrue(any(p.startswith('clips/tb__two/') for p in changed))
        self.assertFalse(any(p.startswith('clips/ta__') for p in changed))
        self.assertEqual(self.built(), ['tb__two'])

    def test_only_accepts_a_clip_name(self):
        r = build(self.src, self.out, 'ta__one'); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.built(), ['ta__one'])

    def test_a_new_theme_gets_its_clip_and_its_own_transition_halves(self):
        add_theme(self.src, 'tc', 'three')
        r = build(self.src, self.out, 'tc'); self.assertEqual(r.returncode, 0, r.stderr)
        for d in ('clips/tc__three', 'transitions/tc__out', 'transitions/tc__in'):
            self.assertTrue(os.path.isdir(os.path.join(self.out, d)), d)

    def test_a_new_theme_does_not_need_the_others_frames(self):
        shutil.rmtree(os.path.join(self.out, 'clips', 'ta__one'))      # another theme's keyframe is gone
        add_theme(self.src, 'tc', 'three')
        r = build(self.src, self.out, 'tc'); self.assertEqual(r.returncode, 0, r.stderr)

    def test_old_per_pair_transitions_are_cleared(self):
        os.makedirs(os.path.join(self.out, 'transitions', 'ta__tb'))
        r = build(self.src, self.out, 'ta'); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.out, 'transitions', 'ta__tb')))

    def test_every_folder_is_a_pack_and_its_count(self):
        from PIL import Image
        for top, n in (('clips', 4), ('transitions', 11)):               # the synthetic clips are 4 frames
            for dd in os.listdir(os.path.join(self.out, top)):
                d = os.path.join(self.out, top, dd)
                want = ['count', 'frames.png'] + (['glow'] if top == 'clips' else [])
                self.assertEqual(sorted(f for f in os.listdir(d) if not f.startswith('.')), want, dd)
                self.assertEqual(int(open(os.path.join(d, 'count')).read()), n, dd)
                sheet = Image.open(os.path.join(d, 'frames.png'))
                self.assertEqual(sheet.size, (185 * min(10, n), 64 * ((n + 9) // 10)), dd)

    def test_an_unknown_name_fails_and_lists_the_known_ones(self):
        r = build(self.src, self.out, 'nope')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unknown theme or clip 'nope'", r.stderr)
        self.assertIn('tb__two', r.stderr)

    def test_a_partial_build_needs_a_full_one_first(self):
        src, out = make_src({'ta': ('one', 1)})
        r = build(src, out, 'ta')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('full build first', r.stderr)

if __name__ == '__main__':
    unittest.main()
