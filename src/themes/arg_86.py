"""Argentina sub-theme "arg-86": Mexico 1986, Argentina 2-1 England, at the Azteca under the sun.
Claude as Diego - the '86 albiceleste, curly dark hair, the captain's armband. Two clips on the same
neutral pose (the ball in the centre circle), with the TV scoreboard (ARG-ING and the minute):
  mano  - a one-two with Valdano, Hodge hooks it back and it loops towards his own keeper; Diego goes up
          with the taller Shilton; close-up: the fist gets there first. The English surround the referee,
          Shilton points at his hand, Diego celebrates with a sideways look: LA MANO DE DIOS.
  siglo - he spins between two Englishmen in his own half, then runs - the camera follows him up the
          pitch past a sliding tackle, a lunge and one more, round Shilton, Butcher's tackle from behind
          as he scores. The commentary as captions: TA TA TA TA, GOLAZO, BARRILETE COSMICO,
          DE QUE PLANETA VINISTE.
England: generic figures in white, the keeper in grey - kit colours, never likenesses."""
from engine import *
from themes.arg import PLAYER, DIVE, KIT_ARG, CELESTE, WHITE, albiceleste, draw_goal   # same country

THEME = 'arg-86'
N_MANO, N_SIGLO = 280, 420

GOLD = (250,210,60)
DPAL = {'c':CELESTE, 'W':WHITE, 'b':(24,24,28), 'y':(236,200,60), 'h':(30,24,22), 'H':(56,44,40)}
KIT_ENG  = {'j':(240,240,240), 'J':(240,240,240), 's':(226,184,150), 'h':(120,80,50), 'p':(30,40,90)}
KIT_KEEP = {'j':(120,120,128), 'J':(120,120,128), 's':(226,184,150), 'h':(90,70,50), 'p':(40,40,48)}
KIT_REF  = {'j':(30,30,34), 'J':(30,30,34), 's':(210,160,120), 'h':(40,30,26), 'p':(30,30,34)}
CROWD = ((116,172,223),(240,240,240),(220,60,60),(240,200,60),(60,60,70),(116,172,223))

CURLS = ["h.H.hh.H.h..", ".hhHhhhhHhh.", "hHhhhhhhhhHh"]
DIEGO=variant(lambda s: albiceleste(overlay(s,CURLS,-1,0)))
# Shilton: a head taller than everyone (extra leg rows)
_tall=[r for r in PLAYER['idle']]; _tall=_tall[:13]+_tall[13:15]*2+_tall[13:]
TALL=poses(S(_tall),7,'s',3)

register_bg(THEME, lambda v: (v//2+40,v+30,v//3+10))       # the field itself is drawn by a86_field (it scrolls)

# ---------------------------------------------------------------- the Azteca, with a camera
@fx('a86_field')
def _fx_field(d,im,e,f):
    """Sky, packed tiers, a sun-bleached striped pitch and its lines, all at camera position cam
    (world x = screen x + cam; the stands move at half speed). goal: world x of the goal."""
    _,cam,goal=e; cam=int(cam)
    for y in range(0,12):
        t=y/12; d.line([0,y,W,y],fill=(int(lerp(120,170,t)),int(lerp(180,210,t)),int(lerp(236,240,t))))
    d.rectangle([0,12,W,28],fill=(96,90,86))
    sc=cam//2
    for y in range(13,28,2):
        for x in range((y//2)%2,W,3):
            col=(x+sc)//3
            if (col*7+y*13)%10<8: d.point((x,y),fill=CROWD[(col*5+y*3)%len(CROWD)])
    for x in range(W):
        d.line([x,29,x,GROUND],fill=(122,152,78) if ((x+cam)//8)%2 else (110,140,70))
    d.line([0,28,W,28],fill=(240,240,230))
    for wx in (20,):                                                                        # halfway line, circle
        sx=wx-cam
        if -40<sx<W: d.line([sx,28,sx,GROUND],fill=(240,240,230)); d.arc([sx-16,32,sx+16,GROUND+10],-60,60,fill=(240,240,230))
    bx=goal-26-cam
    if 0<bx<W: d.line([bx,34,bx,GROUND],fill=(240,240,230)); d.point((goal-16-cam,50),fill=(240,240,230))
    if goal-cam<W+10: draw_goal(d,goal-cam,1)
    _fx_boards(d,im,('a86_boards',cam),f)

@fx('a86_hud')
def _fx_hud(d,im,e,f):
    """TV scoreboard: ARG a-e ING and the minute."""
    _,a,g,minute=e
    d.rounded_rectangle([3,3,72,11],radius=2,fill=(16,16,22),outline=(90,90,110))
    d.rectangle([5,5,7,9],fill=CELESTE)
    text(d,f"ARG {a}-{g} ING",10,4,(236,236,236),shadow=None)
    d.rectangle([58,4,71,10],fill=(40,40,56)); text(d,str(minute),61,4,GOLD,shadow=None)

@fx('a86_trail')
def _fx_trail(d,im,e,f):
    """Speed streaks behind Diego's run."""
    _,x,y=e
    for k in range(4): d.line([x-10-k*5,y-4-k*2,x-4-k*5,y-4-k*2],fill=(250,250,240))

@fx('a86_swirl')
def _fx_swirl(d,im,e,f):
    """Dust swirling round the spin."""
    _,x,y,k=e
    for i in range(6):
        a=k*0.6+i*1.05; r=6+k*0.6; d.point((int(x+math.cos(a)*r),int(y+math.sin(a)*r*0.4)),fill=(200,190,150))

@fx('a86_turf')
def _fx_turf(d,im,e,f):
    """Grass and dirt kicked up by a sliding tackle."""
    _,x,y,k=e; rr=random.Random(int(x)*7)
    for _ in range(8):
        vx=rr.uniform(-2,2); vy=rr.uniform(-3,-1); px=x+vx*k; py=y+vy*k+0.2*k*k
        if py<GROUND: d.point((int(px),int(py)),fill=(90,140,60) if rr.random()<0.6 else (140,110,70))

@fx('a86_caption')
def _fx_caption(d,im,e,f):
    """The commentary running along the top, as it's shouted."""
    _,txt=e; w=len(txt)*4+6; x=W//2-w//2+20
    d.rectangle([x,2,x+w,11],fill=(250,210,60),outline=(20,16,16)); text(d,txt,x+3,4,(20,16,16),shadow=None)

@fx('a86_big')
def _fx_big(d,im,e,f):
    _,txt,y,c=e; big_text(im,txt,y,c,shadow=(0,0,0),outline=(0,0,0))

@fx('a86_point')
def _fx_point(d,im,e,f):
    """Shilton tapping his hand: a small raised hand with motion marks."""
    _,x,y=e
    if (f//4)%2: d.rectangle([x-1,y-2,x+1,y],fill=(250,250,250)); d.line([x+3,y-3,x+5,y-5],fill=(250,250,250))

# ---------------------------------------------------------------- close-ups
def closeup_hand(t,f):
    """Primer plano: in the air - Diego's curls under his raised left fist, Shilton's head and gloves
    behind; the fist gets there first."""
    im=Image.new('RGB',(W,H),(150,196,238)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([0,y,W,y],fill=(int(lerp(130,176,y/H)),int(lerp(186,214,y/H)),int(lerp(236,242,y/H))))
    d.ellipse([150,4,176,30],fill=(255,244,200))                                           # the sun
    rise=ease(min(1,t/0.35))
    # Shilton, behind and taller: head, grey shoulder, gloves reaching
    sy=int(lerp(H+20,30,rise))
    d.rectangle([108,min(sy+10,H+4),150,H+5],fill=KIT_KEEP['j'])
    gx,gy=int(lerp(W,112,rise)),int(lerp(H,8,rise))
    d.line([146,sy+14,gx+8,gy+8],fill=KIT_KEEP['j'],width=8)                             # the arm, behind the head
    d.ellipse([112,sy-8,138,sy+14],fill=KIT_KEEP['s']); d.rectangle([112,sy-8,138,sy-2],fill=KIT_KEEP['h'])
    d.rectangle([118,sy+1,122,sy+4],fill=(24,14,12)); d.rectangle([128,sy+1,132,sy+4],fill=(24,14,12))
    d.rounded_rectangle([gx-4,gy-4,gx+14,gy+10],radius=4,fill=(250,250,250),outline=(80,80,80))
    # Diego, in front: the curls, the face looking up, the albiceleste sleeve, the left fist
    dy=int(lerp(H+20,34,rise))
    top=min(dy+10,H+4)
    d.rectangle([52,top,90,H+5],fill=WHITE)
    for x in range(52,90,8): d.rectangle([x,top,x+3,H+5],fill=CELESTE)
    fx_,fy=int(lerp(40,92,rise)),int(lerp(H,14,rise))
    for k in range(5): d.line([84+k*2,dy+12,fx_-6+k*2,fy+10],fill=CELESTE if k%2 else WHITE,width=2)   # the arm, behind the head
    d.rectangle([58,dy-6,86,dy+16],fill=(217,119,87)); d.rectangle([82,dy-6,86,dy+16],fill=(168,80,54))
    d.ellipse([54,dy-16,90,dy],fill=DPAL['h'])
    for k in range(6): d.ellipse([54+k*6,dy-18,60+k*6,dy-10],fill=DPAL['H'])
    d.rectangle([64,dy+1,68,dy+5],fill=(24,14,12)); d.rectangle([76,dy+1,80,dy+5],fill=(24,14,12))
    d.rounded_rectangle([fx_-8,fy-6,fx_+6,fy+8],radius=4,fill=(217,119,87),outline=(120,60,40))
    for k in range(3): d.line([fx_+6,fy-3+k*4,fx_+2,fy-3+k*4],fill=(168,80,54))
    # the ball: dropping in, off the fist, away (right, down)
    if t<0.35: bx,by=lerp(100,98,t/0.35),lerp(-10,10,t/0.35)
    else: q=min(1,(t-0.35)/0.35); bx,by=lerp(98,W+10,q),lerp(10,40,q)
    d.ellipse([bx-5,by-5,bx+5,by+5],fill=(250,250,250),outline=(40,40,40)); d.point((int(bx),int(by)),fill=(40,40,40))
    if 0.33<t<0.42: spark(d,96,12,5,(255,255,255))
    if t<0.06: zoom_lines(d)
    return im

def closeup_joy(t,f):
    """Primer plano: Diego celebrating, arms up, the crowd behind; BARRILETE COSMICO, then
    DE QUE PLANETA VINISTE."""
    im=Image.new('RGB',(W,H),(96,90,86)); d=ImageDraw.Draw(im)
    rr=random.Random(10+f//4)
    for _ in range(160): d.point((rr.randint(0,W),rr.randint(0,H)),fill=rr.choice(CROWD))
    cx=40
    for sx in (-1,1):
        d.line([cx+sx*16,44,cx+sx*26,12],fill=CELESTE,width=6)
        d.ellipse([cx+sx*26-5,4,cx+sx*26+5,14],fill=(217,119,87),outline=(120,60,40))
    d.rectangle([cx-20,38,cx+20,H],fill=WHITE)
    for x in range(cx-20,cx+20,8): d.rectangle([x,38,x+3,H],fill=CELESTE)
    d.rectangle([cx-16,10,cx+16,40],fill=(217,119,87)); d.rectangle([cx+12,10,cx+16,40],fill=(168,80,54))
    d.ellipse([cx-20,2,cx+20,18],fill=DPAL['h'])
    for k in range(7): d.ellipse([cx-20+k*6,0,cx-14+k*6,8],fill=DPAL['H'])
    d.rectangle([cx-10,22,cx-6,27],fill=(24,14,12)); d.rectangle([cx+4,22,cx+8,27],fill=(24,14,12))
    d.chord([cx-8,28,cx+8,38],0,180,fill=(70,20,20))
    if 0.05<=t<0.5:                                                                        # 2 s each
        big_text(im,"BARRILETE",10,(250,250,250),cx=124,shadow=(0,0,0),outline=(0,0,0))
        big_text(im,"COSMICO",28,CELESTE,cx=124,shadow=(0,0,0),outline=(0,0,0))
    if t>=0.52:
        big_text(im,"DE QUE PLANETA",10,(250,250,250),cx=124,shadow=(0,0,0),outline=(0,0,0))
        big_text(im,"VINISTE",28,GOLD,cx=124,shadow=(0,0,0),outline=(0,0,0))
    if t<0.05: zoom_lines(d)
    return im

# ---------------------------------------------------------------- clip 1: la mano de Dios
def clip_mano(f):
    s=scene(f,THEME)
    # the camera: at the centre circle for the neutral pose (like siglo), then it pans up to the box with
    # Diego; the play below is written in box-view coordinates, shifted by what the pan hasn't covered yet
    cam=180*ease((f-14)/26) if 14<=f<40 else (180 if 40<=f<250 else 0)
    shift=180-cam if 14<=f<40 else 0
    s['under'].insert(0,('a86_field',cam,356))
    dx,dy,dpose,dflip=40,GROUND,guard_pose(f),False
    ball=(49,GROUND-2) if f<14 or f>=250 else None
    others=[]
    vx,hx,kx,ky,kpose=130,146,170,GROUND,'idle'                     # Valdano, Hodge, Shilton
    if 14<=f<250: s['fx'].append(('a86_hud',1 if f>=132 else 0,0,51))
    # the one-two: Diego to Valdano, Hodge hooks it back, it loops towards his own keeper
    if 14<=f<40: dx,dpose=ez(40,100,(f-14)/26),'dash'; ball=(dx+9,GROUND-2)
    if 40<=f<46: dx=100; ball=(lerp(109,126,(f-40)/6),GROUND-2)
    if 46<=f<52: ball=(lerp(126,142,(f-46)/6),GROUND-3)
    if 52<=f<84: p=(f-52)/32; ball=(lerp(142,164,p),lerp(GROUND-4,26,p)-34*math.sin(p*math.pi))
    if 46<=f<76: dx,dpose=ez(100,156,(f-46)/30),'dash'
    # up they go: the taller keeper comes off his line, Diego leaps higher
    if 72<=f<86:
        p=min(1,(f-72)/10); dx=156; dy=GROUND-24*math.sin(p*math.pi/2); dpose='armsup'
        kx=lerp(170,164,p); ky=GROUND-10*math.sin(p*math.pi/2); kpose='attack'
    if 86<=f<132: s['image']=closeup_hand((f-86)/46,f); return s
    # the goal; the English protest round the referee; Diego's sideways look
    if 132<=f<146: ball=(180,40); s['fx'].append(('arg_net',182,40,f-132))
    if 132<=f<160: dx,dflip,dpose=ez(156,78,(f-132)/28),True,'armsup'
    if 160<=f<210: dx,dpose,dflip=78,'armsup' if (f//10)%2 else guard_pose(f),(f//16)%2==0     # glancing back
    protest=132<=f<236
    if protest:
        others.append(actor(PLAYER['attack'],104,pal=KIT_REF,flip=True))                        # pointing to the centre
        for x in (118,132): others.append(actor(PLAYER['attack'],x,flip=True,pal=KIT_ENG,alpha=1 if f<216 else max(0,1-(f-216)/20)))
        kx,kpose=150,'attack'; s['fx'].append(('a86_point',152,GROUND-16))
    if 160<=f<210:                                                                               # 2.5 s
        s['fx'].append(('a86_big',"LA MANO",14,(250,250,250))); s['fx'].append(('a86_big',"DE DIOS",30,CELESTE))
    if 210<=f<250: dx,dflip,dpose=ez(78,40,(f-210)/40),True,guard_pose(f)
    if f>=250: dx,dflip=40,False
    if 14<=f<132: others.append(actor(PLAYER['attack' if 40<=f<46 else 'idle'],vx,pal=KIT_ARG))
    if 14<=f<132: others.append(actor(PLAYER['attack' if 46<=f<52 else 'idle'],hx,flip=True,pal=KIT_ENG))
    if 14<=f<236: others.append(actor(TALL[kpose],kx,ky,flip=True,pal=KIT_KEEP,alpha=1 if f<216 else max(0,1-(f-216)/20)))
    if ball: s['fx'].append(('arg_ball',)+ball)                                   # at his feet: already in screen space
    for a in others: a['x']+=shift
    s['actors']=others+[actor(DIEGO[dpose],dx,dy,flip=dflip,pal=DPAL)]
    return s

# ---------------------------------------------------------------- clip 2: el gol del siglo (2.5D)
# Depth: z 0 = the far side of the pitch, 1 = the near side. Feet sit higher up the grass the farther
# they are; far figures are drawn 3/4 size and a little faded; everything is sorted back to front and
# moves with a touch of parallax. Diego weaves between lanes, always to the side away from the man.
GOAL=356                                     # world x of England's goal
AHEAD=((150,'slide',0.35),(210,'lunge',0.8),(262,'lunge',0.45))   # (world x, kind, depth) up the pitch
WEAVE=((40,1.0),(80,0.7),(128,0.6),(150,0.88),(188,0.7),(210,0.32),(240,0.55),(262,0.82),(330,0.6),(344,0.6))

def feet_of(z): return int(lerp(46,GROUND,z))

from engine import people
def shrink(spr,k=0.75):
    """A 3/4-size copy of a sprite grid (the engine's, at 3/4)."""
    return people.shrink(spr,k)

def place(spr,wx,z,cam,flip,pal,alpha=1.0,lift=0):
    """An actor at world x / depth z: parallax, size, fade and feet line from the depth."""
    sx=wx-cam*lerp(0.9,1.0,z); far=z<0.5
    return actor(shrink(spr) if far else spr,sx,feet_of(z)-lift,flip=flip,pal=pal,alpha=alpha*(0.82 if far else 1.0)), sx

@fx('a86_shadow')
def _fx_shadow(d,im,e,f):
    """A soft shadow on the grass under a figure or the ball."""
    _,x,y,w=e; L=Image.new('L',(W,H),0); ImageDraw.Draw(L).ellipse([x-w,y-1,x+w,y+1],fill=90)
    im.paste((40,60,30),(0,0),L)

@fx('a86_boards')
def _fx_boards(d,im,e,f):
    """Advertising boards along the far touchline, sliding at their own speed."""
    _,cam=e; off=int(cam*0.8)
    cols=((200,40,40),(240,240,240),(30,60,140),(240,200,40),(40,120,60))
    for i in range(-1,W//18+2):
        k=(i+off//18)%len(cols); x=i*18-off%18
        d.rectangle([x,29,x+16,32],fill=cols[k]); d.line([x+3,30,x+12,30],fill=(250,250,250) if k!=1 else (40,40,40))

def diego_world(f):
    """Diego's world x: the spin at the halfway line, then the run up to the goal."""
    if f<40: return 40
    if f<250: return lerp(40,330,ease((f-40)/210)*0.35+((f-40)/210)*0.65)
    if f<262: return lerp(330,344,(f-250)/12)
    return 344

def diego_depth(wx):
    """The weave: his lane at world x, eased between the keyframes."""
    for (x0,z0),(x1,z1) in zip(WEAVE,WEAVE[1:]):
        if x0<=wx<=x1: return lerp(z0,z1,ease((wx-x0)/max(1,x1-x0)))
    return WEAVE[-1][1]

def clip_siglo(f):
    s=scene(f,THEME)
    wx=diego_world(f); dz=diego_depth(wx)
    cam=max(0,min(180,wx-70)) if f<380 else 0
    s['under'].insert(0,('a86_field',cam,GOAL))
    dpose,dflip='dash' if 40<=f<262 else guard_pose(f),False
    hop=abs(math.sin(f*0.8))*3 if 22<=f<250 else 0                       # the ball bobbing off his foot
    ball=(wx+9,dz,hop) if 22<=f<262 else None
    figs=[]                                                                # (spr, world x, z, flip, pal, alpha)
    if 14<=f<360: s['fx'].append(('a86_hud',2 if f>=270 else 1,0,55))
    # the pass arrives; two close in from either side and he spins between them
    if 14<=f<22: ball=(lerp(4,40,(f-14)/8),1.0,0)
    for i,(x0,z0) in enumerate(((58,0.45),(66,0.85))):
        if f<40:
            z=lerp(z0+(0.2 if i==0 else -0.2),z0,min(1,(f-14)/16)) if f>=14 else z0
            figs.append((PLAYER['attack' if 34<=f<40 else 'idle'],lerp(x0+30,x0,min(1,max(0,(f-14)/16))),z,True,KIT_ENG,1))
        elif i==0 and f<200: figs.append((DIVE,x0,z0,True,KIT_ENG,1))
    if 30<=f<40: dflip=(f//2)%2==1; s['fx'].append(('a86_swirl',40-cam,feet_of(dz)-3,f-30))
    # the ones up the pitch: each steps across into his lane, and is left on the grass
    ta=0
    for x0,kind,z0 in AHEAD:
        reach=x0-16
        if wx<reach-24: figs.append((PLAYER['idle'],x0,z0,True,KIT_ENG,1))
        elif wx<reach: figs.append((PLAYER['idle'],x0,lerp(z0,dz,0.5*(wx-reach+24)/24),True,KIT_ENG,1))
        elif wx<x0+2:
            zz=lerp(z0,dz,0.5); ta+=1
            figs.append((DIVE if kind=='slide' else PLAYER['attack'],x0-4,zz,True,KIT_ENG,1))
            if kind=='slide': s['fx'].append(('a86_turf',x0-4-cam,feet_of(zz)-2,int(wx-reach)))
        else: figs.append((DIVE,x0+2,lerp(z0,dz,0.5),True,KIT_ENG,1)); ta+=1
    # the chaser, near side, who tackles as he shoots
    if 40<=f<262: figs.append((PLAYER['idle'] if f<258 else DIVE,lerp(66,wx-18,min(1,(f-40)/200)),0.92,False,KIT_ENG,1))
    if 262<=f<330: figs.append((DIVE,wx-14,0.92,False,KIT_ENG,1))
    # Shilton comes out, is sent the wrong way
    kz=0.6 if f<240 else lerp(0.6,0.4,min(1,(f-240)/10))
    figs.append((TALL['idle'] if f<252 else DIVE,GOAL-12 if f<240 else lerp(GOAL-12,GOAL-22,min(1,(f-240)/10)),kz,True,KIT_KEEP,1))
    if 250<=f<262: dpose='guard' if (f//3)%2 else 'dash'
    if 258<=f<266: ball=(lerp(wx+9,GOAL+2,(f-258)/8),lerp(dz,0.6,(f-258)/8),0)
    if 266<=f<280: ball=(GOAL+2,0.6,0); s['fx'].append(('arg_net',GOAL+4-cam,feet_of(0.6)-4,f-266))
    if 262<=f<300: dpose,dflip='armsup',(f//12)%2==1
    if 40<=f<262 and ta: s['fx'].append(('a86_caption',' '.join(['TA']*(ta+1))))
    if 270<=f<300: s['fx'].append(('a86_big',"GOLAZO",20,GOLD))                          # 1.5 s
    if 300<=f<380: s['image']=closeup_joy((f-300)/80,f); return s
    # back to the centre circle
    if 380<=f<410:
        s['fx'].append(('arg_confetti',f-380,1-(f-380)/30))
        wx,dz,dflip,dpose=ez(120,40,(f-380)/30),1.0,True,guard_pose(f); figs=[]
    neutral=f>=410 or f<14
    if neutral: wx,dz,dflip,dpose=40,1.0,False,guard_pose(f); figs=[]; ball=(49,1.0,0)
    figs.append((DIEGO[dpose],wx,dz,dflip,DPAL,1))
    acts=[]
    for spr,x,z,flip,pal,a in sorted(figs,key=lambda t:t[2]):                # back to front
        act,sx=place(spr,x,z,cam,flip,pal,a)
        if -14<sx<W+14:
            if not neutral: s['under'].append(('a86_shadow',sx,feet_of(z),5 if z<0.5 else 7))   # the neutral pose matches mano
            acts.append(act)
    if 40<=f<262: s['under'].append(('a86_trail',wx-cam*lerp(0.9,1.0,dz),feet_of(dz)))
    if ball:
        bx,bz,bh=ball; bsx=bx-cam*lerp(0.9,1.0,bz); by=feet_of(bz)
        if not neutral: s['under'].append(('a86_shadow',bsx,by,2))
        s['fx'].append(('arg_ball',bsx,by-2-bh))
    s['actors']=acts
    return s

CLIPS = [clip('mano', N_MANO, clip_mano), clip('siglo', N_SIGLO, clip_siglo)]
