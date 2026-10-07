"""Cyberpunk: Edgerunners (sub-theme of cyberpunk): Claude is David Martinez (the yellow ambulance
jacket, the green streak in his hair, the Sandevistan down his spine) vs Adam Smasher in the Arasaka
plaza at night, rain and neon under a huge moon. Smasher opens fire; the Sandevistan kicks in: the
world goes green and slow, the bullets hang in the air and David walks between them with afterimages
trailing behind. Lucy fades out of her optical camo and hacks the tower: code streams, the Arasaka
drones drop. Smasher crushes David's arm: the red cyberpsychosis glitch, the eyes go red. Close-up:
the Militech cyberskeleton closes on him piece by piece, I'M GONNA GET TO THE TOP. The brawl pushes
Smasher to the edge of the plaza. Then the Moon: Lucy from behind, the Earth in the sky, I WANT TO
GO TO THE MOON. Back in the plaza, both walk back to their spots."""
import zlib
from engine import *

THEME = 'cyberpunk-edgerunners'
N_ = 288                                                           # N_ % 8 == 0: the rain loops too
CX, VX = 30, 150                                                   # the neutral pose: David, Smasher
SANDY = (40,255,150)                                               # the Sandevistan green
HOLD = N_-8                                                        # the last frames hold the neutral pose

# ---- David: Claude in the yellow jacket, the green streak, the Sandevistan spine ---------------
def _david(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])
    coat=max(bot-3,max(y for y in range(h) if 'K' in spr[y])+2)
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and not inside: g[y][x]='O'                              # a bare fist
            elif c=='O' and y>=coat: g[y][x]='k' if y==coat else ('j' if y==bot else 'J')
            elif c=='o' and y>bot: g[y][x]='k'                                 # dark trousers
            elif c=='o' and y==bot and inside: g[y][x]='j'
            elif c=='o': g[y][x]='J'                                           # the sleeves
    for y in range(t+2,bot):                                                   # the spine implant, on his back
        if g[y][l] not in '.K': g[y][l]='e' if (y-t)%2 else 'z'
    return overlay(ungrid(g),["..kkkkkk...",".kkkgkkkkk.","kkkkgkkkkkk"],-1,0,bangs="kkkg.kkk")
DAVID=variant(_david)
DVPAL={'J':(250,214,40),'j':(196,150,20),'k':(24,22,30),'g':(60,240,140),'e':(60,255,150),'z':(110,112,124)}
PSYCHO=dict(DVPAL,K=(255,40,40))

# the Militech cyberskeleton around him (hand-drawn, bigger)
_SK=S([
".....kkkkk.......",
"....kkkgkkk......",
"....kOOOOOk......",
"....OOKOOKO......",
"....OOOOOOO......",
"..DDDdJJJdDDD....",
".DDdDJJJJJDdDD...",
".DDdDJJkJJDdDD...",
".DD.DJJJJJD.DD...",
".DD.DDDDDDD.DD...",
".VV.DdDDDdD.VV...",
".VV..DDDDD..VV...",
"....DD...DD......",
"....Dd...dD......",
"...DDD...DDD.....",
"...Dd.....dD.....",
"..DDD.....DDD....",])
_SK_PUNCH=S([r if not 8<=i<=10 else r[:12]+"DDDDV" for i,r in enumerate(_SK)])
_SK_PUNCH=S([r if i not in (10,11) else r[:11]+'.....' for i,r in enumerate(_SK_PUNCH)])
SKEL={'guard':_SK,'punch':_SK_PUNCH}
SKPAL=dict(PSYCHO,D=(120,124,138),d=(70,72,84),V=(60,255,150))

# ---- Adam Smasher ------------------------------------------------------------------------------
_SM=S([
"......mmmmmmm.........",
".....mMMMMMMMm........",
".....MMrrrrrMM........",
".....MMMMMMMMM........",
"......MkkkkkM.........",
"...mmmMMMMMMMmmm......",
"..mMMMMMMMMMMMMMm.....",
".mMMMMMMrMMrMMMMMm....",
".MMM.MMMMMMMMM.MMM....",
".MMM.MMMMMMMMM.MMM....",
".MMM.mMMMMMMMm.MMMCC..",
".kkk.mMMMMMMMm.MMCCCCC",
".kkk..MMMMMMM..MCCCCCC",
".kkk..mmmmmmm...CCCCC.",
"......MMM.MMM.........",
"......MMM.MMM.........",
".....MMMM.MMMM........",
".....MMM...MMM........",
".....MMM...MMM........",
"....MMMM...MMMM.......",
"....kkkk...kkkk.......",])
SM=poses(_SM,11,'k',4)
SM['idle2']=S([r.replace('rrrrr','rRrRr') for r in _SM])
SM['down']=rotate90(SM['hurt'],1,trim=True)
SMPAL={'M':(92,94,108),'m':(52,54,64),'r':(255,40,40),'R':(255,150,140),'k':(26,26,32),'C':(70,72,86)}
def sm_idle(f): return SM['idle'] if (f//6)%2==0 or f>=HOLD else SM['idle2']
MUZZLE=hand_at(_SM,VX,GROUND,True,21,12)

# ---- Lucy --------------------------------------------------------------------------------------
_LU=S([
"...WWWWW....",
"..WWWWWWW...",
"..WWsssWWn..",
"..WWsEsEWc..",
"..WnssssWn..",
"..Wc.ss.Wc..",
"....kkkk....",
"...kkkkkk...",
"..skkkkkks..",
"..s.kkkk.s..",
"....kkkk....",
"....kkkk....",
"....k..k....",
"....k..k....",
"....k..k....",
"....k..k....",
"...kk..kk...",])
LU=poses(_LU,8,'s',3)
LUPAL={'W':(240,240,250),'n':(255,110,200),'c':(80,230,255),'s':(250,214,190),'E':(200,60,160),'k':(26,24,34)}
_LU_BACK=S([   # the Moon: Lucy from behind, sitting
"...WWWW...",
"..WWWWWW..",
".WWWWWWWW.",
".WWWWWWWW.",
".WWWWWWWW.",
".nWWWWWWc.",
".nnWkkWcc.",
"..kkkkkk..",
".kkkkkkkk.",
"skkkkkkkks",
"skkkkkkkks",
".kkkkkkkk.",
"kkkkkkkkkk",])

# ---- background: the Arasaka plaza at night ----------------------------------------------------
def _plaza(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(14+16*k),int(8+6*k),int(30+18*k)))
    d.ellipse([16,-8,58,34],fill=(232,226,196)); d.ellipse([18,-6,56,32],fill=(244,238,210))   # the huge moon
    for cx,cy,r in ((30,6,3),(44,16,4),(36,22,2)): d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(218,212,184))
    rr=random.Random(zlib.crc32(b'arasaka-plaza'))
    for x,w,h in ((0,12,26),(64,14,30),(80,10,22),(160,25,24)):                                 # blocks
        d.rectangle([x,GROUND-h,x+w,GROUND],fill=(20,14,34))
        for wy in range(GROUND-h+3,GROUND-2,3):
            for wx in range(x+2,x+w-1,3):
                if rr.random()<0.35: d.point((wx,wy),fill=rr.choice([(255,90,200),(80,230,255),(250,210,90)]))
    d.rectangle([118,2,150,GROUND],fill=(16,12,26)); d.rectangle([122,2,146,GROUND],fill=(24,18,38))  # the tower
    for y in range(8,GROUND-4,4): d.line([124,y,144,y],fill=(36,28,52))
    d.rectangle([126,10,142,16],fill=(200,20,30)); text(d,'ARA',128,11,(255,230,230),shadow=None)
    d.rectangle([92,30,96,46],fill=(255,60,180)); d.rectangle([100,34,112,38],fill=(60,220,255))   # neon
    d.rectangle([0,GROUND-1,W,GROUND],fill=(40,30,56))
    for x in range(0,W,6): d.point((x,GROUND),fill=(80,60,110))                                  # wet glints
register_bg(THEME, lambda v: (v//2+16,v//3+8,v+20), decor=_plaza)

# ---- effects -----------------------------------------------------------------------------------
_DROPS=[(random.Random(i*7+1).randint(0,W+20),random.Random(i*11+3).randint(0,63)) for i in range(46)]
@fx('cpe_rain')
def _fx_rain(d,im,e,f):
    _,ph=e
    for x0,y0 in _DROPS:
        y=(y0+ph*8)%64; x=(x0-ph*2)%(W+20)-10
        d.line([x,y,x-1,y+3],fill=(110,120,170))

@fx('cpe_tint')
def _fx_tint(d,im,e,f):
    """The Sandevistan: the world slows and turns green."""
    _,a=e; im.paste(fade_to(im,SANDY,a))

@fx('cpe_after')
def _fx_after(d,im,e,f):
    _,spr,x,y,flip,a,pal=e; draw(im,spr,x,y,flip,alpha=a,tint=SANDY,f=f,pal=pal)

@fx('cpe_bullet')
def _fx_bullet(d,im,e,f):
    _,x,y=e; d.line([x,y,x+3,y],fill=(255,230,120)); d.point((x,y),fill=(255,255,255))

@fx('cpe_glitch')
def _fx_glitch(d,im,e,f):
    """Cyberpsychosis: torn horizontal bands, red."""
    _,a=e; src=im.copy(); rr=random.Random(zlib.crc32(b'psycho')+f)
    for _ in range(6):
        y=rr.randint(0,H-6); h=rr.randint(2,6); dx=rr.randint(-8,8)
        im.paste(src.crop((0,y,W,y+h)),(dx,y))
    im.paste(fade_to(im,(255,20,40),a))

@fx('cpe_code')
def _fx_code(d,im,e,f):
    """Lucy's hack: code streaming down the tower."""
    rr=random.Random(zlib.crc32(b'breach'))
    for i in range(6):
        x=123+i*4; sp=rr.randint(2,4); off=rr.randint(0,40)
        for j in range(5):
            y=(off+f*sp+j*6)%(GROUND-4)
            d.point((x,y),fill=(80,230,255) if j else (220,255,255)); d.point((x+1,y+2),fill=(60,255,150))

@fx('cpe_wire')
def _fx_wire(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(80,230,255)); d.point((x1,y1),fill=(255,255,255))

@fx('cpe_drone')
def _fx_drone(d,im,e,f):
    _,x,y,dead=e; x,y=int(x),int(y)
    d.rectangle([x-3,y-1,x+3,y+1],fill=(50,50,60)); d.line([x-5,y-3,x-1,y-3],fill=(120,120,130)); d.line([x+1,y-3,x+5,y-3],fill=(120,120,130))
    d.point((x+1,y),fill=(90,40,40) if dead else (255,40,40))

@fx('cpe_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('cpe_say',txt,y,c,scale,outline))

# ---- close-ups ---------------------------------------------------------------------------------
_PLATES=[((-40,40),(20,50,14,5)),((120,40),(60,50,14,5)),((48,90),(34,55,26,5)),
         ((-40,70),(15,46,5,14)),((120,70),(75,46,5,14))]
def closeup_skeleton(t,f):
    """The Militech cyberskeleton closes on him piece by piece: I'M GONNA GET TO THE TOP."""
    im=Image.new('RGB',(W,H),(30,6,14)); d=ImageDraw.Draw(im)
    for x in range(0,W,8): d.line([x,0,x,H],fill=(48,12,24))
    for y in range(0,H,8): d.line([0,y,W,y],fill=(48,12,24))
    bust=sprite_img(DAVID['guard'],PSYCHO,scale=3)
    im.paste(bust,(48-bust.width//2,H-bust.height+10),bust); d=ImageDraw.Draw(im)
    for i,((sx,sy),(x,y,w,h)) in enumerate(_PLATES):
        k=ease((t-0.08*i)/0.14)
        if k<=0: continue
        px=int(lerp(sx,x,k)); py=int(lerp(sy,y,k))
        d.rectangle([px,py,px+w,py+h],fill=(120,124,138),outline=(40,40,50)); d.line([px+1,py+1,px+w-1,py+1],fill=(190,194,206))
        if 0.95<k and (t-0.08*i)<0.16: spark(d,px+w//2,py+h//2,3)
    if t>=0.6:
        a=ease((t-0.6)/0.08)
        if a>0.5:
            jx=(f%3)-1 if t<0.7 else 0
            for i,line in enumerate(("I'M GONNA","GET TO","THE TOP")):
                big_text(im,line,6+i*18,(255,240,120),cx=136+jx,outline=(150,20,30))
    if t<0.06: zoom_lines(d,(255,60,80))
    return im

_STARS=[(random.Random(i).randint(0,W-1),random.Random(i+500).randint(0,40)) for i in range(40)]
def closeup_moon(t,f):
    """The Moon: Lucy from behind, the Earth up in the black: I WANT TO GO TO THE MOON."""
    im=Image.new('RGB',(W,H),(4,4,10)); d=ImageDraw.Draw(im)
    for i,(x,y) in enumerate(_STARS): d.point((x,y),fill=(200,200,220) if (i+f//6)%5 else (90,90,120))
    d.ellipse([150,4,176,30],fill=(40,90,200)); d.ellipse([154,8,166,20],fill=(70,160,90)); d.ellipse([162,18,172,26],fill=(70,160,90))
    d.arc([150,4,176,30],200,330,fill=(180,220,255))
    d.ellipse([-40,46,W+40,110],fill=(150,150,156))
    for cx,cy,r in ((30,54,5),(120,52,4),(160,58,6),(80,60,3)): d.ellipse([cx-r,cy-r//2,cx+r,cy+r//2],fill=(120,120,128))
    lu=sprite_img(_LU_BACK,LUPAL,scale=3); paste_feet(im,lu,122,56); d=ImageDraw.Draw(im)
    if t<0.1: im=fade_to(im,(0,0,0),1-t/0.1)
    elif t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1)
    if 0.2<=t<0.92:
        big_text(im,"I WANT TO GO",8,(255,255,255),cx=54,shadow=(40,40,80))
        if t>=0.32: big_text(im,"TO THE MOON.",22,(255,255,255),cx=54,shadow=(40,40,80))
    return im

# ---- the clip ----------------------------------------------------------------------------------
def slow(f):
    """The Sandevistan window."""
    return 22<=f<62

def clip_moon(f):
    s=scene(f,THEME)
    held=f>=HOLD
    if 142<=f<178:
        im=closeup_skeleton((f-142)/36,f); return dict(s,image=im)
    if 222<=f<256:
        im=closeup_moon((f-222)/34,f); return dict(s,image=im)
    rain_ph=(30 if slow(f) else f)%8
    s['under'].append(('cpe_rain',rain_ph))
    cl=actor(DAVID['guard' if held else guard_pose(f)],CX,pal=DVPAL)
    sm=actor(sm_idle(f),VX,flip=True,pal=SMPAL)
    extra=[]
    # 1) Smasher opens fire; the Sandevistan
    if 10<=f<24: sm['spr']=SM['attack']
    if 12<=f<22 and f%2==0: s['fx'].append(('spark',MUZZLE[0]-1,MUZZLE[1],3))
    rr=random.Random(zlib.crc32(b'volley'))
    shots=[(rr.uniform(46,128),GROUND-rr.randint(5,19)) for _ in range(9)]
    if 14<=f<70:
        for i,(bx,by) in enumerate(shots):
            if f<22: x=lerp(MUZZLE[0],bx,(f-14)/8)                                  # out of the cannon
            elif f<62: x=bx-(f-22)*0.25                                             # hanging in the air
            else: x=bx-10-(f-62)*28                                                 # time is back
            if x>-4: s['fx'].append(('cpe_bullet',int(x),by))
    if 18<=f<22: s['flash']=0.3*(f-18); s['fc']=(CX,GROUND-8); s['flashc']=SANDY; cl['spr']=DAVID['armsup']
    if slow(f):
        s['fx'].insert(0,('cpe_tint',0.18))
        if f<34: banner(s,"SANDEVISTAN",4,(200,255,220),2,(20,90,50))
    def dpos(g):
        if g<26: return CX
        if g<58: return lerp(CX,124,(g-26)/32)+(3 if (g//4)%2 else 0)*0          # walks between the bullets
        return 124
    if 26<=f<62:
        x=dpos(f); cl.update(spr=DAVID['dash' if (f//4)%2 else 'guard'],x=x,y=GROUND-((f//4)%2))
        for k,a in ((5,0.4),(10,0.25),(15,0.14)):
            s['under'].append(('cpe_after',DAVID['dash' if ((f-k)//4)%2 else 'guard'],dpos(f-k),GROUND,False,a,DVPAL))
    if 62<=f<68: cl.update(spr=DAVID['punch'],x=126)
    if f==62: s['fx'].append(('spark',138,GROUND-12,6)); s['shake']=rshake(2)
    if 64<=f<72: shout(s,"HEH.",(255,90,90))
    if 68<=f<72: sm['spr']=SM['attack']
    if 68<=f<80:
        t=(f-68)/12; cl.update(spr=DAVID['hurt'],x=lerp(126,60,t),y=GROUND-int(10*math.sin(math.pi*t)))
        if f==68: s['fx'].append(('spark',128,GROUND-10,5)); s['shake']=rshake(2)
    if 80<=f<112: cl.update(spr=DAVID[guard_pose(f)],x=60)
    # 2) Lucy out of her optical camo; the hack
    DR=[(98,14),(114,8),(104,24)]
    if 72<=f<114:
        lu=actor(LU['attack'] if 84<=f<106 else LU['idle'],18,pal=LUPAL)
        if f<80: lu['holo']=(f-72)/8
        if f>=108: lu['holo']=1-(f-108)/6
        extra.append(lu)
        if 84<=f<106:
            s['fx'].append(('cpe_code',)); s['fx'].append(('cpe_wire',24,GROUND-9,122,30+(f%6)))
            shout(s,"BREACH PROTOCOL",(80,230,255))
    if 74<=f<118:
        for i,(x,y) in enumerate(DR):
            if f<100: s['fx'].append(('cpe_drone',lerp(200,x,(f-74)/10),y+((f+i*3)//4)%2,False))
            else:
                t=f-100; yy=y+t*t*0.3
                if yy<GROUND-1: s['fx'].append(('cpe_drone',x-t*0.5,yy,True))
                if t<3: s['fx'].append(('spark',x,y,3))
                if int(yy)>=GROUND-2 and yy<GROUND+6: s['fx'].append(('dust',x,GROUND-1))
    if 100<=f<110: shout(s,"I GOT YOU, DAVID.",(255,140,220),y=10)
    # 3) Smasher crushes the arm; cyberpsychosis
    if 112<=f<122: sm.update(spr=SM['attack'],x=ez(VX,82,(f-112)/10))
    if 122<=f<142:
        sm.update(spr=SM['attack'],x=82); cl.update(spr=DAVID['hurt'],x=64,pal=PSYCHO)
        if f==122: s['fx'].append(('spark',70,GROUND-8,7)); s['shake']=rshake(3)
        if f<128: banner(s,"CRUNCH",6,(255,255,255),2,(120,0,20))
        if f>=128:
            s['fx'].append(('cpe_glitch',0.12+0.1*((f//2)%2))); s['shake']=rshake()
            shout(s,"CYBERPSYCHOSIS",(255,40,60),y=2)
    # 4) the cyberskeleton: the brawl to the edge
    if 178<=f<222:
        sx=lambda g: VX-64+min(4,max(0,(g-186)//8))*16 if g<214 else ez(VX+16,174,(g-214)/6)
        x=sx(f)
        ph=(f-186)%8
        cl.update(spr=SKEL['punch'] if f>=186 and ph<3 else SKEL['guard'],x=x-18,pal=SKPAL)
        sm.update(spr=SM['hurt'] if f>=186 and ph<5 else sm_idle(f),x=x)
        if f>=214: cl.update(spr=SKEL['punch'],x=VX-2); sm.update(spr=SM['hurt'],x=x)
        if f>=186 and ph==0 and f<214: s['fx'].append(('spark',x-10,GROUND-12,5)); s['shake']=rshake(2)
        if f==214: s['fx'].append(('spark',x-10,GROUND-12,8)); s['shake']=rshake(3); s['flash']=0.4; s['fc']=(x,GROUND-12); s['flashc']=(255,240,200)
        if 178<=f<184: s['flash']=0.5-(f-178)*0.08; s['fc']=(x-18,GROUND-10); s['flashc']=SANDY
        if 188<=f<212: shout(s,"AAAAARGH!",(255,240,120))
        if f>=180: s['under'].append(('cpe_after',SKEL['guard'],x-24,GROUND,False,0.25,SKPAL))
    # 5) back in the plaza: both walk back to their spots
    if 256<=f<HOLD:
        t=(f-256)/(HOLD-256)
        cl.update(spr=DAVID[guard_pose(f)],x=ez(120,CX,t),flip=t<0.95)
        sm.update(spr=sm_idle(f),x=ez(178,VX,t))
    s['actors']=[sm]+extra+[cl]
    return s

CLIPS = [clip('moon', N_, clip_moon)]
