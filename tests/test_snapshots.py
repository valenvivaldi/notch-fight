"""Snapshots: a hash of every frame of every clip, kept in tests/snapshots.txt, so a change to the engine
or a theme that alters a clip shows up, by name, instead of slipping by. And every character a clip
writes must be in the font (missing ones would silently draw as spaces).

When a clip is meant to change (a new theme, a better sprite), record the new hashes:

    python3 tests/test_snapshots.py --update

Renders every clip, in parallel (JOBS=<n>, as build.py), the way build.py does."""
import hashlib, multiprocessing, os, random, sys, unittest, zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshots.txt')

def _render(job):
    """One clip in a worker: (name, hash of all its frames, characters the font lacked)."""
    sys.path.insert(0, SRC)
    from themes import load_themes
    import importlib; font = importlib.import_module("engine.text")   # the module (engine exports a text() too)
    global _THEMES
    if '_THEMES' not in globals(): _THEMES = load_themes()
    theme, name = job
    n, fn = next((n, fn) for nm, n, fn, _ in _THEMES[theme] if nm == name)
    font.MISSING.clear(); random.seed(zlib.crc32(name.encode())); h = hashlib.sha1()
    for f in range(n): h.update(fn(f).convert('RGB').tobytes())
    return f'{theme}__{name}', h.hexdigest()[:16], ''.join(sorted(font.MISSING))

def snapshot():
    """{clip: (hash, missing chars)} for every clip."""
    sys.path.insert(0, SRC)
    from themes import load_themes
    jobs = [(t, c[0]) for t, items in load_themes().items() for c in items]
    n = max(1, min(int(os.environ.get('JOBS') or os.cpu_count() or 1), len(jobs)))
    with multiprocessing.get_context('spawn').Pool(n) as pool:
        return {k: (h, miss) for k, h, miss in pool.imap_unordered(_render, jobs)}

def read():
    if not os.path.exists(FILE): return {}
    return dict(line.split() for line in open(FILE) if line.strip() and not line.startswith('#'))

def write(snap):
    with open(FILE, 'w') as fh:
        fh.write('# clip  hash of all its frames (python3 tests/test_snapshots.py --update)\n')
        for k in sorted(snap): fh.write(f'{k} {snap[k][0]}\n')

_SNAP = None
def snap():
    global _SNAP
    if _SNAP is None: _SNAP = snapshot()
    return _SNAP

class Snapshots(unittest.TestCase):
    def test_every_clip_matches_its_snapshot(self):
        want, got = read(), {k: h for k, (h, _) in snap().items()}
        changed = sorted(k for k in got if k in want and want[k] != got[k])
        new = sorted(k for k in got if k not in want); gone = sorted(k for k in want if k not in got)
        msg = (f'changed: {changed}\nnew: {new}\ngone: {gone}\n'
               'If that is what you meant, record it: python3 tests/test_snapshots.py --update')
        self.assertEqual((changed, new, gone), ([], [], []), msg)

    def test_every_character_is_in_the_font(self):
        missing = {k: m for k, (_, m) in snap().items() if m}
        self.assertEqual(missing, {}, 'these clips write characters the font lacks (they draw as spaces)')

if __name__ == '__main__':
    if '--update' in sys.argv:
        s = snapshot(); old = read(); write(s)
        changed = [k for k in s if old.get(k) not in (None, s[k][0])]
        print(f'{len(s)} clips recorded ({len(changed)} changed, {len([k for k in s if k not in old])} new)')
    else:
        unittest.main()
