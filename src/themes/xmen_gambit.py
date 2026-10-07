"""X-Men '97 sub-theme "xmen-gambit": Claude as Gambit (Remy LeBeau: the cowl and the auburn hair, red-on-
black eyes, pink chest armour, the long brown coat, the bo staff) in the French Quarter at night,
wrought-iron balconies and gas lamps. Three Sentinel drones jet in (BONJOUR MES AMIS); a charged card
for each and they go up in pink. A giant Sentinel stomps in (SURRENDER MUTANT) and grabs; Gambit vaults
over its hand on his staff. Close-up: the ace of spades in his fingers, the kinetic charge crawling over
it — CHARGED. He throws it into the Sentinel's chest and it blows apart; he walks back out of the smoke,
coat flapping (DEALER WINS.). The heroic take: in the show his big moment is Genosha, not this."""
from engine import *
from themes.xmen_nightcrawler import DR                            # same show: the Sentinel drone

THEME = 'xmen-gambit'
N_ = 317
CX = 30                                                             # the loop keyframe position

PINK, PINK_HI = (255,80,200), (255,210,244)
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
# Gambit: the cowl, auburn hair, red eyes, pink armour, the brown coat, dark trousers, brown boots
GPAL = {'1':(58,48,72),'2':(150,60,40),'3':(240,40,50),'4':(196,70,140),'5':(140,40,100),
        '6':(138,90,54),'7':(44,44,76),'8':(98,60,36)}
HAIR = ["...2.2.2....","..2222222...",".111111111.."]

def _gambit(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0,bangs="1111111111")]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='K': g[y][x]='3'
            elif c=='O':
                if y<top+5: g[y][x]='1' if x<=l+2 else 'O'             # the cowl round the face
                elif y<top+8: g[y][x]='6' if x in (l,l+1,r) else ('4' if (x+y)%3 else '5')   # coat over the armour
                else: g[y][x]='6'
            elif c=='o': g[y][x]='6' if y<top+8 else ('8' if y==h-1 else '7')
    return S([''.join(x) for x in g])
GAM=variant(_gambit)

# ---- background: the French Quarter at night ---------------------------------------------------------
def _quarter(d):
    for y in range(40):
        k=y/39; d.line([0,y,W,y],fill=(int(30+40*k),int(20+22*k),int(60+36*k)))
    d.ellipse([20,4,30,14],fill=(240,236,214)); d.ellipse([23,4,31,12],fill=(int(30),int(20),int(60)))   # a crescent
    rr=random.Random(1718)
    walls=[(150,96,80),(120,104,130),(170,130,90),(104,120,110)]
    x=-4; i=0
    while x<W:                                                      # townhouses with iron balconies
        w=rr.randint(26,36); top=rr.randint(10,16); c=walls[i%4]
        d.rectangle([x,top,x+w,48],fill=c); d.rectangle([x,top,x+w,top+2],fill=tuple(v-30 for v in c))
        for wx in range(x+4,x+w-4,9):
            for wy in (top+5,top+21):
                lit=rr.random()<0.5
                d.rectangle([wx,wy,wx+4,wy+9],fill=(255,206,120) if lit else (50,40,60))
                d.line([wx-1,wy-1,wx+5,wy-1],fill=tuple(v-40 for v in c))
        by=top+15; d.rectangle([x,by,x+w,by+1],fill=(26,22,30))      # the balcony
        for bx in range(x,x+w,3): d.line([bx,by+1,bx,by+5],fill=(26,22,30))
        d.line([x,by+5,x+w,by+5],fill=(26,22,30))
        x+=w+1; i+=1
    for lx in (60,128):                                             # gas lamps
        d.line([lx,48,lx,30],fill=(26,22,30)); d.rectangle([lx-2,26,lx+2,30],fill=(255,220,140),outline=(26,22,30))
    d.rectangle([0,48,W,H],fill=(70,60,74))                         # the cobbles
    for y in range(50,H,3):
        for x in range((y//3)%2*3,W,6): d.point((x,y),fill=(56,48,60))
register_bg(THEME, lambda v: (v+50,v+40,v+60), decor=_quarter)

# ---- effects ----------------------------------------------------------------------------------------
@fx('gm_coat')
def _fx_coat(d,im,e,f):
    """The tails of the long coat, behind his legs (sw: how hard it flaps)."""
    _,x,feet,flip,sw=e; back=1 if flip else -1
    for k in range(4):
        sx=x+back*(1+k); wav=math.sin(f*0.3+k)*(1+sw*2)
        d.line([sx,feet-6,sx+back*(1+sw*3)+wav,feet-1],fill=GPAL['6'] if k%2 else (112,72,44))

@fx('gm_staff')
def _fx_staff(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(150,150,166)); d.point((x0,y0),fill=(220,220,236)); d.point((x1,y1),fill=(220,220,236))

def card(d,x,y,glow,f):
    x,y=int(x),int(y)
    if glow:
        r=3+(f%2); d.ellipse([x-r,y-r,x+r,y+r],fill=PINK)
    d.rectangle([x-1,y-2,x+1,y+2],fill=(250,250,250),outline=(120,120,140) if not glow else PINK_HI)

@fx('gm_card')
def _fx_card(d,im,e,f):
    """A charged card in flight with its pink trail (from x0,y0)."""
    _,x0,y0,x,y=e
    n=8
    for j in range(n):
        t=j/n; d.point((int(lerp(x0,x,0.6+0.4*t)),int(lerp(y0,y,0.6+0.4*t))),fill=PINK if j%2 else PINK_HI)
    card(d,x,y,True,f)

@fx('gm_blast')
def _fx_blast(d,im,e,f):
    """A kinetic explosion: pink rings round a white core, sparks."""
    _,x,y,r=e; x,y,r=int(x),int(y),int(r)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-r-6,y-r-6,x+r+6,y+r+6],fill=170)
    im.paste(PINK,(0,0),g.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    d.ellipse([x-r,y-r,x+r,y+r],outline=PINK_HI,width=2)
    d.ellipse([x-r//2,y-r//2,x+r//2,y+r//2],fill=(255,255,255))
    rr=random.Random(f)
    for _ in range(8):
        a=rr.uniform(0,6.283); L=r+rr.randint(2,8); d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L)),fill=PINK_HI)

# ---- the giant Sentinel -----------------------------------------------------------------------------
SV,SVD,SP_,SFACE=(106,58,178),(64,32,120),(240,120,170),(190,190,206)
def sentinel(d,x,f,reach=0.0,eyes=1.0):
    """The giant Sentinel, facing left, filling the panel's height; reach 0..1 sends its hand out."""
    x=int(x)
    def part(box,c): d.rectangle(box,fill=c,outline=OUT)
    part([x-12,40,x-3,GROUND],SV); part([x+4,40,x+13,GROUND],SV)     # legs
    part([x-13,GROUND-4,x-2,GROUND],SP_); part([x+3,GROUND-4,x+14,GROUND],SP_)
    part([x-12,46,x-3,49],SP_); part([x+4,46,x+13,49],SP_)            # knees
    part([x+16,18,x+24,38],SVD); part([x+17,38,x+23,42],SP_)         # the back arm
    part([x-16,14,x+16,40],SV)                                       # the torso
    d.polygon([(x-10,18),(x+10,18),(x+6,30),(x-6,30)],fill=SP_,outline=OUT)   # the chest plate
    d.ellipse([x-4,21,x+4,27],fill=SFACE,outline=OUT)
    part([x-17,13,x+17,17],SVD)                                      # shoulders
    part([x-9,-6,x+9,13],SV)                                         # the head, cropped by the top edge
    part([x-7,0,x+7,12],SFACE)
    for ex in (x-5,x+1):
        c=tuple(int(v*eyes) for v in (255,230,90)); d.rectangle([ex,4,ex+3,6],fill=c)
    d.line([x-4,9,x+4,9],fill=(60,60,70))
    hx,hy=int(lerp(x-20,x-74,reach)),int(lerp(38,46,reach))          # the front arm
    d.line([x-14,18,hx+4,hy-2],fill=OUT,width=8); d.line([x-14,18,hx+4,hy-2],fill=SVD,width=6)
    d.ellipse([hx-6,hy-6,hx+6,hy+6],fill=SP_,outline=OUT)
    for j in range(3): d.line([hx-6,hy-3+j*3,hx-10,hy-3+j*3],fill=SP_,width=2)

@fx('gm_sentinel')
def _fx_sentinel(d,im,e,f):
    _,x,reach,eyes=e; sentinel(d,x,f,reach,eyes)

@fx('gm_debris')
def _fx_debris(d,im,e,f):
    """The Sentinel in pieces, t frames after the blast."""
    _,x,y,t=e; rr=random.Random(42)
    for i in range(30):
        vx=rr.uniform(-3,3); vy=rr.uniform(-4,0.5); s=rr.randint(2,5)
        px=x+vx*t; py=min(GROUND-1,y+vy*t+0.12*t*t+rr.randint(-14,24))
        d.rectangle([px,py,px+s,py+s//2+1],fill=rr.choice([SV,SVD,SP_,SFACE]),outline=OUT)

# ---- close-up ---------------------------------------------------------------------------------------
def closeup_card(t,f):
    """Primer plano: the ace of spades between two fingers; the charge crawls over it — CHARGED."""
    im=Image.new('RGB',(W,H),(26,16,40)); d=ImageDraw.Draw(im)
    k=min(1,max(0,(t-0.12)/0.4))                                     # how charged
    if k:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([60-30*k,4-20*k,110+30*k,64+20*k],fill=int(150*k))
        im.paste(PINK,(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    ox=4                                                            # his face, below, in the cowl's shadow
    d.rectangle([ox,30,ox+52,H],fill=GPAL['1']); d.rectangle([ox+10,38,ox+44,H],fill=SKIN)
    for j in range(6): d.polygon([(ox+2+j*9,32),(ox+10+j*9,32),(ox+4+j*9,22+(j%2)*4)],fill=GPAL['2'])
    for ex in (ox+18,ox+36):
        d.rectangle([ex-4,44,ex+4,49],fill=(10,6,10)); d.rectangle([ex-1,45,ex+2,48],fill=(240,40,50) if k<1 or f%4<3 else (255,140,140))
    d.line([ox+12,42,ox+24,43],fill=INK); d.line([ox+30,43,ox+42,42],fill=INK)
    d.line([ox+20,58,ox+32,57],fill=(90,30,20))                      # the half smile
    cx,cy=84,30; jx=random.Random(f).randint(-1,1) if k>=1 else 0    # the card, trembling once full
    d.rectangle([cx-12+jx,cy-18,cx+12+jx,cy+18],fill=(250,248,240),outline=PINK_HI if k else (120,120,140),width=2 if k else 1)
    d.polygon([(cx+jx,cy-8),(cx-6+jx,cy+2),(cx+6+jx,cy+2)],fill=(20,20,26)); d.ellipse([cx-7+jx,cy-2,cx-1+jx,cy+4],fill=(20,20,26))
    d.ellipse([cx+1+jx,cy-2,cx+7+jx,cy+4],fill=(20,20,26)); d.polygon([(cx-2+jx,cy+2),(cx+2+jx,cy+2),(cx+jx,cy+9)],fill=(20,20,26))   # the spade
    text(d,"A",cx-10+jx,cy-16,(20,20,26),shadow=None); text(d,"A",cx+7+jx,cy+11,(20,20,26),shadow=None)
    d.rectangle([cx-16,cy+12,cx-6,cy+26],fill=SKIN,outline=INK); d.rectangle([cx-6,cy+12,cx+4,cy+22],fill=SKIN,outline=INK)   # two fingers
    d.polygon([(cx-24,H),(cx-16,cy+22),(cx+4,cy+22),(cx+8,H)],fill=(40,30,40))   # the glove
    if k:                                                           # the charge, crawling from the fingers up
        rr=random.Random(f)
        for _ in range(int(40*k)):
            px=cx+rr.randint(-13,13); py=cy+18-rr.randint(0,int(38*k)); d.point((px+jx,py),fill=rr.choice([PINK,PINK_HI,(255,255,255)]))
    if t>=0.35:
        jj=(f%3)-1 if t<0.45 else 0
        big_text(im,"CHARGED",22,PINK_HI,scale=2,cx=148+jj,outline=(90,10,70))
    if t<0.06: zoom_lines(d,PINK_HI)
    if t>0.88: im=fade_to(im,PINK,(t-0.88)/0.12*0.7)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
DRONES=[84,116,148]
THROWS=[44,54,64]                                                   # one card each
SX=150                                                              # the giant Sentinel
def clip_charged(f):
    s=scene(f,THEME)
    gx,gy,gpose,sw=CX,GROUND,guard_pose(f),0
    acts=[]
    if 20<=f<58: callout(s,"BONJOUR MES AMIS",c=PINK_HI)
    # 1) the drones, and a card for each
    for i,x in enumerate(DRONES):
        if not 14<=f<290: continue
        t0=THROWS[i]; hit=t0+8
        if f<34: feet=lerp(-4,GROUND-6,ease((f-14-i*3)/18)); pose='idle'; fly=True
        elif f<hit: feet=GROUND-6+int(math.sin(f*0.2+i)); pose='idle'; fly=True
        elif f<hit+6: feet=GROUND-6; pose='hurt'; fly=False
        else: feet=GROUND; pose='wreck'; fly=False
        a=1 if f<270 else max(0,1-(f-270)/14)
        if not (hit<=f<hit+3): acts.append(actor(DR[pose],x+(min(f-hit,6) if f>=hit else 0),int(feet),flip=True,alpha=a))
        if fly: s['fx'].append(('nc_jet',x,int(feet)))
        if t0<=f<hit:
            p=(f-t0)/8; s['fx'].append(('gm_card',CX+8,GROUND-6,lerp(CX+8,x,p),lerp(GROUND-6,feet-8,p)))
        if hit<=f<hit+8: s['fx'].append(('gm_blast',x,feet-8,3+(f-hit)*2))
        if f==hit: s['shake']=rshake(2); s['flash']=0.4; s['fc']=(x,GROUND-10); s['flashc']=PINK
        if f>=hit+6 and f<290 and random.Random(f//3+i).random()<0.4: s['fx'].append(('smoke',x+3,GROUND-5,2,(90,80,96)))
    for t0 in THROWS:
        if t0-2<=f<t0+3: gpose='punch'
    # 2) the giant Sentinel stomps in and grabs; Gambit vaults over its hand
    sx,reach,eyes=None,0.0,1.0
    if 84<=f<200:
        sx=ez(230,SX,(f-84)/16)
        if f in (92,100): s['shake']=rshake(3); s['fx']+= [('dust',int(sx)+random.randint(-14,14),GROUND-1) for _ in range(4)]
        if 104<=f<126: reach=math.sin(math.pi*(f-104)/22)
    if 98<=f<130: s['fx'].append(('big',"SURRENDER MUTANT",22,(255,236,120)))
    if 110<=f<126:
        p=(f-110)/16; gx,gy,gpose,sw=ez(CX,70,p),GROUND-int(22*math.sin(math.pi*p)),'armsup',1
        s['under'].append(('gm_staff',int(lerp(CX+4,70,p)),GROUND,int(gx),int(gy)-12))
    if 126<=f<240: gx=70
    # 3) close-up: the card
    if 130<=f<180: s['image']=closeup_card((f-130)/50,f); return s
    # 4) the throw, the blast
    if 180<=f<194:
        gpose='punch' if f<186 else gpose; p=(f-182)/12
        if f>=182: s['fx'].append(('gm_card',72,GROUND-8,lerp(72,SX,p),lerp(GROUND-8,24,p)))
    if 194<=f<200: s['flash']=1.0; s['fc']=(SX,24); s['flashc']=PINK_HI
    if 194<=f<214: s['fx'].append(('gm_blast',SX,24,4+(f-194)*3)); s['shake']=rshake(3 if f<204 else 1)
    if 198<=f<236: s['fx'].append(('gm_debris',SX,24,f-198))
    if 200<=f<236: sw=1
    if 200<=f<236:
        rr=random.Random(f//2)
        for j in range(int(10*(236-f)/36)): s['fx'].append(('smoke',SX+rr.randint(-30,30),GROUND-rr.randint(0,40),rr.randint(2,5),(150,110,150)))
    if sx is not None and f<196: s['under'].append(('gm_sentinel',sx,reach,eyes))
    # 5) he walks back out of the smoke
    if 240<=f<276: s['fx'].append(('big',"DEALER WINS.",4,PINK_HI))
    if 246<=f<276: p=(f-246)/30; gx,gpose,sw=ez(70,CX,p),guard_pose(f),1 if p<1 else 0
    if 246<=f<276: gy=GROUND-((f//3)%2 if p<1 else 0)
    flip=246<=f<276
    s['under'].append(('gm_coat',gx,gy,flip,sw))
    if not (110<=f<126): s['under'].append(('gm_staff',gx+(6 if flip else -6),gy,gx+(6 if flip else -6),gy-20))
    acts.append(actor(GAM[gpose],gx,gy,flip=flip,pal=GPAL))
    s['actors']=acts
    return s

CLIPS = [clip('charged', N_, clip_charged)]
