"""Studio Ghibli sub-theme "ghibli-totoro" (My Neighbor Totoro): the bus stop in the rain. No fight.
Claude as Satsuki waits under her umbrella at dusk; fireflies, puddles, the camphor forest. Totoro comes
and stands beside her, rain dripping off the leaf on his head. She lends him the spare umbrella; drops
from the trees plink on it and he loves it: he hops, and every tree lets its water go at once. Close-up:
his grin under the umbrella. The Catbus's eyes glow far down the road; it runs up and waits, Totoro
leaves her a bundle of acorns wrapped in leaves and boards; the Catbus runs off grinning. No text."""
from engine import *

THEME = 'ghibli-totoro'
N_ = 336

INK = (26,30,34)
RAIN = (150,170,190)
FIREFLY, FIREFLY_HI = (200,236,120), (250,255,200)
# Satsuki: short dark hair, a yellow shirt; the umbrellas are drawn apart
SPAL = {'l':(58,40,34), 'f':(88,62,50), 'a':(236,186,70), 'i':(206,150,52)}
HAIR = ["..llllllll..", ".llllllllll.", "lllfllllflll"]

def _satsuki(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top,min(top+2,len(g))):                              # a short bob down the sides
        for x in (l-1,r+1):
            if 0<=x<len(g[0]) and g[y][x]=='.': g[y][x]='l'
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
    return S([''.join(x) for x in g])
SATSUKI=variant(_satsuki)

# ---------------------------------------------------------------- the bus stop at dusk
def _dusk(d):
    """A painted dusk: sky gradient, layered camphor trees, the road, the bus stop sign, a lamp post."""
    for y in range(0,GROUND):
        t=y/GROUND; d.line([0,y,W,y],fill=(int(lerp(28,46,t)),int(lerp(44,70,t)),int(lerp(78,76,t))))
    rr=random.Random(1988)
    for layer,(c,base) in enumerate((((34,58,52),30),((26,46,40),38),((20,36,32),44))):   # canopy, far to near
        for _ in range(9):
            x=rr.randint(-10,W+10); r=rr.randint(12,22)-layer*2; y=base+rr.randint(-6,4)
            d.ellipse([x-r,y-r*0.8,x+r,y+r*0.8],fill=c)
    for x in (18,152,176): d.rectangle([x-1,34,x+1,GROUND],fill=(24,26,24))                 # trunks
    d.rectangle([0,GROUND-4,W,GROUND],fill=(48,52,50))                                        # the road
    for x0,w in ((20,18),(104,26),(150,14)): d.ellipse([x0,GROUND-3,x0+w,GROUND-1],fill=(64,80,96))   # puddles
    d.line([64,GROUND,64,22],fill=(80,70,60)); d.ellipse([58,14,70,26],fill=(200,190,170),outline=(90,80,70))   # sign
    d.line([61,18,67,18],fill=(90,80,70)); d.line([61,21,67,21],fill=(90,80,70))
    d.line([82,GROUND,82,16],fill=(60,58,54)); d.line([82,16,88,16],fill=(60,58,54))       # lamp post
    d.rectangle([87,16,90,18],fill=(255,226,150))
register_bg(THEME, lambda v: (v//3+10,v//2+14,v//3+16), decor=_dusk, clip_ground=True)   # Totoro sinks into the Catbus

@fx('tot_lamp')
def _fx_lamp(d,im,e,f):
    """The lamp's warm glow, soft and blended."""
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).ellipse([64,4,112,GROUND+6],fill=40)
    im.paste((255,214,140),(0,0),L.filter(ImageFilter.GaussianBlur(6)))

@fx('tot_rain')
def _fx_rain(d,im,e,f):
    """Slanted rain and ripples in the puddles; dens 0..1."""
    _,dens=e; rr=random.Random((f%42)*7)                       # a 42-frame cycle: the clip loops
    for _ in range(int(46*dens)):
        x=rr.randint(-10,W); y=rr.randint(-4,H); d.line([x,y,x-2,y+5],fill=RAIN)
    for x0,w in ((20,18),(104,26),(150,14)):
        for k in range(2):
            ph=((f%16)/16+k*0.5+x0*0.01)%1; r=1+ph*4
            if dens>0.2: d.ellipse([x0+w//2-r+k*4,GROUND-2-r*0.3,x0+w//2+r+k*4,GROUND-2+r*0.3],outline=(110,130,150) if ph<0.6 else (80,96,112))

@fx('tot_fireflies')
def _fx_fireflies(d,im,e,f):
    for i in range(6):
        x=(20+i*31+math.sin(2*math.pi*f/N_+i)*8)%W; y=24+math.sin(4*math.pi*f/N_+i*1.7)*8+i%3*6
        if (f//4+i)%6: d.point((int(x),int(y)),fill=FIREFLY_HI if (f//2+i)%4==0 else FIREFLY)

@fx('tot_umbrella')
def _fx_umbrella(d,im,e,f):
    """An open umbrella: canopy centred at (x,top), handle down to hand_y."""
    _,x,top,hand_y,c,w=e
    d.pieslice([x-w,top,x+w,top+w],180,360,fill=c,outline=INK)
    for k in (-w//2,0,w//2): d.line([x,top+w//2,x+k,top+w//2],fill=tuple(max(0,v-30) for v in c))
    d.line([x,top+w//2,x,hand_y],fill=(60,48,40)); d.point((x+1,hand_y),fill=(60,48,40))

@fx('tot_closed')
def _fx_closed(d,im,e,f):
    """The spare umbrella, closed, held out."""
    _,x,y=e; d.line([x,y,x+9,y-3],fill=(40,40,56)); d.line([x+1,y+1,x+8,y-2],fill=(60,60,80)); d.point((x+9,y-4),fill=(60,48,40))

@fx('tot_totoro')
def _fx_totoro(d,im,e,f):
    """Totoro, facing left: grey, a pale belly with chevrons, pointed ears, round eyes, whiskers.
    lift: pixels off the ground (the hop); grin 0..1; leaf: the leaf on his head."""
    _,x,lift,grin,leaf,blink=e; x=int(x); feet=GROUND-int(lift)
    grey,dark,belly,chev=(128,128,122),(92,92,88),(222,216,196),(104,100,92)
    d.polygon([(x-8,feet-38),(x-6,feet-48),(x-3,feet-38)],fill=grey,outline=INK)            # ears
    d.polygon([(x+3,feet-38),(x+6,feet-48),(x+8,feet-38)],fill=grey,outline=INK)
    d.ellipse([x-17,feet-42,x+17,feet+1],fill=grey,outline=INK)                               # body
    d.ellipse([x-12,feet-28,x+12,feet-2],fill=belly)                                          # belly
    for cx,cy in ((x-5,feet-24),(x,feet-25),(x+5,feet-24),(x-3,feet-20),(x+3,feet-20)):
        d.line([cx-2,cy-1,cx,cy+1],fill=chev); d.line([cx,cy+1,cx+2,cy-1],fill=chev)
    for ex in (x-8,x+4):                                                                     # eyes
        if blink: d.line([ex,feet-33,ex+4,feet-33],fill=INK)
        else: d.ellipse([ex,feet-36,ex+4,feet-31],fill=(250,250,244),outline=INK); d.ellipse([ex+1,feet-35,ex+3,feet-32],fill=INK)
    d.point((x-1,feet-32),fill=INK); d.point((x,feet-32),fill=INK)                             # nose
    for s in (-1,1):                                                                          # whiskers
        for k in (0,2): d.line([x+s*6,feet-29+k,x+s*14,feet-30+k*1.5],fill=dark)
    if grin>0:
        w=int(4+grin*8); d.chord([x-w,feet-31-int(grin*2),x+w,feet-23],0,180,fill=(70,30,30),outline=INK)
        for k in range(-w+2,w-1,3): d.line([k+x,feet-27,k+x+1,feet-25],fill=(250,250,244))
    else: d.line([x-2,feet-28,x+2,feet-28],fill=INK)
    d.line([x-16,feet-20,x-19,feet-14],fill=grey); d.line([x+16,feet-20,x+19,feet-14],fill=grey)   # arms
    if leaf:
        d.polygon([(x-3,feet-42),(x+4,feet-46),(x+2,feet-41)],fill=(90,170,80),outline=(40,90,40))
        if (f//6)%2: d.point((x,feet-40),fill=(180,210,240))                                  # a drip

@fx('tot_drops')
def _fx_drops(d,im,e,f):
    """Water shaken off the trees: drops falling, a little splash where they land (n of them)."""
    _,n,x0,x1,top,land,k=e; rr=random.Random(4040)
    for i in range(n):
        x=rr.uniform(x0,x1); t=(k*0.09+rr.random())%1 if n<10 else min(1,k/14+rr.random()*0.3)
        y=lerp(top,land,t)
        if t<1: d.line([x,y,x,y+2],fill=(170,200,230))
        else: d.point((x-1,land),fill=(170,200,230)); d.point((x+1,land),fill=(170,200,230))

@fx('tot_catbus')
def _fx_catbus(d,im,e,f):
    """The Catbus, facing left: a long ginger body with windows, many running legs, a grin, eyes that are
    headlights. s: scale (it grows as it comes down the road); run: legs moving."""
    _,x,y,s,run,door=e
    if s<0.4:                                                                                 # far away: just the eyes
        for dx in (-3*s*4,3*s*4): d.ellipse([x+dx-1,y-1,x+dx+1,y+1],fill=(255,236,120))
        return
    body,dark,stripe=(214,140,58),(150,90,34),(186,110,44)
    w,h=int(40*s),int(14*s); top=int(y-h)
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).polygon([(x-w,top+h//2),(x-w-30*s,top+h//2-6*s),(x-w-30*s,top+h//2+8*s)],fill=36)
    im.paste((255,236,150),(0,0),L)                                                            # headlight beam
    for k in range(6):                                                                        # legs
        lx=x-w+6+k*(2*w-12)/5; ph=math.sin(f*0.8+k*1.3)*3*s*run
        d.line([lx,y-2,lx+ph,y+4*s],fill=dark,width=2)
    d.rounded_rectangle([x-w,top,x+w,y],radius=int(6*s),fill=body,outline=INK)
    for k in range(4): d.line([x-w+10+k*int(18*s),top+2,x-w+14+k*int(18*s),top+6],fill=stripe)
    for k in range(4):                                                                        # windows
        wx=x-w+int(10*s)+k*int(16*s)
        d.rectangle([wx,top+int(3*s),wx+int(10*s),top+int(8*s)],fill=(250,226,150) if not (door and k==1) else (60,30,20),outline=dark)
    d.polygon([(x-w+2,top),(x-w+5,top-6*s),(x-w+9,top)],fill=body,outline=INK)               # ears
    d.polygon([(x-w+12,top),(x-w+15,top-6*s),(x-w+19,top)],fill=body,outline=INK)
    for ex in (x-w+4,x-w+13): d.ellipse([ex,top+2,ex+4,top+6],fill=(255,236,120),outline=INK)  # headlight eyes
    if h>=10: d.chord([x-w+1,top+7,x-w+22,top+h-1],0,180,fill=(250,250,244),outline=INK)       # the grin
    d.line([x+w,top+4,x+w+8*s,top-4*s],fill=body,width=2)                                     # tail

@fx('tot_bundle')
def _fx_bundle(d,im,e,f):
    """Acorns wrapped in a leaf, tied with grass."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-3,y-2,x+3,y+2],fill=(90,160,80),outline=(40,90,40)); d.point((x,y-3),fill=(40,90,40))
    d.point((x-1,y),fill=(150,100,50)); d.point((x+1,y+1),fill=(150,100,50))

def closeup_grin(t,f):
    """Primer plano: Totoro's grin under the little umbrella, rain on the canopy. No text."""
    im=Image.new('RGB',(W,H),(30,44,56)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([0,y,W,y],fill=(int(lerp(26,40,y/H)),int(lerp(40,62,y/H)),int(lerp(70,72,y/H))))
    grey,belly=(128,128,122),(222,216,196)
    d.ellipse([22,14,162,150],fill=grey,outline=INK)                                          # the face fills the frame
    d.ellipse([52,52,132,150],fill=belly)
    g=ease((t-0.15)/0.35)
    for ex in (62,106):                                                                       # eyes, widening
        r=6+int(3*g); d.ellipse([ex-r,34-r,ex+r,34+r],fill=(250,250,244),outline=INK)
        d.ellipse([ex-r//2,34-r//2,ex+r//2,34+r//2],fill=INK); d.point((ex-r//3,34-r//3),fill=(255,255,255))
    d.polygon([(89,40),(95,40),(92,43)],fill=INK)                                             # nose
    for s in (-1,1):
        for k in (0,4): d.line([92+s*18,48+k,92+s*44,46+k*1.4],fill=(92,92,88))
    w=int(10+g*34); d.chord([92-w,40,92+w,62+int(g*6)],0,180,fill=(70,30,30),outline=INK)      # the grin
    for k in range(-w+4,w-3,6): d.polygon([(92+k,51),(92+k+4,51),(92+k+2,55)],fill=(250,250,244))
    d.pieslice([30,-40,154,20],0,180,fill=(40,40,56),outline=INK)                              # the umbrella's edge
    rr=random.Random(f)
    for _ in range(8):
        x=rr.randint(34,150); d.point((x,rr.randint(0,10)),fill=(170,200,230))
        d.line([x+rr.randint(-3,3),22,x,26],fill=(170,200,230))
    return im

# ---------------------------------------------------------------- the clip
CX, TX, BUS = 38, 100, 150        # Satsuki, Totoro, where the Catbus stops

def clip_busstop(f):
    s=scene(f,THEME)
    s['under'].append(('tot_lamp',))
    rain=1.0 if f<300 else lerp(0.6,1.0,(f-300)/20)
    if 170<=f<190: rain=1.0                                                    # plus the trees' shower below
    s['under'].append(('tot_rain',rain)); s['fx'].append(('tot_fireflies',))
    cx,cpose,cflip=CX,guard_pose(f),False
    t=None; bus=None; bundle=None
    # 1-2) waiting; Totoro comes and stands beside her
    if 50<=f<296:
        tx=ez(214,TX,(f-50)/50) if f<100 else TX
        lift=abs(math.sin(f*0.25))*2 if f<100 else 0
        t=dict(x=tx,lift=lift,grin=0,leaf=f<130,blink=f in (104,105,142,143),umbrella=False)
    # 3) the spare umbrella; drops plink on it; the hop and the shower
    if 110<=f<124: cx,cpose=ez(CX,62,(f-110)/14),'dash'
    if 124<=f<136:
        cx,cpose=62,'punch'; hx,hy=hand_at(SATSUKI['punch'],62,GROUND,False,16,5,h=11)
        s['fx'].append(('tot_closed',lerp(hx,TX-16,(f-124)/12),lerp(hy,GROUND-20,(f-124)/12)))
    if 136<=f<176: cx=ez(62,CX,(f-136)/20); cpose=guard_pose(f) if f>=140 else 'guard'
    if t and 134<=f<296: t['umbrella']=True
    if t and 140<=f<168:
        s['fx'].append(('tot_drops',6,TX-12,TX+12,0,GROUND-50,f-140)); t['grin']=min(1,(f-140)/12)
    if t and 160<=f<176:
        p=(f-160)/10; t['lift']=12*math.sin(min(1,p)*math.pi) if p<1 else 0; t['grin']=1
    if 168<=f<192: s['fx'].append(('tot_drops',60,0,W,0,GROUND-1,f-168))       # every tree lets go at once
    # 4) close-up
    if 192<=f<237: s['image']=closeup_grin((f-192)/45,f); return s
    # 5) the Catbus: far eyes, the run up, the bundle, boarding, off it goes
    if t and f>=237: t['grin']=0.4
    if 237<=f<257: p=(f-237)/20; bus=(lerp(178,176,p),GROUND-18,lerp(0.12,0.3,p),1,False)
    if 257<=f<271: p=ease((f-257)/14); bus=(lerp(230,BUS+10,p),GROUND,lerp(0.5,1,p),1,False)
    if 271<=f<296: bus=(BUS+10,GROUND,1,0,f>=279)
    if 267<=f<281:
        p=ease((f-267)/14); hx,hy=hand_at(SATSUKI['guard'],CX,GROUND,False,13,4,h=11)
        bundle=(lerp(TX-18,hx,p),lerp(GROUND-16,hy+2,p)-6*math.sin(p*math.pi))
    if 281<=f<300: hx,hy=hand_at(SATSUKI['guard'],CX,GROUND,False,13,4,h=11); bundle=(hx,hy+2)
    if t and 281<=f<296:
        t['x']=ez(TX,BUS,(f-281)/12); t['boarding']=True
        if f>=284: t['lift']=-(f-284)*7                                       # sinks into the bus
    if t and f>=290: t=None                                                  # aboard
    if 296<=f<312: p=(f-296)/16; bus=(lerp(BUS+10,-80,p*p),GROUND,1,1,False)
    # 6) she tucks the bundle away; back to the neutral pose
    if 298<=f<304: s['fx'].append(('twinkle',CX+6,GROUND-8,1))
    if t and t.get('boarding'):                                               # behind the bus: it swallows him
        s['under'].append(('tot_totoro',t['x'],t['lift'],t['grin'],False,False))
    if bus: s['under'].append(('tot_catbus',)+bus)
    acts=[actor(SATSUKI[cpose],cx,pal=SPAL)]
    s['actors']=acts
    hx,hy=hand_at(SATSUKI['guard'],cx,GROUND,cflip,13,4,h=11)
    s['fx'].append(('tot_umbrella',cx+2,GROUND-24,GROUND-10,(52,84,150),11))
    if t and not t.get('boarding'):
        s['fx'].append(('tot_totoro',t['x'],t['lift'],t['grin'],t['leaf'],t['blink']))
        if t['umbrella']: s['fx'].append(('tot_umbrella',t['x']-14,GROUND-int(t['lift'])-58,GROUND-int(t['lift'])-22,(40,40,56),7))
    if bundle: s['fx'].append(('tot_bundle',*bundle))
    return s


CLIPS = [clip('busstop', N_, clip_busstop)]
