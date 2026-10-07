"""Haikyuu!!: Claude as Hinata (the orange hair sticking up, Karasuno's black kit) in the tournament gym, in
2.5D: the court in perspective, everyone sorted by depth with a shadow under them, the net a plane across the
middle, the ball with its own height and shadow. Shiratorizawa serves; Nishinoya digs it; Kageyama gets
under it while Hinata runs in on the diagonal and leaps with his eyes shut — the freak quick — and Tendou
has already guessed wrong. Close-up, from behind him in the air: the number 10, the net and the block below,
the whole other court wide open, THE VIEW FROM THE TOP. The spike goes over Ushijima's hands and into the
floor; black crow feathers come down, the score turns to 21-19, OI, I'M HERE!"""
from engine import *

THEME = 'haikyuu'
N_ = 300                                                            # a multiple of 12: the ready bounce loops
VP, NX = 40, 92                                                     # the vanishing x, the net's world x
ORANGE, BLACK, WHITE, PURPLE = (250,140,30), (24,24,30), (244,244,244), (120,70,170)
SKIN = (246,206,170)
FLOOR, COURT, LINE = (196,150,100), (224,150,82), (250,246,236)

# ---- the projection: world x, depth z (0 = far sideline, 1 = near), height above the floor ---------------
def sc(z): return lerp(0.62,1.0,z)
def px(wx,z): return VP+(wx-VP)*sc(z)
def feet(z): return lerp(33,62,z)
def proj(wx,z,h=0): return px(wx,z), feet(z)-h*sc(z)

# ---- the players: built from a pose (arms, legs), so they all move the same way --------------------------
GW, GH, C = 20, 28, 10                                              # grid size, centre column
ARMS = {                                                             # (back hand, front hand) from the shoulders' row
 'down':((-3,'T'),(3,'T')), 'ready':((2,4),(4,4)), 'bump':((4,'T+1'),(5,'T+1')), 'set':((1,-6),(3,-6)),
 'up':((-1,-8),(3,-8)), 'back':((-7,3),(-6,4)), 'swing':((5,-6),(-1,-7)), 'hit':((-4,4),(7,-4)),
 'cheer':((-5,-7),(5,-7)), 'toss':((-6,-1),(2,-8)), 'hold':((-3,'T'),(4,2)),
}
def _number(g, at):                                                 # the number on the jersey
    c, ty = at['c'], at['ty']
    for y in (ty + 1, ty + 2): put(g, c - 1, y, 'n'); put(g, c + 1, y, 'n')

def build(who, arms='down', legs='stand', shut=False):
    """A player in a pose: legs (stand, bent, run1, run2, jump), arms (ARMS), eyes shut or not. Faces right:
    engine/people.py's figure(), with straight arms."""
    (bh, fh) = ARMS[arms]
    return figure(who, (None, bh, None, fh, 0, legs), **({'shut': True} if shut else {}))

def _kit(hair,jersey,trim,num,shorts,skin=SKIN,shoes=(236,236,240)):
    return {'h':hair,'y':(250,226,120),'s':skin,'j':jersey,'J':trim,'n':num,'p':shorts,'w':(250,250,250),'k':shoes}
def player(name, L, T, hoff, hair):
    """A volleyball player: engine/people.py's body spec (bare legs with knee pads, shorts, the jersey)."""
    return dict(name=name, w=GW, h=GH, c=C, legs=L, torso=T, head=4, hair=hair, hair_y=hoff, torso_cols=(-2, 3),
                shorts='p', leg=dict(color='s', pad='w', gap=-2, stand=(0, 0)), body=dict(collar='J'),
                arm=dict(sleeve='j', shoulders=((-3, 0), (3, 0))), paint={'body': [_number]})
HINATA   = player('hinata',   4, 4, 2, ["h..h.h.", ".hhhhhh", "hhhhhhh", "hh.h..h", "h......"])
KAGEYAMA = player('kageyama', 6, 5, 1, [".hhhhh.", "hhhhhhh", "hhhhhh.", "h......"])
NOYA     = player('noya',     4, 4, 3, ["...y...", "..hyh..", ".hhhhh.", "hhhhhhh", "hh....h"])
USHIJIMA = player('ushijima', 6, 6, 1, [".hhhhh.", "hhhhhhh", "hh...h.", "h......"])
TENDOU   = player('tendou',   7, 5, 3, ["h.h.h..", "hhhhh..", ".hhhhhh", "hhhhhhh", "h.....h"])
SERVER   = player('server',   5, 5, 1, [".hhhhh.", "hhhhhhh", "h.....h"])
K_KARASUNO = _kit(ORANGE,BLACK,WHITE,ORANGE,BLACK)
K_KAGEYAMA = _kit((20,20,26),BLACK,WHITE,ORANGE,BLACK)
K_NOYA     = _kit((20,20,26),(250,170,60),WHITE,BLACK,BLACK)    # the libero, in the other colour
K_USHIJIMA = _kit((96,84,52),WHITE,PURPLE,PURPLE,PURPLE,skin=(226,184,150))
K_TENDOU   = _kit((214,40,40),WHITE,PURPLE,PURPLE,PURPLE)
K_SERVER   = _kit((70,50,36),WHITE,PURPLE,PURPLE,PURPLE,skin=(226,184,150))


# ---- the gym ------------------------------------------------------------------------------------------
def _quad(d,wx0,wx1,z0,z1,c):
    d.polygon([proj(wx0,z0),proj(wx1,z0),proj(wx1,z1),proj(wx0,z1)],fill=c)
def _wline(d,a,b,c):
    d.line([proj(*a),proj(*b)],fill=c)

def _gym(d):
    d.rectangle([0,0,W,H],fill=(70,62,58))                          # the stands, packed
    rr=random.Random(10)
    for y in range(2,21,3):
        for x in range((y//3)%2*2,W,4):
            d.point((x,y),fill=rr.choice([(230,200,170),(60,40,30),(240,240,240),(30,30,30),(140,90,190),(250,140,30)]))
            d.point((x,y+1),fill=rr.choice([(24,24,30),(240,240,240),(140,90,190),(200,200,200)]))
    d.rectangle([0,21,W,22],fill=(150,150,156))                       # the railing, the wall
    d.rectangle([0,23,W,31],fill=(196,190,176))
    d.rectangle([4,22,32,30],fill=BLACK); text(d,"FLY",12,24,WHITE,shadow=None)       # Karasuno's banner
    d.rectangle([150,22,178,30],fill=PURPLE); text(d,"SRZ",158,24,WHITE,shadow=None)
    d.rectangle([0,31,W,H],fill=FLOOR)
    for z in (0.15,0.35,0.6,0.9): d.line([0,feet(z),W,feet(z)],fill=(184,140,92))
    _quad(d,8,176,0.06,0.96,COURT)                                   # the court and its lines
    for a,b in (((8,0.06),(176,0.06)),((8,0.96),(176,0.96)),((8,0.06),(8,0.96)),((176,0.06),(176,0.96)),
                ((NX,0.06),(NX,0.96)),((NX-30,0.06),(NX-30,0.96)),((NX+30,0.06),(NX+30,0.96))):
        _wline(d,a,b,LINE)
register_bg(THEME, lambda v: (v+120,v+90,v+50), decor=_gym)

NET_TOP, NET_LOW = 26, 13
@fx('hq_net')
def _fx_net(d,im,e,f):
    """The net: a plane across the court, see-through mesh, the white tape on top, the posts."""
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for i in range(0,31):
        z=i/30; md.line([proj(NX,z,NET_TOP),proj(NX,z,NET_LOW)],fill=150)
    for k in range(1,7):
        h=lerp(NET_LOW,NET_TOP,k/7); md.line([proj(NX,0,h),proj(NX,1,h)],fill=150)
    im.paste((30,30,36),(0,0),m); d=ImageDraw.Draw(im)
    d.line([proj(NX,0,NET_TOP),proj(NX,1,NET_TOP)],fill=WHITE,width=2); d.line([proj(NX,0,NET_LOW),proj(NX,1,NET_LOW)],fill=WHITE)
    for z in (-0.02,1.04):
        d.line([proj(NX,z,0),proj(NX,z,NET_TOP+2)],fill=(70,70,80),width=2)
    for z in (0.06,0.96):                                            # the antennae
        x,y=proj(NX,z,NET_TOP)
        for k in range(4): d.line([x,y-k*2,x,y-k*2-1],fill=(220,40,40) if k%2 else WHITE)

@fx('hq_shadow')
def _fx_shadow(d,im,e,f):
    _,wx,z,w=e; x,y=proj(wx,z); w*=sc(z)
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).ellipse([x-w,y-1,x+w,y+1],fill=80); im.paste((90,60,30),(0,0),L)

@fx('hq_figs')
def _fx_figs(d,im,e,f):
    """Players drawn under the net (Shiratorizawa, on the far side of it from us)."""
    for spr,wx,z,h,flip,pal in e[1]:
        x,y=proj(wx,z,h); draw(im,shrink(spr) if z<0.5 else spr,x,y,flip,pal=pal)

def draw_ball(d,x,y,r=2):
    x,y=int(round(x)),int(round(y))
    d.ellipse([x-r,y-r,x+r,y+r],fill=(250,214,40),outline=(30,60,150)); d.line([x-r+1,y,x+r-1,y],fill=(30,60,150))

@fx('hq_ball')
def _fx_ball(d,im,e,f):
    _,wx,z,h,trail=e; x,y=proj(wx,z,h)
    for k in range(1,int(trail)+1): d.line([x-k*4,y-k*3,x-k*4+2,y-k*3+1],fill=(255,240,180))
    draw_ball(d,x,y)

@fx('hq_ring')
def _fx_ring(d,im,e,f):
    """The impact on the floor, in perspective."""
    _,wx,z,k=e; x,y=proj(wx,z); r=(4+k*2)*sc(z)
    d.ellipse([x-r,y-r*0.3,x+r,y+r*0.3],outline=(255,240,180))

@fx('hq_feather')
def _fx_feather(d,im,e,f):
    """A black crow feather, rocking as it falls."""
    _,x,y,a=e; dx,dy=math.cos(a)*4,math.sin(a)*2
    d.polygon([(x-dx,y-dy),(x+dy*0.6,y-dx*0.3-1),(x+dx,y+dy),(x-dy*0.6,y+dx*0.3+1)],fill=(18,18,26))
    d.line([x-dx,y-dy,x+dx,y+dy],fill=(60,64,90))

@fx('hq_score')
def _fx_score(d,im,e,f):
    _,us,them,glow=e
    d.rectangle([66,1,118,9],fill=(16,16,20),outline=(90,90,96))
    c=tuple(int(lerp(v,255,glow)) for v in ORANGE)
    text(d,"KRS",68,3,(220,220,220),shadow=None); text(d,f"{us}",82,3,c,shadow=None)
    text(d,f"{them}",94,3,(190,150,230),shadow=None); text(d,"SRZ",104,3,(220,220,220),shadow=None)

@fx('hq_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(250,250,250),ink=(30,30,30))                     # the engine's bubble (engine/people.py)

# ---- close-up: from behind him, up there -------------------------------------------------------------
def closeup_top(t,f):
    """Primer plano: behind Hinata in the air — his hair and the 10 on his back, the arm cocked; below,
    the tape of the net and the block's hands that don't reach; beyond, the whole other court, wide open."""
    im=Image.new('RGB',(W,H),(70,62,58)); d=ImageDraw.Draw(im)
    rise=ease(min(1,t/0.4)); sink=int(10*rise)                        # he goes up, the world drops away
    rr=random.Random(3)
    for y in range(0,14-sink//2,3):
        for x in range((y//3)%2*2,W,4): d.point((x,y),fill=rr.choice([(230,200,170),(140,90,190),(240,240,240),(40,30,30),(250,140,30)]))
    hz=16-sink//2                                                    # the far wall / floor edge
    d.rectangle([0,hz-3,W,hz],fill=(196,190,176))
    d.polygon([(60,hz),(180,hz),(W+60,H),(20,H)],fill=FLOOR)
    d.polygon([(76,hz+2),(170,hz+2),(W+40,H+10),(40,H+10)],fill=COURT)   # their half, empty
    d.line([(76,hz+2),(170,hz+2)],fill=LINE); d.line([(76,hz+2),(40,H+10)],fill=LINE); d.line([(170,hz+2),(W+40,H+10)],fill=LINE)
    ya=hz+12; d.line([(66,ya),(178,ya)],fill=LINE)                  # their attack line
    for x,y in ((108,hz+6),(146,hz+8),(126,hz+16)):                  # two of them in the back, tiny, looking up
        d.rectangle([x,y,x+2,y+4],fill=WHITE); d.rectangle([x,y-2,x+2,y-1],fill=(70,50,36))
    ny=38+sink//3                                                    # the net's tape, under him
    d.rectangle([40,ny,W,ny+2],fill=WHITE)
    for x in range(40,W,4): d.line([x,ny+3,x,H],fill=(40,40,46))
    for hx,hc in ((96,(96,84,52)),(132,(214,40,40))):                # the block: heads, hands not reaching
        hh=ny+5-int(6*(1-rise))
        d.ellipse([hx-6,hh,hx+6,hh+12],fill=hc)
        for s in (-9,7):
            d.rounded_rectangle([hx+s,hh-6,hx+s+4,hh+4],radius=1,fill=(226,184,150),outline=(120,80,60))
    # Hinata, from behind: the shoulders in the black shirt with the 10, the arm cocked, the hair
    d.rounded_rectangle([2,40,70,H+8],radius=10,fill=BLACK,outline=(70,70,80))
    d.line([(22,41),(50,41)],fill=WHITE,width=2)                     # the collar
    big_text(im,"10",47,WHITE,scale=2,cx=36,shadow=None,outline=ORANGE); d=ImageDraw.Draw(im)
    d.line([(58,44),(64,26)],fill=BLACK,width=9)                     # the sleeve, the upper arm, the forearm
    d.line([(64,26),(66,22)],fill=SKIN,width=6); d.line([(66,22),(72,10)],fill=SKIN,width=5)
    d.ellipse([67,3,79,13],fill=SKIN,outline=(150,100,70))           # the open hand
    for k in range(3): d.line([(70+k*3,4),(71+k*3,1)],fill=SKIN,width=2)
    d.rectangle([30,36,42,44],fill=SKIN)                             # the neck
    pts=[]
    for i in range(29):                                              # the hair: a ragged mass of spikes
        a=math.pi*(0.9+i*1.2/28); r=(21 if i%2 else 13)+(3 if i%4==1 else 0)
        pts.append((36+math.cos(a)*r*1.15,26+math.sin(a)*r))
    pts+=[(56,32),(52,40),(44,38),(36,42),(28,38),(20,40),(16,32)]
    d.polygon(pts,fill=ORANGE,outline=(190,90,20))
    for k in range(6):                                               # strands
        x=20+k*6; d.line([(x,30),(x-3+k,14+(k%2)*4)],fill=(214,108,22))
    draw_ball(d,82,8,4)
    if t>=0.1:
        big_text(im,"THE VIEW",4,WHITE,scale=2,cx=140,shadow=None,outline=BLACK)
        big_text(im,"FROM THE TOP",18,WHITE,scale=2,cx=134,shadow=None,outline=BLACK)
    if t<0.05: zoom_lines(d,(255,255,255))
    return im

# ---- the rally ----------------------------------------------------------------------------------------
def arc(p0,p1,peak,t):
    """(wx, z, h) along a throw from p0 to p1 with an extra peak height."""
    t=max(0,min(1,t)); return (lerp(p0[0],p1[0],t),lerp(p0[1],p1[1],t),lerp(p0[2],p1[2],t)+4*peak*t*(1-t))

def ready(f): return 'bent' if (f//6)%2==0 else 'stand'
def run(f): return 'run1' if (f//3)%2 else 'run2'

HOME = {'hinata':(44,0.86),'kageyama':(74,0.52),'noya':(22,0.45),'ushijima':(110,0.6),'tendou':(116,0.9),'server':(174,0.5),'back':(150,0.28)}
CAST = {'hinata':(HINATA,K_KARASUNO),'kageyama':(KAGEYAMA,K_KAGEYAMA),'noya':(NOYA,K_NOYA),'ushijima':(USHIJIMA,K_USHIJIMA),
        'tendou':(TENDOU,K_TENDOU),'server':(SERVER,K_SERVER),'back':(SERVER,K_SERVER)}

def clip_quick(f):
    s=scene(f,THEME)
    P={k:dict(wx=v[0],z=v[1],h=0,arms='ready',legs=ready(f),flip=False,shut=False) for k,v in HOME.items()}
    for k in ('ushijima','tendou','server','back'): P[k]['flip']=True
    P['server'].update(arms='hold',legs='stand')
    ball=(166,0.5,8,0)                                               # in the server's hand
    score=None
    # the serve: the toss, the jump serve, over to Nishinoya
    if 14<=f<20: P['server']['arms']='toss'; ball=(170,0.5,lerp(8,30,(f-14)/6),0)
    if 20<=f<26: P['server'].update(arms='hit',legs='jump',h=4*math.sin((f-20)/6*math.pi))
    if 20<=f<40: ball=(*arc((168,0.5,30),(22,0.45,6),14,(f-20)/20),1)
    if 32<=f<46: P['noya'].update(arms='bump',legs='bent')
    if 40<=f<58: ball=(*arc((22,0.45,6),(78,0.52,20),24,(f-40)/18),0)
    # Kageyama gets under it; Hinata runs in on the diagonal and leaps, eyes shut
    if 40<=f<50: P['kageyama'].update(wx=lerp(74,78,(f-40)/10),legs=run(f))
    if 50<=f<64: P['kageyama'].update(wx=78,arms='set',legs='stand')
    if 64<=f<204: P['kageyama']['wx']=78
    if 44<=f<58: t=(f-44)/14; P['hinata'].update(wx=lerp(44,76,t),z=lerp(0.86,0.66,t),arms='back' if f>=54 else 'ready',legs=run(f))
    if 58<=f<60: P['hinata'].update(wx=76,z=0.66,arms='back',legs='bent')
    if 60<=f<130:
        t=min(1,(f-60)/8); P['hinata'].update(wx=lerp(76,82,t),z=0.66,h=22*math.sin(t*math.pi/2),arms='swing' if f>=63 else 'back',legs='jump',shut=True)
    if 58<=f<64: ball=(*arc((78,0.52,20),(88,0.66,38),2,(f-58)/6),2)
    if 64<=f<130: ball=(88,0.66,38,0)
    # Tendou guessed the other way: up and down already; Ushijima goes up late
    if 48<=f<62: P['tendou'].update(arms='up',legs='jump',h=12*math.sin((f-48)/14*math.pi))
    if 64<=f<150:
        h=6*min(1,(f-64)/6) if f<130 else (6+8*min(1,(f-130)/6) if f<140 else 14*max(0,1-(f-140)/10))
        P['ushijima'].update(arms='up',legs='jump' if h>0.5 else 'bent',h=h)
    if 70<=f<130: s['image']=closeup_top((f-70)/60,f); return s
    # the spike: over the hands, into the floor
    if 130<=f<134: P['hinata']['arms']='hit'
    if 130<=f<136: ball=(*arc((88,0.66,38),(140,0.36,0),-4,(f-130)/6),3)
    if 136<=f<160: ball=(*arc((140,0.36,0),(204,0.2,4),16,(f-136)/24),0)
    if 136<=f<150:
        s['fx'].append(('hq_ring',140,0.36,f-136))
        if f<142: s['shake']=rshake(1)
    if 136<=f<156: s['fx'].append(('dmg',"DON!",*map(int,proj(130,0.36,22)),(255,240,120)))
    if 138<=f<152: P['back'].update(wx=lerp(150,142,(f-138)/8),arms='bump',legs='bent')
    if 152<=f<200: P['back']['wx']=142
    if 200<=f<230: P['back'].update(wx=lerp(142,150,(f-200)/30),legs=run(f))
    if 134<=f<150: t=(f-134)/16; P['hinata'].update(wx=lerp(82,86,t),z=0.66,h=22*(1-t*t),arms='down',legs='jump')
    if 150<=f<156: P['hinata'].update(wx=86,z=0.66,legs='bent',arms='down')
    if 156<=f<204: P['hinata'].update(wx=86,z=0.66,arms='cheer',legs='stand' if (f//8)%2 else 'bent')
    if 156<=f<200: s['fx'].append(('hq_bubble',"OI, I'M HERE!",proj(86,0.66)[0]+4,18))
    # everyone back to their places; a ball comes back to the server
    if 204<=f<264:
        t=ease((f-204)/60); P['hinata'].update(wx=lerp(86,44,t),z=lerp(0.66,0.86,t),flip=f<262,arms='down',legs=run(f) if f<262 else 'stand')
    if 204<=f<240: P['kageyama'].update(wx=lerp(78,74,(f-204)/36),flip=True,legs=run(f),arms='down')
    if 160<=f<240: ball=None
    if 240<=f<264: ball=(*arc((200,0.62,14),(166,0.5,8),10,(f-240)/24),0); P['server']['arms']='down' if f<258 else 'hold'
    if 14<=f<276: score=(20 if f<136 else 21, max(0.0,1-(f-136)/24) if 136<=f<160 else 0.0)
    # crows' feathers over everything
    if 136<=f<236:
        rr=random.Random(7)
        for i in range(24):
            x0=rr.uniform(0,W); start=136+rr.uniform(0,40); v=rr.uniform(0.35,0.7); y=-6+(f-start)*v
            if f>=start and y<H: s['fx'].append(('hq_feather',x0+4*math.sin((f+i*7)/9),y,math.sin((f+i*5)/7)*0.8))
    # draw: shadows, Shiratorizawa, the net, Karasuno, the ball
    for k,p in P.items(): s['under'].append(('hq_shadow',p['wx'],p['z'],5))
    if ball and ball[2]<40: s['under'].append(('hq_shadow',ball[0],ball[1],2))
    far=[]; acts=[]
    for k,p in sorted(P.items(),key=lambda kv:kv[1]['z']):
        spec,pal=CAST[k]; spr=build(spec,p['arms'],p['legs'],p['shut'])
        if p['wx']>NX: far.append((spr,p['wx'],p['z'],p['h'],p['flip'],pal))
        else:
            x,y=proj(p['wx'],p['z'],p['h']); acts.append(actor(shrink(spr) if p['z']<0.5 else spr,x,y,flip=p['flip'],pal=pal))
    s['under'].append(('hq_figs',far)); s['under'].append(('hq_net',))
    if score: s['under'].insert(0,('hq_score',score[0],19,score[1]))
    s['actors']=acts
    if ball: s['fx'].insert(0,('hq_ball',*ball))
    return s

CLIPS = [clip('quick', N_, clip_quick)]
