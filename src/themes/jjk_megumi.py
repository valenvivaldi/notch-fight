"""Jujutsu Kaisen sub-theme "jjk-megumi": Claude as Megumi Fushiguro (spiky black hair, the dark
high-collared uniform) in Shibuya on the night of 10.31, against Haruta Shigemo (shaggy brown hair,
stubble, a long tan coat, the machete). Haruta cuts him down; bleeding, Megumi gets up and presses his
fist into his open palm — close-up: FUHE YURA YURA. His shadow spreads over the street, the eight-handled
wheel rises out of it (EIGHT-HANDLED SWORD DIVERGENT SILA DIVINE GENERAL) and then the giant under it:
close-up of the pale head, the wings over its eyes, the wheel — MAHORAGA. One punch puts Haruta into the
109 tower. The wheel turns (CLANK), Mahoraga turns to the one who summoned it and raises the Sword of
Extermination; the shadow swallows the street and the night starts over."""
from engine import *
from themes.jjk import city, say, shout                            # same franchise: Shibuya, the M/W glyphs

THEME = 'jjk-megumi'
N_ = 360                                                            # a multiple of 12: the guard bounce loops
CX, HX = 30, 150                                                    # Megumi, Haruta (the loop keyframe)
MX = 66                                                             # where Mahoraga comes up out of the shadow

register_bg(THEME, lambda v: (v//2+4,v//2+4,v//2+16), decor=city)

# ---- Claude as Megumi: the spiky black hair, the dark uniform up to the collar --------------------------
MPAL = {'l':(26,28,40), 'f':(58,62,86), 'a':(34,38,62), 'i':(24,26,44)}
HAIR = ["..l..l..l...", "l.ll.ll.ll.l", ".llllllllll.", "llflllllflll"]

def _megumi(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top+5,len(g)):
        for x in range(len(g[0])):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
            elif g[y][x]=='o': g[y][x]='i'
    return S([''.join(x) for x in g])

def _blood(spr):
    """The cut on the head: a red streak down the forehead and on the collar."""
    g=[list(r) for r in spr]; top,l,r=body_box(spr)
    for x,y in ((l+1,top),(l+2,top),(l+1,top+1),(l+1,top+3),(l+5,top+5),(l+5,top+6)):
        if g[y][x]!='.': g[y][x]='r'
    return S([''.join(x) for x in g])

# the sign: both hands meet in front of the chest, the fist pressed into the palm
_SIGN = S(["...OOOOOOOO....","...OOOOOOOO....","...OOOOKOOK....","...OOOOKOOK....","...OOOOOOOOooo.",
           "...OOOOOOOOoOo.","...OOOOOOOO....","...OOOOOOOO....","...oOOOOOOo....","..oo.....oo....",".oo.......oo...",])
MEG = variant(_megumi); MEG['sign'] = _megumi(_SIGN)
MEGB = {k: _blood(v) for k, v in MEG.items()}

# ---- Haruta Shigemo: shaggy brown hair, stubble, the long tan coat open on a dark shirt, a machete -------
HPAL = {'c':(160,134,94), 'm':(214,218,230), 'q':(110,82,56)}
_HARUTA = [
"....q.qq.q......",
"...qqqqqqqq.....",
"..qqqqqqqqqq....",
"..qqssssssqq....",
"..qsKsssKsqq....",
"...ssssssss.....",
"...sqssssqs.....",
"....sqqqqs......",
".....ssss.......",
"..cccckkcccc....",
".ccccckkccccc...",
".cccckkkkcccc...",
".sccckkkkcccs...",
".s.cckkkkcc.sm..",
"...cckkkkcc..m..",
"...cBBBBBBc..m..",
"...cBB..BBc.....",
"....BB..BB......",
"....BB..BB......",
"...kkk..kkk.....",]

def _swing(rows):
    """The machete swung out in front at chest height."""
    g=[r.replace('m','.') for r in rows]
    g[11]=g[11].rstrip('.')+'ssmmmmmm'; g[12]=g[12].rstrip('.')+'s'
    w=max(map(len,g)); return S([r.ljust(w,'.') for r in g])
HARUTA = poses(S(_HARUTA),11,'s',2); HARUTA['attack'] = _swing(_HARUTA)

# ---- Mahoraga: drawn, not a grid — three times Megumi's height -----------------------------------------
MSKIN, MSKIN2, MINK = (230,228,234), (176,172,190), (24,22,30)
MCLOTH, MCLOTH2 = (44,42,56), (78,74,94)
WING = (248,248,252)
BLADE, BLADE2 = (240,244,252), (140,150,182)
WHEEL, WHEEL2 = (206,170,100), (120,88,46)
K = 0.8                                                             # body units to pixels
# (shoulder, elbow, wrist) of the front (sword) arm and the back arm, in units, facing right
ARMS = {
 'stand': (((14,-36),(16,-27),(17,-19)), ((-14,-36),(-16,-27),(-17,-19))),
 'punch': (((14,-36),(25,-35),(36,-34)), ((-14,-36),(-19,-29),(-12,-25))),
 'raise': (((14,-36),(20,-46),(14,-55)), ((-14,-36),(-17,-28),(-16,-20))),
 'cut':   (((14,-36),(25,-31),(33,-22)), ((-14,-36),(-17,-28),(-16,-20))),
}

def wheel(d,cx,cy,r,ang,w=1):
    """The eight-handled wheel: a rim, eight spokes, a knob on each handle past the rim."""
    for k in range(8):
        a=math.radians(ang+k*45); c,s=math.cos(a),math.sin(a)
        d.line([cx,cy,cx+c*(r+2*w),cy+s*(r+2*w)],fill=WHEEL2,width=w)
        kx,ky=cx+c*(r+3*w),cy+s*(r+3*w)
        d.ellipse([kx-w,ky-w,kx+w,ky+w],fill=WHEEL,outline=WHEEL2)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=WHEEL,width=w)
    d.ellipse([cx-1.5*w,cy-1.5*w,cx+1.5*w,cy+1.5*w],fill=WHEEL,outline=WHEEL2)

def draw_mahoraga(im,cx,feet,pose='stand',flip=False,rise=1.0,ang=0.0):
    """Mahoraga standing at cx with its feet on `feet`; rise<1 is still partly under the ground (only
    what is above GROUND shows). The wheel floats over its head."""
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    sx=-1 if flip else 1; fy=feet+(1-rise)*56
    P=lambda x,y: (cx+sx*x*K, fy+y*K)
    poly=lambda pts,fill: d.polygon([P(*p) for p in pts],fill=fill,outline=MINK)
    def limb(a,b,c):
        pts=[P(*a),P(*b),P(*c)]
        d.line(pts,fill=MINK,width=6,joint='curve'); d.line(pts,fill=MSKIN,width=4,joint='curve')
        x,y=pts[2]; d.ellipse([x-2.5,y-2.5,x+2.5,y+2.5],fill=MSKIN,outline=MINK)
    (ra,rb,rc),(la,lb,lc)=ARMS[pose]
    limb(la,lb,lc)                                                  # the back arm, behind the body
    for s in (-1,1):                                                # legs and feet
        poly([(s*3,-3),(s*10,-3),(s*10,-16),(s*3,-16)],MSKIN)
        poly([(s*3,0),(s*11,0),(s*10,-3),(s*3,-3)],MSKIN2)
    poly([(-12,-12),(12,-12),(9,-24),(-9,-24)],MCLOTH)              # the hakama, a flap down the front
    poly([(-3,-24),(3,-24),(4,-9),(-4,-9)],MCLOTH2)
    poly([(-9,-24),(9,-24),(14,-38),(-14,-38)],MSKIN)               # the torso
    for s in (-1,1):
        x,y=P(s*14,-36); d.ellipse([x-3.5,y-3.5,x+3.5,y+3.5],fill=MSKIN,outline=MINK)
    d.line([P(-8,-33),P(-1,-31)],fill=MSKIN2); d.line([P(1,-31),P(8,-33)],fill=MSKIN2)
    d.line([P(0,-30),P(0,-25)],fill=MSKIN2); d.line([P(-3,-28),P(3,-28)],fill=MSKIN2)
    d.rectangle([min(P(-3,-41)[0],P(3,-38)[0]),P(0,-41)[1],max(P(-3,-41)[0],P(3,-38)[0]),P(0,-38)[1]],fill=MSKIN)
    hx,hy=P(0,-44); d.ellipse([hx-4.5,hy-4.5,hx+4.5,hy+4.5],fill=MSKIN,outline=MINK)       # the head
    for s in (-1,1):                                                # two pairs of wings over the eyes
        poly([(s*1,-46),(s*11,-52),(s*13,-49),(s*10,-48),(s*12,-45),(s*2,-43)],WING)
        poly([(s*1,-43),(s*10,-43),(s*11,-40),(s*3,-41)],WING)
    d.line([P(-1.5,-40.5),P(1.5,-40.5)],fill=(120,40,50))
    limb(ra,rb,rc)                                                  # the front arm and its sword
    (ex,ey),(wx,wy)=P(*rb),P(*rc); L=math.hypot(wx-ex,wy-ey) or 1; ux,uy=(wx-ex)/L,(wy-ey)/L; nx,ny=-uy,ux
    tip=(wx+ux*15,wy+uy*15)
    d.polygon([(ex+nx*2,ey+ny*2),(wx+nx*3,wy+ny*3),tip,(wx+nx*1,wy+ny*1)],fill=BLADE,outline=BLADE2)
    wheel(d,cx,fy-46*K-7,6,ang)
    a=lay.split()[3]; ImageDraw.Draw(a).rectangle([0,GROUND+2,W,H],fill=0); lay.putalpha(a)
    im.paste(lay,(0,0),lay)

@fx('mahoraga')
def _fx_mahoraga(d,im,e,f):
    _,cx,pose,flip,rise,ang=e; draw_mahoraga(im,cx,GROUND,pose,flip,rise,ang)

@fx('mg_wheel')
def _fx_wheel(d,im,e,f):
    """The wheel alone, coming up out of the shadow ahead of the body."""
    _,cx,cy,ang=e; lay=Image.new('RGBA',(W,H),(0,0,0,0)); wheel(ImageDraw.Draw(lay),cx,cy,6,ang)
    a=lay.split()[3]; ImageDraw.Draw(a).rectangle([0,GROUND+2,W,H],fill=0); lay.putalpha(a)
    im.paste(lay,(0,0),lay)

@fx('mg_pool')
def _fx_pool(d,im,e,f):
    """Megumi's shadow spread over the street: a black pool, a violet rim, wisps rising off it."""
    _,x0,x1=e
    if x1-x0<2: return
    d.ellipse([x0,GROUND-2,x1,GROUND+4],fill=(6,4,12),outline=(80,46,120))
    rr=random.Random(f)
    for _ in range(int((x1-x0)/6)):
        x=rr.uniform(x0+3,x1-3); h=rr.randint(2,7)
        d.line([x,GROUND,x+rr.choice((-1,0,1)),GROUND-h],fill=(30,18,46) if rr.random()<0.6 else (90,56,140))

@fx('mg_blood')
def _fx_blood(d,im,e,f):
    """Drops thrown off the cut: (x, y, k) k frames since."""
    _,x,y,k=e; rr=random.Random(31)
    for i in range(10):
        vx,vy=rr.uniform(-1.4,0.4),rr.uniform(-1.6,0.2)
        px,py=x+vx*k,y+vy*k+0.15*k*k
        if py<GROUND: d.point((px,py),fill=(200,20,30) if i%3 else (120,0,10))

@fx('mg_cut')
def _fx_cut(d,im,e,f):
    _,x,y=e; d.line([x-8,y-6,x+6,y+5],fill=(255,255,255)); d.line([x-7,y-6,x+7,y+5],fill=(255,190,190))

@fx('mg_black')
def _fx_black(d,im,e,f):
    _,a=e; im.paste(fade_to(im,(4,2,8),min(1,max(0,a))))

# ---- close-up 1: the fist into the palm — FUHE YURA YURA -----------------------------------------------
O, o, INK = (217,119,87), (168,80,54), (24,14,12)
NAVY = (34,38,62)
CHANT = "FUHE YURA YURA"

def _sign(im,d,t,f):
    rr=random.Random(f)                                             # shadow welling up behind the hands
    for _ in range(26):
        x=rr.randint(0,96); y=rr.randint(0,H); L=rr.randint(4,14)
        d.line([x,y,x+rr.randint(-2,2),y-L],fill=(24,12,40) if rr.random()<0.7 else (70,40,110))
    d.rectangle([30,52,60,H],fill=NAVY,outline=INK)                 # the left sleeve, the open palm
    d.rectangle([34,26,56,56],fill=O,outline=INK); d.rectangle([34,26,38,56],fill=o)
    for i in range(4):
        x0=34+i*5.5; d.rounded_rectangle([x0,6+abs(i-1.5)*4,x0+5,30],radius=2,fill=O,outline=INK)
    dx=int(36*(1-ease(t/0.22)))                                     # the fist comes in from the right
    d.polygon([(78+dx,40),(110+dx,30),(120+dx,H),(84+dx,H)],fill=NAVY,outline=INK)
    d.rounded_rectangle([54+dx,24,84+dx,50],radius=6,fill=O,outline=INK)
    d.rounded_rectangle([60+dx,19,82+dx,27],radius=3,fill=O,outline=INK)   # the thumb over the top
    for y in (31,37,43): d.line([55+dx,y,66+dx,y],fill=o)          # the curled fingers against the palm
    if t>=0.22:
        k=(t-0.22)/0.78
        for i,x in enumerate((60,68,76)):                           # blood running off the knuckles
            L=min(14,int(k*40)-i*4)
            if L>0: d.line([x,50,x,50+L],fill=(190,20,30)); d.point((x,51+L+int(k*20)%6),fill=(150,0,10))
        if t<0.34:                                                  # the clap: a ring of shadow
            r=int((t-0.22)/0.12*40); d.ellipse([56-r,38-r//2,56+r,38+r//2],outline=(120,80,180))
    return im

# ---- close-up 2: the pale head, the wings over the eyes, the wheel — MAHORAGA --------------------------
def _face(im,d,t,f):
    for y in range(H): d.line([0,y,W,y],fill=(10+y//6,8+y//8,18+y//5))
    wheel(d,52,2,20,t*12,w=2)                                       # the wheel, above, cut by the top
    d.ellipse([28,16,76,84],fill=MSKIN,outline=MINK); d.chord([28,16,76,84],-60,80,fill=MSKIN2)
    d.ellipse([30,17,72,82],fill=MSKIN)
    for s,cx in ((-1,52),(1,52)):                                   # two pairs of wings over the eyes
        X=lambda x: cx+s*x
        d.polygon([(X(3),38),(X(30),24),(X(36),30),(X(30),32),(X(34),38),(X(5),45)],fill=WING,outline=MINK)
        d.polygon([(X(3),47),(X(28),47),(X(32),54),(X(6),53)],fill=WING,outline=MINK)
        for k in range(3): d.line([X(12+k*7),33-k*2,X(15+k*7),39-k*2],fill=(190,190,206))
    d.line([45,62,59,62],fill=(110,30,40)); d.line([47,63,57,63],fill=(60,10,20))
    if t>=0.2: say(im,"DIVINE GENERAL",12,(220,210,240),scale=1,cx=142)
    if t>=0.32:
        j=(f%3)-1 if t<0.42 else 0
        say(im,"MAHORAGA",26,(255,255,255),scale=2,cx=142+j,outline=(60,40,100))

# ---- the clip ------------------------------------------------------------------------------------------
TITLE = "EIGHT-HANDLED SWORD DIVERGENT SILA DIVINE GENERAL"
SIGN_AT, SIGN_LEN = 90, 50                                          # close-up 1
TITLE_AT = 142
RISE_AT, RISE_LEN = 180, 30                                         # the body comes up under the wheel
FACE_AT, FACE_LEN = 212, 40                                         # close-up 2
PUNCH = 262
CLANK = 292
BLACK_AT, BACK_AT = 316, 334                                        # the shadow swallows it; the night again

def clip_mahoraga(f):
    s=scene(f,THEME); s['under'].append(('jjk_city',N_,False))
    hurt = 34<=f<BLACK_AT+8
    me=(MEGB if hurt else MEG)[guard_pose(f)]; mx=CX; aura=None
    hp,hx,hy,hflip='idle',HX,GROUND,True
    # 1) Haruta cuts him down
    if 24<=f<34: hp,hx='attack',ez(HX,48,(f-24)/10)
    if 34<=f<40:
        hp,hx='attack',48
        s['fx'].append(('mg_cut',CX+4,GROUND-10)); s['fx'].append(('mg_blood',CX+2,GROUND-12,f-34))
        if f<36: s['flash']=0.7; s['fc']=(CX+4,GROUND-10); s['flashc']=(255,60,60); s['shake']=rshake(1)
    if 40<=f<52: hx=ez(48,104,(f-40)/12)
    if 52<=f<RISE_AT+30: hx=104
    if 54<=f<74: s['fx'].append(('dmg',"HA HA",hx-12,GROUND-30-(f//3)%2,(230,200,150)))
    if 34<=f<60: me,mx=MEGB['hurt'],ez(CX,24,(f-34)/6)
    # 2) he gets up and makes the sign
    if 60<=f<76: me,mx=MEGB[guard_pose(f)],24
    if 76<=f<SIGN_AT: me,mx,aura=MEGB['sign'],24,((70,40,110),1+(f%2))
    if SIGN_AT<=f<SIGN_AT+SIGN_LEN:
        s['image']=closeup((f-SIGN_AT)/SIGN_LEN,f,bg=(8,6,14),draw=_sign,txt=CHANT,box=(100,6,W-2,58),
                           text_from=0.34,color=(210,180,255),outline=(30,10,50),zoom=(150,110,220)); return s
    # 3) the shadow spreads, the wheel rises out of it; the name
    rise=0.0; wheel_y=None
    if SIGN_AT+SIGN_LEN<=f<RISE_AT+RISE_LEN: me,mx,aura=MEGB['sign'],24,((70,40,110),1)
    if 140<=f<BLACK_AT:
        w=min(1,(f-140)/24)
        s['under'].append(('mg_pool',24-8-4*w,lerp(32,MX+20,w)))
    if 152<=f<RISE_AT: wheel_y=ez(GROUND+8,GROUND-6,(f-152)/20); s['fx'].append(('mg_wheel',MX,wheel_y,f*3))
    if cue(f,TITLE_AT,TITLE): s['fx'].append(('caption',TITLE,{'box':(2,1,W-2,16),'color':(220,200,255),'max_scale':1}))
    if 150<=f<170: s['fx'].append(('dmg',"?!",hx-6,GROUND-28,(255,230,120)))
    if 140<=f<RISE_AT+RISE_LEN and f%4==0: s['shake']=rshake(1)
    # 4) Mahoraga comes up under the wheel
    if RISE_AT<=f<RISE_AT+RISE_LEN:
        rise=ease((f-RISE_AT)/RISE_LEN)*(1-0.16)+0.16               # the wheel is already up: start under it
        for _ in range(3): s['fx'].append(('rock',MX+random.Random(f*7+_).randint(-16,16),GROUND-random.Random(f+_).randint(0,5)))
    if FACE_AT<=f<FACE_AT+FACE_LEN:
        s['image']=closeup((f-FACE_AT)/FACE_LEN,f,bg=(10,8,18),draw=_face,zoom=(230,228,234)); return s
    if RISE_AT+RISE_LEN<=f<BLACK_AT: rise=1.0
    # 5) one punch: Haruta goes into the 109
    mpose,mflip,ang='stand',False,0
    if 250<=f<PUNCH: hx=ez(104,110,(f-250)/6)
    if 250<=f<PUNCH: s['fx'].append(('dmg',"!?",hx-6,GROUND-28,(255,230,120)))
    if PUNCH<=f<PUNCH+10:
        mpose='punch'
        if f<PUNCH+2: s['flash']=0.9; s['fc']=(104,GROUND-24); s['flashc']=(255,255,255)
        if f<PUNCH+6: s['shake']=rshake(2)
    if PUNCH<=f<PUNCH+8:
        k=(f-PUNCH)/8; hp='hurt'; hx=lerp(110,164,k); hy=int(lerp(GROUND,36,k)-10*math.sin(math.pi*k))
        s['fx'].append(('spark',104,GROUND-27,3+(f-PUNCH)))
    if PUNCH+6<=f<BLACK_AT: s['under'].append(('jjk_crater',164,27))
    if PUNCH+8<=f<BLACK_AT: hp,hx,hy='hurt',164,36
    # 6) the wheel turns; it turns on Megumi and raises the sword
    if PUNCH+14<=f<BLACK_AT: mflip=True
    if f>=RISE_AT+30 and f<BLACK_AT: me,mx,aura=MEGB['hurt'],24,None
    if CLANK<=f<CLANK+8:
        ang=ease((f-CLANK)/6)*45
        if f<CLANK+3: s['shake']=rshake(1)
    if CLANK<=f<CLANK+16: shout(s,"CLANK",(230,200,130),y=8,scale=2,cx=MX+42,outline=(60,40,20))
    if CLANK+12<=f<BLACK_AT: mpose='raise'
    if BLACK_AT-4<=f<BLACK_AT+4: mpose='cut'
    if rise>0: s['under'].append(('mahoraga',MX,mpose,mflip,rise,ang))
    # 7) the shadow swallows the street, the night starts over
    if BLACK_AT-4<=f<BLACK_AT: s['fx'].append(('mg_cut',mx+6,GROUND-14))
    if BLACK_AT<=f<BACK_AT: s['fx'].append(('mg_black',(f-BLACK_AT+1)/6))
    if BACK_AT<=f<N_: s['fx'].append(('mg_black',(N_-f)/(N_-BACK_AT)))
    s['actors']=[actor(me,mx,pal=MPAL,aura=aura),
                 actor(HARUTA[hp],hx,hy,flip=hflip,pal=HPAL)]
    return s

CLIPS = [clip('mahoraga', N_, clip_mahoraga)]
