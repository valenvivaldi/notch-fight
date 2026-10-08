"""nf new-theme: a skeleton for a new theme that starts out right (it imports, renders, loops and passes
`nf check`), with TODOs where the theme's own content goes.

    nf new-theme <id> [--sub-of <theme>] [--people] [--2.5d] [--no-fight]

Writes src/themes/<id with - as _>.py, adds the theme's row to the README table and the module to its source
tree, then runs `nf check <id>` and scripts/sheet.py and prints the next steps.
- --sub-of <theme>: a sub-theme of that franchise (its own loop keyframe; the sibling's sprites can be imported)
- --people: Claude and the rival as pose-built people (engine/people.py: figure(), POSES)
- --2.5d: the scene on a Stage (engine/stage25.py): depth, shadows, drawing back to front
- --no-fight: no rival, a calm scene
`arg` and `arg-*` themes never get DEFAULT_OFF; the others get it as a commented line.

NOTCH_FIGHT_README points at another README (tests); the files are written under the repo `root`."""
import argparse, glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLIP = 'main'                                                         # the example clip's name
ID_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

class NewThemeError(Exception): pass

def _read(path):
    with open(path) as fh: return fh.read()

# ---- what exists already --------------------------------------------------------------------------------
def themes_in(root):
    """{theme id: module name} of every theme file in src/themes/ (read as text, nothing imported)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(root, 'src', 'themes', '*.py'))):
        m = re.search(r"^THEME\s*=\s*['\"]([^'\"]+)['\"]", _read(path), re.M)
        if m: out[m.group(1)] = os.path.basename(path)[:-3]
    return out

def fx_names(root):
    """Every effect name registered anywhere in src/ (effect names are global)."""
    names = set()
    for path in glob.glob(os.path.join(root, 'src', '**', '*.py'), recursive=True):
        names |= set(re.findall(r"@fx\(\s*['\"]([^'\"]+)['\"]", _read(path)))
    return names

def fx_prefix(theme_id, taken):
    """A short prefix for the theme's effect names that no existing effect starts with: the initials of its
    parts (arg-salta: as), else the first letters of the id, as many as it takes."""
    flat = theme_id.replace('-', '')
    cands = [''.join(p[0] for p in theme_id.split('-'))] + [flat[:n] for n in range(2, len(flat) + 1)]
    for c in cands:
        if len(c) >= 2 and not any(n.startswith(c + '_') for n in taken): return c
    return flat + 'x'

# ---- the template ---------------------------------------------------------------------------------------
def _align(line, col=68):
    """A line's trailing comment moved to column col (the repo's habit), if the code leaves room."""
    m = re.match(r'^(\s*[^#\s].*?\S)\s{2,}(# .*)$', line)
    return m.group(1).ljust(col) + m.group(2) if m and len(m.group(1)) < col else line

def source(tid, parent=None, parent_mod=None, people=False, stage=False, fight=True, prefix='th'):
    """The text of the theme file."""
    arg = tid == 'arg' or tid.startswith('arg-')
    sub = f' sub-theme "{tid}" of "{parent}"' if parent else ''
    out = [f'"""TODO Franchise{sub}: Claude as TODO (who he is and what tells him apart: hair, clothes, a prop), in TODO',
           'the place (what is in it, what the light is like). '
           + (f'Clip `{CLIP}`: TODO the rival (who, where) and what happens between them' if fight else
              f'Clip `{CLIP}`: no fight, a calm scene. TODO what Claude does')
           + ';',
           'TODO the line of text he says. Close-up: TODO what it shows. TODO how it ends, back on the neutral pose."""']
    out.append('from engine import *')
    if parent:
        out += [f'# TODO sprites and helpers can come from the sibling theme instead of being copied:',
                f'# from themes.{parent_mod} import ...']
    out += ['', f"THEME = '{tid}'",
            'N_ = 120                                                            # a multiple of 12: the ready bounce loops']
    if not arg: out.append('# DEFAULT_OFF = True                                                # TODO niche (a club, a brand, an in-joke)? ship it off')
    out += ['CX, RX = 50, 134                                                   # Claude; the rival (TODO where they stand)' if fight else
            'CX = 92                                                            # Claude (TODO where he stands)',
            'INK = (16,14,22)',
            'SKY, SKY2, FLOOR, ACCENT = (34,30,58), (86,60,96), (52,44,64), (255,200,90)      # TODO the palette',
            'LINE = "TODO: WHAT CLAUDE SAYS"                                    # up for hold(LINE) frames (engine/director.py)',
            'CLOSE = "TODO: CLOSE-UP LINE"',
            'LINE_AT = 36                                                       # when it starts',
            'CLOSE_AT, CLOSE_LEN = LINE_AT + hold(LINE) + 4, 40                 # the close-up follows it (ends before N_)']
    if stage:
        out += ['', '# ---- the floor, in 2.5D: world x, depth z (0 far .. 1 near), height (engine/stage25.py) -------------------',
                'ST = Stage(far_y=40, near_y=60, vp_x=W // 2, far_scale=0.75)',
                'Z = 0.8                                                            # the depth they stand at']
    if people:
        out += ['', '# ---- people, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------',
                'GW, GH, C = 24, 24, 11                                             # the grid and its centre column (they face right)',
                'POSES = dict(POSES)                                                # TODO add this theme\'s own poses to the copy (same shape:',
                '                                                                   # back elbow, back hand, front elbow, front hand, lean, legs)',
                f"_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)",
                f"CLAUDE = dict(_BODY, name='{tid}-claude', hair=['..hhhh.', '.hhhhhh'], hair_y=2)   # TODO hair, clothes (paint: small painters)"]
        if fight: out.append(f"RIVAL = dict(_BODY, name='{tid}-rival', hair=['hhhhhhh', 'h.hhh.h'], hair_y=2)    # TODO who they are")
        out += ["CPAL = {'s':(217,119,87),'K':INK,'h':(168,80,54),'j':(168,80,54),'p':(60,52,70),'k':INK}      # one char per colour"]
        if fight: out.append("RPAL = {'s':(226,184,150),'K':INK,'h':(60,40,70),'j':(90,60,150),'p':(40,36,56),'k':INK}")
        out += ['', 'def build(' + ('who, ' if fight else '') + 'pose):',
                '    """' + ('Claude or the rival' if fight else 'Claude') + ' in a pose (POSES): engine/people.py\'s figure()."""',
                '    return figure(' + ('CLAUDE if who == \'claude\' else RIVAL' if fight else 'CLAUDE') + ', POSES[pose])']
    elif fight:
        out += ['', '# ---- the rival: a sprite (Claude is CL[...] from the engine) ---------------------------------------------',
                'RIVAL = S([     # TODO draw them',
                '"...rrrrrr...",', '"..rrrrrrrr..",', '"..rrKrrKrr..",', '"..rrrrrrrr..",', '".RrrrrrrrrR.",',
                '"RRrrrrrrrrRR",', '"..rrrrrrrr..",', '"..RRR..RRR..",', '".RRR....RRR.",])',
                "RPAL = {'r':(120,90,200),'R':(70,50,130),'K':INK}"]
    # ---- the place
    out += ['', '# ---- the place ------------------------------------------------------------------------------------------',
            'def _set(d):                                                       # TODO draw the place: the sky, the wall, what is in it',
            '    for y in range(H):',
            '        k = y / H; d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip(SKY, SKY2)))']
    if stage:
        out += ['    d.rectangle([0, int(ST.feet(0)) - 2, W, H], fill=FLOOR)',
                '    ST.quad(d, 8, 176, 0.05, 0.95, (64,54,78))                       # a patch of floor, in perspective',
                '    for z in (0.05, 0.95): ST.line(d, (8, z), (176, z), ACCENT)']
    else:
        out.append('    d.rectangle([0, GROUND + 2, W, H], fill=FLOOR)')
    out += ['    d.rectangle([70, 12, 112, 32], outline=ACCENT)                  # TODO something big behind them',
            "register_bg(THEME, lambda v: (v+30,v+24,v+44), decor=_set)", '',
            f"@fx('{prefix}_spark')",
            'def _fx_spark(d, im, e, f):',
            '    """A spark: (name, x, y, k), k the frames since it started."""',
            '    _, x, y, k = e; spark(d, int(x), int(y), 3 + int(k))']
    if stage:
        out += ['', f"@fx('{prefix}_shadow')", 'def _fx_shadow(d, im, e, f):',
                '    """The shadow under someone: (name, world x, z, width)."""',
                '    _, wx, z, w = e; ST.shadow(im, wx, z, w, (0, 0, 0), 90)']
    # ---- the close-up
    out += ['', '# ---- the close-up ---------------------------------------------------------------------------------------',
            'def _face(im, d, t, f):                                            # TODO what the close-up shows (t: 0..1 through it)',
            '    x = int(lerp(14, 8, ease(t)))                                  # a slow push in',
            "    d.rectangle([x, 8, x + 56, 56], fill=(217,119,87), outline=INK)  # Claude's face, big",
            '    d.rectangle([x + 12, 24, x + 18, 34], fill=INK); d.rectangle([x + 38, 24, x + 44, 34], fill=INK)', '']
    # ---- the clip
    out += ['# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 --------------------------------',
            'def ready(f):                                                      # the neutral pose: it moves every 12 frames, which divides N_']
    out.append("    return 'stand'" if people and not fight else "    return pose_cycle(f, 'guard', 'guard2')")
    act = ('jab' if fight else 'point') if people else ('punch' if fight else 'armsup')
    out += ['', 'def put_on(spr, wx, flip=False, pal=None):',
            '    """An actor standing at world x' + (' (on the Stage)' if stage else '') + '."""',
            '    return ' + ('ST.place(spr, wx, Z, flip=flip, pal=pal)' if stage else 'actor(spr, wx, flip=flip, pal=pal)'), '',
            'def clip_' + CLIP + '(f):',
            '    s = scene(f, THEME)',
            '    me = ready(f)' + ('; rival = ready(f); rx = RX' if fight else '')]
    sprite_me = 'build(\'claude\', me)' if people and fight else 'build(me)' if people else 'CL[me]'
    if fight:
        out += [f"    if 30 <= f < 34: me = '{act}'                                         # TODO the action",
                f"    if 32 <= f < 46: rival = 'hurt'; rx = RX + 4"]
        out += ["    if 32 <= f < 40: s['shake'] = rshake(1)"]
        hit = 'ST.proj(RX - 8, Z, 10)' if stage else '(RX - 14, GROUND - 14)'
        out += ["    if 32 <= f < 40: s['fx'].append(('%s_spark', *%s, f - 32))                # the hit" % (prefix, hit)]
    else:
        out += [f"    if 30 <= f < 46: me = '{act}'                                        # TODO what Claude does"]
        hit = 'ST.proj(CX + 8, Z, 22)' if stage else '(CX + 8, GROUND - 22)'
        out += ["    if 32 <= f < 40: s['fx'].append(('%s_spark', *%s, f - 32))" % (prefix, hit)]
    out += ['    if cue(f, LINE_AT, LINE): s[\'fx\'].append((\'caption\', LINE))   # the text director sets how long it stays up',
            '    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:',
            "        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=SKY, draw=_face, txt=CLOSE); return s",
            "    # s['under'].append(('fireflies', {'n': 8}))                    # an ambient effect (engine/ambient.py): rain, snow, ash, embers,",
            '    #                                                                 fireflies, fog, torch, stars, flashes. They loop on their own.']
    # actors
    if people:
        mine = f"put_on(build('claude', me), CX, pal=CPAL)" if fight else "put_on(build(me), CX, pal=CPAL)"
        theirs = "put_on(build('rival', rival), rx, flip=True, pal=RPAL)"
    else:
        mine = 'put_on(CL[me], CX)'
        theirs = "put_on(RIVAL, rx, flip=True, pal=RPAL)"
    if stage:
        out += ["    s['under'] += [('%s_shadow', CX, Z, 7)" % prefix + (", ('%s_shadow', rx, Z, 7)]" % prefix if fight else ']')]
        out += ['    s[\'actors\'] = Stage.back_to_front([(Z, %s)' % mine + (', (Z, %s)])' % theirs if fight else '])')]
    else:
        out += ['    s[\'actors\'] = [%s' % mine + (', %s]' % theirs if fight else ']')]
    out += ['    return s', '', f"CLIPS = [clip('{CLIP}', N_, clip_{CLIP})]", '']
    return '\n'.join(_align(l) for l in out)

# ---- the README ---------------------------------------------------------------------------------------------
def readme_edit(text, tid, module, sub, fight):
    """The README with the theme's row in the themes table and its module in the source tree."""
    lines = text.split('\n')
    head = next((i for i, l in enumerate(lines) if l.startswith('| Theme |')), None)
    if head is None: raise NewThemeError('the README has no themes table (| Theme | ...)')
    end = head + 1
    while end < len(lines) and lines[end].startswith('|'): end += 1
    opp = 'TODO the rival' if fight else 'none (no fight)'
    lines.insert(end, f'| `{tid}` | TODO Claude as ... (what the clip shows) | {opp} | {CLIP} |')
    tree = next((i for i, l in enumerate(lines) if '# sub-themes' in l), None) if sub else \
           next((i for i, l in enumerate(lines) if re.search(r'├── dbz\.py\s', l)), None)
    if tree is None: raise NewThemeError('the README has no source tree listing of the themes')
    if sub: lines[tree] = lines[tree].replace('   # sub-themes', f'  {module}.py   # sub-themes')
    else: lines[tree] = lines[tree].rstrip() + f'  {module}.py'
    return '\n'.join(lines)

# ---- the command --------------------------------------------------------------------------------------------
def create(tid, parent=None, people=False, stage=False, fight=True, root=ROOT, readme=None):
    """Write the theme file and the README edits; returns the file's path. Refuses what already exists."""
    readme = readme or os.environ.get('NOTCH_FIGHT_README') or os.path.join(root, 'README.md')
    if not ID_RE.match(tid): raise NewThemeError(f"'{tid}' is not a theme id: lowercase letters, digits and dashes (arg-salta)")
    have = themes_in(root); module = tid.replace('-', '_')
    path = os.path.join(root, 'src', 'themes', module + '.py')
    if tid in have: raise NewThemeError(f"theme '{tid}' already exists (src/themes/{have[tid]}.py)")
    if os.path.exists(path): raise NewThemeError(f'{os.path.relpath(path, root)} already exists')
    if parent and parent not in have: raise NewThemeError(f"--sub-of: no theme '{parent}'. Known: {', '.join(sorted(have))}")
    if parent and not tid.startswith(parent + '-'):                 # a sub-theme is named after its parent: dbz-buu, naruto-edo
        raise NewThemeError(f"a sub-theme of '{parent}' is named '{parent}-<something>' (e.g. {parent}-{tid})")
    text = source(tid, parent, have.get(parent), people, stage, fight, fx_prefix(tid, fx_names(root)))
    new_readme = readme_edit(_read(readme), tid, module, bool(parent), fight)
    with open(path, 'w') as fh: fh.write(text)
    with open(readme, 'w') as fh: fh.write(new_readme)
    return path

def run(script, *args, root=ROOT):
    """A script of this repo, its output shown; its exit code."""
    return subprocess.run([sys.executable, os.path.join(root, 'scripts', script), *args], cwd=root).returncode

def main(argv, root=ROOT):
    ap = argparse.ArgumentParser(prog='nf new-theme', description='A skeleton for a new theme that starts out right.')
    ap.add_argument('id', help='the theme id: lowercase letters, digits and dashes (arg-salta)')
    ap.add_argument('--sub-of', metavar='THEME', help='a sub-theme of that theme (dbz-cell: --sub-of dbz)')
    ap.add_argument('--people', action='store_true', help='Claude and the rival built with figure() and POSES')
    ap.add_argument('--2.5d', dest='stage', action='store_true', help='the scene on a Stage (depth, shadows)')
    ap.add_argument('--no-fight', dest='fight', action='store_false', help='no rival, a calm scene')
    a = ap.parse_args(argv)
    try: path = create(a.id, a.sub_of, a.people, a.stage, a.fight, root)
    except NewThemeError as e: print(f'nf: {e}', file=sys.stderr); return 1
    rel = os.path.relpath(path, root)
    print(f'Wrote {rel} and added {a.id} to the README (the themes table and the source tree)\n')
    bad = run('check.py', a.id, root=root)
    sheet = run('sheet.py', a.id, root=root)
    print(f"""
Next:
  1. Fill in every TODO in {rel} (grep TODO); look at the sheet again with: python3 scripts/sheet.py {a.id}
  2. See it play: FIRST={a.id}__{CLIP} ONLY={a.id} GIFS=1 ./build.sh
  3. When the theme is finished: python3 tests/test_snapshots.py --update
     (and fill in its row in the README table, then commit the source, the GIFs and tests/snapshots.txt)""")
    return 1 if bad or sheet else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
