"""Foster's Home for Imaginary Friends, no fight: Claude is the new imaginary friend in the
mansion's grand hall (the staircase, gilt portraits, the chandelier, the red carpet). Bloo, the
blue blob, pulls out his paddle ball: BET YOU CANT BEAT THIS! Both play, the counters climb
while the house goes by: Eduardo trembles past (NO ME GUSTA!), Coco lays a plastic egg (COCO!),
Wilt bumps into the banister (SORRY!). Bloo's ball snaps off the string, ricochets round the
hall and smashes the vase; Bloo points at Claude (HE DID IT!). Close-up: Mr. Herriman's monocle,
MASTER CLAUDE! RULE 37! Claude keeps going and wins 99 to 98 (NO FAIR!), Frankie sweeps up the
pieces with a sigh and puts a new vase out; Bloo ties his ball back on."""
import zlib
from engine import *

THEME = 'foster'
N_ = 293
CX, VX = 30, 150                                                   # the neutral pose: Claude, Bloo
VASE = 96                                                          # the vase on its pedestal
PERIOD = 6                                                         # frames per paddle-ball hit

# ---- Bloo: the blue capsule, big eyes, a stub arm for the paddle -------------------------------
_BLOO=S([
"...bbbbbb...",
"..bbbbbbbb..",
".bbbWWbWWbb.",
".bbbWKbWKbb.",
".bbbWKbWKbb.",
".bbbbbbbbbb.",
".bbbbbbbbbbb",
".bbbbbbbbbbb",
".bbbbbbbbbb.",
".bbbbbbbbbb.",
".bbbbbbbbbb.",
"..bbbbbbbb..",])
_BLOO2=S(["............"]+_BLOO[:-2]+[".bbbbbbbbbb.","..bbbbbbbb.."])     # squashes a pixel
_BLOO_POINT=S([r+('bbb' if i in (6,7) else '...') for i,r in enumerate(_BLOO)])
_BLOO_SULK=S([r.replace('WK','KW') if i in (3,4) else r for i,r in enumerate(_BLOO)][:2]+
             [".bbbbbbbbbb.",".bbKKbbKKbb.",".bbbbbbbbbb."]+_BLOO[5:])
BLOO={'idle':_BLOO,'idle2':_BLOO2,'point':_BLOO_POINT,'sulk':_BLOO_SULK}
BLOOPAL={'b':(70,130,230),'W':(250,250,255),'K':(16,16,30)}
def bloo_idle(f): return BLOO['idle'] if (f//6)%2==0 else BLOO['idle2']

# ---- the housemates ----------------------------------------------------------------------------
_EDU=S([   # Eduardo: big purple fur, horns, a shaking snout
"..h..............h..",
"..hh............hh..",
"...hh..pppppp..hh...",
"....hpppppppppph....",
"....ppWKppppWKpp....",
"....pppppppppppp....",
"...ppppPPPPPPpppp...",
"...pppPPPPPPPPppp...",
"..ppppPPKKKKPPpppp..",
"..ppppPPPPPPPPpppp..",
".pppppppppppppppppp.",
"pppppppppppppppppppp",
"pp.pppppppppppppp.pp",
"pp.pppppppppppppp.pp",
"pp.pppppppppppppp.pp",
"PP.pppppppppppppp.PP",
"...pppppppppppppp...",
"...pppppppppppppp...",
"...pppp......pppp...",
"...pppp......pppp...",
"..PPPPP......PPPPP..",])
EDUPAL={'p':(150,96,180),'P':(110,64,140),'h':(236,226,200),'W':(250,250,250),'K':(20,16,24)}

_COCO=S([  # Coco: palm-tree head, bird body, plane wings
"..g...g...g...",
"...g..g..g....",
"gg..ggggg..gg.",
"..gggggggggg..",
"....ttttt.....",
"....tWKtt.....",
"....tttttyy...",
"..ccctttttc...",
"DDDDDcccccDDDD",
".DDDDcccccDDD.",
"....ccccccc...",
"....ccccccc...",
".....ccccc....",
".....y...y....",
"....yy...yy...",])
COCOPAL={'g':(60,170,70),'t':(150,110,60),'c':(110,200,90),'D':(200,200,210),'y':(250,200,50),
         'W':(250,250,250),'K':(20,16,24)}

_WILT=S([  # Wilt: very tall, red, one arm, a bent eye stalk
".W.....",
".KWW...",
"..WW...",
"..rrr..",
".rrrrr.",
".rWKrr.",
".rrrrr.",
".rrkkr.",
"..rrr..",
"..rrr..",
".rrrrr.",
".rrrrrr",
".rrrrr.r",
".rrrrr.r",
".rrrrr.r",
".rrrrr.W",
".rrrrr..",
"..rrr...",
"..rrr...",
"..r.r...",
"..r.r...",
"..r.r...",
"..r.r...",
"..r.r...",
"..r.r...",
".kk.kk..",])
WILTPAL={'r':(220,60,50),'W':(250,250,250),'K':(20,16,24),'k':(60,60,70)}

_FRANK=S([  # Frankie: red ponytail, green top, jeans
"...RRRR....",
"..RRRRRR...",
"..RsssRRRR.",
"..sKssKRRRR",
"..sssss..RR",
"...sss....R",
"..GGGGG....",
".GGGGGGG...",
".sGGGGGs...",
".sGGGGGs...",
"..GGGGG....",
"..JJJJJ....",
"..JJ.JJ....",
"..JJ.JJ....",
"..JJ.JJ....",
"..JJ.JJ....",
".kkk.kkk...",])
FRANKPAL={'R':(210,70,40),'s':(250,214,180),'K':(20,16,24),'G':(90,190,90),'J':(70,100,170),'k':(40,30,30)}
_FRANK2=S(_FRANK[:12]+["..JJ.JJ....","..JJ..JJ...",".JJ....JJ..",".JJ....JJ..","kkk....kkk."])

# ---- the hall -----------------------------------------------------------------------------------
def _hall(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(58+14*k),int(28+8*k),int(40+8*k)))
    for x in range(0,W,6): d.line([x,10,x,GROUND-8],fill=(70,36,50))   # striped wallpaper
    d.rectangle([0,GROUND-8,W,GROUND],fill=(84,52,40))                 # wainscot
    d.line([0,GROUND-8,W,GROUND-8],fill=(140,96,60))
    for x in range(4,W,12): d.rectangle([x,GROUND-6,x+8,GROUND-2],outline=(104,66,48))
    d.rectangle([0,0,W,9],fill=(44,22,32)); d.line([0,9,W,9],fill=(170,130,60))   # cornice
    # the grand staircase, rising to the right in the back
    for i in range(10):
        x=118+i*6; y=GROUND-8-i*4
        d.rectangle([x,y,x+6,GROUND-8],fill=(96,58,44)); d.line([x,y,x+6,y],fill=(160,40,50))
    d.line([118,GROUND-18,178,GROUND-58],fill=(200,160,90))         # banister
    for i in range(0,10,2): d.line([120+i*6,GROUND-18-i*4,120+i*6,GROUND-10-i*4],fill=(200,160,90))
    for x,y,c in ((22,16,(90,110,160)),(52,14,(150,110,90)),(84,18,(90,140,110))):  # gilt portraits
        d.rectangle([x,y,x+12,y+14],fill=(200,160,60)); d.rectangle([x+2,y+2,x+10,y+12],fill=c)
        d.ellipse([x+4,y+3,x+8,y+7],fill=(240,210,180)); d.rectangle([x+3,y+8,x+9,y+12],fill=(60,40,50))
    d.line([66,0,66,4],fill=(200,160,60))                            # the chandelier
    d.arc([58,3,74,10],0,180,fill=(220,180,80))
    for x in (59,63,66,69,73): d.point((x,6),fill=(255,240,180))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(150,30,40))              # the red carpet
register_bg(THEME, lambda v: (v+40,v//4+6,v//3+10), decor=_hall)

# ---- effects -----------------------------------------------------------------------------------
@fx('fos_vase')
def _fx_vase(d,im,e,f):
    """The pedestal and the vase on it (whole, or gone)."""
    _,x,whole=e
    d.rectangle([x-3,GROUND-12,x+3,GROUND],fill=(220,210,190)); d.rectangle([x-4,GROUND-13,x+4,GROUND-12],fill=(240,232,214))
    if whole:
        d.ellipse([x-3,GROUND-21,x+3,GROUND-14],fill=(70,120,200)); d.rectangle([x-1,GROUND-24,x+1,GROUND-20],fill=(70,120,200))
        d.line([x-2,GROUND-18,x+2,GROUND-18],fill=(250,220,90)); d.rectangle([x-2,GROUND-25,x+2,GROUND-24],fill=(70,120,200))

@fx('fos_shards')
def _fx_shards(d,im,e,f):
    """The vase's pieces: flying at t<8, then lying on the carpet; n of them left."""
    _,x,t,n=e; rr=random.Random(zlib.crc32(b'vase'))
    for j in range(10):
        vx=rr.uniform(-2.2,2.2); vy=rr.uniform(-2.5,-0.5); rest=x+rr.randint(-14,14)
        if j>=n: continue
        if t<8: px,py=x+vx*t,GROUND-20+vy*t+0.35*t*t; py=min(py,GROUND-1)
        else: px,py=rest,GROUND-1
        d.rectangle([px,py,px+1,py],fill=(70,120,200) if j%3 else (250,220,90))

@fx('fos_paddle')
def _fx_paddle(d,im,e,f):
    """A paddle at (x,y) and its ball on the string, h px up (h<0: no ball, the string cut)."""
    _,x,y,h=e; x,y=int(x),int(y)
    d.rectangle([x,y,x,y+3],fill=(150,100,50))                       # handle
    d.ellipse([x-3,y-4,x+3,y],fill=(220,50,50),outline=(140,20,30))
    if h>=0:
        by=y-4-int(h); d.line([x,y-3,x,by],fill=(230,230,230)); d.rectangle([x-1,by-1,x,by],fill=(255,80,80))

@fx('fos_ball')
def _fx_ball(d,im,e,f):
    _,x,y=e; d.rectangle([int(x)-1,int(y)-1,int(x),int(y)],fill=(255,80,80))

@fx('fos_broom')
def _fx_broom(d,im,e,f):
    _,x,ang=e
    tx,ty=x+int(6*math.sin(ang)),GROUND-1
    d.line([x,GROUND-16,tx,ty-3],fill=(170,120,60))
    d.polygon([(tx-3,ty),(tx+3,ty),(tx+2,ty-4),(tx-2,ty-4)],fill=(230,200,100))

@fx('fos_egg')
def _fx_egg(d,im,e,f):
    _,x,y=e; d.ellipse([x-2,y-3,x+2,y+1],fill=(250,240,200),outline=(200,160,90))

def shout(s,txt,c,y=2,x=None):
    s['fx'].append(('dmg',txt,(W//2 if x is None else x)-len(txt)*2,y,c))

# ---- the paddle-ball contest -------------------------------------------------------------------
P0=20                                                              # the first hit
BREAK=124                                                          # Bloo's string snaps
def hits(f,f0=P0): return max(0,(f-f0)//PERIOD)
def ball_h(f): return 9*math.sin(math.pi*((f-P0)%PERIOD)/PERIOD)
def bloo_score(f): return min(98,81+hits(min(f,BREAK)))           # stuck at 98 once the string snaps
def cl_score(f):
    if f<204: return min(98,81+hits(f))
    return 99                                                      # the winning hit

# the loose ball's ricochet: straight segments between bounce points, then the vase
_RICO=[(BREAK,(VX-8,GROUND-26)),(BREAK+3,(176,10)),(BREAK+6,(120,2)),(BREAK+9,(60,40)),
       (BREAK+12,(30,4)),(BREAK+16,(VASE,GROUND-20))]
def rico(f):
    for (f0,p0),(f1,p1) in zip(_RICO,_RICO[1:]):
        if f0<=f<f1: t=(f-f0)/(f1-f0); return lerp(p0[0],p1[0],t),lerp(p0[1],p1[1],t)
    return None
CRASH=_RICO[-1][0]

# ---- close-up: Mr. Herriman ---------------------------------------------------------------------
def closeup_herriman(t,f):
    im=Image.new('RGB',(W,H),(90,40,56)); d=ImageDraw.Draw(im)
    for x in range(0,W,8): d.line([x,0,x,H],fill=(104,48,64))
    cx=92; jx=(f%2) if 0.3<=t<0.5 else 0; cx+=jx
    grey,dark,pink=(196,196,206),(140,140,152),(236,170,180)
    for ex in (-14,8):                                              # the long ears
        d.polygon([(cx+ex,24),(cx+ex+6,24),(cx+ex+8,-10),(cx+ex+1,-14)],fill=grey)
        d.polygon([(cx+ex+2,22),(cx+ex+5,22),(cx+ex+6,-6),(cx+ex+3,-9)],fill=pink)
    d.ellipse([cx-22,16,cx+22,62],fill=grey)                         # the head
    d.ellipse([cx-12,40,cx+12,58],fill=(236,236,240))                # the muzzle
    d.ellipse([cx-3,40,cx+3,45],fill=pink)                           # the nose
    for s in (-1,1):                                                 # whiskers
        for k in (-2,1,4): d.line([cx+s*8,47+k//2,cx+s*30,44+k*2],fill=(240,240,240))
    d.ellipse([cx-13,28,cx-5,36],fill=(250,250,250)); d.ellipse([cx-10,30,cx-6,35],fill=(20,16,24))
    d.ellipse([cx+4,26,cx+16,38],fill=(250,250,250)); d.ellipse([cx+7,29,cx+12,35],fill=(20,16,24))
    d.ellipse([cx+2,24,cx+18,40],outline=(230,190,70),width=2)      # the monocle and its chain
    d.line([cx+18,34,cx+26,58],fill=(230,190,70))
    glint=0.12<=t<0.2
    if glint: d.line([cx+6,27,cx+10,27],fill=(255,255,255)); d.point((cx+14,31),fill=(255,255,255))
    d.line([cx-16,25,cx-4,27],fill=dark,width=2); d.line([cx+4,23,cx+16,21],fill=dark,width=2)  # stern brows
    d.rectangle([cx-26,58,cx+26,H],fill=(40,40,60))                  # the tailcoat collar
    d.polygon([(cx-6,58),(cx,64),(cx+6,58)],fill=(250,250,250))
    d.polygon([(cx-6,56),(cx-1,59),(cx-6,62)],fill=(200,30,40)); d.polygon([(cx+6,56),(cx+1,59),(cx+6,62)],fill=(200,30,40))
    if t<0.06: zoom_lines(d,(255,230,200))
    if t>=0.2: big_text(im,"MASTER CLAUDE!",3,(255,255,255),cx=W//2+jx,outline=(120,30,40))
    if t>=0.5:
        big_text(im,"RULE 37!",22,(255,220,90),cx=36,outline=(120,30,40))
        text(d,"NO BALLS",8,42,(255,255,255)); text(d,"IN THE HALL.",8,49,(255,255,255))
    return im

# ---- the clip ----------------------------------------------------------------------------------
def clip_bloo(f):
    s=scene(f,THEME)
    cl=actor(CL[guard_pose(f)],CX)
    bl=actor(bloo_idle(f),VX,flip=True,pal=BLOOPAL)
    extra=[]
    vase_whole=f<CRASH or f>=252
    s['under'].append(('fos_vase',VASE,vase_whole))
    # 1) the challenge
    if 8<=f<30: shout(s,"BET YOU CANT BEAT THIS!",(140,190,255))
    if 14<=f<P0: s['fx'].append(('fos_paddle',VX-6,GROUND-8,0))
    if 20<=f<P0+6: shout(s,"YOU'RE ON.",(255,200,170),y=10,x=CX+6)
    # 2) both play: the paddles, the balls, the counters
    playing=P0<=f<236
    if playing:
        cl['spr']=CL['charge']
        hx,hy=hand_at(CL['charge'],CX,GROUND,False,15,5)
        s['fx'].append(('fos_paddle',hx+1,hy,ball_h(f) if f<228 else 0))
        s['fx'].append(('dmg',str(cl_score(f)),CX-4,GROUND-26,(255,220,150) if f<204 else (255,255,120)))
    if P0<=f<BREAK:
        s['fx'].append(('fos_paddle',VX-8,GROUND-8,ball_h(f+3)))
    if P0<=f<236:
        s['fx'].append(('dmg',str(bloo_score(f)),VX-4,GROUND-26,(150,200,255)))
    # 3) the housemates go by
    if 40<=f<80:                                                      # Eduardo, trembling, left to right
        t=(f-40)/40; extra.append(actor(_EDU,int(lerp(-14,200,t))+((f//2)%2),pal=EDUPAL))
        if 48<=f<70: shout(s,"NO ME GUSTA!",(200,160,240),y=10)
    if 64<=f<108:                                                     # Coco hops in, lays an egg, leaves
        x=int(ez(200,112,(f-64)/12)) if f<92 else int(ez(112,-20,(f-92)/16))
        y=GROUND-(abs(int(4*math.sin(f*0.6))) if f<76 or f>=92 else 0)
        extra.append(actor(_COCO,x,y,flip=f<92,pal=COCOPAL))
        if 78<=f<92: shout(s,"COCO! COCO!",(140,230,120),y=10)
    if 84<=f<236: s['under'].append(('fos_egg',112,GROUND-1) if f<200 else ('fos_egg',int(ez(112,190,(f-200)/16)),GROUND-1))
    if 96<=f<126:                                                     # Wilt, bumping the banister
        x=int(lerp(-6,124,(f-96)/22)) if f<118 else 124
        extra.append(actor(_WILT,x,pal=WILTPAL))
        if f==118: s['shake']=rshake()
        if 116<=f<126: shout(s,"SORRY! SORRY!",(255,140,120),y=10)
    if 126<=f<140: extra.append(actor(_WILT,int(ez(124,200,(f-126)/14)),pal=WILTPAL))
    # 4) the string snaps, the ball ricochets, CRASH
    if f==BREAK: s['fx'].append(('spark',VX-8,GROUND-24,3))
    if BREAK<=f<CRASH+6: s['fx'].append(('fos_paddle',VX-8,GROUND-8,-1))
    p=rico(f)
    if p:
        s['fx'].append(('fos_ball',*p))
        for k in (1,2):
            q=rico(f-k)
            if q: s['fx'].append(('mote',q[0],q[1],(255,160,160)))
        if f in [g for g,_ in _RICO[1:-1]]: s['fx'].append(('spark',int(p[0]),int(p[1]),2))
    if f==CRASH: s['shake']=rshake(2); s['flash']=0.3; s['fc']=(VASE,GROUND-20); s['flashc']=(200,220,255)
    if CRASH<=f<CRASH+8: s['fx'].append(('big',"CRASH!",14,(200,220,255),VASE))
    nshard=10 if f<230 else max(0,10-(f-230)//2)
    if CRASH<=f<252: s['under'].append(('fos_shards',VASE,f-CRASH,nshard))
    # 5) Bloo points at Claude
    if CRASH+8<=f<CRASH+18:
        bl['spr']=BLOO['point']; shout(s,"HE DID IT!",(140,190,255))
    # 6) the close-up
    if 158<=f<190: s['image']=closeup_herriman((f-158)/32,f); return s
    # 7) Claude wins 99 to 98
    if 190<=f<236 and f>=BREAK: bl['spr']=BLOO['sulk'] if f>=206 else bloo_idle(f)
    if 206<=f<226:
        shout(s,"99 TO 98!",(255,255,120)); s['fx'].append(('dmg',"NO FAIR!",VX-16,GROUND-34,(140,190,255)))
    if 204<=f<214: s['fx'].append(('twinkle',CX,GROUND-30,2+(f%2)))
    if 228<=f<236: cl['spr']=CL['armsup']
    # 8) Frankie sweeps up and brings a new vase
    if 222<=f<262:
        if f<230: fx_,fr=int(ez(-10,VASE-14,(f-222)/8)),_FRANK2 if (f//3)%2 else _FRANK
        elif f<250: fx_,fr=VASE-14+((f//4)%2)*2,_FRANK
        else: fx_,fr=int(ez(VASE-14,-12,(f-250)/12)),_FRANK2 if (f//3)%2 else _FRANK
        extra.append(actor(fr,fx_,pal=FRANKPAL))
        if 230<=f<250: s['fx'].append(('fos_broom',fx_+5,math.sin(f*0.8)))
        if 236<=f<250: shout(s,"SIGH...",(255,170,120),y=10,x=fx_+4)
    # 9) Bloo ties his ball back on
    if 236<=f<256: bl['spr']=bloo_idle(f)
    if 244<=f<258: shout(s,"REMATCH!",(140,190,255),y=2)
    s['actors']=extra+[bl,cl]
    return s

CLIPS = [clip('bloo', N_, clip_bloo)]
