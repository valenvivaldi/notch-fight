"""Alien vs Predator: Claude caught in the middle of the war, inside the ancient pyramid under the
Antarctic ice. A Xenomorph creeps behind him while the Predator's red triple-dot laser lands on his
head — WHOEVER WINS... WE LOSE. The two leap over him and clash: tail against wrist blades, acid
blood sizzling through the Predator's armour, a blade through the Alien's dome. The walls slide open
and the swarm pours in; the Predator cloaks, blasts them with the shoulder cannon and saves Claude.
Close-up: the Predator marks Claude's forehead with the acid-blood clan mark and hands him a shield
made from an Alien's head and a spear. The Queen breaks in; they fight as a tag team; close-up of
the two back to back. Claude spears the Queen and the pyramid ceiling buries her. The Predator
salutes him; the dust settles and the standoff is back for the loop."""
from engine import *

THEME = 'avp'
N_ = 360
CX, AX, PX = 92, 30, 155                                           # neutral: Claude between them

# ---- Claude ----------------------------------------------------------------------------------
MARK = (190,255,70)
def _mark(s):
    """The clan mark on Claude's forehead: a small glowing V/Y above the eyes."""
    top,l,r=body_box(s); g=[list(row) for row in s]
    for x,y in ((l+4,top),(l+6,top),(l+5,top+1)):
        if g[y][x]!='.': g[y][x]='a'
    return S([''.join(row) for row in g])
CLM={k:_mark(v) for k,v in CL.items()}
CLPAL={'a':MARK}

# the alien-head shield on the front arm ('x' dome, 'z' sheen, 'W' teeth) + a spear in the other hand
_SHIELD=[".xxx..","xxzzx.","xxxzzx","xxxxzx","xxxxxx",".xxxxx",".WxWx.","..WW.."]
def _armed(name,s):
    s=_mark(s)
    if name in ('punch','dash','charge'):                          # spear thrust forward
        L=len(s[0])
        return paint(s,[(L,5,'qqqqqqHH'),(L,6,'qqqqqqH.')],right=8)
    if name=='armsup':                                             # spear raised high, shield up
        return paint(s,[(0,-7,'.H'),(0,-6,'.H')]+[(1,y,'q') for y in range(-5,0)]+
                       [(10,-7+i,r) for i,r in enumerate(_SHIELD)],top=7,right=3)
    if name=='hurt': return s
    items=[(13,1+i,r) for i,r in enumerate(_SHIELD)]               # shield in front, spear upright
    items+=[(1,-4,'H'),(1,-3,'H')]+[(1,y,'q') for y in range(-2,9)]
    return paint(s,items,top=4,right=4)
CLA={k:_armed(k,v) for k,v in CL.items()}
CLAPAL={'a':MARK,'x':(40,44,56),'z':(120,132,150),'W':(220,220,200),'q':(120,86,50),'H':(210,214,224)}

# ---- the Predator ----------------------------------------------------------------------------
_PR_HEAD=[
".....kkkk..........",
"...kkkDDDDD........",
"..kkkDDDDDDD.......",
".kkkDDDeeeDD.......",
".kkkDDDDDDDD.......",]
_PR_DREADS=[[
"kkkk.dDDDDd........",
"kkk.k.ydddy........",
"kk.kcccCYY.........",
"kk.kAAAAAAA........",
"k.kAAAAAAAAA.......",],[
".kkk.dDDDDd........",
"kk.k..ydddy........",
"k.k.cccCYY.........",
"k.kkAAAAAAA........",
".k.AAAAAAAAA.......",]]
_PR_ARM=[
"...YYANNNNNAYY.....",
"...YY.NYNYNY.YY....",
"...YY.NNNNNN.BBHHH.",]
_PR_LEGS=[
"...BB.YNYNYN.......",
"...YY.AAAAAA.......",
"......ABBBBA.......",
"......YY..YY.......",
".....YY....YY......",
".....YY....YY......",
".....yY....Yy......",
".....BB....BB......",
"....BBB....BBB.....",]
_PR=_PR_HEAD+_PR_DREADS[0]+_PR_ARM+_PR_LEGS
_PR2=_PR_HEAD+_PR_DREADS[1]+_PR_ARM+_PR_LEGS
_PR_ATK=_PR_HEAD+_PR_DREADS[0]+[                                   # wrist blades thrust forward
"...YYANNNNNAYYYYBBHHHH",
"...YY.NYNYNY..........",
"...YY.NNNNNN..........",]+_PR_LEGS
_PR_RAISE=[                                                        # the fist raised (salute / roar)
"..............HH...",
"..............HH...",
".............BB....",
".............YY....",
".............YY....",
"............YY.....",
"...........YY......",]+[r[:11]+('Y' if i==4 else '.')+r[12:] for i,r in enumerate(_PR_HEAD)]+_PR_DREADS[0][:4]+[
"k.kAAAAAAAAA.......",
"...YYANNNNNA.......",
"...YY.NYNYNY.......",
"...YY.NNNNNN.......",]+_PR_LEGS
PR={'idle':S(_PR),'idle2':S(_PR2),'attack':S(_PR_ATK),'raise':S(_PR_RAISE)}
PR['hurt']=hurt(PR['idle'])
def pr_idle(f): return PR['idle'] if (f//6)%2==0 else PR['idle2']
PRPAL={'k':(34,28,24),'D':(176,170,150),'d':(112,104,88),'e':(70,40,30),'Y':(150,146,86),'y':(104,102,58),
       'A':(146,112,62),'N':(66,66,70),'B':(92,76,54),'H':(222,226,236),'c':(78,80,90),'C':(150,40,30)}
PR_CANNON=(7,7)                                                    # the barrel tip's cell (idle poses)
PR_EYE=(9,3)

# ---- the Xenomorph ---------------------------------------------------------------------------
_XE_TOP=[
"tt............................",
".Tt............kkkk...........",
"..T.......p.p.pkkhhkkk........",
"..T......pkpkpkp.kkkkhhkkkk...",
"..T....kkkkkkkkkkkkkkkkkkkkkk.",
"...T..kkkkjkjkjkkkkk.....kkkWk",
"....TTkkkkkkkkkkkkk.k.....WkW.",]
_XE_LEGS=[[
"......kk.kk....kk..k..........",
".....kk...kk...kk...kk........",
".....kk....k...kk....k........",
"......k....kk...k....kk.......",
".....kk...kk...kk...kk........",],[
"......kk.kk....kk..k..........",
"......kk..kk....kk..kk........",
".....kk....k....k....k........",
".....k.....kk...kk...kk.......",
"....kk....kk....kk..kk........",]]
_XE=_XE_TOP+_XE_LEGS[0]
_XE2=["t.............................",".T"+_XE_TOP[1][2:]]+_XE_TOP[2:]+_XE_LEGS[0]
_XE_WALK=_XE_TOP+_XE_LEGS[1]
_XE_LUNGE=[                                                        # stretched, the inner jaw out
"...............................",
"tt..............kkkk...............",
".TT.......p.p.pkkhhkkk.............",
"...T.....pkpkpkp.kkkkhhkkkk........",
"...TT..kkkkkkkkkkkkkkkkkkkkkk......",
".....TTkkkjkjkjkkkkkk.....kkkWkWW..",
".......kkkkkkkkkkkk.kkk..WWkWiiiIW.",
".....kk..kk....kk.....kk..WkW......",
"....kk....kk....kk......kk.........",
"...kk......kk....kk................",]
_XE_TAIL=[                                                         # the tail arched over, blade forward
"...........TTTTTTTTTt..........",
"........TTT....kkkk.tt.........",
".......T......kkhhkkk..........",
"......T...pkpkpkkkkkhhkkkk.....",
"......T.kkkkkkkkkkkkkkkkkkkkkk.",
".....T.kkkkjkjkjkkkkk.....kkkWk",
"......kkkkkkkkkkkkkk.k.....WkW.",]+_XE_LEGS[0]
XE={'idle':S(_XE),'idle2':S(_XE2),'walk':S(_XE_WALK),'lunge':S(_XE_LUNGE),'tail':S(_XE_TAIL)}
XE['hurt']=hurt(XE['idle'])
XE['dead']=S([r for r in reversed(XE['idle'])])
def xe_idle(f,k=0): return XE['idle'] if ((f+k)//6)%2==0 else XE['idle2']
def xe_walk(f,k=0): return XE['walk'] if ((f+k)//3)%2==0 else XE['idle']
XEPAL={'k':(44,48,60),'h':(128,140,160),'j':(80,88,106),'p':(62,68,84),'T':(52,56,70),'t':(170,180,196),
       'W':(220,222,206),'i':(150,70,80),'I':(236,236,220)}
ACID=(190,240,40)

# ---- the Queen -------------------------------------------------------------------------------
_QU=[
"...........kkkkkkkkkk..........",
"........kkkhhhhkkkkkkkkk.......",
"......kkkhkkkkkkkkkkkkkkkk.....",
".....kkhkkkkkkkkkkkkkkkkkkkk...",
"....kkhkkkkkkkkkkkkkkkkkkkkkkk.",
"....kkkkkkkjkjkjkkkkkkkkkkkkkkk",
".....kkkkkkkkkkkkkkkkkkkkkkWkWk",
"......kkkkkkkk.......kkkkkWkWk.",
"........kkkk..........kkkk.....",
"........pkpkp........kk.kk.....",
".......kkkkkkk......kk...kk....",
"......kkkjkjkkk....kk..........",
".....kk.kkkkk.kkkkkk...........",
".....kk.kjkjk.kk...............",
"....kk..kkkkk..kk..............",
"...kk...kkkkk...kk.............",
"........kkkkk..................",
"TT.....kkk.kkk.................",
".TT...kkk...kkk................",
"..TTTkkk.....kkk...............",
"....kkk.......kkk..............",
"....kk.........kk..............",
"...kk...........kk.............",
"...kk...........kk.............",
"..kkk...........kkk............",]
QU={'idle':S(_QU)}
def _qroar(s):
    g=list(s); g[6]=g[6][:26]+"WkWWWiiI"; g[7]=g[7][:25]+"WkWW"
    return S(g)
QU['roar']=_qroar(QU['idle'])
QU['hurt']=hurt(QU['idle'])

# ---- background: the pyramid chamber under the ice -------------------------------------------
TORCHES=(14,171)
DOOR=(78,106)                                                      # the sliding wall in the back
def _chamber(d):
    for y in range(6,GROUND,6):                                     # stone blocks
        off=5 if (y//6)%2 else 0
        d.line([0,y,W,y],fill=(17,15,14))
        for x in range(off,W,10): d.line([x,y,x,y+5],fill=(17,15,14))
        for x in range(off,W,10): d.line([x+1,y+1,x+8,y+1],fill=(34,30,27))
    for x0,x1 in ((40,144),(50,134),(60,124),(70,114)):             # the stepped pyramid relief
        y=GROUND-(x0-40)//10*9-9
        d.rectangle([x0,y,x1,GROUND],fill=(28,25,22)); d.line([x0,y,x1,y],fill=(52,46,38))
        d.line([x0,y,x0,GROUND],fill=(20,18,16))
    d.rectangle([DOOR[0]-2,22,DOOR[1]+2,GROUND],fill=(44,40,34))    # the door frame
    d.rectangle([DOOR[0],24,DOOR[1],GROUND],fill=(4,6,10))          # the passage behind the wall
    rr=random.Random(2004)                                          # carved glyphs
    for gx in (28,156):
        for gy in (12,24,36,48):
            d.rectangle([gx-5,gy-4,gx+5,gy+4],fill=(30,27,24)); d.rectangle([gx-5,gy-4,gx+5,gy+4],outline=(40,36,30))
            for _ in range(4):
                x,y=gx+rr.randint(-3,2),gy+rr.randint(-2,1); d.line([x,y,x+rr.randint(0,2),y+rr.randint(0,2)],fill=(74,64,48))
    for x in range(0,W):                                            # ice creeping in from above
        h=2+int(2*math.sin(x*0.37)+1.5*math.sin(x*0.11))
        d.line([x,0,x,max(0,h)],fill=(96,130,160))
        if x%7==3: d.line([x,h,x,h+2+(x*5)%4],fill=(150,190,220))
    for x in TORCHES: d.rectangle([x-1,30,x+1,35],fill=(60,48,36)); d.rectangle([x-2,29,x+2,29],fill=(80,64,44))
register_bg(THEME, lambda v: (v//2+8,v//2+12,v+16), decor=_chamber, clip_ground=True)

# ---- effects ---------------------------------------------------------------------------------
@fx('avp_torch')
def _fx_torch(d,im,e,f):
    """Torch flames + their warm glow on the stone (12-frame flicker: loop-safe)."""
    rr=random.Random(f%12)
    for x in TORCHES:
        h=4+rr.randint(0,2); d.polygon([(x-2,28),(x+2,28),(x+rr.randint(-1,1),28-h)],fill=(255,140,40))
        d.line([x,27,x,28-h+2],fill=(255,230,150))

@fx('avp_wall')
def _fx_wall(d,im,e,f):
    """The sliding stone wall that seals the passage: open 0..1 (the slabs part sideways)."""
    _,o=e; half=(DOOR[1]-DOOR[0])//2; sh=int(half*ease(o))
    for x0,x1 in ((DOOR[0],DOOR[0]+half-sh),(DOOR[0]+half+sh,DOOR[1])):
        if x1<=x0: continue
        d.rectangle([x0,24,x1,GROUND],fill=(38,34,30))
        for y in range(24,GROUND,6): d.line([x0,y,x1,y],fill=(24,22,20))
        for y in range(30,GROUND-4,12): d.rectangle([x0+2,y,x0+4,y+2],fill=(70,60,44))
    if 0<o<1: s=rshake(); d.point((DOOR[0]+half+s[0],GROUND-2),fill=(90,80,70))

@fx('avp_laser')
def _fx_laser(d,im,e,f):
    """The Predator's triple red dot (a small triangle) on a target point."""
    _,x,y=e; x,y=int(x),int(y)
    for dx,dy in ((0,-1),(-1,1),(1,1)): d.point((x+dx,y+dy),fill=(255,30,20))

@fx('avp_beam')
def _fx_beam(d,im,e,f):
    """The laser beam itself: a faint red line from the cannon to the target."""
    _,x0,y0,x1,y1=e
    n=int(max(abs(x1-x0),abs(y1-y0)))
    for k in range(0,n,2): blend(im.load(),int(lerp(x0,x1,k/n)),int(lerp(y0,y1,k/n)),(255,40,30),0.4)

@fx('avp_bolt')
def _fx_bolt(d,im,e,f):
    """A plasma-cannon bolt: blue-white ball with a short trail."""
    _,x,y,dirn=e; x,y=int(x),int(y)
    for k in range(1,6): blend(im.load(),x-dirn*k,y,(90,150,255),0.8-k*0.13)
    d.ellipse([x-2,y-2,x+2,y+2],fill=(90,160,255)); d.rectangle([x-1,y-1,x+1,y],fill=(230,245,255))

@fx('avp_acid')
def _fx_acid(d,im,e,f):
    """Acid-blood spray from x,y: drops arcing out and falling (t 0..1), seeded."""
    _,x,y,t,seed=e; rr=random.Random(seed)
    for i in range(10):
        vx=rr.uniform(-1.4,1.4)*18; vy=-rr.uniform(4,14); tt=t*1.2
        X=x+vx*tt; Y=min(GROUND,y+vy*tt+22*tt*tt)
        d.point((int(X),int(Y)),fill=ACID if i%3 else (240,255,160))

@fx('avp_sizzle')
def _fx_sizzle(d,im,e,f):
    """Acid eating through something: bright drops + grey smoke puffs rising from x,y (w wide)."""
    _,x,y,w,a,seed=e; rr=random.Random(seed)
    for i in range(int(8*a)):
        bx=x+rr.uniform(-w,w); life=rr.randint(8,14); ph=(f+rr.randint(0,life))%life; k=ph/life
        yy=y-k*10; r=1+int(k*2)
        c=tuple(int(v) for v in lerp_c((150,150,140),(60,60,60),k))
        d.ellipse([bx-r,yy-r,bx+r,yy+r],fill=c)
    for i in range(int(4*a)): d.point((int(x+rr.uniform(-w,w)),int(y+rr.randint(0,3))),fill=ACID)
def lerp_c(a,b,t): return tuple(lerp(a[i],b[i],t) for i in range(3))

@fx('avp_pool')
def _fx_pool(d,im,e,f):
    """A bubbling acid pool on the floor."""
    _,x,w=e; d.line([x-w,GROUND,x+w,GROUND],fill=(120,170,30)); d.line([x-w+2,GROUND-1,x+w-2,GROUND-1],fill=ACID)
    if f%4<2: d.point((x+(f*3)%(2*w)-w,GROUND-2),fill=(240,255,160))

@fx('avp_cloak')
def _fx_cloak(d,im,e,f):
    """The cloak shimmer: the sprite's outline as a refracting glassy edge (a 0..1 = visibility of it)."""
    _,spr,cx,feet,flip,a=e
    if a<=0: return
    ox,oy=origin(spr,cx,feet); px=im.load(); w=len(spr[0])
    pts={((w-1-x) if flip else x,y) for y,r in enumerate(spr) for x,ch in enumerate(r) if ch!='.'}
    for (x,y) in pts:
        X,Y=ox+x,oy+y
        if (x+1,y) not in pts or (x-1,y) not in pts or (x,y-1) not in pts:
            if (x+y+f)%3: blend(px,X,Y,(170,210,230),0.45*a)
        elif (x*3+y+f)%7==0: blend(px,X,Y,(120,150,170),0.25*a)

@fx('avp_after')
def _fx_after(d,im,e,f):
    _,spr,x,y,flip,a,pal=e; draw(im,spr,x,y,flip,alpha=a,f=f,pal=pal)

_WIDE={'W':["10001","10001","10101","10101","01010"]}
def big_text_w(im,txt,y,c,cx=W//2,outline=None,scale=2):
    """big_text with a 5-px wide W (the 3x5 font's W reads as an H at this size)."""
    ws=[len(_WIDE[ch][0]) if ch in _WIDE else 3 for ch in txt]
    m=Image.new('L',(sum(ws)+len(ws),5),0); md=ImageDraw.Draw(m); x=0
    for ch,w in zip(txt,ws):
        rows=_WIDE[ch] if ch in _WIDE else [FONT.get(ch,FONT[' '])[i*3:i*3+3] for i in range(5)]
        for j,r in enumerate(rows):
            for i,b in enumerate(r):
                if b=='1': md.point((x+i,j),fill=255)
        x+=w+1
    m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        im.paste((0,0,0),(x+2,y+2),m)
    im.paste(c,(x,y),m)

@fx('avp_card')
def _fx_card(d,im,e,f):
    """The tagline card: the scene dims, two lines of big text."""
    _,a,l1,l2=e
    im.paste(fade_to(im,(0,0,0),0.7*min(1,a)))
    if l1: big_text_w(im,"WHOEVER WINS...",12,(230,230,220),outline=(60,10,10))
    if l2: big_text_w(im,"WE LOSE.",34,(255,60,40),outline=(60,10,10))

@fx('avp_gift')
def _fx_gift(d,im,e,f):
    """The Predator's gift in flight: the Alien-head shield and a spear."""
    _,x,y=e; x,y=int(x),int(y)
    d.line([x-5,y-12,x-5,y+2],fill=(120,86,50)); d.line([x-5,y-14,x-5,y-13],fill=(210,214,224))
    draw(im,S(_SHIELD),x,y+2,False,pal=CLAPAL)

@fx('avp_block')
def _fx_block(d,im,e,f):
    """A falling ceiling block (x, y, w, h)."""
    _,x,y,w,h=e; x,y=int(x),int(y)
    d.rectangle([x,y,x+w,y+h],fill=(58,50,42),outline=(24,20,18)); d.line([x+1,y+1,x+w-1,y+1],fill=(82,72,58))
    d.line([x+w//2,y+2,x+w//2-2,y+h-2],fill=(34,30,26))

@fx('avp_rubble')
def _fx_rubble(d,im,e,f):
    """The pile of stone where the Queen was buried (a 0..1 fades it)."""
    _,x,a=e
    if a<=0: return
    rr=random.Random(77); px=im.load()
    for i in range(16):
        bx=x+rr.randint(-24,18); w=rr.randint(6,11); h=max(2,16-abs(bx+w//2-x)//2-rr.randint(0,5))
        c=(58,50,42) if i%3 else (72,62,50)
        for yy in range(GROUND-h,GROUND+1):
            for xx in range(bx,bx+w): blend(px,xx,yy,(24,20,18) if yy==GROUND-h or xx==bx else c,a)

@fx('avp_tail')
def _fx_tail(d,im,e,f):
    """A tail strike: a segmented dark tail from (x0,y0) to (x1,y1), a pale blade at the tip."""
    _,x0,y0,x1,y1=e; n=max(1,int(abs(x1-x0)))
    for k in range(0,n+1):
        t=k/n; x=lerp(x0,x1,t); y=lerp(y0,y1,t)-math.sin(math.pi*t)*6
        d.point((int(x),int(y)),fill=(52,56,70) if k%3 else (90,96,112)); d.point((int(x),int(y)+1),fill=(30,32,40))
    sx=1 if x1>x0 else -1
    d.polygon([(x1,y1-1),(x1+sx*4,y1),(x1,y1+2)],fill=(190,200,214))

@fx('avp_chain')
def _fx_chain(d,im,e,f):
    """Dust cloud: grey puffs spreading from x (a 0..1)."""
    _,x,a,seed=e; rr=random.Random(seed)
    for i in range(int(16*a)):
        bx=x+rr.uniform(-26,26)*(1.2-a*0.4); by=GROUND-rr.uniform(0,16)*(1.3-a*0.5); r=rr.randint(2,5)
        d.ellipse([bx-r,by-r,bx+r,by+r],fill=(70,64,56) if i%2 else (96,88,76))

# ---- close-ups -------------------------------------------------------------------------------
def _cl_face(d,x0,x1,y0,right,eyes='open'):
    """Claude's big face for the close-ups, facing right (eyes near x1) or left."""
    d.rectangle([x0,y0,x1,H],fill=(217,119,87))
    if right: d.rectangle([x0,y0,x0+6,H],fill=(176,92,66))
    else: d.rectangle([x1-6,y0,x1,H],fill=(176,92,66))
    ex=(x1-34,x1-14) if right else (x0+10,x0+30)
    for x in ex:
        if eyes=='open': d.rectangle([x,y0+22,x+5,y0+35],fill=(24,14,12))
        else: d.rectangle([x-1,y0+28,x+6,y0+30],fill=(24,14,12))
    return ex

def _mark_glow(im,cx,y,g,prog=1.0):
    """The clan mark drawn big on the forehead: a V with a stem (prog draws it stroke by stroke)."""
    d=ImageDraw.Draw(im); segs=[((cx-8,y),(cx,y+10)),((cx+8,y),(cx,y+10)),((cx,y+10),(cx,y+15))]
    if g>0:
        m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
        for (a,b) in segs: md.line([a,b],fill=int(200*g),width=6)
        im.paste(MARK,(0,0),m.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    left=prog*3
    for i,(a,b) in enumerate(segs):
        k=min(1,max(0,left-i))
        if k<=0: break
        e=(lerp(a[0],b[0],k),lerp(a[1],b[1],k)); d.line([a,e],fill=(90,140,20),width=3); d.line([a,e],fill=(230,255,150),width=1)
    return d

def _pred_mask(d,x0,facing_left,f):
    """The Predator's head for the close-ups: dreads, the angular bio-mask, visor, tusks."""
    sx=-1 if facing_left else 1; X=lambda u: x0+sx*u                  # u grows towards the face
    for i in range(9):                                                  # dreads behind the head
        u=-6-i*3; d.line([X(u+4),0,X(u-2),52+(i%3)*5],fill=(34,28,24),width=2)
        d.point((X(u-1),30+(i%4)*6),fill=(170,160,120))
    d.polygon([(X(-4),50),(X(0),4),(X(22),0),(X(40),6),(X(48),22),(X(44),40),(X(30),46)],fill=(112,104,88))
    d.polygon([(X(-2),44),(X(2),6),(X(22),3),(X(38),8),(X(45),22),(X(42),36),(X(28),42)],fill=(176,170,150))
    d.line([X(4),8,X(36),10],fill=(214,208,190))                        # the brow ridge
    d.polygon([(X(14),16),(X(44),18),(X(43),24),(X(18),24)],fill=(40,24,20))   # the visor
    d.line([X(20),19,X(42),20],fill=(120,40,30))
    for u,y in ((30,42),(38,38)): d.polygon([(X(u),y),(X(u+3),y),(X(u+4),y+7)],fill=(226,220,196))   # tusks
    d.rectangle([min(X(-6),X(40)),48,max(X(-6),X(40)),H],fill=(146,112,62))   # shoulder armour
    for y in range(52,H,4): d.line([min(X(-4),X(36)),y,max(X(-4),X(36)),y],fill=(66,66,70))

def closeup_mark(t,f):
    """Primer plano: the Predator's clawed finger, dipped in acid blood, burns the clan mark on
    Claude's forehead; it sizzles, then glows."""
    im=Image.new('RGB',(W,H),(14,10,8)); d=ImageDraw.Draw(im)
    for x in range(0,W,10): d.line([x,0,x,H],fill=(20,16,12))
    _cl_face(d,8,100,4,True,'shut' if 0.3<t<0.62 else 'open')
    _pred_mask(d,178,True,f)
    prog=ease((t-0.3)/0.3); cx,my=74,6
    # the hand: in (0.08-0.3), drawing (0.3-0.6), out (0.62-0.8)
    if t<0.3: k=ease((t-0.08)/0.22)
    elif t<0.62: k=1
    else: k=1-ease((t-0.62)/0.18)
    if k>0:
        segs=[((cx-8,my),(cx,my+10)),((cx+8,my),(cx,my+10)),((cx,my+10),(cx,my+15))]
        if t<0.3: tip=(cx-8,my)
        elif t<0.6:
            q=prog*3; i=min(2,int(q)); a,b=segs[i]; u=q-i; tip=(lerp(a[0],b[0],u),lerp(a[1],b[1],u))
        else: tip=(cx,my+15)
        hx=lerp(W+10,tip[0],k); hy=lerp(50,tip[1],k)
        d.line([hx+20,hy+10,hx+70,H+10],fill=(150,146,86),width=9)         # the forearm
        d.line([hx+44,hy+30,hx+70,H+14],fill=(92,76,54),width=12)          # the gauntlet
        d.line([hx+50,hy+34,hx+64,H+4],fill=(66,66,70),width=2)
        d.ellipse([hx+10,hy+2,hx+26,hy+16],fill=(150,146,86))              # the hand
        for j in range(2): d.line([hx+12+j*6,hy+14,hx+8+j*6,hy+20],fill=(110,108,62),width=2)
        d.line([hx+2,hy+1,hx+14,hy+6],fill=(150,146,86),width=3)          # the finger
        d.polygon([(hx-2,hy),(hx+3,hy-2),(hx+4,hy+2)],fill=(30,26,22))     # the claw
        d.ellipse([hx-2,hy-1,hx+1,hy+2],fill=ACID)
    g=ease((t-0.62)/0.15)*(0.8+0.2*math.sin(f*0.6))
    d=_mark_glow(im,cx,my,g,prog if t<0.6 else 1)
    if 0.3<t<0.72:                                                  # the burn sizzles
        rr=random.Random(f)
        for _ in range(8):
            x=cx+rr.randint(-10,10); y=my+rr.randint(-4,4)-rr.randint(0,10); d.ellipse([x-2,y-2,x+2,y+1],fill=(120,120,110))
    if t<0.06: zoom_lines(d,(190,255,70))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

def closeup_back(t,f):
    """Primer plano: Claude and the Predator back to back, the mark glowing, the laser dot hunting;
    Alien heads close in from both edges."""
    im=Image.new('RGB',(W,H),(10,8,10)); d=ImageDraw.Draw(im)
    rr=random.Random(f%12)
    for x in range(0,W,10): d.line([x,0,x,H],fill=(18,14,12))
    # Claude, facing left
    d.line([70,0,40,64],fill=(120,86,50),width=3); d.polygon([(69,0),(75,0),(72,-6)],fill=(210,214,224))
    _cl_face(d,12,92,12,False)
    _mark_glow(im,48,14,0.7+0.3*math.sin(f*0.5)); d=ImageDraw.Draw(im)
    _pred_mask(d,120,False,f)                                       # the Predator, facing right
    # the Aliens creeping in
    k=ease(t/0.8)
    for side in (-1,1):
        bx=(0 if side<0 else W)+side*int(lerp(20,-4,k))
        pts=[(bx,26),(bx-side*20,32),(bx-side*24,40),(bx-side*14,44),(bx,42)]
        d.polygon(pts,fill=(44,48,60)); d.line([pts[0],pts[1]],fill=(128,140,160))
        for j in range(3): d.line([bx-side*(15+j*3),40,bx-side*(15+j*3),43],fill=(220,222,206))
    if t>0.3:
        tx=int(lerp(W-8,W+4,1-k)) if t<0.7 else int(W-12+rr.randint(-1,1))
        for dx,dy in ((0,-1),(-1,1),(1,1)): d.point((tx+dx,34+dy),fill=(255,30,20))
    if t<0.06: zoom_lines(d,(255,80,60))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- the clip --------------------------------------------------------------------------------
def _cannon(spr,x,feet,flip):
    return hand_at(spr,x,feet,flip,*PR_CANNON)
DEAD_X=112
SWARM=[(92,124,70,138),(-20,122,14,144),(92,132,104,150)]          # (from x, frame in, to x, frame shot)

def clip_pyramid(f):
    s=scene(f,THEME)
    s['under'].append(('avp_torch',)); wall=0
    cl=actor(CL[guard_pose(f)],CX); al=actor(xe_idle(f),AX,pal=XEPAL); pr=actor(pr_idle(f),PX,flip=True,pal=PRPAL)
    extra=[]; cloak=0
    # 1) caught in the middle: the laser lands on Claude, the Alien hisses behind him
    if 12<=f<44:
        cx,cy=_cannon(pr['spr'],pr['x'],pr['y'],True); tx=int(lerp(cx-10,CX+4,min(1,(f-12)/6))); ty=GROUND-9
        s['fx'].append(('avp_beam',cx,cy,tx,ty)); s['fx'].append(('avp_laser',tx,ty))
    if 16<=f<30: al['spr']=XE['lunge']
    if 18<=f<24: cl.update(flip=True,x=CX+rshake()[0])
    # 2) the tagline card
    if 24<=f<60:
        cl['flip']=((f-24)//6)%2==0
        s['fx'].append(('avp_card',(f-24)/6,f>=26,f>=38))
    # 3) they leap at each other over Claude, who ducks and scurries out
    if 60<=f<76:
        t=(f-60)/16
        al.update(spr=XE['lunge'],x=ez(AX,DEAD_X-6,t),y=GROUND-int(24*math.sin(math.pi*t)))
        pr.update(spr=PR['attack'],x=ez(PX,DEAD_X+22,t),y=GROUND-int(20*math.sin(math.pi*t)))
        if f<70: cl.update(spr=hurt(CL['guard']),x=CX)
        if f==68: s['flash']=0.4; s['fc']=(DEAD_X+8,GROUND-22); s['shake']=rshake(2)
        if 68<=f<72: s['fx'].append(('spark',DEAD_X+8,GROUND-24,5))
    if 70<=f<82: cl.update(spr=CL['dash'],flip=True,x=ez(CX,44,(f-70)/12))
    if 82<=f<348: cl['x']=44                                        # (then back between them: the neutral pose)
    if 82<=f<156: cl.update(spr=CL[guard_pose(f)] if f%24<18 else hurt(CL['guard']))
    # 4) the clash
    if 76<=f<112:
        al.update(spr=xe_idle(f),x=DEAD_X-6); pr.update(spr=pr_idle(f),x=DEAD_X+22)
        k=(f-76)//12; ph=(f-76)%12
        if k==0:                                                    # tail vs wrist blades
            if ph<8: al['spr']=XE['tail']
            if 3<=ph<8: s['fx'].append(('avp_tail',DEAD_X-10,GROUND-12,DEAD_X+16,GROUND-12)); pr['spr']=PR['attack']
            if ph==5: s['fx'].append(('spark',DEAD_X+16,GROUND-12,5)); s['shake']=rshake()
        if k==1:                                                    # a slash; acid sprays onto the armour
            if ph<6: pr['spr']=PR['attack']
            if 1<=ph<6: al.update(spr=XE['hurt'],x=DEAD_X-8)
            if ph==1: s['fx'].append(('spark',DEAD_X+6,GROUND-8,4))
            s['fx'].append(('avp_acid',DEAD_X+8,GROUND-8,ph/12,5))
            if ph>=5: pr['spr']=PR['hurt']
        if k>=1: s['fx'].append(('avp_sizzle',DEAD_X+22,GROUND-10,3,1,9))
        if k==2:                                                    # the inner jaw... and the blades through the dome
            if ph<6: al['spr']=XE['lunge']
            if ph<4: pr['spr']=PR['raise']
            if 4<=ph<8: pr['spr']=PR['attack']
            if ph==4: s['fx'].append(('spark',DEAD_X+8,GROUND-12,6)); s['flash']=0.3; s['fc']=(DEAD_X+8,GROUND-12); s['shake']=rshake(2)
            if ph>=4: s['fx'].append(('avp_acid',DEAD_X+6,GROUND-12,(ph-4)/10,8)); al.update(spr=XE['hurt'])
    if 112<=f<156:
        al.update(spr=XE['dead'],x=DEAD_X-6,alpha=max(0,1-(f-116)/12) if f>=116 else 1)
        s['under'].append(('avp_pool',DEAD_X-6,10))
        if f<130: s['fx'].append(('avp_sizzle',DEAD_X-6,GROUND-2,10,1,14))
        if f<120: pr['spr']=PR['raise']
        pr['x']=DEAD_X+22
    # 5) the walls slide open, the swarm pours in; the Predator cloaks and hunts them
    if 116<=f<160: wall=min(1,(f-116)/8) if f<150 else 1-(f-150)/6
    for i,(x0,t0,x1,dead) in enumerate(SWARM):
        if not (t0<=f<156): continue
        t=min(1,(f-t0)/14); x=ez(x0,x1,t); y=GROUND; fl=x1<x0
        if i==1 and f>=138: x=ez(x1,28,(f-138)/6); y=GROUND-int(8*math.sin(math.pi*min(1,(f-138)/6)))
        if f<dead:
            spr=xe_walk(f,i*2) if t<1 else xe_idle(f,i*3)
            if i==1 and f>=138: spr=XE['lunge']
            extra.append(actor(spr,x,y,flip=fl,pal=XEPAL))
        elif f<dead+4:
            extra.append(actor(XE['hurt'],x,flip=fl,pal=XEPAL)); s['fx'].append(('avp_acid',x,GROUND-8,(f-dead)/8,20+i))
            if f==dead: s['fx'].append(('boom',x,GROUND-8,5)); s['shake']=rshake()
        else:
            extra.append(actor(XE['dead'],x,flip=fl,pal=XEPAL)); s['under'].append(('avp_pool',int(x),8))
    if 120<=f<156:                                                  # cloaked: a shimmer that hunts
        cloak=min(1,(f-120)/6)
        if f>=142: cloak=max(0,1-(f-142)/3)
        pr.update(x=DEAD_X+22 if f<138 else ez(DEAD_X+22,6,(f-138)/4),flip=f<138,spr=pr_idle(f))
        for tx,t0 in ((SWARM[0][2],130),(SWARM[2][2],142)):         # the laser dots, then a bolt
            if not (t0<=f<t0+8): continue
            cx,cy=_cannon(pr['spr'],pr['x'],pr['y'],pr['flip'])
            if f<t0+4: s['fx'].append(('avp_laser',tx,GROUND-8))
            else: k=(f-t0-4)/4; s['fx'].append(('avp_bolt',lerp(cx,tx,k),lerp(cy,GROUND-8,k),-1 if pr['flip'] else 1))
        if 142<=f<148:                                              # decloaks behind the pouncer: blades
            pr['spr']=PR['attack']
            if f==144: s['fx'].append(('spark',17,GROUND-12,6)); s['flash']=0.3; s['fc']=(17,GROUND-12)
    # 6) close-up: the clan mark
    if 156<=f<192: s['image']=closeup_mark((f-156)/36,f); return s
    # 7) the gift: a shield from an Alien head and a spear; the Queen breaks in
    marked=f>=192
    if 192<=f<348:
        al['vis']=False
        cl.update(spr=CLM[guard_pose(f)],x=70,flip=False,pal=CLPAL)
        pr.update(spr=pr_idle(f),x=98,flip=True)
    if 192<=f<204:
        pr['spr']=PR['attack']
        if f<198: t=(f-192)/6; s['fx'].append(('avp_gift',lerp(84,76,t),GROUND-8-int(4*math.sin(math.pi*t))))
    if 198<=f<348: cl.update(spr=CLA[guard_pose(f)],pal=CLAPAL)
    if 200<=f<212: cl['spr']=CLA['armsup']
    qu=None
    if 208<=f<320:
        qx=ez(-24,34,(f-208)/20) if f<228 else 34
        qu=actor(QU['idle'],qx,pal=XEPAL)
        if 212<=f<226: qu['spr']=QU['roar']; s['shake']=rshake() if f%2 else (0,0)
        if f<222: s['fx'].append(('avp_chain',4,1-(f-208)/14,61))    # she bursts through the dust
    if 212<=f<228: callout(s,"SKREEEEE!",y=4,c=(255,90,70))
    if 214<=f<348:                                                  # they turn to face her, tag team
        t=min(1,(f-214)/10); cl.update(x=ez(70,CX,t),flip=True); pr.update(x=ez(98,124,t),flip=True)
    # 8) tag team: the shield takes the tail, the cannon and the spear answer
    if 228<=f<240:
        ph=f-228
        if 2<=ph<8: s['fx'].append(('avp_tail',48,GROUND-14,CX-8,GROUND-10)); qu['spr']=QU['roar']
        if ph==6: s['fx'].append(('spark',CX-8,GROUND-10,5)); s['shake']=rshake()
        if 6<=ph<10: cl['x']=CX+2
    if 240<=f<252:
        ph=f-240; cx,cy=_cannon(pr['spr'],pr['x'],pr['y'],True)
        if ph<4: s['fx'].append(('avp_laser',40,GROUND-22))
        elif ph<8: s['fx'].append(('avp_bolt',lerp(cx,40,(ph-4)/4),lerp(cy,GROUND-22,(ph-4)/4),-1))
        if ph==8: s['fx'].append(('boom',40,GROUND-22,5)); qu['spr']=QU['hurt']
        if ph>=8: qu['spr']=QU['hurt']
    # 9) close-up: back to back
    if 252<=f<288: s['image']=closeup_back((f-252)/36,f); return s
    # 10) the finish: the spear into the Queen, a cannon shot into the ceiling, the pyramid buries her
    if 288<=f<298:
        t=(f-288)/6; cl.update(spr=CLA['dash'],x=ez(CX,62,t))
        if f>=294: qu['spr']=QU['hurt']; s['fx'].append(('avp_acid',48,GROUND-14,(f-294)/8,31))
        if f==294: s['fx'].append(('spark',46,GROUND-14,6)); s['shake']=rshake(2)
    if 298<=f<308: cl.update(spr=CLA[guard_pose(f)],x=ez(62,CX,(f-298)/8),y=GROUND-int(6*math.sin(math.pi*min(1,(f-298)/8))))
    if 296<=f<320 and qu: qu['spr']=QU['roar'] if (f//3)%2 else QU['hurt']
    if 300<=f<308:
        cx,cy=_cannon(pr['spr'],pr['x'],pr['y'],True); t=(f-300)/6
        if f<302: s['fx'].append(('avp_laser',34,6))
        else: s['fx'].append(('avp_bolt',lerp(cx,34,t),lerp(cy,6,t),-1))
    if f==306: s['fx'].append(('boom',34,6,6)); s['flash']=0.3; s['fc']=(34,6)
    if 306<=f<322:
        s['shake']=rshake(2 if f<316 else 1)
        for i,(bx,bw,bh,dl) in enumerate(((18,16,11,0),(38,16,12,2),(4,14,10,4),(28,14,9,6),(50,12,10,3))):
            t=(f-306-dl)/8
            if 0<t<1.4: s['fx'].append(('avp_block',bx,lerp(-12,GROUND-bh-4*(i%2),min(1,t*t)),bw,bh))
    if 318<=f<348 and qu is not None: qu=None
    rub=0
    if 314<=f<348: rub=min(1,(f-314)/4)
    if 348<=f<360: rub=1-(f-348)/10
    if rub>0: s['fx'].append(('avp_rubble',34,rub))
    if 314<=f<336: s['fx'].append(('avp_chain',34,1-(f-314)/22,55))
    # 11) the salute
    if 328<=f<348:
        pr['spr']=PR['raise']; cl['flip']=f<330                     # Claude turns to him and answers
        if f>=332: cl['spr']=CLA['armsup']
        if f>=334: callout(s,"HONOR",y=4,c=(230,220,190))
    # 12) back to the standoff
    if 348<=f<360:
        t=(f-348)/10
        cl.update(spr=CL[guard_pose(f)],x=CX,flip=False,pal=None)
        pr.update(spr=pr_idle(f),x=ez(124,PX,t),flip=True)
        al.update(vis=True,alpha=min(1,t))
        if f<352: s['fx'].append(('twinkle',CX,GROUND-8,2))
    s['under'].insert(1,('avp_wall',wall))
    if cloak:
        pr['alpha']=1-cloak
        s['fx'].append(('avp_cloak',pr['spr'],pr['x'],pr['y'],pr['flip'],cloak))
    s['actors']=[al]+extra+([qu] if qu else [])+[cl,pr]
    return s

CLIPS = [clip('pyramid', N_, clip_pyramid)]
