"""JoJo's Bizarre Adventure: Stone Ocean (sub-theme of `jojo`). Claude is Jolyne (the two buns
and the braid, the green outfit with the spider web, the butterfly tattoo) with Stone Free, in
the yard of Green Dolphin Street prison at night (the wall, the sea behind it, a searchlight,
the fence). Pucci sends Whitesnake: it pulls a DISC out of Claude's head and Claude falls
asleep; Claude unravels into string and a thread pulls the disc back. Close-up: the tattooed
arm, the fingers coming undone into taut strings — STONE FREE! Then MADE IN HEAVEN: time
accelerates (the sun and the moon race across the sky, day and night flicker, the shadows spin)
and Pucci is a blur hitting from everywhere. Claude weaves a net of string across the yard, and
at that speed Pucci flies right into it. ORA ORA ORA, Pucci into the fence. YARE YARE DAWA.
Time is back to normal; Pucci gets up on his spot."""
import zlib
from engine import *
from themes.jojo import _stand, ST_A

THEME = 'jojo-stone'
N_ = 288
CX, VX = 30, 150
SKY_H = 30                                                         # the sky ends at the sea

# ---- Claude as Jolyne --------------------------------------------------------------------------
def _jolyne(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])
    top=max(bot-3,max(y for y in range(h) if 'K' in spr[y])+2)       # the outfit starts below the eyes
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and inside and y>=top: g[y][x]='g' if (x+y)%3==0 or (x-y)%4==0 else 'G'   # the web
            elif c=='o' and y>bot: g[y][x]='G'                                               # legs
            elif c=='o' and y==bot and inside: g[y][x]='G'
    arm=[(x,y) for y in range(h) for x in range(w) if g[y][x]=='o' and x>r]
    if arm: x,y=min(arm,key=lambda p:(p[1],p[0])); g[y][x]='T'                              # the tattoo
    s=ungrid(g)
    s=overlay(s,[".qq....qq.","qqqq..qqqq",".qqqqqqqq.","qqqyqqqqqq"],-1,0,bangs="qqyq..qq")
    t2,l2,_=body_box(s)
    return paint(s,[(l2-1,t2+1,'q'),(l2-1,t2+2,'y'),(l2-1,t2+3,'q'),(l2-1,t2+4,'y')])     # the braid
JOL=variant(_jolyne)
JOLPAL={'q':(58,40,34),'y':(232,196,84),'G':(84,168,96),'g':(30,84,44),'T':(110,60,170)}
SLEEP=rotate90(JOL['hurt'],3,trim=True)

STONE=_stand({'h':'E','E':'H','b':'L','c':'N','f':'E','a':'Y'},'LLLLEE')     # Stone Free
SNAKE=_stand({'h':'H','E':'r','b':'h','c':'b','f':'H','a':'d'},'hhhhHH')     # Whitesnake
HEAVEN=_stand({'h':'W','E':'g','b':'W','c':'y','f':'W','a':'g'},'WWWWWW')    # Made in Heaven
STRING=(110,180,255)
ORA_B=((110,180,255),(40,60,150))

# ---- Enrico Pucci ------------------------------------------------------------------------------
_PU=S([
".....hhhhh.....",
"....hhhhhhh....",
"....hhhhhhhh...",
"....httttttt...",
"....tttKtttK...",
"....tttttttt...",
".....ttttzt....",
".....tttttt....",
"......tttt.....",
"...kkkWWWkkk...",
"..kkkkkYkkkkk..",
"..kk.kYYYk.kk..",
"..kk.kkYkk.kk..",
"..tt.kkYkk.tt..",
".....kkkkk.....",
"....kkkvkkk....",
"....kkkvkkk....",
"....kkk.kkk....",
"....kkk.kkk....",
"....kkk.kkk....",
"...bbbb.bbbb...",])
PU=poses(_PU,10,'t',3)
PU['idle2']=S([_PU[0]]+_PU[:15]+_PU[16:])                         # breathes
PU['down']=rotate90(PU['hurt'],3,trim=True)
PUPAL={'h':(214,214,224),'t':(150,100,72),'K':(20,16,16),'z':(110,70,50),'k':(46,42,62),
       'W':(240,240,240),'Y':(236,196,72),'v':(90,84,120),'b':(20,20,24)}
def pu_idle(f): return PU['idle'] if (f//6)%2==0 else PU['idle2']

# ---- background: Green Dolphin Street prison yard at night -------------------------------------
NIGHT_TOP,NIGHT_BOT=(8,10,30),(30,34,70)
def _sky(d,top=NIGHT_TOP,bot=NIGHT_BOT):
    for y in range(SKY_H):
        k=y/SKY_H; d.line([0,y,W,y],fill=tuple(int(top[i]+(bot[i]-top[i])*k) for i in range(3)))
def _yard(d):
    """Everything in front of the sky (also drawn alone to find which pixels are sky)."""
    for y in range(SKY_H,36):                                       # the sea, behind the wall
        d.line([0,y,W,y],fill=(18,30,64) if y%2 else (22,38,78))
    d.rectangle([0,36,W,50],fill=(70,72,80)); d.line([0,36,W,36],fill=(100,102,110))      # the wall
    for x in range(0,W,14): d.line([x,37,x,50],fill=(58,60,68))
    d.rectangle([94,16,106,50],fill=(60,62,72)); d.rectangle([91,13,109,17],fill=(48,50,60))   # the tower
    d.rectangle([97,19,103,24],fill=(240,230,160))
    for x in range(91,110,3): d.point((x,12),fill=(48,50,60))
    d.rectangle([0,50,W,GROUND],fill=(44,40,44))                    # the yard
    for x in range(6,W,16): d.line([x,54,x+6,54],fill=(54,50,54))
    d.rectangle([20,44,36,46],fill=(90,70,50)); d.line([22,46,22,49],fill=(90,70,50)); d.line([34,46,34,49],fill=(90,70,50))
    fx0=156                                                          # the fence on the right
    for x in (fx0,184): d.line([x,28,x,GROUND],fill=(110,112,120))
    for y in range(29,GROUND):                                      # the chain-link mesh
        for x in range(fx0+1,184):
            if (x+y)%4==0 or (x-y)%4==0: d.point((x,y),fill=(64,68,78))
    for x in range(fx0,W,3): d.point((x,28),fill=(150,150,160)); d.point((x+1,27),fill=(150,150,160))
def sky_at(top,bot,y): k=y/SKY_H; return tuple(int(top[i]+(bot[i]-top[i])*k) for i in range(3))
MOON=(92,6)                                                         # where the racing moon stops
def moon(d,x,y,sky,r=4):
    d.ellipse([x-r,y-r,x+r,y+r],fill=(236,232,200)); d.ellipse([x-r+3,y-r-1,x+r+3,y+r-1],fill=sky)

def _bg(d):
    _sky(d)
    rr=random.Random(zlib.crc32(b'green-dolphin'))
    for _ in range(22): d.point((rr.randint(0,W-1),rr.randint(0,SKY_H-6)),fill=rr.choice([(120,130,170),(200,200,230)]))
    moon(d,MOON[0],MOON[1],sky_at(NIGHT_TOP,NIGHT_BOT,MOON[1]-1))
    _yard(d)
register_bg(THEME, lambda v: (v+20,v+22,v+30), decor=_bg)

_SKYMASK=[]
def sky_mask():
    """'L' mask of the pixels where the sky shows (the yard drawn alone on a key colour)."""
    if not _SKYMASK:
        im=Image.new('RGB',(W,H),(255,0,255)); _yard(ImageDraw.Draw(im))
        m=Image.new('L',(W,H),0); px=im.load(); mp=m.load()
        for y in range(SKY_H):
            for x in range(W):
                if px[x,y]==(255,0,255): mp[x,y]=255
        _SKYMASK.append(m)
    return _SKYMASK[0]

# ---- effects -----------------------------------------------------------------------------------
ACC0,ACC1=150,206                                                   # Made in Heaven: time accelerates
def accel(f):
    """How many extra 'days' have flown by at frame f (0 outside, whole numbers at both ends)."""
    if f<ACC0 or f>=ACC1: return 0.0
    t=(f-ACC0)/(ACC1-ACC0); return 7*(t*t*(3-2*t))
def search_angle(f):
    return math.sin(2*math.pi*(f/144+accel(f)*3))

@fx('jojos_search')
def _fx_search(d,im,e,f):
    """The tower's searchlight: a translucent beam swinging over the yard."""
    a=search_angle(f); x0,y0=100,21; ex=round(100+a*70,6)            # (rounded: the float noise of sin(4pi) shifted a pixel)
    m=Image.new('L',(W,H),0)
    ImageDraw.Draw(m).polygon([(x0-1,y0),(x0+1,y0),(ex+12,GROUND),(ex-12,GROUND)],fill=46)
    im.paste((250,244,200),(0,0),m)

@fx('jojos_sky')
def _fx_sky(d,im,e,f):
    """Time accelerating: day and night flicker, the sun and the moon race over the sky."""
    _,days=e; ph=days%1
    k=0.5-0.5*math.cos(2*math.pi*ph)                                 # 0 night .. 1 day
    sky=Image.new('RGB',(W,H)); sd=ImageDraw.Draw(sky)
    top=tuple(int(NIGHT_TOP[i]+((80,140,220)[i]-NIGHT_TOP[i])*k) for i in range(3))
    bot=tuple(int(NIGHT_BOT[i]+((190,210,240)[i]-NIGHT_BOT[i])*k) for i in range(3))
    _sky(sd,top,bot)
    for body,off,c,r in (('sun',0.0,(255,226,120),5),('moon',0.5,None,4)):
        p=(ph+off)%1                                                 # rises left, sets right
        if 0.25<=p<=0.75:
            u=(p-0.25)/0.5; x=int(-8+u*(W+16)); y=int(SKY_H+2-math.sin(math.pi*u)*(SKY_H-4))
            if body=='sun':
                sd.ellipse([x-r,y-r,x+r,y+r],fill=c); sd.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],outline=(255,240,170))
            else: moon(sd,x,y,sky_at(top,bot,y-1))
    im.paste(sky,(0,0),sky_mask())

@fx('jojos_shadow')
def _fx_shadow(d,im,e,f):
    """A shadow under x that swings around with the racing sun."""
    _,x,days=e; a=2*math.pi*(days%1)
    cx=x+math.cos(a)*8
    d.ellipse([cx-7,GROUND-1,cx+7,GROUND+1],fill=(24,22,26))

@fx('jojos_disc')
def _fx_disc(d,im,e,f):
    """A Whitesnake DISC: a silver CD with a rainbow glint."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-4,y-2,x+4,y+2],fill=(200,204,220),outline=(110,110,130))
    d.point((x,y),fill=(30,30,40)); d.line([x-3,y-1,x-1,y-1],fill=[(255,120,200),(120,220,255),(255,240,120)][f%3])

@fx('jojos_thread')
def _fx_thread(d,im,e,f):
    """A string from (x0,y0) to (x1,y1), sagging by sag px (0: taut)."""
    _,x0,y0,x1,y1,sag=e; n=12; pts=[]
    for i in range(n+1):
        u=i/n; pts.append((x0+(x1-x0)*u,y0+(y1-y0)*u+sag*math.sin(math.pi*u)))
    d.line(pts,fill=STRING)

@fx('jojos_unravel')
def _fx_unravel(d,im,e,f):
    """Loose strings curling out of a body coming undone (k: how far)."""
    _,x,y,k=e; rr=random.Random(zlib.crc32(b'unravel'))
    for j in range(7):
        a=rr.uniform(0,math.tau); L=4+k*rr.uniform(6,14); pts=[]
        for i in range(8):
            u=i/7; pts.append((x+math.cos(a+u*2+f*0.2)*L*u,y+math.sin(a+u*2)*L*u*0.5))
        d.line(pts,fill=STRING if j%2 else (70,130,230))

@fx('jojos_net')
def _fx_net(d,im,e,f):
    """The string net across the yard: anchored on the wall, grown by k, pulled in at (px,py)."""
    _,k,px,py,pull=e
    x0,x1,y0,y1=64,134,22,GROUND
    lines=[]
    for i in range(6):
        u=i/5
        lines.append(((x0,y0+u*(y1-y0)),(x1,y1-u*(y1-y0))))          # the crossing diagonals
        lines.append(((x0+u*(x1-x0),y0),(x0+u*(x1-x0),y1)))         # the uprights
        lines.append(((x0,y0+u*(y1-y0)),(x1,y0+u*(y1-y0))))         # the rungs
    n=int(len(lines)*k)
    for (ax,ay),(bx,by) in lines[:n]:
        mx,my=(ax+bx)/2,(ay+by)/2
        if pull:                                                      # bowed towards the catch
            dd=max(0,1-math.hypot(mx-px,my-py)/40); mx+=(px-mx)*dd*pull; my+=(py-my)*dd*pull
        d.line([(ax,ay),(mx,my),(bx,by)],fill=STRING)

@fx('jojos_after')
def _fx_after(d,im,e,f):
    """A grey speed afterimage."""
    _,spr,x,y,flip,a,pal=e; draw(im,spr,x,y,flip,alpha=a,tint=(170,170,200),f=f,pal=pal)

@fx('jojos_z')
def _fx_z(d,im,e,f):
    _,x,y=e
    for j in range(3):
        k=((f*0.05+j/3)%1); text(d,'Z',int(x+k*8),int(y-k*12),(200,210,255))

@fx('jojos_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)
def banner(s,txt,y,c,scale=2,outline=(20,30,80)): s['fx'].append(('jojos_say',txt,y,c,scale,outline))

# ---- close-up: STONE FREE ----------------------------------------------------------------------
def closeup_stonefree(t,f):
    """The arm across the frame, the butterfly tattoo, the fingers coming undone into taut strings."""
    im=Image.new('RGB',(W,H),(10,14,40)); d=ImageDraw.Draw(im)
    for i in range(14):                                              # speed lines, blue
        y=i*5+2; d.line([0,y,W,y+((i*7)%5)-2],fill=(18,26,64))
    skin,shade=(217,119,87),(176,92,66)
    sleeve=[(0,26),(46,24),(46,48),(0,52)]
    web=Image.new('RGB',(W,H),(84,168,96)); wd=ImageDraw.Draw(web)        # the green sleeve with the web
    for k in range(-60,60,6): wd.line([k,24,k+30,52],fill=(30,84,44)); wd.line([k+30,24,k,52],fill=(30,84,44))
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(sleeve,fill=255); im.paste(web,(0,0),m)
    d.line([0,26,46,24],fill=(30,84,44))
    d.polygon([(46,26),(120,30),(120,44),(46,46)],fill=skin)       # the forearm
    d.line([46,46,120,44],fill=shade)
    bx,by=78,36                                                      # the butterfly tattoo
    for sx in (-1,1):
        d.polygon([(bx,by),(bx+sx*7,by-6),(bx+sx*8,by-1)],fill=(90,50,150))
        d.polygon([(bx,by),(bx+sx*6,by+5),(bx+sx*3,by+6)],fill=(110,60,170))
    d.line([bx,by-5,bx,by+5],fill=(30,20,40))
    d.rounded_rectangle([118,27,138,47],radius=4,fill=skin)        # the hand
    undo=min(1,max(0,(t-0.15)/0.3))                                  # the fingers unravel
    for i in range(4):
        y=29+i*5; L=int(14*(1-undo))
        d.rectangle([138,y,138+L,y+3],fill=skin); d.line([138,y+3,138+L,y+3],fill=shade)
        taut=t>=0.5
        x0=138+L
        if undo>0:
            pts=[(x0+j*4,y+1.5+(0 if taut else math.sin(j*0.9+f*0.6+i)*2*(1-undo*0.5))) for j in range((W-x0)//4+2)]
            d.line(pts,fill=STRING,width=2 if taut else 1)
            if taut and (f+i)%3==0: d.line([x0,y+1,W,y+1],fill=(230,245,255))
    if t>=0.3:
        jx=(f%3)-1 if t<0.45 else 0
        big_text(im,"STONE FREE!",6,(255,255,255),scale=2,cx=W//2-10+jx,outline=(30,60,170))
    if t<0.06: zoom_lines(d,STRING)
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- the clip ----------------------------------------------------------------------------------
BLUR=[(CX+16,True),(CX-16,False),(CX+14,True),(CX-14,False),(CX+18,True),(CX-16,False)]
def clip_heaven(f):
    s=scene(f,THEME)
    days=accel(f)
    s['under'].append(('jojos_search',))
    if ACC0<=f<ACC1:
        s['under'].insert(0,('jojos_sky',days))
    cl=actor(JOL[guard_pose(f)],CX,pal=JOLPAL)
    pu=actor(pu_idle(f),VX,flip=True,pal=PUPAL)
    st=actor(STONE['idle'],CX+14,GROUND-3,alpha=ST_A,vis=False)
    ws=actor(SNAKE['idle'],VX+12,GROUND-3,flip=True,alpha=ST_A,vis=False)
    hv=actor(HEAVEN['idle'],VX+12,GROUND-3,flip=True,alpha=ST_A,vis=False)
    if f<20 or f>=272: s['under'].append(('jojo_menace',f))
    # 1) Whitesnake: the disc comes out, Claude falls asleep
    if 16<=f<36:
        banner(s,"WHITESNAKE!",4,(230,230,240),2,(40,40,60)); pu['spr']=PU['attack']
        ws.update(vis=True,alpha=ST_A*min(1,(f-16)/8))
    if 26<=f<40: ws.update(vis=True,x=ez(VX+12,48,(f-26)/14))
    hand=None
    if 40<=f<60: ws.update(vis=True,x=48,spr=SNAKE['attack']); hand=(35,GROUND-14)
    if 40<=f<56:
        t=(f-40)/16; cl['spr']=JOL['hurt']
        disc=(lerp(CX+1,40,t),lerp(GROUND-13,GROUND-18,t))
        s['fx'].append(('jojos_disc',*disc))
        if f<48: s['fx'].append(('dmg',"!?",CX-4,GROUND-26,(255,120,120)))
    if 56<=f<84:
        cl['spr']=SLEEP; s['fx'].append(('jojos_z',CX+4,GROUND-10))
        x=ez(48,112,(f-60)/16); ws.update(vis=True,x=x,spr=SNAKE['idle'],flip=True)
        s['fx'].append(('jojos_disc',x-10,GROUND-16))
    # 2) Claude comes undone into string, a thread pulls the disc back
    if 72<=f<108: cl['spr']=SLEEP
    if 72<=f<100:
        k=min(1,(f-72)/10); cl['alpha']=1-0.5*k
        s['fx'].append(('jojos_unravel',CX,GROUND-4,k))
    if 84<=f<108: ws.update(vis=True,x=112,spr=SNAKE['hurt'] if f>=92 else SNAKE['idle'])
    if 80<=f<90:
        u=(f-80)/6; ex,ey=lerp(CX+6,102,u),lerp(GROUND-4,GROUND-16,u)
        s['fx'].append(('jojos_thread',CX+6,GROUND-4,ex,ey,0)); s['fx'].append(('jojos_disc',102,GROUND-16))
    if 90<=f<100:
        u=ease((f-90)/10); dx,dy=lerp(102,CX+2,u),lerp(GROUND-16,GROUND-6,u)
        s['fx'].append(('jojos_thread',CX+6,GROUND-4,dx,dy,2)); s['fx'].append(('jojos_disc',dx,dy))
        if f==90: s['fx'].append(('spark',104,GROUND-16,4))
    if 100<=f<108:
        cl.update(spr=JOL['armsup'],alpha=1)
        if f<104: s['flash']=0.3; s['fc']=(CX,GROUND-8); s['flashc']=(170,210,255)
    if 108<=f<120: ws.update(vis=True,x=ez(112,VX+12,(f-108)/10),alpha=ST_A*(1-(f-108)/12))
    # 3) close-up: STONE FREE
    if 112<=f<144: s['image']=closeup_stonefree((f-112)/32,f); return s
    # 4) MADE IN HEAVEN: time accelerates
    if 144<=f<160:
        hv.update(vis=True,alpha=ST_A*min(1,(f-144)/6),x=VX+12+(f%2 if f>=ACC0 else 0))
        if f<160: banner(s,"MADE IN HEAVEN!",4,(255,255,255),2,(110,140,60)); pu['spr']=PU['attack']
        if f==144: s['flash']=0.6; s['fc']=(VX,GROUND-14); s['flashc']=(255,255,230)
    if ACC0<=f<ACC1:
        for x in (CX,VX): s['under'].append(('jojos_shadow',x,days))
        if 160<=f<186: s['fx'].append(('dmg',"TIME IS ACCELERATING!",W//2-42,2,(240,240,160)))
    if 160<=f<192:                                                   # Pucci, a blur hitting from everywhere
        k=(f-160)//5; ph=(f-160)%5; bx,flip=BLUR[k%len(BLUR)]
        pu.update(spr=PU['attack'] if ph<3 else pu_idle(f),x=bx,flip=flip)
        for j in (1,2,3):
            px,pflip=BLUR[(k-j)%len(BLUR)] if k>=j else (VX,True)
            s['under'].append(('jojos_after',PU['idle'],px,GROUND,pflip,0.35-j*0.09,PUPAL))
        if ph==1:
            s['fx'].append(('spark',CX+(4 if flip else -4),GROUND-9,4)); s['shake']=rshake()
            cl['spr']=JOL['hurt']; cl['flip']=not flip
    # 5) the net: Claude weaves it; Pucci flies into it
    if 186<=f<200: cl.update(spr=JOL['armsup'],flip=False); pu.update(vis=f>=192,x=170)
    if 186<=f<192: pu['vis']=False
    if 186<=f<244:
        k=min(1,(f-186)/10); px,py=100,GROUND-12; pull=0
        if f>=200: pull=min(1,(f-200)/4)
        s['fx'].append(('jojos_net',k,px,py,pull))
    if 192<=f<200:
        u=(f-192)/8; pu.update(spr=PU['attack'],x=lerp(178,100,u),flip=True,vis=True)
        s['under'].append(('jojos_after',PU['idle'],lerp(178,100,u)+14,GROUND,True,0.3,PUPAL))
    if f==200: s['shake']=rshake(2); s['flash']=0.35; s['fc']=(100,GROUND-12); s['flashc']=(170,210,255)
    if 200<=f<236:
        pu.update(spr=PU['hurt'],x=100+(f%2 if f>=212 else 0),flip=True)
        if f<210: s['fx'].append(('dmg',"CAUGHT!",86,GROUND-34,(170,210,255)))
    # 6) ORA ORA ORA
    if 206<=f<214: cl.update(spr=JOL['dash'],x=ez(CX,62,(f-206)/8))
    if 206<=f<252:
        a=min(1,(f-206)/6)*ST_A if f<240 else ST_A*max(0,1-(f-240)/12)
        st.update(vis=True,alpha=a,x=ez(CX+14,80,(f-206)/8))
    if 214<=f<236:
        hit=(f//2)%2; cl['x']=62; cl['spr']=JOL['punch']
        st['spr']=STONE['attack' if hit else 'idle']
        s['fx'].append(('jojo_fists',86,98,GROUND-22,GROUND-6,ORA_B,1,10,f*11))
        rr=random.Random(f*3); s['fx'].append(('spark',94+rr.randint(0,8),GROUND-rr.randint(6,20),rr.choice((2,3))))
        if f%2: s['shake']=rshake()
        banner(s,"ORA ORA ORA!",22,(150,200,255),2,(30,40,120))
    if 236<=f<240:
        cl.update(x=62,spr=JOL['punch']); st['spr']=STONE['attack']
        banner(s,"ORA!",22,(150,200,255),3,(30,40,120)); s['flash']=0.4; s['fc']=(100,GROUND-12); s['flashc']=(220,235,255)
    if 236<=f<248:
        u=(f-236)/12; pu.update(spr=PU['hurt'],x=ez(100,172,u),y=GROUND-int(14*math.sin(math.pi*u)),flip=True)
    if f==248: s['shake']=rshake(2); s['fx'].append(('dust',166,GROUND-1)); s['fx'].append(('dust',178,GROUND-1))
    if 248<=f<258: pu.update(spr=PU['down'],x=172,flip=True)
    if 248<=f<252: s['fx'].append(('spark',176,GROUND-14,5))
    # 7) YARE YARE DAWA
    if 240<=f<270: cl.update(x=ez(62,CX,(f-240)/16),spr=JOL[guard_pose(f)])
    if 244<=f<268: banner(s,"YARE YARE DAWA.",6,(255,255,255),2,(30,40,120))
    if 258<=f<262: pu.update(spr=PU['hurt'],x=172,flip=True)
    if 262<=f<274: pu.update(spr=pu_idle(f),x=ez(172,VX,(f-262)/12),y=GROUND-((f//3)%2) if f<272 else GROUND,flip=True)
    s['actors']=[hv,ws,st,cl,pu]
    return s

CLIPS = [clip('heaven', N_, clip_heaven)]
