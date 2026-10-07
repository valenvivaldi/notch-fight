"""Cyberpunk 2077: Claude is V (the Samurai jacket with the gold collar, a cyan optic implant) vs
Royce, the Maelstrom boss (red optics, the jaw mask, a powered exoskeleton with an arm cannon),
inside the Maelstrom plant in Watson: red neon, rain on the windows, Night City through a hole in
the wall. The scan tags him THREAT: EXTREME; a SHORT CIRCUIT quickhack fries his systems in a glitch;
the Sandevistan slows the world, V leaves colour trails and lands three mantis-blade cuts; the arm
cannon fires, V leaps it. Johnny Silverhand flickers in, close-up: WAKE UP, SAMURAI. WE HAVE A CITY TO
BURN. One shot of his Malorian: Royce goes down in sparks, FLATLINED. He gets back up on his spot."""
import zlib
from PIL import ImageChops
from engine import *

THEME = 'cyberpunk'
N_ = 280                                                           # frame 280 would be frame 0 again (rain, neon, breathing): it loops
CX, VX = 30, 150                                                   # the neutral pose: V, Royce
YEL = (252,238,10)                                                 # the HUD yellow
CYAN = (60,240,255)
NEON = (255,40,70)

# ---- Claude as V: dark hair with magenta tips, the Samurai jacket, a cyan implant under the eye --
def _v(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])
    kb=max(y for y in range(h) if 'K' in spr[y])
    jak=max(bot-3,kb+2)                                            # the jacket starts below the eyes
    for y in range(h):
        rgt=[x for x in range(w) if g[y][x]=='o' and x>r]; lft=[x for x in range(w) if g[y][x]=='o' and x<l]
        tips=({max(rgt)} if rgt else set())|({min(lft)} if lft else set())
        for x in range(w):
            c=g[y][x]; inside=l-1<=x<=r
            if c=='O' and x>r+1: g[y][x]='O'                        # a bare fist
            elif c=='O' and y==jak: g[y][x]='Y' if x in (l,r) else 'k'   # the gold collar
            elif c=='O' and y>jak: g[y][x]='r' if (y==jak+1 and x==(l+r)//2) else 'k'
            elif c=='o' and y>bot: g[y][x]='N'                       # trousers, boots
            elif c=='o' and y==bot and inside: g[y][x]='k'
            elif c=='o': g[y][x]='O' if x in tips and y<jak else 'k'   # sleeves, hands
    eye=[(x,y) for y in range(h-1) for x in range(w) if g[y][x]=='K' and g[y+1][x]=='O']
    if eye: x,y=eye[-1]; g[y+1][x]='c'                             # the optic implant, under one eye
    return overlay(ungrid(g),["..hhhhhm.",".hhhhhhhm","hhhhhhhhh"],-1,0,bangs="hhhh.....")
V=variant(_v)
VPAL={'k':(24,22,28),'Y':(240,190,40),'r':(220,30,40),'N':(36,38,66),'h':(40,26,46),'m':(240,60,170),
      'c':CYAN}

def _mantis(spr):
    """The punch pose with a mantis blade folding out of the forearm."""
    w=len(spr[0]); y=next(i for i,r in enumerate(spr) if r.rstrip('.').endswith('O') and len(r.rstrip('.'))==w)
    return paint(spr,[(w-3,y-1,'bm'),(w-1,y-2,'bm'),(w+1,y-3,'bm'),(w+3,y-4,'m')],grow=True)
V['mantis']=_mantis(V['punch'])
def _malorian(spr):
    w=len(spr[0]); y=next(i for i,r in enumerate(spr) if len(r.rstrip('.'))==w)
    return paint(spr,[(w,y-1,'GGGGq'),(w,y,'GGGGG'),(w+1,y+1,'G')],grow=True)
V['gun']=_malorian(V['charge'])
VPAL.update(b=(220,224,240),G=(64,66,76),q=(255,140,40))

# ---- Royce --------------------------------------------------------------------------------------
_ROY=S([
"........dddddd..........",
".......dDDDDDDd.........",
"......dDDDDDDDDd........",
"......dDrrDDrrDd........",
"......dDDDDDDDDd........",
"......dssRRRRssd........",
"......dRRdRRdRRd........",
".......dRRRRRRd.........",
".....kkkkkkkkkkkk.......",
"...DDDkkkkkkkkkkkDDD....",
"..DDDDDkkkrrkkkkDDDDD...",
"..DdDDkkkkkkkkkkkDDDDGGGG",
"..DdDDkkkDDDDkkkkDDDGGGGr",
"..Dd.DkkkkkkkkkkkD.DGGGG.",
"..Dd.DkkkkkkkkkkkD......",
"..DD.DDDDDDDDDDDDD......",
"..GG..kkkkkkkkkkk.......",
"......kkkkk.kkkkk.......",
"......DDDD...DDDD.......",
"......DrDD...DDrD.......",
"......kkkk...kkkk.......",
"......DDDD...DDDD.......",
"......DDDD...DDDD.......",
".....DDDDD...DDDDD......",
"....ddddddd..ddddddd....",])
ROY={'idle':_ROY,'idle2':S([r.replace('kkkrrkkkk','kkkRRkkkk') for r in _ROY]),'hurt':hurt(_ROY)}
ROY['down']=rotate90(ROY['hurt'],3,trim=True)
ROYPAL={'D':(118,122,136),'d':(58,60,72),'r':(255,40,50),'R':(140,22,30),'k':(28,26,32),
        'G':(82,84,96),'s':(196,164,146)}
MUZZLE=hand_at(_ROY,VX,GROUND,True,24,12)
def roy_idle(f): return ROY['idle'] if (f//6)%2==0 else ROY['idle2']

# ---- background: the Maelstrom plant -------------------------------------------------------------
_WINS=[(6,8,30),(38,8,62),(120,8,144),(152,8,178)]                 # (x0, y0, x1): 24 px of rain each
_HOLE=(76,4,108,30)
def _plant(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(16+10*k),int(10+4*k),int(18+6*k)))
    for x0,y0,x1 in _WINS:                                          # tall windows, the rain behind
        d.rectangle([x0-1,y0-1,x1+1,y0+25],fill=(36,30,40))
        d.rectangle([x0,y0,x1,y0+24],fill=(14,20,40))
        d.line([(x0+x1)//2,y0,(x0+x1)//2,y0+24],fill=(36,30,40))
    x0,y0,x1,y1=_HOLE                                               # the blown-out wall: Night City
    d.polygon([(x0,y1),(x0+3,y0+4),(x0+10,y0),(x1-6,y0+2),(x1,y0+8),(x1-2,y1)],fill=(30,12,46))
    rr=random.Random(zlib.crc32(b'night-city'))
    for x in range(x0+4,x1-3,4):
        hh=rr.randint(8,22); d.rectangle([x,y1-hh,x+3,y1],fill=(18,8,30))
        for wy in range(y1-hh+2,y1-1,3):
            if rr.random()<0.5: d.point((x+1+rr.randint(0,1),wy),fill=rr.choice([(255,60,200),(60,220,255),(255,200,80)]))
    d.rectangle([0,34,W,35],fill=(52,40,48))                        # the catwalk
    for x in range(0,W,8): d.line([x,35,x,40],fill=(40,30,38))
    d.line([0,40,W,40],fill=(52,40,48))
    for x in (2,70,114,182): d.rectangle([x,34,x+2,GROUND],fill=(44,34,42))   # pillars
    d.rectangle([128,44,146,GROUND-1],fill=(50,28,30),outline=(80,40,40))       # crates
    d.rectangle([20,46,36,GROUND-1],fill=(50,28,30),outline=(80,40,40))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(40,24,30))
register_bg(THEME, lambda v: (v+16,v//3+4,v//2+8), decor=_plant)

# ---- effects -----------------------------------------------------------------------------------
@fx('cp_world')
def _fx_world(d,im,e,f):
    """Rain in the windows (an 8-frame cycle) and the flickering MAELSTROM neon (40 frames)."""
    rr=random.Random(zlib.crc32(b'cp-rain'))
    for x0,y0,x1 in _WINS:
        for _ in range(7):
            x=rr.randint(x0,x1); b=rr.randint(0,23); y=y0+(b+(f%8)*3)%24
            d.line([x,y,x,min(y0+24,y+2)],fill=(90,110,160))
    on=(f%40) not in (3,5,22)
    c=NEON if on else (90,20,30)
    text(d,'MAELSTROM',W//2-18,44,c,shadow=None)
    if on: d.line([W//2-20,50,W//2+18,50],fill=(150,20,40))

@fx('cp_scan')
def _fx_scan(d,im,e,f):
    """The scanner: brackets close in on Royce, a sweep line, then the info panel."""
    _,t=e; x0,y0,x1,y1=VX-16,GROUND-30,VX+16,GROUND+1
    k=int(10*(1-ease(t/0.4)))
    for (x,y,sx,sy) in ((x0-k,y0-k,1,1),(x1+k,y0-k,-1,1),(x0-k,y1+k,1,-1),(x1+k,y1+k,-1,-1)):
        d.line([x,y,x+4*sx,y],fill=YEL); d.line([x,y,x,y+4*sy],fill=YEL)
    if t<0.6:
        sy=int(lerp(y0,y1,(t*3)%1)); d.line([x0,sy,x1,sy],fill=(255,250,120))
    if t>=0.45:
        n=min(3,int((t-0.45)/0.12)+1)
        d.rectangle([80,7,138,30],fill=(20,14,10),outline=YEL)
        for i,(txt,c) in enumerate((('ROYCE',YEL),('MAELSTROM',(255,190,120)),('THREAT:EXTREME',NEON))[:n]):
            text(d,txt,82,[9,16,23][i],c,shadow=None)

@fx('cp_hack')
def _fx_hack(d,im,e,f):
    """The quickhack upload over V: name and a cyan bar."""
    _,t=e
    d.rectangle([8,8,66,22],fill=(8,18,24),outline=CYAN)
    text(d,'SHORT CIRCUIT',10,10,CYAN,shadow=None)
    d.rectangle([10,17,64,19],outline=(30,90,110)); d.rectangle([10,17,10+int(54*min(1,t)),19],fill=CYAN)

@fx('cp_zap')
def _fx_zap(d,im,e,f):
    """Electric arcs crawling over a body: x, feet, height."""
    _,x,feet,hgt=e; rr=random.Random(f%16*31+7)
    for _ in range(3):
        px,py=x+rr.randint(-10,10),feet-rr.randint(2,hgt)
        pts=[(px,py)]
        for _ in range(4): px+=rr.randint(-4,4); py+=rr.randint(-4,4); pts.append((px,py))
        d.line(pts,fill=CYAN); d.point(pts[0],fill=(255,255,255))

@fx('cp_glitch')
def _fx_glitch(d,im,e,f):
    """Shifted bands and a split red channel (strength a)."""
    _,a=e; rr=random.Random(f*13+5); src=im.copy()
    for _ in range(int(3+a*4)):
        y=rr.randint(0,H-6); hh=rr.randint(2,6); dx=rr.randint(-6,6)*a
        im.paste(src.crop((0,y,W,y+hh)),(int(dx),y))
    r,g,b=im.split(); r=ImageChops.offset(r,int(2*a)+1,0); im.paste(Image.merge('RGB',(r,g,b)))

@fx('cp_tint')
def _fx_tint(d,im,e,f):
    _,c,a=e; im.paste(fade_to(im,c,a))

@fx('cp_after')
def _fx_after(d,im,e,f):
    """A Sandevistan afterimage."""
    _,spr,x,y,flip,c,a=e; draw(im,spr,x,y,flip,alpha=a,tint=c,f=f,pal=VPAL)

@fx('cp_slash')
def _fx_slash(d,im,e,f):
    """A mantis-blade cut across the body, t frames old."""
    _,x,y,k,t=e
    if t>=6: return
    L=10; dx=[-1,1,-1][k%3]
    c=(255,255,255) if t<2 else (255,80,180)
    d.line([x-L*dx,y-L//2,x+L*dx,y+L//2],fill=c,width=2 if t<3 else 1)

@fx('cp_charge')
def _fx_charge(d,im,e,f):
    _,x,y,t=e; r=int(1+t*4)+(f%2)
    d.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],outline=(255,120,40)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,200,90))

@fx('cp_tracer')
def _fx_tracer(d,im,e,f):
    _,x0,x1,y=e; d.line([x0,y,x1,y],fill=(255,170,60),width=3); d.line([x0,y,x1,y],fill=(255,255,220))

@fx('cp_flat')
def _fx_flat(d,im,e,f):
    """The FLATLINED card: red box, big letters, a little jitter."""
    _,t=e; jx=((f//2)%3-1) if t<0.2 else 0
    d.rectangle([42+jx,14,143+jx,34],fill=(20,4,8),outline=NEON); d.line([42+jx,16,143+jx,16],fill=(120,20,30))
    big_text(im,'FLATLINED.',18,NEON,scale=2,cx=W//2+jx,outline=(60,0,10))

@fx('cp_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('cp_say',txt,y,c,scale,outline))

# ---- close-up: Johnny Silverhand ------------------------------------------------------------------
_JOHNNY=S([
"......hhhhhhhhh.......",
"....hhhhhhhhhhhhh.....",
"...hhhhhhhhhhhhhhh....",
"...hhhhhhhhhhhhhhhh...",
"...hhsssshhhhhssshh...",
"...hssssssssssssssh...",
"...hssssssssssssssh...",
"...YYYYYYYsYYYYYYYY...",
"...YLLLLLYsYLLLLLLY...",
"...YLlLLLYsYLlLLLLY...",
"....YLLLYsssYLLLLY....",
"....sYYYsssssYYYYs....",
"....ssssssssssssss....",
"....sssssssKssssss....",
"....ssssssssssssss....",
"....sbbbbssssbbbbs....",
".....bbbKKKKKbbbb.....",
".....bbbbbbbbbbbb.....",
"......bbbbbbbbbb......",
".......bbbbbbbb.......",
"........ssssss........",
"........ssssss........",
"...kkkkkkkkkkkkkAAA...",
"..kkkkkkkkkkkkkAaAAA..",
".kkkkkkkkkkkkkkAAaAAA.",
"kkkkkkkkkkkkkkAAAAaAAA",
"kkkkkkkkkkkkkkAaAAAaAA",
"kkkkkkkkkkkkkkAAaAAAaA",])
JPAL={'h':(24,20,26),'s':(214,170,140),'Y':(220,180,60),'L':(60,20,30),'l':(160,60,70),'K':(70,40,36),
      'b':(110,80,70),'k':(22,22,26),'A':(196,200,212),'a':(120,124,140)}
_JIMG=sprite_img(_JOHNNY,JPAL,scale=2)

def closeup_johnny(t,f):
    """Johnny flickers in like a broken hologram, aviators and the silver arm: WAKE UP, SAMURAI."""
    im=Image.new('RGB',(W,H),(18,10,24)); d=ImageDraw.Draw(im)
    for x in range(0,W,6): d.line([x,0,x-30,H],fill=(30,16,40))
    d.rectangle([0,H-6,W,H],fill=(60,10,30))
    paste_feet(im,_JIMG,44,H+2)
    for y in range(0,H,2):
        if (y//2+f)%7==0: d.line([0,y,96,y],fill=(18,10,24))                  # hologram scanlines
    if t<0.12 or 0.5<t<0.53: _fx_glitch(d,im,('',1.0),f); d=ImageDraw.Draw(im)
    if t>=0.15:
        text(d,'JOHNNY SILVERHAND',96,8,CYAN,shadow=None)
        d.line([96,14,162,14],fill=(40,120,140))
    if t>=0.25: big_text(im,'WAKE UP,',20,(255,255,255),cx=136,outline=(140,20,60))
    if t>=0.38: big_text(im,'SAMURAI.',34,(255,255,255),cx=136,outline=(140,20,60))
    if t>=0.62: text(d,'WE HAVE A CITY TO BURN.',90,52,YEL)
    if t<0.06: zoom_lines(d,NEON)
    return im

# ---- the clip ----------------------------------------------------------------------------------
SX=VX-16                                                           # where V lands the cuts
def v_sande(f):
    """V's x during the Sandevistan (86-122): three cuts at 94, 102, 110."""
    if f<92: return ez(CX,SX,(f-86)/6)
    if f<112: return SX+[0,-4,2][min(2,(f-92)//8)]
    return ez(SX,62,(f-112)/8)

def clip_nightcity(f):
    s=scene(f,THEME); s['under'].append(('cp_world',))
    v=actor(V[guard_pose(f)],CX,pal=VPAL)
    roy=actor(roy_idle(f),VX,flip=True,pal=ROYPAL)
    vx=CX
    # 1) the scan
    if 10<=f<40:
        s['fx'].append(('cp_scan',(f-10)/30))
        v['pal']=dict(VPAL,K=CYAN)
    # 2) the quickhack: SHORT CIRCUIT
    if 40<=f<58: s['fx'].append(('cp_hack',(f-40)/14)); v['spr']=V['armsup']
    if 56<=f<70:
        roy['spr']=ROY['hurt']; roy['x']=VX+((f//2)%2)
        s['fx'].append(('cp_zap',VX,GROUND,24))
        if f<60: s['fx'].append(('cp_glitch',0.8))
        s['fx'].append(('dmg',str(120+(f-56)*9),VX-8,GROUND-34-(f-56)//3,CYAN))
    if 70<=f<86: shout(s,"YOU'RE DEAD, CHOOM!",NEON)
    # 3) the Sandevistan: the world slows, three cuts
    if 80<=f<86:
        banner(s,"SANDEVISTAN",20,(120,255,170),2,(10,80,40)); v['spr']=V['charge']
        s['fx'].append(('cp_tint',(40,255,140),0.2-(f-80)*0.02))
    if 86<=f<122:
        vx=v_sande(f)
        pose='mantis' if f>=92 and (f-92)%8<4 and f<112 else ('dash' if f<92 or f>=112 else 'guard')
        v.update(spr=V[pose],x=vx,flip=f>=112)
        for k,c in enumerate(((60,255,150),(60,200,255),(255,60,200))):
            g=f-2*(k+1)
            if g>=86: s['under'].append(('cp_after',V['dash'] if g<92 or g>=112 else V['mantis'],v_sande(g),GROUND,g>=112,c,0.45-k*0.12))
        s['fx'].append(('cp_tint',(30,255,130),0.12))
        roy.update(spr=ROY['hurt'],x=VX+(f-86)//6)
        for k,f0 in enumerate((94,102,110)):
            if f0<=f<f0+6: s['fx'].append(('cp_slash',VX-2+(f-86)//6,GROUND-14+k*3,k,f-f0))
            if f==f0: s['fx'].append(('spark',VX-4,GROUND-14+k*3,4))
    if 122<=f<128: s['flash']=0.3-(f-122)*0.05; s['fc']=(VX,GROUND-14); s['flashc']=(200,255,220)
    if 122<=f<134:
        roy.update(spr=ROY['hurt'],x=VX+6); s['shake']=rshake() if f<126 else (0,0)
        s['fx'].append(('dmg','3X CRIT!',VX-14,GROUND-36,(255,120,200)))
    if 122<=f<196: vx=62; v.update(x=62,flip=False)
    # 4) the arm cannon; V leaps it
    if 134<=f<150: roy['x']=ez(VX+6,VX,(f-134)/6)
    if 136<=f<148: s['fx'].append(('cp_charge',MUZZLE[0],MUZZLE[1],(f-136)/12))
    if 146<=f<160:
        t=(f-146)/14; v.update(spr=V['armsup'],y=GROUND-int(20*math.sin(math.pi*t)))
    if 148<=f<158:
        bx=lerp(MUZZLE[0],-4,(f-148)/9)
        s['fx'].append(('orbc',bx,MUZZLE[1],3,((200,60,20),(255,170,60))))
        for j in range(3): s['fx'].append(('mote',bx+4+j*3,MUZZLE[1]+random.randint(-1,1),(255,120,40)))
    if f==148: s['shake']=rshake(2); s['fx'].append(('spark',MUZZLE[0],MUZZLE[1],5))
    if 157<=f<163: s['fx'].append(('boom',4,MUZZLE[1],2+(f-157))); s['shake']=rshake(2)
    # 5) Johnny
    if 162<=f<198: s['image']=closeup_johnny((f-162)/36,f); return s
    # 6) the Malorian
    if 198<=f<212: v['spr']=V['gun']
    if 198<=f<210: shout(s,"MALORIAN ARMS 3516",(255,170,60))
    if f==210:
        s['flash']=0.6; s['fc']=(80,GROUND-8); s['flashc']=(255,220,160); s['shake']=rshake(3)
    if 210<=f<213:
        gy=GROUND-len(V['gun'])+next(i for i,r in enumerate(V['gun']) if 'q' in r)
        s['fx'].append(('cp_tracer',62+12,VX-6,gy)); s['fx'].append(('spark',62+13,gy,5))
        v['spr']=V['gun']
    if 210<=f<222:
        if f<216: banner(s,"BANG!",4,(255,200,90),3,(150,40,10))
        roy.update(spr=ROY['hurt'],x=ez(VX,VX+8,(f-210)/6))
        s['fx'].append(('cp_zap',VX+6,GROUND,26)); s['fx'].append(('spark',VX+4,GROUND-14-(f%3)*3,3))
    if 212<=f<220: v['spr']=V['gun']
    if 222<=f<250:
        roy.update(spr=ROY['down'],x=VX+8)
        if f<232 and f%3==0: s['fx'].append(('spark',VX+2+(f%7),GROUND-4,2))
        if f==222: s['fx'].append(('dust',VX,GROUND-1)); s['fx'].append(('dust',VX+14,GROUND-1)); s['shake']=rshake(2)
        if f>=226: s['fx'].append(('cp_flat',(f-226)/24))
    if 250<=f<258: roy.update(spr=ROY['hurt'],x=VX+8)
    if 258<=f<272: roy.update(x=ez(VX+8,VX,(f-258)/10))
    # 7) V walks back
    if 196<=f<244: v['x']=62
    if 244<=f<272: v.update(x=ez(62,CX,(f-244)/22),flip=f<266)
    s['actors']=[roy,v]
    return s

CLIPS = [clip('nightcity', N_, clip_nightcity)]
