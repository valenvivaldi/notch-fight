"""Argentina sub-theme "arg-cordoba": a cuarteto dance in Córdoba, at night, no fight. The hall under
spinning coloured lights, the band up on the stage (La Mona Jiménez himself at the front — the curly mane, bare-chested — the keyboard, the congas), the
dancers going round the floor in the ronda (in 2.5D: the circle has depth, the far side smaller, everyone
sorted front to back), the shoulders going. Claude at the bar in Belgrano's sky blue, the 2.25 l Coca
bottle cut in half on the counter (the bottom half: the waist, the five-lobed base), the fernet beside it.
Clip `fernet`: ice to the top, fernet to a third, then the Coca — close-up: nearly full, the Coca still
pouring, the light-brown foam swelling and fizzing over the ice, bubbles rising through the dark, right
to the brim and not a drop over. He raises it and joins the ronda (ARRIBA CORDOBA!), downs it, and goes
back to the bar."""
from engine import *

THEME = 'arg-cordoba'
N_ = 480                                                            # a multiple of 12, 96 (the lights), 240 (the ronda)
CX, BAR, TOPY = 50, 40, 50                                          # Claude by the bar; the counter's end and top
VX, VY = 30, 50                                                     # the cut bottle on the counter (its base)
RC, RX, RY = (124,51), 50, 8                                        # the ronda: centre, radii
INK = (14,10,16)
COCA, FOAM, FERNET = (52,22,14), (214,170,120), (26,14,10)
CELESTE = (110,190,232)

# ---- people, built from a pose --------------------------------------------------------------------------
GW, GH, C = 22, 22, 10
POSES = {   # pose -> (back elbow, back hand, front elbow, front hand, lean, legs), from (C, shoulder row)
 'stand': ((-1,3),(-1,6),(3,3),(3,6),0,'stand'),
 'dance1':((-4,2),(-3,-1),(4,2),(3,-1),1,'stance'),
 'dance2':((-4,2),(-3,-1),(4,2),(3,-1),-1,'stand'),
 'reach': ((-1,3),(-1,6),(4,1),(7,-1),1,'stand'),
 'pour':  ((-1,3),(-1,6),(4,-3),(6,-9),1,'stand'),
 'up':    ((-4,2),(-3,-1),(3,-1),(3,-6),0,'stand'),
 'updance':((-4,2),(-3,-1),(3,-1),(3,-6),1,'stance'),
 'drink': ((-1,3),(-1,6),(4,0),(2,-3),-2,'stand'),
 'walk1': ((-1,3),(-2,6),(3,3),(4,6),0,'stance'),
 'walk2': ((-1,3),(0,6),(3,3),(2,6),0,'stand'),
}

L_, T_ = 8, 6
HIP=GH-L_; TY=HIP-T_; HY=TY-5
def _skirt(g, at):                                                  # a skirt over the thighs, bare legs below
    c, hip, L = at['c'], at['hip'], at['L']
    for y in range(hip + 4, hip + L - 1): g[y] = ['s' if ch == 'p' else ch for ch in g[y]]
    for t in range(4):
        for x in range(c - 3 - t // 2, c + 4 + t // 2): put(g, x, hip + t, 'j')
def _stripes(g, at):                                                # Talleres: blue and white
    for y in range(at['ty'], at['hip']):
        o = at['sh'](y)
        for x in range(at['c'] - 3 + o, at['c'] + 3 + o):
            if (x - o) % 2: put(g, x, y, 'J')
def _bare(g, at):                                                   # bare-chested
    c, ty = at['c'], at['ty']
    for y in range(ty, at['hip'] - 1):
        o = at['sh'](y)
        for x in range(c - 3 + o, c + 3 + o): put(g, x, y, 'n' if y == ty + 2 and (x - o) in (c - 2, c + 1) else 's')
def _mouth(g, at): put(g, at['c'] + 1 + at['sh'](at['hy']), at['hy'] + 4, 'm')

def person(name, hair, sleeves=False, skirt=False, stripes=False, bare=False, hx=-3, hy=2):
    """A dancer, a musician, Claude: engine/people.py's body spec for figure()."""
    return dict(name=name, w=GW, h=GH, c=C, legs=L_, torso=T_, hair=hair, hair_x=hx, hair_y=hy,
                body=dict(hip=None if skirt else 'b'), arm=dict(sleeve='j' if sleeves else 's'),
                paint={'legs': [_skirt] if skirt else [], 'body': ([_stripes] if stripes else []) + ([_bare] if bare else []),
                       'head': [_mouth]})

def build(who, pose):
    """Someone in a pose (POSES): engine/people.py's figure()."""
    return figure(who, POSES[pose])

def hand_xy(x,feet,pose,flip=False):
    _,_,_,h,lean,_=POSES[pose]; o=round(lean*(HIP-TY)/(HIP-HY))
    hx=C+h[0]+o; return (x-GW//2+(GW-1-hx) if flip else x-GW//2+hx), feet-GH+TY+h[1]

SHORT=["..hhh..",".hhhhh.","hhhhhhh","h.....h"]
LONG =["..hhh..",".hhhhh.","hhhhhhh","hh...hh","h.....h","h.....h","h.....h"]
CLAUDE = person('claude', SHORT, sleeves=True)
CPAL = {'s':(226,180,140),'K':INK,'m':(170,80,70),'h':(40,28,22),'j':CELESTE,'b':(40,40,60),'p':(46,56,90),'k':(240,240,240)}
DANCERS = [   # (who, palette): the ronda, couple by couple
 (person('d1',LONG,skirt=True),{'s':(232,190,156),'K':INK,'m':(200,60,80),'h':(30,22,18),'j':(220,40,90),'p':(40,30,30),'k':(30,20,20)}),
 (person('d2',hair=SHORT,stripes=True,sleeves=True),{'s':(210,160,120),'K':INK,'m':(150,70,60),'h':(26,20,16),'j':(30,50,120),'J':(240,240,240),'b':(30,30,40),'p':(40,44,60),'k':(240,240,240)}),
 (person('d3',hair=LONG,skirt=True),{'s':(220,176,140),'K':INK,'m':(200,60,80),'h':(150,90,40),'j':(250,200,40),'p':(40,30,30),'k':(30,20,20)}),
 (person('d4',hair=SHORT,sleeves=True),{'s':(200,150,110),'K':INK,'m':(150,70,60),'h':(20,16,12),'j':(240,240,240),'b':(30,30,40),'p':(60,50,40),'k':(30,26,22)}),
 (person('d5',hair=LONG,skirt=True),{'s':(236,200,170),'K':INK,'m':(200,60,80),'h':(60,30,20),'j':(40,170,150),'p':(40,30,30),'k':(30,20,20)}),
 (person('d6',hair=SHORT,sleeves=True),{'s':(214,170,130),'K':INK,'m':(150,70,60),'h':(30,24,20),'j':CELESTE,'b':(30,30,40),'p':(40,44,60),'k':(240,240,240)}),
 (person('d7',hair=LONG,skirt=True),{'s':(226,184,150),'K':INK,'m':(200,60,80),'h':(20,16,14),'j':(150,70,200),'p':(40,30,30),'k':(30,20,20)}),
 (person('d8',hair=SHORT,stripes=True,sleeves=True),{'s':(230,186,150),'K':INK,'m':(150,70,60),'h':(90,60,30),'j':(30,50,120),'J':(240,240,240),'b':(30,30,40),'p':(40,44,60),'k':(30,26,22)}),
]
BAND = [(person('keys',hair=SHORT,sleeves=True),{'s':(214,170,130),'K':INK,'m':(150,70,60),'h':(20,16,14),'j':(30,30,36),'b':(20,20,24),'p':(30,30,36),'k':(20,20,24)}),
        (person('mona',bare=True,hx=-5,hy=4,hair=["..h.h.h.h..",".hhhhhhhhh.","hhhhhhhhhhh","hhhhhhhhhhh","hhh.....hhh","hh.......hh","hh.......hh","hhh.....hhh",".hh.....hh."]),   # La Mona Jiménez
         {'s':(214,160,120),'n':(150,90,60),'K':INK,'m':(120,50,40),'h':(26,20,18),'j':(214,160,120),'b':(240,240,240),'p':(20,20,24),'k':(20,20,24)}),
        (person('perc',hair=SHORT),{'s':(200,150,110),'K':INK,'m':(150,70,60),'h':(40,30,24),'j':(240,240,240),'b':(20,20,24),'p':(30,30,36),'k':(20,20,24)})]


# ---- the hall -------------------------------------------------------------------------------------------
def _hall(d):
    d.rectangle([0,0,W,H],fill=(24,16,34))
    d.rectangle([86,0,184,30],fill=(34,22,46))                       # the stage, with the band's backdrop
    for x in range(88,184,6): d.point((x,1),fill=(255,230,150))      # the bulbs along the top
    d.rectangle([84,30,184,34],fill=(80,50,40)); d.line([84,30,184,30],fill=(140,100,70))
    d.rectangle([0,34,W,H],fill=(54,40,40))                          # the floor
    for y in (40,47,55): d.line([0,y,W,y],fill=(64,48,46))
    for x,c in ((4,(30,60,30)),(10,(120,80,30)),(16,(200,200,210))):  # bottles on the shelf behind the bar
        d.rectangle([x,24,x+3,34],fill=c); d.rectangle([x+1,21,x+2,24],fill=c)
    d.line([0,35,30,35],fill=(110,80,50))
    d.rectangle([0,TOPY,BAR,H],fill=(96,60,36))                      # the bar
    d.rectangle([0,TOPY+2,BAR,TOPY+3],fill=(70,42,26)); d.line([0,TOPY,BAR,TOPY],fill=(150,100,60))
    for x in range(4,BAR,9): d.rectangle([x,TOPY+6,x+5,H],outline=(80,50,30))
register_bg(THEME, lambda v: (v+40,v+30,v+50), decor=_hall)

@fx('co_sign')
def _fx_sign(d,im,e,f):
    """The sign over the band: CUAR - TE - TO, one syllable to each beat, then all three together."""
    beat=(f//8)%4
    for i,(syl,cx) in enumerate((("CUAR",40),("-",62),("TE",76),("-",90),("TO",104))):
        k=i//2 if i%2==0 else None
        on=(k is not None and (beat==k or beat==3)) or (k is None and beat==3)
        big_text(im,syl,3 if syl!='-' else 6,(255,220,90) if on else (90,70,40),scale=2 if syl!='-' else 1,cx=cx,shadow=None)

@fx('co_lights')
def _fx_lights(d,im,e,f):
    """The coloured lights from the rig, sweeping the floor (a full turn every 96 frames)."""
    m=Image.new('RGB',(W,H),(0,0,0)); md=ImageDraw.Draw(m)
    for i,(x,c) in enumerate(((100,(255,40,120)),(130,(40,200,255)),(160,(255,220,40)),(70,(120,255,90)))):
        a=2*math.pi*((f%96)/96)+i*1.6; tx=x+math.sin(a)*70
        md.polygon([(x-2,0),(x+2,0),(tx+12,H),(tx-12,H)],fill=tuple(v//5 for v in c))
    im.paste(ImageChops_add(im,m.filter(ImageFilter.GaussianBlur(2))))

def ImageChops_add(a,b):
    from PIL import ImageChops
    return ImageChops.add(a,b)

def bottle_shape(x,y,w,h):
    """The cut-off bottom of a 2.25 l bottle, base (x,y), w wide, h tall: the cut edge at the top, the
    waist just under it, the bulge, the five-lobed foot. Outline points, round from the top left."""
    prof=((0.0,0.44),(0.08,0.40),(0.16,0.43),(0.3,0.5),(0.5,0.5),(0.7,0.5),(0.84,0.47),(0.92,0.42))   # (down, half-width)
    pts=[(x-w*hw,y-h+t*h) for t,hw in prof]
    for i in range(11):                                              # the lobes along the bottom
        t=i/10; pts.append((x-w*0.42+t*w*0.84,y-(0.0 if i%2==0 else h*0.07)))
    pts+=[(x+w*hw,y-h+t*h) for t,hw in reversed(prof)]
    return pts

def draw_vessel(im,x,y,w,h,level,foam,ice,f,big=False):
    """The cut bottle with its fernet and Coca: the dark up to level (0..1), foam on top, ice cubes."""
    pts=bottle_shape(x,y,w,h)
    mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).polygon(pts,fill=255)
    fill=Image.new('RGB',(W,H),(0,0,0)); fd=ImageDraw.Draw(fill)
    top=y-h*level; ftop=top-foam*h
    fd.rectangle([0,0,W,H],fill=(70,72,84))                          # the empty plastic
    if level>0:
        fd.rectangle([0,top,W,H],fill=COCA); fd.rectangle([0,top+h*0.2,W,H],fill=FERNET)
    if big and level>0:
        for k in range(5): fd.line([x-w*0.36+k*w*0.18,top+6,x-w*0.38+k*w*0.18,y-8],fill=(70,34,20))   # the light in it
        rr=random.Random(5)
        for i in range(26):                                          # bubbles rising through it
            bx=rr.uniform(x-w*0.38,x+w*0.38); by=y-6-((rr.uniform(0,h)+f*1.5)%max(1,y-6-top))
            fd.point((bx,by),fill=(140,80,46))
    for i,(dx,dy) in enumerate(((-0.22,0.02),(0.14,-0.02),(-0.02,0.12),(0.28,0.1))[:min(4,ice)]):   # the ice, floating
        r=w*0.12; cx,cy=x+dx*w,(ftop if foam>0 else max(top,y-h*0.9))+dy*h+r*0.3
        if level<=0: cy=y-h*0.25-(i%2)*r*1.6
        fd.rectangle([cx-r,cy-r,cx+r,cy+r],fill=(150,154,166),outline=(210,214,226))
        if big: fd.line([cx-r+2,cy-r+2,cx-r+5,cy-r+2],fill=(240,244,250))
    if foam>0:
        fd.rectangle([0,min(ftop+2,top+1),W,top+1],fill=FOAM)
        n=14 if big else 4
        for k in range(n):                                           # the foam's puffy top
            bx=x-w*0.5+k*w/(n-1); r=w*0.07+(1 if big else 0)
            fd.ellipse([bx-r,ftop-r*0.6+(math.sin(f*0.4+k)*1.2 if big else 0),bx+r,ftop+r],fill=FOAM)
        if big:
            rr=random.Random(f//3)
            for _ in range(16): fd.point((rr.uniform(x-w*0.4,x+w*0.4),rr.uniform(ftop,top)),fill=(240,212,172))
    im.paste(fill,(0,0),mask)
    d=ImageDraw.Draw(im); d.line(pts,fill=(200,204,216) if big else (170,174,186),width=2 if big else 1)
    d.line([pts[2],pts[5]],fill=(236,240,250))                       # a shine on the plastic

@fx('co_vessel')
def _fx_vessel(d,im,e,f):
    _,x,y,level,foam,ice=e; draw_vessel(im,x,y,7,10,level,foam,ice,f)

@fx('co_bottle')
def _fx_bottle(d,im,e,f):
    """A bottle standing on the bar (hand None), or held up and tipped: its mouth at (x,y) over the cut
    bottle, the body back up towards the hand, and the stream falling straight in to (x,sy)."""
    _,kind,x,y,hand,sy=e
    body=(26,20,16) if kind=='fernet' else COCA
    label=(240,230,200) if kind=='fernet' else (220,30,40)
    if hand is None: ca,sa,ox,oy=0.0,-1.0,x,y-15                    # upright: mouth at the top
    else:
        hx,hy=hand; L=math.hypot(hx-x,hy-y) or 1; ca,sa=(hx-x)/L,(hy-y)/L; ox,oy=x,y
    P=lambda u,v: (ox+u*ca-v*sa, oy+u*sa+v*ca)                       # u: from the mouth back to the base
    d.polygon([P(0,-1),P(3,-1),P(5,-3),P(15,-3),P(15,3),P(5,3),P(3,1),P(0,1)],fill=body,outline=INK)
    d.polygon([P(8,-3),P(12,-3),P(12,3),P(8,3)],fill=label)
    if kind!='fernet': d.line([P(10,-2),P(10,2)],fill=(255,255,255))
    if hand is not None and sy is not None:
        d.line([x,y+1,x,sy],fill=(60,30,18) if kind!='fernet' else (30,16,10),width=1)

@fx('co_ice')
def _fx_ice(d,im,e,f):
    _,x,y=e; d.rectangle([x-1,y-1,x+1,y+1],fill=(210,220,235),outline=(150,160,180))

@fx('co_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(244,240,232),ink=INK)                     # the engine's bubble (engine/people.py)

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_fernet(t,f):
    """Primer plano: the cut bottle, nearly full, the Coca still pouring in; the foam swells to the brim."""
    im=Image.new('RGB',(W,H),(30,20,40)); d=ImageDraw.Draw(im)
    for i,c in enumerate(((255,40,120),(40,200,255),(255,220,40))):   # the lights behind, out of focus
        x=(f*2+i*70)%(W+60)-30; d.ellipse([x-20,10+i*12,x+20,40+i*12],fill=tuple(v//4 for v in c))
    im=im.filter(ImageFilter.GaussianBlur(4)); d=ImageDraw.Draw(im)
    vx,vy,vw,vh=60,H+2,48,62
    level=lerp(0.62,0.7,t); foam=lerp(0.1,0.25,ease(t))              # the foam right up to the cut edge
    draw_vessel(im,vx,vy,vw,vh,level,foam,6,f,big=True)
    d=ImageDraw.Draw(im)
    if t<0.85:                                                       # the Coca, still going in
        ang=-0.55; ca,sa=math.cos(ang),math.sin(ang); ox,oy=72,4   # the mouth of the 2.25 l bottle, the rest up out of frame
        P=lambda u,v: (ox+u*ca-v*sa, oy+u*sa+v*ca)
        d.polygon([P(0,-3),P(6,-3),P(10,-8),P(60,-8),P(60,8),P(10,8),P(6,3),P(0,3)],fill=COCA,outline=INK)
        d.polygon([P(22,-8),P(40,-8),P(40,8),P(22,8)],fill=(220,30,40)); d.line([P(25,0),P(37,-2)],fill=(255,255,255))
        sy=vy-vh*(level+foam)
        d.line([ox,oy,68,sy],fill=(70,34,20),width=3); d.line([ox-1,oy,67,sy],fill=(120,66,40))
        for k in range(5): d.point((66+k%3,sy-1-k),fill=(240,212,172))
    if t>=0.1:
        big_text(im,"FERNET",8,(250,240,220),scale=2,cx=146,shadow=INK)
        big_text(im,"CON COCA",26,(220,30,40),scale=2,cx=146,shadow=INK)
    if t>=0.6: big_text(im,"RICASO CULIAO",46,(250,240,220),scale=1,cx=146,shadow=INK)
    if t<0.04: zoom_lines(d,FOAM)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
# (engine/stage25.py: no vanishing point, x is the screen x; the ronda is an ellipse on the floor, z 0.5 +- 0.5;
# the far half, z < 0.5, is drawn smaller)
ST = Stage(far_y=RC[1]-RY, near_y=RC[1]+RY, far_below=0.5)
def ronda_pos(a):                                                   # screen (x, y): ST.ring + feet(z) differs in the last bit
    return RC[0]+RX*math.cos(a), RC[1]+RY*math.sin(a)

def clip_fernet(f):
    s=scene(f,THEME)
    if 140<=f<220: s['image']=closeup_fernet((f-140)/80,f); return s
    s['under']+=[('co_lights',),('co_sign',)]
    figs=[]                                                          # (z, actor)
    # the ronda, couple by couple, going round (one turn per 240 frames)
    for i,(who,pal) in enumerate(DANCERS):
        a=2*math.pi*(f%240)/240+i*2*math.pi/len(DANCERS)
        x,y=ronda_pos(a); z=ST.depth(y)
        pose='dance1' if (f//6+i)%2 else 'dance2'
        figs.append((z,ST.place_at(build(who,pose),x,y,flip=math.sin(a)>0,pal=pal)))
    for k,(x,(who,pal)) in enumerate(zip((110,144,170),BAND)):        # the band, up on the stage
        pose='dance1' if (f//8+k)%2 else 'dance2'
        if who['name']=='mona':                                      # La Mona, front and centre, full size
            pose='up' if (f//12)%2 else 'dance1'; figs.append((ST.depth(31),actor(build(who,pose),x,31,pal=pal))); continue
        figs.append((ST.depth(30),ST.place_at(build(who,pose),x,30,flip=k==2,pal=pal)))
    # Claude: ice, fernet, Coca; then up, the ronda, down it in one, back to the bar
    cx,cy,pose,flip=CX,GROUND,'stand',True
    level,foam,ice=0.0,0.0,0; held=False
    if 14<=f<34: pose='reach'
    for k in range(6):                                               # the ice, a cube at a time
        t0=16+k*3
        if t0<=f<t0+5: s['fx'].append(('co_ice',VX+(k%3-1)*2,lerp(VY-16,VY-6,(f-t0)/5)))
        if f>=t0+5 and f<440: ice=k+1
    if 34<=f<78:
        pose='pour'; level=0.34*max(0,min(1,(f-40)/30))
        hx,hy=hand_xy(cx,cy,'pour',True)
        s['fx'].append(('co_bottle','fernet',VX+1,VY-12,(hx,hy),VY-10*level-1 if 40<=f<72 else None))
    if f>=78 and f<236: level=0.34
    if 78<=f<140:
        pose='pour'; t=max(0,min(1,(f-84)/52)); level=lerp(0.34,0.62,t); foam=0.1*t
        hx,hy=hand_xy(cx,cy,'pour',True)
        s['fx'].append(('co_bottle','coca',VX+1,VY-12,(hx,hy),VY-10*(level+foam)-1 if f>=84 else None))
    if 220<=f<380: level,foam=0.7,0.25
    if 220<=f<236: pose='up'; held=True
    if 236<=f<260:
        t=(f-236)/24; p0=ronda_pos(math.pi*0.6); cx,cy=lerp(CX,p0[0],t),lerp(GROUND,p0[1],t); pose='walk1' if (f//4)%2 else 'walk2'; held=True; flip=False
    if 260<=f<380:                                                   # half a turn in the ronda, the fernet up high
        a=math.pi*0.6+math.pi*(f-260)/120; cx,cy=ronda_pos(a); pose='updance' if (f//6)%2 else 'up'; held=True; flip=math.sin(a)>0
    if 270<=f<320: s['fx'].append(('co_bubble',"ARRIBA CORDOBA!",144,6,144))
    if 380<=f<400:
        cx,cy=ronda_pos(math.pi*1.6); pose='drink'; held=True; t=(f-380)/20; level,foam=0.7*(1-t),0.25*(1-t)
    if 392<=f<420: s['fx'].append(('co_bubble',"AHH!",cx,cy-34,cx))
    if 400<=f<440:
        p1=ronda_pos(math.pi*1.6); t=(f-400)/40; cx,cy=lerp(p1[0],CX,t),lerp(p1[1],GROUND,t); pose='walk1' if (f//4)%2 else 'walk2'; held=True; flip=True
    if 440<=f<448: pose='reach'; ice=0
    if 400<=f<440: ice=0; level=foam=0
    figs.append((ST.depth(cy),ST.place_at(build(CLAUDE,pose),cx,cy,flip=flip,pal=CPAL)))
    s['actors']=ST.back_to_front(figs)
    if held:
        hx,hy=hand_xy(cx,cy,pose,flip)
        s['fx'].append(('co_vessel',hx,hy+5 if pose!='drink' else hy+3,level,foam,ice))
    else: s['fx'].append(('co_vessel',VX,VY,level,foam,ice))
    s['fx'].append(('co_bottle','fernet',12,TOPY,None,None)) if not 34<=f<78 else None
    s['fx'].append(('co_bottle','coca',20,TOPY,None,None)) if not 78<=f<140 else None
    return s

CLIPS = [clip('fernet', N_, clip_fernet)]
