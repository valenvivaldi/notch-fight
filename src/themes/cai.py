"""Independiente: Claude in the red shirt of the Rojo (blue shorts, the captain's armband) in the clasico de
Avellaneda against Racing, at the Libertadores de America under its double roof, the stands red and
white. Minute 90, 0-0: he takes the ball past three Racing defenders (OLE!) — a nutmeg, a lob over the
second, a feint that sits the third down. Close-up: the strike. It curls past the diving keeper into
the top corner: GOL DEL ROJO, red flares in the stands. Close-up: the trophy cabinet, the seven Copas
Libertadores lighting up one by one — REY DE COPAS. The ball comes back to the centre for the loop."""
from engine import *
from themes.arg import PLAYER, DIVE, draw_goal, CELESTE, WHITE      # the same pitch and players as arg

THEME = 'cai'
N_ = 377
CX = 40                                                             # the loop keyframe position
RED, RED_D, BLUE = (206,22,36), (140,12,24), (34,44,120)
HUD_BG, HUD_INK, GOLD = (16,16,22), (236,236,236), (236,190,60)
# Claude in the Rojo's shirt: red jersey, blue shorts, the captain's armband
RPAL = {'1':RED, '2':RED_D, '3':BLUE, 'y':(236,200,60)}
KIT_RAC  = {'j':CELESTE, 'J':WHITE, 's':(210,160,120), 'h':(40,30,26), 'p':(24,24,28)}
KIT_KEEP = {'j':(70,70,80), 'J':(70,70,80), 's':(226,184,150), 'h':(60,40,30), 'p':(40,40,48)}

def _rojo(spr):
    g=[list(r) for r in spr]
    top,l,r=body_box(spr); h=len(g)
    for y in range(top+4,min(top+9,h)):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='1' if y<top+8 else '3'
    for y in range(top+5,min(top+7,h)):                              # the captain's armband
        for x in range(len(g[0])):
            if g[y][x]=='o' and x<l: g[y][x]='y'; break
    return S([''.join(x) for x in g])
ROJO=variant(_rojo)

# ---- background: the Libertadores de America, the double roof -----------------------------------------
def _cancha(d):
    d.rectangle([0,0,W,28],fill=(14,14,22))
    d.polygon([(0,2),(W,0),(W,3),(0,5)],fill=(70,70,84))            # the double roof: two visors
    d.polygon([(0,7),(W,5),(W,8),(0,10)],fill=(60,60,74))
    for x in range(6,W,22): d.line([x,5,x,10],fill=(90,90,104))
    rr=random.Random(1905)
    for y in range(11,28,3):                                         # the stands: red and white
        for x in range(0,W,3):
            c=rr.choice((RED,RED,(236,236,236),RED_D,(60,40,44)))
            if rr.random()<0.75: d.point((x+(y//3)%2,y),fill=c)
    for x0 in (20,96,150):                                           # banners
        d.rectangle([x0,20,x0+20,25],fill=RED); d.rectangle([x0,22,x0+20,23],fill=(236,236,236))
    for x in range(0,W,16): d.rectangle([x,28,x+7,GROUND],fill=(46,110,52))
    for x in range(8,W,16): d.rectangle([x,28,x+7,GROUND],fill=(54,124,60))
    d.line([0,28,W,28],fill=(236,236,236))
    d.line([150,34,150,GROUND],fill=(220,230,220)); d.point((160,50),fill=(236,236,236))
    draw_goal(d,176,1)
register_bg(THEME, lambda v: (v//3,v+20,v//3), decor=_cancha)

@fx('cai_hud')
def _fx_hud(d,im,e,f):
    """The TV scoreboard: CAI 0-0 RAC, minute 90."""
    _,score=e
    d.rounded_rectangle([3,3,70,12],radius=2,fill=HUD_BG,outline=(90,90,110))
    d.rectangle([5,5,7,10],fill=RED)
    text(d,"CAI "+score+" RAC",10,5,HUD_INK,shadow=None)
    d.rectangle([60,4,69,11],fill=(40,40,56)); text(d,"90",61,5,GOLD,shadow=None)

@fx('cai_ball')
def _fx_ball(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.ellipse([x-2,y-2,x+1,y+1],fill=(250,250,250),outline=(40,40,40)); d.point((x-1,y-1),fill=(40,40,40))

@fx('cai_net')
def _fx_net(d,im,e,f):
    _,x,y,k=e
    if k<12: r=3+k//2; d.arc([x-r,y-r,x+r,y+r],-80,80,fill=(250,250,250))

@fx('cai_flares')
def _fx_flares(d,im,e,f):
    """Red flares in the stands and their smoke drifting over the pitch (a 0..1)."""
    _,a=e
    if a<=0: return
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); rr=random.Random(3)
    for i in range(14):
        x=rr.randint(0,W); y=rr.randint(8,30)-((f//2+i*5)%20); r=rr.randint(6,12)
        md.ellipse([x-r,y-r,x+r,y+r],fill=int(120*a))
    im.paste((220,60,60),(0,0),m.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    for i,x in enumerate((14,40,70,110,140,172)):
        if (f//2+i)%3: d.point((x,22+(i%2)*2),fill=(255,230,200)); d.point((x+1,21+(i%2)*2),fill=(255,90,60))

@fx('cai_confetti')
def _fx_confetti(d,im,e,f):
    _,k,dens=e; rr=random.Random(11)
    for i in range(int(60*dens)):
        x=(rr.uniform(0,W)+math.sin(k*0.1+i)*4)%W; y=(rr.uniform(-H,0)+k*rr.uniform(0.8,1.6))%(H+10)-5
        d.rectangle([x,y,x+1,y],fill=RED if i%2 else (240,240,240))

@fx('cai_big')
def _fx_big(d,im,e,f):
    _,txt,y,c=e; big_text(im,txt,y,c,shadow=(0,0,0),outline=(0,0,0))

# ---- close-ups --------------------------------------------------------------------------------------
def closeup_strike(t,f):
    """Primer plano: the red sock and the boot swinging through; the ball squashes and goes."""
    im=Image.new('RGB',(W,H),(46,110,52)); d=ImageDraw.Draw(im)
    for x in range(-64,W,16): d.polygon([(x,H),(x+8,H),(x+40,0),(x+32,0)],fill=(54,124,60))
    a=lerp(-1.4,0.5,ease(t/0.45))                                   # the leg swings from the hip, top left
    hx,hy=10,-20; L=70
    kx,ky=hx+math.cos(a+1.2)*L*0.55,hy+math.sin(a+1.2)*L*0.55
    fx_,fy=kx+math.cos(a+0.6)*40,ky+math.sin(a+0.6)*40
    d.line([hx,hy,kx,ky],fill=(206,180,150),width=14)               # the thigh
    d.line([kx,ky,fx_,fy],fill=RED,width=12); d.line([kx,ky,(kx+fx_)/2,(ky+fy)/2],fill=(240,240,240),width=12)   # the sock
    d.ellipse([fx_-12,fy-7,fx_+14,fy+7],fill=(24,24,28)); d.line([fx_-8,fy+5,fx_+10,fy+5],fill=(220,220,220))   # the boot
    hit=t>=0.45
    bx=96 if not hit else int(lerp(100,W+30,(t-0.45)/0.15))
    sq=0.6 if 0.45<=t<0.52 else 1.0
    r=11; d.ellipse([bx-r*sq,44-r,bx+r*sq,44+r],fill=(250,250,250),outline=(30,30,30),width=2)
    d.polygon([(bx-3*sq,40),(bx+3*sq,40),(bx+4*sq,46),(bx-4*sq,46)],fill=(30,30,30))
    if hit:
        for j in range(6): d.line([bx-14-j*6,36+j*3,bx-30-j*6,36+j*3],fill=(250,250,250))
        if t<0.52: d.ellipse([bx-24,20,bx+24,68],outline=(255,255,255),width=2)
    if t<0.05: zoom_lines(d)
    return im

def libertadores(d,x,y,lit):
    """A Copa Libertadores: the silver cup on its black base, the little footballer on top."""
    c=(220,224,232) if lit else (80,84,92); hi=(255,255,255) if lit else (110,114,120)
    d.rectangle([x-5,y,x+5,y+6],fill=(30,26,24)); d.line([x-4,y+2,x+4,y+2],fill=(150,120,60) if lit else (60,50,40))
    d.polygon([(x-4,y),(x+4,y),(x+6,y-16),(x-6,y-16)],fill=c)
    d.ellipse([x-7,y-20,x+7,y-13],fill=c); d.line([x-3,y-14,x-3,y-2],fill=hi)
    for hx in (-8,8): d.arc([x+hx-3,y-18,x+hx+3,y-10],90 if hx<0 else 270,270 if hx<0 else 90,fill=c)
    d.rectangle([x-1,y-26,x+1,y-20],fill=c); d.point((x,y-27),fill=hi); d.point((x+2,y-22),fill=c)   # the figure

def closeup_vitrina(t,f):
    """Primer plano: the trophy cabinet; the seven Libertadores light up one by one — REY DE COPAS."""
    im=Image.new('RGB',(W,H),(30,14,16)); d=ImageDraw.Draw(im)
    d.rectangle([4,6,W-5,H-2],fill=(70,36,24),outline=(120,70,40))  # the cabinet, wood
    d.rectangle([8,10,W-9,H-6],fill=(24,12,14))
    n=min(7,int(t/0.08))
    for i in range(7):
        x=22+i*24
        lit=i<n
        if lit:
            g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-12,6,x+12,60],fill=90)
            im.paste((255,236,190),(0,0),g.filter(ImageFilter.GaussianBlur(6))); d=ImageDraw.Draw(im)
        libertadores(d,x,50,lit)
    d.line([8,57,W-9,57],fill=(120,70,40))
    for x in range(8,W-9,30): d.line([x,10,x+12,H-6],fill=(60,40,40))   # reflections on the glass
    if n>0: text(d,str(n),W-16,12,GOLD)
    if t>=0.6:
        big_text(im,"REY DE COPAS",2,(255,255,255),scale=2,cx=W//2,outline=RED_D)
    if t<0.05: zoom_lines(d)
    if t>0.92: im=fade_to(im,(0,0,0),0.6*(t-0.92)/0.08)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
DEF=[(68,'cano'),(97,'sombrero'),(126,'amague')]                     # three Racing defenders, where they wait (Claude reaches each at 80, 100, 120)
def clip_clasico(f):
    s=scene(f,THEME)
    cx,cpose,cflip=CX,guard_pose(f),False
    ball=(CX+9,GROUND-2); others=[]; hud=None; score='0-0'
    if 14<=f<206: hud=True
    if 16<=f<58: s['fx'].append(('cai_big',"CLASICO",14,WHITE)); s['fx'].append(('cai_big',"DE AVELLANEDA",30,RED))
    # 1) three defenders; three dribbles
    for i,(x,kind) in enumerate(DEF):
        if not 56<=f<300: continue
        dx,dpose,dalpha=x,'idle',1.0
        if f<70: dx=lerp(220,x,(f-56)/14)
        t0=80+i*20
        if t0<=f: dpose='hurt'                                       # beaten
        if f>=270: dalpha=max(0,1-(f-270)/20)
        spr=DIVE if kind=='amague' and f>=t0 else PLAYER[dpose]               # the feint sits him down
        a=actor(spr,dx+(4 if spr is DIVE else 0),flip=True,pal=KIT_RAC); a['alpha']=dalpha; others.append(a)
    if 70<=f<146:
        cx=lerp(CX,150,(f-70)/76); cpose='dash' if (f//4)%2 else 'guard'
        ball=(cx+9,GROUND-2)
        for i,(x,kind) in enumerate(DEF):
            t0=80+i*20
            if t0-4<=f<t0+6:
                if kind=='cano': ball=(lerp(x-10,x+12,(f-t0+4)/10),GROUND-2)
                if kind=='sombrero': p=(f-t0+4)/10; ball=(lerp(x-10,x+12,p),GROUND-2-16*math.sin(p*math.pi))
        if 76<=f<146: s['fx'].append(('cai_big',"OLE!",24,WHITE))
    # 2) close-up: the strike
    if 146<=f<186: s['image']=closeup_strike((f-146)/40,f); return s
    # 3) top corner; the keeper too late
    keeper=actor(PLAYER['idle'],168,flip=True,pal=KIT_KEEP)
    if 186<=f<206:
        cx,cpose=150,'punch'; p=(f-186)/8
        if f<194: ball=(lerp(156,182,p),lerp(GROUND-4,36,p))
        else: ball=(182,36); s['fx'].append(('cai_net',184,36,f-194))
        if f>=190: keeper=actor(DIVE,170,flip=True,pal=KIT_KEEP); keeper['y']=GROUND-6
    if 194<=f<380 and f<206: score='1-0'
    if f>=194 and f<206: hud=True
    # 4) GOL DEL ROJO, red flares
    if 206<=f<256:
        ball=None; cx,cpose=ez(150,110,(f-206)/12),'armsup' if (f//5)%2 else 'dash'
        s['fx'].append(('cai_big',"GOL DEL",12,WHITE)); s['fx'].append(('cai_big',"ROJO",28,RED))
    if 200<=f<330: s['under'].append(('cai_flares',min(1,(f-200)/10) if f<310 else 1-(f-310)/20))
    if 206<=f<330: s['fx'].append(('cai_confetti',f-206,1.0 if f<310 else 1-(f-310)/20))
    # 5) close-up: the trophy cabinet
    if 256<=f<320: s['image']=closeup_vitrina((f-256)/64,f); return s
    # 6) back to the centre; the ball comes back
    if 320<=f<350: ball=None; cx,cflip,cpose=ez(110,CX,(f-320)/24),True,guard_pose(f)
    if 330<=f<350: ball=(lerp(170,CX+9,(f-330)/20),GROUND-2-6*math.sin((f-330)/20*math.pi))
    if f>=350: cx,cflip=CX,False
    if f>=354 and f<378: pass
    others.append(keeper)
    if hud: s['fx'].append(('cai_hud',score))
    if ball: s['fx'].append(('cai_ball',)+tuple(ball))
    s['actors']=others+[actor(ROJO[cpose],cx,flip=cflip,pal=RPAL)]
    return s

CLIPS = [clip('clasico', N_, clip_clasico)]
