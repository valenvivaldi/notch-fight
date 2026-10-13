"""Transitions between two themes' loop keyframes. They are built per theme, not per pair: one half closes
on the theme being left (out) and the other opens on the one arriving (in), each to or from black, so
each theme needs just its own halves and any out goes with any in.

Several styles; the app picks one at random on each change of theme (config "transitions": "mix", or a
style's name to always use that one):
  iris      the asterisk iris (transitions/<theme>__out, <theme>__in: also what the Claude Code mod plays)
  dissolve  the picture falls apart into black in square blocks
  wipe      a diagonal sweep with an orange edge
  crt       an old TV switching off: squashed to a bright line, then to a dot
A theme can have its own instead (TRANSITION = '<style>' in its module, e.g. the cinema's curtain): then
that is its only style. The theme's first style is <theme>__out / __in; the others <theme>__out__<style>."""
from engine import *

ORANGE = (217, 119, 87)
HALF = 11                                                      # frames per half (22 for a whole change)
GENERIC = ['iris', 'dissolve', 'wipe', 'crt']

def asterisk_thick(d,x,y,r,f,c=(217,119,87)):
    for k in range(8):
        a=k*math.pi/4+f*0.25; L=r*(1 if k%2==0 else 0.75)
        d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=c,width=max(1,int(r/5)))
    d.ellipse([x-r*0.18,y-r*0.18,x+r*0.18,y+r*0.18],fill=c)

# Each style: (img, t, k) -> frame, t from 0 (the picture) to 1 (closed), k the frame's place in the whole
# 22-frame change (for what keeps turning across both halves).

def iris(img,t,k):
    r=int(lerp(115,0,t)); cx,cy=W//2,GROUND-12
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
    im=Image.composite(img,Image.new('RGB',(W,H)),m)
    asterisk_thick(ImageDraw.Draw(im),cx,cy,int(4+14*t),k)
    return im

BLOCK = 5
_ORDER = random.Random(7).sample([(x,y) for y in range(0,H,BLOCK) for x in range(0,W,BLOCK)],
                                 len(range(0,H,BLOCK))*len(range(0,W,BLOCK)))   # the same in every build
def dissolve(img,t,k):
    im=img.copy(); d=ImageDraw.Draw(im)
    for x,y in _ORDER[:round(t*len(_ORDER))]: d.rectangle([x,y,x+BLOCK-1,y+BLOCK-1],fill=(0,0,0))
    return im

def wipe(img,t,k):
    slope=0.8; edge=lerp(-6,W+H*slope+6,t)                     # the edge travels from the left past the right
    m=Image.new('L',(W,H),255)
    ImageDraw.Draw(m).polygon([(edge,0),(edge-H*slope,H),(-1,H),(-1,0)],fill=0)
    im=Image.composite(img,Image.new('RGB',(W,H)),m); d=ImageDraw.Draw(im)
    if 0<t<1:
        for o,c in ((0,ORANGE),(2,(120,64,48))): d.line([(edge+o,0),(edge+o-H*slope,H)],fill=c,width=2)
    return im

def crt(img,t,k):
    im=Image.new('RGB',(W,H)); cy=H//2
    if t>=1: return im
    if t<0.6:                                                  # squashed towards a bright line
        u=t/0.6; h=max(2,round(H*(1-u)**1.5))
        squashed=Image.blend(img.resize((W,h),Image.NEAREST),Image.new('RGB',(W,h),(255,255,255)),min(1,u*1.2))
        im.paste(squashed,(0,cy-h//2))
    else:                                                      # the line shrinks to a dot, then out
        w=max(2,round(W*(1-(t-0.6)/0.4)**2))
        ImageDraw.Draw(im).rectangle([W//2-w//2,cy-1,W//2+w//2,cy],fill=(255,255,255))
    return im

def curtain(img,t,k):
    """Red stage curtains closing from both sides, folds and a gold fringe (the cinema)."""
    im=img.copy(); d=ImageDraw.Draw(im); reach=round(lerp(0,W//2+2,(t/0.75)**0.8))   # closed by t = 0.75
    for side in (0,1):
        for i in range(reach):
            x=i if side==0 else W-1-i; fold=(reach-i)%9          # the folds travel with the cloth
            d.line([(x,0),(x,H-1)],fill=((150 if fold<4 else 120 if fold<6 else 95),18,24))
        if reach:
            x0,x1=(0,reach-1) if side==0 else (W-reach,W-1)
            d.rectangle([x0,H-3,x1,H-1],fill=(200,150,40))
            for x in range(x0,x1+1,3): d.point((x,H-4),fill=(160,110,30))
    if t>0.75: im=Image.blend(im,Image.new('RGB',(W,H)),(t-0.75)/0.25)   # then the lights go down, to black
    return im

STYLES = {'iris': iris, 'dissolve': dissolve, 'wipe': wipe, 'crt': crt, 'curtain': curtain}

def half_out(style,img):
    """Leaving a theme: the picture closes (the first half of a change)."""
    fn=STYLES[style]; return [fn(img,i/(HALF-1),i) for i in range(HALF)]

def half_in(style,img):
    """Arriving at a theme: it opens (the second half)."""
    fn=STYLES[style]; return [fn(img,(HALF-1-i)/(HALF-1),HALF+i) for i in range(HALF)]

def iris_out(img,T=22): return half_out('iris',img)
def iris_in(img,T=22): return half_in('iris',img)

def transition(a_img,b_img,T=22,style='iris'):
    """The whole thing, A closing then B opening, as the app plays it."""
    return half_out(style,a_img)+half_in(style,b_img)
