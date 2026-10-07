"""Effect registry. A scene lists effects as tuples ('name', *args); each theme registers the
effects it owns with @fx('name'). Effects used by several themes live here."""
from .core import *
from . import loop
from .text import text, big_text
from .closeup import fade_to

FX={}
def fx(name):
    def reg(fn):
        assert name not in FX, f"fx '{name}' registered twice"
        FX[name]=fn; return fn
    return reg

def draw_fx(d,im,e,f):
    h=FX.get(e[0])
    if h is None: raise KeyError(f"unknown fx '{e[0]}' (registered: {sorted(FX)})")
    h(d,im,e,f)

@fx('spark')
def _fx_spark(d,im,e,f):
    spark(d,int(e[1]),int(e[2]),e[3])

@fx('dust')
def _fx_dust(d,im,e,f):
    d.rectangle([e[1],e[2],e[1]+1,e[2]+1],fill=(150,130,100))

@fx('rock')
def _fx_rock(d,im,e,f):
    d.rectangle([e[1],e[2],e[1]+1,e[2]+1],fill=(120,92,66))

@fx('ring')
def _fx_ring(d,im,e,f):
    x,y,r,c=int(e[1]),int(e[2]),int(e[3]),e[4]
    d.ellipse([x-r,y-r//2,x+r,y+r//2],outline=c,width=1)
    if r<5: d.ellipse([x-2,y-2,x+2,y+1],fill=(255,240,200))

@fx('smoke')
def _fx_smoke(d,im,e,f):
    x,y,r,c=int(e[1]),int(e[2]),int(e[3]),e[4]
    d.ellipse([x-r,y-r,x+r,y+r],fill=c)

@fx('mote')
def _fx_mote(d,im,e,f):
    d.point((int(e[1]),int(e[2])),fill=e[3])

@fx('beam')
def _fx_beam(d,im,e,f):
    _,x0,x1,y,(oc,mc)=e; x0,x1,y=int(x0),int(x1),int(y); wob=f%2
    d.rectangle([x0,y-3-wob,x1,y+3+wob],fill=oc); d.rectangle([x0,y-2,x1,y+2],fill=mc); d.rectangle([x0,y-1+wob,x1,y],fill=(255,255,255))

@fx('boom')
def _fx_boom(d,im,e,f):
    x,y,r=int(e[1]),int(e[2]),int(e[3])
    d.ellipse([x-r-3,y-r-3,x+r+3,y+r+3],outline=(255,210,120),width=3); d.ellipse([x-r//2,y-r//2,x+r//2,y+r//2],fill=(255,255,255))

@fx('twinkle')
def _fx_twinkle(d,im,e,f):
    x,y,s=int(e[1]),int(e[2]),e[3]; d.line([x-s,y,x+s,y],fill=(255,255,255)); d.line([x,y-s,x,y+s],fill=(255,255,255))

@fx('shard')
def _fx_shard(d,im,e,f):
    _,x,y,c=e; d.point((int(x),int(y)),fill=c)

@fx('arc')
def _fx_arc(d,im,e,f):
    _,x,y,r,a0,a1,c,wd=e; d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=c,width=wd)

@fx('circle')
def _fx_circle(d,im,e,f):
    _,x,y,r,c=e; d.ellipse([x-r,y-r,x+r,y+r],outline=c)

@fx('orbc')
def _fx_orbc(d,im,e,f):
    # colored orb: x,y,r,(outer,mid)
    _,x,y,r,(oc,mc)=e; r=r+(f%2)
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=oc); d.ellipse([x-r,y-r,x+r,y+r],fill=mc); rc=max(1,r//2); d.ellipse([x-rc,y-rc,x+rc,y+rc],fill=(255,255,255))

@fx('dmg')
def _fx_dmg(d,im,e,f):
    _,txt,x,y,c=e; text(d,txt,int(x),int(y),c)

@fx('tracer')
def _fx_tracer(d,im,e,f):
    _,x0,x1,y=e; d.line([x0,y,x1,y],fill=(255,240,140))

@fx('fire')
def _fx_fire(d,im,e,f):
    """A column of flame: white-hot core, orange body, red tips, flickering."""
    _,x,feet,sz=e; rr=random.Random(loop.frame(f)*13+int(x))       # per frame, and frame N is frame 0
    for j in range(int(10+sz*3)):
        up=rr.random()**0.7; yy=feet-up*sz*3; xx=x+rr.uniform(-1,1)*sz*(1-up*0.6); r=max(1,int(sz*(1-up)*0.7+rr.randint(0,2)))
        c=(255,245,170) if up<0.25 else ((255,160,40) if up<0.6 else (220,60,20))
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=c)

@fx('big')
def _fx_big(d,im,e,f):
    """2x text for announcer lines and shouts (ROUND 1, FATALITY, ZA WARUDO!), centred at x (default: screen)."""
    _,txt,y,c,*rest=e; big_text(im,txt,y,c,cx=rest[0] if rest else W//2)

@fx('dim')
def _fx_dim(d,im,e,f):
    _,a=e; im.paste(fade_to(im,(0,0,0),min(1,max(0,a))))

@fx('dizzy')
def _fx_dizzy(d,im,e,f):
    _,x,y=e
    for k in range(3): a=f*0.4+k*2.1; d.point((x+math.cos(a)*6,y+math.sin(a)*2),fill=(255,230,90))
