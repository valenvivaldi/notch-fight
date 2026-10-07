"""Arcane (League of Legends): Claude as Jinx (the blue braids down to her boots, pink eyes, the cloud
tattoos, the striped trousers) with Fishbones, the shark-faced rocket launcher, on her shoulder, down in
Zaun: green haze, pipes and neon, her pink graffiti on the walls, golden Piltover shining up top. Clip
`sisters`: Vi walks in, the Atlas gauntlets humming — POWDER... — and Jinx falters: the voices, the pink
scribbles crawling round her head. Then Fishbones fires; Vi takes it on the gauntlets and charges, Jinx
hops back and lets a wind-up monkey bomb go; every blast lights her graffiti up. Close-up: the eyes in
the scribbles, the cracked grin, I AM JINX. The last rocket goes up to the Council's tower — a pink blast,
drawn clouds — and Vi just stands there watching, then goes."""
from engine import *

THEME = 'arcane'
N_ = 432                                                            # a multiple of 12 and of 48 (the braids)
JX, VX = 40, 134
INK = (14,12,20)
PINK, PINK_L, CYAN = (255,80,170), (255,170,220), (90,230,240)
HAIR = (60,110,220)

# ---- the two sisters: built from a pose ---------------------------------------------------------------
GW, GH, C = 26, 24, 12                                              # grid, centre column (they face right)
POSES = {   # pose -> (back elbow, back hand, front elbow, front hand, lean, legs), from (C, shoulder row)
 'stand': ((-1,4),(-1,7),(3,3),(2,0),0,'stand'),
 'aim':   ((2,3),(5,1),(4,2),(7,1),0,'stance'),
 'up':    ((2,2),(5,-1),(4,1),(6,-2),-1,'stance'),
 'hold':  ((-3,1),(-1,-5),(4,1),(2,-5),0,'knock'),
 'throw': ((-2,4),(-3,6),(3,-1),(7,-4),1,'stance'),
 'laugh': ((-3,-2),(-4,-7),(4,-2),(5,-7),-1,'stand'),
 'vstand':((-1,4),(-1,7),(3,4),(3,7),0,'stand'),
 'guard': ((1,4),(4,-2),(3,4),(6,-3),0,'stance'),
 'reach': ((-1,4),(-1,7),(5,1),(9,1),0,'stand'),
 'punch': ((1,4),(4,-2),(6,0),(11,-1),2,'lunge'),
 'hurt':  ((-3,3),(-6,1),(1,5),(4,6),-2,'reel'),
 'walk1': ((-1,4),(-2,7),(3,4),(4,7),0,'stance'),
 'walk2': ((-1,4),(0,7),(3,4),(2,7),0,'stand'),
}
LEGS = {'stand':(-1,1,0),'stance':(-3,3,0),'lunge':(-5,5,1),'reel':(-4,2,0),'knock':(0,0,0)}


HIP=GH-9; TY=HIP-7; HY=TY-5                                         # legs 9 rows, torso 7, head 5
def _top(g, at):                                                    # Jinx's crop top, two rows
    for y in (at['ty'], at['ty'] + 1):
        for x in range(at['c'] - 2 + at['sh'](y), at['c'] + 3 + at['sh'](y)): put(g, x, y, 'b')
    put(g, at['c'] - 1 + at['sh'](at['ty'] + 3), at['ty'] + 3, 't')   # a cloud on her belly
def _shirt(g, at):                                                  # Vi's, under the open jacket
    for y in range(at['ty'], at['hip'] - 1):
        for dx in (0, 1): put(g, at['c'] + dx + at['sh'](y), y, 'u')
def _mouth(g, at): put(g, at['c'] + 1 + at['sh'](at['hy']), at['hy'] + 4, 'm')
def _vi_tattoo(g, at): put(g, at['c'] + 2 + at['sh'](at['hy']), at['hy'] + 3, 'v')

_SISTER = dict(w=GW, h=GH, c=C, legs=9, torso=7, torso_cols=(-2, 3), hair_y=1, leg=dict(boot_rows=3))
JINX = dict(_SISTER, name='jinx', eye='e', hair=["hhhhhhh", "hhhhhhh", "hh.h..h", "h.....h"],   # the fringe, cut straight
            leg=dict(boot_rows=3, stripe='P'), body=dict(color='s', belt='B', hip='p'),
            arm=dict(sleeve='s', back_sleeve='S', fore='s', back_fore='S', back_hand='S', mark='t'),
            paint={'body': [_top], 'head': [_mouth]})
VI = dict(_SISTER, name='vi', hair=[".hhhhh.", "hhhhhhh", "hhh...."],                          # the pink undercut
          body=dict(belt='B'), arm=dict(sleeve='j', back_sleeve='J', fore='g', fist=5),       # the Atlas gauntlets
          paint={'body': [_shirt], 'head': [_vi_tattoo]})

def build(who, pose):
    """Jinx or Vi in a pose (POSES): engine/people.py's figure()."""
    return figure(JINX if who == 'jinx' else VI, POSES[pose])

JPAL = {'s':(244,226,228),'S':(214,196,200),'e':(255,60,160),'h':HAIR,'b':(40,30,60),'B':PINK,'p':(110,60,150),'P':PINK,
        'k':(40,34,50),'t':PINK,'m':(200,60,90)}
VPAL = {'s':(236,196,170),'K':INK,'h':(240,100,150),'j':(176,44,52),'J':(130,30,40),'u':(40,40,50),'B':(70,50,40),
        'p':(70,56,50),'k':(36,30,30),'g':(200,160,70),'G':(255,230,150),'c':CYAN,'v':(60,60,70)}

def head_xy(x,feet,pose):
    """Screen position of the head's top-left (for the braids, the scribbles)."""
    o=round(POSES[pose][4]*(HIP-HY)/(HIP-HY))
    return x-GW//2+C-2+o, feet-GH+HY

def hand_xy(x,feet,pose,flip=False):
    _,_,_,h,lean,_=POSES[pose]; o=round(lean*(HIP-TY)/(HIP-HY))
    hx=C+h[0]+o; return (x-GW//2+(GW-1-hx) if flip else x-GW//2+hx), feet-GH+TY+h[1]

# ---- Zaun -----------------------------------------------------------------------------------------------
TAGS = ((8,30,"JINX"),(64,22,None),(150,30,"X"),(104,36,"<>"))      # her graffiti: words and doodles
def _tag(d,x,y,what,c):
    if what=='JINX': text(d,"JINX",x,y,c,shadow=None); d.line([x-1,y+7,x+16,y+5],fill=c)
    elif what is None:                                               # a grinning shark
        d.polygon([(x,y+4),(x+12,y),(x+16,y+4),(x+12,y+8)],outline=c); d.point((x+12,y+3),fill=c)
        for k in range(3): d.line([x+3+k*3,y+5,x+4+k*3,y+3],fill=c)
    elif what=='X': d.line([x,y,x+6,y+6],fill=c); d.line([x+6,y,x,y+6],fill=c); d.ellipse([x-2,y-2,x+8,y+8],outline=c)
    else: d.line([x,y+3,x+4,y],fill=c); d.line([x,y+3,x+4,y+6],fill=c); d.line([x+10,y,x+14,y+3],fill=c); d.line([x+10,y+6,x+14,y+3],fill=c)

def _zaun(d):
    for y in range(H):                                               # the haze, greener lower down
        k=y/H; d.line([0,y,W,y],fill=(int(lerp(30,18,k)),int(lerp(40,46,k)),int(lerp(44,40,k))))
    for x,w,h in ((0,30,10),(26,22,8),(70,36,12),(120,24,9),(150,40,11)):   # Piltover, golden, up top
        d.rectangle([x,0,x+w,h],fill=(150,120,60)); d.line([x,h,x+w,h],fill=(240,200,110))
        for wx in range(x+2,x+w-1,4): d.point((wx,h-3),fill=(255,230,150))
    d.rectangle([146,0,156,16],fill=(170,140,70),outline=(240,200,110)); d.pieslice([144,10,158,22],180,360,fill=(200,170,90))   # the Council
    d.line([151,0,151,10],fill=(255,240,180))
    for x0,c in ((0,(38,50,50)),(52,(34,46,46)),(118,(40,52,50)),(160,(36,48,48))):   # the undercity walls
        d.rectangle([x0,18,x0+50,GROUND],fill=c)
        for y in range(22,GROUND,6): d.line([x0,y,x0+50,y],fill=(30,40,40))
    for y,c in ((20,(80,90,80)),(46,(70,80,70))):                    # pipes
        d.rectangle([0,y,W,y+2],fill=c); d.line([0,y,W,y],fill=(120,130,110))
    for x in (30,98,140): d.rectangle([x,20,x+2,GROUND],fill=(70,80,70))
    d.rectangle([110,24,128,30],fill=(30,20,40),outline=PINK); text(d,"BAR",113,25,PINK,shadow=None)   # neon
    d.rectangle([12,40,24,44],fill=(20,30,40),outline=CYAN)
    for x,y,what in TAGS: _tag(d,x,y,what,(150,50,110))
    d.rectangle([0,GROUND,W,H],fill=(36,40,38))                      # the grating
    for x in range(0,W,4): d.line([x,GROUND+1,x,H],fill=(26,30,28))
register_bg(THEME, lambda v: (v+30,v+60,v+50), decor=_zaun)

@fx('ar_glow')
def _fx_glow(d,im,e,f):
    """Her graffiti, lit up by a blast (a: 0..1)."""
    _,a=e
    for x,y,what in TAGS: _tag(d,x,y,what,tuple(int(lerp(c0,c1,a)) for c0,c1 in zip((150,50,110),PINK_L)))

@fx('ar_haze')
def _fx_haze(d,im,e,f):
    """Green motes drifting up through the undercity."""
    rr=random.Random(4)
    for i in range(24):
        x=rr.uniform(0,W); y=(rr.uniform(0,H)-(f%144)*H*rr.randint(1,2)/144)%H        # loops every 144 frames
        x+=2*math.sin(2*math.pi*(f%48)/48+i)
        d.point((int(x),int(y)),fill=(110,200,120))

@fx('ar_braids')
def _fx_braids(d,im,e,f):
    """The two braids, swinging, from the sides of her head nearly to the ground."""
    _,hx,hy,feet,swing=e
    for side,root in ((-1,hx-1),(1,hx+5)):
        pts=[]
        for i in range(0,int(feet-hy-5)):
            sw=math.sin(2*math.pi*(f%48)/48+i*0.12+side)*i*0.06*swing
            pts.append((root+side*min(1.5,i*0.1)+sw-i*0.06,hy+3+i))
        d.line(pts,fill=INK,width=4); d.line(pts,fill=HAIR,width=2)
        for i in range(2,len(pts),3): d.point(pts[i],fill=(30,60,150))

@fx('ar_scribble')
def _fx_scribble(d,im,e,f):
    """The voices: pink scribbles round her head (amount 0..1), redrawn every few frames."""
    _,x,y,amt=e; rr=random.Random(f//3)
    for i in range(int(14*amt)):
        a=rr.uniform(0,2*math.pi); r=rr.uniform(6,18)
        px_,py=x+math.cos(a)*r*1.3,y+math.sin(a)*r*0.8
        kind=rr.randint(0,3)
        if kind==0:
            pts=[(px_+rr.randint(-3,3),py+rr.randint(-3,3)) for _ in range(5)]; d.line(pts,fill=PINK)
        elif kind==1: d.line([px_-2,py-2,px_+2,py+2],fill=PINK); d.line([px_+2,py-2,px_-2,py+2],fill=PINK)
        elif kind==2: d.ellipse([px_-3,py-3,px_+3,py+3],outline=PINK); d.point((px_-1,py-1),fill=PINK); d.point((px_+1,py-1),fill=PINK)
        else: d.arc([px_-4,py-2,px_+4,py+4],0,180,fill=PINK_L)
    if amt>0.6 and (f//6)%2:
        for k,(dx,dy) in enumerate(((-22,-8),(16,-12),(-14,10))):
            text(d,"JINX",int(x+dx),int(y+dy),(255,120,190),shadow=None)

def fishbones(d,cx,cy,ang,flip=False):
    """Fishbones: the shark-faced launcher, centre (cx,cy), pointing ang (radians, 0 = right, - = up)."""
    s=-1 if flip else 1
    ca,sa=math.cos(ang),math.sin(ang)
    P=lambda x,y: (cx+s*(x*ca-y*sa), cy+(x*sa+y*ca)*(1 if not flip else 1))
    d.polygon([P(-9,-3),P(6,-4),P(10,-2),P(10,3),P(6,4),P(-9,3)],fill=(80,104,140),outline=INK)
    d.polygon([P(6,-2),P(11,-1),P(11,2),P(6,3)],fill=(200,50,80))       # the open mouth
    for k in range(3): d.point(P(7+k*1.5,-1),fill=(255,255,255)); d.point(P(7+k*1.5,2),fill=(255,255,255))
    d.point(P(4,-2),fill=INK)                                           # the eye
    d.polygon([P(-2,-3),P(-6,-8),P(1,-3)],fill=PINK,outline=INK)        # the fin
    d.polygon([P(-9,-2),P(-12,-4),P(-12,4),P(-9,2)],fill=(60,70,90),outline=INK)   # the back
    d.line([P(-3,3),P(-4,6)],fill=(50,50,60),width=2)                  # the grip
    return P(12,0)

@fx('ar_fish')
def _fx_fish(d,im,e,f):
    _,x,y,ang=e; fishbones(d,x,y,ang)

@fx('ar_rocket')
def _fx_rocket(d,im,e,f):
    """A shark rocket with its pink smoke trail (from (x0,y0) to where it is)."""
    _,x0,y0,x,y=e; n=8
    for i in range(n):
        t=i/n; px_,py=lerp(x0,x,t),lerp(y0,y,t); r=1+2*(1-t)
        d.ellipse([px_-r,py-r,px_+r,py+r],fill=PINK_L if i%2 else (220,200,220))
    a=math.atan2(y-y0,x-x0); ca,sa=math.cos(a),math.sin(a)
    P=lambda u,v: (x+u*ca-v*sa, y+u*sa+v*ca)
    d.polygon([P(-5,-2),P(3,-2),P(5,0),P(3,2),P(-5,2)],fill=(80,104,140),outline=INK); d.point(P(2,-1),fill=INK)
    d.point(P(-6,0),fill=(255,220,120))

@fx('ar_boom')
def _fx_boom(d,im,e,f):
    """A Jinx blast: pink and cyan, then drawn cartoon clouds."""
    _,x,y,k,big=e; R=(14 if big else 9)
    if k<6:
        r=R*k/6+3; d.ellipse([x-r,y-r,x+r,y+r],fill=(255,240,250)); d.ellipse([x-r*0.7,y-r*0.7,x+r*0.7,y+r*0.7],fill=PINK)
        d.ellipse([x-r,y-r,x+r,y+r],outline=CYAN,width=2)
    rr=random.Random(int(x)*7+int(y))
    for i in range(7 if big else 5):                                 # the clouds, the way she'd draw them
        a=rr.uniform(0,2*math.pi); dist=R*0.6+k*0.4; r=R*0.45*(1-max(0,k-26)/20)
        if r<=0: continue
        cx,cy=x+math.cos(a)*dist,y+math.sin(a)*dist*0.6-k*0.3
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(240,140,200) if i%2 else (200,110,180),outline=INK)
        d.arc([cx-r*0.6,cy-r*0.6,cx+r*0.2,cy+r*0.2],180,270,fill=(255,220,240))

@fx('ar_monkey')
def _fx_monkey(d,im,e,f):
    """The monkey bomb: a wind-up toy, hopping along, the key turning on its back."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-3,y-6,x+3,y],fill=(150,96,60),outline=INK); d.ellipse([x-2,y-11,x+2,y-6],fill=(150,96,60),outline=INK)
    d.ellipse([x-1,y-9,x+1,y-7],fill=(240,200,160)); d.point((x+1,y-9),fill=INK)
    for s in (-1,1): d.line([x+s*3,y-4,x+s*5,y-6],fill=(150,96,60)); d.ellipse([x+s*6-2,y-8,x+s*6+2,y-5],fill=(240,200,80),outline=INK)   # the cymbals
    k=(f//2)%2; d.line([x-4,y-4+k,x-6,y-4-k],fill=(200,200,210))   # the key
    if (f//3)%2: d.point((x,y-12),fill=(255,80,80))                    # the fuse light

@fx('ar_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(236,236,240),ink=INK)                     # the engine's bubble (engine/people.py)

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_jinx(t,f):
    """Primer plano: her face in the scribbles — the pink eyes, the fringe, the cracked grin. I AM JINX."""
    im=Image.new('RGB',(W,H),(24,30,34)); d=ImageDraw.Draw(im)
    rr=random.Random(f//3)
    for _ in range(int(30*min(1,t*3))):                              # the scribbles everywhere
        x,y=rr.randint(0,W),rr.randint(0,H)
        d.line([(x+rr.randint(-6,6),y+rr.randint(-6,6)) for _ in range(4)],fill=PINK if rr.random()<0.7 else PINK_L)
    for side in (-1,1):                                              # the braids, framing it
        x=40+side*30; d.line([x,10,x+side*4,H],fill=INK,width=8); d.line([x,10,x+side*4,H],fill=HAIR,width=6)
    d.ellipse([12,8,68,H+14],fill=JPAL['s'],outline=INK,width=2)     # the face
    d.chord([8,-6,72,30],180,360,fill=HAIR,outline=INK); d.rectangle([10,8,70,18],fill=HAIR)   # the straight fringe
    for k in range(8): d.line([12+k*7,18,14+k*7,21],fill=HAIR,width=3)
    for ex in (20,44):                                               # the eyes: pink, wide, a spiral in each
        d.ellipse([ex,24,ex+16,36],fill=(255,255,255),outline=INK,width=2)
        d.ellipse([ex+4,25,ex+12,35],fill=(255,60,160)); d.ellipse([ex+6,28,ex+10,32],fill=INK)
        d.arc([ex+3,24,ex+13,36],int(f*30)%360,int(f*30)%360+200,fill=PINK_L)
    d.line([(24,44),(30,48),(36,45),(42,49),(48,45),(56,46)],fill=INK,width=2)   # the grin, cracked
    for x in range(28,54,4): d.line([x,46,x+1,48],fill=(255,255,255))
    d.line([20,40,26,44],fill=PINK); d.line([60,40,54,44],fill=PINK)  # the cloud tattoos creeping up
    if t>=0.15:
        big_text(im,"I AM",8,(240,240,250),scale=2,cx=128,shadow=INK,outline=PINK)
        big_text(im,"JINX",26,(255,120,200),scale=3,cx=128,shadow=INK,outline=INK)
    if t<0.05: zoom_lines(d,PINK)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
def clip_sisters(f):
    s=scene(f,THEME)
    if 226<=f<286: s['image']=closeup_jinx((f-226)/60,f); return s
    s['under'].append(('ar_haze',))
    jx,jy,jpose,fish=JX,GROUND,'stand','shoulder'
    vx,vpose,vflip=None,'vstand',True
    glow=0.0; scrib=0.0
    # Vi walks in; POWDER...
    if 14<=f<366: vx=VX
    if 14<=f<40: vx=lerp(W+14,VX,(f-14)/26); vpose='walk1' if (f//5)%2 else 'walk2'
    if 40<=f<84: vpose='reach'
    if 44<=f<84: s['fx'].append(('ar_bubble',"POWDER...",VX-6,18,VX-6))
    # the voices
    if 60<=f<132: jpose='hold'; fish='down'; scrib=min(1,(f-60)/30)
    # Fishbones: a rocket at Vi, who takes it on the gauntlets
    if 132<=f<150: jpose='aim'; fish='aim'; vpose='guard'
    if 136<=f<150:
        mx,my=hand_xy(jx,jy,'aim'); mx+=12
        s['fx'].append(('ar_rocket',mx,my,lerp(mx,VX-6,(f-136)/14),my))
    if 150<=f<180: s['fx'].append(('ar_boom',VX-6,GROUND-14,f-150,False))
    if 150<=f<156: s['shake']=rshake(1)
    if 150<=f<176: glow=max(glow,1-(f-150)/26)
    # Vi charges; Jinx hops back; the monkey bomb
    if 156<=f<176: t=(f-156)/20; vx=lerp(VX,72,ease(t)); vpose='punch' if f>=166 else 'guard'
    if 162<=f<176: t=(f-162)/14; jx=lerp(JX,26,t); jy=GROUND-10*math.sin(t*math.pi)
    if 176<=f<366: jx=26
    if 176<=f<214: vx=72 if f<200 else lerp(72,104,ease((f-200)/14)); vpose='guard' if f<200 else 'hurt'
    if 176<=f<184: jpose='throw'; fish='down'
    if 180<=f<200:
        t=(f-180)/20; s['fx'].append(('ar_monkey',lerp(34,66,t),GROUND-abs(math.sin(t*math.pi*4))*5))
    if 200<=f<232: s['fx'].append(('ar_boom',70,GROUND-12,f-200,True))
    if 200<=f<206: s['shake']=rshake(2)
    if 200<=f<226: glow=max(glow,1-(f-200)/26)
    if 214<=f<366: vx=104
    if 206<=f<226: jpose='laugh'; fish='down'
    # the last rocket goes up to the Council
    if 286<=f<300: jpose='up'; fish='up'
    if 292<=f<316:
        mx,my=hand_xy(jx,jy,'up'); mx+=11; my-=6
        t=(f-292)/24; s['fx'].append(('ar_rocket',mx,my,lerp(mx,151,t),lerp(my,8,t)-14*math.sin(t*math.pi)))
    if 316<=f<366: s['fx'].append(('ar_boom',151,8,(f-316)*0.6,True))
    if 316<=f<324: s['shake']=rshake(2)
    if 316<=f<350: glow=max(glow,1-(f-316)/34)
    if 330<=f<366: s['fx'].append(('ar_bubble',"...",vx,24,vx-4))
    if 366<=f<396: vx=lerp(104,W+14,(f-366)/30); vpose='walk1' if (f//5)%2 else 'walk2'; vflip=False   # Vi goes
    if 366<=f<396: jx=lerp(26,JX,ease((f-366)/30))
    if glow>0: s['under'].append(('ar_glow',glow))
    # draw: braids behind her, her, Fishbones, Vi, the scribbles
    hx,hy=head_xy(jx,jy,jpose)
    s['under'].append(('ar_braids',hx,hy,GROUND,1.0 if jy==GROUND else 2.0))
    acts=[actor(build('jinx',jpose),jx,y=jy,pal=JPAL)]
    if vx is not None: acts.append(actor(build('vi',vpose),vx,flip=vflip,pal=VPAL))
    s['actors']=acts
    if fish=='shoulder': s['fx'].append(('ar_fish',jx+9,jy-GH+TY+3,-0.2))   # tucked under her arm
    elif fish=='aim': x,y=hand_xy(jx,jy,'aim'); s['fx'].append(('ar_fish',x+1,y,0.0))
    elif fish=='up': x,y=hand_xy(jx,jy,'up'); s['fx'].append(('ar_fish',x+1,y-2,-0.6))
    else: s['under'].append(('ar_fish',jx-8,GROUND-3,0.15))       # put down at her feet
    if scrib>0: s['fx'].append(('ar_scribble',hx+2,hy+2,scrib))
    return s

CLIPS = [clip('sisters', N_, clip_sisters)]
