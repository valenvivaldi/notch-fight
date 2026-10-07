"""Mistborn sub-theme "mist-kelsier": Claude as Kelsier, the Survivor of Hathsin (the Pits' scars on his
arms), in Luthadel's Fountain Square under the red sun, a crowd of skaa watching. A Steel Inquisitor
drops in; Kelsier hops the axe, rains coins on him from the air and puts him down with a pewter punch.
Then THE LORD RULER walks in. Kelsier charges and the Lord Ruler runs him through with a spear. Close-up:
Kelsier smiles at him — THERES ALWAYS ANOTHER SECRET. He falls; the Lord Ruler walks off; one by one
the skaa raise their hands. The mists roll in, and Kelsier stands up out of them for the loop."""
from engine import *
from themes.mist import INQ, IPAL, LINE_HI          # same series: the Inquisitor; its fx (mist_*) are registered there

THEME = 'mist-kelsier'
DEFAULT_OFF = True            # niche (books), like mist
N_ = 360
CX = 30                       # the loop keyframe position
IX, LX = 150, 140             # where the Inquisitor lands; where the Lord Ruler stops

SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
# Kelsier: light swept-back hair, dark clothes, white scars up his arms
KPAL = {'l':(196,164,104), 'f':(232,206,146), 'a':(52,50,62), 'i':(38,36,46), 'c':(246,232,214)}
# the Lord Ruler: black hair, black coat over a white shirt, gold feruchemical bracers
LPAL = {'y':(236,196,80)}
HAIR = ["...lfllll...", "..llllllfl..", ".lllllllll.."]

def _kelsier(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and top+5<=y<top+9: g[y][x]='a' if y<top+8 else 'i'
            elif c=='o' and y<top+8 and (x<l or x>r) and (x+y)%2==0: g[y][x]='c'   # the scars of the Pits
    return S([''.join(x) for x in g])
KEL=variant(_kelsier)

LR=poses(S([
".....ZZZZZ......","....ZZZZZZZ.....","....ZZsssss.....","....Z.sKssK.....","......sssss.....",
"......sssss.....",".......sss......",".....bbWWbbb....","....bbbWWbbbb...","...bbbbWWbbbbb..",
"...bb.bWWbb.bb..","...bb.bWWbb.bb..","...bb.bbbbb.bb..","...yy.bbbbb.yy..","...ss.bbbbb.ss..",
"......bbbbb.....","......kk.kk.....","......kk.kk.....","......kk.kk.....","......kk.kk.....",
".....kkk.kkk....",]),13,'b',3)

# ---- background: Fountain Square under the red sun ------------------------------------------------
def _square(d):
    for y in range(44):                                             # a sky the colour of rust, thick with ash
        k=y/43; d.line([0,y,W,y],fill=(int(120+70*k),int(64+50*k),int(48+30*k)))
    d.ellipse([22,6,38,22],fill=(214,70,40)); d.ellipse([25,9,35,19],fill=(240,110,60))   # the red sun
    roofs=[(0,38),(16,33),(30,37),(46,31),(60,35),(70,30),(150,32),(164,36),(176,31),(185,34)]
    d.polygon([(0,46)]+roofs+[(185,46)],fill=(64,40,38))
    for x0,top in ((90,10),(100,4),(110,9),(120,2),(130,12)):      # Kredik Shaw, the Lord Ruler's palace
        d.polygon([(x0-3,32),(x0,top),(x0+3,32)],fill=(54,32,32))
    d.rectangle([84,26,136,46],fill=(58,36,36))
    d.rectangle([0,44,W,H],fill=(118,100,88))                       # the paving
    for y in (48,53,58): d.line([0,y,W,y],fill=(104,88,78))
    for x in range(0,W,9):
        for y,o in ((44,0),(48,4),(53,0),(58,4)): d.line([x+o,y,x+o,y+4],fill=(104,88,78))
    d.rectangle([84,38,102,44],fill=(140,124,110)); d.rectangle([90,32,96,38],fill=(150,134,120))   # the fountain
    d.rectangle([86,39,100,41],fill=(90,110,130))
register_bg(THEME, lambda v: (v+70,v+60,v+50), decor=_square)

CROWD=[(5+i*15+(i%3)*2, 50+(i%2)*2) for i in range(12)]
@fx('mk_crowd')
def _fx_crowd(d,im,e,f):
    """The skaa watching from the back of the square; hands[i] 0..1 raises that one's hand."""
    _,hands=e
    for i,(x,fy) in enumerate(CROWD):
        body=(58,46,42) if i%2 else (72,58,50); head=(186,146,116); hair=(50,40,34)
        d.rectangle([x-1,fy-8,x+2,fy-3],fill=body)                  # the coat
        d.rectangle([x-1,fy-2,x-1,fy],fill=body); d.rectangle([x+2,fy-2,x+2,fy],fill=body)
        d.rectangle([x-1,fy-11,x+1,fy-9],fill=head); d.line([x-1,fy-11,x+1,fy-11],fill=hair)
        k=hands[i]
        if k>0: hy=int(lerp(fy-7,fy-16,k)); d.line([x+3,fy-7,x+3,hy],fill=body); d.rectangle([x+3,hy-2,x+4,hy-1],fill=head)
        else: d.line([x+3,fy-7,x+3,fy-4],fill=body)

@fx('mk_spear')
def _fx_spear(d,im,e,f):
    """The Lord Ruler's spear: from his hand to the tip (pointing left)."""
    _,hx,hy,tx=e; d.line([tx,hy,hx+6,hy],fill=(110,80,50)); d.polygon([(tx-4,hy),(tx,hy-1),(tx,hy+1)],fill=(220,222,230))

# ---- close-up -------------------------------------------------------------------------------------
def closeup_smile(t,f):
    """Primer plano: the spear through him, Kelsier looks up at the Lord Ruler and smiles —
    THERES ALWAYS ANOTHER SECRET."""
    im=Image.new('RGB',(W,H),(150,90,62)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([0,y,W,y],fill=(int(120+50*y/H),int(70+30*y/H),int(54+20*y/H)))
    rr=random.Random(9)
    for i in range(30):                                             # ash drifting across
        x=(rr.randint(0,W)+f*0.6)%W; y=(rr.randint(0,H)+f*0.4+i)%H; d.point((int(x),int(y)),fill=(170,160,150))
    ox=8; jj=1 if t<0.15 and f%2 else 0                             # a flinch, then stillness
    d.rectangle([ox+jj,16,ox+56+jj,H],fill=SKIN); d.rectangle([ox+50+jj,16,ox+56+jj,H],fill=SKIN_D)
    for k in range(7):                                              # swept-back hair
        d.polygon([(ox-2+k*9+jj,18),(ox+10+k*9+jj,18),(ox+12+k*9+jj,4+(k%2)*3)],fill=KPAL['l'])
    d.rectangle([ox-2+jj,10,ox+58+jj,17],fill=KPAL['l']); d.line([ox+4+jj,12,ox+40+jj,11],fill=KPAL['f'])
    for ex in (ox+16,ox+38):
        if t<0.15: d.rectangle([ex-4+jj,29,ex+4+jj,37],fill=(24,14,12))   # eyes wide
        else: d.arc([ex-5+jj,28,ex+5+jj,38],200,340,fill=(24,14,12),width=3)   # eyes creased in the smile
        d.line([ex-6+jj,24,ex+6+jj,23 if ex<ox+27 else 25],fill=(110,84,50))
    if t<0.15: d.line([ox+22+jj,52,ox+34+jj,52],fill=(90,30,20))
    else:
        d.arc([ox+16,40,ox+40,56],20,160,fill=(90,30,20),width=2)   # the grin
        d.rectangle([ox+22,52,ox+34,53],fill=(246,240,230))
    d.line([ox+60,H,ox+80,40],fill=(110,80,50),width=3)             # the spear shaft, rising out of frame
    lines=("THERES","ALWAYS","ANOTHER","SECRET.")
    for i,ln in enumerate(lines):
        if t>=0.2+0.05*i: big_text(im,ln,3+i*15,(250,236,214),scale=2,cx=130,outline=(80,30,20))
    if t<0.06: zoom_lines(d,(255,200,160))
    if t>0.85: im=fade_to(im,(236,236,240),0.7*(t-0.85)/0.15)       # the mists take the frame
    return im

# ---- the clip -------------------------------------------------------------------------------------
TARGETS=[(IX-50-(i%2)*2,GROUND-6-(i%3)*5) for i in range(5)]
def kel_state(f):
    """(x, feet, pose, flip) for Kelsier."""
    x,y,pose=CX,GROUND,guard_pose(f)
    if 48<=f<64: p=(f-48)/16; x,y,pose=ez(CX,52,p),GROUND-26*math.sin(p*math.pi/2),'armsup'   # Pushes up over the axe
    if 64<=f<80: x,y,pose=52,GROUND-26+math.sin(f*0.3),'punch' if (f-64)%3<2 else 'guard'
    if 80<=f<88: p=(f-80)/8; x,y,pose=52,lerp(GROUND-26,GROUND,p),'guard2'
    if 88<=f<94: x,pose=ez(52,88,(f-88)/6),'dash'
    if 94<=f<150: x,pose=88,'punch' if f<104 else guard_pose(f)
    if 150<=f<160: x,pose=ez(88,118,(f-150)/10),'dash'
    if 160<=f<238: x,pose=118,'hurt'
    return x,y,pose

def inq_state(f):
    """(x, feet, pose, alpha) for the Inquisitor, or None."""
    if f<14 or f>=128: return None
    if f<24: return IX,lerp(-6,GROUND,((f-14)/10)**2),'idle',1
    x,pose=IX,'idle'
    if 40<=f<54: x=ez(IX,96,(f-40)/14)
    if 54<=f<94: x=96
    if 52<=f<60: pose='attack'
    if 94<=f<104: x,pose=ez(96,150,(f-94)/10),'hurt'
    alpha=1
    if f>=94: x=max(x,ez(96,150,(f-94)/10)); pose='hurt'; alpha=max(0,1-(f-104)/24) if f>=104 else 1
    return x,GROUND,pose,alpha

def clip_survivor(f):
    s=scene(f,THEME)
    s['under'].append(('mist_ash',N_))
    kx,ky,kpose=kel_state(f)
    acts=[]
    # the crowd: cheers at the punch, freezes at the spear, then the hands go up one by one
    hands=[0]*len(CROWD)
    for i in range(len(CROWD)):
        if 100<=f<118: hands[i]=0.5+0.5*((f//3+i)%2)
        if 262<=f<334: hands[i]=min(1,max(0,(f-262-((i*5)%14)*3)/6))
        if 318<=f<334: hands[i]=min(hands[i],max(0,1-(f-318)/12))
    s['under'].append(('mk_crowd',hands))
    # 1) the Inquisitor drops in; the axe, the coins, the punch
    iq=inq_state(f)
    if 22<=f<28: s['shake']=rshake(2); s['fx']+= [('dust',IX-6,GROUND-1),('dust',IX+6,GROUND-1)]
    if 24<=f<46: callout(s,"STEEL INQUISITOR",c=(226,230,240))
    lines=[]
    if 64<=f<80:
        if f<78: callout(s,"STEEL",c=LINE_HI)
        for i,tx_ty in enumerate(TARGETS):
            t0=64+i*3
            if f<t0: continue
            p=min(1,(f-t0)/5); hx,hy=kx+8,ky-6; tx,ty=tx_ty
            c=(lerp(hx,tx,p),lerp(hy,ty,p)); s['fx'].append(('mist_coin',*c)); lines.append(c)
            if f-t0 in (5,6): s['fx'].append(('spark',tx,ty,3))
    if lines: s['fx'].append(('mist_lines',kx,ky-6,lines))
    if 92<=f<96: s['flash']=0.6; s['fc']=(96,GROUND-8); s['flashc']=(255,240,210); s['shake']=rshake(2); s['fx'].append(('spark',98,GROUND-8,6))
    if 90<=f<120: callout(s,"PEWTER",c=(230,230,236))
    if iq and iq[3]>0:
        ix,iy,ipose,ia=iq
        acts.append(actor(INQ[ipose],ix,iy,flip=True,pal=IPAL,alpha=ia))
        if f<94: s['fx'].append(('mist_axe',ix-8,GROUND-11,(-150+(f-52)*25) if 52<=f<60 else -120))
    # 2) the Lord Ruler walks in
    lr=None
    if 112<=f<290:
        x,flip,pose=LX,True,'idle'
        if f<140: x=ez(200,LX,(f-112)/28)
        if 154<=f<238: pose='attack'
        if 246<=f: x,flip=ez(LX,210,(f-246)/40),False
        lr=actor(LR[pose],x,flip=flip,pal=LPAL,y=GROUND-((f//4)%2 if (f<140 or f>=246) else 0))
        acts.append(lr)
    if 114<=f<154: s['fx'].append(('big',"THE LORD RULER",3,(236,236,244)))
    # 3) the spear
    if 156<=f<238:
        hx,hy=hand_at(LR['attack'],LX,GROUND,True,15,13)
        tip=lerp(hx,104,(f-156)/4) if f<230 else lerp(104,hx,(f-230)/8)
        s['fx'].append(('mk_spear',hx,hy,tip))
        if f==160: s['flash']=0.7; s['fc']=(118,GROUND-8); s['flashc']=(200,40,40); s['shake']=rshake(2)
    # 4) close-up: the smile
    if 166<=f<230: s['image']=closeup_smile((f-166)/64,f); return s
    # 5) he falls; the mists come in; Kelsier stands up out of them
    fall=None
    if 238<=f<330:
        lying=S(KEL['guard'][::-1])                       # on his back, legs in the air
        a=1 if f<300 else max(0,1-(f-300)/24)
        fall=actor(lying,114,alpha=a,pal=KPAL) if f>=242 else actor(hurt(KEL['hurt']),118,pal=KPAL)
        acts.append(fall)
        if f<246: s['fx'].append(('dust',112+random.randint(-6,6),GROUND-1))
    dens=0 if f<270 else (min(0.85,(f-270)/30*0.85) if f<330 else max(0,0.85-(f-330)/24*0.85))
    if 316<=f<352:
        k=min(1,(f-316)/14)
        solid=0 if f<336 else min(1,(f-336)/14)
        if solid<1: acts.append(actor(KEL[guard_pose(f)],CX,pal=KPAL,alpha=0.7*k*(1-solid),tint=(232,236,246)))
        if solid>0:
            s['under'].append(('mist_cloak',CX,GROUND,False,0,N_))
            acts.append(actor(KEL[guard_pose(f)],CX,pal=KPAL,alpha=solid))
    show_kel=f<160 or f>=352
    if 160<=f<238: show_kel=True
    if show_kel:
        if 160<=f<238: acts.append(actor(KEL['hurt'],kx,ky,pal=KPAL))
        else:
            s['under'].append(('mist_cloak',kx,ky,False,1 if kpose=='dash' else 0,N_))
            acts.append(actor(KEL[kpose],kx,ky,pal=KPAL))
    if dens>0: s['fx'].append(('mist_fog',dens,N_))
    s['actors']=acts
    return s

CLIPS = [clip('survivor', N_, clip_survivor)]
