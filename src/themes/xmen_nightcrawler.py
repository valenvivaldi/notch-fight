"""X-Men '97 sub-theme "xmen-nightcrawler": Claude as Kurt Wagner, Nightcrawler (blue fur, yellow eyes,
pointed ears, the spade-tipped tail, red and black suit), on a New York rooftop at dusk. Four Sentinel
drones jet in and surround him (MUTANT DETECTED); their beams cross where he was — BAMF, a puff of
indigo smoke. He pops up behind each one in turn and drops it, every jump leaving its cloud. Close-up:
the yellow eyes and the fanged grin, BAMF!. The last drone fires; Kurt grabs it and teleports it high
into the sky, and it falls and smashes (AUF WIEDERSEHEN!). The wrecks burn out for the loop.
The Sentinel drone lives here for the other X-Men '97 themes."""
from engine import *

THEME = 'xmen-nightcrawler'
N_ = 301
CX = 30                                                             # the loop keyframe position

SMOKE = ((110,70,170),(76,46,128),(156,116,214))
# Kurt: blue fur, navy hair, yellow eyes; the suit black down the middle, red at the sides
KPAL = {'1':(70,84,176),'2':(46,56,130),'3':(206,40,52),'4':(30,28,40),'5':(255,226,80),'6':(30,34,84)}
HAIR = ["..6.6.6.6...",".666666666..","66666666666."]

def _kurt(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g); w=len(g[0])
    for y in range(h):
        for x in range(w):
            c=g[y][x]
            if c=='K': g[y][x]='5'
            elif c=='O': g[y][x]='1' if y<top+5 else ('4' if l+2<=x<=r-2 else '3')
            elif c=='o': g[y][x]=('1' if y<top+5 else '3') if y<top+8 else ('2' if y==h-1 else '4')
    for ex in (l-1,r+1):                                            # the pointed ears
        if 0<=ex<w and g[top+1][ex]=='.': g[top+1][ex]='1'
    return S([''.join(x) for x in g])
KURT=variant(_kurt)

# the Sentinel drone: purple armour, pink joints, a grey face plate with glowing eyes
DRONE=S([
".....VVVVV......","....VDDDDDV.....","....DYDDYDV.....","....DDDDDDV.....","....DDppDD......",
".....VVVV.......","...nnVVVVnn.....","..nnVnnnnVnn....","..VV.nnnn.VV....","..VV.VVVV.VV....",
"..nn.VVVV.nn....","..DD.VppV.DD....","....VVVVVV......","....VV..VV......","....nn..nn......",
"....VV..VV......","...VVV..VVV.....",])
DR=poses(DRONE,10,'n',3)
DR['wreck']=rotate90(DR['hurt'],1,trim=True)
DRONE_PALM=(14,10)                                                  # the end of the attacking arm

# ---- background: a New York rooftop at dusk, X-Men '97 colours ----------------------------------------
def _rooftop(d):
    bands=[(250,150,90),(236,110,100),(196,86,126),(140,70,140),(86,54,128)]
    for i,c in enumerate(bands[::-1]):                               # cel-shaded sky in flat bands
        d.rectangle([0,i*9,W,i*9+9],fill=c)
    d.ellipse([140,30,164,54],fill=(255,200,120))
    rr=random.Random(97)
    x=0
    while x<W:                                                      # the skyline, two flat layers
        w=rr.randint(8,18); top=rr.randint(18,34)
        d.rectangle([x,top,x+w,46],fill=(70,40,96))
        for wy in range(top+3,44,4):
            for wx in range(x+2,x+w-1,4):
                if rr.random()<0.3: d.point((wx,wy),fill=(255,214,120))
        x+=w+rr.randint(0,2)
    d.rectangle([60,10,64,30],fill=(56,30,80)); d.polygon([(58,10),(62,2),(66,10)],fill=(56,30,80))   # a spire
    d.rectangle([0,46,W,H],fill=(90,70,96))                         # the rooftop
    d.line([0,46,W,46],fill=(140,110,140)); d.line([0,47,W,47],fill=(60,44,70))
    d.rectangle([150,30,164,46],fill=(110,74,60)); d.polygon([(148,30),(157,24),(166,30)],fill=(90,60,50))   # a water tower
    for lx in (152,162): d.line([lx,46,lx,40],fill=(60,40,40))
    for x in range(4,W,26): d.rectangle([x,40,x+6,46],fill=(110,90,110))   # vents
    for _ in range(30): d.point((rr.randint(0,W-1),rr.randint(49,H-1)),fill=(76,58,82))
register_bg(THEME, lambda v: (v+60,v+40,v+70), decor=_rooftop)

# ---- effects ----------------------------------------------------------------------------------------
@fx('nc_bamf')
def _fx_bamf(d,im,e,f):
    """BAMF: an indigo puff of smoke (t = frames since the jump, 0..13), the word in it at first."""
    _,x,y,t=e; x,y=int(x),int(y)
    if not 0<=t<14: return
    rr=random.Random(int(x)*31+int(y))
    for j in range(10):
        a=rr.uniform(0,6.283); L=rr.uniform(0,7)+t*0.6; r=max(1,int(rr.randint(3,6)-t*0.35))
        px,py=x+math.cos(a)*L,y+math.sin(a)*L*0.7-t*0.4
        d.ellipse([px-r,py-r,px+r,py+r],fill=SMOKE[j%3])
    if t<6: text(d,"BAMF",x-7,y-2,(255,255,255),shadow=(40,20,70))

@fx('nc_tail')
def _fx_tail(d,im,e,f):
    """Kurt's tail: from the small of his back, swaying, with the spade tip."""
    _,x,feet,flip=e; back=1 if flip else -1
    pts=[]
    for k in range(10):
        t=k/9; pts.append((x+back*(3+t*9),feet-3-t*7+math.sin(f*0.25+t*3)*2*t))
    d.line(pts,fill=KPAL['2'],width=1)
    tx,ty=pts[-1]; d.polygon([(tx,ty-2),(tx+back*3,ty),(tx,ty+2)],fill=KPAL['2'])

@fx('nc_jet')
def _fx_jet(d,im,e,f):
    _,x,feet=e
    for dx in (-3,2):
        L=3+(f+dx)%3; d.line([x+dx,feet+1,x+dx,feet+L],fill=(255,200,90)); d.point((x+dx,feet+1),fill=(255,255,255))

@fx('nc_beam')
def _fx_beam(d,im,e,f):
    _,x0,y0,x1,y1=e
    d.line([x0,y0,x1,y1],fill=(255,110,200),width=3); d.line([x0,y0,x1,y1],fill=(255,230,250),width=1)

# ---- close-up ---------------------------------------------------------------------------------------
def closeup_grin(t,f):
    """Primer plano: in the middle of a puff of smoke, the yellow eyes light up and the fanged grin — BAMF!"""
    im=Image.new('RGB',(W,H),(60,36,96)); d=ImageDraw.Draw(im)
    rr=random.Random(f//2)
    for j in range(26):                                             # the smoke he is standing in
        x=rr.randint(-10,W+10); y=rr.randint(-10,H+10); r=rr.randint(8,16)
        d.ellipse([x-r,y-r,x+r,y+r],fill=SMOKE[j%3])
    ox=14; blue,shade,hair=KPAL['1'],KPAL['2'],KPAL['6']
    d.polygon([(ox-8,26),(ox+2,16),(ox+4,36)],fill=blue); d.polygon([(ox+64,26),(ox+54,16),(ox+52,36)],fill=blue)   # ears
    d.rectangle([ox,12,ox+56,H],fill=blue); d.rectangle([ox+50,12,ox+56,H],fill=shade)
    for k in range(8): d.polygon([(ox-2+k*8,16),(ox+8+k*8,16),(ox+2+k*8+(k%2)*3,0)],fill=hair)
    d.rectangle([ox-2,8,ox+58,16],fill=hair)
    lit=t>=0.15
    for ex in (ox+16,ox+40):
        d.polygon([(ex-7,25),(ex+7,23 if ex<ox+28 else 27),(ex+6,32),(ex-6,32)],fill=(255,226,80) if lit else (150,130,60))
        if lit and (f//2)%2: d.polygon([(ex-5,26),(ex+5,25 if ex<ox+28 else 27),(ex+4,30),(ex-4,30)],fill=(255,250,200))
    grin=min(1,max(0,(t-0.2)/0.15))
    if grin:
        w=int(10+12*grin)
        d.chord([ox+28-w,40,ox+28+w,54],0,180,fill=(30,10,20)); d.rectangle([ox+28-w+2,46,ox+28+w-2,48],fill=(250,250,250))
        for fx_ in (ox+28-w+4,ox+28+w-5): d.polygon([(fx_,48),(fx_+2,48),(fx_+1,52)],fill=(250,250,250))   # fangs
    else: d.line([ox+20,47,ox+36,47],fill=(30,10,20))
    if t>=0.3:
        jj=(f%3)-1 if t<0.4 else 0
        big_text(im,"BAMF!",14,(255,255,255),scale=3,cx=136+jj,outline=(60,20,100))
    if t<0.06: zoom_lines(d,(200,170,255))
    if t>0.88: im=fade_to(im,SMOKE[0],(t-0.88)/0.12)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
SPOTS=[8,74,118,162]                                                 # where the drones hover down to
HITS=[(64,3,'dash'),(80,1,'punch'),(96,2,'dash')]                   # (frame he pops in, drone, the blow)
def drone_state(i,f):
    """(x, feet, pose, flip, flying) for drone i, or None when gone."""
    x=SPOTS[i]; flip=x>CX
    if f<14 or f>=280: return None
    if f<34: return x,lerp(-4,GROUND-6,ease((f-14-i*2)/18)),'idle',flip,True
    feet,pose,fly=GROUND-6+int(math.sin(f*0.2+i)),'idle',True
    if 46<=f<60: pose='attack'
    for h,j,_ in HITS:
        if j==i and f>=h+4: return x,GROUND,'wreck',flip,False
    if i==0:
        if 164<=f<176: pose='attack'
        if 180<=f<190: return None                                  # teleported away with him
        if 190<=f<204: return 96,lerp(-4,GROUND,((f-190)/14)**2),'hurt',False,False
        if f>=204: return 96,GROUND,'wreck',False,False
    return x,feet,pose,flip,fly

def clip_bamf(f):
    s=scene(f,THEME)
    kx,ky,kpose,kflip,show=CX,GROUND,guard_pose(f),False,True
    if 30<=f<62: callout(s,"MUTANT DETECTED",c=(255,110,170))
    # 1) the drones jet in and fire; BAMF
    if 50<=f<58:
        for i in range(4):
            st=drone_state(i,f); hx,hy=hand_at(DR['attack'],st[0],int(st[1]),st[3],*DRONE_PALM)
            s['fx'].append(('nc_beam',hx,hy,CX,GROUND-6))
    if 54<=f<64: show=False
    s['under'].append(('nc_bamf',CX,GROUND-6,f-54))
    if 56<=f<62: s['fx'].append(('boom',CX,GROUND-6,2+(f-56)*2)); s['shake']=rshake(2)
    # 2) behind each one in turn
    for h,i,blow in HITS:
        x=SPOTS[i]; side=1 if x>CX else -1; bx=x+side*12
        s['under'].append(('nc_bamf',bx,GROUND-6,f-h))
        if h<=f<h+12: kx,kflip,kpose,show=bx,side>0,(blow if f<h+5 else guard_pose(f)),True
        if h-2<=f<h: show=False
        if f==h+4: s['fx'].append(('spark',x,GROUND-10,6)); s['shake']=rshake(2); s['flash']=0.3; s['fc']=(x,GROUND-10); s['flashc']=(255,150,220)
        if h+12<=f<h+16: show=False
        if f>=h+12: s['under'].append(('nc_bamf',bx,GROUND-6,f-h-12))
    # 3) close-up
    if 112<=f<160: s['image']=closeup_grin((f-112)/48,f); return s
    # 4) the last drone: he grabs it and takes it up into the sky
    if 160<=f<164: show=False
    if 160<=f<180: kx,kflip,kpose,show=SPOTS[0]+12,True,'guard' if f<170 else 'punch',f>=164
    s['under'].append(('nc_bamf',SPOTS[0]+12,GROUND-6,f-160))
    if 164<=f<172: s['fx'].append(('nc_beam',SPOTS[0]+6,GROUND-14,SPOTS[0]+30,GROUND-14))
    if 180<=f<192: show=False
    s['under'].append(('nc_bamf',SPOTS[0]+6,GROUND-8,f-180))
    s['under'].append(('nc_bamf',96,8,f-190))
    if 194<=f<200: s['under'].append(('nc_bamf',CX,GROUND-6,f-194))
    if 192<=f<198: show=False
    if 204<=f<214:
        s['shake']=rshake(3 if f<208 else 1); s['fx'].append(('boom',96,GROUND-6,4+(f-204)*3))
        if f==204: s['flash']=1.0; s['fc']=(96,GROUND-8); s['flashc']=(255,200,160)
        s['fx']+= [('rock',96+random.randint(-20,20),GROUND-random.randint(2,20)) for _ in range(3)]
    if 206<=f<244: s['fx'].append(('big',"AUF WIEDERSEHEN!",4,(255,255,255)))
    # 5) the wrecks smoke, then go up in one last puff each
    for i in range(4):
        st=drone_state(i,f)
        if st and st[2]=='wreck' and f>=214:
            rr=random.Random(f//3+i)
            if rr.random()<0.5: s['fx'].append(('smoke',st[0]+rr.randint(-6,6),GROUND-6-rr.randint(0,8),2,(90,80,96)))
        if 266<=f<280 and st: s['fx'].append(('smoke',st[0],GROUND-4-(f-266)//2,3+(f-266)//3,(120,110,126)))
    acts=[]
    for i in range(4):
        st=drone_state(i,f)
        if not st: continue
        x,feet,pose,flip,fly=st
        a=1 if f<268 else max(0,1-(f-268)/10)
        acts.append(actor(DR[pose],x,int(feet),flip=flip,alpha=a))
        if fly: s['fx'].append(('nc_jet',x,int(feet)))
    if show:
        s['under'].append(('nc_tail',kx,ky,kflip))
        acts.append(actor(KURT[kpose],kx,ky,flip=kflip,pal=KPAL))
    s['actors']=acts
    return s

CLIPS = [clip('bamf', N_, clip_bamf)]
