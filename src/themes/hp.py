"""Harry Potter: Claude as Harry (the round glasses, the scar, the Gryffindor scarf, his wand) in the
graveyard at Little Hangleton by night: the leaning headstones, the yew, the statue of Death with its
scythe, the mist on the ground. Clip `priori`: Voldemort rises out of the mist (pale, no nose, the black
robes, the yew wand). EXPELLIARMUS against AVADA KEDAVRA: the red beam and the green meet and lock,
the bead of light sliding between them. Close-up: the golden cage of Priori Incantatem, the threads of
light humming round them, and the shadows of the dead coming out of the wand. Harry pushes the bead home,
breaks the link and runs for the cup — the Portkey — and he's gone; the mist closes over Voldemort."""
from engine import *

THEME = 'hp'
N_ = 432                                                            # a multiple of 12 and of 48 (the mist)
HX, VX = 40, 146
INK = (10,10,16)
RED, GREEN, GOLD = (255,60,50), (80,255,110), (255,214,90)

# ---- people, built from a pose --------------------------------------------------------------------------
GW, GH, C = 24, 24, 11
POSES = {   # (back elbow, back hand, front elbow, front hand, lean, legs), from (C, shoulder row)
 'stand': ((-1,3),(-1,6),(3,3),(5,4),0,'stand'),
 'cast':  ((-2,3),(-3,5),(5,1),(9,0),1,'stance'),
 'strain':((-2,3),(-4,4),(5,1),(9,1),-1,'stance'),
 'run1':  ((-3,2),(-5,4),(3,3),(6,2),1,'stance'),
 'run2':  ((-1,3),(1,5),(3,3),(2,5),1,'stand'),
 'reach': ((-1,3),(-1,6),(5,0),(9,-1),1,'lunge'),
}
L_, T_ = 9, 7
HIP=GH-L_; TY=HIP-T_; HY=TY-5
_put, _seg = put, seg                                               # the engine's (engine/people.py)

_built={}
def build(who,pose):
    key=(who,pose)
    if key in _built: return _built[key]
    g=[['.']*GW for _ in range(GH)]
    be,bh,fe,fh,lean,legs=POSES[pose]
    spread={'stand':(-1,1),'stance':(-3,3),'lunge':(-5,5)}[legs]
    robe=who=='voldemort'
    for k,dx in enumerate(spread):
        for t in range(L_):
            x=C+round(dx*t/(L_-1))+(k*2-1); _put(g,x,HIP+t,'k' if t==L_-1 else 'p'); _put(g,x+1,HIP+t,'k' if t==L_-1 else 'p')
    if robe:                                                         # the robes, sweeping to the ground
        for t in range(L_-1):
            w=3+t//2
            for x in range(C-w,C+w+1): _put(g,x,HIP+t,'j' if (x+t)%5 else 'J')
    sh=lambda y: round(lean*(HIP-y)/(HIP-HY))
    def arm(e,h,front):
        sx,sy=C+(2 if front else -2)+sh(TY+1),TY+1
        ex,ey=C+e[0]+sh(TY),TY+e[1]; hx,hy=C+h[0]+sh(TY),TY+h[1]
        _seg(g,sx,sy,ex,ey,'j' if front else 'J'); _seg(g,ex,ey,hx,hy,'j' if front else 'J'); _put(g,hx,hy,'s')
    arm(be,bh,False)
    for y in range(TY,HIP+1):
        o=sh(y)
        for x in range(C-3+o,C+3+o): _put(g,x,y,'j')
        if not robe and y<TY+3:                                      # the scarf: red and gold
            for x in range(C-2+o,C+2+o): _put(g,x,y,'r' if (x+y)%2 else 'y')
        if not robe and y==TY+3: _put(g,C+1+o,y,'r'); _put(g,C+1+o,y+1,'y')   # its end hanging
    o=sh(HY)
    for y in range(HY,HY+5):
        for x in range(C-2+o,C+3+o): _put(g,x,y,'s')
    if robe:                                                         # no hair, the slit nose, red eyes
        for x in range(C-2+o,C+3+o): _put(g,x,HY-1,'s')
        _put(g,C+o,HY+2,'e'); _put(g,C+2+o,HY+2,'e'); _put(g,C+1+o,HY+3,'n')
    else:
        for x in range(C-1+o,C+3+o): _put(g,x,HY+2,'G')              # the round glasses
        _put(g,C+o,HY+2,'K'); _put(g,C+2+o,HY+2,'K'); _put(g,C-1+o,HY+1,'z')   # the scar
        for i,row in enumerate(["..h.h.h",".hhhhhh","hhhhhhh","hhh.h.."]):
            for j,ch in enumerate(row):
                if ch!='.': _put(g,C-3+o+j,HY-2+i,ch)
    arm(fe,fh,True)
    _built[key]=S([''.join(r) for r in g]); return _built[key]

HPAL = {'s':(236,200,170),'K':INK,'G':(40,40,44),'z':(200,60,60),'h':(30,24,24),'j':(36,34,44),'J':(26,24,32),
        'r':(170,30,36),'y':(230,180,50),'p':(60,60,70),'k':(24,20,20)}
VPAL = {'s':(226,232,226),'e':(220,30,30),'n':(150,160,150),'j':(18,16,22),'J':(34,30,40),'p':(18,16,22),'k':(10,10,12)}

def wand_tip(x,feet,pose,flip=False):
    _,_,_,h,lean,_=POSES[pose]; o=round(lean*(HIP-TY)/(HIP-HY))
    hx=C+h[0]+o+3; hy=TY+h[1]-1
    return (x-GW//2+(GW-1-hx) if flip else x-GW//2+hx), feet-GH+hy

# ---- the graveyard --------------------------------------------------------------------------------------
def _graveyard(d):
    for y in range(H): k=y/H; d.line([0,y,W,y],fill=(int(lerp(10,26,k)),int(lerp(14,30,k)),int(lerp(30,38,k))))
    rr=random.Random(39)
    for _ in range(40): d.point((rr.randint(0,W-1),rr.randint(0,24)),fill=(180,190,220))
    d.ellipse([150,3,164,17],fill=(220,224,210)); d.ellipse([154,3,168,15],fill=(14,18,34))   # a thin moon
    d.polygon([(0,40),(20,30),(46,36),(70,26),(100,34),(130,28),(160,36),(185,30),(185,46),(0,46)],fill=(22,26,30))   # the hill
    x=92                                                             # the statue of Death, with its scythe
    d.polygon([(x-6,GROUND-2),(x-4,22),(x,16),(x+4,22),(x+6,GROUND-2)],fill=(70,74,80)); d.ellipse([x-3,14,x+3,22],fill=(60,64,70))
    d.line([x+4,24,x+10,6],fill=(80,84,90)); d.arc([x+2,2,x+20,14],180,300,fill=(110,114,120),width=2)
    d.rectangle([x-9,GROUND-3,x+9,GROUND],fill=(80,84,88))
    d.line([20,GROUND,24,20],fill=(30,26,24),width=3)                 # the old yew
    for k in range(8): a=k*0.8; d.line([24,22,24+math.cos(a)*12,20+math.sin(a)*6],fill=(30,40,30),width=2)
    for x,h,tilt in ((10,10,-1),(60,8,1),(118,12,0),(172,9,-1),(132,7,1),(74,6,0)):   # leaning headstones
        d.polygon([(x-3,GROUND),(x-3+tilt,GROUND-h),(x+3+tilt,GROUND-h),(x+3,GROUND)],fill=(96,100,104),outline=(56,58,62))
        d.pieslice([x-3+tilt,GROUND-h-3,x+3+tilt,GROUND-h+3],180,360,fill=(96,100,104))
    d.rectangle([0,GROUND,W,H],fill=(26,32,26))
    for _ in range(50): d.point((rr.randint(0,W-1),rr.randint(GROUND,H-1)),fill=(40,50,36))
register_bg(THEME, lambda v: (v+20,v+26,v+20), decor=_graveyard)

@fx('hp_mist')
def _fx_mist(d,im,e,f):
    """Mist along the ground, drifting (a loop every 48 frames); thick: how much."""
    _,thick=e; m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for i in range(10):
        x=(i*24+(f%48)*24/48)%(W+40)-20; y=GROUND-2+(i%3)
        md.ellipse([x-20,y-4-thick*6,x+20,y+5],fill=int(70+60*thick))
    im.paste((150,160,170),(0,0),m.filter(ImageFilter.GaussianBlur(3)))

@fx('hp_beam')
def _fx_beam(d,im,e,f):
    """A spell's beam from (x0,y0) to (x1,y1), wavering, with its glow."""
    _,x0,y0,x1,y1,c,w=e
    g=Image.new('L',(W,H),0); gd=ImageDraw.Draw(g)
    n=12; pts=[(lerp(x0,x1,i/n),lerp(y0,y1,i/n)+(math.sin(f*0.9+i*1.3)*1.2 if 0<i<n else 0)) for i in range(n+1)]
    gd.line(pts,fill=160,width=w+4); im.paste(c,(0,0),g.filter(ImageFilter.GaussianBlur(2)))
    d=ImageDraw.Draw(im); d.line(pts,fill=c,width=w); d.line(pts,fill=(255,255,255),width=1)

@fx('hp_bead')
def _fx_bead(d,im,e,f):
    """Where the two meet: the bead of light, the sparks."""
    _,x,y=e; r=3+(f%4)//2
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-r-4,y-r-4,x+r+4,y+r+4],fill=200)
    im.paste(GOLD,(0,0),g.filter(ImageFilter.GaussianBlur(3)))
    d=ImageDraw.Draw(im); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,250,220))
    rr=random.Random(f)
    for _ in range(5): a=rr.uniform(0,2*math.pi); L=rr.uniform(3,8); d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=GOLD)

@fx('hp_cage')
def _fx_cage(d,im,e,f):
    """The golden dome over the two of them (a: how far it has risen)."""
    _,a=e
    if a<=0: return
    cx=(HX+VX)/2; rx=(VX-HX)/2+14; top=GROUND-40*a
    for k in range(9):
        t=k/8; x=lerp(cx-rx,cx+rx,t); ph=math.sin(f*0.3+k)*2
        d.arc([cx-rx*abs(1-2*t)-1,top+ph,cx+rx*abs(1-2*t)+1,GROUND*2-top],180,360,fill=(220,180,70))
    d.arc([cx-rx,top,cx+rx,GROUND*2-top],180,360,fill=GOLD,width=2)

@fx('hp_cup')
def _fx_cup(d,im,e,f):
    """The Triwizard Cup — the Portkey — glinting on the grass."""
    _,x,glow=e; y=GROUND
    d.polygon([(x-4,y-9),(x+4,y-9),(x+2,y-4),(x-2,y-4)],fill=(150,200,230),outline=(90,130,160))
    d.rectangle([x-1,y-4,x+1,y-2],fill=(150,200,230)); d.rectangle([x-3,y-2,x+3,y],fill=(150,200,230),outline=(90,130,160))
    for s in (-1,1): d.arc([x+s*4-3,y-9,x+s*4+3,y-4],90 if s>0 else 270,270 if s>0 else 90,fill=(150,200,230))
    if glow>0 and (f//2)%2: d.ellipse([x-8,y-14,x+8,y+2],outline=(200,240,255))

@fx('hp_text')
def _fx_text(d,im,e,f):
    _,txt,cx,y,c=e; big_text(im,txt,y,c,scale=1,cx=cx,shadow=INK)

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_priori(t,f):
    """Primer plano: inside the golden cage, the threads of light humming, the beam between the wands —
    and the shades of the dead coming out of Voldemort's wand, grey and see-through."""
    im=Image.new('RGB',(W,H),(14,12,6)); d=ImageDraw.Draw(im)
    for k in range(14):                                              # the cage's threads, arching over
        a=k/13; ph=math.sin(f*0.25+k)*3
        d.arc([-20+a*40,-30+ph,W+20-a*40,H+70],180,360,fill=(int(150+100*a),int(110+80*a),40))
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([20,10,165,90],fill=60); im.paste(GOLD,(0,0),g.filter(ImageFilter.GaussianBlur(14)))
    d=ImageDraw.Draw(im)
    d.line([0,44,W,44],fill=GOLD,width=3); d.line([0,44,W,44],fill=(255,255,240))   # the link between them
    d.ellipse([86,39,98,49],fill=(255,250,220))
    for k,(sx,start) in enumerate(((150,0.1),(118,0.35),(84,0.6))):  # the shades, one after another
        a=max(0,min(1,(t-start)/0.25))
        if a<=0: continue
        x=lerp(176,sx-40,a); m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
        md.ellipse([x-6,12,x+6,26],fill=150); md.polygon([(x-8,26),(x+8,26),(x+10,H),(x-10,H)],fill=110)
        im.paste((200,210,220),(0,0),m.filter(ImageFilter.GaussianBlur(1)))
    d=ImageDraw.Draw(im)
    d.rectangle([168,40,W,48],fill=(60,40,30)); d.rectangle([0,40,18,48],fill=(120,80,50))   # the two wands
    if t>=0.2: big_text(im,"PRIORI INCANTATEM",2,GOLD,scale=2,shadow=INK)
    if t<0.05: zoom_lines(d,GOLD)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
def clip_priori(f):
    s=scene(f,THEME)
    if 180<=f<250: s['image']=closeup_priori((f-180)/70,f); return s
    hpose,vpose,vvis,valpha='stand','stand',False,1.0
    hx=HX; thick=0.3; cage=0.0; hvis=True
    # Voldemort rises out of the mist
    if 14<=f<396:
        vvis=True; valpha=min(1,(f-14)/30) if f<44 else 1.0
    if 14<=f<50: thick=0.3+0.7*math.sin(min(1,(f-14)/36)*math.pi)
    # the duel: the two spells, the lock, the bead going back and forth
    if 56<=f<304:
        hpose='cast' if f<100 else 'strain'; vpose='cast'
    if 56<=f<92:
        s['fx'].append(('hp_text',"EXPELLIARMUS!",HX+24,10,RED)); s['fx'].append(('hp_text',"AVADA KEDAVRA!",VX-24,18,GREEN))
    if 64<=f<304:
        x0,y0=wand_tip(HX,GROUND,hpose); x1,y1=wand_tip(VX,GROUND,vpose,True)
        if f<76: t=(f-64)/12; mx=lerp(x0,(x0+x1)/2,t); my=lerp(y0,(y0+y1)/2,t); mx2=lerp(x1,(x0+x1)/2,t)
        else:
            mid=(x0+x1)/2+[-0,-8,6,-4,10,18,26][min(6,(f-76)//18)]*(1 if f<260 else 1)+3*math.sin(f*0.4)
            if f>=262: mid=lerp(mid,x1-4,(f-262)/24)                     # Harry pushes it home
            mx=mx2=mid; my=(y0+y1)/2
        s['fx'].append(('hp_beam',x0,y0,mx,my,RED,2)); s['fx'].append(('hp_beam',x1,y1,mx2,my,GREEN,2))
        if f>=76: s['fx'].append(('hp_bead',mx,my)); s['shake']=rshake(1) if f%9==0 else (0,0)
    if 120<=f<304: cage=min(1,(f-120)/40)
    if 284<=f<304: cage=max(0,cage-(f-284)/20)
    # the link breaks; he runs for the cup and is gone
    if 304<=f<312: s['flash']=1-(f-304)/8; s['fc']=(VX-10,GROUND-14); vpose='stand'
    if 304<=f<340: t=(f-304)/36; hx=lerp(HX,24,t); hpose='run1' if (f//4)%2 else 'run2'
    if 300<=f<346: s['under'].append(('hp_cup',16,1 if f>=330 else 0))
    if 340<=f<346: hvis=False; s['flash']=1-(f-340)/6; s['fc']=(16,GROUND-6); s['flashc']=(200,240,255)
    if 346<=f<390: hvis=False; thick=0.3+0.7*math.sin(min(1,(f-346)/44)*math.pi); vpose='stand'
    if 360<=f<390: valpha=max(0,1-(f-360)/30)
    s['under'].append(('hp_cage',cage))
    acts=[]
    if vvis: acts.append(actor(build('voldemort',vpose),VX,flip=True,pal=VPAL,alpha=valpha))
    if hvis: acts.append(actor(build('harry',hpose),hx,pal=HPAL))
    s['actors']=acts
    if hvis and hpose in ('stand','cast','strain'):                   # the wands
        x,y=wand_tip(hx,GROUND,hpose); s['fx'].append(('hp_wand',x-3,x,y,(120,80,50)))
    if vvis and valpha>0.5:
        x,y=wand_tip(VX,GROUND,vpose,True); s['fx'].append(('hp_wand',x,x+3,y,(200,190,170)))
    s['fx'].append(('hp_mist',thick))
    if 380<=f<396: s['image']=fade_to(render(s,f),(0,0,0),(f-380)/16)
    if 396<=f<420:                                                   # and back to the start
        s0=clip_priori(0); s['image']=fade_to(render(s0,f),(0,0,0),1-(f-396)/24)
    return s

@fx('hp_wand')
def _fx_wand(d,im,e,f):
    _,x0,x1,y,c=e; d.line([x0,y,x1,y],fill=c); d.point((x1,y),fill=(255,250,220))

CLIPS = [clip('priori', N_, clip_priori)]
