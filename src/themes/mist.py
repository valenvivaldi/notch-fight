"""Mistborn (Brandon Sanderson): Claude as Vin, Mistborn, vs a Steel Inquisitor in Luthadel at night.
Ash falls and the mists thicken; the Inquisitor drops from the rooftops. Vin burns steel (blue lines
to every metal), Pushes off a dropped coin into the air and rains coins on him; he Pushes them all
back. Close-up: ATIUM — her eyes flare and shadows of the next second trail her face. His three axe
swings cut her atium shadows as she dodges; from behind him she Pulls the spike out of his back.
The coins fly home along their lines.
Shared by the Mistborn sub-themes: VIN, INQ, the mists, the ash, the allomantic lines and coins."""
from engine import *

THEME = 'mist'
DEFAULT_OFF = True            # niche (books): users turn it on with ./clips.sh enable mist
N_ = 264

LINE, LINE_HI = (110,170,255), (200,225,255)
COIN = (206,166,96)
ASH = (150,146,140)
# Vin: short dark hair, dark clothes; the mistcloak is drawn apart ('mist_cloak')
VPAL = {'l':(44,36,44), 'f':(76,64,74), 'a':(58,60,72), 'i':(42,44,54)}
# the Inquisitor: grey robe, pale skin, eye tattoos, silver spikes through the eyes
IPAL = {'g':(104,104,114), 'G':(78,78,88), 'P':(200,194,188), 't':(70,40,52), 'D':(226,230,240)}

HAIR = ["..llllllll..", ".llllllllll.", "llflllllfll."]

def _vin(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
    return S([''.join(x) for x in g])
VIN=variant(_vin)

INQ=poses(S([
"......PPPP......",".....PPPPPP.....",".....tDttDt.....",".....PPPPPP.....","......PkkP......",
".......PP.......","....gggggggg....","...gggggggggg...","..PggggGgggggP..","..PgggggGggggP..",
"..P.gggggggg.P..","....gggGgggg....","....ggggGggg....","...gggggggggg...","...gggGgggggg...",
"...ggggggGggg...","..gggggggggggg..","..gggggggggggg..","..kkk......kkk..",]),8,'P',4)

GRIP = {'guard':(13,4), 'guard2':(13,4), 'punch':(16,5), 'charge':(15,5), 'dash':(16,5), 'armsup':(12,0)}
def hand(pose,x,feet,flip=False):
    col,row=GRIP[pose]; return hand_at(VIN[pose],x,int(feet),flip,col,row,h=11)
def chest(x,feet): return x, feet-6

# ---------------------------------------------------------------- the city, the ash, the mists
def _luthadel(d):
    """Luthadel at night: rooftops, a keep with the spires of Kredik Shaw, a few lit windows."""
    roofs=[(0,40),(14,36),(26,40),(40,34),(58,38),(74,33),(96,37),(160,35),(176,39),(185,39)]
    d.polygon([(0,GROUND)]+roofs+[(185,GROUND)],fill=(20,20,28))
    for x0,top in ((112,14),(120,8),(128,12),(136,6),(144,16)):          # Kredik Shaw's spires
        d.polygon([(x0-3,34),(x0,top),(x0+3,34)],fill=(26,24,34))
    d.rectangle([108,30,150,GROUND],fill=(24,22,32))
    for x,y in ((18,42),(46,40),(64,44),(118,38),(140,42),(168,44)): d.point((x,y),fill=(120,96,50))
register_bg(THEME, lambda v: (v//2+4,v//2+4,v//2+10), decor=_luthadel)

def _fog_mask():
    """A tileable, blurred band of mist (2x the width so it can scroll)."""
    m=Image.new('L',(W*2,H),0); d=ImageDraw.Draw(m); rr=random.Random(4242)
    for _ in range(26):
        x=rr.randint(0,W*2); y=rr.randint(8,H); w=rr.randint(30,70); h=rr.randint(4,9)
        for dx in (-W*2,0,W*2): d.ellipse([x+dx-w,y-h,x+dx+w,y+h],fill=rr.randint(70,150))
    return m.filter(ImageFilter.GaussianBlur(6))
FOG=_fog_mask()

@fx('mist_fog')
def _fx_fog(d,im,e,f):
    """The mists drifting left to right; density 0..1. P: the clip's length (one crossing per loop)."""
    _,dens,*P=e; P=P[0] if P else N_; off=int((f%P)*W/P)
    band=FOG.crop((W-off,0,W*2-off,H)).point(lambda v: int(v*dens))
    im.paste((226,230,240),(0,0),band)

@fx('mist_ash')
def _fx_ash(d,im,e,f):
    """Ash falling on Luthadel, forever. P: the clip's length (each flake falls a whole number of times
    per loop, so it loops)."""
    _,*P=e; P=P[0] if P else N_
    rr=random.Random(77)
    for i in range(22):
        x0=rr.randint(0,W); k=rr.randint(2,4); ph=rr.randint(0,H)
        y=(ph+(f%P)*H*k/P)%H; x=(x0+math.sin(4*math.pi*f/P+i)*3)%W
        d.point((int(x),int(y)),fill=ASH if i%3 else (110,106,100))

@fx('mist_cloak')
def _fx_cloak(d,im,e,f):
    """Vin's mistcloak: tassels from the shoulders, trailing behind her (sw: -1..1 sideways motion)."""
    _,x,feet,flip,sw,*P=e; back=1 if flip else -1; P=P[0] if P else N_
    m=max(1,round(P*0.35/(2*math.pi)))                               # about the old sway, a whole number per loop
    for k in range(6):
        sx=x+back*(1+k)-(0 if flip else 1); sy=feet-9
        L=7+k%2; wav=math.sin(2*math.pi*m*f/P+k*0.9)
        ex=sx+back*(2+abs(sw)*5)+wav; ey=sy+L-abs(sw)*3
        d.line([sx,sy,ex,ey],fill=(96,100,110) if k%2 else (120,124,134))

@fx('mist_lines')
def _fx_lines(d,im,e,f):
    """Allomantic lines: pale blue, from the chest to every metal source; they shimmer."""
    _,x0,y0,targets=e
    for i,(tx,ty) in enumerate(targets):
        n=max(2,int(math.hypot(tx-x0,ty-y0)/3))
        for j in range(n):
            if (j+f+i)%4==0: continue
            t=j/n; d.point((int(lerp(x0,tx,t)),int(lerp(y0,ty,t))),fill=LINE if (j+i)%3 else LINE_HI)
        d.point((int(tx),int(ty)),fill=LINE_HI)

@fx('mist_coin')
def _fx_coin(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x,y,x+1,y],fill=COIN); d.point((x,y-1),fill=(250,220,150))

@fx('mist_axe')
def _fx_axe(d,im,e,f):
    """Obsidian axe from the hand at angle a (degrees)."""
    _,hx,hy,a=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    tx,ty=hx+c*11,hy+s*11
    d.line([hx-c*2,hy-s*2,tx,ty],fill=(90,64,44))
    d.polygon([(tx,ty),(tx-s*4+c*1,ty+c*4+s*1),(tx-c*3-s*3,ty-s*3+c*3)],fill=(30,26,40),outline=(90,80,120))

@fx('mist_spike')
def _fx_spike(d,im,e,f):
    _,x,y=e; d.line([x-3,y,x+3,y],fill=(226,230,240)); d.point((x+3,y),fill=(255,255,255))

def closeup_atium(t,f):
    """Primer plano: Vin's eyes flare with atium; shadows of the next second trail her face; ATIUM."""
    im=Image.new('RGB',(W,H),(8,8,14)); d=ImageDraw.Draw(im)
    FX['mist_fog'](d,im,('mist_fog',0.35),f)
    def face(dx,alpha):
        L=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(L); a=int(255*alpha)
        dd.rectangle([22+dx,14,82+dx,64],fill=(217,119,87,a)); dd.rectangle([76+dx,14,82+dx,64],fill=(168,80,54,a))
        dd.rectangle([18+dx,4,86+dx,16],fill=VPAL['l']+(a,))
        for x in range(20,86,7): dd.polygon([(x+dx,16),(x+7+dx,16),(x+3+dx,22)],fill=VPAL['l']+(a,))
        dd.rectangle([14+dx,10,22+dx,34],fill=VPAL['l']+(a,))                 # short hair at the side
        for x0 in (32,56):
            dd.rectangle([x0+dx,28,x0+14+dx,34],fill=(24,14,12,a))
        dd.line([42+dx,50,62+dx,50],fill=(80,30,24,a))
        im.paste(L,(0,0),L)
    lit=t>=0.2
    if lit:                                                                     # the shadows of the next second
        for k,dx in enumerate((14,8)): face(dx,0.18+0.08*k)
    face(0,1.0)
    if lit:
        for x0 in (32,56):
            glow=(255,255,255) if (f//2)%2 else (220,236,255)
            d.rectangle([x0+4,29,x0+10,33],fill=(160,190,230)); d.rectangle([x0+6,30,x0+8,32],fill=glow)
    if t>=0.35: FX['big'](d,im,('big',"ATIUM",18,(236,236,244),142),f)
    if t>=0.55: text(d,"I SEE WHAT COMES",112,38,(170,200,240))
    if t<0.06: zoom_lines(d)
    return im

# ---------------------------------------------------------------- the clip
IX=150                      # where the Inquisitor lands
DROP=(34,GROUND-1)          # the coin Vin drops to Push off
TARGETS=[(IX-8,GROUND-4-(i%3)*6) for i in range(6)]
SHOWER=(62,65,68,71,74,77)  # a coin leaves her hand every 3 frames
SCATTER=[(40+i*5+(i%2)*3,GROUND-1) for i in range(6)]   # where the Pushed-back coins land
ATTACKS=((150,36),(168,None),(186,96))                  # (swing frame, where Vin dodges to; None = jumps)

def vin_state(f):
    """(x, feet, pose, flip, sideways motion) for Vin at frame f."""
    x,y,pose,flip,sw=30,GROUND,guard_pose(f),False,0
    if 50<=f<62:                                   # Pushes off the dropped coin: up into the air
        p=(f-50)/12; x,y,pose,sw=ez(30,70,p),GROUND-26*math.sin(p*math.pi/2),'armsup',1
    if 62<=f<82: x,y,pose=70,GROUND-26+math.sin(f*0.3),'punch' if (f-62)%3<2 else 'guard'
    if 82<=f<96:                                   # Pushed back: falls, rolls
        p=(f-82)/14; x,y,pose,sw=ez(70,50,p),lerp(GROUND-26,GROUND,min(1,p*1.6)),'hurt',-1
    if 96<=f<140: x=50
    if 140<=f<200:
        x=50
        for sw_f,to in ATTACKS:
            if f>=sw_f-2:
                if to is None: x=36; y=GROUND-18*math.sin(min(1,(f-sw_f+2)/10)*math.pi) if f<sw_f+8 else GROUND
                else: x=ez(x if sw_f==150 else 36,to,(f-sw_f+2)/4); y=GROUND
        pose='dash' if any(s-2<=f<s+2 for s,_ in ATTACKS) else guard_pose(f)
        if 186<=f<192: y=GROUND-14*math.sin((f-186)/6*math.pi)          # the leap over him
    if 200<=f<236: x,pose=96,'charge' if f<216 else guard_pose(f)
    if 236<=f<256: x,flip,pose,sw=ez(96,30,(f-236)/20),True,guard_pose(f),-1
    return x,y,pose,flip,sw

def inq_state(f):
    """(x, feet, pose, alpha) for the Inquisitor, or None."""
    if f<14: return None
    if f<24: return IX,lerp(-6,GROUND,((f-14)/10)**2),'idle',1
    x,pose=IX,'idle'
    if 80<=f<90: pose='attack'
    if 140<=f<150: x=ez(IX,76,(f-140)/10)
    if f>=150: x=76 if f<168 else 64
    if 160<=f<168: x=ez(76,64,(f-160)/8)
    for sw_f,_ in ATTACKS:
        if sw_f-3<=f<sw_f+3: pose='attack'
    if 206<=f<216: pose='hurt'
    alpha=1
    if f>=214: pose='hurt'; alpha=max(0,1-(f-214)/22)
    return x,GROUND,pose,alpha

def clip_inquisitor(f):
    s=scene(f,THEME)
    s['under'].append(('mist_ash',))
    dens=0.25 if f<14 else (min(0.4,0.25+(f-14)/30*0.15) if f<230 else 0.4-(f-230)/34*0.15)
    s['under'].append(('mist_fog',dens))
    vx,vy,vpose,vflip,sw=vin_state(f)
    acts=[]
    # 1) the Inquisitor drops from the rooftops
    iq=inq_state(f)
    if 22<=f<28: s['shake']=rshake(2); s['fx'].append(('dust',IX-6,GROUND-1)); s['fx'].append(('dust',IX+6,GROUND-1))
    if 24<=f<42: callout(s,"STEEL INQUISITOR",c=(226,230,240))
    # 2) steel: lines to her coins and his spikes; the dropped coin, the Push up
    lines=[]
    if 40<=f<96:
        if 42<=f<58: callout(s,"STEEL",c=LINE_HI)
        lines+= [(IX-2,GROUND-16),(IX+1,GROUND-16)] if iq else []
    if 46<=f<62:
        cx,cy=(lerp(vx,DROP[0],min(1,(f-46)/3)),lerp(vy-6,DROP[1],min(1,(f-46)/3)))
        s['fx'].append(('mist_coin',cx,cy)); lines.append((cx,cy))
    # 3) the coin shower, and 4) the Push back
    for i,t0 in enumerate(SHOWER):
        if t0<=f<80:
            hx,hy=hand('punch',70,GROUND-26); tx,ty=TARGETS[i]; p=min(1,(f-t0)/5)
            s['fx'].append(('mist_coin',lerp(hx,tx,p),lerp(hy,ty,p))); lines.append((lerp(hx,tx,p),lerp(hy,ty,p)))
            if f-t0 in (5,6): s['fx'].append(('spark',tx+2,ty,3))
        if 80<=f<220:
            p=min(1,(f-80)/8); x,y=lerp(TARGETS[i][0],SCATTER[i][0],p),lerp(TARGETS[i][1],SCATTER[i][1],p)-10*math.sin(p*math.pi)
            if f>=220: continue
            s['fx'].append(('mist_coin',x,y))
            if f<88: lines.append((x,y))
    if 80<=f<86: s['shake']=rshake(2); s['flash']=0.3; s['fc']=(IX-10,GROUND-10); s['flashc']=LINE_HI
    # 5) close-up
    if 96<=f<140: s['image']=closeup_atium((f-96)/44,f); return s
    # 6) atium: shadows of the next second show where she goes; the axe cuts where she was
    for sw_f,to in ATTACKS:
        if sw_f-8<=f<sw_f-2:
            fx_,fy,fp,_,_=vin_state(sw_f+2)
            acts.append(actor(VIN[fp],fx_,fy,pal=VPAL,alpha=0.35,tint=(200,220,255)))
    # 7) the spike in his back
    if 200<=f<216 and iq:
        sx=iq[0]+6; sy=GROUND-12
        if f<206: lines.append((sx,sy)); callout(s,"IRON",c=LINE_HI)
        else:
            p=min(1,(f-206)/5); s['fx'].append(('mist_spike',lerp(sx,vx-4,p),lerp(sy,vy-8,p)))
            if f<209: s['flash']=0.5; s['fc']=(sx,sy); s['flashc']=(255,255,255); s['shake']=rshake(2)
    # 8) the coins fly home
    if 220<=f<236:
        for i,(cx,cy) in enumerate(SCATTER):
            p=ease((f-220-i)/8)
            if p>=1: continue
            x,y=lerp(cx,vx,p),lerp(cy,vy-6,p); s['fx'].append(('mist_coin',x,y)); lines.append((x,y))
        if f<228: callout(s,"IRON",c=LINE_HI)
    if lines: s['fx'].append(('mist_lines',*chest(vx,vy),lines))
    if iq and iq[3]>0:
        ix,iy,ipose,ia=iq
        acts.append(actor(INQ[ipose],ix,iy,flip=True,pal=IPAL,alpha=ia))
        swinging=[sw_f for sw_f,_ in ATTACKS if sw_f-3<=f<sw_f+3]
        if 140<=f<200 and ia>0:
            a=(-150+(f-swinging[0]+3)*25) if swinging else -120
            s['fx'].append(('mist_axe',ix-8,GROUND-11,a))
    s['under'].append(('mist_cloak',vx,vy,vflip,sw))
    acts.append(actor(VIN[vpose],vx,vy,flip=vflip,pal=VPAL))
    s['actors']=acts
    return s

CLIPS = [clip('inquisitor', N_, clip_inquisitor)]
