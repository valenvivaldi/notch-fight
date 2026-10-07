"""Terminator 2: Claude (the T-800, leather jacket and shades) vs the T-1000 on a steel-mill catwalk.
The lever-action spin-cock, three shotgun blasts that open chrome holes which flow shut again, the
T-1000's arm-blade knocks the shades off (half of Claude's face is endoskeleton, a red eye glows) —
close-up of the red eye and the Terminator HUD choosing HASTA LA VISTA BABY — a shot into the
liquid-nitrogen tank freezes him, one more shot shatters him, the shards melt into silver puddles that
flow back together and re-form him, and Claude puts the shades back on: I'LL BE BACK."""
from engine import *

THEME = 'term'
N_ = 300

# Theme colours live in each actor's `pal` (no PAL.update: other themes are added in parallel).
T800_PAL={'1':(66,60,72),'2':(104,96,112),'3':(8,8,12),'4':(150,164,190),'5':(214,220,234),
          '6':(118,124,140),'7':(255,40,28),'8':(42,48,74),'9':(72,48,36)}
RED=(255,70,50)
FROST=(206,232,255)
SILVER=(192,198,212)

def _t800(spr, damaged):
    """Leather jacket, jeans, short hair; shades — or, damaged, a chrome half-face with a red eye."""
    g=[list(r) for r in spr]; h=len(g); top,l,r=body_box(spr)
    ky=next((y for y,row in enumerate(g) if 'K' in row),top+2)
    kx=[x for x,c in enumerate(g[ky]) if c=='K']
    for y in range(h):
        for x,c in enumerate(g[y]):
            if c=='.': continue
            inside=l<=x<=r
            if y>=h-2: g[y][x]='k' if y==h-1 else '8'                    # jeans + boots
            elif c=='o': g[y][x]='1'                                     # sleeves / hips
            elif inside and y-top>=5: g[y][x]='2' if x==r-2 else '1'     # jacket (lapel line)
            elif inside and y==top: g[y][x]='9'                          # short hair
            if damaged and top<=y<=top+4 and g[y][x] in 'OK9' and x>=l+5+(y%2):
                g[y][x]='6' if x==l+5+(y%2) else '5'                     # torn skin -> chrome
    if damaged:
        g[ky][max(kx)]='7'; g[ky+1][max(kx)]='7' if g[ky+1][max(kx)]!='.' else '.'
    else:
        for x in range(min(kx)-1,max(kx)+1):
            if g[ky][x] in 'OK': g[ky][x]='3'
        for y in (ky,ky+1):
            for x in kx:
                if g[y][x]=='K': g[y][x]='3'
        g[ky][min(kx)]='4'                                               # glint
    return S([''.join(r) for r in g])
T8=variant(lambda s: _t800(s,False))
T8D=variant(lambda s: _t800(s,True))

# T-1000: police uniform, 16x18, padded to 36 wide so growing the arm-blade never shifts the body.
T_BASE={'q':(96,66,44),'s':(226,186,152),'K':(24,14,12),'u':(46,62,124),'Y':(230,196,70),
        'k':(24,24,32),'H':(226,230,240),'h':(150,156,172),'c':(84,98,160)}
_T_RAW=[
"....qqqqqq......","...qqqqqqqq.....","...qssssssq.....","...ssKsssKs.....","...ssssssss.....",
"....ssssss......","..uuuucuuuuu....",".uuuuYcuuuuuu...",".uu.uuuuuu.uu...",".uu.uucuuu.uu...",
".ss.kkkkkk.ss...","....uuuuuu......","....uuuuuu......","....uu..uu......","....uu..uu......",
"....uu..uu......","....kk..kk......","...kkk..kkk.....",]
def _pad(rows): return S(['.'*10+r+'.'*10 for r in rows])
def _blade(n):
    """Front forearm turned into a silver blade n pixels long (rows 9-10 = hand height)."""
    g=[list(r) for r in _T_RAW]
    if n>0:
        g[9][11:13]=list('hh'); g[10][11:13]=list('HH')
        g[9]=g[9][:13]+list('h'*max(0,n-2))+g[9][13+max(0,n-2):]
        g[10]=g[10][:13]+list('H'*n)
    return _pad([''.join(r)[:26] for r in g])
T1K={'idle':_pad(_T_RAW)}
T1K['hurt']=hurt(T1K['idle'])
BLADES={n:_blade(n) for n in range(0,10)}
T1K['bhurt']=hurt(BLADES[9])

def _mix(a,b,k): return tuple(int(lerp(a[i],b[i],k)) for i in range(3))
def _lum(c): return (c[0]*3+c[1]*6+c[2])/10/255
def tpal(frost=0.0, chrome=0.0):
    """T-1000 palette pulled towards ice (frozen) or liquid metal (re-forming)."""
    out={}
    for ch,c in T_BASE.items():
        if frost: c=_mix(c,_mix((120,180,240),(236,248,255),_lum(c)),frost)
        if chrome: c=_mix(c,_mix((110,116,132),(236,240,250),_lum(c)),chrome)
        out[ch]=c
    return out

def _mill(d):
    """A dark steel mill: hanging chains, pipes, a catwalk rail and the liquid-nitrogen tank."""
    for x0,ln in ((44,16),(98,22),(128,12)):
        for y in range(0,ln,2): d.point((x0,y),fill=(34,30,32))
        d.arc([x0-2,ln-1,x0+2,ln+3],0,200,fill=(44,38,40))
    d.line([0,8,W,8],fill=(20,18,22)); d.line([175,0,175,36],fill=(30,32,40))
    d.line([0,GROUND-9,W,GROUND-9],fill=(30,26,28)); d.line([0,GROUND-5,W,GROUND-5],fill=(22,19,21))
    for x in range(4,W,18): d.line([x,GROUND-9,x,GROUND],fill=(26,22,24))
    d.rectangle([167,37,182,GROUND],fill=(26,30,38),outline=(52,58,72))    # LN2 tank
    d.line([169,39,169,GROUND-2],fill=(66,74,92)); d.rectangle([172,34,178,37],fill=(44,50,62))
    text(d,"LN2",169,46,(64,96,140),shadow=None)
register_bg(THEME, lambda v: (v,v*2//5,v//6), decor=_mill)

@fx('term_glow')
def _fx_glow(d,im,e,f):
    """Molten steel far below the catwalk: a low, slowly breathing orange glow + rising embers."""
    px=im.load()
    for x in range(W):
        k=round(0.55+0.25*math.sin(x*0.09+f*math.pi/30)+0.2*math.sin(x*0.23-f*math.pi/15),6)   # (rounded: float noise)
        for y in range(GROUND+3,H):
            a=k*(y-GROUND-2)/(H-GROUND-2)
            blend(px,x,y,(120,34,6),a*0.6)
    for i in range(7):
        x=(i*29+11)%W; y=H-1-((f+i*9)%30)*1.2
        if y>GROUND-24: d.point((x+int(math.sin(2*math.pi*(f+i*5)/20)*2),int(y)),fill=(200,90,30) if i%2 else (150,60,20))

@fx('term_gun')
def _fx_gun(d,im,e,f):
    """The lever-action shotgun held at a hand pivot, at angle a (0 = pointing right)."""
    _,x,y,a=e; ca,sa=math.cos(a),math.sin(a)
    P=lambda u,v: (x+ca*u-sa*v, y+sa*u+ca*v)
    d.line([P(-5,0),P(-1,0)],fill=(128,80,42)); d.line([P(-5,1),P(-2,1)],fill=(98,60,32))   # stock
    d.line([P(-1,0),P(3,0)],fill=(74,76,88)); d.line([P(-1,1),P(3,1)],fill=(58,60,70))      # receiver
    d.line([P(3,0),P(13,0)],fill=(112,116,130)); d.line([P(4,1),P(10,1)],fill=(128,80,42))   # barrel + fore-end
    d.point(P(1,2),fill=(90,92,104)); d.point(P(0,3),fill=(90,92,104)); d.point(P(2,3),fill=(90,92,104))  # lever loop

@fx('term_muzzle')
def _fx_muzzle(d,im,e,f):
    _,x,y=e
    d.polygon([(x,y-2),(x+6,y),(x,y+2)],fill=(255,170,60)); d.polygon([(x,y-1),(x+3,y),(x,y+1)],fill=(255,245,200))

@fx('term_line')
def _fx_line(d,im,e,f):
    _,x0,y0,x1,y1,c=e; d.line([x0,y0,x1,y1],fill=c)

@fx('term_hole')
def _fx_hole(d,im,e,f):
    """A shotgun hit on liquid metal: a chrome crater with peeled petals that flows shut again."""
    _,x,y,age=e
    r=3 if age<4 else max(0,3-(age-4)*0.5)
    if age<6: d.ellipse([x-2-age,y-(2+age)//2,x+2+age,y+(2+age)//2],outline=(150,156,172) if age<4 else (90,96,110))
    if r<=0: return
    rr=int(round(r))
    d.ellipse([x-rr-1,y-rr-1,x+rr+1,y+rr+1],fill=SILVER)
    if rr>=1: d.ellipse([x-rr+1,y-rr+1,x+rr-1,y+rr-1],fill=(58,62,76))
    if age<4:
        for k in range(5):
            a=k*1.26+0.4; d.point((x+math.cos(a)*(rr+2),y+math.sin(a)*(rr+2)),fill=(236,240,250))
    d.point((x-1,y-rr),fill=(250,250,255))

@fx('term_shades')
def _fx_shades(d,im,e,f):
    _,x,y,a=e; x,y=int(x),int(y)
    if abs(math.sin(a))<0.5: d.rectangle([x-2,y,x+2,y+1],fill=(10,10,14)); d.point((x-1,y),fill=(150,164,190)); d.line([x+3,y,x+4,y],fill=(60,60,70))
    else: d.rectangle([x,y-2,x+1,y+2],fill=(10,10,14)); d.point((x,y-1),fill=(150,164,190))

@fx('term_eye')
def _fx_eye(d,im,e,f):
    """The red eye's glow: a soft halo around the pixel, pulsing."""
    _,x,y,k=e; px=im.load()
    for dx in range(-3,4):
        for dy in range(-2,3):
            dist=abs(dx)+abs(dy)
            if 0<dist<=2: blend(px,x+dx,y+dy,(255,30,20),k*(0.4 if dist==1 else 0.15))

@fx('term_ln2')
def _fx_ln2(d,im,e,f):
    """Liquid nitrogen blasting out of the ruptured tank onto the T-1000, as white-blue vapour."""
    _,age,k=e; px=im.load(); x0,y0=172,40; rr=random.Random(f*7+3)
    for p in range(46):
        u=((age*4+p*13)%36)/36
        tx,ty=138+(p%7)*3,40+(p*5)%18
        x=lerp(x0,tx,u)+rr.uniform(-2,2); y=lerp(y0,ty,u)+rr.uniform(-2,2); rad=1+int(u*3)
        c=(236,246,255) if p%3 else (150,200,245)
        for dx in range(-rad,rad+1):
            for dy in range(-rad//2-1,rad//2+2): blend(px,int(x+dx),int(y+dy),c,0.35*k)

@fx('term_frost')
def _fx_frost(d,im,e,f):
    _,x,k=e; rr=random.Random(f//2*11+5)
    for _ in range(int(8*k)):
        sx=x+rr.randint(-7,7); sy=rr.randint(GROUND-18,GROUND-1)
        if (f+sx)%3: d.point((sx,sy),fill=(250,254,255))
        else: d.line([sx-1,sy,sx+1,sy],fill=(236,246,255)); d.line([sx,sy-1,sx,sy+1],fill=(236,246,255))

@fx('term_shard')
def _fx_shard(d,im,e,f):
    _,x,y,sz,c=e; x,y=int(x),int(y)
    if sz>=2: d.polygon([(x,y-1),(x+2,y),(x,y+1)],fill=c)
    else: d.point((x,y),fill=c)

@fx('term_drop')
def _fx_drop(d,im,e,f):
    _,x,y,w,c=e; x,y=int(x),int(y)
    d.ellipse([x-w,y-1,x+w,y+1],fill=c); d.point((x-w//2,y-1),fill=(246,248,255))

@fx('term_say')
def _fx_say(d,im,e,f):
    """2x shout that may contain an apostrophe (the font has none): drawn as a 2x4 tick."""
    _,txt,y,c=e; plain=txt.replace("'"," ")
    x0,*_=big_text(im,plain,y,c)
    for i,ch in enumerate(txt):
        if ch=="'":
            gx=x0+i*8+2; d.rectangle([gx+1,y+1,gx+2,y+4],fill=(0,0,0)); d.rectangle([gx,y,gx+1,y+3],fill=c)

# --- geometry helpers -----------------------------------------------------------------------------
_HAND={'charge':(15,5),'guard':(13,4),'guard2':(13,5)}
def gun_at(pose,cx,a=0.0):
    ox,oy=origin(CL[pose],cx); hx,hy=_HAND[pose]; return ('term_gun',ox+hx-1,oy+hy,a)
def tip(g):
    _,x,y,a=g; return x+math.cos(a)*14,y+math.sin(a)*14
def eye_of(spr,cx):
    ox,oy=origin(spr,cx)
    for y,row in enumerate(spr):
        if '7' in row: return ox+row.index('7'),oy+y
    return None

# Pre-computed shatter: shards taken from the frozen T-1000's own pixels, then flung with gravity.
SHATTER_X=142
def _shards():
    spr=BLADES[9]; ox,oy=origin(spr,SHATTER_X); w=len(spr[0]); rr=random.Random(1000)
    pts=[(ox+(w-1-x),oy+y) for y,row in enumerate(spr) for x,c in enumerate(row) if c!='.']
    out=[]
    for i,(x,y) in enumerate(rr.sample(pts,52)):
        vx=(x-SHATTER_X)*0.1+rr.uniform(-0.8,2.0); vy=rr.uniform(-3.4,-0.4)-(GROUND-y)*0.05
        path=[]; px,py,sx,sy=float(x),float(y),vx,vy
        for _ in range(20):
            path.append((px,py)); px=max(2,min(164,px+sx)); py+=sy; sy+=0.42
            if py>=GROUND-1: py=GROUND-1; sx*=0.3; sy=0
        out.append(dict(path=path,sz=1+(i%3==0),c=_mix((150,200,245),(240,250,255),rr.random())))
    return out
SHARDS=_shards()

def closeup_eye(t,f):
    """Primer plano: the half-chrome face, the red eye lighting up — then through it, the HUD."""
    if t>=0.3: return closeup_hud((t-0.3)/0.7,f)
    im=Image.new('RGB',(W,H),(6,4,6)); d=ImageDraw.Draw(im)
    d.rectangle([38,0,146,H],fill=(217,119,87)); d.rectangle([38,0,146,5],fill=(72,48,36))
    edge=lambda y: 96+((y*5)%7)-3+(2 if (y//6)%2 else 0)
    for y in range(0,H):
        e0=edge(y); v=int(118+34*math.sin(y*0.12))
        d.line([e0,y,146,y],fill=(v,v+6,v+18))
        d.point((e0-1,y),fill=(150,60,40)); d.point((e0-2,y),fill=(190,90,62))
    for y0 in (12,38,44): d.line([100,y0,146,y0],fill=(96,102,118))
    for x in range(102,146,6): d.line([x,52,x,H],fill=(70,74,88))                    # jaw pistons
    d.rectangle([62,18,68,32],fill=(24,14,12))                                         # the human eye
    on=ease(t/0.16)
    d.ellipse([112,14,134,34],fill=(30,30,38)); d.ellipse([115,17,131,31],fill=(60,64,76))
    px=im.load()
    for dx in range(-14,15):
        for dy in range(-10,11):
            dist=math.hypot(dx,dy*1.3)
            if dist<13: blend(px,123+dx,24+dy,(255,30,20),on*max(0,1-dist/13)*0.9)
    d.ellipse([119,20,127,28],fill=_mix((70,10,10),(255,50,36),on)); d.point((122,23),fill=_mix((90,20,20),(255,220,210),on))
    if t>0.2:   # dive into the eye
        r=int(ease((t-0.2)/0.1)*200); d.ellipse([123-r,24-r,123+r,24+r],fill=(60,4,3))
    if t<0.06:
        zoom_lines(d)
    return im

HUD_LINES=[(0.00,"TARGET ACQUIRED",3,3),(0.08,"THREAT: T-1000",3,10),(0.16,"POLYALLOY: MIMETIC",3,17),
           (0.26,"RESPONSE:",3,27),(0.32,"GO AWAY",11,34),(0.37,"COME BACK LATER",11,41),
           (0.42,"HASTA LA VISTA BABY",11,48)]
def closeup_hud(u,f):
    """Terminator vision: red monochrome, scan lines, the T-1000 targeted, the response chosen."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    d.line([0,61,W,61],fill=(70,70,70)); d.line([104,0,104,H],fill=(40,40,40))
    cv=Image.new('RGB',(20,20),(0,0,0)); draw(cv,S(_T_RAW),10,19,True,pal=T_BASE)
    im.paste(cv.resize((60,60),Image.NEAREST),(114,2))
    L=im.convert('L')
    im=Image.merge('RGB',(L.point(lambda v: min(255,int(26+v*1.05))),L.point(lambda v:int(v*0.2)),L.point(lambda v:int(v*0.16))))
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for y in range(1,H,2): md.line([0,y,W,y],fill=110)
    im=Image.composite(Image.new('RGB',(W,H),(0,0,0)),im,m); d=ImageDraw.Draw(im)
    sy=(f*3)%H; d.line([0,sy,W,sy],fill=(120,22,16))
    br=(255,70,50) if (f//3)%2 or u>0.2 else (150,30,20)
    for (x,y,sx,sy2) in ((112,2,1,1),(176,2,-1,1),(112,62,1,-1),(176,62,-1,-1)):
        d.line([x,y,x+6*sx,y],fill=br); d.line([x,y,x,y+6*sy2],fill=br)
    lock=ease(u/0.25); cx,cy=int(lerp(128,144,lock)),int(lerp(40,14,lock))
    d.ellipse([cx-6,cy-6,cx+6,cy+6],outline=br); d.line([cx-9,cy,cx-3,cy],fill=br); d.line([cx+3,cy,cx+9,cy],fill=br)
    d.line([cx,cy-9,cx,cy-3],fill=br); d.line([cx,cy+3,cx,cy+9],fill=br)
    sel=None if u<0.52 else (0 if u<0.6 else 1 if u<0.68 else 2)
    for i,(t0,s,x,y) in enumerate(HUD_LINES):
        if u<t0: continue
        n=min(len(s),int((u-t0)/0.06*len(s))+1)
        if i==0 and u>0.2 and (f//4)%2==0: continue            # TARGET ACQUIRED blinks
        c=(255,196,180) if i<4 else (230,90,70)
        if sel is not None and i==4+sel:
            if sel<2 or (f//2)%3: d.rectangle([x-2,y-1,x+len(s)*4,y+5],fill=(200,30,20))
            c=(255,236,226)
            d.polygon([(x-7,y),(x-4,y+2),(x-7,y+4)],fill=(255,236,226))
        text(d,s[:n],x,y,c,shadow=None)
    if u<0.06:
        zoom_lines(d,(255,190,180))
    return im

SHOTS=[(34,(-1,-11)),(48,(3,-14)),(62,(0,-17))]   # frame, hole offset from the T-1000 centre/feet

def clip_judgment(f):
    s=scene(f,THEME); s['under'].append(('term_glow',))
    cl=actor(T8[guard_pose(f)],30,pal=T800_PAL); tk=actor(T1K['idle'],150,flip=True,pal=tpal())
    gun=None
    # 1) the spin-cock (16-30), then three blasts while the T-1000 walks in (30-72)
    if 16<=f<72:
        cl['spr']=T8['charge']
        a=-2*math.pi*ease((f-16)/10) if f<28 else 0.0
        for sf,_ in SHOTS:
            if sf+3<=f<sf+9: a=-0.45*math.sin(math.pi*(f-sf-3)/6)     # lever cock
        cl['x']=30-(2 if any(0<=f-sf<2 for sf,_ in SHOTS) else 0)
        gun=gun_at('charge',cl['x'],a)
    if 30<=f<72:
        x=lerp(150,64,(f-30)/42); hurt_now=False
        for sf,(hx,hy) in SHOTS:
            if f>=sf: x+=7*max(0,1-(f-sf)/7)
            if 0<=f-sf<3: hurt_now=True
        tk.update(x=x,y=GROUND-(1 if (f//4)%2 else 0),spr=T1K['hurt'] if hurt_now else T1K['idle'])
        for sf,(hx,hy) in SHOTS:
            if 0<=f-sf<14: s['fx'].append(('term_hole',int(x+hx),GROUND+hy,f-sf))
    for sf,(hx,hy) in SHOTS:
        if f==sf:
            tx,ty=tip(gun); s['fx']+= [('term_muzzle',int(tx),int(ty)),('term_line',int(tx)+6,int(ty),int(tk['x'])-6,GROUND+hy,(255,236,150))]
            s['shake']=rshake(1)
        if 3<=f-sf<9: s['fx'].append(('mote',gun[1]-(f-sf-3)*2,gun[2]-6+((f-sf-6)**2)//3,(230,190,70)))  # spent shell
    # 2) the arm becomes a blade (72-82), the stab knocks the shades off (82-100)
    if 72<=f<82: tk.update(x=64,spr=BLADES[int(lerp(1,9,(f-72)/7))]); cl['spr']=T8['charge']; gun=gun_at('charge',30,0.35)
    if 82<=f<100:
        if f<84: tk.update(x=ez(64,68,(f-82)/2),spr=BLADES[9])
        elif f<90: tk.update(x=ez(68,48,(f-84)/2),spr=BLADES[9])
        else: tk.update(x=ez(48,70,(f-90)/8),spr=BLADES[9])
        if f<86: cl['spr']=T8['charge']; gun=gun_at('charge',30,0.35)
        else: cl.update(spr=T8D['hurt'],x=ez(30,22,(f-86)/5))
        if f==86: s['fx'].append(('spark',36,49,6)); s['shake']=rshake(2)
        if 86<=f<100:   # the shades spin away off the left edge
            u=f-86; s['fx'].append(('term_shades',36-u*3,49-u*2.4+u*u*0.14,u*0.9))
    if 100<=f<116:
        tk.update(x=70,spr=BLADES[9],y=GROUND-(1 if (f//6)%2 else 0))
        cl.update(spr=T8D[guard_pose(f)] if f>=104 else T8D['hurt'],x=ez(22,30,(f-100)/12) if f>=104 else 22)
        if f>=104: gun=gun_at(cl['spr'] is T8D['guard'] and 'guard' or 'guard2',cl['x'],0.6)
    # 3) primer plano: the red eye and the HUD
    if 116<=f<172: s['image']=closeup_eye((f-116)/56,f); return s
    # 4) blast him back to the tank, rupture it: liquid nitrogen
    if 172<=f<230:
        cl.update(spr=T8D['charge'],x=30-(2 if f-174 in (0,1) or f-188 in (0,1) or f-230 in (0,1) else 0))
        aim=-0.12 if 184<=f<192 else 0.0
        if 177<=f<183 or 191<=f<197: aim=-0.45*math.sin(math.pi*((f-177)%14)/6)
        gun=gun_at('charge',cl['x'],aim)
    if 172<=f<186:
        tk.update(spr=T1K['bhurt'] if f>=174 else BLADES[9],x=ez(70,146,(f-174)/10) if f>=174 else 70)
        if f==174:
            tx,ty=tip(gun); s['fx']+=[('term_muzzle',int(tx),int(ty)),('term_line',int(tx)+6,int(ty),64,GROUND-11,(255,236,150))]; s['shake']=rshake(1)
        if 174<=f<186: s['fx'].append(('term_hole',int(tk['x'])-1,GROUND-11,f-174))
    if 186<=f<230:
        fr=ease((f-190)/14); tk.update(spr=BLADES[9],x=146-4*fr,pal=tpal(frost=fr))
        if f==188:
            tx,ty=tip(gun); s['fx']+=[('term_muzzle',int(tx),int(ty)),('term_line',int(tx)+6,int(ty),172,40,(255,236,150)),('spark',172,40,4)]
        if 188<=f<212: s['fx'].append(('term_ln2',f-188,1.0 if f<204 else (212-f)/8))
        if f>=192: s['fx'].append(('term_frost',int(tk['x']),fr))
        if 204<=f<230: s['fx'].append(('big',"HASTA LA VISTA",4,RED))
        if 216<=f<230: s['fx'].append(('big',"BABY.",18,RED))
    # 5) one shot: he shatters into ice (230-248), melts into silver (246-262), flows and re-forms (262-280)
    if f>=230:
        tk['vis']=False
        if 230<=f<246: cl.update(spr=T8D['charge'],x=30-(2 if f-230 in (0,1) else 0)); gun=gun_at('charge',cl['x'],-0.45*math.sin(math.pi*(f-234)/6) if 234<=f<240 else 0.0)
        elif f<258: cl.update(spr=T8D[guard_pose(f)])
        if f==230:
            tx,ty=tip(gun); s['fx']+=[('term_muzzle',int(tx),int(ty)),('term_line',int(tx)+6,int(ty),SHATTER_X-8,49,(255,236,150))]
            s['flash']=0.45; s['fc']=(SHATTER_X,48); s['flashc']=FROST; s['shake']=rshake(2)
        if 246<=f<258:   # a fresh pair of shades from the jacket to the face
            ox,oy=origin(CL[guard_pose(f)],30); u=ease((f-246)/10)
            s['fx'].append(('term_shades',lerp(ox+13,ox+8,u),lerp(oy+6,oy+2+(f//6)%2,u),0))
        for i,sh in enumerate(SHARDS):
            u=f-230
            if u<20: x,y=sh['path'][min(u,19)]
            else: x,y=sh['path'][19]
            melt=ease((f-244-(i%5))/8)
            c=_mix(sh['c'],SILVER,melt)
            flow=ease((f-252-(i%7))/10)
            x=lerp(x,150+(i%9)-4,flow)
            if f<262+(i%6) and melt<0.5: s['fx'].append(('term_shard',x,y,sh['sz'],c))
            elif f<264+(i%6): s['fx'].append(('term_drop',x,GROUND-1,1,c))
        if 258<=f<282:   # the puddle gathers and he rises out of it, chrome turning back to uniform
            w=int(lerp(3,9,(f-258)/6)) if f<268 else int(lerp(9,0,(f-268)/12))
            if w>0: s['fx'].append(('term_drop',150,GROUND-1,w,SILVER))
        if 264<=f:
            prog=ease((f-264)/12); spr=T1K['idle']; h=len(spr); cut=int(h*(1-prog))
            rows=[r if i>=cut else '.'*len(r) for i,r in enumerate(spr)]
            tk.update(vis=True,x=150,spr=S(rows),pal=tpal(chrome=1-ease((f-274)/8)))
    if f>=258: cl.update(spr=T8[guard_pose(f)],x=30)
    if 262<=f<290: s['fx'].append(('term_say',"I'LL BE BACK.",6,RED))
    # the damaged half-face glows red
    if 86<=f<258:
        e=eye_of(cl['spr'],cl['x'])
        if e: s['fx'].append(('term_eye',e[0],e[1],0.75+0.25*math.sin(f*0.5)))
    if gun: s['fx'].insert(0,gun)
    s['actors']=[tk,cl]
    return s

CLIPS = [clip('judgment', N_, clip_judgment)]
