"""Inglourious Basterds, sub-theme "basterds-cinema": the premiere at Le Gamaar. Claude as Shosanna, in the
red dress, at the end of the aisle while Stolz der Nation plays to a full house (the sniper in his bell
tower, the grain, the projector's beam over the rows of caps). Clip `cinema`: she slips out — CHAPTER FIVE:
REVENGE OF THE GIANT FACE — the reel cuts, her face comes up on the screen: THIS IS THE FACE OF JEWISH
VENGEANCE.; behind it the nitrate catches, the fire climbs the curtains; close-up: her face thrown onto the
smoke, laughing; the screen is gone, the house in flames."""
from engine import *

THEME = 'basterds-cinema'
N_ = 384                                                            # a multiple of 12
INK = (20,16,12)
register_bg(THEME, lambda v: (v+40,v+10,v+10))                      # every frame is drawn whole

SCR = (52,4,132,36)                                                 # the screen
def _theatre(d,lit):
    """The auditorium: red walls, the boxes, the curtains, the screen's frame, the rows of seats."""
    d.rectangle([0,0,W,H],fill=(int(40*lit+14),int(8*lit+6),int(10*lit+6)))
    for x in (8,24,160,176): d.rectangle([x-6,8,x+6,22],outline=(int(150*lit+30),int(120*lit+20),int(50*lit+10)))   # the boxes
    for x0,x1 in ((38,SCR[0]),(SCR[2],146)):                          # the curtains
        d.rectangle([x0,0,x1,40],fill=(int(130*lit+20),int(16*lit+6),int(20*lit+6)))
        for x in range(x0+2,x1,4): d.line([x,0,x,40],fill=(int(90*lit+14),int(10*lit+4),int(14*lit+4)))
    d.rectangle([SCR[0]-1,SCR[1]-1,SCR[2]+1,SCR[3]+1],outline=(int(170*lit+30),int(140*lit+20),int(60*lit+10)))
    d.rectangle([30,37,154,40],fill=(int(50*lit+10),int(30*lit+8),int(20*lit+6)))   # the stage

def _audience(d,lit,f,panic=0.0):
    """Rows of the audience from behind: heads and caps in silhouette, the seat backs red."""
    rr=random.Random(5)
    for row,(y,sz,step) in enumerate(((44,3,9),(50,4,11),(58,5,13))):
        for i in range(-1,W//step+2):
            x=i*step+(row*5)%step+rr.randint(-1,1)
            jit=int(panic*3*math.sin(f*0.9+i*1.7+row)) if panic else 0
            d.rectangle([x-sz-1,y+sz,x+sz+1,H],fill=(int(60*lit+10),int(10*lit+4),int(12*lit+4)))   # seat back
            c=(int(10+20*lit),int(10+18*lit),int(12+16*lit))
            d.ellipse([x-sz+jit,y-sz+abs(jit),x+sz+jit,y+sz+abs(jit)],fill=c)
            d.arc([x-sz+jit,y-sz+abs(jit),x+sz+jit,y+sz+abs(jit)],200,340,fill=(int(70+90*lit),int(66+80*lit),int(60+70*lit)))   # the screen's light on them
            if rr.random()<0.5: d.rectangle([x-sz-1+jit,y-sz-1+abs(jit),x+sz+1+jit,y-sz+1+abs(jit)],fill=c)   # a cap
            if panic and rr.random()<0.4: d.line([x+jit,y,x+jit+(3 if i%2 else -3),y-sz-3],fill=c,width=2)  # arms up

def _beam(im,a):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon([(84,H),(100,H),(SCR[2],SCR[3]),(SCR[0],SCR[3])],fill=int(30*a))
    im.paste((230,230,210),(0,0),m.filter(ImageFilter.GaussianBlur(2)))

def _warfilm(d,f):
    """Stolz der Nation: the sniper up in his bell tower, the muzzle flashes, the grain."""
    x0,y0,x1,y1=SCR; d.rectangle(SCR,fill=(150,150,146))
    d.rectangle([x0,y1-8,x1,y1],fill=(90,90,88))
    d.rectangle([x0+50,y0+6,x0+62,y1-8],fill=(70,70,70)); d.polygon([(x0+48,y0+6),(x0+56,y0+1),(x0+64,y0+6)],fill=(60,60,60))
    d.rectangle([x0+53,y0+9,x0+59,y0+15],fill=(20,20,20)); d.ellipse([x0+54,y0+10,x0+57,y0+13],fill=(200,200,196))
    if (f//4)%3==0: d.ellipse([x0+48,y0+10,x0+53,y0+14],fill=(250,250,240))
    rr=random.Random(f%12)
    for _ in range(10): d.point((rr.randint(x0,x1),rr.randint(y0,y1)),fill=(40,40,40))
    if f%12==0: d.line([rr.randint(x0,x1),y0,rr.randint(x0,x1),y1],fill=(200,200,196))   # a scratch

def shosanna(d,cx,cy,k,mouth,tone=lambda c:c):
    """Her face, k = scale: hair up, the dark lips (speaking or laughing: mouth 0..1)."""
    sk,hr,ink=tone((210,206,200)),tone((70,60,56)),tone((20,18,18))
    d.ellipse([cx-12*k,cy-15*k,cx+12*k,cy+16*k],fill=sk)
    d.chord([cx-13*k,cy-17*k,cx+13*k,cy-1*k],180,360,fill=hr)                       # the hair, swept up
    d.ellipse([cx-5*k,cy-21*k,cx+5*k,cy-13*k],fill=hr); d.ellipse([cx-14*k,cy-10*k,cx-9*k,cy+2*k],fill=hr)   # the bun, a curl
    for ex in (-6,4): d.rectangle([cx+ex*k,cy-2*k,cx+(ex+3)*k,cy],fill=ink); d.line([cx+ex*k,cy-5*k,cx+(ex+4)*k,cy-5*k],fill=hr,width=max(1,int(k)))
    d.line([cx,cy+1*k,cx-1*k,cy+6*k],fill=tone((170,166,160)))
    d.ellipse([cx-5*k,cy+9*k,cx+5*k,cy+(10+4*mouth)*k],fill=tone((60,30,30)))

def _onscreen_face(d,f):
    x0,y0,x1,y1=SCR; d.rectangle(SCR,fill=(40,40,40))
    shosanna(d,(x0+x1)//2,(y0+y1)//2+3,1,0.6 if (f//4)%2 else 0.1)
    rr=random.Random(f)
    for _ in range(8): d.point((rr.randint(x0,x1),rr.randint(y0,y1)),fill=(90,90,90))

def _burn(im,d,f,a):
    """Fire: along the bottom of the screen, up the curtains; smoke under the ceiling (a 0..1)."""
    for i,x in enumerate(range(SCR[0],SCR[2]+1,10)):
        draw_fx(d,im,('fire',x+((f+i*3)%5)-2,SCR[3]+3,2+a*3),f)
    if a>0.4:
        for x in (42,46,138,142): draw_fx(d,im,('fire',x,40,2+a*2),f)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); rr=random.Random(9)
    for i in range(16):
        x=rr.uniform(0,W)+math.sin((f+i*13)/11)*6; y=rr.uniform(-6,16)*a; r=rr.uniform(8,16)*a
        md.ellipse([x-r,y-r*0.6,x+r,y+r*0.6],fill=int(150*a))
    im.paste((40,34,34),(0,0),m.filter(ImageFilter.GaussianBlur(3)))

def chapter_card(t,f):
    im=Image.new('RGB',(W,H),(6,6,6))
    big_text(im,"CHAPTER FIVE",6,(240,230,200),scale=2,shadow=None)
    if t>=0.2:
        big_text(im,"REVENGE OF",26,(220,40,30),scale=2,shadow=None)
        big_text(im,"THE GIANT FACE",44,(220,40,30),scale=2,shadow=None)
    return im

def closeup_smoke(t,f):
    """Primer plano: her face, huge, thrown onto the smoke, laughing, the fire under it."""
    im=Image.new('RGB',(W,H),(20,12,10)); d=ImageDraw.Draw(im)
    for i in range(10):                                              # the fire below
        draw_fx(d,im,('fire',i*20+((f+i*7)%9),H+4,4),f)
    face=Image.new('RGB',(W,H),(0,0,0)); fd=ImageDraw.Draw(face)
    shosanna(fd,W//2,32,1.6,0.9 if (f//3)%2 else 0.3)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); rr=random.Random(3)  # the smoke she's projected onto
    for i in range(30):
        x=rr.uniform(0,W)+math.sin((f+i*9)/10)*8; y=rr.uniform(0,H)-((f*0.5+i*7)%20); r=rr.uniform(10,22)
        md.ellipse([x-r,y-r,x+r,y+r],fill=int(rr.uniform(90,170)))
    m=m.filter(ImageFilter.GaussianBlur(4))
    smoke=Image.new('RGB',(W,H),(70,60,56))
    lit=Image.composite(Image.blend(smoke,face,0.7),smoke,face.convert('L').point(lambda v:255 if v>0 else 0))
    a=min(1,t/0.3); im.paste(lit,(0,0),m.point(lambda v:int(v*a)))
    return im

# Shosanna, in the red dress, at the end of the aisle (from the side, facing the screen)
SHOS = S([
"....hhh.....","...hhhhh....","...hhsss....","...hsKsK....","....ssss....",".....ss.....",
"...rrrrr....","..srrrrrs...","..srrrrrs...","..s.rrr.s...","...rrrrr....","..rrrrrrr...",
"..rrrrrrr...",".rrrrrrrrr..","....s..s....","....k..k....",])
SPAL = {'h':(196,150,96),'s':(236,206,184),'K':INK,'r':(200,24,30),'k':(30,10,12)}
SHX = 20

def auditorium(f,step=0.0):
    """The neutral frame: the premiere going, Stolz der Nation on the screen, Shosanna by the aisle."""
    lit=0.35+(0.08 if (f//3)%2 else 0)
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    _theatre(d,lit); _warfilm(d,f); _beam(im,1.0); d=ImageDraw.Draw(im)
    _audience(d,lit,f)
    return im

def with_shosanna(im,x,f):
    if x is not None: draw(im,SHOS,x,GROUND+4,False,pal=SPAL)
    return im

def clip_cinema(f):
    s=scene(f,THEME)
    if f<14 or f>=N_: s['image']=with_shosanna(auditorium(f),SHX,f); return s
    if f<40: s['image']=with_shosanna(auditorium(f),lerp(SHX,-10,(f-14)/26),f); return s     # she slips out
    if f<102: s['image']=chapter_card((f-40)/62,f); return s
    if 232<=f<292: s['image']=closeup_smoke((f-232)/60,f); return s
    if f>=358:
        im=with_shosanna(auditorium(f),SHX,f); s['image']=fade_to(im,(0,0,0),1-(f-358)/26); return s
    burn=0.0 if f<222 else min(0.6,(f-222)/16) if f<232 else min(1,0.6+(f-292)/30)
    lit=0.35+0.15*burn+(0.08 if (f//3)%2 else 0)
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    _theatre(d,lit)
    if f<150: _warfilm(d,f)
    elif f<160: d.rectangle(SCR,fill=(250,250,246) if (f//2)%2 else (30,30,30))   # the reel cuts
    elif f<300: _onscreen_face(d,f)
    else: d.rectangle(SCR,fill=(30,20,16))                           # the screen is gone
    _beam(im,1.0 if f<300 else 0.0); d=ImageDraw.Draw(im)
    if burn>0: _burn(im,d,f,burn); d=ImageDraw.Draw(im)
    _audience(d,lit,f,panic=0.0 if f<292 else 1.0)
    if 160<=f<222:
        for i,l in enumerate(("THIS IS THE FACE OF","JEWISH VENGEANCE.")):
            w=len(l)*4; text(d,l,W//2-w//2,40+i*7,(250,246,236))
    if f>=292:
        rr=random.Random(f)
        for _ in range(12): d.point((rr.randint(0,W-1),rr.randint(0,H-1)),fill=(255,180,80))   # embers
    if f>=338: im=fade_to(im,(0,0,0),min(1,(f-338)/20))
    s['image']=im; return s

CLIPS = [clip('cinema', N_, clip_cinema)]
