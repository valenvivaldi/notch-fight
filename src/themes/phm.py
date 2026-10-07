"""Project Hail Mary (Andy Weir): Claude as Ryland Grace in the Hail Mary's lab, Tau Ceti in the window.
No fight: the rival is a problem, and Rocky is a friend. Two clips on the same neutral pose.
  rocky      - the Blip-A arrives, a xenonite tunnel joins the ships, Rocky taps on the wall; his chords
               turn into AMAZE AMAZE AMAZE; close-up: fists on both sides of the glass, FIST MY BUMP.
  astrophage - Astrophage swarms over the star and the lab goes cold; Grace works the bench; close-up:
               Taumoeba eating Astrophage under the microscope; the sample goes out, the star comes back,
               Rocky cheers on the monitor: IT WORKS!
Only moments from the first half of the book. Niche (books): shipped off by default."""
from engine import *

THEME = 'phm'
DEFAULT_OFF = True
N_ = 300

INK = (18,18,24)
STAR, STAR_HI = (255,170,70), (255,236,190)
NOTE_COLOURS = ((255,150,120),(150,210,255),(190,255,150),(255,220,120))
# Grace: sandy hair, the blue-grey mission jumpsuit
GPAL = {'l':(196,160,96), 'f':(150,118,66), 'a':(88,104,132), 'i':(64,78,102)}
HAIR = ["..llllllll..", ".llllllllll.", "llflllllfll."]

def _grace(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
    return S([''.join(x) for x in g])
GRACE=variant(_grace)

# ---------------------------------------------------------------- the lab
def _lab(d):
    """The Hail Mary's lab: panelled walls, two monitors, a bench with tubes, the window onto Tau Ceti."""
    d.rectangle([0,0,W,GROUND],fill=(42,46,58))
    for x in range(0,W,24): d.line([x,0,x,GROUND],fill=(36,40,50))
    d.line([0,40,W,40],fill=(36,40,50))
    for x0 in (6,40):                                                                   # monitors
        d.rectangle([x0,6,x0+30,24],fill=(14,20,24),outline=(90,96,110))
    d.rectangle([64,44,112,GROUND],fill=(70,74,86)); d.line([64,44,112,44],fill=(120,124,138))   # the bench
    for x in (70,76,82): d.rectangle([x,36,x+2,44],outline=(170,200,220))                  # tube rack
    d.rectangle([128,4,183,40],fill=(4,4,12),outline=(110,116,130))                       # the window
    rr=random.Random(7)
    for _ in range(18): d.point((rr.randint(130,181),rr.randint(6,38)),fill=(150,150,170))
    d.line([155,4,155,40],fill=(110,116,130))
register_bg(THEME, lambda v: (v//2+8,v//2+10,v//2+16), decor=_lab)

@fx('phm_star')
def _fx_star(d,im,e,f):
    """Tau Ceti through the window, and the Petrova line (Astrophage's infrared trail); bright 0..1."""
    _,b=e; cx,cy=166,20
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).ellipse([cx-12,cy-12,cx+12,cy+12],fill=int(90*b))
    im.paste(STAR,(0,0),L.filter(ImageFilter.GaussianBlur(3)))
    r=5; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=tuple(int(lerp(60,c,b)) for c in STAR_HI))
    for k in range(20):                                                                     # the Petrova line
        x=cx-2-k*1.4; y=cy+6+k*0.8+math.sin(2*math.pi*f/50+k*0.5)
        if x>129 and (k+f//4)%3: d.point((int(x),int(y)),fill=(int(160*b)+40,40,50))

@fx('phm_tint')
def _fx_tint(d,im,e,f):
    """The lab light going cold as the star dims (a: 0..1)."""
    _,a=e; im.paste(fade_to(im,(20,30,60),min(0.6,max(0,a))))

@fx('phm_screens')
def _fx_screens(d,im,e,f):
    """Data on the monitors: a scrolling trace (green, or red when the star is failing)."""
    _,bad=e
    for x0 in (6,40):
        c=(220,80,80) if bad else (110,230,140)
        pts=[(x0+2+i,15+int(4*math.sin((i+x0)*0.4+2*math.pi*f/25))*(0.3 if bad else 1)) for i in range(27)]
        d.line(pts,fill=c)

@fx('phm_rocky')
def _fx_rocky(d,im,e,f):
    """Rocky: a rocky five-legged carapace, no eyes, legs out like a spider; wave raises the front legs.
    s scales him (1 = full size)."""
    _,x,feet,wave,s=e; x=int(x)
    body,dark,hi=(128,124,116),(84,80,74),(170,166,156)
    leg=(150,146,136)                                                                      # lighter legs read on the haze
    top=feet-int(16*s)
    legs=[(-12,0),(-6,1),(0,1),(6,1),(12,0)]
    for i,(dx,_) in enumerate(legs):                                                        # five legs
        kx=x+dx*s; ky=top+int(8*s)
        up=wave and i in (0,4) and (f//4)%2
        fx_=x+dx*1.6*s; fy=(top+int(2*s)) if up else feet
        d.line([x,top+int(6*s),kx,ky],fill=leg,width=2); d.line([kx,ky,fx_,fy],fill=leg,width=2)
        d.point((int(fx_),int(fy)),fill=hi)
    pts=[(x-9*s,top+8*s),(x-6*s,top+1*s),(x+6*s,top+1*s),(x+9*s,top+8*s),(x,top+12*s)]      # the carapace
    d.polygon(pts,fill=body,outline=INK)
    d.line([x-4*s,top+4*s,x+2*s,top+9*s],fill=hi); d.line([x+5*s,top+3*s,x+1*s,top+7*s],fill=dark)
    d.ellipse([x-1*s,top+2*s,x+1*s,top+4*s],fill=dark)                                      # the vent on top

@fx('phm_notes')
def _fx_notes(d,im,e,f):
    """Rocky's chords: little musical notes rising from (x,y), drifting towards (tx,ty) as p goes 0..1."""
    _,x,y,tx,ty,p=e
    for i in range(7):
        q=min(1,max(0,p*1.6-i*0.09))
        if q<=0 or q>=1: continue
        nx=lerp(x,tx+(i-3)*9,q)+math.sin(f*0.3+i)*2; ny=lerp(y,ty,q)-math.sin(q*math.pi)*10
        c=NOTE_COLOURS[i%4]; d.ellipse([nx-1,ny,nx+1,ny+2],fill=c); d.line([nx+1,ny+1,nx+1,ny-4],fill=c)

@fx('phm_ship')
def _fx_ship(d,im,e,f):
    """The Blip-A out of the window: a spindly silhouette with a warm glow; s: size."""
    _,x,y,s=e
    d.line([x-8*s,y,x+8*s,y],fill=(140,120,100),width=max(1,int(2*s)))
    d.ellipse([x-3*s,y-2*s,x+3*s,y+2*s],fill=(150,130,110),outline=INK)
    d.point((int(x+8*s),int(y)),fill=(255,190,120))

@fx('phm_tunnel')
def _fx_tunnel(d,im,e,f):
    """The xenonite tunnel on Rocky's side: hexagonal panels appear top to bottom (p 0..1); Rocky's side is
    warm and hazy; the dividing wall glints."""
    _,p=e; x0=120
    rows=int(p*9)
    if rows<=0: return
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).rectangle([x0,0,W,min(GROUND,rows*7)],fill=110)
    im.paste((120,104,70),(0,0),L)                                                         # the ammonia haze
    for r in range(rows):
        for c in range(9):
            cx=x0+4+c*8+(r%2)*4; cy=3+r*7
            if cx<W and cy<=GROUND-4: d.regular_polygon((cx,cy,4),6,outline=(160,150,110))
    if p>=1:
        d.line([x0,0,x0,GROUND],fill=(200,230,240)); d.line([x0+1,0,x0+1,GROUND],fill=(120,150,160))
        if (f//6)%3==0: d.line([x0,10+(f%30),x0,14+(f%30)],fill=(255,255,255))

@fx('phm_tap')
def _fx_tap(d,im,e,f):
    _,x,y,k=e
    if k<6: d.arc([x-k,y-k,x+k,y+k],-60,60,fill=(220,240,250))

@fx('phm_swarm')
def _fx_swarm(d,im,e,f):
    """Astrophage: black specks swarming round the star (dens 0..1)."""
    _,dens=e; rr=random.Random(33)
    for i in range(int(90*dens)):
        a=rr.random()*6.28+f*0.02*(1 if i%2 else -1); r=rr.uniform(3,20)
        x=166+math.cos(a)*r; y=20+math.sin(a)*r*0.8
        if 129<x<182 and 5<y<39: d.point((int(x),int(y)),fill=(6,6,8))

@fx('phm_bench')
def _fx_bench(d,im,e,f):
    """Bubbling tubes and the sample jar (glow 0..1)."""
    _,glow=e
    for i,x in enumerate((70,76,82)):
        d.rectangle([x+1,40-(i%2),x+1,43],fill=(120,200,160))
        if (f//3+i)%4==0: d.point((x+1,37-(f%3)),fill=(200,255,220))
    if glow>0:
        L=Image.new('L',(W,H),0); ImageDraw.Draw(L).ellipse([90,32,108,50],fill=int(70*glow))
        im.paste((120,255,170),(0,0),L.filter(ImageFilter.GaussianBlur(2)))
        d.rectangle([96,36,102,44],fill=(80,140,110),outline=(200,230,220))

@fx('phm_capsule')
def _fx_capsule(d,im,e,f):
    _,x,y=e; d.ellipse([x-2,y-1,x+2,y+1],fill=(200,210,220)); d.point((int(x)-3,int(y)),fill=(120,255,170))

@fx('phm_rocky_screen')
def _fx_rocky_screen(d,im,e,f):
    """Rocky cheering on the left monitor (a tiny Rocky bouncing, notes around)."""
    L=Image.new('RGB',(29,17),(14,20,24)); dd=ImageDraw.Draw(L)
    _fx_rocky(dd,L,('phm_rocky',14,15-(f//3)%2,True,0.6),f)
    im.paste(L,(7,7))
    for i in range(3):
        x=8+i*9+math.sin(f*0.3+i)*2; y=10-((f*0.5+i*4)%8)
        c=NOTE_COLOURS[i]; d.point((int(x),int(y)),fill=c); d.point((int(x)+1,int(y)-2),fill=c)

@fx('phm_text')
def _fx_text(d,im,e,f):
    _,txt,y,c=e; big_text(im,txt,y,c,shadow=(0,0,0),outline=(0,0,0))

def closeup_fists(t,f):
    """Primer plano: two fists meet on either side of the xenonite; a soft glow; FIST MY BUMP."""
    im=Image.new('RGB',(W,H),(30,34,44)); d=ImageDraw.Draw(im)
    d.rectangle([W//2,0,W,H],fill=(96,84,58))                                               # Rocky's side
    for r in range(10):
        for c in range(13):
            cx=W//2+4+c*8+(r%2)*4; cy=3+r*7
            if cx<W: d.regular_polygon((cx,cy,4),6,outline=(140,128,94))
    d.line([W//2,0,W//2,H],fill=(210,236,244)); d.line([W//2+1,0,W//2+1,H],fill=(130,160,170))
    p=ease(min(1,t/0.3))
    lx=int(lerp(-10,W//2-24,p))                                                            # Grace's fist
    d.rounded_rectangle([lx,34,lx+22,54],radius=5,fill=(217,119,87),outline=(120,60,40))
    for k in range(4): d.line([lx+22,37+k*4,lx+18,37+k*4],fill=(168,80,54))
    d.rectangle([lx-30,40,lx,50],fill=GPAL['a'])                                            # the sleeve
    rx=int(lerp(W+10,W//2+4,p))                                                            # Rocky's claw
    d.polygon([(rx,36),(rx+20,32),(rx+26,44),(rx+20,56),(rx,52)],fill=(128,124,116),outline=INK)
    for k in (38,44,50): d.line([rx,k,rx+6,k-1],fill=(84,80,74))
    d.line([rx+26,44,W,40],fill=(84,80,74),width=4)
    if t>=0.3:
        L=Image.new('L',(W,H),0); ImageDraw.Draw(L).ellipse([W//2-14,30,W//2+14,58],fill=int(90*min(1,(t-0.3)*4)))
        im.paste((255,244,210),(0,0),L.filter(ImageFilter.GaussianBlur(4)))
        big_text(im,"FIST MY BUMP",6,(255,236,190),shadow=(0,0,0),outline=(0,0,0))
    if t<0.06: zoom_lines(d,(200,210,220))
    return im

def closeup_microscope(t,f):
    """Primer plano: the microscope's round field - Taumoeba (green) eating Astrophage (black), one by one."""
    im=Image.new('RGB',(W,H),(10,10,14)); d=ImageDraw.Draw(im)
    cx,cy,r=W//2,32,29
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(210,220,200))
    rr=random.Random(515); specks=[(cx+rr.uniform(-22,22),cy+rr.uniform(-20,20)) for _ in range(26)]
    eaten=int(len(specks)*ease((t-0.1)/0.8))
    for i,(x,y) in enumerate(specks):
        if i>=eaten: d.ellipse([x-1,y-1,x+1,y+1],fill=(8,8,10))
    for k in range(5):                                                                     # Taumoeba, wandering
        a=k*1.25+f*0.05; ax=cx+math.cos(a)*14*(1-t*0.3); ay=cy+math.sin(a*1.3)*12
        rb=3+int(t*3)+k%2
        d.ellipse([ax-rb,ay-rb*0.8,ax+rb,ay+rb*0.8],fill=(120,200,120),outline=(60,130,70))
        d.point((int(ax),int(ay)),fill=(40,90,50))
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(60,60,70),width=3)
    for x0 in (10,W-40): d.rectangle([x0,20,x0+30,44],fill=(30,32,40),outline=(70,74,86))    # the eyepiece housing
    if t<0.06: zoom_lines(d,(200,210,220))
    return im

# ---------------------------------------------------------------- clip 1: rocky
def clip_rocky(f):
    s=scene(f,THEME)
    s['under'].append(('phm_star',1.0)); s['fx'].append(('phm_screens',False)); s['fx'].append(('phm_bench',0))   # the lab, as astrophage has it
    gx,gpose,gflip=40,guard_pose(f),False
    tunnel=0; rocky=None
    if 14<=f<50: s['under'].append(('phm_ship',lerp(182,150,(f-14)/36),26,lerp(0.4,1,(f-14)/36)))
    if 50<=f<290: s['under'].append(('phm_ship',150,26,1)) if f<270 else s['under'].append(('phm_ship',lerp(150,184,(f-270)/20),26,lerp(1,0.4,(f-270)/20)))
    if 50<=f<262: tunnel=min(1,(f-50)/40)
    if 262<=f<280: tunnel=1-(f-262)/18
    if 90<=f<262:
        rx=ez(206,150,(f-90)/12) if f<102 else (ez(150,206,(f-246)/16) if f>=246 else 150)
        rocky=(rx,GROUND,228<=f<246,1.5)
    if 102<=f<130:                                                         # toc toc
        k=(f-102)%10; s['fx'].append(('phm_tap',121,GROUND-12,k))
    if 104<=f<130: gx,gpose=ez(40,100,(f-104)/20),'dash' if f<124 else 'guard'
    if 130<=f<262: gx=100
    if 130<=f<178:
        s['fx'].append(('phm_notes',146,GROUND-14,92,8,min(1,(f-130)/20)))
        if f>=138: s['fx'].append(('phm_text',"AMAZE AMAZE AMAZE",4,(255,220,140)))       # 2 s
    if 178<=f<228: s['image']=closeup_fists((f-178)/50,f); return s
    if 262<=f<290: gx,gflip,gpose=ez(100,40,(f-262)/28),True,guard_pose(f)
    if f>=290: gx,gflip=40,False
    if tunnel>0: s['under'].append(('phm_tunnel',tunnel))
    if rocky: s['under'].append(('phm_rocky',)+rocky)
    s['actors']=[actor(GRACE[gpose],gx,flip=gflip,pal=GPAL)]
    return s

# ---------------------------------------------------------------- clip 2: astrophage
def clip_astrophage(f):
    s=scene(f,THEME)
    dens=0; bright=1.0
    if 14<=f<60: dens=(f-14)/46
    if 60<=f<200: dens=1
    if 200<=f<240: dens=1-(f-200)/40
    bright=1-0.75*dens
    s['under'].append(('phm_star',bright)); s['under'].append(('phm_swarm',dens))
    s['fx'].append(('phm_screens',dens>0.5 and f<236))
    gx,gpose,gflip=40,guard_pose(f),False
    glow=0
    if 56<=f<70: gx,gpose=ez(40,86,(f-56)/14),'dash'
    if 70<=f<176: gx,gpose=86,'punch' if (f//10)%2 else 'guard'
    if 76<=f<176: glow=min(1,(f-76)/20)
    s['fx'].append(('phm_bench',glow))
    if 120<=f<170: s['image']=closeup_microscope((f-120)/50,f); return s
    if 176<=f<194:                                                          # the sample goes out to the star
        gx,gpose=86,'punch'; p=(f-176)/18; s['fx'].append(('phm_capsule',lerp(104,166,p),lerp(40,20,p)))
    if 194<=f<198: s['flash']=0.5; s['fc']=(166,20); s['flashc']=STAR_HI
    if 176<=f<236 and f>=194: gx=86
    if 236<=f<276:
        s['fx'].append(('phm_rocky_screen',))
        if f>=242: s['fx'].append(('phm_text',"IT WORKS!",4,(190,255,170)))                # 1.6 s
    if 236<=f<270: gx=86
    if 270<=f<294: gx,gflip,gpose=ez(86,40,(f-270)/24),True,guard_pose(f)
    if f>=294: gx,gflip=40,False
    s['fx'].append(('phm_tint',0.45*dens))
    s['actors']=[actor(GRACE[gpose],gx,flip=gflip,pal=GPAL)]
    return s

CLIPS = [clip('rocky', N_, clip_rocky), clip('astrophage', N_, clip_astrophage)]
