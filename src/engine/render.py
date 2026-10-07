"""Generic scene model + renderer shared by every theme (except DBZ, which predates it)."""
from .core import *
from .fx import draw_fx
from . import loop

GROUND_COLORS={}    # theme -> v -> rgb of the dotted ground line
BG_DECOR={}         # theme -> fn(draw) extra background decoration
GROUND_CLIP=set()   # themes whose actors may sink INTO the ground (clipped below it)

def register_bg(theme, ground, decor=None, clip_ground=False):
    GROUND_COLORS[theme]=ground
    if decor: BG_DECOR[theme]=decor
    if clip_ground: GROUND_CLIP.add(theme)

def make_bg(kind):
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    for x in range(0,W,2):
        a=1-abs(x-W/2)/(W/2); v=int(10+26*a)
        d.point((x,GROUND+1),fill=GROUND_COLORS[kind](v))
    if kind in BG_DECOR: BG_DECOR[kind](d)
    return im

_BGS={}
def bg_for(kind):
    if kind not in _BGS: _BGS[kind]=make_bg(kind)
    return _BGS[kind]

def actor(spr,x,y=GROUND,flip=False,**kw):
    a=dict(spr=spr,x=x,y=y,flip=flip,aura=None,pal=None,vis=True,holo=None); a.update(kw); return a

def scene(f,kind):
    return dict(kind=kind,actors=[],under=[],fx=[],shake=(0,0),flash=0.0,fc=(93,GROUND-10),flashc=(255,250,235))

def draw_holo(im,spr,x,feet,flip,prog,f,alpha=0.85,pal=None):
    """Hologram: reveal from the feet up, scanline flicker."""
    h=len(spr); cut=int(h*(1-prog))
    full=prog>=1
    rows=[(r if (i>=cut and (full or (i+f)%3)) else '.'*len(r)) for i,r in enumerate(spr)]
    if full and f%9==0: rows=[r if i%2 else '.'*len(r) for i,r in enumerate(rows)]
    draw(im,S(rows),x,feet,flip,alpha=alpha,f=f,pal=pal)
    if 0<prog<1:
        y=int(feet-h+cut); w=len(spr[0])
        ImageDraw.Draw(im).line([x-w//2-1,y,x+w//2+1,y],fill=(200,160,255))

def render(s,f):
    if 'image' in s: return s['image']          # a clip may hand over a full custom frame
    im=bg_for(s['kind']).copy(); d=ImageDraw.Draw(im)
    for e in s['under']: draw_fx(d,im,e,f)
    for a in s['actors']:
        if not a['vis']: continue
        if a['holo'] is not None: draw_holo(im,a['spr'],a['x'],a['y'],a['flip'],a['holo'],f,pal=a['pal'])
        else: draw(im,a['spr'],a['x'],a['y'],a['flip'],aura=a['aura'],f=f,pal=a['pal'],alpha=a.get('alpha',1.0),tint=a.get('tint'))
    if s['kind'] in GROUND_CLIP: d.rectangle([0,GROUND+2,W,H],fill=(0,0,0))
    for e in s['fx']: draw_fx(d,im,e,f)
    if s['shake']!=(0,0):
        im2=bg_for(s['kind']).copy(); im2.paste(im,s['shake']); im=im2
    if s['flash']>0:
        m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); r=int(20+90*s['flash']); cx,cy=s['fc']
        md.ellipse([cx-r,cy-r//2,cx+r,cy+r//2],fill=int(255*min(1,s['flash'])))
        m=m.filter(ImageFilter.GaussianBlur(8))
        im=Image.composite(Image.new('RGB',(W,H),s['flashc']),im,m)
    return im

def callout(s,txt,y=2,c=(255,226,90)):
    """Centered shout at the top of the panel (technique / jutsu names)."""
    s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))

def clip(name, n, fn, off=None):
    """Declare a clip: `fn(f)` returns a scene; frames are render(fn(f), f).
    off=True ships it off by default (users turn it on with ./clips.sh); off=False keeps it on in a
    theme with DEFAULT_OFF = True; None follows the theme.
    Before each frame it tells engine/loop.py the clip's length, so effects can loop on it."""
    def frame(f):
        loop.at(n); return render(fn(f), f)
    return (name, n, frame, {} if off is None else {'off': off})
