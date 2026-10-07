"""Memento: Claude as Leonard Shelby (short blond hair, the pale suit, a polaroid in one hand, the gun in the
other) and the film's structure as the clip. It opens in colour and runs backwards: the polaroid
un-develops to white as he shakes it, the shell casing flies up off the floor back into the gun. Then
black and white, forwards: the motel room, the phone, REMEMBER SAMMY JANKIS. Close-up, in colour: the
tattoo across his chest in the mirror, JOHN G. RAPED AND MURDERED MY WIFE. Black and white again: he
writes on Teddy's polaroid, DON'T BELIEVE HIS LIES. And the end meets the start, as in the film: back in
the derelict building in black and white, a fresh polaroid develops in his hand and the colour comes
up with it — which is the clip's first frame."""
from engine import *
from PIL import ImageOps

THEME = 'memento'
N_ = 360                                                            # a multiple of 12
LX = 70                                                             # Leonard
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(30,30,40)
# Leonard: short blond hair, the pale linen suit, a blue shirt
LPAL = {'1':(226,196,120),'2':(214,200,170),'3':(170,156,128),'4':(110,140,180)}
HAIR = [".1111111111.","111111111111"]

def _leonard(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=top+5: g[y][x]='4' if x in ((l+r)//2,(l+r)//2+1) and y<top+8 else '2'   # jacket, shirt
            elif c=='o' and y>=top+5: g[y][x]='3' if y>=top+8 else '2'
    return S([''.join(x) for x in g])
LEONARD=variant(_leonard)

# ---- the two places ------------------------------------------------------------------------------------
def _building(d):
    """The derelict building by the refinery, warm dusty light through the broken windows."""
    d.rectangle([0,0,W,H],fill=(150,110,80))
    for y in range(0,46,5):                                          # bricks
        for x in range((y//5)%2*8,W,16): d.rectangle([x,y,x+14,y+3],fill=(160,118,86))
    for wx in (20,120):                                             # broken windows, the light pouring in
        d.rectangle([wx,8,wx+30,30],fill=(250,220,160)); d.line([wx+15,8,wx+15,30],fill=(90,70,56),width=2)
        d.polygon([(wx+4,8),(wx+12,8),(wx+6,16)],fill=(110,84,64)); d.polygon([(wx+20,30),(wx+28,22),(wx+30,30)],fill=(110,84,64))
    d.polygon([(20,30),(50,30),(80,H),(0,H)],fill=(190,150,110))      # the shafts of light on the floor
    d.rectangle([0,46,W,H],fill=(120,92,70)); d.line([0,46,W,46],fill=(90,70,56))
    for x,y in ((40,54),(150,58),(100,50)): d.ellipse([x-6,y-1,x+6,y+1],fill=(104,80,62))   # rubble
register_bg(THEME, lambda v: (v+90,v+70,v+50), decor=_building)

@fx('mm_motel')
def _fx_motel(d,im,e,f):
    """The motel room: the bed, the lamp, the phone, his notes and photos pinned all over the wall."""
    d.rectangle([0,0,W,H],fill=(170,170,150))
    for x in range(0,W,8): d.line([x,0,x,46],fill=(160,160,140))
    rr=random.Random(8)
    for i in range(14):                                              # notes and polaroids on the wall
        x=rr.randint(96,176); y=rr.randint(4,30)
        if i%2: d.rectangle([x,y,x+6,y+7],fill=(250,250,250)); d.rectangle([x+1,y+1,x+5,y+5],fill=(80,80,80))
        else: d.rectangle([x,y,x+8,y+5],fill=(240,230,190)); d.line([x+1,y+2,x+6,y+2],fill=(100,100,100))
    for i in range(5): d.line([96+i*16,8+i*3,112+i*16,14],fill=(160,40,40))   # string between them
    d.rectangle([0,46,W,H],fill=(120,100,80))
    d.rectangle([14,40,60,50],fill=(200,190,170),outline=(80,80,80)); d.rectangle([14,36,24,42],fill=(240,240,240))   # the bed
    d.rectangle([66,40,76,48],fill=(110,80,60)); d.line([71,40,71,30],fill=(60,60,60)); d.polygon([(66,30),(76,30),(73,24),(69,24)],fill=(230,220,160))   # lamp
    d.rectangle([67,37,75,40],fill=(40,40,44))                        # the phone

@fx('mm_gray')
def _fx_gray(d,im,e,f):
    """Black and white: the whole frame drained of colour (a 0..1)."""
    _,a=e
    if a>0:
        g=ImageOps.grayscale(im).convert('RGB'); g=Image.blend(g,Image.new('RGB',im.size,(20,20,20)),0.08)
        im.paste(Image.blend(im,g,a))

def polaroid(d,x,y,dev,w=6,h=7):
    """A polaroid: white frame, the picture coming up out of white as it develops (dev 0..1)."""
    x,y=int(x),int(y)
    d.rectangle([x,y,x+w,y+h],fill=(250,250,246),outline=(170,170,170))
    pic=tuple(int(lerp(240,v,dev)) for v in (70,60,52))
    d.rectangle([x+1,y+1,x+w-1,y+h-3],fill=pic)
    if dev>0.6: d.point((x+w//2,y+h//2-1),fill=tuple(int(lerp(240,v,dev)) for v in (150,40,40)))

@fx('mm_polaroid')
def _fx_polaroid(d,im,e,f):
    _,x,y,dev=e; polaroid(d,x,y,dev)

@fx('mm_gun')
def _fx_gun(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x,y,x+5,y+1],fill=(40,40,44)); d.rectangle([x,y+1,x+1,y+3],fill=(40,40,44))

@fx('mm_casing')
def _fx_casing(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x,y,x+1,y],fill=(220,180,80)); d.point((x+1,y+1),fill=(180,140,60))

@fx('mm_rewind')
def _fx_rewind(d,im,e,f):
    """The tell that it is running backwards: a little rewind mark in the corner."""
    for k in (0,6): d.polygon([(10+k,4),(4+k,8),(10+k,12)],fill=(250,250,250))

@fx('mm_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(250,250,250),ink=(30,30,30))                     # the engine's bubble (engine/people.py)

@fx('mm_teddy')
def _fx_teddy(d,im,e,f):
    """Teddy's polaroid, held up big, and what he writes under it (k 0..1: how much is written)."""
    _,k=e; x,y=118,4
    d.rectangle([x,y,x+56,y+54],fill=(250,250,246),outline=(150,150,150))
    d.rectangle([x+4,y+3,x+52,y+28],fill=(120,130,140))
    d.ellipse([x+20,y+5,x+36,y+23],fill=(220,190,160),outline=(60,60,60))   # a smiling face (not a portrait)
    d.rectangle([x+22,y+11,x+27,y+14],outline=(40,40,40)); d.rectangle([x+29,y+11,x+34,y+14],outline=(40,40,40))
    d.arc([x+23,y+15,x+33,y+21],20,160,fill=(60,40,40)); d.rectangle([x+20,y+23,x+36,y+28],fill=(80,90,110))
    text(d,"TEDDY",x+18,y+31,(40,40,40),shadow=None)
    line1,line2="DON'T BELIEVE","HIS LIES"; n=int(k*(len(line1)+len(line2)))
    text(d,line1[:n],x+3,y+39,(160,30,30),shadow=None)
    if n>len(line1): text(d,line2[:n-len(line1)],x+12,y+46,(160,30,30),shadow=None)

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_tattoo(t,f):
    """Primer plano, in colour: his chest in the bathroom mirror, the tattoo — JOHN G. RAPED AND MURDERED
    MY WIFE — and the smaller ones round it."""
    im=Image.new('RGB',(W,H),(200,200,190)); d=ImageDraw.Draw(im)
    d.rectangle([6,2,W-7,H-3],fill=(170,180,180),outline=(120,120,120),width=2)   # the mirror
    d.rectangle([20,4,W-21,H],fill=SKIN); d.rectangle([W-30,4,W-21,H],fill=SKIN_D)
    d.line([92,4,92,H],fill=SKIN_D)                                   # the breastbone
    for y in (52,58): d.arc([30,y-10,90,y+6],20,160,fill=SKIN_D); d.arc([94,y-10,154,y+6],20,160,fill=SKIN_D)
    a=min(1,t/0.1)
    ink=tuple(int(lerp(s_,v,a)) for s_,v in zip(SKIN,(40,40,70)))
    big_text(im,"JOHN G. RAPED AND",12,ink,scale=1,cx=W//2,shadow=None)
    big_text(im,"MURDERED MY WIFE",22,ink,scale=1,cx=W//2,shadow=None)
    if t>=0.3:
        for i,(txt,x,y) in enumerate((("FACT 1: MALE",26,34),("FACT 2: WHITE",112,34),("FIND HIM AND KILL HIM",50,46))):
            if t>=0.3+i*0.1: text(d,txt,x,y,(70,60,90),shadow=None)
    if t<0.05: zoom_lines(d,(120,120,120))
    return im

# ---- the clip -------------------------------------------------------------------------------------------
HAND=(13,4)
def clip_polaroids(f):
    s=scene(f,THEME)
    pose=guard_pose(f); gray=0.0
    spr=LEONARD[pose]
    hx,hy=hand_at(spr,LX,GROUND,False,*HAND,h=11)
    ox,oy=origin(spr,LX); top,l,r=body_box(spr)
    gun=(ox+l-6,oy+top+8)
    dev=1.0
    # 1) colour, running backwards: the polaroid un-develops, the casing flies back up into the gun
    if 14<=f<80:
        s['fx'].append(('mm_rewind',))
        dev=max(0,1-(f-14)/40)
        if (f//3)%2: hx+=1                                            # shaking it
        if 30<=f<60:
            p=(f-30)/30; cx=lerp(gun[0]-14,gun[0]+4,p); cy=lerp(GROUND-1,gun[1],p)-12*math.sin(p*math.pi)
            s['fx'].append(('mm_casing',cx,cy))
        if 60<=f<64: s['flash']=0.5; s['fc']=(gun[0]+6,gun[1]); s['flashc']=(255,230,160)   # the shot, un-fired
    if 80<=f<96: dev=0.0
    # 2) black and white, forwards: the motel, the phone
    motel=96<=f<150 or 220<=f<266
    if motel:
        s['under'].append(('mm_motel',)); gray=1.0
    if 96<=f<150:
        s['fx'].append(('mm_bubble',"REMEMBER SAMMY JANKIS.",LX+10,12))
        pose='charge'
    if 80<=f<96: gray=(f-80)/16
    # 3) close-up, in colour: the tattoo
    if 150<=f<220: s['image']=closeup_tattoo((f-150)/70,f); return s
    # 4) black and white: Teddy's polaroid
    if 220<=f<266: s['fx'].append(('mm_teddy',min(1,(f-222)/24))); pose='charge'
    # 5) the end meets the start: black and white in the building, a fresh polaroid develops, the colour comes up
    if 266<=f<330:
        gray=1.0 if f<284 else max(0,1-(f-284)/36)
        dev=0.0 if f<276 else min(1,(f-276)/44)
        if (f//3)%2 and f<320: hx+=1
    if 96<=f<266: dev=0.0
    acts=[actor(LEONARD[pose],LX,pal=LPAL)]
    s['actors']=acts
    if not (96<=f<150 or 220<=f<266): s['fx'].append(('mm_polaroid',hx,hy-6,dev)); s['fx'].append(('mm_gun',)+gun)
    if gray>0: s['fx'].append(('mm_gray',gray))
    return s

CLIPS = [clip('polaroids', N_, clip_polaroids)]
