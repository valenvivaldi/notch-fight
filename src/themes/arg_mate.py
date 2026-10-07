"""Argentina sub-theme "arg-mate": no fight, a ronda de mate in a patio. Claude on a stool with the mate
and the termo, three friends round the table with a plate of facturas, the parra overhead, the flag with
the Sol de Mayo on the wall. He ceba the first mate and spits it out (EL PRIMERO ES DEL CEBADOR); the
mate goes round, friend by friend, each one finishing it with the bombilla's rattle (RRRP). Close-up:
the yerba from above, the water from the termo, the foam — until it is pale: ESTA LAVADO; he pours in
fresh yerba. One friend hands it back with a GRACIAS; the golden hour comes and goes."""
from engine import *
from themes.arg import PLAYER, CELESTE, WHITE                       # same country: the generic people

THEME = 'arg-mate'
N_ = 360                                                            # a multiple of 12 (the guard pose), 60 (the flag) and 15 (the steam)
CX = 30                                                             # Claude on his stool
FRIENDS = [(78,{'j':(200,70,60),'J':(200,70,60),'s':(226,184,150),'h':(60,40,30),'p':(60,80,140),'k':(40,30,26)}),
           (118,{'j':(70,140,90),'J':(70,140,90),'s':(196,140,104),'h':(30,24,22),'p':(50,50,60),'k':(40,30,26)}),
           (158,{'j':(240,200,80),'J':(240,200,80),'s':(230,190,160),'h':(150,90,40),'p':(70,90,150),'k':(40,30,26)})]
GOURD, GOURD_D, YERBA, BOMBILLA = (130,84,40), (90,56,26), (96,150,60), (210,214,222)
TERMO, TERMO_D = (60,120,72), (40,84,50)
GOLD = (246,190,50)

# ---- background: a patio under the parra -----------------------------------------------------------
def _patio(d):
    d.rectangle([0,0,W,H],fill=(236,226,204))                       # the whitewashed wall
    for y in range(0,46,7): d.line([0,y,W,y],fill=(226,214,190))
    d.rectangle([96,14,124,46],fill=(60,110,80)); d.rectangle([98,16,122,44],fill=(70,126,92))   # the door, with its persiana
    for y in range(18,44,3): d.line([99,y,121,y],fill=(56,100,72))
    d.point((120,32),fill=(200,180,100))
    d.rectangle([140,22,156,24],fill=(120,84,54))                    # a shelf and the radio
    d.rectangle([142,16,154,22],fill=(150,60,50)); d.ellipse([144,17,148,21],fill=(60,40,36)); d.line([150,17,153,17],fill=(220,210,190))
    for x0 in (60,170):                                             # malvones in pots
        d.polygon([(x0-4,46),(x0+4,46),(x0+3,52),(x0-3,52)],fill=(180,90,60))
        for dx,dy in ((-3,-3),(0,-5),(3,-3),(-1,-1),(2,-1)): d.ellipse([x0+dx-2,46+dy-2,x0+dx+1,46+dy+1],fill=(60,130,60))
        for dx,dy in ((-2,-5),(2,-6),(0,-3)): d.point((x0+dx,46+dy),fill=(230,40,60))
    for x in range(0,W,24): d.line([x,0,x+4,10],fill=(120,84,54))   # the parra: beams, leaves, grapes
    d.line([0,1,W,1],fill=(120,84,54),width=2)
    rr=random.Random(1816)
    for _ in range(70):
        x=rr.randint(-4,W+4); y=rr.randint(0,9); r=rr.randint(2,4)
        d.ellipse([x-r,y-r,x+r,y+r],fill=rr.choice([(70,130,50),(90,150,60),(60,110,44)]))
    for x in (30,88,140):
        for k in range(5): d.point((x+(k%2),11+k),fill=(110,50,110)); d.point((x+1-(k%2),11+k),fill=(140,70,140))
    d.rectangle([0,46,W,H],fill=(176,80,60))                         # the tiles
    for y in range(46,H,5):
        for x in range((y//5)%2*6,W,12): d.rectangle([x,y,x+5,y+4],fill=(196,96,70))
register_bg(THEME, lambda v: (v+120,v+60,v+40), decor=_patio)

# ---- effects ----------------------------------------------------------------------------------------
@fx('mate_flag')
def _fx_flag(d,im,e,f):
    """The flag on the wall, waving: celeste, white with the Sol de Mayo, celeste."""
    x0,y0,w,h=10,14,30,18
    d.line([x0-1,y0-2,x0-1,y0+h+4],fill=(120,100,80))
    for x in range(w):
        dy=int(round(1.5*math.sin(2*math.pi*(f/60)-x*0.35)*(x/w)))
        for y in range(h):
            c=CELESTE if y<h//3 or y>=2*h//3 else WHITE
            d.point((x0+x,y0+y+dy),fill=c)
    sx,sy=x0+w//2,y0+h//2+int(round(1.5*math.sin(2*math.pi*(f/60)-(w//2)*0.35)*0.5))
    for k in range(8): a=k*math.pi/4; d.line([sx,sy,sx+math.cos(a)*3,sy+math.sin(a)*3],fill=GOLD)
    d.ellipse([sx-1,sy-1,sx+1,sy+1],fill=GOLD); d.point((sx,sy),fill=(200,140,30))

def gourd(d,x,y):
    """The mate: a little gourd, the yerba at its mouth, the silver bombilla."""
    x,y=int(x),int(y)
    d.ellipse([x-3,y-4,x+3,y+2],fill=GOURD,outline=GOURD_D); d.line([x-2,y-2,x+2,y-2],fill=GOURD_D)
    d.line([x-2,y-4,x+2,y-4],fill=YERBA); d.line([x+1,y-3,x+3,y-8],fill=BOMBILLA)

@fx('mate_gourd')
def _fx_gourd(d,im,e,f):
    _,x,y=e; gourd(d,x,y)

@fx('mate_termo')
def _fx_termo(d,im,e,f):
    """The termo: upright under his arm, or tilted over the mate pouring (pour 0..1)."""
    _,x,y,pour=e; x,y=int(x),int(y)
    if pour<=0:
        d.rectangle([x-2,y-11,x+2,y],fill=TERMO,outline=TERMO_D); d.rectangle([x-2,y-13,x+2,y-11],fill=(190,194,200))
        d.line([x-1,y-9,x-1,y-2],fill=(90,160,100)); return
    a=-0.9*pour                                                      # tipped over towards the mate
    pts=[(x+math.cos(a)*u-math.sin(a)*v,y+math.sin(a)*u+math.cos(a)*v) for u,v in ((-12,-2),(0,-2),(0,2),(-12,2))]
    d.polygon(pts,fill=TERMO,outline=TERMO_D)
    if pour>=1:                                                      # the water, and the steam off it
        d.line([x+1,y,x+1,y+6],fill=(200,230,250))
        for k in range(2): ph=(f+k*6)%12; d.point((x+2+k,y-ph//2),fill=(236,236,240))

@fx('mate_stool')
def _fx_stool(d,im,e,f):
    _,x=e; d.rectangle([x-7,GROUND-6,x+7,GROUND-5],fill=(120,84,54))
    for lx in (x-6,x+6): d.line([lx,GROUND-5,lx,GROUND],fill=(100,70,44))

@fx('mate_table')
def _fx_table(d,im,e,f):
    """The little table with the plate of facturas (left: how many are left)."""
    _,left=e; x=98
    d.rectangle([x-12,GROUND-8,x+12,GROUND-7],fill=(120,84,54)); d.line([x-10,GROUND-7,x-10,GROUND],fill=(100,70,44)); d.line([x+10,GROUND-7,x+10,GROUND],fill=(100,70,44))
    d.ellipse([x-9,GROUND-11,x+9,GROUND-7],fill=(240,240,236),outline=(200,200,196))
    for i in range(left):
        fx_=x-6+i*4
        if i%2==0: d.arc([fx_-2,GROUND-12,fx_+2,GROUND-8],180,360,fill=(220,160,70),width=2)   # medialunas
        else: d.ellipse([fx_-2,GROUND-12,fx_+1,GROUND-9],fill=(230,190,120)); d.point((fx_,GROUND-11),fill=(150,80,40))   # bolas de fraile

@fx('mate_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(250,250,250),ink=(40,30,30))                     # the engine's bubble (engine/people.py)

@fx('mate_warm')
def _fx_warm(d,im,e,f):
    """The golden hour washing over the patio (a 0..1)."""
    _,a=e
    if a>0: im.paste(Image.blend(im,Image.new('RGB',im.size,(255,170,80)),0.28*a))

# ---- close-up ---------------------------------------------------------------------------------------
def closeup_yerba(t,f):
    """Primer plano: the mate from above: the water from the termo, the foam — then pale: ESTA LAVADO —
    and fresh yerba poured in from the packet."""
    im=Image.new('RGB',(W,H),(176,80,60)); d=ImageDraw.Draw(im)
    for y in range(0,H,8):
        for x in range((y//8)%2*12,W,24): d.rectangle([x,y,x+11,y+7],fill=(196,96,70))
    cx,cy=70,34
    d.ellipse([cx-30,cy-28,cx+30,cy+28],fill=GOURD,outline=GOURD_D,width=3)
    pale=min(1,max(0,(t-0.3)/0.15)) if t<0.62 else max(0,1-(t-0.62)/0.1)
    base=tuple(int(lerp(c,p,pale)) for c,p in zip(YERBA,(190,190,130)))
    d.ellipse([cx-25,cy-23,cx+25,cy+23],fill=base)
    rr=random.Random(5)
    for _ in range(160):
        a=rr.uniform(0,6.283); r=rr.uniform(0,23)
        d.point((cx+math.cos(a)*r,cy+math.sin(a)*r*0.92),fill=tuple(max(0,v-30) for v in base) if rr.random()<0.5 else tuple(min(255,v+20) for v in base))
    if t<0.3:                                                        # the water, the foam building up
        d.line([cx+14,0,cx+14,cy-4],fill=(210,236,250),width=3)
        k=t/0.3
        for i in range(int(30*k)):
            a=rr.uniform(0,6.283); r=rr.uniform(0,10*k+2)
            d.point((cx+14+math.cos(a)*r,cy-4+math.sin(a)*r),fill=(230,240,200))
        for j in range(3): ph=(f+j*5)%15; d.point((cx+12+j*3,cy-10-ph),fill=(236,236,240))
    d.line([cx-6,cy+6,cx+40,cy-40],fill=BOMBILLA,width=3); d.line([cx-6,cy+6,cx+40,cy-40],fill=(240,242,246),width=1)
    if 0.38<=t<0.62: big_text(im,"ESTA LAVADO",24,(255,255,255),scale=2,cx=136,outline=(60,40,20))
    if t>=0.62:                                                      # fresh yerba from the packet
        d.polygon([(118,0),(150,0),(146,18),(114,14)],fill=(240,200,40),outline=(160,110,20))
        text(d,"YERBA",120,4,(200,40,40),shadow=None)
        if t<0.78:
            for i in range(14): d.point((cx+20+rr.randint(-8,8),rr.randint(12,cy)),fill=(96,150,60))
    if t<0.05: zoom_lines(d)
    if t>0.92: im=fade_to(im,(0,0,0),0.5*(t-0.92)/0.08)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
HAND=(13,4)                                                          # Claude's front hand (guard pose)
SEAT=GROUND-5                                                        # his feet, up on the stool
def friend_hand(i,pose='idle'):
    x,_=FRIENDS[i]; return hand_at(PLAYER[pose],x,GROUND,True,10,7)
ROUND=[(70,0),(102,1),(134,2)]                                       # (frame the mate leaves Claude, friend)
def clip_ronda(f):
    s=scene(f,THEME)
    s['under'].append(('mate_flag',))
    pose=guard_pose(f)
    hx,hy=hand_at(CL[pose],CX,SEAT,False,*HAND)
    mate=(hx+1,hy); termo=(CX-9,SEAT,0.0); fposes=['idle']*3; left=5
    # 1) the first one: he cebas it and spits it out
    if 14<=f<30: termo=(hx+4,hy-6,min(1,(f-14)/4))
    if 30<=f<44: mate=(hx+1,hy-3)                                    # to his mouth
    if 40<=f<46: s['fx'].append(('spark',hx+8,hy-2,2))                # ptuh
    if 16<=f<70: s['fx'].append(('mate_bubble',["EL PRIMERO","ES DEL CEBADOR"],CX+10,14))
    # 2) the ronda: ceba, pass, the friend finishes it (RRRP), back
    for t0,i in ROUND+[(234,2)]:
        fx_,fy=friend_hand(i,'attack')
        if t0-12<=f<t0-4: termo=(hx+4,hy-6,1.0)
        if t0<=f<t0+8: p=(f-t0)/8; mate=(lerp(hx,fx_,p),lerp(hy,fy,p)-6*math.sin(p*math.pi)); fposes[i]='attack'
        if t0+8<=f<t0+22: mate=(fx_+2,fy-4); fposes[i]='idle'
        if t0+16<=f<t0+22 and t0!=234: s['fx'].append(('dmg',"RRRP",fx_-6,fy-14,(255,255,255)))
        if t0+22<=f<t0+28 and t0!=234: p=(f-t0-22)/6; mate=(lerp(fx_,hx,p),lerp(fy,hy,p)-6*math.sin(p*math.pi))
    if 110<=f<146: left=4
    if 146<=f<336: left=3
    if 336<=f<342: s['fx'].append(('twinkle',98,GROUND-12,2))           # somebody brought more
    # 3) close-up: the yerba, lavado, renewed
    if 166<=f<226: s['image']=closeup_yerba((f-166)/60,f); return s
    # 4) GRACIAS: the third friend hands it back for good
    if 256<=f<296:
        fx_,fy=friend_hand(2,'attack'); p=min(1,(f-256)/8); mate=(lerp(fx_,hx,p),lerp(fy,hy,p)-6*math.sin(p*math.pi))
        s['fx'].append(('mate_bubble',"GRACIAS",FRIENDS[2][0],18))
    # 5) one more for himself; the golden hour comes and goes
    if 300<=f<330: termo=(hx+4,hy-6,1.0) if f<310 else (CX-9,SEAT,0.0); mate=(hx+1,hy-3) if f>=312 else mate
    if 314<=f<336: s['fx'].append(('mate_bubble',"AAAH",CX+8,24))
    if 240<=f<350: s['fx'].append(('mate_warm',min(1,(f-240)/30) if f<320 else max(0,1-(f-320)/30)))
    s['under'].append(('mate_table',left))
    s['under'].append(('mate_termo',)+tuple(termo))
    acts=[actor(PLAYER[fposes[i]],x,flip=True,pal=pal) for i,(x,pal) in enumerate(FRIENDS)]
    s['under'].append(('mate_stool',CX))
    acts.append(actor(CL[pose],CX,SEAT))
    s['actors']=acts
    s['fx'].append(('mate_gourd',)+tuple(mate))
    return s

CLIPS = [clip('ronda', N_, clip_ronda)]
