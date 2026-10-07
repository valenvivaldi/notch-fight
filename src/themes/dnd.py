"""Dungeons & Dragons: Claude as a wizard (pointed hat, starry robe, white beard, a staff with a crystal)
vs a Beholder in a torchlit dungeon, the DM narrating in parchment boxes. Two clips on one neutral pose:
  nat20 - ROLL INITIATIVE; the eye rays break on his Shield; FIREBALL! — close-up of the d20 tumbling
          across the table: NAT 20! A bead of flame, a huge bloom: CRITICAL HIT! The Beholder burns and
          crashes; and, as Beholders do, it dreams another Beholder into being for the loop.
  nat1  - the same opening, but the d20 lands on a 1: NAT 1. The fireball pops straight up and comes
          down on his own hat: CRITICAL FAIL. The Beholder laughs at him; he cleans himself up with
          PRESTIDIGITATION."""
from engine import *

THEME = 'dnd'
N_ = 360
CX, BX, BY = 30, 146, 28                                            # the wizard; the Beholder's centre

# the wizard: the blue pointed hat with a star, the purple robe, the white beard
WPAL = {'1':(60,74,176),'2':(255,226,90),'3':(96,62,156),'4':(64,40,112),'6':(236,236,240)}
HAT = ["..1.........","..11........","...111......","...1121.....","..1111111...","111111111111"]

def _wizard(spr):
    g=[list(r) for r in overlay(spr,HAT,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=top+4 and r-4<=x<=r and y<top+8: g[y][x]='6'          # the beard
            elif c=='O' and y>=top+5: g[y][x]='3' if (x+y)%5 else '2'               # the starry robe
            elif c=='o' and y>=top+5: g[y][x]='4'
    return S([''.join(x) for x in g])
WIZ=variant(_wizard)
# soot all over after a NAT 1: every colour darkened, the eyes still white
SOOT={k:tuple(int(c*0.45) for c in v) for k,v in WPAL.items()}
SOOT.update({'O':(96,64,54),'o':(70,48,40),'K':(240,240,240),'6':(120,116,116)})
PAPER, PAPER_INK = (232,214,170), (92,60,30)

# ---- background: a dungeon hall --------------------------------------------------------------------------
def _dungeon(d):
    d.rectangle([0,0,W,H],fill=(34,32,42))
    rr=random.Random(2020)
    for y in range(0,48,6):                                         # the stone blocks
        off=(y//6)%2*7
        for x in range(-off,W,14):
            c=rr.randint(44,58); d.rectangle([x,y,x+12,y+4],fill=(c,c-2,c+8))
    d.polygon([(78,48),(78,22),(92,12),(106,22),(106,48)],fill=(20,18,26))   # an arched doorway
    d.arc([78,12,106,32],180,360,fill=(70,66,80),width=2)
    for x in (4,180):                                                # cobwebs
        for k in range(4): d.line([x,0,x+(10 if x<W//2 else -10)-k*2,k*3+2],fill=(110,110,120))
    for x in (40,140): d.rectangle([x-1,22,x+1,30],fill=(80,60,40))  # torch sconces
    d.rectangle([0,48,W,H],fill=(52,48,56))                          # flagstones
    for y in (52,57,62): d.line([0,y,W,y],fill=(40,36,44))
    for x in range(0,W,12):
        for y,o in ((48,0),(52,6),(57,0),(62,6)): d.line([x+o,y,x+o,y+4],fill=(40,36,44))
register_bg(THEME, lambda v: (v+30,v+28,v+40), decor=_dungeon)

@fx('dd_torch')
def _fx_torch(d,im,e,f):
    _,x=e; rr=random.Random((f//2)%30+x)                              # a 60-frame flicker: it loops
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-22,0,x+22,44],fill=60)
    im.paste((255,170,80),(0,0),g.filter(ImageFilter.GaussianBlur(8))); d=ImageDraw.Draw(im)
    for _ in range(3):
        h=rr.randint(4,7); dx=rr.randint(-1,1); d.polygon([(x-2+dx,22),(x+dx,22-h),(x+2+dx,22)],fill=rr.choice([(255,200,70),(255,120,40)]))

# ---- effects ----------------------------------------------------------------------------------------
@fx('dd_caption')
def _fx_caption(d,im,e,f):
    """The DM's narration: a parchment box with brown ink, centred at x."""
    _,lines,cx,y=e; lines=[lines] if isinstance(lines,str) else lines
    w=max(len(l) for l in lines)*4+7; h=len(lines)*7+4; x=max(1,min(W-w-1,int(cx-w/2)))
    d.rectangle([x,y,x+w,y+h],fill=PAPER,outline=PAPER_INK); d.line([x+1,y+h+1,x+w+1,y+h+1],fill=(40,30,20))
    for i,l in enumerate(lines): text(d,l,x+4,y+3+i*7,PAPER_INK,shadow=None)

@fx('dd_staff')
def _fx_staff(d,im,e,f):
    """The staff in his back hand, the crystal on top (glow 0..1)."""
    _,x,feet,glow=e; x=int(x)
    d.line([x,feet,x,feet-22],fill=(110,76,44)); d.line([x-1,feet-21,x+1,feet-23],fill=(140,100,60))
    c=(120,220,255) if glow<0.5 else (230,250,255)
    if glow>0:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-8,feet-33,x+8,feet-17],fill=int(160*glow))
        im.paste((120,220,255),(0,0),g.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    d.polygon([(x,feet-28),(x+2,feet-25),(x,feet-22),(x-2,feet-25)],fill=c)

@fx('dd_shield')
def _fx_shield(d,im,e,f):
    """The Shield spell: a shimmering blue hexagon in front of him."""
    _,x,y,a=e
    pts=[(x+math.cos(k*math.pi/3)*5,y+math.sin(k*math.pi/3)*11) for k in range(6)]
    d.polygon(pts,outline=(150,210,255) if f%2 else (220,240,255))
    if a>0.5: d.line([x,y-10,x,y+10],fill=(150,210,255))

@fx('dd_ray')
def _fx_ray(d,im,e,f):
    _,x0,y0,x1,y1,c=e; d.line([x0,y0,x1,y1],fill=c); d.point((int(x1),int(y1)),fill=(255,255,255))

@fx('dd_bead')
def _fx_bead(d,im,e,f):
    """The bead of flame a Fireball starts as, with its trail."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-2,y-2,x+2,y+2],fill=(255,150,40)); d.point((x,y),fill=(255,250,200))
    for k in range(1,5): d.point((x-k*2,y+(k%2)),fill=(255,110,30) if k%2 else (255,200,90))

@fx('dd_bloom')
def _fx_bloom(d,im,e,f):
    """The Fireball going off: a sphere of flame blooming, licking outward (r grows, a fades)."""
    _,x,y,r,a=e; x,y,r=int(x),int(y),int(r)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    md.ellipse([x-r,y-r,x+r,y+r],fill=int(230*a))
    im.paste((255,120,30),(0,0),m.filter(ImageFilter.GaussianBlur(2)))
    m2=Image.new('L',(W,H),0); ImageDraw.Draw(m2).ellipse([x-r*0.65,y-r*0.65,x+r*0.65,y+r*0.65],fill=int(240*a))
    im.paste((255,220,120),(0,0),m2.filter(ImageFilter.GaussianBlur(2))); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(int(16*a)):
        t=rr.uniform(0,6.283); L=r+rr.randint(0,6)
        d.line([x+math.cos(t)*r*0.8,y+math.sin(t)*r*0.8,x+math.cos(t)*L,y+math.sin(t)*L],fill=(255,170,60))

# ---- the Beholder -----------------------------------------------------------------------------------
BH,BH_D,BH_S=(156,76,116),(110,48,84),(196,110,150)
STALKS=[(-0.5,-12),(-0.9,-10),(-1.3,-6),(0.3,-12),(0.8,-10),(1.2,-6),(-0.1,-13),(1.5,-2)]   # (lean, height)
def beholder(d,x,y,f,eye='open',mood='angry',charred=False,flat=0.0):
    """The Beholder, facing left: a floating orb, one great eye, a fanged mouth, eight eyestalks.
    mood: angry | laugh | ko; flat 0..1 squashes it on the floor."""
    x,y=int(x),int(y); body=(60,40,40) if charred else BH; dark=(40,26,26) if charred else BH_D
    ry=int(13*(1-0.45*flat)); rx=int(13*(1+0.3*flat))
    for i,(lean,hgt) in enumerate(STALKS):                            # the eyestalks, waving
        if flat>0.5: continue
        sw=math.sin(f*math.tau/36+i*1.3)*2 if mood!='ko' else 3
        bx,by=x+int(lean*7),y-ry+3; tx,ty=bx+int(lean*6+sw),by+hgt+(4 if mood=='ko' else 0)
        d.line([bx,by,(bx+tx)//2+int(sw),(by+ty)//2,tx,ty],fill=dark,width=2)
        d.ellipse([tx-2,ty-2,tx+2,ty+2],fill=(236,230,200) if not charred else (120,110,90),outline=OUT)
        if mood=='laugh': d.line([tx-1,ty,tx+1,ty],fill=OUT)
        else: d.point((tx-1,ty),fill=(30,120,60))
    d.ellipse([x-rx,y-ry,x+rx,y+ry],fill=body,outline=OUT)
    if not charred:
        for sx,sy in ((5,-6),(8,3),(-2,8)): d.point((x+sx,y+sy),fill=BH_S)
    ex,ey=x-3,y-3-int(2*flat)
    if eye=='open':
        d.ellipse([ex-6,ey-5,ex+6,ey+5],fill=(240,236,214),outline=OUT); d.ellipse([ex-4,ey-3,ex+1,ey+3],fill=(60,170,90))
        d.ellipse([ex-3,ey-2,ex,ey+2],fill=(10,10,10))
        d.line([ex-7,ey-6,ex+6,ey-4],fill=OUT,width=2)                # the scowl
    elif eye=='laugh': d.arc([ex-6,ey-4,ex+6,ey+4],200,340,fill=OUT,width=2)
    else:
        d.line([ex-5,ey-3,ex+3,ey+3],fill=OUT,width=2); d.line([ex-5,ey+3,ex+3,ey-3],fill=OUT,width=2)   # x'd out
    my=y+5-int(3*flat)
    if mood=='laugh': d.chord([x-10,my-2,x+4,my+8],0,180,fill=(40,10,20),outline=OUT)
    else: d.chord([x-10,my-1,x+3,my+5],0,180,fill=(40,10,20),outline=OUT)
    for tx in range(x-9,x+3,3): d.polygon([(tx,my+1),(tx+2,my+1),(tx+1,my+3)],fill=(240,236,220))   # the fangs

@fx('dd_beholder')
def _fx_beholder(d,im,e,f):
    _,x,y,eye,mood,charred,flat,a=e
    if a>=1: beholder(d,x,y,f,eye,mood,charred,flat); return
    if a<=0: return
    L=im.copy(); beholder(ImageDraw.Draw(L),x,y,f,eye,mood,charred,flat)
    im.paste(Image.blend(im,L,a))

@fx('dd_dream')
def _fx_dream(d,im,e,f):
    """A thought bubble from the fallen Beholder, a little Beholder inside it (k 0..1)."""
    _,x,y,k=e
    for i,(dx,dy,r) in enumerate(((4,-6,1),(8,-12,2))):
        if k>i*0.2: d.ellipse([x+dx-r,y+dy-r,x+dx+r,y+dy+r],fill=(236,236,244))
    if k>0.4:
        r=int(10*min(1,(k-0.4)/0.3)); cx,cy=x+14,y-26
        d.ellipse([cx-r-4,cy-r,cx+r+4,cy+r],fill=(236,236,244),outline=(160,160,180))
        if r>6: d.ellipse([cx-5,cy-5,cx+5,cy+5],fill=BH,outline=OUT); d.ellipse([cx-3,cy-2,cx+1,cy+2],fill=(240,236,214)); d.point((cx-1,cy),fill=OUT)

# ---- close-up: the d20 ------------------------------------------------------------------------------
def d20(d,cx,cy,r,ang,num,col):
    """A d20 seen face-on: a hexagon outline, the triangle of the top face, the number in it."""
    pts=[(cx+math.cos(ang+k*math.pi/3)*r,cy+math.sin(ang+k*math.pi/3)*r) for k in range(6)]
    d.polygon(pts,fill=col,outline=(20,16,30))
    tri=[(cx+math.cos(ang-math.pi/2+k*2*math.pi/3)*r*0.62,cy+math.sin(ang-math.pi/2+k*2*math.pi/3)*r*0.62) for k in range(3)]
    for p,q in zip(tri,[pts[(k*2+1)%6] for k in range(3)]): pass
    for k in range(6): d.line([pts[k],tri[(k//2)%3]],fill=tuple(max(0,v-50) for v in col))
    d.polygon(tri,fill=tuple(min(255,v+30) for v in col),outline=(20,16,30))
    return tri

def closeup_d20(t,f,result):
    """Primer plano: the d20 tumbling across the table — and landing on result (20 or 1)."""
    good=result==20
    im=Image.new('RGB',(W,H),(96,60,34)); d=ImageDraw.Draw(im)
    for y in range(0,H,9): d.line([0,y,W,y],fill=(76,46,26))         # the planks of the table
    for x in (30,92,150): d.line([x,0,x,H],fill=(80,50,28))
    land=0.42
    if t<land:                                                       # rolling in from the left, bouncing
        p=t/land; cx=int(lerp(-20,70,p)); cy=int(34-abs(math.sin(p*math.pi*3))*16*(1-p)); ang=p*9
        num=str(random.Random(int(p*30)).randint(2,19))
    else: cx,cy,ang,num=70,34,0.0,str(result)
    d.ellipse([cx-18,52,cx+18,58],fill=(70,42,22))                   # its shadow
    col=(220,40,50) if not good else (200,30,40)
    if t>=land and good:
        k=min(1,(t-land)/0.12)
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([cx-36,cy-36,cx+36,cy+36],fill=int(200*k))
        im.paste((255,214,90),(0,0),g.filter(ImageFilter.GaussianBlur(8))); d=ImageDraw.Draw(im)
    if t>=land and not good: col=(150,40,46)
    d20(d,cx,cy,20,ang,num,col)
    big_text(im,num,cy-4,(255,255,255) if not (t>=land and good) else (255,240,150),scale=2,cx=cx,outline=(40,10,10))
    if t>=land and good:
        rr=random.Random(f)
        for _ in range(10): d.point((cx+rr.randint(-30,30),cy+rr.randint(-26,26)),fill=(255,250,200))
    if t>=land+0.06:
        big_text(im,"NAT 20!" if good else "NAT 1.",22,(255,226,90) if good else (200,200,210),scale=3 if good else 2,cx=144,outline=(80,30,0) if good else (40,40,50))
    if t>=land and not good and t>=land+0.2: im=fade_to(im,(30,30,50),0.3)
    if t<0.05: zoom_lines(d)
    return im

# ---- the clips --------------------------------------------------------------------------------------
def bob(f): return round(2*math.sin(2*math.pi*f/40))                  # 40-frame bob: N_ is a multiple

def opening(s,f):
    """The shared opening: ROLL INITIATIVE, the eye rays break on his Shield, FIREBALL!, ROLL A D20.
    Returns (pose, staff glow)."""
    pose,glow=guard_pose(f),0.0
    if 16<=f<50: s['fx'].append(('dd_caption',"ROLL INITIATIVE!",92,3))
    if 28<=f<48:
        pose='charge'; s['fx'].append(('dd_shield',CX+12,GROUND-10,1))
        for i,c in enumerate(((255,90,90),(120,255,120),(140,170,255))):
            if 30+i*5<=f<36+i*5:
                tx,ty=BX+int(STALKS[i][0]*13),BY-13+STALKS[i][1]
                s['fx'].append(('dd_ray',tx,ty,CX+12,GROUND-10+i*3,c)); s['fx'].append(('spark',CX+12,GROUND-10+i*3,3))
    if 54<=f<92:
        pose,glow='armsup',min(1,(f-54)/10)
        callout(s,"FIREBALL!",y=2,c=(255,170,70)); s['fx'].append(('dd_caption',"ROLL A D20.",92,12))
    return pose,glow

def finish(s,f,pose,glow,bh,flip=False,tint=None,x=CX):
    s['under'].append(('dd_torch',40)); s['under'].append(('dd_torch',140))
    if bh: s['under'].append(('dd_beholder',)+tuple(bh))
    s['under'].append(('dd_staff',x+(7 if flip else -7),GROUND,glow))
    s['actors']=[actor(WIZ[pose],x,flip=flip,pal=SOOT if tint else WPAL)]
    return s

def clip_nat20(f):
    s=scene(f,THEME)
    pose,glow=opening(s,f)
    by=BY+bob(f); bh=[BX,by,'open','angry',False,0.0,1.0]
    if 92<=f<156: s['image']=closeup_d20((f-92)/64,f,20); return s
    # the bead, the bloom
    if 156<=f<170:
        pose,glow='punch',1.0; p=(f-156)/14; s['fx'].append(('dd_bead',lerp(CX+10,BX-4,p),lerp(GROUND-10,by,p)-8*math.sin(p*math.pi)))
    if 170<=f<200:
        k=f-170; s['fx'].append(('dd_bloom',BX,by,min(34,6+k*3),1 if k<20 else 1-(k-20)/10))
        if k==0: s['flash']=1.0; s['fc']=(BX,by); s['flashc']=(255,220,150)
        if k<16: s['shake']=rshake(3 if k<8 else 1)
    if 172<=f<210: s['fx'].append(('big',"CRITICAL HIT!",3,(255,226,90)))
    # it burns and crashes
    if 176<=f<250: bh=[BX,by,'ko','ko',True,0.0,1.0]
    if 200<=f<214: p=(f-200)/14; bh=[BX,lerp(by,GROUND-8,p*p),'ko','ko',True,0.0,1.0]
    if 214<=f<300:
        bh=[BX,GROUND-6,'ko','ko',True,min(1,(f-214)/4),1.0 if f<280 else max(0,1-(f-280)/20)]
        if f<220: s['shake']=rshake(2)
        if f<240: s['fx'].append(('smoke',BX+random.randint(-10,10),GROUND-8-random.randint(0,10),2,(90,86,90)))
    if 218<=f<256: s['fx'].append(('dd_caption',"THE BEHOLDER FALLS.",92,3))
    if 214<=f<246: pose='armsup' if (f//6)%2 else 'guard'               # a little victory dance
    # ...and dreams another Beholder into being
    if 252<=f<300: s['fx'].append(('dd_dream',BX,GROUND-14,min(1,(f-252)/20)))
    if 258<=f<302: s['fx'].append(('dd_caption',["BEHOLDERS DREAM","OTHER BEHOLDERS."],80,3))
    if 300<=f<330:
        p=(f-300)/30; bh=[BX,lerp(GROUND-26,BY,ease(p))+bob(f)*p,'open','angry',False,0.0,min(1,p*1.5)]
    if f>=330: bh=[BX,by,'open','angry',False,0.0,1.0]
    return finish(s,f,pose,glow,bh)

def clip_nat1(f):
    s=scene(f,THEME)
    pose,glow=opening(s,f)
    by=BY+bob(f); bh=[BX,by,'open','angry',False,0.0,1.0]
    x,flip,tint=CX,False,None
    if 92<=f<156: s['image']=closeup_d20((f-92)/64,f,1); return s
    # the fireball pops straight up... and comes down on his hat
    if 156<=f<176:
        pose,glow='armsup',1.0; p=(f-156)/20
        s['fx'].append(('dd_bead',CX+1,lerp(GROUND-26,-6,math.sin(p*math.pi/2)) if p<0.5 else lerp(-6,GROUND-18,(p-0.5)*2)))
    if 176<=f<182: s['fx'].append(('dd_bloom',CX,GROUND-16,6+(f-176)*2,1)); s['shake']=rshake(2)
    if 176<=f<214: s['fx'].append(('big',"CRITICAL FAIL",3,(220,220,230)))
    if 180<=f<214:                                                    # hat on fire, running in circles
        k=f-180; x=CX+int(14*math.sin(k*0.4)); flip=math.cos(k*0.4)<0; pose='dash'
        s['fx'].append(('fire',x,GROUND-18,3))
    if 182<=f<270: tint=None if f>=270 else ((104,94,94) if 214<=f else None)
    if 214<=f<270: tint=(104,94,94); pose=guard_pose(f); s['fx'].append(('smoke',x+random.randint(-2,2),GROUND-20-random.randint(0,6),1,(90,90,96)))
    # the Beholder laughs at him
    if 214<=f<264:
        bh=[BX,by+(f%4<2),'laugh','laugh',False,0.0,1.0]
        if (f//8)%2: s['fx'].append(('dmg',"HA",BX+10+(f//8)%3*4,BY-22,(255,200,220)))
        s['fx'].append(('dd_caption',"IT LAUGHS AT YOU.",80,3))
    # PRESTIDIGITATION
    if 270<=f<306:
        pose,glow='armsup',1.0; s['fx'].append(('big',"PRESTIDIGITATION",3,(170,230,255)))
        rr=random.Random(f)
        for _ in range(8): s['fx'].append(('twinkle',CX+rr.randint(-10,10),GROUND-rr.randint(0,22),1))
        if f<280: tint=(104,94,94)
    if 306<=f<316: glow=max(0,1-(f-306)/10)
    return finish(s,f,pose,glow,bh,flip,tint,x)

CLIPS = [clip('nat20', N_, clip_nat20), clip('nat1', N_, clip_nat1)]
