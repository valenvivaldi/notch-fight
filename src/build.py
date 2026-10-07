"""Renders every clip of every theme + all theme-to-theme transitions into the cwd:
clips/<theme>__<clip>/ and transitions/<theme>__out|in/, plus sheet_<theme>_<clip>.png. Each folder
holds frames.png, all its frames packed in one image (a grid of SHEET_COLS columns, in order, row by
row), and count, how many: one file per clip instead of hundreds. scripts/frames.py reads them back
(the GIFs, the Claude Code mod).

A transition is per theme: the iris closing on the theme being left (<theme>__out), then opening on the
next one (<theme>__in); both come from the theme's keyframe (its first clip's first frame).
ONLY=<theme|theme__clip>[,...] renders just those clips and, when a theme's first clip is among them, that
theme's two halves, leaving the rest of the cwd as it is (it needs a full build first).
Clips render in parallel, one per process (JOBS=<n> sets how many; JOBS=1 renders them in this process). Either way `.built` lists the clips
rendered by this run (build.sh makes GIFs for those)."""
import multiprocessing, os, random, shutil, sys, zlib
from engine import *
from themes import load_themes
from transitions import iris_out, iris_in

def selected(themes, only):
    """(theme, clip) pairs named by ONLY; exits listing the known names on a typo."""
    known={f'{t}__{c[0]}' for t,items in themes.items() for c in items}
    picked=[]
    for name in only:
        hits=[(t,c) for t,items in themes.items() for c in items if name in (t,f'{t}__{c[0]}')]
        if not hits: sys.exit(f"unknown theme or clip '{name}'. Known: {', '.join(sorted(known|set(themes)))}")
        picked+=[h for h in hits if h not in picked]
    return picked

SHEET_COLS = 10

def pack(dd, frames):
    """frames.png (the frames in a grid of SHEET_COLS columns, row by row) and count, in folder dd."""
    cols=min(SHEET_COLS,len(frames)); rows=(len(frames)+cols-1)//cols
    sh=Image.new('RGB',(W*cols,H*rows))
    for i,fr in enumerate(frames): sh.paste(fr,((i%cols)*W,(i//cols)*H))
    sh.save(f'{dd}/frames.png'); open(f'{dd}/count','w').write(f'{len(frames)}\n')

def render_clip(theme, name, n, frame_fn, off):
    random.seed(zlib.crc32(name.encode()))
    frames=[frame_fn(f) for f in range(n)]
    dd=f'clips/{theme}__{name}'; shutil.rmtree(dd,ignore_errors=True); os.makedirs(dd)
    pack(dd,frames)
    if off: open(f'{dd}/.default-off','w').close()   # shipped off: ./clips.sh and the app read this
    big=[fr.resize((W*2,H*2),Image.NEAREST) for fr in frames]
    sh=Image.new('RGB',(W*4,H*12)); pick=[int(i*(n-1)/11) for i in range(12)]
    for j,i in enumerate(pick): sh.paste(big[i],((j%2)*W*2,(j//2)*H*2))
    sh.save(f'sheet_{theme}_{name}.png'); print(theme,name,n,flush=True)

_THEMES=None
def _load():
    global _THEMES
    _THEMES=load_themes()
def _render(job):
    """A worker: the clip's frame function can't cross processes (it's a lambda), so each worker loads
    the themes once and is sent just the names."""
    theme,name=job
    n,frame_fn,off=next((n,fn,off) for nm,n,fn,off in _THEMES[theme] if nm==name)
    render_clip(theme,name,n,frame_fn,off)

if __name__=='__main__':
    THEMES=load_themes()
    only=[n for n in os.environ.get('ONLY','').split(',') if n]
    if only and not os.path.isdir('clips'): sys.exit('ONLY needs an existing build: run a full build first (./build.sh)')
    todo=selected(THEMES,only) if only else [(t,c) for t,items in THEMES.items() for c in items]
    if not only: shutil.rmtree('clips',ignore_errors=True); shutil.rmtree('transitions',ignore_errors=True)
    jobs=sorted(((t,c[0]) for t,c in todo),key=lambda j:-next(c[1] for c in THEMES[j[0]] if c[0]==j[1]))   # longest first
    n_jobs=max(1,min(int(os.environ.get('JOBS') or os.cpu_count() or 1),len(jobs)))
    if n_jobs==1:
        _THEMES=THEMES
        for job in jobs: _render(job)
    else:
        with multiprocessing.get_context('spawn').Pool(n_jobs,initializer=_load) as pool:
            for _ in pool.imap_unordered(_render,jobs): pass
    first={}                                                     # a theme's keyframe: its first clip's first frame
    for theme,(name,*_) in todo:
        if name==THEMES[theme][0][0]: first[theme]=Image.open(f'clips/{theme}__{name}/frames.png').convert('RGB').crop((0,0,W,H))
    os.makedirs('transitions',exist_ok=True)
    for dd in os.listdir('transitions'):                         # the old per-pair transitions, gone
        if not dd.endswith(('__out','__in')): shutil.rmtree(f'transitions/{dd}',ignore_errors=True)
    for theme,img in first.items():
        for half,frames in (('out',iris_out(img)),('in',iris_in(img))):
            dd=f'transitions/{theme}__{half}'; shutil.rmtree(dd,ignore_errors=True); os.makedirs(dd)
            pack(dd,frames)
    open('.built','w').write('\n'.join(f'{t}__{c[0]}' for t,c in todo)+'\n')
    print('transitions ok')
