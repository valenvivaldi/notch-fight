"""The Odyssey (Homer, book 9): Claude as Odysseus, in a bronze Corinthian helmet with a red crest, in
the cave of the Cyclops Polyphemus: firelight, cheeses on the ledge, the flock in the back, the boulder
across the mouth. The giant grabs at him (WHO ARE YOU?); Odysseus gives him wine (MORE WINE!). Close-up:
MY NAME IS NOBODY. The Cyclops falls asleep; Odysseus heats the olive stake in the fire and drives it
into the eye (close-up, the hiss). The Cyclops roars NOBODY IS HURTING ME! and the other Cyclopes call
back NOBODY? THEN HUSH!. He rolls the boulder away and sits at the mouth feeling the sheep's backs;
Odysseus rides out clinging under the big ram. The tale goes dark and starts again by the fire."""
from engine import *

THEME = 'odyssey'
# deadpool's notchverse crossover uses the background, od_fire and od_cyclops: changing them changes that
# clip too (rebuild with ONLY=odyssey,deadpool).
N_ = 408
CX, PX = 30, 148                                                    # Odysseus; Polyphemus

SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
BRONZE,BRONZE_HI,BRONZE_D,CREST=(196,150,60),(240,204,120),(132,94,40),(200,40,40)
# Odysseus: the Corinthian helmet and its crest, a bronze breastplate
OPAL={'l':BRONZE,'f':BRONZE_HI,'a':(180,136,56),'i':BRONZE_D,'c':CREST}
HELM=["...ccccc....","..ccccccc...","...lllll....",".lflllllll..."]

def _odysseus(spr):
    g=[list(r) for r in overlay(spr,HELM,-1,0,bangs="llllllllll")]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y==top+1: g[y][x]='l'                       # the brow of the helmet
            elif c=='O' and top+2<=y<=top+4 and x<=l+1: g[y][x]='i'   # the back of it
            elif c=='O' and top+5<=y<top+8: g[y][x]='a' if (x+y)%3 else 'f'   # the breastplate
    return S([''.join(x) for x in g])
ODY=variant(_odysseus)

# ---- background: the Cyclops' cave -----------------------------------------------------------------
def _cave(d):
    d.rectangle([0,0,W,H],fill=(30,22,20))
    rr=random.Random(909)
    for _ in range(140):                                            # the rock, lit warmer near the fire
        x=rr.randint(0,W); y=rr.randint(0,50); r=rr.randint(3,9); k=max(0,1-abs(x-92)/110)
        c=int(36+30*k+rr.randint(-6,6)); d.ellipse([x-r,y-r,x+r,y+r],fill=(c+6,c-4,c-10))
    for x in range(4,W,11):                                         # stalactites
        L=rr.randint(3,10); d.polygon([(x-3,0),(x+3,0),(x,L)],fill=(44,32,28))
    d.polygon([(160,52),(162,26),(170,16),(180,14),(185,16),(185,52)],fill=(150,180,200))   # the mouth, daylight
    d.polygon([(166,52),(168,30),(176,22),(185,22),(185,52)],fill=(186,206,214))
    d.rectangle([4,22,40,24],fill=(70,52,40))                       # the ledge: cheeses and milk pails
    for x in (8,16,24): d.ellipse([x-3,17,x+3,22],fill=(226,200,120),outline=(150,120,60))
    d.rectangle([31,17,36,22],fill=(150,110,70)); d.line([31,18,36,18],fill=(236,236,230))
    d.rectangle([0,52,W,H],fill=(58,44,36)); d.line([0,52,W,52],fill=(80,62,48))
    for _ in range(50): d.point((rr.randint(0,W-1),rr.randint(53,H-1)),fill=rr.choice([(72,56,44),(46,34,28),(90,80,60)]))
    for x in range(52,84,5): d.line([x,52,x+1,50],fill=(120,110,70))   # straw where the flock beds down
register_bg(THEME, lambda v: (v+40,v+30,v+20), decor=_cave)

@fx('od_fire')
def _fx_fire(d,im,e,f):
    """The fire in the middle of the cave, and its glow."""
    _,x=e; rr=random.Random((f//2)%17)                               # a 34-frame flicker: it loops
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-46,GROUND-40,x+46,GROUND+14],fill=60+(f%3)*8)
    im.paste((255,150,60),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    for k in range(-2,3): d.line([x+k*3-2,GROUND+1,x+k*3+2,GROUND-1],fill=(70,46,30))
    for i in range(6):
        h=rr.randint(5,11); dx=rr.randint(-5,5)
        d.polygon([(x+dx-3,GROUND),(x+dx,GROUND-h),(x+dx+3,GROUND)],fill=(240,110,30) if i%2 else (255,190,60))
    d.polygon([(x-2,GROUND),(x,GROUND-5),(x+2,GROUND)],fill=(255,240,180))

SHEEP_BACK=((58,49),(70,50),(80,49))                                # the flock, bedded down at the back
def sheep(d,x,feet,big=False,f=0,walk=False):
    """A woolly sheep facing right (the ram is bigger, with curled horns)."""
    w,h,lg=(14,8,12) if big else (7,4,3)
    sw=(f//2)%2 if walk else 0
    for lx in (x-w+2,x+w-3):
        d.line([lx,feet-lg,lx+(sw if lx<x else -sw),feet],fill=(40,34,30),width=2 if big else 1)
    d.ellipse([x-w,feet-lg-h*2,x+w,feet-lg+2],fill=(232,226,210),outline=(150,140,124))
    rr=random.Random(int(x*0)+(7 if big else 3))
    for _ in range(10 if big else 3):
        px=x+rr.randint(-w+2,w-2); py=feet-lg-rr.randint(1,h*2-1); d.point((px,py),fill=(250,246,236))
    hx,hy=x+w,feet-lg-h-(2 if big else 1)
    d.ellipse([hx-2,hy-2,hx+(4 if big else 2),hy+(3 if big else 1)],fill=(50,42,38))
    if big: d.arc([hx-4,hy-5,hx+2,hy+1],90,360,fill=(180,160,120),width=2)

@fx('od_flock')
def _fx_flock(d,im,e,f):
    _,gone=e
    for i,(x,y) in enumerate(SHEEP_BACK):
        if i not in gone: sheep(d,x,y)

@fx('od_sheep')
def _fx_sheep(d,im,e,f):
    _,x,big=e; sheep(d,int(x),GROUND,big,f,walk=True)

@fx('od_boulder')
def _fx_boulder(d,im,e,f):
    _,x=e; x=int(x)
    d.ellipse([x-17,GROUND-36,x+17,GROUND+2],fill=(96,88,80),outline=(40,34,30))
    d.ellipse([x-12,GROUND-32,x+4,GROUND-16],fill=(118,110,100)); d.arc([x-10,GROUND-20,x+12,GROUND-4],20,120,fill=(70,62,56))

@fx('od_spear')
def _fx_spear(d,im,e,f):
    """Odysseus' spear, upright at his back hand."""
    _,x,feet=e; x=int(x)
    d.line([x,feet,x,feet-24],fill=(120,84,50)); d.polygon([(x-1,feet-24),(x,feet-29),(x+1,feet-24)],fill=BRONZE_HI)

@fx('od_bowl')
def _fx_bowl(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.chord([x-4,y-3,x+4,y+3],0,180,fill=(170,100,50),outline=(90,50,24)); d.line([x-3,y,x+3,y],fill=(120,20,50))

@fx('od_stake')
def _fx_stake(d,im,e,f):
    """The olive-wood stake, its point glowing (x0,y0 → x1,y1 = the point)."""
    _,x0,y0,x1,y1,hot=e
    d.line([x0,y0,x1,y1],fill=(130,96,56),width=2)
    if hot:
        d.ellipse([x1-2,y1-2,x1+2,y1+2],fill=(255,120,40) if f%4<2 else (255,200,90))
        for k in range(2): d.point((int(x1)+random.randint(-2,2),int(y1)-2-random.randint(0,4)),fill=(140,130,126))

@fx('od_z')
def _fx_z(d,im,e,f):
    _,x,y=e
    for k in range(3):
        ph=((f+k*11)%34)/34; text(d,"Z",int(x+ph*8),int(y-ph*14),(220,220,236) if ph<0.7 else (140,140,160))

# ---- the Cyclops ------------------------------------------------------------------------------------
CY_SKIN,CY_D,CY_HAIR,WOOL=(176,140,112),(140,106,84),(54,40,32),(220,212,190)
def limb(d,a,b,w=6,c=CY_SKIN):
    d.line([a,b],fill=OUT,width=w+2); d.line([a,b],fill=c,width=w)
def cyclops(d,x,pose,eye,f,k=0.0):
    """Polyphemus, facing left. pose: stand | reach (k: how far) | drink | sleep | blind | sit (k: groping);
    eye: open | closed | hurt."""
    dy={'sleep':16,'sit':14}.get(pose,0); x=int(x)
    sh_l,sh_r=(x-12,22+dy),(x+11,22+dy)
    hands={'stand':((x-17,42),(x+16,42)),'drink':((x-8,16),(x+16,42)),'blind':((x-7,12),(x-1,15)),
           'sleep':((x-16,46),(x+14,48)),'sit':((x-28+int(3*math.sin(2*math.pi*f/17)),48),(x+14,48))}
    if pose=='reach': hl=(int(lerp(x-17,x-62,k)),int(lerp(42,46,k))); hr=(x+16,42)
    else: hl,hr=hands[pose]
    limb(d,sh_r,hr,7); d.ellipse([hr[0]-4,hr[1]-4,hr[0]+4,hr[1]+4],fill=CY_D,outline=OUT)   # the back arm
    if dy:                                                          # sitting: thighs out front, shins down
        for lx in (x-4,x+4):
            limb(d,(lx,40+dy),(lx-14,GROUND-8),8); limb(d,(lx-14,GROUND-8),(lx-16,GROUND),7)
    else:
        for lx in (x-6,x+6): limb(d,(lx,40),(lx,GROUND-1),8); d.rectangle([lx-6,GROUND-2,lx+4,GROUND],fill=CY_D,outline=OUT)
    d.polygon([(x-14,20+dy),(x+13,20+dy),(x+10,44+dy),(x-11,44+dy)],fill=CY_SKIN,outline=OUT)   # the torso
    d.line([x-6,30+dy,x+4,30+dy],fill=CY_D); d.line([x-1,24+dy,x-1,36+dy],fill=CY_D)
    d.rectangle([x-12,38+dy,x+11,46+dy],fill=WOOL,outline=OUT)      # a sheepskin
    for tx in range(x-11,x+11,3): d.point((tx,46+dy+1),fill=WOOL)
    hy=dy+(2 if pose=='sleep' else 0)
    d.ellipse([x-11,1+hy,x+8,22+hy],fill=CY_SKIN,outline=OUT)        # the head
    d.chord([x-10,-1+hy,x+9,12+hy],200,340,fill=CY_HAIR); d.rectangle([x+5,4+hy,x+8,15+hy],fill=CY_HAIR)   # wild hair
    for k in range(4): d.line([x-8+k*5,1+hy,x-10+k*5,-2+hy],fill=CY_HAIR)
    d.polygon([(x-9,16+hy),(x+5,16+hy),(x+2,27+hy),(x-6,27+hy)],fill=CY_HAIR)   # the beard
    d.line([x-6,16+hy,x-1,16+hy],fill=(110,40,40))                 # the mouth
    ex,ey=x-2,9+hy                                                  # one eye, mid-brow
    d.line([ex-6,ey-5,ex+5,ey-5],fill=CY_HAIR,width=2)              # one heavy brow
    if eye=='open':
        d.ellipse([ex-6,ey-3,ex+5,ey+3],fill=(240,234,220),outline=OUT); d.ellipse([ex-4,ey-2,ex,ey+2],fill=(110,70,30)); d.rectangle([ex-3,ey-1,ex-2,ey],fill=(10,6,4))
    elif eye=='closed': d.arc([ex-6,ey-3,ex+5,ey+2],20,160,fill=OUT,width=1); d.line([ex-6,ey,ex+5,ey],fill=CY_D)
    else:
        d.ellipse([ex-6,ey-3,ex+5,ey+3],fill=(40,10,8),outline=OUT); d.point((ex-1,ey),fill=(255,120,40) if f%4<2 else (200,40,20))
    if pose=='drink': d.rectangle([x-8,16+hy,x-1,18+hy],fill=(80,20,30))
    limb(d,sh_l,hl,7); d.ellipse([hl[0]-5,hl[1]-5,hl[0]+5,hl[1]+5],fill=CY_SKIN,outline=OUT)   # the front arm
    if pose=='reach' and k>0.3:
        for j in range(3): d.line([hl[0]-5,hl[1]-3+j*3,hl[0]-8,hl[1]-3+j*3],fill=CY_SKIN)     # fingers
@fx('od_cyclops')
def _fx_cyclops(d,im,e,f):
    _,x,pose,eye,k=e; cyclops(d,x,pose,eye,f,k)

# ---- close-ups --------------------------------------------------------------------------------------
def helmet_face(d,ox,f):
    """Claude-as-Odysseus in the Corinthian helmet (x ox..ox+60): the crest, the T-shaped opening."""
    for i in range(16):                                             # the horsehair crest
        x=ox+4+i*3; d.line([x,10,x-2+int(math.sin(f*0.2+i)),-2],fill=CREST if i%3 else (150,20,20),width=2)
    d.rectangle([ox,8,ox+58,H],fill=BRONZE,outline=BRONZE_D)
    d.rectangle([ox+2,10,ox+8,H],fill=BRONZE_HI)
    d.rectangle([ox+12,24,ox+52,36],fill=SKIN); d.rectangle([ox+26,34,ox+38,H],fill=SKIN)   # the T opening
    for ex in (ox+18,ox+44):
        d.rectangle([ex-3,27,ex+3,33],fill=(24,14,12)); d.point((ex-1,28),fill=(255,230,170))
    d.line([ox+12,23,ox+52,23],fill=BRONZE_D,width=2); d.line([ox+31,24,ox+31,34],fill=BRONZE)   # the nose guard
    d.line([ox+29,54,ox+35,54],fill=(90,30,20))
    for y in range(40,H,6): d.point((ox+10,y),fill=BRONZE_D); d.point((ox+54,y),fill=BRONZE_D)   # rivets

def closeup_nobody(t,f):
    """Primer plano: Odysseus lit by the fire, the giant's shadow over him — MY NAME IS NOBODY."""
    im=Image.new('RGB',(W,H),(24,16,14)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([-30,10,90,90],fill=120+(f%3)*10)
    im.paste((255,140,50),(0,0),g.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(im)
    helmet_face(d,10,f)
    if t>=0.15: big_text(im,"MY NAME",12,(250,226,170),scale=2,cx=134,outline=(70,30,10))
    if t>=0.3: big_text(im,"IS NOBODY.",32,(250,226,170),scale=2,cx=134,outline=(70,30,10))
    if t<0.06: zoom_lines(d,(255,190,110))
    if t>0.9: im=fade_to(im,(0,0,0),0.6*(t-0.9)/0.1)
    return im

def closeup_eye(t,f):
    """Primer plano: the sleeping giant's eye, the glowing point coming in from the right; a white flash,
    the hiss, smoke — and the eye is gone."""
    im=Image.new('RGB',(W,H),CY_SKIN); d=ImageDraw.Draw(im)
    for y in range(0,H,7): d.line([0,y,W,y+3],fill=(166,130,104))
    d.rectangle([0,0,W,10],fill=CY_HAIR); d.polygon([(0,10),(W,6),(W,12),(0,16)],fill=CY_HAIR)   # the brow
    hit=t>=0.5
    if not hit:
        d.ellipse([38,16,122,54],fill=(190,154,124),outline=CY_D)    # the shut lid, bulging
        d.arc([44,22,116,40],200,340,fill=(206,172,142),width=2)   # its sheen
        d.arc([40,20,120,50],15,165,fill=OUT,width=2)              # the lash line
        for x in range(50,112,6): d.line([x,48+int(2*abs(math.sin(x*0.3))),x-2,53],fill=CY_HAIR)   # lashes
        p=ease(t/0.5); tx=int(lerp(W+10,84,p)); ty=36
        d.line([tx,ty,W+40,ty-8],fill=(130,96,56),width=7)
        d.ellipse([tx-5,ty-5,tx+5,ty+5],fill=(255,120,40) if f%4<2 else (255,200,90))
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([tx-20,ty-16,tx+20,ty+16],fill=120)
        im.paste((255,160,70),(0,0),g.filter(ImageFilter.GaussianBlur(8))); d=ImageDraw.Draw(im)
    else:
        d.ellipse([40,18,120,52],fill=(50,16,12),outline=OUT,width=2)
        d.line([84,36,W+40,28],fill=(70,50,34),width=7)
        rr=random.Random(f)
        for _ in range(int(40*(1-(t-0.5)))):                         # smoke and sparks
            x=84+rr.randint(-30,40); y=36-rr.randint(0,40); r=rr.randint(2,6)
            d.ellipse([x-r,y-r,x+r,y+r],fill=rr.choice([(150,140,136),(110,104,100)]))
        for _ in range(10): d.point((84+rr.randint(-16,16),36+rr.randint(-12,12)),fill=(255,200,90))
        big_text(im,"TSSSS",44,(255,236,200),scale=2,cx=140,outline=(90,30,10))
        if t<0.56: im=fade_to(im,(255,255,255),1-(t-0.5)/0.06); d=ImageDraw.Draw(im)
    if t<0.05: zoom_lines(d)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
def clip_nobody(f):
    s=scene(f,THEME)
    s['under'].append(('od_fire',92))
    ox,oy,opose,show=CX,GROUND,guard_pose(f),True
    cpose,ceye,ck,cxp=('stand','open',0.0,PX)
    boulder=176; gone=[]
    # 1) WHO ARE YOU?: the giant hand sweeps for him
    if 16<=f<54: s['fx'].append(('big',"WHO ARE YOU?",3,(236,214,180)))
    if 18<=f<44:
        t=(f-18)/26; cpose,ck='reach',math.sin(math.pi*t)
        if 24<=f<36: p=(f-24)/12; ox,oy,opose=ez(CX,16,p),GROUND-int(12*math.sin(math.pi*p)),'guard2'
        elif f>=36: ox=ez(16,CX,(f-36)/8)
    # 2) the wine
    if 50<=f<64: ox,opose=ez(CX,70,(f-50)/14),guard_pose(f)
    if 64<=f<110: ox=70 if f<96 else ez(70,50,(f-96)/12)
    if 64<=f<72: opose='armsup'; s['fx'].append(('od_bowl',70,GROUND-17))
    if 72<=f<80: p=(f-72)/8; s['fx'].append(('od_bowl',lerp(70,PX-12,p),lerp(GROUND-17,26,p)))
    if 72<=f<96: cpose='drink'
    if 76<=f<96: s['fx'].append(('od_bowl',PX-10,24))
    if 80<=f<112: s['fx'].append(('big',"MORE WINE!",3,(236,214,180))); cxp=PX+int(2*math.sin(f*0.25))
    if f>=110 and f<170: ox=50
    # 3) close-up: MY NAME IS NOBODY
    if 110<=f<170: s['image']=closeup_nobody((f-110)/60,f); return s
    # 4) he sleeps; the stake heats in the fire; Odysseus drives it in
    if 170<=f<262: cpose,ceye='sleep','closed'
    if 176<=f<262: s['fx'].append(('od_z',PX+2,14))
    if 170<=f<196: ox=50
    if 196<=f<216: ox,opose=ez(50,82,(f-196)/10),'charge'
    if 196<=f<226:
        if f<206: s['fx'].append(('od_stake',92,GROUND,98,GROUND-6,f>=200))
        else:
            if f>=216: ox,opose=ez(82,PX-28,(f-216)/10),'dash'
            s['fx'].append(('od_stake',ox-6,GROUND-6,ox+14,GROUND-14,True))
    if 226<=f<262: s['image']=closeup_eye((f-226)/36,f); return s
    # 5) NOBODY IS HURTING ME!
    if 262<=f<312:
        cpose,ceye='blind','hurt'; cxp=PX+(rshake(2)[0] if f<290 else 0)
        if f<280: s['shake']=rshake(2)
        p=min(1,(f-262)/12); ox,oy,opose=ez(PX-28,46,p),GROUND-int(14*math.sin(math.pi*p)),'hurt' if p<1 else guard_pose(f)
        s['fx'].append(('big',"NOBODY IS",3,(255,200,170))); s['fx'].append(('big',"HURTING ME!",17,(255,200,170)))
        rr=random.Random(f//2)
        for j in range(3): s['fx'].append(('smoke',PX-4+rr.randint(-3,3),8-rr.randint(0,6),1+j%2,(150,140,136)))
    if 312<=f<350:
        callout(s,"NOBODY? THEN HUSH!",y=12,c=(180,190,210)); ox=46
    # 6) the boulder rolls away; he sits at the mouth feeling the sheep's backs
    if 312<=f<378: cpose,ceye='sit','hurt'
    if 312<=f<378: boulder=ez(176,216,(f-312)/16)
    if 312<=f<330: cpose='blind'
    flock=[(330,False,0),(340,True,1),(352,False,2)]
    if 330<=f<378:
        for t0,big,i in flock:
            if f<t0: continue
            gone.append(i); x=lerp(SHEEP_BACK[i][0],214,(f-t0)/26)
            if big:
                show=x<200
                ox,oy,opose=x+1,GROUND-1,None                        # clinging under the ram
            s['fx'].append(('od_sheep',x,big))
        if f>=340: show=lerp(SHEEP_BACK[1][0],214,(f-340)/26)<200
        ck=1
    if 340<=f<378 and opose is None:
        s['actors'].append(actor(S(ODY['guard'][::-1]),ox,GROUND-1,pal=OPAL)); show=False
    s['under'].append(('od_flock',gone))
    s['under'].append(('od_boulder',boulder))
    s['under'].append(('od_cyclops',cxp,cpose,ceye,ck))
    if show:
        s['under'].append(('od_spear',ox-7,oy))
        s['actors'].append(actor(ODY[opose or 'guard'],ox,oy,pal=OPAL))
    # 7) the tale goes dark, and starts again by the fire
    if 366<=f<388: s['fx'].append(('dim',min(1,(f-366)/10)))
    if 388<=f<400: s['fx'].append(('dim',max(0,1-(f-388)/11)))
    return s

CLIPS = [clip('nobody', N_, clip_nobody)]
