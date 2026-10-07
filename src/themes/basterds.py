"""Inglourious Basterds: Claude as Lt. Aldo Raine (the olive jacket, slicked hair and moustache, the rope
scar round his neck, the Bowie knife) in the French woods by the old stone tunnel; a German sergeant and a
private kneel in the leaves, two Basterds stand watch. Clip `bear`: TELL ME WHERE YOUR BOYS ARE. —
I RESPECTFULLY REFUSE, SIR. — Aldo calls into the tunnel: DONNY! Out of the dark, a bat on the stone,
louder each time: TOC... TOC... TOC. Close-up: the Bear Jew comes out of the black, the bat on his
shoulder, THE BEAR JEW. One swing (a white cut, CRACK); the Basterds whoop. Aldo crouches by the
private with his knife: THIS JUST MIGHT BE MY MASTERPIECE."""
from engine import *

THEME = 'basterds'
N_ = 384                                                            # a multiple of 12
AX, PX, SX, TUN = 34, 62, 92, 166                                   # Aldo, the private, the sergeant, the tunnel
INK = (20,16,12)
WOOD = (204,164,104)

# ---- people, built from a pose --------------------------------------------------------------------------
GW, GH, C = 28, 26, 12
POSES = {   # pose -> (back elbow, back hand, front elbow, front hand, lean, legs), from (C, shoulder row)
 'stand': ((-1,4),(-1,7),(3,4),(4,6),0,'stand'),
 'knife': ((-1,4),(-1,7),(4,3),(7,3),0,'stance'),
 'point': ((-1,4),(-1,7),(5,1),(9,0),0,'stance'),
 'call':  ((-1,4),(-1,7),(3,0),(3,-4),-1,'stance'),
 'cheer': ((-3,-2),(-4,-7),(4,-2),(5,-7),0,'stand'),
 'kneel': ((-1,4),(1,7),(3,4),(5,6),0,'kneel'),
 'crouch':((-1,4),(2,6),(4,2),(8,1),1,'crouch'),
 'walk1': ((-1,4),(-2,7),(3,4),(4,7),0,'stance'),
 'walk2': ((-1,4),(0,7),(3,4),(2,7),0,'stand'),
 'bat':   ((1,3),(3,0),(3,3),(4,0),0,'stand'),                     # the bat on his shoulder
 'wind':  ((-3,2),(-5,0),(-1,3),(-4,0),-1,'stance'),
 'swing': ((4,3),(8,2),(5,3),(9,2),2,'lunge'),
}
_put, _seg = put, seg                                               # the engine's (engine/people.py)

def _legs(g,kind,hip,L):
    """The legs from the hip: standing (stand, stance, lunge) or down (kneel, crouch)."""
    if kind in ('kneel','crouch'):
        for k,(kx,fx_) in enumerate((((-1,-6) if kind=='kneel' else (2,-2)),(4,4))):
            ky=GH-1 if (kind=='kneel' and k==0) else hip+2
            _seg(g,C-1+k*2,hip,C+kx,ky,'p'); _seg(g,C+kx+1,hip,C+kx+1,ky,'p') if kind=='crouch' else None
            if kind=='kneel' and k==0: _seg(g,C+kx,GH-1,C+fx_,GH-1,'p'); _put(g,C+fx_-1,GH-1,'k')
            else:
                _seg(g,C+kx,ky,C+fx_,GH-2,'p'); _seg(g,C+kx+1,ky,C+fx_+1,GH-2,'p')
                for x in range(C+fx_,C+fx_+3): _put(g,x,GH-1,'k')
        return
    spread={'stand':(-1,1),'stance':(-3,3),'lunge':(-5,5)}[kind]
    for k,dx in enumerate(spread):
        for t in range(L):
            x=C+round(dx*t/(L-1))+(k*2-1); c='k' if t>=L-3 else 'p'
            _put(g,x,hip+t,c); _put(g,x+1,hip+t,c)
        _put(g,C+dx+(k*2-1)+2,GH-1,'k')

_built={}
def build(who,pose):
    key=(who['name'],pose)
    if key in _built: return _built[key]
    g=[['.']*GW for _ in range(GH)]
    be,bh,fe,fh,lean,legs=POSES[pose]
    L=who['L']; down=legs in ('kneel','crouch')
    hip=GH-6 if down else GH-L; ty=hip-7; hy=ty-5
    _legs(g,legs,hip,L)
    sh=lambda y: round(lean*(hip-y)/(hip-hy))
    def arm(e,h,front):
        sx,sy=C+(2 if front else -2)+sh(ty+1),ty+1
        ex,ey=C+e[0]+sh(ty),ty+e[1]; hx,hy_=C+h[0]+sh(ty),ty+h[1]
        _seg(g,sx,sy,ex,ey,who['sleeve'] if front else who['sleeve2']); _seg(g,ex,ey,hx,hy_,who['fore'] if front else who['fore2'])
        _put(g,hx,hy_,'s'); _put(g,hx+1,hy_,'s')
    arm(be,bh,False)
    for y in range(ty,hip+1):
        o=sh(y)
        for x in range(C-3+o,C+3+o): _put(g,x,y,'B' if y==hip-1 else 'j')
        for x in who.get('straps',()): _put(g,C+x+o,y,'q')
    o=sh(ty);
    if who.get('medal'): _put(g,C-1+o,ty+2,'X')
    o=sh(hy)
    for y in range(hy,hy+5):
        for x in range(C-2+o,C+3+o): _put(g,x,y,'s')
    _put(g,C+o,hy+2,'K'); _put(g,C+2+o,hy+2,'K')
    if who.get('tache'): _put(g,C+1+o,hy+3,'m'); _put(g,C+2+o,hy+3,'m'); _put(g,C+o,hy+3,'m')
    if who.get('scar'): _put(g,C-1+o,ty,'r'); _put(g,C+o,ty,'r'); _put(g,C+1+o,ty,'r')   # the rope's scar
    for i,row in enumerate(who['hair']):
        for j,ch in enumerate(row):
            if ch!='.': _put(g,C-3+o+j,hy-len(who['hair'])+2+i,ch)
    arm(fe,fh,True)
    _built[key]=S([''.join(r) for r in g]); return _built[key]

ALDO   = dict(name='aldo',  L=9, hair=[".hhhhh.","hhhhhhh","hh....."], tache=True, scar=True,
              sleeve='j',sleeve2='J',fore='j',fore2='J')
DONNY  = dict(name='donny', L=10,hair=["h.h.h.h","hhhhhhh","hhhhhhh","hh....h"], straps=(-2,1),
              sleeve='s',sleeve2='S',fore='s',fore2='S')
SARGE  = dict(name='sarge', L=9, hair=["...cc..",".ccccc.","ccccccc","h.....c"], medal=True,
              sleeve='j',sleeve2='J',fore='j',fore2='J')
PRIVATE= dict(name='priv',  L=9, hair=[".ccccc.","ccccccc","h.....h"], sleeve='j',sleeve2='J',fore='j',fore2='J')
BASTARD= dict(name='bast',  L=9, hair=["..HHH..",".HHHHH.","HHHHHHH"], sleeve='j',sleeve2='J',fore='j',fore2='J')
APAL = {'s':(226,180,140),'K':INK,'h':(40,30,24),'m':(60,40,28),'r':(170,60,50),'j':(96,96,60),'J':(78,78,48),'B':(70,50,30),
        'p':(150,130,94),'k':(60,40,26)}
DPAL = {'s':(226,184,150),'S':(200,160,128),'K':INK,'h':(30,24,20),'j':(236,232,220),'B':(70,50,30),'q':(70,56,40),
        'p':(96,90,60),'k':(40,30,22)}
GPAL = {'s':(220,184,150),'K':INK,'h':(150,120,80),'c':(110,114,104),'j':(116,120,108),'J':(96,100,90),'B':(40,36,30),
        'p':(110,114,104),'k':(30,26,22),'X':(20,20,20)}
BPAL = {'s':(220,176,140),'K':INK,'H':(86,90,56),'j':(100,98,64),'J':(82,80,52),'B':(70,50,30),'p':(130,116,84),'k':(60,40,26)}

def hand_xy(x,feet,who,pose,flip=False):
    """Screen position of the front hand (for the bat, the knife)."""
    _,_,_,h,lean,legs=POSES[pose]; down=legs in ('kneel','crouch')
    hip=GH-6 if down else GH-who['L']; ty=hip-7; hy=ty-5; o=round(lean*(hip-ty)/(hip-hy))
    hx=C+h[0]+o; return (x-GW//2+(GW-1-hx) if flip else x-GW//2+hx), feet-GH+ty+h[1]

# ---- the woods ------------------------------------------------------------------------------------------
def _woods(d):
    for y in range(H): k=y/H; d.line([0,y,W,y],fill=(int(lerp(120,70,k)),int(lerp(140,86,k)),int(lerp(100,52,k))))
    rr=random.Random(37)
    for i in range(14):                                              # trunks, far and near
        x=rr.randint(0,W); w=rr.randint(2,6); c=(60,52,40) if w>3 else (90,86,66)
        d.rectangle([x,0,x+w,GROUND],fill=c)
    for _ in range(60): x,y=rr.randint(0,W),rr.randint(0,14); d.ellipse([x-6,y-3,x+6,y+3],fill=rr.choice([(56,80,40),(70,96,48),(46,66,34)]))
    m=Image.new('L',(W,H),0)                                         # light through the leaves
    for x in (40,96,130): ImageDraw.Draw(m).polygon([(x,0),(x+8,0),(x+30,GROUND),(x+16,GROUND)],fill=40)
    d.bitmap((0,0),m,fill=(230,220,160))
    x=TUN                                                            # the old stone tunnel, into the bank
    d.polygon([(x-22,GROUND),(x-22,20),(W,14),(W,GROUND)],fill=(110,100,80))
    d.rectangle([x-16,22,x+16,GROUND],fill=(130,124,112),outline=(80,76,70))
    d.pieslice([x-16,12,x+16,34],180,360,fill=(130,124,112),outline=(80,76,70))
    d.rectangle([x-10,26,x+10,GROUND],fill=(10,8,8)); d.pieslice([x-10,18,x+10,34],180,360,fill=(10,8,8))
    for y in range(26,GROUND,5): d.line([x-16,y,x-11,y],fill=(96,92,84)); d.line([x+11,y,x+16,y],fill=(96,92,84))
    d.rectangle([0,GROUND,W,H],fill=(96,70,40))                      # leaves on the ground
    for _ in range(80): d.point((rr.randint(0,W-1),rr.randint(GROUND,H-1)),fill=rr.choice([(150,90,40),(120,80,40),(170,120,60)]))
register_bg(THEME, lambda v: (v+70,v+50,v+20), decor=_woods)

@fx('bs_bat')
def _fx_bat(d,im,e,f):
    """The bat, from the hands at angle a (radians, 0 = right, - = up)."""
    _,x,y,a=e; ex,ey=x+math.cos(a)*14,y+math.sin(a)*14
    d.line([x,y,ex,ey],fill=INK,width=4); d.line([x,y,ex,ey],fill=WOOD,width=2)
    d.line([x,y,x+math.cos(a)*3,y+math.sin(a)*3],fill=(60,50,40),width=2)   # the taped grip
    d.ellipse([ex-2,ey-2,ex+2,ey+2],fill=WOOD,outline=INK)

@fx('bs_knife')
def _fx_knife(d,im,e,f):
    _,x,y,a=e; ex,ey=x+math.cos(a)*7,y+math.sin(a)*7
    d.line([x,y,ex,ey],fill=(220,224,230),width=2); d.point((ex,ey),fill=(255,255,255))
    d.line([x-1,y-2,x+1,y+2],fill=(150,110,60))

@fx('bs_toc')
def _fx_toc(d,im,e,f):
    """The bat on the stone in the dark: TOC, bigger and nearer each time."""
    _,n,k=e
    for i,(txt,y,sc,cx) in enumerate((("TOC...",40,1,TUN),("TOC...",22,2,TUN-36),("TOC!",2,3,TUN-80))[:n]):
        big_text(im,txt,y,(240,230,200),scale=sc,cx=cx,shadow=INK)

@fx('bs_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(244,238,220),ink=INK)                     # the engine's bubble (engine/people.py)

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_bear(t,f):
    """Primer plano: out of the black of the tunnel — the curls, the stare, the vest, the bat on his
    shoulder — THE BEAR JEW."""
    im=Image.new('RGB',(W,H),(8,6,6)); d=ImageDraw.Draw(im)
    x0=24
    d.rectangle([x0-16,46,x0+50,H],fill=DPAL['j'],outline=INK)      # the vest, the shoulders
    for sx in (x0-6,x0+38): d.rectangle([sx,46,sx+4,H],fill=(226,184,150))
    d.line([x0-2,46,x0-2,H],fill=DPAL['q'],width=3); d.line([x0+34,46,x0+34,H],fill=DPAL['q'],width=3)
    d.rectangle([x0+6,6,x0+30,46],fill=DPAL['s'],outline=INK)       # the face
    for k in range(8): d.ellipse([x0+2+k*4-2,0,x0+2+k*4+4,10],fill=DPAL['h'])   # the curls
    d.rectangle([x0+6,6,x0+30,9],fill=DPAL['h'])
    for ex in (x0+11,x0+22): d.rectangle([ex,18,ex+4,21],fill=INK); d.line([ex-1,15,ex+5,16],fill=DPAL['h'],width=2)   # the stare, brows down
    d.line([x0+12,36,x0+24,36],fill=(120,70,60),width=2)
    for k in range(12): d.point((x0+8+k*2,30+(k%3)),fill=(80,60,50))   # stubble
    d.line([x0+40,50,x0+90,2],fill=INK,width=8); d.line([x0+40,50,x0+90,2],fill=WOOD,width=6)   # the bat
    d.ellipse([x0+84,-4,x0+98,8],fill=WOOD,outline=INK)
    a=min(1,t/0.4)                                                   # he comes out of the dark
    im=Image.blend(Image.new('RGB',(W,H),(8,6,6)),im,a); d=ImageDraw.Draw(im)
    if t>=0.25:
        big_text(im,"THE",8,(240,230,200),scale=2,cx=134,shadow=INK)
        big_text(im,"BEAR JEW",26,(240,230,200),scale=3,cx=130,shadow=INK)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
def clip_bear(f):
    s=scene(f,THEME)
    if 200<=f<260: s['image']=closeup_bear((f-200)/60,f); return s
    if 292<=f<296: s['image']=Image.new('RGB',(W,H),(250,248,240)); return s   # the swing: a white cut
    apose,akn='knife',0.2; dx,dpose,dvis=None,'bat',False; sarge='kneel'; cheer=False
    if 14<=f<74: apose='point'; s['fx'].append(('bs_bubble',["TELL ME WHERE","YOUR BOYS ARE."],AX+10,8,AX+8))
    if 78<=f<124: s['fx'].append(('bs_bubble',["I RESPECTFULLY","REFUSE, SIR."],SX,6,SX+2))
    if 128<=f<160: apose='call'; s['fx'].append(('bs_bubble',"DONNY!",AX+14,10,AX+8))
    if 150<=f<200:                                                   # the bat on the stone, in the dark
        n=1+(f>=166)+(f>=182); s['fx'].append(('bs_toc',n,f))
        for hit in (150,166,182):
            if hit<=f<hit+3: s['shake']=rshake(1 if hit<182 else 2)
    if 260<=f<292:                                                   # he walks out to the sergeant
        dvis=True; t=(f-260)/22; dx=lerp(TUN,SX+17,min(1,t)); dpose=('walk1' if (f//5)%2 else 'walk2') if t<1 else 'bat'
        if f>=284: dpose='wind'
    if 296<=f<372:
        dvis=True; dx=SX+17; dpose='swing' if f<304 else 'bat'; sarge='down'; cheer=f<336
        if f<310: s['fx'].append(('big',"CRACK",4,(240,230,200),SX+10)); s['shake']=rshake(2) if f<300 else (0,0)
    if 316<=f<372:                                                   # Aldo, by the private, with his knife
        apose='crouch'
        big_text_lines=(("THIS JUST MIGHT BE",2),("MY MASTERPIECE.",18))
        for txt,y in big_text_lines: s['fx'].append(('big',txt,y,(240,230,200)))
    ax=AX if not 316<=f<372 else lerp(AX,PX-13,min(1,(f-316)/14))
    acts=[actor(build(BASTARD,'cheer' if cheer and (f//6)%2 else 'stand'),14,pal=BPAL),
          actor(build(BASTARD,'cheer' if cheer and (f//6+1)%2 else 'stand'),138,flip=True,pal=BPAL)]
    if sarge=='kneel': acts.append(actor(build(SARGE,'kneel'),SX,flip=True,pal=GPAL))
    else: acts.append(actor(rotate90(build(SARGE,'stand'),3,trim=True),SX-4,pal=GPAL))       # down in the leaves
    acts.append(actor(build(PRIVATE,'kneel'),PX,flip=True,pal=GPAL))
    acts.append(actor(build(ALDO,apose),ax,pal=APAL))
    if dvis: acts.append(actor(build(DONNY,dpose),dx,flip=True,pal=DPAL))
    s['actors']=acts
    hx,hy=hand_xy(ax,GROUND,ALDO,apose)
    s['fx'].insert(0,('bs_knife',hx+1,hy,-0.4 if apose!='crouch' else -0.9))
    if dvis:
        bx,by=hand_xy(dx,GROUND,DONNY,dpose,flip=True)
        ang={'bat':-2.2,'walk1':-2.2,'walk2':-2.2,'wind':-0.6,'swing':math.pi+0.3}[dpose]
        s['fx'].insert(0,('bs_bat',bx,by,ang))
    if 360<=f<372: s['image']=fade_to(render(s,f),(0,0,0),(f-360)/12)
    if 372<=f: s['image']=fade_to(render(s,f),(0,0,0),1-(f-372)/12)
    return s

CLIPS = [clip('bear', N_, clip_bear)]
