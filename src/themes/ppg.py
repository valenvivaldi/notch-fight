"""The Powerpuff Girls: Claude is the fourth Powerpuff (big shiny eyes, the black stripe of the
dress) vs Mojo Jojo, the green chimp with the giant brain under the white helmet and the purple
cape, over Townsville at dusk. "I, MOJO JOJO, SHALL DESTROY YOU!": the ray gun fires, Claude takes
off on an orange streak and lands a flying punch; the second shot knocks Claude out of the sky.
Three streaks dive in — pink, blue, green: Blossom, Bubbles, Buttercup — and hit Mojo one after
another; Claude charges and the POW sends Mojo into orbit. THE DAY IS SAVED! The girls streak away,
Mojo crashes back onto his spot, dizzy, and gets up."""
import zlib
from engine import *

THEME = 'ppg'
N_ = 257
CX, VX = 30, 150                                                   # the neutral pose: Claude, Mojo
SKY = 26                                                           # hover height (feet)

# ---- the Powerpuffs: Claude's body with the big shiny eyes and the black stripe of the dress ----
def _puff(spr):
    t,l,r=body_box(spr); g=grid(spr)
    for y in range(len(g)):
        for x in range(1,len(g[0])):
            if g[y][x]=='K' and g[y][x-1]=='O':                    # each eye one pixel wider, a shine on top
                g[y][x-1]='W' if y>0 and g[y-1][x]!='K' else 'K'
    if t+6<len(g):
        for x in range(l,r+1):
            if g[t+6][x]=='O': g[t+6][x]='k'                        # the black stripe
    return ungrid(g)
PUFF=variant(_puff)
CLPAL={'W':(255,255,255),'k':(26,24,30)}

def _girl(pat,dx,bangs):
    return {k:overlay(v,pat,dx,0,bangs=bangs) for k,v in PUFF.items()}
BLOSSOM=_girl([".rrr..rrr.","..rrrrrr..",".xxxxxxxx.","xxxxxxxxxx"],-1,"xxx..xxx")
BUBBLES=_girl(["yy........yy","yyy.yyyy.yyy"],-2,"yyy..yyy")
BUTTERCUP=_girl([".kkkkkkkk.","kkkkkkkkkk"],-1,"kkkk.kkk")
GIRLS=[  # sprites, palette, streak colour
 (BLOSSOM,  dict(CLPAL,O=(246,140,190),o=(200,90,140),x=(214,96,40),r=(220,30,50)),(255,120,190)),
 (BUBBLES,  dict(CLPAL,O=(120,196,250),o=(70,140,210),y=(250,226,90)),(110,190,255)),
 (BUTTERCUP,dict(CLPAL,O=(120,210,110),o=(70,150,70)),(110,230,100)),
]
CL_TRAIL=(255,150,90)

# ---- Mojo Jojo ---------------------------------------------------------------------------------
_MJ=S([
"......HHHHHH......",
"....HHHHHHHHHH....",
"...HHHHHHHHHHHH...",
"...HHHHHHHHHHHH...",
"...nnCnnnCnnnCn...",
"...nnnnCnnnCnnn...",
"....GGGGGGGGGG....",
"....GGYYKGGYYK....",
"....GGYYKGGYYK....",
"....GGGGGGGGGG....",
".....GgKKKKKg.....",
".....GgWKWKWg.....",
"......GGGGGG......",
"..VVVVHHHHHHVVVV..",
".VVVVLLLLLLLLVVVV.",
".VVV.LLLLLLLL.VVV.",
".VV.HLLLLLLLLH.VV.",
".VV..LLLLLLLL..VV.",
".VVV.LLLLLLLL.VVV.",
"..VV.LLL..LLL.VV..",
"..V..LLL..LLL..V..",
".....LLL..LLL.....",
"....HHHH..HHHH....",])
_MJ2=S(_MJ[:15]+[r.replace('.VV.','VV..',1) if i%2 else r for i,r in enumerate(_MJ[15:])])   # the cape sways
MJ=poses(_MJ,15,'H',2)
MJ['shoot']=paint(MJ['attack'],[(19,15,'DDDD'),(19,16,'Dd..'),(23,15,'r')],right=5)  # the ray gun
MJ['idle2']=_MJ2
MJ['down']=rotate90(MJ['hurt'],3,trim=True)
MJPAL={'H':(236,236,244),'n':(236,150,170),'C':(196,90,120),'G':(118,170,76),'g':(70,118,50),
       'Y':(250,220,70),'K':(20,16,16),'W':(250,250,250),'V':(120,60,160),'L':(46,48,110),
       'D':(150,150,166),'d':(90,90,104),'r':(255,60,60)}
GUN=hand_at(MJ['shoot'],VX,GROUND,True,23,15)                      # the muzzle, Mojo facing left
def mj_idle(f): return MJ['idle'] if (f//6)%2==0 else MJ['idle2']

# ---- background: Townsville at dusk ------------------------------------------------------------
def _townsville(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(40+30*k),int(16+12*k),int(60+10*k)))
    rr=random.Random(zlib.crc32(b'townsville'))
    for _ in range(18): d.point((rr.randint(0,W-1),rr.randint(0,22)),fill=(150,120,180))
    for x,w,h in ((0,14,22),(16,10,30),(28,16,18),(46,8,26),(56,14,14),(124,12,24),(138,18,32),
                  (158,10,20),(170,15,27)):                        # the skyline
        d.rectangle([x,GROUND-h,x+w,GROUND],fill=(30,18,44))
        for wy in range(GROUND-h+3,GROUND-3,4):
            for wx in range(x+2,x+w-1,3):
                if rr.random()<0.45: d.point((wx,wy),fill=(250,200,110))
    d.rectangle([76,GROUND-14,110,GROUND],fill=(36,22,50))         # City Hall: columns and the dome
    for x in range(78,110,5): d.line([x,GROUND-12,x,GROUND],fill=(54,36,70))
    d.polygon([(74,GROUND-14),(93,GROUND-20),(112,GROUND-14)],fill=(36,22,50))
    d.pieslice([85,GROUND-30,101,GROUND-14],180,360,fill=(36,22,50))
    d.line([93,GROUND-36,93,GROUND-30],fill=(36,22,50))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(28,18,36))
register_bg(THEME, lambda v: (v+20,v//2+8,v+16), decor=_townsville)

# ---- effects -----------------------------------------------------------------------------------
@fx('ppg_trail')
def _fx_trail(d,im,e,f):
    """A Powerpuff streak: the thick coloured light trail behind a flier (pts: newest first)."""
    _,pts,c=e
    hi=tuple(min(255,v+90) for v in c)
    for i in range(len(pts)-1):
        (x0,y0),(x1,y1)=pts[i],pts[i+1]
        w=max(1,4-i*4//len(pts))
        d.line([x0,y0,x1,y1],fill=c,width=w)
        if i<len(pts)//2: d.line([x0,y0,x1,y1],fill=hi)

@fx('ppg_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

@fx('ppg_ray')
def _fx_ray(d,im,e,f):
    """Mojo's ray: a diagonal green beam."""
    _,x0,y0,x1,y1=e
    d.line([x0,y0,x1,y1],fill=(80,200,80),width=4+f%2); d.line([x0,y0,x1,y1],fill=(220,255,200),width=1)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('ppg_say',txt,y,c,scale,outline))

# ---- the fliers: (x, feet, pose, streak?) per frame; the trail samples the last frames ----------
def cl_at(f):
    if 40<=f<48: return CX,ez(GROUND,SKY,(f-40)/8),'armsup',True                 # takes off
    if 48<=f<58:                                                                # dives at Mojo
        t=(f-48)/10; return lerp(CX,VX-16,t),lerp(SKY,GROUND,t)-8*math.sin(math.pi*t),'dash',True
    if 58<=f<64: return VX-16,GROUND,'punch',False
    if 64<=f<74:
        t=(f-64)/10; return lerp(VX-16,96,t),lerp(GROUND,SKY+4,ease(t)),'armsup',True
    if 74<=f<80: return 96,SKY+4+(f//3)%2,guard_pose(f),False                    # hovers
    if 80<=f<94:                                                                # shot down
        t=(f-80)/14; return lerp(96,CX,t),lerp(SKY+4,GROUND,t*t),'hurt',False
    if 94<=f<104: return CX,GROUND,'hurt',False
    if 152<=f<160: return CX,GROUND,'charge',False
    if 160<=f<166:
        t=(f-160)/6; return lerp(CX,VX-16,t),GROUND-4*math.sin(math.pi*t),'dash',True
    if 166<=f<176: return VX-16,GROUND,'punch',False
    if 176<=f<190:
        t=(f-176)/14; return lerp(VX-16,CX,ease(t)),GROUND-10*math.sin(math.pi*t),'armsup',t<0.9
    return CX,GROUND,guard_pose(f),False

GX=[50,64,78]                                                       # where the girls land
def girl_at(i,f):
    """Girl i: dives in, waits, hits Mojo, hovers in formation, streaks away."""
    t0=96+i*4
    if f<t0: return None
    if f<t0+8:
        t=(f-t0)/8; return lerp(-10+i*20,GX[i],t),lerp(-4,GROUND,ease(t)),'dash',True
    h0=122+i*10                                                    # her hit
    if f<h0: return GX[i],GROUND,guard_pose(f+i*3),False
    if f<h0+4:
        t=(f-h0)/4; return lerp(GX[i],VX-16,t),GROUND-3*math.sin(math.pi*t),'dash',True
    if f<h0+7: return VX-16,GROUND,'punch',False
    hx,hy=60+i*16,SKY-4-(i==1)*4                                    # the formation, above
    if f<h0+15:
        t=(f-h0-7)/8; return lerp(VX-16,hx,ease(t)),lerp(GROUND,hy,ease(t)),'armsup',True
    if f<184: return hx,hy+((f+i*2)//4)%2,guard_pose(f),False
    if f<196:
        t=(f-184)/12; return lerp(hx,hx+30+i*20,t),lerp(hy,-20,t),'armsup',True
    return None

def _trail(s,at,f,c,n=7):
    pts=[]
    for k in range(n):
        p=at(f-k)
        if p is None or not p[3]: break
        pts.append((p[0],p[1]-5))
    if len(pts)>1: s['under'].append(('ppg_trail',pts,c))

# ---- the clip ----------------------------------------------------------------------------------
def clip_townsville(f):
    s=scene(f,THEME)
    x,y,pose,_=cl_at(f)
    cl=actor(PUFF[pose],x,int(y),pal=CLPAL)
    mj=actor(mj_idle(f),VX,flip=True,pal=MJPAL)
    _trail(s,cl_at,f,CL_TRAIL)
    girls=[]
    for i,(spr,pal,c) in enumerate(GIRLS):
        p=girl_at(i,f)
        if p is None: continue
        _trail(s,lambda g,i=i: girl_at(i,g),f,c)
        girls.append(actor(spr[p[2]],p[0],int(p[1]),pal=pal))
    # 1) the narrator, Mojo's speech
    if 6<=f<22: shout(s,"THE CITY OF TOWNSVILLE!",(255,200,230))
    if 22<=f<44: shout(s,"I, MOJO JOJO, SHALL DESTROY YOU!",(140,230,110))
    # 2) the first shot misses: Claude takes off
    if 30<=f<50: mj['spr']=MJ['shoot']
    if 38<=f<40: s['fx'].append(('spark',GUN[0],GUN[1],3))
    if 40<=f<48: s['fx'].append(('beam',0,GUN[0],GUN[1],((80,200,80),(170,255,140))))
    if 40<=f<44: s['fx'].append(('dust',CX-3,GROUND-1)); s['fx'].append(('dust',CX+3,GROUND-1))
    # 3) the flying punch
    if f==58: s['fx'].append(('spark',VX-8,GROUND-12,7)); s['shake']=rshake(2)
    if 58<=f<70:
        mj.update(spr=MJ['hurt'],x=ez(VX,VX+8,(f-58)/4))
        s['fx'].append(('dmg','POW!',VX-8,GROUND-34-(f-58)//3,(255,230,120)))
    if 70<=f<78: mj['x']=ez(VX+8,VX,(f-70)/8)
    # 4) the second shot knocks Claude out of the sky
    if 72<=f<84: mj['spr']=MJ['shoot']
    if 76<=f<82: s['fx'].append(('ppg_ray',GUN[0],GUN[1],96,SKY-1))
    if f==80: s['fx'].append(('spark',96,SKY-2,6)); s['shake']=rshake(2); s['flash']=0.35; s['fc']=(96,SKY-2); s['flashc']=(170,255,140)
    if 82<=f<96: shout(s,"MWA HA HA HA!",(140,230,110))
    if f==94: s['fx'].append(('dust',CX-4,GROUND-1)); s['fx'].append(('dust',CX+4,GROUND-1)); s['shake']=rshake()
    if 94<=f<104: s['fx'].append(('dizzy',CX,GROUND-14))
    # 5) the girls dive in
    if 104<=f<122: shout(s,"BLOSSOM! BUBBLES! BUTTERCUP!",(255,255,255))
    for i in range(3):
        if f==104+i*4: s['fx'].append(('dust',GX[i]-3,GROUND-1)); s['fx'].append(('dust',GX[i]+3,GROUND-1))
    # 6) one hit each
    for i in range(3):
        h=122+i*10+4
        if f==h: s['fx'].append(('spark',VX-8,GROUND-10-i*3,6)); s['shake']=rshake()
        if h<=f<h+6: s['fx'].append(('dmg',str(10+i*5),VX-6,GROUND-30-(f-h),GIRLS[i][2]))
    if 126<=f<160: mj.update(spr=MJ['hurt'],x=VX+((f-126)//10)*2)
    # 7) Claude charges up, the POW sends Mojo flying
    if 152<=f<160:
        cl['aura']=((255,170,110),1); shout(s,"HIYAAA!",CL_TRAIL)
    if 160<=f<166: mj.update(spr=MJ['hurt'],x=VX+6)
    if f==166: s['flash']=0.5; s['fc']=(VX-8,GROUND-12); s['flashc']=(255,230,200); s['shake']=rshake(3)
    if 166<=f<172:
        s['fx'].append(('spark',VX-8,GROUND-12,9)); banner(s,"POW!",14,(255,230,120),3,(160,40,30))
    if 166<=f<182:
        t=(f-166)/16; mj.update(spr=rotate90(MJ['hurt'],(f//2)%4),x=lerp(VX+6,200,t),y=int(lerp(GROUND,-20,t)))
    if 182<=f<204: mj['vis']=False
    if 166<=f<182 and f%4==0: s['fx'].append(('twinkle',min(182,int(lerp(VX+6,200,(f-166)/16))),max(2,int(lerp(GROUND,-20,(f-166)/16))),2))
    # 8) the day is saved
    if 184<=f<212:
        shout(s,"AND SO, ONCE AGAIN,",(255,220,240),y=8)
        banner(s,"THE DAY IS SAVED!",18,(255,255,255),2,(200,60,130))
    # 9) Mojo crashes back onto his spot
    if 204<=f<212: mj.update(vis=True,spr=MJ['hurt'],y=int(ez(-30,GROUND,(f-204)/8)))
    if f==212: s['fx'].append(('dust',VX-8,GROUND-1)); s['fx'].append(('dust',VX+8,GROUND-1)); s['shake']=rshake(2)
    if 212<=f<232:
        mj.update(spr=MJ['down'])
        s['fx'].append(('dizzy',VX,GROUND-10))
        if f>=216: shout(s,"CURSE YOU, POWERPUFF CLAUDE!",(140,230,110))
    if 232<=f<238: mj['spr']=MJ['hurt']
    s['actors']=[mj]+girls+[cl]
    return s

CLIPS = [clip('townsville', N_, clip_townsville)]
