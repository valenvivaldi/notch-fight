"""Jujutsu Kaisen sub-theme "jjk-toji": Claude as Toji Fushiguro vs young Gojo (Hidden Inventory arc).
Gojo's Infinity stops every punch and the thrown knife dead in the air. Toji pulls the Inverted
Spear of Heaven out of the curse worm he wears; close-up: SORCERER KILLER. The spear shatters the
Infinity like glass, Toji stabs, Gojo goes down — and gets back up glowing blue."""
from engine import *

THEME = 'jjk-toji'
N_ = 264

BLUE, BLUE_HI = (90,150,255), (170,210,255)
# Toji: black spiky hair, black tight shirt, the scar at the corner of the mouth
TPAL = {'l':(44,44,54), 'f':(80,80,96), 'a':(48,48,60), 'i':(34,34,44), 'c':(236,200,180)}
# young Gojo: white hair, round dark glasses, navy Jujutsu High uniform
GPAL = {'b':(44,50,84), 'Z':(16,16,22), 'z':(90,96,120)}

HAIR = ["l.l.l.l.l...", ".llllllllll.", "lfllllllfll."]

def _toji(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    ks=[(x,y) for y,row in enumerate(g) for x,c in enumerate(row) if c=='K']
    if ks:
        x1=max(x for x,_ in ks); y1=max(y for _,y in ks)
        for dy in (1,2):                                               # the scar under the mouth corner
            if y1+dy<len(g) and g[y1+dy][x1] in 'Oo': g[y1+dy][x1]='c'
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
    return S([''.join(x) for x in g])
TOJI=variant(_toji)

GOJO_H=poses(S([
"....H.H.H.H.....","...HHHHHHHHH....","...HHHHHHHHH....","...HPPPPPPPH....","...PZZzPZZz.....",
"...PPPPPPPP.....","....PPkkPP......",".....PPPP.......","...bbbbbbbb.....","..bbbbbbbbbb....",
"..bbbbzbbbbb....","..PbbbzbbbbP....","..P.bbzbbb.P....","....bbbbbb......","....bbbbbb......",
"....bbbbbb......","....bb..bb......","....bb..bb......","....bb..bb......","...kkk..kkk.....",]),11,'P',4)

def _temple(d):
    """Night at the temple: a dim torii gate, stone lanterns, a thin crescent."""
    for x0 in (74,106): d.rectangle([x0,16,x0+3,GROUND],fill=(70,18,20))
    d.rectangle([66,12,118,15],fill=(84,22,24)); d.rectangle([70,20,114,22],fill=(70,18,20))
    d.line([64,11,120,11],fill=(40,12,14))
    for x in (20,166):
        d.rectangle([x-2,GROUND-10,x+2,GROUND],fill=(40,40,48)); d.rectangle([x-4,GROUND-14,x+4,GROUND-10],fill=(52,52,62))
        d.rectangle([x-1,GROUND-13,x+1,GROUND-11],fill=(120,96,50))
    d.arc([150,3,160,13],100,260,fill=(200,200,180))
register_bg(THEME, lambda v: (v//2+2,v//2+2,v//2+12), decor=_temple)

@fx('tj_worm')
def _fx_worm(d,im,e,f):
    """Toji's Inventory curse wrapped round his waist like a sash, its head resting at his hip;
    mouth 0..1 opens its maw (the spear comes out)."""
    _,x,feet,mouth=e; y0=feet-5
    pts=[]
    for k in range(10):
        t=k/9; a=math.pi*(1+t)                                    # the lower half of a loop: sags in front
        pts.append((x-1+math.cos(a)*8,y0-math.sin(a)*2+math.sin(f*math.pi/12+k)*0.4))   # a 24-frame sway: it loops
    for i,(px,py) in enumerate(pts[:-1]):
        d.rectangle([px-1,py-1,px+1,py],fill=(150,120,164) if i%2 else (126,98,142))
    hx,hy=pts[-1]; op=int(3*mouth)
    d.ellipse([hx-1,hy-3,hx+3,hy+1],fill=(150,120,164),outline=(60,40,70))
    d.point((hx+1,hy-2),fill=(250,240,120))
    if op: d.rectangle([hx+2,hy-1,hx+4,hy-1+op],fill=(60,10,20)); d.point((hx+3,hy-1),fill=(240,230,220))

@fx('tj_spear')
def _fx_spear(d,im,e,f):
    """Inverted Spear of Heaven: dark haft, a ring at the butt, a forked silver blade."""
    _,hx,hy,a,L=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.ellipse([hx-c*6-1,hy-s*6-1,hx-c*6+1,hy-s*6+1],outline=(150,150,160))
    d.line([hx-c*5,hy-s*5,hx+c*(L-5),hy+s*(L-5)],fill=(90,56,60))
    tx,ty=hx+c*L,hy+s*L
    d.line([hx+c*(L-5),hy+s*(L-5),tx,ty],fill=(220,224,236)); d.point((tx,ty),fill=(255,255,255))
    d.line([hx+c*(L-4),hy+s*(L-4),hx+c*(L-2)-s*3,hy+s*(L-2)+c*3],fill=(200,204,220))   # the inverted prong

@fx('tj_knife')
def _fx_knife(d,im,e,f):
    _,x,y=e; d.line([x-3,y,x+2,y],fill=(210,214,226)); d.line([x-5,y,x-4,y],fill=(90,56,40))

@fx('tj_glass')
def _fx_glass(d,im,e,f):
    """The Infinity shattering: pale blue shards thrown off a sphere around (x,y)."""
    _,x,y,k=e; rr=random.Random(8123)
    for i in range(30):
        a=rr.random()*6.28; sp=rr.uniform(0.8,2.6); r=10+k*sp
        px,py=x+math.cos(a)*r,y+math.sin(a)*r*0.7+0.12*k*k
        if py<GROUND: d.line([px,py,px+rr.randint(-2,2),py+rr.randint(-2,2)],fill=BLUE_HI if i%3 else (255,255,255))

GRIP = {'guard':(13,4), 'guard2':(13,4), 'punch':(16,5), 'charge':(15,5), 'dash':(16,5)}
def hand_of(pose,x,y,flip=False):
    col,row=GRIP[pose]; return hand_at(TOJI[pose],x,y,flip,col,row,h=11)

def closeup_grin(t,f):
    """Primer plano: Toji's face, the scar pulling a grin, green eyes; SORCERER / KILLER."""
    im=Image.new('RGB',(W,H),(6,6,12)); d=ImageDraw.Draw(im)
    for i in range(0,64,4): d.line([0,i,96,i],fill=(12,12,22))
    O,o=(217,119,87),(168,80,54)
    d.rectangle([22,12,82,64],fill=O); d.rectangle([76,12,82,64],fill=o)
    hair=[(16,16)]+[(x,2 if (x//8)%2 else 10) for x in range(16,92,4)]+[(88,16)]
    d.polygon(hair,fill=TPAL['l']); d.rectangle([20,10,84,16],fill=TPAL['l'])
    for x in range(22,84,7): d.polygon([(x,16),(x+6,16),(x+2,23)],fill=TPAL['l'])
    for x0 in (32,56):
        d.rectangle([x0,28,x0+14,33],fill=(24,14,12)); d.rectangle([x0+4,29,x0+8,32],fill=(60,120,80))
        d.point((x0+5,29),fill=(200,255,210))
    d.line([31,26,46,28],fill=(60,30,20)); d.line([56,28,71,26],fill=(60,30,20))           # brows, down
    g=min(1,t*3)                                                                             # the grin widens
    d.polygon([(40,48),(66,48),(66-4*(1-g),52),(44+4*(1-g),51)],fill=(60,16,16))
    d.line([42,48,64,48],fill=(255,255,255))
    d.line([64,44,62,55],fill=TPAL['c']); d.line([65,44,63,55],fill=TPAL['c'])              # the scar across the lip
    for j,w in enumerate(("SORCERER","KILLER")):
        if t>=0.2+j*0.25: FX['big'](d,im,('big',w,14+j*18,(236,236,244) if j==0 else (255,80,80),138),f)
    if t<0.06: zoom_lines(d)
    return im

GX=150            # Gojo's spot
BARRIER=136       # where Infinity stops everything

def clip_sakahoko(f):
    s=scene(f,THEME)
    tx,ty,tflip,tpose=30,GROUND,False,guard_pose(f)
    gx,gpose,gaura=GX,'idle',None
    worm_mouth=0; spear=None                                     # spear: angle when Toji holds it
    # 1) Infinity
    if 14<=f<30: gpose='attack'
    if 16<=f<36: callout(s,"MUGEN",c=BLUE_HI)
    if 14<=f<158:
        for r in range(3): s['fx'].append(('circle',GX-4,GROUND-10,6+r*4+(f%3),BLUE if r%2 else BLUE_HI))
    # 2) punches stopped dead, the knife hangs in the air
    if 30<=f<38: tpose,tx='dash',ez(30,124,(f-30)/8)
    if 38<=f<62:
        tx=124; k=(f-38)%8; tpose='punch' if k<4 else 'guard'
        if k<3:
            s['fx'].append(('spark',BARRIER,GROUND-6-(f//8%3)*3,2+k))
            s['fx'].append(('dmg',"...",BARRIER-4,GROUND-26,BLUE_HI))
    if 62<=f<72: tpose,tx,tflip='dash',ez(124,70,(f-62)/10),True
    if 64<=f<104:                                                 # the knife, thrown on the way back
        p=min(1,(f-64)/5); kx=lerp(90,BARRIER-2,p); ky=GROUND-18
        if f>=69: kx=BARRIER-2+(1 if f%4<2 else 0)
        if f>=92: ky=min(GROUND-1,GROUND-18+(f-92)**2*0.4)
        s['fx'].append(('tj_knife',kx,ky))
    if f>=72: tx=70
    # 3) the spear comes out of the worm
    if 76<=f<96:
        tflip=False; worm_mouth=min(1,(f-76)/6) if f<90 else max(0,1-(f-90)/6)
        if f>=82: spear=-90+min(1,(f-82)/10)*60
    if 82<=f<112: callout(s,"INVERTED SPEAR OF HEAVEN",c=(236,200,180))
    # 4) close-up
    if 96<=f<140: s['image']=closeup_grin((f-96)/44,f); return s
    if 140<=f<150: tpose,spear='charge',-10
    if 150<=f<158: tpose,tx,spear='dash',ez(70,124,(f-150)/8),0
    # 5) the Infinity shatters; the stab
    if 158<=f<180:
        k=f-158; s['fx'].append(('tj_glass',GX-4,GROUND-10,k))
        if k<2: s['flash']=0.8; s['fc']=(BARRIER,GROUND-10); s['flashc']=(200,230,255)
        if k<6: s['shake']=rshake(2)
    if 158<=f<172: tpose,tx,spear='punch',128,0
    if 160<=f<174: gpose='hurt'; s['fx'].append(('spark',GX-6,GROUND-12,3+(f%3)))
    if 162<=f<176: callout(s,"SORCERER KILLER",c=(255,80,80))
    if 166<=f<206: gpose,gx='hurt',ez(GX,172,(f-166)/10)
    # 6) Toji walks back, the spear goes home; Gojo gets up, glowing
    if 172<=f<182: tpose,spear,tx='guard',-60,128
    if 182<=f<222: tpose,tx,tflip,spear=guard_pose(f),ez(128,30,(f-182)/40),True,-60
    if 222<=f<236:
        tx,tflip=30,False; worm_mouth=min(1,(f-222)/4) if f<230 else max(0,1-(f-230)/6)
        if f<228: spear=-90
    if f>=236: tx,tflip=30,False
    if 206<=f<256:
        gx=ez(172,GX,(f-230)/20) if f>=230 else 172
        if (f//4)%2 or f<230: gaura=(BLUE_HI,1)
    if 206<=f<222: s['fx'].append(('dmg',"...",170,GROUND-30,BLUE_HI))
    toji=actor(TOJI[tpose],tx,ty,flip=tflip,pal=TPAL)
    gojo=actor(GOJO_H[gpose],gx,flip=True,pal=GPAL,aura=gaura)
    s['actors']=[gojo,toji]
    s['fx'].append(('tj_worm',tx,ty,worm_mouth))
    if spear is not None and tpose in GRIP:
        hx,hy=hand_of(tpose,tx,ty,tflip)
        s['fx'].append(('tj_spear',hx,hy,(180-spear) if tflip else spear,16))
    return s

CLIPS = [clip('sakahoko', N_, clip_sakahoko)]
