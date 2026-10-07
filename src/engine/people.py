"""Shared pieces for themes that build their people from a pose (haikyuu, fightclub, arcane, basterds,
arg-cordoba, hp): a character grid painted cell by cell, limbs as lines of cells, the lean of a body, the
far-away copy of a sprite, and the speech bubble they all talk in.

A pose-built figure is a list of rows of palette chars ('.' = clear): start from blank(w,h), paint it
with put/seg, finish with to_sprite(). Each theme keeps its own anatomy (legs, clothes, hair) on top."""
from .core import *
from .text import text
from .fx import fx

def blank(w,h):
    """An empty character grid, w x h."""
    return [['.']*w for _ in range(h)]

def to_sprite(g):
    """The grid as a sprite."""
    return S([''.join(r) for r in g])

def put(g,x,y,c):
    """One cell, if it falls inside the grid."""
    if 0<=y<len(g) and 0<=x<len(g[0]): g[y][x]=c

def seg(g,x0,y0,x1,y1,c,first=None):
    """A straight run of cells from (x0,y0) to (x1,y1), both ends included (an arm, a leg, a bat);
    first: a different char for the starting cell (a sleeve at the shoulder)."""
    n=max(abs(x1-x0),abs(y1-y0),1)
    for i in range(n+1): put(g,round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),first if (first and i==0) else c)

def leaner(lean,top,bottom):
    """How far each row shifts for a body leaning `lean` cells at the top row, nothing at the bottom one."""
    return lambda y: round(lean*(bottom-y)/(bottom-top))

_small={}
def shrink(spr,k=0.8):
    """A smaller copy of a sprite (nearest sampling), for the far side of a 2.5D scene; cached."""
    key=(tuple(spr),k)
    if key not in _small:
        h,w=len(spr),len(spr[0]); nh,nw=max(1,round(h*k)),max(1,round(w*k))
        _small[key]=S([''.join(spr[min(h-1,int(y/k))][min(w-1,int(x/k))] for x in range(nw)) for y in range(nh)])
    return _small[key]

def cell_xy(x,feet,w,h,cx,cy,flip=False):
    """Screen position of grid cell (cx,cy) of a w x h sprite drawn centred on x with its feet at feet."""
    return (x-w//2+(w-1-cx) if flip else x-w//2+cx), feet-h+cy

def speech_bubble(d,lines,cx,y,tail=None,fill=(250,250,250),ink=(30,30,30)):
    """A speech bubble: one line or a list of them, centred on cx (kept on screen), its top at y, the
    tail pointing down to x=tail (the speaker; default cx)."""
    lines=[lines] if isinstance(lines,str) else lines
    tail=cx if tail is None else tail
    w=max(len(l) for l in lines)*4+7; h=len(lines)*7+4; x=max(1,min(W-w-2,int(cx-w/2)))
    d.rectangle([x,y,x+w,y+h],fill=fill,outline=ink)
    tx=max(x+4,min(x+w-4,int(tail))); d.polygon([(tx-2,y+h),(tx+2,y+h),(int(tail),y+h+5)],fill=fill,outline=ink)
    d.line([tx-1,y+h,tx+1,y+h],fill=fill)
    for i,l in enumerate(lines): text(d,l,x+4,y+3+i*7,ink,shadow=None)

@fx('bubble')
def _fx_bubble(d,im,e,f):
    """('bubble', text or [lines], cx, y[, tail_x[, fill[, ink]]])."""
    speech_bubble(d,*e[1:])
