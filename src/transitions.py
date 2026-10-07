"""Asterisk-iris transition between two themes' loop keyframes. It is built per theme, not per pair: the
iris closes on the theme being left (iris_out) and opens on the one arriving (iris_in), so each theme
needs just its own two halves, transitions/<theme>__out and transitions/<theme>__in."""
from engine import *

def asterisk_thick(d,x,y,r,f,c=(217,119,87)):
    for k in range(8):
        a=k*math.pi/4+f*0.25; L=r*(1 if k%2==0 else 0.75)
        d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=c,width=max(1,int(r/5)))
    d.ellipse([x-r*0.18,y-r*0.18,x+r*0.18,y+r*0.18],fill=c)

def _iris(img,ts,f0):
    """The iris over img at each t in ts (0 open .. 1 closed), the asterisk spinning in the middle."""
    out=[]
    for k,t in enumerate(ts):
        r=int(lerp(115,0,t)); cx,cy=W//2,GROUND-12
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
        im=Image.composite(img,Image.new('RGB',(W,H)),m)
        d=ImageDraw.Draw(im); asterisk_thick(d,cx,cy,int(4+14*t),f0+k)
        out.append(im)
    return out

def iris_out(img,T=22):
    """Leaving a theme: the iris closes on its keyframe (the first half of a transition)."""
    half=T//2; return _iris(img,[i/(half-1) for i in range(half)],0)

def iris_in(img,T=22):
    """Arriving at a theme: the iris opens on its keyframe (the second half)."""
    half=T//2; return _iris(img,[(T-1-i)/(half-1) for i in range(half,T)],half)

def transition(a_img,b_img,T=22):
    """The whole thing, A closing then B opening: what the app plays, as iris_out(A) + iris_in(B)."""
    return iris_out(a_img,T)+iris_in(b_img,T)
