"""Jujutsu Kaisen sub-theme "jjk-sukuna": the Domain Expansion battle in the ruins of Shibuya under a
red moon. Sukuna forms his hand sign — close-up: the four eyes open over that grin, RYOIKI TENKAI —
and Malevolent Shrine rises out of the rubble; Dismantle and Cleave shred the street, Infinity holds.
Claude (Gojo) answers — close-up: the blindfold tips up over one Six Eye, the crossed fingers,
MURYOKUSHO — and Unlimited Void swallows the shrine. Frozen by infinite information, Sukuna eats
four Black Flashes, both domains shatter, and he picks himself up laughing."""
from engine import *
from themes.jjk import GOJO, SUKUNA, city, say, shout, _eye, SUKUNA_AURA, INF_C   # same franchise

THEME = 'jjk-sukuna'
N_ = 312
CX, EX = 30, 150

register_bg(THEME, lambda v: (v+30,v//3+6,v//3+6), decor=lambda d: city(d,ruined=True))

# Sukuna's hand sign: both hands pressed together in front of the chest
_SK=list(SUKUNA['idle'])
_SK[11]="..WWWWsWWWWW...."; _SK[12]="..WWWssWWWWW...."
SUKUNA_SIGN=S(_SK)

def _shrine():
    """Malevolent Shrine: two-tier roof, fanged mouth between the pillars, a pile of skulls."""
    w,h=44,36; im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.polygon([(3,1),(8,3),(36,3),(41,1),(38,9),(6,9)],fill=(120,16,24)); d.line([(6,9),(38,9)],fill=(190,40,40))
    d.polygon([(0,10),(5,12),(39,12),(44,10),(41,17),(3,17)],fill=(140,20,30)); d.line([(3,17),(41,17)],fill=(200,50,44))
    for x in (7,15,28,36): d.rectangle([x,17,x+1,30],fill=(64,18,20))
    d.rectangle([17,18,27,29],fill=(40,0,4))
    for x in range(17,28,2): d.polygon([(x,18),(x+2,18),(x+1,21)],fill=(236,226,206)); d.polygon([(x,29),(x+2,29),(x+1,26)],fill=(236,226,206))
    for i,x in enumerate(range(2,43,5)):
        y=31+(i%2); d.ellipse([x,y,x+4,y+4],fill=(222,212,190)); d.point((x+1,y+2),fill=(30,20,20)); d.point((x+3,y+2),fill=(30,20,20))
    for x in (8,22,36): d.line([(x,1),(x,-1)],fill=(190,40,40)); d.point((x,0),fill=(220,60,50))
    return im
SHRINE=_shrine()

@fx('shrine')
def _fx_shrine(d,im,e,f):
    """Rises out of the ground: only the part above GROUND is shown."""
    _,x,rise=e; w,h=SHRINE.size; top=int(GROUND+1-h*rise); vis=GROUND+1-top
    if vis>0: im.paste(SHRINE.crop((0,0,w,vis)),(int(x)-w//2,top),SHRINE.crop((0,0,w,vis)))

@fx('redsky')
def _fx_redsky(d,im,e,f):
    _,a=e; im.paste(fade_to(im,(70,0,10),a))

_STARS=[(random.Random(i).randint(0,W-1),random.Random(i*7+1).randint(0,H-1),random.Random(i*3+2).random()) for i in range(90)]
@fx('void')
def _fx_void(d,im,e,f):
    """Unlimited Void: a starfield with a slow galaxy swirl, inside an ellipse of radius r."""
    _,cx,cy,r=e
    v=Image.new('RGB',(W,H),(2,2,10)); vd=ImageDraw.Draw(v)
    for k in range(3):
        rr=16+k*14; a0=(f*360/52+k*120)%360                         # a 52-frame turn: it loops
        vd.arc([W//2-rr*2,H//2-rr,W//2+rr*2,H//2+rr],a0,a0+140,fill=(60,40,140) if k%2 else (40,80,170))
    for i,(x,y,p) in enumerate(_STARS):
        c=(255,255,255) if (i+f//4)%6 else (150,190,255)
        vd.point((x,y),fill=c)
        if p>0.9 and (f+i)%8<4: vd.point((x+1,y),fill=(180,200,255)); vd.point((x-1,y),fill=(180,200,255))
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r*0.7,cx+r,cy+r*0.7],fill=255)
    im.paste(v,(0,0),m)
    if r<200: ImageDraw.Draw(im).ellipse([cx-r,cy-r*0.7,cx+r,cy+r*0.7],outline=(170,210,255))

@fx('blackflash')
def _fx_blackflash(d,im,e,f):
    """Black Flash: black lightning with a red rim, radiating from the point of impact."""
    _,x,y,sz=e; rr=random.Random(f)
    for k in range(6):
        a=k*1.05+rr.random()*0.5; pts=[(x,y)]; px,py=x,y
        for j in range(3): px+=math.cos(a)*sz/3+rr.randint(-2,2); py+=math.sin(a)*sz/5+rr.randint(-2,2); pts.append((px,py))
        d.line(pts,fill=(230,30,40),width=3); d.line(pts,fill=(0,0,0),width=1)
    d.ellipse([x-3,y-3,x+3,y+3],fill=(0,0,0),outline=(255,60,60))

@fx('jjk_rend')
def _fx_rend(d,im,e,f):
    """Cleave: one huge cut across the whole frame, white core with a red edge."""
    _,x,y,a=e; dx,dy=math.cos(a)*200,math.sin(a)*200
    d.line([x-dx,y-dy,x+dx,y+dy],fill=(200,20,30),width=3); d.line([x-dx,y-dy,x+dx,y+dy],fill=(255,255,255))

@fx('jjk_cracks')
def _fx_cracks(d,im,e,f):
    """The shrine splitting apart as the Void takes over (t 0..1)."""
    _,x,t=e; rr=random.Random(66)
    for k in range(int(8*t)+1):
        x0=x+rr.randint(-18,18); y0=GROUND-rr.randint(4,30); pts=[(x0,y0)]
        for _ in range(3): pts.append((pts[-1][0]+rr.randint(-4,4),pts[-1][1]+rr.randint(2,5)))
        d.line(pts,fill=(255,200,190))

@fx('jjk_info')
def _fx_info(d,im,e,f):
    """Infinite information pouring into Sukuna's head: digits and glyph strokes rushing in."""
    _,x,y=e; rr=random.Random(f*3)
    for j in range(7):
        ang=rr.random()*6.28; L=(1-((f+j*5)%10)/10)*34
        px,py=x+math.cos(ang)*L,y+math.sin(ang)*L*0.6
        if j%2: text(d,str(rr.randint(0,9)),int(px),int(py),(170,210,255))
        else: d.line([px,py,px+math.cos(ang)*3,py+math.sin(ang)*2],fill=(230,240,255))

# ---- close-up 1: Sukuna's grin -------------------------------------------------------------------
def closeup_grin(t,f):
    """Primer plano: the second pair of eyes opens, the grin splits wide, the hand sign rises."""
    im=Image.new('RGB',(W,H),(40,0,6)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([0,-10,130,80],fill=150)
    im.paste((150,10,24),(0,0),g.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(im)
    rr=random.Random(f//2)
    for _ in range(3 if t>0.4 else 1):                              # slashes flickering through the dark
        x=rr.randint(0,W); y=rr.randint(0,H); a=rr.uniform(-0.8,0.8)
        d.line([x-40*math.cos(a),y-40*math.sin(a),x+40*math.cos(a),y+40*math.sin(a)],fill=(255,200,200))
    jx=((f%3)-1) if t>0.72 else 0
    for i in range(9):                                              # pink hair, swept back
        x0=34+i*7+jx; tip=(x0-6+(i%2)*3,2+(i*3)%7)
        d.polygon([(x0,26),(x0+10,26),tip],fill=(240,120,170),outline=(180,70,120))
    d.rectangle([34+jx,18,96+jx,27],fill=(240,120,170))
    d.rectangle([36+jx,26,94+jx,64],fill=(240,200,160)); d.rectangle([36+jx,26,40+jx,64],fill=(200,160,124))
    for ex in (52,76):                                              # the main eyes: narrow, red, slit pupils
        d.polygon([(ex-8+jx,35),(ex+7+jx,31),(ex+8+jx,40),(ex-7+jx,41)],fill=(24,14,12))
        d.polygon([(ex-6+jx,35),(ex+6+jx,32),(ex+6+jx,39),(ex-6+jx,40)],fill=(220,40,40))
        d.line([ex+jx,32,ex+jx,39],fill=(24,14,12)); d.point((ex-3+jx,35),fill=(255,200,200))
        d.line([ex-9+jx,31,ex+8+jx,28],fill=(24,14,12))             # brows
    lo=ease((t-0.15)/0.2)                                           # the second pair opens under them
    for ex in (52,76):
        if lo>0: d.line([ex-3+jx,44,ex+3+jx,44-int(2*lo)],fill=(24,14,12)); d.line([ex-2+jx,45,ex+2+jx,45-int(lo)],fill=(220,40,40) if lo>0.5 else (24,14,12))
    for y in (47,50):                                               # the cheek tattoos
        d.line([36+jx,y,44+jx,y],fill=(24,14,12)); d.line([86+jx,y,94+jx,y],fill=(24,14,12))
    d.line([56+jx,27,74+jx,27],fill=(24,14,12))
    wide=ease((t-0.25)/0.25)                                        # the grin
    mw=int(8+16*wide); my=57; mh=int(2+4*wide)
    d.chord([64-mw+jx,my-mh,64+mw+jx,my+mh],0,180,fill=(60,0,8),outline=(24,14,12))
    d.line([64-mw+jx,my,64+mw+jx,my],fill=(24,14,12))
    for x in range(64-mw+2,64+mw-1,3):
        d.polygon([(x+jx,my),(x+2+jx,my),(x+1+jx,my+2)],fill=(246,240,228))
        if wide>0.4: d.polygon([(x+1+jx,my+mh),(x+3+jx,my+mh),(x+2+jx,my+mh-2)],fill=(246,240,228))
    if t>=0.3:                                                      # the hand sign rises into frame
        hy=int(lerp(64,34,(t-0.3)/0.15))
        for dx0 in (0,12):
            d.rounded_rectangle([98+dx0,hy+8,110+dx0,hy+30],radius=3,fill=(240,200,160),outline=(24,14,12))
        d.polygon([(104,hy+10),(110,hy),(116,hy+10)],fill=(240,200,160),outline=(24,14,12))
        if hy+24<H: d.rectangle([98,hy+24,122,H],fill=(236,236,242)); d.line([110,hy+24,110,H],fill=(170,170,190))
    if 0.45<=t<0.5:
        im=fade_to(im,(255,220,220),1-(t-0.45)/0.05); d=ImageDraw.Draw(im); zoom_lines(d,(255,80,80))
    if t>=0.48:
        j=(f%3)-1 if t<0.56 else 0
        say(im,"RYOIKI",8,(255,90,90),scale=2,cx=156+j,outline=(40,0,0))
        say(im,"TENKAI",28,(255,230,220),scale=2,cx=156+j,outline=(120,0,10))
    if t<0.06: zoom_lines(d,(255,120,120))
    if t>0.9: im=fade_to(im,(90,0,14),(t-0.9)/0.1*0.8)
    return im

# ---- close-up 2: the Void's hand sign ------------------------------------------------------------
def closeup_voidsign(t,f):
    """Primer plano: a finger tips the blindfold up over one Six Eye, then the crossed fingers."""
    im=Image.new('RGB',(W,H),(6,8,24)); d=ImageDraw.Draw(im)
    lift=ease((t-0.1)/0.2)
    if lift>0:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([20,10,110,70],fill=int(100*lift))
        im.paste((60,140,255),(0,0),g.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    for i in range(10):                                             # standing white hair
        x0=18+i*7; tip=(x0+4+(i%3-1)*3,2+(4 if i%2 else 0)+(i*37%5))
        d.polygon([(x0,26),(x0+9,26),tip],fill=(242,242,250),outline=(186,186,206))
    d.rectangle([18,22,88,28],fill=(242,242,250))
    d.rectangle([22,28,84,64],fill=(217,119,87)); d.rectangle([22,28,27,64],fill=(176,92,66))
    if lift>0.4: _eye(d,im,42,46,f)
    else: d.rounded_rectangle([40,42,44,50],radius=1,fill=(24,14,12))
    up=int(12*lift)                                                 # the blindfold, left end tipped up
    d.polygon([(20,34-up),(52,34-up),(60,34),(86,34),(86,45),(60,45),(52,45-up),(20,45-up)],fill=(26,26,34))
    d.line([60,44,86,44],fill=(60,60,76))
    if 0.08<=t<0.34:                                                # the finger doing it
        d.rectangle([48,45-up,53,64],fill=(217,119,87),outline=(24,14,12))
    if t>=0.34:                                                     # index up, middle crossed over it
        k=ease((t-0.34)/0.12); oy=int(30*(1-k))
        d.rounded_rectangle([106,38+oy,136,70+oy],radius=5,fill=(217,119,87),outline=(24,14,12))
        d.rectangle([112,10+oy,119,42+oy],fill=(217,119,87),outline=(24,14,12))
        d.polygon([(126,40+oy),(133,40+oy),(117,14+oy),(110,17+oy)],fill=(236,140,106),outline=(24,14,12))
        d.line([108,50+oy,134,50+oy],fill=(168,80,54)); d.line([108,58+oy,134,58+oy],fill=(168,80,54))
    if t>=0.5:
        j=(f%3)-1 if t<0.58 else 0
        say(im,"RYOIKI TENKAI",4,(150,210,255),scale=1,cx=160+j)
        say(im,"MURYO",14,(230,246,255),scale=2,cx=162+j,outline=(20,40,120))
        say(im,"KUSHO",30,(150,210,255),scale=2,cx=162+j,outline=(20,40,120))
    if t>0.74:                                                      # the void swallows the frame from the eye
        _fx_void(d,im,('void',42,46,int((t-0.74)/0.26*230)),f)
    if t<0.06: zoom_lines(d,(150,210,255))
    return im

# ---- the clip ------------------------------------------------------------------------------------
SCARS=[tuple(random.Random(40+i).randint(*r) for r in ((84,126),(4,180),(6,40),(5,10))) for i in range(12)]

def clip_domain(f):
    s=scene(f,THEME); s['under'].append(('jjk_city',N_,True))
    cl=actor(GOJO[guard_pose(f)],CX); sk=actor(SUKUNA['idle'],EX,flip=True)
    def pose(p): cl['spr']=GOJO[p]
    for t0,x,y,L in SCARS:
        if t0<=f<234: s['under'].append(('jjk_scar',x,y,L))
    # 1) the hand sign
    if 12<=f<24:
        sk.update(spr=SUKUNA_SIGN,aura=(SUKUNA_AURA,1+(f%2)))
        shout(s,"RYOIKI TENKAI",(255,90,90),scale=2,outline=(40,0,0))
        if f%3==0: s['shake']=rshake()
    # 2) close-up: the grin
    if 24<=f<60: s['image']=closeup_grin((f-24)/36,f); return s
    # 3) Malevolent Shrine rises
    domain=60<=f<236
    if 60<=f<248: s['under'].append(('redsky',min(0.55,(f-60)/12*0.55) if f<236 else 0.55*(248-f)/12))
    if domain and f<228: s['under'].append(('shrine',166,min(1,(f-60)/16)))
    if 60<=f<84:
        sk.update(spr=SUKUNA_SIGN,aura=(SUKUNA_AURA,1))
        shout(s,"FUKUMA MIZUSHI",(255,120,110),y=3,scale=2,outline=(60,0,0))
        if f%3==0: s['shake']=rshake(2 if f<76 else 1)
        if f<76:
            for _ in range(3): s['fx'].append(('rock',166+random.randint(-22,22),GROUND-random.randint(0,6)))
    # 4) Dismantle and Cleave shred everything; Infinity holds
    if 84<=f<128:
        if (f-84)%8<3: sk['spr']=SUKUNA['attack']
        rr=random.Random(f)
        for j in range(5):
            x=rr.randint(20,W-10); y=rr.randint(12,GROUND-2)
            if abs(x-38)<14 and y>GROUND-26: s['fx'].append(('spark',46,y,2))
            else: s['fx'].append(('slash',x,y,6,(255,210,210)))
        if (f-84)%12<2:                                             # a Cleave across the whole frame
            s['fx'].append(('jjk_rend',random.randint(40,150),random.randint(12,40),random.uniform(-0.5,0.5)))
            s['shake']=rshake(2)
        for r in range(3): s['fx'].append(('jjk_ripple',CX,GROUND-8,9+r*4+(f%3),INF_C if r%2 else (230,240,255)))
        shout(s,"KAI!" if f<106 else "HACHI!",(255,110,110),scale=2,outline=(60,0,0))
    # 5) Claude answers
    if 128<=f<140:
        pose('armsup'); cl['aura']=((150,200,255),1+(f%2))
        shout(s,"RYOIKI TENKAI",(150,210,255),scale=2,outline=(20,40,120))
    if 140<=f<180: s['image']=closeup_voidsign((f-140)/40,f); return s
    # 6) Unlimited Void eats the shrine; infinite information freezes Sukuna
    if 180<=f<196: s['under'].append(('jjk_cracks',166,min(1,(f-180)/12)))
    if 180<=f<236: s['under'].append(('void',30,GROUND-10,min(260,60+(f-180)*10)))
    if 180<=f<236:
        sk.update(spr=SUKUNA['hurt'],x=150+(1 if f%4<2 else 0))
        s['fx'].append(('jjk_info',EX,GROUND-18))
    if 180<=f<196: shout(s,"MURYOKUSHO",(170,215,255),scale=2,outline=(20,40,120))
    # 7) four Black Flashes
    if 196<=f<204:
        pose('dash'); t=(f-196)/8; cl['x']=lerp(CX,132,t)
        s['fx'].append(('jjk_ripple',cl['x']-8,GROUND-8,6,(230,240,255)))
    if 204<=f<232:
        k=(f-204)//7; ph=(f-204)%7; px=150+k*6
        pose('punch' if ph<4 else 'guard'); cl['x']=px-18
        sk.update(x=px+(2 if ph<3 else 0))
        if ph<3:
            s['fx'].append(('blackflash',px-6,GROUND-8,16+ph*4))
            if ph==0: s['under'].append(('dim',0.55))
        if ph==0: s['flash']=0.8; s['fc']=(px-6,GROUND-8); s['flashc']=(255,40,50); s['shake']=rshake(2)
        shout(s,"KOKUSEN!",(255,255,255) if ph<3 else (255,70,70),scale=3 if ph<3 else 2,outline=(200,20,30) if ph<3 else (40,0,0))
    # 8) both domains shatter
    if 232<=f<254:
        t=(f-232)/22; rr=random.Random(5)
        for j in range(44):
            a=rr.random()*6.28; sp=rr.uniform(20,110)
            x=90+math.cos(a)*sp*(0.3+t); y=GROUND-16+math.sin(a)*sp*0.5*(0.3+t)+20*t*t
            s['fx'].append(('shard',x,y,(200,220,255) if j%3 else (255,120,120)))
        if f==234: s['flash']=0.9; s['fc']=(90,GROUND-16); s['flashc']=(220,235,255)
        if f<240: s['shake']=rshake(2)
    if 232<=f<258: pose('guard'); cl['x']=ez(168,CX,(f-232)/24) if f>=234 else 168
    if 232<=f<296:
        if f<240: sk.update(spr=SUKUNA['hurt'],x=ez(170,176,(f-232)/8),y=GROUND-int(4*math.sin(math.pi*(f-232)/8)))
        elif f<266: sk.update(spr=SUKUNA['hurt'],x=176)
        else: sk.update(spr=SUKUNA['idle'],x=ez(176,EX,(f-266)/26),aura=(SUKUNA_AURA,1) if f<286 else None)
    if 250<=f<290: s['fx'].append(('dmg',"HA HA HA",min(sk['x']-14,W-34),GROUND-28-(f//3)%2,(255,120,150)))
    s['actors']=[cl,sk]
    return s

CLIPS = [clip('domain', N_, clip_domain)]
