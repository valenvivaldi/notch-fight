"""Argentina: the 2022 World Cup final. Claude as the number 10 in the albiceleste, Lusail at night.
3-3 at minute 123: Kolo Muani runs clean through on Argentina's goal and Dibu blocks it with his leg
(close-up: DIBU!). Then PENALES: Claude scores, Dibu saves one, the dots fill up, Montiel scores the
last one - CAMPEONES DEL MUNDO. Claude lifts the Cup, blue-and-white confetti, the third star lights up.
Other players are generic figures (kit colours, a number), never likenesses.
The pitch, ball, goals and TV scoreboard live here; they move to src/engine/ when a second football
theme (cai, lfc) needs them."""
from engine import *

THEME = 'arg'
N_ = 384

CELESTE, WHITE, GOLD = (116,172,223), (244,244,244), (236,190,60)
FRA = (34,48,120)
HUD_BG, HUD_INK = (16,16,22), (236,236,236)
# Claude as the 10: sky-blue and white stripes, black shorts, the captain's armband
CPAL = {'c':CELESTE, 'W':WHITE, 'b':(24,24,28), 'y':(236,200,60)}
# generic players: jersey j/J (J = second stripe colour), skin s, hair h, shorts p, boots k
KIT_FRA   = {'j':FRA, 'J':FRA, 's':(150,104,78), 'h':(24,20,20), 'p':(236,236,236)}
KIT_DIBU  = {'j':(150,235,70), 'J':(150,235,70), 's':(226,184,150), 'h':(40,30,26), 'p':(110,190,50), 'g':(248,248,248), 'k':(230,60,50)}
KIT_ARG   = {'j':CELESTE, 'J':WHITE, 's':(210,160,120), 'h':(40,30,26), 'p':(24,24,28)}

def _albiceleste(spr):
    g=[list(r) for r in spr]
    top,l,r=body_box(spr); h=len(g)
    for y in range(top+4,min(top+9,h)):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]=('c' if (x-l)//2%2==0 else 'W') if y<top+8 else 'b'
    for y in range(top+5,min(top+7,h)):                                    # the captain's armband
        for x in range(len(g[0])):
            if g[y][x]=='o' and x<l: g[y][x]='y'; break
    return S([''.join(x) for x in g])
TEN=variant(_albiceleste)
albiceleste=_albiceleste               # for the sub-themes (arg-86)

PLAYER=poses(S([
"....hhhh....","...hhhhhh...","...ssssss...","...sKssKs...","...ssssss...","....ssss....",
"..jJjJjJjJ..",".sjJjJjJjJs.",".sjJjJjJjJs.","..jJjJjJjJ..","..jJjJjJjJ..","...pppppp...",
"...pppppp...","...ss..ss...","...ss..ss...","...kk..kk...",]),7,'s',3)
DIVE=rotate90(PLAYER['idle'],1,trim=True)            # a keeper at full stretch
STARFISH=S([                                         # Dibu spread wide: arms up, legs out (front on)
"g.....hhhh.....g",".j....ssss....j.","..j...sKKs...j..","...j.jjjjjj.j...","....jjjjjjjj....",
".....jjjjjj.....",".....pppppp.....","....pp....ppp...","...jj......jjj..","..jj.........jj.",
".kk...........kk",])

# ---------------------------------------------------------------- Lusail at night
def _lusail(d):
    """Stands full of fans under the lights, a striped pitch, the goal on the right with its net."""
    d.rectangle([0,0,W,28],fill=(20,20,30))
    rr=random.Random(2022)
    for y in range(4,28,3):
        for x in range(0,W,3):
            c=rr.choice(((116,172,223),(236,236,236),(116,172,223),(40,50,90),(200,60,60),(80,80,100)))
            if rr.random()<0.7: d.point((x+(y//3)%2,y),fill=c)
    for x in range(0,W,16): d.rectangle([x,28,x+7,GROUND],fill=(46,110,52))              # mown stripes
    for x in range(8,W,16): d.rectangle([x,28,x+7,GROUND],fill=(54,124,60))
    d.line([0,28,W,28],fill=(236,236,236))
    d.line([150,34,150,GROUND],fill=(220,230,220)); d.point((160,50),fill=(236,236,236))  # box line, spot
    draw_goal(d,176,1)

def draw_goal(d,x,side):
    """A goal seen from the side: posts, crossbar, net hatching (side 1: right, -1: left)."""
    x0,x1=(x,x+8) if side>0 else (x-8,x)
    for gx in range(x0,x1,2): d.line([gx,34,gx,GROUND],fill=(170,180,180))
    for gy in range(34,GROUND,3): d.line([x0,gy,x1,gy],fill=(170,180,180))
    post=x0 if side>0 else x1
    d.line([post,32,post,GROUND],fill=(250,250,250)); d.line([x0,32,x1,32],fill=(250,250,250))
register_bg(THEME, lambda v: (v//3,v+20,v//3), decor=_lusail)

@fx('arg_leftgoal')
def _fx_leftgoal(d,im,e,f): draw_goal(d,8,-1)

@fx('arg_net')
def _fx_net(d,im,e,f):
    """The net bulging where the ball went in (k: frames since)."""
    _,x,y,k=e
    if k<12: r=3+k//2; d.arc([x-r,y-r,x+r,y+r],-80,80,fill=(250,250,250))

@fx('arg_ball')
def _fx_ball(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.ellipse([x-2,y-2,x+1,y+1],fill=(250,250,250),outline=(40,40,40)); d.point((x-1,y-1),fill=(40,40,40))

@fx('arg_flashes')
def _fx_flashes(d,im,e,f):
    """Phones flashing in the stands."""
    rr=random.Random((f%96)*3)                                       # a 96-frame cycle: the clip loops
    for _ in range(5): d.point((rr.randint(0,W),rr.randint(4,26)),fill=(255,255,255))

@fx('arg_hud')
def _fx_hud(d,im,e,f):
    """The TV scoreboard: ARG 3-3 FRA, the minute or PENALES, and the shootout dots."""
    _,label,arg,fra=e
    d.rounded_rectangle([3,3,70,12],radius=2,fill=HUD_BG,outline=(90,90,110))
    d.rectangle([5,5,7,10],fill=CELESTE); d.point((6,7),fill=WHITE)
    text(d,"ARG 3-3 FRA",10,5,HUD_INK,shadow=None)
    d.rectangle([56,4,69,11],fill=(40,40,56)); text(d,label,57,5,GOLD,shadow=None)
    if arg is not None:
        for row,(dots,y) in enumerate(((arg,15),(fra,20))):
            d.rounded_rectangle([3,y-1,40,y+4],radius=2,fill=HUD_BG)
            text(d,"ARG" if row==0 else "FRA",5,y,HUD_INK,shadow=None)
            for i,st in enumerate(dots):
                cx=22+i*4; c={'g':(90,220,110),'x':(230,70,70),'.':(80,80,90)}[st]
                d.ellipse([cx-1,y+1,cx+1,y+3],fill=c)

@fx('arg_big')
def _fx_big(d,im,e,f):
    _,txt,y,c=e; big_text(im,txt,y,c,shadow=(0,0,0),outline=(0,0,0))

@fx('arg_confetti')
def _fx_confetti(d,im,e,f):
    _,k,dens=e; rr=random.Random(10)
    for i in range(int(70*dens)):
        x=(rr.uniform(0,W)+math.sin(k*0.1+i)*4)%W; y=(rr.uniform(-H,0)+k*rr.uniform(0.8,1.6))%(H+10)-5
        c=CELESTE if i%2 else WHITE
        if (k+i)%3: d.rectangle([x,y,x+1,y],fill=c)
        else: d.point((int(x),int(y)),fill=c)

@fx('arg_cup')
def _fx_cup(d,im,e,f):
    """The World Cup, gold, held up at (x,y), with a glint."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-4,y-9,x+4,y-2],fill=GOLD,outline=(150,110,30))                      # the globe
    d.polygon([(x-3,y-3),(x+3,y-3),(x+2,y+4),(x-2,y+4)],fill=GOLD,outline=(150,110,30))
    d.rectangle([x-3,y+4,x+3,y+6],fill=(40,110,60))                                    # the green band
    d.point((x-2,y-7),fill=(255,250,210))
    if (f//3)%4==0: d.line([x+3,y-10,x+3,y-6],fill=(255,255,255)); d.line([x+1,y-8,x+5,y-8],fill=(255,255,255))

def _star(d,cx,cy,c):
    pts=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5; r=3 if k%2==0 else 1.3
        pts.append((cx+math.cos(a)*r,cy+math.sin(a)*r))
    d.polygon(pts,fill=c)

@fx('arg_stars')
def _fx_stars(d,im,e,f):
    """The stars over the crest: two, then the third lights up."""
    _,x,y,third=e
    for i,dx in enumerate((-8,0,8)):
        if i<2 or third>0: _star(d,x+dx,y,GOLD if (i<2 or third>=1) else (120,100,50))
    if 0<third<1 and (f//2)%2: d.ellipse([x+5,y-3,x+11,y+3],outline=(255,250,210))

def closeup_leg(t,f):
    """Primer plano: minute 123, from the front. Kolo Muani shoots from the left; Dibu spreads like a
    starfish - arms flung up, gloves wide - and his outstretched left leg takes the ball off his shin."""
    im=Image.new('RGB',(W,H),(46,110,52)); d=ImageDraw.Draw(im)
    for x in range(0,W,24): d.rectangle([x,0,x+11,H],fill=(54,124,60))
    d.line([0,10,W,4],fill=(220,230,220))                                                  # a line on the grass
    lime,lime_d,skin=KIT_DIBU['j'],KIT_DIBU['p'],KIT_DIBU['s']
    reach=ease(min(1,t/0.25))
    # Kolo Muani, left, just struck it (navy, number on the back)
    d.rectangle([14,20,32,40],fill=FRA); d.ellipse([16,8,30,22],fill=KIT_FRA['s']); d.rectangle([16,7,30,11],fill=KIT_FRA['h'])
    d.line([18,40,10,58],fill=FRA,width=5); d.line([28,40,40,54],fill=FRA,width=5)            # standing leg, kicking leg
    d.rectangle([38,52,44,56],fill=(90,200,220)); text(d,"12",19,26,(236,190,60),shadow=None)
    # Dibu, front on: arms up and out, gloves, orange wrists
    cx=112
    for sx in (-1,1):
        d.line([cx+sx*12,18,cx+sx*44,4],fill=lime,width=5)
        gx=cx+sx*47; d.rectangle([gx-3,0,gx+3,6],fill=(248,248,248),outline=(60,60,60))
        d.rectangle([cx+sx*42-2,4,cx+sx*42+2,8],fill=(255,130,40))
    d.rectangle([cx-14,12,cx+14,34],fill=lime,outline=lime_d)                                # shirt
    text(d,"23",cx-3,20,lime_d,shadow=None)
    d.ellipse([cx-7,0,cx+7,14],fill=skin); d.rectangle([cx-7,0,cx+7,3],fill=KIT_DIBU['h'])   # head
    d.rectangle([cx-12,34,cx+12,40],fill=lime_d)                                              # shorts
    d.line([cx-8,40,cx-20,48],fill=lime,width=6); d.line([cx-20,48,cx-26,58],fill=lime,width=5)   # bent right leg
    d.rectangle([cx-30,56,cx-22,60],fill=(248,248,248))
    lx,ly=int(lerp(cx+14,cx+62,reach)),int(lerp(44,54,reach))                               # the outstretched left leg
    d.line([cx+8,40,lx,ly],fill=lime,width=6); d.rectangle([lx-2,ly-3,lx+6,ly+3],fill=(230,60,50))
    # the ball: from Kolo Muani's boot to Dibu's shin, then away
    shin=(lerp(cx+8,lx,0.7),lerp(40,ly,0.7))
    if t<0.25: bx,by=lerp(44,shin[0],t/0.25),lerp(52,shin[1],t/0.25)
    else: q=min(1,(t-0.25)/0.3); bx,by=lerp(shin[0],W+10,q),lerp(shin[1],-10,q)
    d.ellipse([bx-5,by-5,bx+5,by+5],fill=(250,250,250),outline=(40,40,40)); d.point((int(bx),int(by)),fill=(40,40,40))
    if 0.24<t<0.32: spark(d,int(shin[0]),int(shin[1]),6,(255,255,255))
    if t>=0.28: big_text(im,"DIBU!",44,(170,250,110),cx=60,shadow=(0,0,0),outline=(0,0,0))
    text(d,"123",4,4,(236,236,236))
    if t<0.06: zoom_lines(d)
    return im

# ---------------------------------------------------------------- the clip
def clip_final(f):
    s=scene(f,THEME)
    s['under'].append(('arg_flashes',))
    tx,ty,tpose,tflip=40,GROUND,guard_pose(f),False
    ball=(49,GROUND-2) if f<44 or f>=370 else None
    others=[]; hud=None
    # 1) the scoreboard
    if 14<=f<46: hud=('123',None,None)
    # 2) minute 123: Kolo Muani clean through on Argentina's goal (left); Claude chasing back
    if 44<=f<112:
        s['under'].append(('arg_leftgoal',)); hud=('123',None,None)
        p=(f-44)/40
        km=ez(170,52,p) if f<84 else 52
        others.append(actor(PLAYER['attack' if 80<=f<86 else 'idle'],km,flip=True,pal=KIT_FRA))
        dibu_x=ez(26,34,p)
        others.append(actor(PLAYER['idle'] if f<80 else STARFISH,dibu_x,flip=True,pal=KIT_DIBU))
        tx,tpose,tflip=ez(40,126,min(1,(f-44)/14)) if f<58 else ez(126,70,(f-58)/40),'dash',True
        if f<82: ball=(km-6,GROUND-2)
        elif f<86: ball=(lerp(km-6,30,(f-82)/4),GROUND-6)
        else: ball=(lerp(30,60,(f-86)/20),GROUND-20-10*math.sin((f-86)/20*math.pi))
        if 86<=f<90: s['fx'].append(('spark',30,GROUND-8,4))
    # 3) close-up: the leg
    if 112<=f<158: s['image']=closeup_leg((f-112)/46,f); return s
    # 4) PENALES
    arg_dots,fra_dots='.....','.....'
    if 158<=f<350: tx,tflip=40,False
    if 158<=f<190: hud=('PEN','.....','.....'); s['fx'].append(('arg_big',"PENALES",24,GOLD))
    if 190<=f<226:                                                               # Claude's penalty
        tx,tpose=ez(130,150,(f-190)/14) if f<204 else 150,'dash' if f<204 else 'punch'
        if f<204: ball=(160,50)
        elif f<210: ball=(lerp(160,180,(f-204)/6),lerp(50,40,(f-204)/6))
        else: ball=(180,40); s['fx'].append(('arg_net',182,40,f-210))
        others.append(actor(PLAYER['idle'] if f<205 else DIVE,178,flip=True,pal={**KIT_FRA,'j':(90,90,96),'J':(90,90,96)}))
        if f>=210: s['fx'].append(('arg_big',"GOL",24,WHITE))
        arg_dots='g....' if f>=210 else arg_dots
    if 190<=f<226: hud=('PEN',arg_dots,'.....')
    if 226<=f<256:                                                               # the shootout rolls on
        k=(f-226)//6
        arg_dots=('gg...','gg...','ggg..','ggg..','ggg..')[min(4,k)]
        fra_dots=('g....','gx...','gx...','gxx..','gxg..')[min(4,k)]
        hud=('PEN',arg_dots,fra_dots)
        if 232<=f<240: others.append(actor(DIVE,172,flip=True,pal=KIT_DIBU)); s['fx'].append(('spark',166,44,3))
    if 256<=f<296:                                                               # Montiel: the last one
        if f<268: hud=('PEN','ggg' + ('g.' if f>=266 else '..'),'gxgx.')          # gone once the celebration starts
        others.append(actor(PLAYER['attack' if 262<=f<266 else 'idle'],ez(130,152,(f-256)/8),pal=KIT_ARG))
        if f<264: ball=(160,50)
        elif f<268: ball=(lerp(160,180,(f-264)/4),lerp(50,42,(f-264)/4))
        else: ball=(180,42); s['fx'].append(('arg_net',182,42,f-268))
        others.append(actor(PLAYER['idle'] if f<265 else DIVE,178,flip=True,pal={**KIT_FRA,'j':(90,90,96),'J':(90,90,96)}))
        tx,tpose=60,'armsup' if f>=268 else guard_pose(f)
    if 268<=f<318:                                                               # 2.5 s
        s['fx'].append(('arg_big',"CAMPEONES",14,WHITE)); s['fx'].append(('arg_big',"DEL MUNDO",30,CELESTE))
    # 5) the Cup, the third star, confetti
    if 268<=f<366: s['fx'].append(('arg_confetti',f-268,1.0 if f<346 else 1-(f-346)/20))
    if 296<=f<318: tx,tpose=60,guard_pose(f)                                     # the text first
    if 318<=f<352:                                                               # then the Cup and the stars
        tx,tpose=60,'armsup'; hx,hy=hand_at(TEN['armsup'],60,GROUND,False,12,0,h=11)
        s['fx'].append(('arg_cup',hx,hy-2))
        s['fx'].append(('arg_stars',hx,hy-18,min(1,max(0,(f-328)/12))))
    # 6) back to the neutral pose
    if 352<=f<370: tx,tflip,tpose=ez(60,40,(f-352)/18),True,guard_pose(f)
    if f>=370: tx,tflip=40,False
    if hud: s['fx'].append(('arg_hud',)+hud)
    if ball: s['fx'].append(('arg_ball',)+ball)
    s['actors']=others+[actor(TEN[tpose],tx,ty,flip=tflip,pal=CPAL)]
    return s

CLIPS = [clip('final', N_, clip_final)]
