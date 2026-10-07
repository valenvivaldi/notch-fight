"""Jujutsu Kaisen: Claude (Gojo: white hair, blindfold) vs Sukuna at the Shibuya scramble crossing
on the night of 10.31. Sukuna's Dismantle slashes carve the street but stop dead on Infinity, his
lunge freezes an inch from Claude's face (MUGEN). Close-up: the blindfold comes off — SIX EYES.
Blue drags Sukuna into the air, Red blasts him into the 109 tower; he laughs it off and comes back,
so Claude joins the two — close-up: HOLLOW PURPLE — and erases a strip of Shibuya with him in it.
Sukuna reforms from a swarm of cursed motes, the blindfold goes back on."""
from engine import *

THEME = 'jjk'
N_ = 336
CX, EX = 30, 150                                                    # the loop keyframe positions

# ---- local glyphs: a wider M and W (the 3x5 font's read as H) ------------------------------------
_GLYPH = {'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"), 'W':(5,"10001"+"10001"+"10101"+"11011"+"10001")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,''.join(FONT.get(ch,FONT[' '])[j*3:j*3+3] for j in range(5))) for ch in txt]
    m=Image.new('L',(sum(w+1 for w,_ in gl)-1,5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=1,cx=W//2,outline=None,shadow=(0,0,0)):
    """Like big_text, with the local glyphs; scale=1 gives a normal callout."""
    m=_mask(txt); m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

@fx('jjk_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('jjk_say',txt,y,c,scale,cx,outline))

# ---- Claude as Gojo: tall white hair held up by the black blindfold; without it the hair falls
#      over the forehead and the Six Eyes show (blue) -----------------------------------------------
def _gojo(spr,eyes):
    top,l,r=body_box(spr); g=grid(spr)
    rows=[y for y,row in enumerate(g) if 'K' in ''.join(row[l:r+1])]
    for y in rows:
        for x in range(l,r+1):
            if eyes and g[y][x]=='K': g[y][x]='E'
            elif not eyes and g[y][x] in 'OK': g[y][x]='b'
    if not eyes and rows and l>=1:                                  # the knot's tails, behind the head
        g[rows[0]][l-1]='b'
        if l>=2 and rows[0]+1<len(g): g[rows[0]+1][l-2]='b'
    s=ungrid(g)
    if eyes: return overlay(s,["..H.H..H.H.",".HHHHHHHHHH","HHhHHHHHhHH"],-2,0,bangs="HhH.HH.hH")
    return overlay(s,["..H..H...H..","..HH.HH.HH..",".HHHHHHHHHH.","HHHhHHHhHHHH","HhHHHHHHHHh.",".hHHHHHHHh.."],-2,0)
GOJO=variant(lambda s: _gojo(s,False))
GOJO_EYES=variant(lambda s: _gojo(s,True))
EYEPAL={'E':(120,210,255)}
BLUE=((150,210,255),(50,110,245))
RED=((255,150,140),(225,30,45))
PURPLE=((214,160,255),(130,40,210))
INF_C=(150,200,255)

# ---- Sukuna (in Yuji's body): pink hair, the face tattoos, a grin, white kimono with a dark sash ----
SUKUNA=poses(S([
".....n.n.n......",
"....nnnnnnn.....",
"...nnnnnnnnn....",
"...nsssssssn....",
"...skrsssrks....",
"...sksssssks....",
"...ssWkWkWss....",
"....sskkkss.....",
".....ssss.......",
"...WWWWWWWW.....",
"..WWWWkWWWWW....",
"..WWWWWkWWWW....",
"..sWWWWWWWWs....",
"..s.kkkkkk.s....",
"....WWWWWW......",
"....WWWWWW......",
"....WW..WW......",
"....WW..WW......",
"....vv..vv......",
"...kkk..kkk.....",]),12,'s',4)
SUKUNA_AURA=(220,40,50)

# ---- background: the Shibuya scramble crossing at night -------------------------------------------
HZ=44                                                               # back edge of the street
def _mix(a,b,k): return tuple(int(lerp(a[i],b[i],k)) for i in range(3))

def _glow(im,x,y,rx,ry,c,a):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([x-rx,y-ry,x+rx,y+ry],fill=a)
    im.paste(c,(0,0),m.filter(ImageFilter.GaussianBlur(max(1,min(rx,ry)//2))))

def city(d,ruined=False):
    """Shibuya: QFRONT's big screen, the JR viaduct with the station sign, the 109 tower, lamps and
    the zebra stripes of the crossing. ruined=True: the same street after the fight (jjk-sukuna)."""
    im=d._image; rr=random.Random(1031)
    top,bot=((18,2,8),(104,24,22)) if ruined else ((6,6,24),(56,30,78))
    for y in range(HZ): d.line([0,y,W,y],fill=_mix(top,bot,y/(HZ-1)))
    if ruined:                                                      # a red moon over the smoke
        _glow(im,112,11,14,12,(160,30,30),120); d=ImageDraw.Draw(im)
        d.ellipse([105,4,119,18],fill=(214,64,54)); d.ellipse([108,6,114,11],fill=(236,110,90))
    else:
        for _ in range(26): d.point((rr.randint(0,W-1),rr.randint(0,18)),fill=rr.choice([(90,90,130),(160,160,200)]))
    far=(46,16,22) if ruined else (24,24,50)                        # the far skyline
    x=0
    while x<W:
        w=rr.randint(6,13); t=rr.randint(16,30)
        if ruined: d.polygon([(x,HZ),(x,t+rr.randint(0,6)),(x+w//2,t),(x+w,t+rr.randint(2,9)),(x+w,HZ)],fill=far)
        else:
            d.rectangle([x,t,x+w,HZ],fill=far)
            for wy in range(t+2,HZ-2,3):
                for wx in range(x+1,x+w,2):
                    if rr.random()<0.3: d.point((wx,wy),fill=rr.choice([(255,210,120),(120,220,255),(70,70,110)]))
        x+=w+rr.randint(0,2)
    lit=(lambda: rr.random()<0.12) if ruined else (lambda: rr.random()<0.55)
    wall=(40,30,38) if ruined else (32,30,58)
    # QFRONT: the glass corner with the giant screen
    d.rectangle([0,4,36,HZ],fill=wall); d.rectangle([3,7,33,27],fill=(14,14,20))
    for wy in range(30,HZ-1,3):
        for wx in range(2,35,3):
            if lit(): d.point((wx,wy),fill=(150,220,255) if not ruined else (255,140,60))
    if ruined: d.polygon([(0,4),(36,4),(36,12),(30,9),(24,14),(18,8),(10,13),(0,7)],fill=top)
    # a mid block with a vertical neon sign
    d.rectangle([38,20,58,HZ],fill=wall)
    for wy in range(23,HZ-1,3):
        for wx in range(40,52,3):
            if lit(): d.point((wx,wy),fill=(255,214,130) if not ruined else (255,120,50))
    d.rectangle([53,22,57,40],fill=(40,10,30) if ruined else (255,90,170))
    for k in range(5): d.rectangle([54,23+k*3,56,24+k*3],fill=(20,10,20) if ruined else (255,220,240))
    # the JR viaduct and the station sign
    d.rectangle([58,24,130,31],fill=(38,24,30) if ruined else (40,40,64))
    for x0 in range(60,131,10):
        for wy in (26,28):
            if lit(): d.point((x0+rr.randint(0,6),wy),fill=(255,230,170))
    d.rectangle([58,32,130,36],fill=(70,54,56) if ruined else (78,78,100)); d.line([58,32,130,32],fill=(120,110,120) if ruined else (130,130,160))
    for x0 in (62,84,106,126): d.rectangle([x0,37,x0+3,HZ],fill=(56,44,46) if ruined else (60,60,82))
    d.rectangle([79,31,109,37],fill=(150,140,130) if ruined else (232,236,236)); text(d,"SHIBUYA",81,32,(30,110,60),shadow=None)
    # a billboard block
    d.rectangle([132,16,149,HZ],fill=wall)
    for i,c in enumerate([(255,210,60),(80,220,255),(255,90,170)]):
        d.rectangle([134,19+i*7,147,24+i*7],fill=_mix(c,(30,20,20),0.7) if ruined else c)
        d.line([136,21+i*7,136+rr.randint(4,9),21+i*7],fill=(30,30,40))
    # the 109 tower: a silver cylinder crowned with the red sign
    for x0 in range(151,175):
        k=abs(x0-161)/12; d.line([x0,10,x0,HZ],fill=_mix((176,176,196) if not ruined else (120,100,104),(70,70,92) if not ruined else (50,36,40),k))
    for wy in range(14,HZ,4): d.line([152,wy,174,wy],fill=(90,90,114) if not ruined else (60,44,48))
    d.rectangle([151,2,175,10],fill=(20,16,22)); d.rectangle([151,2,175,10],outline=(230,40,60) if not ruined else (110,30,34))
    text(d,"109",157,4,(255,70,90) if not ruined else (120,40,40),shadow=None)
    if ruined: d.polygon([(151,2),(158,2),(155,6),(160,10),(151,10)],fill=top); d.line([165,14,170,26],fill=(30,20,20)); d.line([170,26,166,34],fill=(30,20,20))
    d.rectangle([176,20,W,HZ],fill=wall)
    # the street
    d.rectangle([0,HZ,W,HZ+1],fill=(66,60,70) if ruined else (70,68,90)); d.line([0,HZ+2,W,HZ+2],fill=(110,104,110) if ruined else (120,120,146))
    d.rectangle([0,HZ+3,W,H],fill=(34,30,34) if ruined else (34,34,48))
    for x0 in range(-24,W+24,8):                                    # zebra stripes, in perspective
        xt=92+(x0-92)*0.82
        d.polygon([(xt,48),(xt+3,48),(x0+4,57),(x0,57)],fill=(80,72,76) if ruined else (100,100,120))
    d.line([0,GROUND+1,W,GROUND+1],fill=(60,56,62) if ruined else (70,70,92))
    for x0 in range(4,W,16): d.line([x0,62,x0+7,62],fill=(120,100,40) if ruined else (210,180,70))
    for lx in (66,122):                                             # street lamps
        if ruined and lx==122:
            d.line([lx,HZ+1,lx+12,30],fill=(50,44,50)); continue
        _glow(im,lx,52,24,6,(120,104,80) if not ruined else (90,40,20),70 if not ruined else 40); d=ImageDraw.Draw(im)
        d.line([lx,18,lx,HZ+1],fill=(54,54,70)); d.line([lx,18,lx+4,18],fill=(54,54,70))
        d.rectangle([lx+3,19,lx+6,20],fill=(255,236,180) if not ruined else (120,80,50))
    d.line([44,30,44,HZ+1],fill=(54,54,70)); d.rectangle([42,30,46,34],fill=(20,20,26))   # the signal
    d.point((44,32),fill=(80,255,140) if not ruined else (60,40,40))
    if ruined:                                                      # rubble, cracks, scorch
        for cx0,w0 in ((88,10),(140,14),(20,8)):
            for k in range(w0*2):
                x0=cx0+rr.randint(-w0,w0); y0=GROUND-rr.randint(0,max(1,int((w0-abs(x0-cx0))/3))); d.rectangle([x0,y0,x0+1,y0+1],fill=rr.choice([(70,62,66),(100,90,92),(46,40,44)]))
        for _ in range(6):
            x0=rr.randint(0,W); pts=[(x0,HZ+3)]
            for _ in range(4): x0+=rr.randint(-5,5); pts.append((x0,pts[-1][1]+rr.randint(2,4)))
            d.line(pts,fill=(14,12,14))
register_bg(THEME, lambda v: (v+20,v+20,v+40), decor=city)

# ---- effects -------------------------------------------------------------------------------------
@fx('jjk_city')
def _fx_city(d,im,e,f):
    """The living street: QFRONT's screen cycles ads, a neon sign flickers, the Yamanote train
    crosses the viaduct once per clip (n = the clip length, so the loop is seamless)."""
    _,n,ruined=e
    if ruined:                                                      # a dead screen and burning windows
        g=f%n                                                       # frame n is frame 0: the noise and fire loop too
        rr=random.Random(g//2)
        for _ in range(20): d.point((rr.randint(4,32),rr.randint(8,26)),fill=rr.choice([(60,60,70),(30,30,40),(120,120,130)]))
        FX['fire'](d,im,('fire',12,24,2),g); FX['fire'](d,im,('fire',100,HZ+1,2),g); FX['fire'](d,im,('fire',180,28,2),g)
        return
    k=(f*6//n)%3
    if k==0:
        for y in range(8,27): d.line([4,y,32,y],fill=_mix((40,80,220),(220,60,200),(y-8)/18))
        text(d,"CLAUDE",6,15,(255,255,255))
    elif k==1:
        d.rectangle([4,8,32,26],fill=(30,20,18)); asterisk(d,18,17,7,(217,119,87),f); d.ellipse([16,15,20,19],fill=(217,119,87))
    else:
        d.rectangle([4,8,32,26],fill=(250,210,70)); text(d,"JJK",12,11,(30,20,40),shadow=None)
        d.rectangle([6,19,30,24],fill=(230,40,60)); d.line([8,21,8+(f%20),21],fill=(255,255,255))
    if f%48 in (3,4,9):                                             # the pink sign stutters
        d.rectangle([53,22,57,40],fill=(60,20,50))
    p=(f%n)/n                                                       # the train: one pass, 8%..45%
    if 0.08<=p<0.45:
        x=int(W+4-(p-0.08)/0.37*(W+100))
        for c in range(4):
            x0=x+c*22; d.rectangle([x0,26,x0+20,31],fill=(190,196,200)); d.line([x0,29,x0+20,29],fill=(120,200,90))
            for wx in range(x0+2,x0+19,4): d.rectangle([wx,27,wx+2,28],fill=(255,240,190))

@fx('slash')
def _fx_slash(d,im,e,f):
    _,x,y,L,c=e; d.line([x,y,x+L,y-L*0.8],fill=c); d.line([x+1,y,x+L+1,y-L*0.8],fill=(255,255,255))

@fx('jjk_scar')
def _fx_scar(d,im,e,f):
    """A cut left by Dismantle on a wall or the road."""
    _,x,y,L=e; d.line([x,y,x+L,y-L*0.6],fill=(10,8,12)); d.line([x,y+1,x+L,y-L*0.6+1],fill=(200,190,210))

@fx('jjk_ripple')
def _fx_ripple(d,im,e,f):
    """Infinity: a dotted shimmer where something is kept from touching Claude."""
    _,x,y,r,c=e
    for k in range(20):
        a=k*math.pi/10+f*0.2
        if (k+f)%3: d.point((int(x+math.cos(a)*r*0.5),int(y+math.sin(a)*r)),fill=c)

@fx('jjk_orb')
def _fx_orb(d,im,e,f):
    """An orb with a soft glow and a flickering corona: x,y,r,(outer,mid)."""
    _,x,y,r,(oc,mc)=e; x,y,r=int(x),int(y),int(r)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-r-5,y-r-5,x+r+5,y+r+5],fill=110)
    im.paste(oc,(0,0),g.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    ball(d,x,y,r,oc,mc,f); asterisk(d,x,y,r+3,oc,f)

@fx('jjk_crater')
def _fx_crater(d,im,e,f):
    """A body-shaped dent in a wall with cracks running out of it."""
    _,x,y=e; rr=random.Random(109)
    for k in range(7):
        a=k*0.9+rr.random()*0.4; pts=[(x,y)]; px,py=x,y
        for _ in range(3): px+=math.cos(a)*4+rr.randint(-1,1); py+=math.sin(a)*4+rr.randint(-1,1); pts.append((px,py))
        d.line(pts,fill=(20,16,24))
    d.ellipse([x-4,y-6,x+4,y+6],fill=(24,20,30)); d.ellipse([x-2,y-4,x+2,y+4],fill=(10,8,12))

@fx('jjk_wake')
def _fx_wake(d,im,e,f):
    """What Hollow Purple leaves: a strip where nothing is left, rimmed in violet."""
    _,x0,x1,y,hh,a=e; x0,x1=int(max(0,x0)),int(min(W,x1))
    if x1<=x0 or a<=0: return
    rr=random.Random(77); m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    pts_t=[(x,y-hh+rr.randint(-2,2)) for x in range(x0,x1+1,4)]; pts_b=[(x,y+hh+rr.randint(-2,1)) for x in range(x1,x0-1,-4)]
    md.polygon(pts_t+pts_b,fill=int(255*a)); im.paste((10,2,20),(0,0),m)
    rim=_mix((10,2,20),(190,120,255),a)
    d.line(pts_t,fill=rim); d.line(pts_b[::-1],fill=rim)

@fx('jjk_motes')
def _fx_motes(d,im,e,f):
    """Cursed energy swirling in to (x,y) — Sukuna putting himself back together (t 0..1)."""
    _,x,y,t=e; rr=random.Random(5)
    for i in range(24):
        a=i*2.4+f*0.25; L=(1-t)*34*(0.5+rr.random())
        d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L*0.5)),fill=(230,40,60) if i%3 else (40,0,10))

# ---- close-up 1: the blindfold comes off — SIX EYES -----------------------------------------------
_BOKEH=[(random.Random(i).randint(0,W),random.Random(i+50).randint(0,H),random.Random(i+99).randint(4,10),
         random.Random(i+7).choice([(255,90,170),(80,200,255),(255,210,90),(160,120,255)])) for i in range(14)]
def _night(dim=1.0):
    im=Image.new('RGB',(W,H),(10,10,30))
    g=Image.new('RGB',(W,H),(0,0,0)); gd=ImageDraw.Draw(g)
    for x,y,r,c in _BOKEH: gd.ellipse([x-r,y-r,x+r,y+r],fill=_mix((0,0,0),c,0.55*dim))
    return Image.composite(g.filter(ImageFilter.GaussianBlur(3)),im,g.convert('L').point(lambda v: 255 if v>12 else 0))

def _spikes(d,down,ox):
    """Gojo's hair: spikes standing straight up (down=0) or fallen over the forehead (down=1)."""
    for i in range(10):
        x0=40+i*7+ox; up=(4 if i%2 else 0)+(i*37%5)
        tip=(x0+4+(i%3-1)*3-6*(1-down)*((i-4)/5), lerp(2+up,30+up//2,down))
        d.polygon([(x0,26),(x0+9,26),tip],fill=(242,242,250),outline=(186,186,206))
    d.rectangle([40+ox,22,110+ox,28],fill=(242,242,250))
    if down>0.5:                                                    # the bangs
        for i in range(6):
            x0=48+i*10+ox; d.polygon([(x0,26),(x0+10,26),(x0+4+(i%2)*3,int(26+12*(down-0.5)*2))],fill=(242,242,250),outline=(186,186,206))

def _eye(d,im,ex,ey,f,big=1.0):
    d.rounded_rectangle([ex-8,ey-12,ex+8,ey+12],radius=6,fill=(24,14,12))
    d.rounded_rectangle([ex-6,ey-10,ex+6,ey+10],radius=5,fill=(40,110,240))
    d.rounded_rectangle([ex-4,ey-7,ex+4,ey+8],radius=4,fill=(120,200,255))
    d.ellipse([ex-2,ey-3,ex+2,ey+3],fill=(230,248,255))
    d.point((ex-3,ey-8),fill=(255,255,255)); d.point((ex+2,ey-7),fill=(255,255,255))
    if (f//2)%2: d.point((ex+3,ey+6),fill=(255,255,255))
    for k in range(4): d.line([ex-7+k*4,ey-12,ex-8+k*4,ey-15],fill=(242,242,250))   # white lashes

def closeup_sixeyes(t,f):
    """Primer plano: a hand pulls the blindfold down, the hair falls, the Six Eyes open."""
    im=_night(); d=ImageDraw.Draw(im)
    pull=ease((t-0.14)/0.3)                                         # 0 on, 1 pulled down to the neck
    opened=t>=0.5
    if opened:                                                      # the eyes' blue glow behind
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([30,4,140,70],fill=int(90*min(1,(t-0.5)/0.1)))
        im.paste((60,140,255),(0,0),g.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    ox=0
    _spikes(d,pull,ox)
    d.rectangle([44,28,106,64],fill=(217,119,87)); d.rectangle([44,28,49,64],fill=(176,92,66))
    _spikes_front=pull>0.5
    if _spikes_front:
        for i in range(6):
            x0=48+i*10; d.polygon([(x0,27),(x0+10,27),(x0+4+(i%2)*3,int(27+10*(pull-0.5)*2))],fill=(242,242,250),outline=(186,186,206))
    for ex in (64,88):
        if opened: _eye(d,im,ex,44,f)
        else: d.rounded_rectangle([ex-2,40,ex+2,48],radius=1,fill=(24,14,12))
    by=int(34+26*pull)                                              # the blindfold slides down
    d.rectangle([42,by,108,by+11],fill=(26,26,34)); d.line([42,by+10,108,by+10],fill=(60,60,76))
    d.line([42,by+1,108,by+1],fill=(48,48,62))
    if 0.1<=t<0.56:                                                 # the hand hooking the cloth
        hy=by+8; hx=100
        d.rounded_rectangle([hx-4,hy,hx+14,hy+14],radius=3,fill=(217,119,87),outline=(24,14,12))
        for k in range(3): d.rectangle([hx-8,hy+1+k*4,hx,hy+3+k*4],fill=(217,119,87),outline=(24,14,12))
        if hy+14<H: d.rectangle([hx+4,hy+14,hx+12,H],fill=(168,80,54))
    if 0.5<=t<0.56:
        im=fade_to(im,(220,240,255),1-(t-0.5)/0.06); d=ImageDraw.Draw(im); zoom_lines(d,(150,210,255))
    if t>=0.58:
        jj=(f%3)-1 if t<0.66 else 0
        say(im,"SIX",8,(230,246,255),scale=3,cx=148+jj,outline=(30,70,160))
        say(im,"EYES",32,(150,210,255),scale=3,cx=148+jj,outline=(30,70,160))
        rr=random.Random(f//2)
        for _ in range(10): d.point((rr.randint(40,110),rr.randint(22,64)),fill=(200,236,255))
    if t<0.06: zoom_lines(d)
    if t>0.92: im=fade_to(im,(10,10,30),(t-0.92)/0.08*0.6)
    return im

# ---- close-up 2: Blue and Red become HOLLOW PURPLE ------------------------------------------------
def closeup_purple(t,f):
    im=Image.new('RGB',(W,H),(6,4,14)); d=ImageDraw.Draw(im)
    cx,cy=74,26
    merged=t>=0.5
    if merged:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([cx-60,cy-40,cx+60,cy+40],fill=140)
        im.paste((120,40,200),(0,0),g.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(30 if merged else 12):                           # radial streaks pulled inward
        a=rr.random()*6.28; L0=rr.randint(20,90); L1=L0+rr.randint(6,16)
        c=(200,150,255) if merged else rr.choice([(120,180,255),(255,130,130)])
        d.line([cx+math.cos(a)*L0,cy+math.sin(a)*L0*0.6,cx+math.cos(a)*L1,cy+math.sin(a)*L1*0.6],fill=c)
    # Claude's arm from the bottom-left, index finger pointing at the knot of energy
    d.polygon([(0,64),(0,48),(52,36),(58,46),(20,64)],fill=(217,119,87),outline=(24,14,12))
    d.polygon([(0,64),(0,56),(40,44),(44,50),(18,64)],fill=(176,92,66))
    d.rounded_rectangle([48,34,62,46],radius=3,fill=(217,119,87),outline=(24,14,12))
    d.rectangle([60,35,70,38],fill=(217,119,87),outline=(24,14,12))   # the index finger
    if not merged:
        k=ease(t/0.5); a=k*math.pi*2.2; L=36*(1-k)+2
        bx,by=cx+math.cos(a)*L,cy+math.sin(a)*L*0.55; rx,ry=cx-math.cos(a)*L,cy-math.sin(a)*L*0.55
        for j in range(1,5):                                        # the spiral trails
            aa=a-j*0.22; LL=L+j*3
            d.point((int(cx+math.cos(aa)*LL),int(cy+math.sin(aa)*LL*0.55)),fill=(120,180,255))
            d.point((int(cx-math.cos(aa)*LL),int(cy-math.sin(aa)*LL*0.55)),fill=(255,130,130))
        _fx_orb(d,im,('jjk_orb',bx,by,5,BLUE),f); d=ImageDraw.Draw(im)
        _fx_orb(d,im,('jjk_orb',rx,ry,5,RED),f); d=ImageDraw.Draw(im)
        if t<0.3: say(im,"AO",44,(150,210,255),scale=2,cx=146,outline=(20,40,120)); say(im,"AKA",44,(255,140,140),scale=2,cx=170,outline=(120,20,30))
    else:
        r=int(8+8*ease((t-0.5)/0.2))
        _fx_orb(d,im,('jjk_orb',cx,cy,r,PURPLE),f); d=ImageDraw.Draw(im)
        for k in range(4):                                          # lightning crawling off it
            a=rr.random()*6.28; pts=[(cx+math.cos(a)*r,cy+math.sin(a)*r*0.8)]
            for _ in range(4): pts.append((pts[-1][0]+math.cos(a)*5+rr.randint(-3,3),pts[-1][1]+math.sin(a)*4+rr.randint(-3,3)))
            d.line(pts,fill=(240,210,255))
    if 0.5<=t<0.57:
        im=fade_to(im,(250,236,255),1-(t-0.5)/0.07); d=ImageDraw.Draw(im); zoom_lines(d,(220,170,255))
    if t>=0.6:
        jj=(f%3)-1 if t<0.68 else 0
        say(im,"HOLLOW",8,(236,220,255),scale=2,cx=146+jj,outline=(70,20,120))
        say(im,"PURPLE",26,(200,140,255),scale=3,cx=146+jj,outline=(70,20,120))
    if t<0.06: zoom_lines(d,(200,170,255))
    return im

# ---- the clip ------------------------------------------------------------------------------------
SLASHES=[(44+k*12+j*2,GROUND-4-j*7) for k in range(3) for j in range(3)]       # (fired at, height)
SCARS=[(44+k*12,x,y,L) for k in range(3) for (x,y,L) in
       [tuple(random.Random(k*10+i).randint(*r) for r in ((20,178),(6,40),(5,9))) for i in range(3)]]

def clip_infinity(f):
    s=scene(f,THEME); s['under'].append(('jjk_city',N_,False))
    eyes=160<=f<312
    G=GOJO_EYES if eyes else GOJO
    cl=actor(G[guard_pose(f)],CX,pal=EYEPAL if eyes else None); sk=actor(SUKUNA['idle'],EX,flip=True)
    extra=[]
    def pose(p): cl['spr']=G[p]
    # scars stay on the city until the purple flash wipes the slate
    for t0,x,y,L in SCARS:
        if t0<=f<298: s['under'].append(('jjk_scar',x,y,L))
    # 1) SHIBUYA, 10.31 — Sukuna laughs
    if 10<=f<44:
        y=4 if f>=14 else 4-(14-f)*3
        shout(s,"SHIBUYA",(255,255,255),y=y,scale=3,outline=(170,30,70))
        if f>=18: shout(s,"10.31",(255,210,90),y=24)
    if 26<=f<42: s['fx'].append(('dmg',"HA HA",EX-9,GROUND-28-(f//4)%2,(255,120,150)))
    # 2) Dismantle: the slashes stop dead on Infinity
    if 44<=f<84:
        if (f-44)%12<4: sk['spr']=SUKUNA['attack']
        if f<60: shout(s,"KAI!",(255,90,90),scale=2)
        for t0,y in SLASHES:
            if f<t0: continue
            x=138-10*(f-t0)
            if x>46: s['fx'].append(('slash',x,y,7,(235,230,255)))
            elif x>36: s['fx'].append(('spark',46,y,3)); s['fx'].append(('jjk_ripple',CX,GROUND-8,12,INF_C))
        s['fx'].append(('jjk_ripple',CX,GROUND-8,10+(f%4),(90,140,230)))
        if (f-44)%12 in (0,1): s['shake']=rshake()
    # 3) the lunge freezes an inch from Claude's face: MUGEN
    if 84<=f<90:
        t=(f-84)/6; sk.update(spr=SUKUNA['attack'],x=ez(EX,58,t),aura=(SUKUNA_AURA,1))
        extra+=[actor(SUKUNA['attack'],sk['x']+8,flip=True,alpha=0.35,tint=(255,140,150)),actor(SUKUNA['attack'],sk['x']+16,flip=True,alpha=0.2,tint=(255,140,150))]
    if 90<=f<104:
        sk.update(spr=SUKUNA['attack'],x=58+(1 if f%4<2 else 0),aura=(SUKUNA_AURA,1))
        for j in range(3): s['fx'].append(('jjk_ripple',46,GROUND-10,5+j*4+(f%3),INF_C if j%2 else (230,240,255)))
        say_x=W//2
        shout(s,"MUGEN",(160,215,255),y=4,scale=3,cx=say_x,outline=(20,50,130))
        if f>=94: s['fx'].append(('dmg',"?!",60,GROUND-30,(255,120,150)))
        if f==90: s['flash']=0.4; s['fc']=(46,GROUND-10); s['flashc']=(200,230,255)
    if 104<=f<116:                                                  # a flick of the finger
        pose('punch' if f<108 else 'guard')
        t=(f-104)/10; sk.update(spr=SUKUNA['hurt'],x=ez(58,EX,t),y=GROUND-int(6*math.sin(math.pi*min(1,t))))
        if f<108: s['fx'].append(('ring',48,GROUND-8,(f-104)*5+3,INF_C))
        if f>=110:
            for _ in range(2): s['fx'].append(('dust',sk['x']+random.randint(-4,6),GROUND-random.randint(0,3)))
    # 4) close-up: SIX EYES
    if 116<=f<160: s['image']=closeup_sixeyes((f-116)/44,f); return s
    # 5) Blue: Sukuna is dragged up into the orb
    if 160<=f<198:
        pose('charge'); cl['aura']=((120,190,255),1)
        t=(f-160)/38; ox,oy=112,GROUND-20; r=2+4*ease(t*2)
        s['fx'].append(('jjk_orb',ox,oy,r,BLUE))
        for i in range(12):
            a=i*2.4; ph=((f*0.06+i*0.13)%1); L=(1-ph)*44
            s['fx'].append(('mote',ox+math.cos(a)*L,oy+math.sin(a)*L*0.6,(150,210,255)))
        if f%2==0: s['fx'].append(('rock',ox+random.randint(-30,30),oy+random.randint(4,20)))
        if f>=170:
            k=(f-170)/14; sk.update(spr=SUKUNA['hurt'],x=ez(EX,ox+10,k),y=int(ez(GROUND,GROUND-10,k)))
        if f>=176: s['shake']=rshake() if f%2 else (0,0)
        if f<180: shout(s,"AO",(150,210,255),scale=3,outline=(20,50,130))
    # 6) Red: blown into the 109 tower
    if 198<=f<226:
        cl['aura']=((255,140,140),1)
        if f<206:
            pose('charge'); s['fx'].append(('jjk_orb',44,GROUND-6,1+(f-198)//2,RED))
            sk.update(spr=SUKUNA['hurt'],x=122,y=GROUND-10+(f-198))
        elif f<210:
            pose('punch'); x=lerp(44,114,(f-206)/4)
            s['fx'].append(('jjk_orb',x,GROUND-8,4,RED)); s['under'].append(('beam',44,int(x),GROUND-8,RED))
            sk.update(spr=SUKUNA['hurt'],x=122,y=GROUND-2)
        else:
            pose('punch' if f<214 else 'guard')
            t=(f-210)/8; sk.update(spr=SUKUNA['hurt'],x=ez(122,170,t),y=GROUND-int(10*math.sin(math.pi*min(1,t))))
            if f==210: s['flash']=0.9; s['fc']=(118,GROUND-10); s['flashc']=(255,130,120)
            if f<218: s['fx'].append(('spark',118,GROUND-10,9-(f-210))); s['fx'].append(('ring',118,GROUND-8,(f-210)*5+4,(255,110,100))); s['shake']=rshake(2)
            if f==218: s['shake']=rshake(2)
        shout(s,"AKA!",(255,130,130),scale=3,outline=(120,20,30))
    if 218<=f<298: s['under'].append(('jjk_crater',167,34))
    if 218<=f<232:
        sk.update(spr=SUKUNA['hurt'],x=170)
        if f<226:
            for _ in range(3): s['fx'].append(('dust',170+random.randint(-8,8),GROUND-random.randint(0,20)))
    # Sukuna laughs it off and walks back in
    if 232<=f<256:
        t=(f-232)/20; sk.update(spr=SUKUNA['idle'],x=ez(170,EX,t),aura=(SUKUNA_AURA,1+(f%2)))
        s['fx'].append(('dmg',"HA HA HA",min(sk['x']-14,W-34),GROUND-28-(f//3)%2,(255,120,150)))
    if 244<=f<256:
        pose('armsup'); cl['aura']=((200,150,255),1)
        s['fx'].append(('jjk_orb',CX-8,GROUND-18,2,BLUE)); s['fx'].append(('jjk_orb',CX+8,GROUND-18,2,RED))
    # 7) close-up: HOLLOW PURPLE
    if 256<=f<292: s['image']=closeup_purple((f-256)/36,f); return s
    # 8) it erases a strip of Shibuya, Sukuna with it
    if 292<=f<326:
        a=1 if f<306 else max(0,1-(f-306)/20)
        x=lerp(44,W+40,(f-292)/14)
        s['under'].append(('jjk_wake',44,min(x,W) if f<306 else W,GROUND-10,11,a))
    if 292<=f<306:
        pose('charge'); cl['aura']=((200,150,255),2)
        s['fx'].append(('jjk_orb',x,GROUND-10,12,PURPLE)); s['shake']=rshake(2)
        if x>=138: sk['vis']=False
        else: sk.update(spr=SUKUNA['hurt'],aura=(SUKUNA_AURA,1))
        if 296<=f<302: s['flash']=0.9; s['fc']=(150,GROUND-10); s['flashc']=(230,190,255)
    if 306<=f<316: sk['vis']=False
    # 9) Sukuna reforms from cursed motes; the blindfold goes back on
    if 312<=f<336:
        t=(f-312)/20
        if f<332: s['fx'].append(('jjk_motes',EX,GROUND-10,min(1,t)))
        sk.update(spr=SUKUNA['hurt'] if f<326 else SUKUNA['idle'],alpha=min(1,t*1.3))
    if 312<=f<316: s['fx'].append(('twinkle',CX+2,GROUND-12,2+(f%2)))
    s['actors']=extra+[cl,sk]
    return s

CLIPS = [clip('infinity', N_, clip_infinity)]
