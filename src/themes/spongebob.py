"""SpongeBob SquarePants: Claude is SpongeBob (square yellow sponge with holes, big eyes, buck
teeth, white shirt, red tie, brown square pants) at the grill outside the Krusty Krab, under the
flower clouds of Bikini Bottom; tiny Plankton waits by the Chum Bucket. I'M READY! I'M READY!:
Krabby Patties flip into the air. Plankton climbs into his giant robot: THE FORMULA WILL BE MINE!
SpongeBob hops its claw without leaving the grill and flips patties into it (SPLAT!); Squidward
sighs at the porthole (UGH.), Mr. Krabs bursts out of the door (MONEY!). Close-up: the spatula
raised, the eyes shining: ORDER UP! One last patty straight into the cockpit: the robot falls apart
and Plankton flies back to the Chum Bucket (I'LL GET YOU NEXT TIME!). A bubble wipe, the title
card: 2000 YEARS LATER... and Plankton trudges back to his spot."""
import zlib
from engine import *

THEME = 'spongebob'
N_ = 293
CX, VX = 30, 150                                                   # the neutral pose: Claude, Plankton
RX = 128                                                           # where the robot stands
GRILL = (41, 53)                                                   # the grill's top-left corner
PATTY = (47, 51)                                                   # a patty resting on it

# ---- Claude as SpongeBob -------------------------------------------------------------------------
def _sb(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])
    mid=(l+r)//2+1
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and not inside: g[y][x]='Y'                              # a fist
            elif c=='O' and y>=bot-1: g[y][x]='q'                              # square pants
            elif c=='O' and y==bot-2: g[y][x]='r' if x==mid else 'W'            # shirt and tie
            elif c=='O': g[y][x]='h' if (x*3+y*5)%7==0 else 'Y'                 # the sponge, with holes
            elif c=='o' and y>bot: g[y][x]='k' if y==h-1 else 'Y'              # legs, black shoes
            elif c=='o' and y==bot: g[y][x]='q'
            elif c=='o': g[y][x]='Y'                                           # arms
    eyes=[(x,y) for y in range(h-1) for x in range(1,w) if spr[y][x]=='K' and (y==0 or spr[y-1][x]!='K') and spr[y+1][x]=='K']
    for x,y in eyes:                                                           # big round eyes, blue iris
        g[y][x-1]=g[y][x]=g[y+1][x-1]='W'; g[y+1][x]='E'
    if eyes:                                                                   # the grin and the buck teeth
        ys=eyes[0][1]+2; xs=[x for x,_ in eyes]
        for x in range(min(xs)-1,max(xs)+1):
            if g[ys][x] in 'Yh': g[ys][x]='k'
        for x in (mid-1,mid):
            if ys+1<h and g[ys+1][x] in 'Yh': g[ys+1][x]='W'
    return ungrid(g)
SB=variant(_sb)
SBPAL={'Y':(250,232,80),'h':(196,182,52),'W':(250,250,250),'E':(60,140,230),'k':(24,20,20),
       'r':(220,40,40),'q':(150,98,48)}

# ---- Plankton and his robot ----------------------------------------------------------------------
_PK=S([
"k...k",
".k.k.",
"..k..",
".ggg.",
"gWWWg",
"gWrWg",
"gWKWg",
"gWWWg",
".ggg.",
"kgggk",
".ggg.",
".g.g.",])
_PK2=S([".k.k.","..k..","..k.."]+_PK[3:])                         # the antennae twitch
PK={'idle':_PK,'idle2':_PK2,'hurt':hurt(S(_PK+[])),'down':rotate90(_PK,1)}
PKPAL={'g':(70,150,60),'W':(250,250,240),'r':(220,40,40),'K':(10,10,10),'k':(30,60,30)}
def pk_idle(f): return PK['idle'] if (f//6)%2==0 else PK['idle2']

_ROBOT=S([
".......dddddddd.......",
"......dccccccccd......",
"......dccgWWgccd......",
"......dccgrKgccd......",
"......dccggggccd......",
"......dddddddddd......",
"....DDDDDDDDDDDDDD....",
"...DDDDDDDDDDDDDDDD...",
"dddDDrDDDDDDDDDDrDDddd",
"dDdDDDDDDDDDDDDDDDDdDd",
"dDdDDDDDDggDDDDDDDDdDd",
"dDdDDDDDDggDDDDDDDDdDd",
"dDdDDDDDDDDDDDDDDDDdDd",
"kkk.DDDDDDDDDDDDDD.kkk",
"k.k.DDDDDDDDDDDDDD.k.k",
"....dddddddddddddd....",
".....dDd......dDd.....",
".....dDd......dDd.....",
".....dDd......dDd.....",
"....ddDdd....ddDdd....",
"...ddddddd..ddddddd...",])
ROBOT=poses(_ROBOT,13,'k',6)
ROBOT['step']=S(_ROBOT[:16]+[".....dDd.......dDd....",".....dDd.......dDd....","....ddDdd.....dDd.....",
                             "...ddddddd...ddDdd....","............ddddddd..."])
ROBOTPAL={'d':(60,80,70),'D':(110,140,120),'c':(160,230,200),'g':(70,150,60),'W':(250,250,240),
          'r':(220,40,40),'K':(10,10,10),'k':(40,44,48)}

# ---- Squidward and Mr. Krabs, in the Krusty Krab's door --------------------------------------------
SQUID=S([
"..TTTTT..",
".TTTTTTT.",
"TTTTTTTTT",
"TkkTTTkkT",
"TWKTTTWKT",
".TTTTTTT.",
"...TTT...",
"...TTT...",
"....T....",
"..qqqqq..",
".TqqqqqT.",
"..qqqqq..",
"..T.T.T..",
".T..T..T.",])
SQUIDPAL={'T':(150,200,190),'k':(110,150,140),'W':(250,250,240),'K':(20,20,20),'q':(160,100,60)}
KRABS=S([
"..WK...WK...",
"...R...R....",
"...R...R....",
"..RRRRRRR...",
".RRRRRRRRR..",
"RRRRkkkRRRR.",
"RRLLLLLLLRR.",
"RR.LLLLL.RR.",
"RRR.LLL.RRR.",
"....RRR.....",
"...R...R....",
"..RR...RR...",])
KRABS_UP=S(["RR........RR","RR..WK.WK.RR",".R...R..R.R."]+[".."+r[2:10]+".." for r in KRABS[3:]])
KRABSPAL={'R':(220,60,40),'W':(250,250,240),'K':(20,20,20),'k':(120,20,20),'L':(90,150,220)}
DOOR = 90

# ---- background: Bikini Bottom, the Krusty Krab, the Chum Bucket -----------------------------------
def _flower(d,x,y,r,c):
    for k in range(5):
        a=k*math.tau/5; d.ellipse([x+math.cos(a)*r-r,y+math.sin(a)*r-r,x+math.cos(a)*r+r,y+math.sin(a)*r+r],fill=c)
    d.ellipse([x-r+1,y-r+1,x+r-1,y+r-1],fill=tuple(min(255,v+40) for v in c))

def _bikini(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(30+10*k),int(90+40*k),int(150+20*k)))
    for x,y,r,c in ((14,8,3,(70,150,190)),(52,5,2,(110,170,200)),(140,9,3,(90,160,180)),(176,4,2,(110,150,200)),
                    (100,4,2,(80,140,200))):
        _flower(d,x,y,r,c)
    d.rectangle([0,GROUND-3,W,GROUND],fill=(200,184,130))           # the sand
    rr=random.Random(zlib.crc32(b'bikini-bottom'))
    for _ in range(30): d.point((rr.randint(0,W-1),rr.randint(GROUND-3,GROUND)),fill=(170,154,104))
    # the Krusty Krab: a lobster trap of planks with portholes and a door
    x0,x1,top=64,118,30
    d.rectangle([x0,top,x1,GROUND-3],fill=(140,96,56))
    for x in range(x0,x1,6): d.line([x,top,x,GROUND-3],fill=(112,74,40))
    d.polygon([(x0-3,top),(x0+8,top-8),(x1-8,top-8),(x1+3,top)],fill=(110,140,160))   # the roof
    for x in range(x0+2,x1,8): d.line([x,top-7,x+2,top],fill=(80,108,128))
    for wx in (70,104):
        d.ellipse([wx-4,top+5,wx+4,top+13],fill=(60,80,100),outline=(70,52,30))       # portholes
        d.ellipse([wx-2,top+7,wx+2,top+11],fill=(130,190,220))
    d.rectangle([DOOR-5,top+8,DOOR+5,GROUND-3],fill=(70,52,30))     # the door
    d.rectangle([x0+3,top-16,x1-3,top-9],fill=(240,230,200),outline=(140,30,30))
    text(d,"KRUSTY KRAB",x0+6,top-14,(200,40,40),shadow=None)
    # the Chum Bucket, far right
    d.polygon([(166,GROUND-3),(168,40),(184,40),(186,GROUND-3)],fill=(110,116,124))
    d.rectangle([166,40,186,42],fill=(80,86,92)); d.arc([168,32,184,48],180,360,fill=(80,86,92))
    # the grill
    gx,gy=GRILL
    d.rectangle([gx,gy,gx+12,gy+2],fill=(80,80,86)); d.line([gx,gy,gx+12,gy],fill=(255,110,40))
    d.line([gx+1,gy+3,gx+1,GROUND],fill=(60,60,64)); d.line([gx+11,gy+3,gx+11,GROUND],fill=(60,60,64))
register_bg(THEME, lambda v: (v+40,v+30,v//2+10), decor=_bikini)

# ---- effects ---------------------------------------------------------------------------------------
@fx('sb_patty')
def _fx_patty(d,im,e,f):
    """A Krabby Patty: bun, lettuce, meat."""
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x-2,y-2,x+2,y-2],fill=(230,170,80)); d.rectangle([x-3,y-1,x+3,y-1],fill=(90,190,60))
    d.rectangle([x-3,y,x+3,y],fill=(110,60,30)); d.rectangle([x-2,y+1,x+2,y+1],fill=(230,170,80))

@fx('sb_spat')
def _fx_spat(d,im,e,f):
    """The spatula from the hand at (x,y): flat over the grill, or flicked up."""
    _,x,y,up=e
    if up: d.line([x,y,x+3,y-3],fill=(150,100,50)); d.rectangle([x+3,y-6,x+5,y-3],fill=(200,200,210))
    else: d.line([x,y,x+3,y],fill=(150,100,50)); d.rectangle([x+4,y-1,x+7,y],fill=(200,200,210))

@fx('sb_bubbles')
def _fx_bubbles(d,im,e,f):
    """The bubble wipe: t in 0..1, bubbles rise and cover the screen around t=0.5."""
    _,t=e; rr=random.Random(4242)
    for i in range(70):
        x=rr.randint(-6,W+6); r=rr.randint(3,11); sp=rr.uniform(0.8,1.3)
        y=H+20-(t*sp)*(H+60)+rr.randint(-10,30)
        if -r<y<H+r:
            d.ellipse([x-r,y-r,x+r,y+r],fill=(170,220,250),outline=(230,250,255))
            d.arc([x-r+2,y-r+2,x-1,y-1],180,270,fill=(255,255,255))

@fx('sb_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('sb_say',txt,y,c,scale,outline))

# ---- close-up and the title card -------------------------------------------------------------------
def closeup_order(t,f):
    """SpongeBob's face fills the panel, the spatula comes up, the eyes shine: ORDER UP!"""
    im=Image.new('RGB',(W,H),(250,232,80)); d=ImageDraw.Draw(im)
    rr=random.Random(7)
    for _ in range(26):                                             # the holes
        x,y,r=rr.randint(0,W),rr.randint(0,H),rr.randint(2,5)
        d.ellipse([x-r,y-r//1.4,x+r,y+r//1.4],fill=(196,182,52))
    for ex in (62,112):                                             # the eyes
        d.ellipse([ex-17,6,ex+17,40],fill=(250,250,250),outline=(30,30,30))
        d.ellipse([ex-9,14,ex+9,32],fill=(60,140,230)); d.ellipse([ex-4,19,ex+4,27],fill=(10,10,10))
        d.ellipse([ex+2,17,ex+6,21],fill=(255,255,255))
        for k in (-8,0,8): d.line([ex+k,6,ex+k*1.4,0],fill=(30,30,30),width=2)       # lashes
    d.chord([56,34,118,60],0,180,fill=(150,40,40),outline=(30,30,30))               # the grin
    d.rectangle([80,44,86,52],fill=(255,255,255),outline=(30,30,30)); d.rectangle([88,44,94,52],fill=(255,255,255),outline=(30,30,30))
    d.ellipse([40,38,50,46],fill=(240,140,110)); d.ellipse([124,38,134,46],fill=(240,140,110))
    up=ease((t-0.15)/0.25)                                          # the spatula rises into frame
    sy=int(lerp(H+30,10,up))
    d.line([170,sy+30,160,sy+8],fill=(150,100,50),width=3); d.rectangle([150,sy-6,170,sy+8],fill=(200,200,210),outline=(120,120,130))
    for k in range(3): d.line([154+k*5,sy-4,154+k*5,sy+6],fill=(150,150,160))
    if t>=0.4:                                                      # the shine
        for i,(sx,sy2) in enumerate(((52,12),(104,12),(176,sy-4))):
            s=2+((f+i)%4)
            d.line([sx-s,sy2,sx+s,sy2],fill=(255,255,255)); d.line([sx,sy2-s,sx,sy2+s],fill=(255,255,255))
    if t>=0.5:
        jx=(f%3)-1 if t<0.6 else 0
        big_text(im,"ORDER UP!",44,(255,255,255),scale=2,cx=W//2+jx,outline=(40,90,160))
    if t<0.08: zoom_lines(d,(255,255,255))
    return im

def title_card(t,f):
    """The narrator's card: 2000 YEARS LATER..."""
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        k=y/H; d.line([0,y,W,y],fill=(int(120+60*k),int(60+30*k),int(160-40*k)))
    for i in range(8):                                              # a starburst behind the words
        a=i*math.pi/4+t*0.6
        d.polygon([(W//2,H//2),(W//2+math.cos(a)*140,H//2+math.sin(a)*90),(W//2+math.cos(a+0.25)*140,H//2+math.sin(a+0.25)*90)],fill=(150,80,180))
    big_text(im,"2000 YEARS",14,(255,226,60),scale=3,outline=(140,60,20))
    big_text(im,"LATER...",38,(255,226,60),scale=2,outline=(140,60,20))
    return im

# ---- the clip --------------------------------------------------------------------------------------
HAND = hand_at(SB['charge'],CX,GROUND,False,15,5)                  # the spatula hand, at the grill

def flip_y(ph):
    """A patty tossed from the grill: height above it at phase ph (0..1)."""
    return PATTY[1]-int(22*math.sin(math.pi*ph))

def robot_x(f):
    if f<104: return VX
    if f<128: return ez(VX,RX,(f-104)/24)
    return RX

def clip_krabby(f):
    s=scene(f,THEME)
    cl=actor(SB[guard_pose(f)],CX,pal=SBPAL)
    pk=actor(pk_idle(f),VX,flip=True,pal=PKPAL)
    rb=None; extras=[]
    cooking=False
    # 1) I'M READY! I'M READY!
    if 8<=f<40:
        shout(s,"I'M READY! I'M READY!",(255,240,120))
        cl.update(spr=SB['armsup'],y=GROUND-int(5*abs(math.sin(math.pi*(f-8)/8))))
    # 2) flipping patties
    if 40<=f<190 and not (150<=f<182): cooking=True
    if 40<=f<88:
        ph=((f-40)%16)/16
        s['fx'].append(('sb_patty',PATTY[0],flip_y(ph)))
        s['fx'].append(('sb_spat',HAND[0],HAND[1],ph<0.25))
        if ph<0.1: s['fx'].append(('dmg','FLIP!',PATTY[0]-8,PATTY[1]-30,(255,255,255)))
    elif cooking: s['fx'].append(('sb_spat',HAND[0],HAND[1],False))
    if cooking: cl['spr']=SB['charge']
    # 3) Plankton climbs into his robot
    if 56<=f<80: shout(s,"THE FORMULA WILL BE MINE!",(120,220,100))
    if 72<=f<80: pk.update(y=GROUND-int(10*math.sin(math.pi*(f-72)/8)))
    if 80<=f<92:
        rb=actor(ROBOT['idle'],VX,int(ez(-4,GROUND,(f-80)/8)),flip=True,pal=ROBOTPAL); pk['vis']=False
    if f==88: s['shake']=rshake(3); s['fx'].append(('dust',VX-10,GROUND-1)); s['fx'].append(('dust',VX+10,GROUND-1))
    if 92<=f<200:
        x=robot_x(f); step=104<=f<128 and (f//6)%2==0
        rb=actor(ROBOT['step'] if step else ROBOT['idle'],x,GROUND,flip=True,pal=ROBOTPAL); pk['vis']=False
        if 104<=f<128 and f%6==0: s['shake']=rshake(); s['fx'].append(('dust',x,GROUND-1))
    if 92<=f<104: shout(s,"HEH HEH HEH!",(120,220,100))
    # 4) the claw swings: SpongeBob hops it and keeps cooking; patties fly into the robot
    for f0 in (128,152):
        if f0<=f<f0+8: rb['spr']=ROBOT['attack']
        if f0+2<=f<f0+8: cl['y']=GROUND-int(10*math.sin(math.pi*(f-f0-2)/6))
        if f==f0+4: s['fx'].append(('spark',CX+8,GROUND-6,4))
    for f0 in (112,136,160):
        if f0<=f<f0+10:
            t=(f-f0)/10; px=lerp(PATTY[0],RX-6,t); py=PATTY[1]-int(18*math.sin(math.pi*t))-int(t*10)
            s['fx'].append(('sb_patty',px,py))
            if f<f0+3: s['fx'].append(('sb_spat',HAND[0],HAND[1],True))
        if f==f0+10: s['fx'].append(('spark',RX-6,GROUND-21,5)); s['shake']=rshake()
        if f0+10<=f<f0+18: s['fx'].append(('dmg','SPLAT!',RX-14,GROUND-34-(f-f0-10)//2,(255,200,120)))
    # 5) Squidward at the porthole-door, Mr. Krabs bursts out
    if 116<=f<136:
        extras.append(actor(SQUID,DOOR,GROUND-3,pal=SQUIDPAL))
        if f>=120: shout(s,"UGH.",(150,200,190))
    if 138<=f<152:
        extras.append(actor(KRABS_UP if (f//3)%2 else KRABS,DOOR,GROUND-3,pal=KRABSPAL))
        shout(s,"MONEY! MONEY! MONEY!",(255,120,90))
    # 6) close-up: ORDER UP!
    if 168<=f<200:
        s['image']=closeup_order((f-168)/32,f); return s
    # 7) the last patty into the cockpit; the robot falls apart, Plankton flies home
    if 200<=f<208:
        t=(f-200)/8; px=lerp(PATTY[0],RX,t); py=lerp(PATTY[1],GROUND-17,t)-int(10*math.sin(math.pi*t))
        s['fx'].append(('sb_patty',px,py)); cl['spr']=SB['punch']
        rb=actor(ROBOT['idle'],RX,GROUND,flip=True,pal=ROBOTPAL); pk['vis']=False
    if f==208: s['flash']=0.6; s['fc']=(RX,GROUND-17); s['flashc']=(255,240,200); s['shake']=rshake(3)
    if 208<=f<222:
        t=f-208; rr=random.Random(zlib.crc32(b'robot')+t)
        for j in range(12):
            a=j*math.tau/12; s['fx'].append(('shard',RX+math.cos(a)*t*4,GROUND-14+math.sin(a)*t*2+t*t*0.25,(110,140,120)))
        for j in range(5): s['fx'].append(('smoke',RX-6+j*3,GROUND-6-t-j%2*3,2+t//4,(90,96,100)))
        u=t/14; pk.update(vis=True,spr=rotate90(PK['idle'],(f//2)%4),x=lerp(RX,176,u),y=int(lerp(GROUND-20,30,u)-14*math.sin(math.pi*u)))
        shout(s,"I'LL GET YOU NEXT TIME!",(120,220,100))
    if 222<=f<228: pk['vis']=False; shout(s,"I'LL GET YOU NEXT TIME!",(120,220,100))
    if 212<=f<228: cl['spr']=SB['armsup']
    # 8) the bubble wipe, the title card, Plankton trudges back
    if 226<=f<240: s['fx'].append(('sb_bubbles',(f-226)/28))
    if 233<=f<249:
        s['image']=title_card((f-233)/16,f)
        ImageDraw.Draw(s['image'])
        return s
    if 249<=f<256: s['fx'].append(('sb_bubbles',0.5+(f-249)/14))
    if 228<=f<276:
        u=(f-252)/20; pk.update(vis=True,spr=pk_idle(f),x=ez(178,VX,u) if f>=252 else 178,y=GROUND)
        if f<252: pk['vis']=False
        if 256<=f<272: shout(s,"SIGH...",(120,220,100))
    s['actors']=extras+[pk]+([rb] if rb else [])+[cl]
    return s

CLIPS = [clip('krabby', N_, clip_krabby)]
