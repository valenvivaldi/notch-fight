"""Checks a theme's clips against the rules, straight from the code (no build), and says what to fix:

- loop: frame N must be frame 0 (whatever moves needs a period that divides the clip; engine/loop.py)
- neutral: a theme's clips all start on the same frame
- font: every character written is in the font
- text: every line of two or more words stays up long enough to read (engine/director.py hold(): 0.5 s +
  0.2 s a word, at least 1 s; a blink of a few frames, or a line typed out letter by letter, counts as
  one showing), and nothing that stays put is cut off by the panel's edge

    python3 scripts/check.py [theme ...]          (every theme when none is named; nf check does the same)
    python3 scripts/check.py --baseline           (record today's problems as known, for tests/test_check.py)

Exits 1 when something fails. Renders in parallel (JOBS=<n>)."""
import importlib, multiprocessing, os, random, re, sys, zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
GAP = 8                                                             # frames a text may blink out and still be one showing
SLACK = 2                                                           # frames of leeway on hold()

def _clip(job):
    """One clip in a worker: its frame 0 and N, missing characters, and the texts on every frame."""
    sys.path.insert(0, SRC)
    from themes import load_themes
    font = importlib.import_module('engine.text')
    global _THEMES
    if '_THEMES' not in globals(): _THEMES = load_themes()
    theme, name = job
    n, fn = next((n, fn) for nm, n, fn, _ in _THEMES[theme] if nm == name)
    font.MISSING.clear(); random.seed(zlib.crc32(name.encode())); texts = []
    first = None
    for f in range(n):
        font.RECORD = []; im = fn(f).convert('RGB'); texts.append(font.RECORD)
        if f == 0: first = im.tobytes()
    font.RECORD = None
    random.seed(zlib.crc32(name.encode())); last = fn(n).convert('RGB').tobytes()
    return theme, name, n, first, last, ''.join(sorted(font.MISSING)), texts

def _runs(frames, n):
    """Consecutive frames (gaps up to GAP bridged, and the loop's seam joined) as (start, length)."""
    if not frames: return []
    fs = sorted(frames); runs = [[fs[0], fs[0]]]
    for f in fs[1:]:
        if f - runs[-1][1] <= GAP + 1: runs[-1][1] = f
        else: runs.append([f, f])
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][1] == n - 1:  # up across the seam: one showing
        runs[0] = [runs[-1][0] - n, runs[0][1]]; runs.pop()
    return [(a, b - a + 1) for a, b in runs]

def text_problems(texts, n, W, H, hold):
    """The text rules for one clip: [(kind, text, frame, detail)]."""
    out = []; at = {}
    for f, recs in enumerate(texts):                                 # a scoreboard is one text, whatever it reads
        for txt, *_ in recs: at.setdefault(re.sub(r'[0-9]', '#', txt), set()).add(f)
    for txt, frames in at.items():
        if len([w for w in txt.split() if any(c.isalpha() for c in w)]) < 2: continue   # labels, sounds, numbers
        if any(o != txt and o.startswith(txt) for o in at): continue  # a stage of a line being typed out
        grown = set(frames)                                          # typed out: its beginnings count too
        for other, fo in at.items():
            if other != txt and len(other) >= 3 and txt.startswith(other): grown |= fo
        for start, length in _runs(grown, n):
            if not any((start + k) % n in frames for k in range(length)): continue
            if length + SLACK < hold(txt): out.append(('short', txt, start % n, f'{length} frames, needs {hold(txt)}'))
    seen = {}
    for f, recs in enumerate(texts):
        for txt, x0, y0, x1, y1 in recs:
            if x0 < 0 or y0 < 0 or x1 >= W or y1 >= H: seen.setdefault((txt, x0, y0, x1, y1), []).append(f)
    for (txt, x0, y0, x1, y1), fs in seen.items():
        if len(fs) >= 6: out.append(('cut off', txt, fs[0], f'box ({x0},{y0})-({x1},{y1}) on a {W}x{H} panel'))   # still, not passing through
    return out

def check(themes=None):
    """{theme: [problem lines]} for the named themes (every theme when None)."""
    sys.path.insert(0, SRC)
    from themes import load_themes
    from engine import W, H, hold
    all_ = load_themes()
    if themes:
        bad = [t for t in themes if t not in all_]
        if bad: raise SystemExit(f"unknown theme {', '.join(bad)}. Known: {', '.join(sorted(all_))}")
    names = themes or sorted(all_)
    jobs = [(t, c[0]) for t in names for c in all_[t]]
    k = max(1, min(int(os.environ.get('JOBS') or os.cpu_count() or 1), len(jobs)))
    with multiprocessing.get_context('spawn').Pool(k) as pool: results = list(pool.imap(_clip, jobs))
    report = {t: [] for t in names}; firsts = {}
    for theme, name, n, first, last, missing, texts in results:   # (key, message): the key names it in a baseline
        r = report[theme]; firsts.setdefault(theme, set()).add(first)
        if first != last: r.append((f'{theme}__{name} loop', f'{name}: loop: frame {n} is not frame 0 (something moving in the neutral pose has a period that doesn\'t divide {n}; engine/loop.py)'))
        if missing: r.append((f'{theme}__{name} font {missing}', f'{name}: font: no glyph for {" ".join(repr(c) for c in missing)} (drawn as spaces)'))
        for kind, txt, f, detail in sorted(text_problems(texts, n, W, H, hold), key=lambda p: p[2]):
            r.append((f'{theme}__{name} {kind} {txt}', f'{name}: text {kind}: "{txt}" at frame {f}: {detail}'))
    for t, fs in firsts.items():
        if len(fs) > 1: report[t].insert(0, (f'{t} neutral', 'neutral: its clips start on different frames'))
    return report

BASELINE = os.path.join(ROOT, 'tests', 'check_baseline.txt')

def baseline():
    """The problems already known (tests/check_baseline.txt): the test fails only on new ones."""
    if not os.path.exists(BASELINE): return set()
    return {l.rstrip('\n') for l in open(BASELINE) if l.strip() and not l.startswith('#')}

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] in ('-h', '--help'): print(__doc__); return 0
    if argv and argv[0] == '--baseline':                            # record today's problems as known
        report = check(None); keys = sorted(k for ps in report.values() for k, _ in ps)
        with open(BASELINE, 'w') as fh:
            fh.write('# problems scripts/check.py already knew about; tests/test_check.py fails only on new ones.\n'
                     '# Fix one, and drop its line (or rerun: python3 scripts/check.py --baseline).\n')
            fh.writelines(k + '\n' for k in keys)
        print(f'{len(keys)} known problems recorded in {os.path.relpath(BASELINE, ROOT)}'); return 0
    report = check(argv or None); bad = 0; known = baseline()
    for theme, problems in report.items():
        if problems or argv:
            print(f'{theme}: ' + ('ok' if not problems else f'{len(problems)} to fix'))
            for k, msg in problems: print(f'  {msg}' + ('  (known)' if k in known else ''))
        bad += len(problems)
    if not argv: print(f'{len(report)} themes, {bad} problems' if bad else f'{len(report)} themes: all ok')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
