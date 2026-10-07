"""Dungeon Meshi: Claude (Laios: blond hair, chainmail, sword) vs the Red Dragon.
The dragon stomps in and breathes fire; Laios rolls under it and just stares — close-up:
I WONDER HOW IT TASTES... — then leaps and stabs its neck. Senshi shows up with his pot:
DRAGON STEW. Laios eats, happy; the pot, Senshi and what is left of the dragon fade away."""
from engine import *

THEME = 'meshi'
N_ = 264

FIRE, FIRE_HI = (255,150,40), (255,240,170)
GOLD = (250,210,60)
# Laios: blond hair, chainmail torso (two greys for the ring pattern)
LPAL = {'l':(238,208,110), 'f':(196,158,70), 'a':(150,158,176), 'i':(104,110,130)}
# Senshi: iron helmet, long brown beard, green tunic, leather boots
SPAL = {'a':(150,150,162), 'u':(150,100,58), 'c':(232,184,142), 't':(92,112,70), 'm':(86,62,40)}

HAIR = ["..llllllll..", ".llllllllll.", "llflllllfll."]

def _laios(spr):
    """Blond bowl cut over the body, chainmail from the chest down (the arms stay bare)."""
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if (x+y)%2 else 'i'
    return S([''.join(x) for x in g])
LAIOS=variant(_laios)

SENSHI=S([
"....aaaa....","...aaaaaa...","..aaaaaaaa..","..cKccccKc..","..cccccccc..",
".uuuuuuuuuu.",".uuuuuuuuuu.","..uuuuuuuu..",".ttuuuuuutt.","cttttttttttc",
"cttttttttttc","..tttttttt..","..mmm..mmm..","..mmm..mmm..",".kkkk..kkkk.",])

def _dungeon(d):
    """Stone walls: faint brick courses on both sides, two pillars, a torch bracket."""
    for y in range(4,GROUND-2,5):
        off=0 if (y//5)%2 else 4
        for x in range(off,W,9):
            if 40<x<150 and y<40: continue                       # keep the middle dark (text reads there)
            d.line([x,y,x+7,y],fill=(20,16,18))
    for x in (6,96):
        d.rectangle([x,6,x+5,GROUND],fill=(24,20,22)); d.line([x,6,x+5,6],fill=(40,34,34))
    d.rectangle([98,26,101,28],fill=(60,44,30))                  # torch bracket on the pillar
register_bg(THEME, lambda v: (v,v*9//10,v*4//5), decor=_dungeon)

@fx('meshi_torch')
def _fx_torch(d,im,e,f):
    _,x,y=e; rr=random.Random((f%24)*7+x)                             # a 24-frame flicker: it loops
    for _ in range(5):
        px,py=x+rr.randint(-1,1),y-rr.randint(0,4); d.point((px,py),fill=FIRE_HI if py>y-2 else FIRE)

# where the hand is on each Claude pose (col,row in the 11-row body grid), and how Laios holds the sword there
GRIP = {'guard':(13,4,-60), 'guard2':(13,4,-60), 'punch':(16,5,0), 'charge':(15,5,-30)}

@fx('meshi_sword')
def _fx_sword(d,im,e,f):
    """Laios' sword from the hand (hx,hy) at angle a (degrees, 0 = right, -90 = up)."""
    _,hx,hy,a,L=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.line([hx-c*2,hy-s*2,hx,hy],fill=(110,70,40))                                  # grip
    d.line([hx+2*c-2*s,hy+2*s+2*c,hx+2*c+2*s,hy+2*s-2*c],fill=GOLD)                   # crossguard
    d.line([hx+3*c,hy+3*s,hx+L*c,hy+L*s],fill=(206,212,228))                         # blade
    d.point((hx+L*c,hy+L*s),fill=(255,255,255))

def laios(s,pose,x,y=GROUND,flip=False,sword=True):
    """Laios actor; adds his sword (drawn over him) for the poses that hold it."""
    spr=LAIOS[pose]; a=actor(spr,x,y,flip=flip,pal=LPAL)
    if sword and pose in GRIP:
        col,row,ang=GRIP[pose]; hx,hy=hand_at(spr,x,y,flip,col,row,h=11)
        s['fx'].append(('meshi_sword',hx,hy,(180-ang) if flip else ang,12))
    return a

@fx('meshi_dragon')
def _fx_dragon(d,im,e,f):
    """The Red Dragon, facing left, standing on the ground at body centre cx.
    neck 0..1 rears the head up, mouth 0..1 opens the jaw, lying 0..1 collapses it (head on the floor),
    tint blends the whole body (hurt flash), keep<1 dissolves it pixel by pixel."""
    _,cx,neck,mouth,lying,tint,keep=e; cx=int(cx); gy=GROUND
    L=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(L)
    red,dark,belly,horn,eye=(190,40,36,255),(112,20,24,255),(232,170,92,255),(232,222,190,255),(255,220,60,255)
    ly=int(6*lying)
    # tail: tapering segments down to the floor, spikes on top
    for i in range(8):
        t=i/7; x=cx+12+i*4; y=gy-12+ly*0.5+t*9+math.sin(2*math.pi*f/44+i*0.7)*(1-lying); r=max(1,4-i//2)
        dd.ellipse([x-r,y-r,x+r,y+r],fill=red,outline=dark)
        if i%2==0: dd.point((x,y-r-1),fill=horn)
    # legs (front + back), claws
    for x0 in (cx-13,cx+4):
        dd.rectangle([x0,gy-11+ly,x0+8,gy],fill=red,outline=dark)
        for k in range(3): dd.point((x0+1+k*3,gy),fill=horn)
    # body + belly
    dd.ellipse([cx-17,gy-27+ly,cx+17,gy-6+ly],fill=red,outline=dark)
    dd.ellipse([cx-13,gy-15+ly,cx+9,gy-6+ly],fill=belly)
    for x in range(cx-11,cx+8,3): dd.line([x,gy-13+ly,x,gy-7+ly],fill=(200,130,70,255))
    # folded wing on the back
    fl=int(2*math.sin(2*math.pi*f/33)*(1-lying))          # periods that divide the clip: it loops
    wing=[(cx-8,gy-22+ly),(cx+1,gy-39+ly*2-fl),(cx+21,gy-31+ly*2-fl),(cx+15,gy-18+ly)]
    dd.polygon(wing,fill=dark,outline=(60,10,14,255))
    for p in wing[1:3]: dd.line([cx-6,gy-22+ly,p[0],p[1]],fill=(150,40,40,255))
    # head position: reared (neck=1), resting, or on the floor (lying)
    hx=int(lerp(cx-38,cx-46,lying)); hy=int(lerp(gy-42-6*neck,gy-10,lying))
    # neck: a thick curve from the chest to the back of the head
    bx,by=cx-12,gy-18+ly; ex,ey=hx+14,hy+6; mx,my=(bx+ex)/2+4*(1-lying),min(by,ey)-2*(1-lying)
    for k in range(13):
        t=k/12; x=(1-t)**2*bx+2*(1-t)*t*mx+t*t*ex; y=(1-t)**2*by+2*(1-t)*t*my+t*t*ey; r=5-t*1.5
        dd.ellipse([x-r,y-r,x+r,y+r],fill=red,outline=dark)
    for k in range(1,12,3):
        t=k/12; x=(1-t)**2*bx+2*(1-t)*t*mx+t*t*ex; y=(1-t)**2*by+2*(1-t)*t*my+t*t*ey
        dd.point((x+2,y-5),fill=horn)
    # head: skull, snout, jaw (drops with mouth), horns, eye
    op=int(5*mouth)
    if op: dd.rectangle([hx+1,hy+6,hx+13,hy+7+op],fill=(70,8,10,255))
    dd.rectangle([hx+1,hy+8+op,hx+14,hy+10+op],fill=red,outline=dark)                # jaw
    for k in range(3): dd.point((hx+3+k*3,hy+7+op),fill=horn)                          # lower teeth
    dd.rectangle([hx+8,hy,hx+19,hy+8],fill=red,outline=dark)                           # skull
    dd.rectangle([hx,hy+2,hx+10,hy+7],fill=red,outline=dark)                           # snout
    if op:
        for k in range(3): dd.point((hx+2+k*3,hy+8),fill=horn)                         # upper teeth
    dd.line([hx+16,hy+1,hx+23,hy-6],fill=horn); dd.line([hx+12,hy,hx+16,hy-6],fill=horn)
    dd.point((hx+1,hy+3),fill=dark)                                                    # nostril
    if lying<0.5: dd.rectangle([hx+11,hy+3,hx+12,hy+3],fill=eye)
    else: dd.line([hx+10,hy+4,hx+13,hy+4],fill=dark)                                   # closed
    if tint:
        rgb=fade_to(L.convert('RGB'),tint,0.55); rgb.putalpha(L.getchannel('A')); L=rgb
    if keep<1:
        a=L.getchannel('A'); pa=a.load()
        for y in range(H):
            for x in range(W):
                if pa[x,y] and ((x*37+y*91)%97)/97>=keep: pa[x,y]=0
        L.putalpha(a)
    im.paste(L,(0,0),L)

def mouth_at(cx,neck): return cx-37, int(GROUND-42-6*neck)+8

@fx('meshi_breath')
def _fx_breath(d,im,e,f):
    """Fire breath: a jittery stream of flame blobs from the mouth to (x1,y1), hottest near the mouth."""
    _,x0,y0,x1,y1,p=e; rr=random.Random(f*17)
    n=int(28*p)
    for i in range(n):
        t=i/28; x=lerp(x0,x1,t)+rr.uniform(-2,2); y=lerp(y0,y1,t)+rr.uniform(-2,2)*(0.5+t); r=1+int(t*3)+rr.randint(0,1)
        c=FIRE_HI if t<0.3 else (FIRE if t<0.75 else (220,60,20))
        d.ellipse([x-r,y-r,x+r,y+r],fill=c)

@fx('meshi_pot')
def _fx_pot(d,im,e,f):
    """Senshi's pot on a small wood fire: bubbling red stew, steam curling up."""
    _,x=e; y=GROUND; rr=random.Random((f%24)*5)
    for k in range(4):                                             # fire under the pot
        fx_,fy=x-5+k*3+rr.randint(-1,1),y-1-rr.randint(0,2); d.point((fx_,fy),fill=FIRE if k%2 else FIRE_HI)
    d.line([x-7,y,x+7,y],fill=(90,60,36))                          # logs
    d.rectangle([x-8,y-11,x+8,y-2],fill=(40,40,46),outline=(90,90,100))
    d.line([x-9,y-11,x+9,y-11],fill=(120,120,132))                 # rim
    d.rectangle([x-7,y-10,x+7,y-9],fill=(190,70,40))               # the stew
    for k in range(3):
        if (f//4+k)%3==0: d.point((x-4+k*4,y-10),fill=(250,160,90))   # bubbles
    for k in range(3):                                             # steam
        ph=((f%12)/12+k/3)%1; sx=x-4+k*4+math.sin(2*math.pi*f/24+k*2)*2; sy=y-12-ph*20
        d.point((int(sx),int(sy)),fill=(200,200,210) if ph<0.6 else (110,110,120))

@fx('meshi_ladle')
def _fx_ladle(d,im,e,f):
    _,x,y,x1,y1=e; d.line([x,y,x1,y1],fill=(150,110,70)); d.rectangle([x1-1,y1,x1+1,y1+1],fill=(150,110,70))

@fx('meshi_heart')
def _fx_heart(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); c=(250,110,140)
    d.point((x-1,y),fill=c); d.point((x+1,y),fill=c); d.line([x-2,y+1,x+2,y+1],fill=c)
    d.line([x-1,y+2,x+1,y+2],fill=c); d.point((x,y+3),fill=c)

def closeup_taste(t,f):
    """Primer plano: Laios' face, eyes shining, drool; I WONDER / HOW IT / TASTES..."""
    im=Image.new('RGB',(W,H),(8,6,8)); d=ImageDraw.Draw(im)
    for i in range(0,64,4): d.line([0,i,96,i],fill=(18,8,8))                    # red haze from the dragon
    O,o=(217,119,87),(168,80,54); hair,hair2=LPAL['l'],LPAL['f']
    d.rectangle([22,12,82,64],fill=O); d.rectangle([76,12,82,64],fill=o)        # the block head
    d.rectangle([18,2,86,16],fill=hair)                                          # bowl cut
    for x in range(20,86,6): d.polygon([(x,16),(x+6,16),(x+3,22)],fill=hair)     # bangs
    for x in (30,52,70): d.line([x,4,x-2,14],fill=hair2)
    for x0 in (32,56):                                                           # big shining eyes
        d.rectangle([x0,26,x0+14,36],fill=(24,14,12))
        d.rectangle([x0+2,27,x0+5,30],fill=(255,255,255)); d.point((x0+10,33),fill=(255,255,255))
        if (f//3)%2: d.point((x0+4,28),fill=(255,250,200))
    for k,(sx,sy) in enumerate(((28,24),(74,24),(50,22))):                       # sparkles around the eyes
        if (f//2+k*2)%6<3: d.line([sx-2,sy,sx+2,sy],fill=GOLD); d.line([sx,sy-2,sx,sy+2],fill=GOLD)
    d.rectangle([40,46,66,52],fill=(60,16,16)); d.rectangle([42,46,64,47],fill=(255,255,255))   # grin
    dl=min(12,int(t*30))                                                         # drool growing from the corner
    if dl: d.line([64,52,64,52+dl],fill=(170,210,240)); d.point((64,53+dl),fill=(230,245,255))
    lines=("I WONDER","HOW IT","TASTES...")
    for j,w in enumerate(lines):
        if t>=0.12+j*0.18: FX['big'](d,im,('big',w,8+j*17,GOLD if j==2 else (236,236,244),138),f)
    if t<0.06: zoom_lines(d)
    return im

DX=150               # the dragon's body centre once it has walked in
STAB=(110,36)        # Laios' position (x, feet) when the sword meets the neck

def clip_dragonstew(f):
    s=scene(f,THEME)
    s['under'].append(('meshi_torch',99,25))
    acts=[]
    # the dragon's state for this frame
    dx,neck,mouth,lying,tint,keep=None,0,0,0,None,1
    if 14<=f<168: dx=ez(240,DX,(f-14)/30)
    if 44<=f<56: neck=(f-44)/12; mouth=neck*0.6
    if 56<=f<84: neck,mouth=1,1
    if 84<=f<92: neck=1-(f-84)/8; mouth=neck
    if 138<=f<162: neck=0.3
    if 162<=f<168: neck,mouth,tint=0.3,0.8,(255,255,255) if f%2 else (255,80,60)
    if f>=168:
        dx=DX; lying=ease((f-168)/14); tint=None
        if f>=244: keep=max(0,1-(f-244)/12)
    # 1) the dragon stomps in
    if 14<=f<44:
        if (f-14)%8<2: s['shake']=rshake(1); s['fx'].append(('dust',dx-12,GROUND-1)); s['fx'].append(('dust',dx+6,GROUND-1))
    if 26<=f<70: callout(s,"RED DRAGON",c=(255,90,70))
    # 2) fire breath; Laios rolls out from under it
    lx,lpose,lflip,ly=30,guard_pose(f),False,GROUND
    if 56<=f<84:
        mx,my=mouth_at(DX,1); tx=lerp(34,20,(f-56)/28)
        s['fx'].append(('meshi_breath',mx,my,tx,GROUND-3,min(1,(f-56)/6)))
        if f>=60:
            for j in range(4): s['fx'].append(('fire',14+j*9,GROUND,3+((f+j)%3)))
        if f%3==0: s['shake']=rshake(1)
        s['flash']=0.12; s['fc']=(40,GROUND-6); s['flashc']=(255,150,60)
    if 58<=f<70: lx,lpose=ez(30,66,(f-58)/12),'dash'
    if 84<=f<90:
        for j in range(4): s['fx'].append(('smoke',14+j*9,GROUND-4-(f-84),2,(40,34,34)))
    if f>=70: lx=66
    # 3) close-up: I WONDER HOW IT TASTES...
    if 92<=f<138: s['image']=closeup_taste((f-92)/46,f); return s
    # 4) the leap and the stab
    if 138<=f<150:
        lpose='charge'
        if (f//2)%2: s['fx'].append(('twinkle',83,GROUND-8,2))
    if 150<=f<162:
        p=(f-150)/12; lpose='punch'; lx=lerp(66,STAB[0],p); ly=lerp(GROUND,STAB[1],p)-12*math.sin(p*math.pi)
    if 162<=f<168:
        lpose,lx,ly='punch',STAB[0],STAB[1]
        if f<164: s['flash']=0.7; s['fc']=(126,30); s['flashc']=(255,240,220)
        s['fx'].append(('spark',128,30,7)); s['fx'].append(('ring',128,30,(f-162)*4,(255,200,120)))
        s['shake']=rshake(2)
    if 168<=f<182:
        p=(f-168)/14; lpose='guard'; lx=lerp(STAB[0],88,p); ly=lerp(STAB[1],GROUND,p*p)
        if f<174: s['shake']=rshake(2 if f<171 else 1)
        if f in (176,177,178): s['fx'].append(('dust',DX-30,GROUND-1)); s['fx'].append(('dust',DX-10,GROUND-1))
    if 168<=f<184: callout(s,"FELLED!",c=GOLD)
    # 5) dragon stew
    if f>=182: lx,lflip=88,True
    sx=None
    if 184<=f<244: sx=ez(-10,40,(f-184)/12)
    if 244<=f<256: sx=ez(40,-12,(f-244)/12)
    if 196<=f<244:
        s['under'].append(('meshi_pot',64))
        if f<200: s['fx'].append(('smoke',64,GROUND-8,3,(120,120,130)))
        k=(f//4)%4; s['fx'].append(('meshi_ladle',46,GROUND-10,58+k,GROUND-12+(k%2)))
    if 244<=f<250: s['fx'].append(('smoke',64,GROUND-6,2+(f-244)//2,(90,90,100)))
    if 200<=f<218: s['fx'].append(('big',"DRAGON STEW",2,FIRE))
    if 218<=f<228: callout(s,"1 RED DRAGON",c=(236,236,244))
    if 228<=f<236: callout(s,"SIMMER 3 HRS",c=(236,236,244))
    if 234<=f<246:
        lpose='armsup'; callout(s,"DELICIOUS!",c=GOLD) if f>=236 else None
        for k in range(3):
            ph=((f-234)/12+k/3)%1; s['fx'].append(('meshi_heart',82+k*6,GROUND-14-ph*14))
    # 6) back to the neutral pose
    if 246<=f<258: lx,lflip,lpose=ez(88,30,(f-246)/12),True,guard_pose(f)
    if f>=258: lx,lflip,lpose=30,False,guard_pose(f)
    if 182<=f<234 and lpose not in ('armsup',): lpose=guard_pose(f)
    if dx is not None and keep>0: s['under'].append(('meshi_dragon',dx,neck,mouth,lying,tint,keep))
    if sx is not None: acts.append(actor(SENSHI,sx,pal=SPAL))
    acts.append(laios(s,lpose,lx,ly,flip=lflip))
    s['actors']=acts
    return s

CLIPS = [clip('dragonstew', N_, clip_dragonstew)]
