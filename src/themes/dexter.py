"""Dexter's Laboratory: Claude is the boy genius (parted orange hair, the glasses, the white lab
coat, purple gloves, black boots) and Dee Dee is in the lab again (blonde pigtails, pink tutu).
"OOOH! WHAT DOES THIS BUTTON DO?" — "DEE DEE! GET OUT OF MY LABORATORY!" Claude pulls the lever and
the mech drops from the ceiling around him; it stomps forward firing lasers and Dee Dee pirouettes
through every shot. She twirls up to the mech and presses the big red button on its chest: SELF
DESTRUCT, KABOOM. Claude stands in the smoke, black with soot: "DEE DEEEE!" She skips back to her
spot giggling; Claude dusts off and walks back to his."""
import zlib
from engine import *

THEME = 'dexter'
N_ = 288
CX, VX = 30, 150                                                   # the neutral pose: Claude, Dee Dee
MX = 34                                                            # where the mech lands

# ---- Claude as Dexter --------------------------------------------------------------------------
def _dex(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])                             # the body's last row
    coat=max(bot-3,max(y for y in range(h) if 'K' in spr[y])+2)               # below the eyes
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and not inside: g[y][x]='V'                             # a fist
            elif c=='O' and y>=coat: g[y][x]='v' if x==(l+r)//2+1 else 'W'   # the coat, open in front
            elif c=='o' and y>bot: g[y][x]='k'                                # boots
            elif c=='o' and y==bot and inside: g[y][x]='W'
            elif c=='o': g[y][x]='V'                                          # gloves
    eyes=[(x,y) for y in range(1,h-1) for x in range(2,w) if g[y][x]=='K' and g[y-1][x]!='K' and g[y+1][x]=='K']
    for i,(x,y) in enumerate(eyes):                                           # the glasses: white lenses, a dot of pupil
        g[y-1][x-1]=g[y-1][x]='k'; g[y][x-1]=g[y+1][x-1]=g[y+1][x]='H'
        if i==0 and g[y][x-2]=='O': g[y][x-2]=g[y-1][x-2]='k'
        if g[y][x+1]=='O': g[y][x+1]='k'
    return overlay(ungrid(g),["..xxxx.xxx.",".xxxxxx.xxxx"],-1,0)
DEX=variant(_dex)
DEXPAL={'x':(214,84,34),'W':(240,240,244),'v':(176,176,192),'V':(120,70,180),'k':(24,22,28),
        'H':(232,244,255)}
def sooty(a):
    """The palette a of the way from soot-black (1) back to normal (0)."""
    soot={'O':(56,46,44),'o':(40,32,30),'x':(50,40,36),'W':(70,68,70),'v':(50,48,50),'V':(46,40,52),
          'K':(250,250,250),'H':(60,60,64)}
    out=dict(DEXPAL)
    for k,c in soot.items():
        b=out.get(k) or PAL[k]; out[k]=tuple(int(b[i]+(c[i]-b[i])*a) for i in range(3))
    return out

# ---- Dee Dee -----------------------------------------------------------------------------------
_DD=S([
"......yyyy......",
"yyy..yyyyyy..yyy",
"yyyyyyyyyyyyyyyy",
"yyy.ysssssss.yyy",
"....ssEsssEs....",
"....ssEsssEs....",
"....ssssssss....",
".....ssnnss.....",
"......ssss......",
".....nnnnnn.....",
"...ssnnnnnnss...",
"..ss.nnnnnn.ss..",
"..s..nnnnnn..s..",
"..PPPPPPPPPPPP..",
".PPnPPnPPnPPnPP.",
"......ss.ss.....",
"......ss.ss.....",
"......ss.ss.....",
"......ss.ss.....",
"......ss.ss.....",
"......ss.ss.....",
".....nnn.nnn....",])
_DD2=S([_DD[0].replace('yyyy','.yy.')]+[r if i!=1 else "y....yyyyyy....y" for i,r in enumerate(_DD[1:3],1)]+_DD[3:])
_DD_UP=S([   # the pirouette: arms up over the head, on her toes, one knee out
".....ss..ss.....",
"......yyyy......",
"yyy..yyyyyy..yyy",
"yyyyyyyyyyyyyyyy",
"yyy.ysssssss.yyy",
"....ssEsssEs....",
"....ssEsssEs....",
"....ssssssss....",
".....ssnnss.....",
"......ssss......",
".....nnnnnn.....",
".....nnnnnn.....",
".....nnnnnn.....",
"..PPPPPPPPPPPP..",
".PPnPPnPPnPPnPP.",
"......ss.ss.....",
"......ss..ss....",
"......ss...ss...",
"......ss..ss....",
"......ss.ss.....",
"......ss........",
"......nn........",])
DD=poses(_DD,10,'s',4)
DD.update(idle2=_DD2,up=_DD_UP)
DDPAL={'y':(250,226,110),'s':(250,214,180),'E':(60,120,220),'n':(244,130,180),'P':(255,190,220)}
def dd_idle(f): return DD['idle'] if (f//6)%2==0 else DD['idle2']

# ---- the mech, Claude in the glass dome ----------------------------------------------------------
_MECH=S([
"........kkkkkkkk.........",
".......kccccccccck.......",
"......kcxxxxxxxxcck......",
"......kcOOOOOOOOcck......",
"......kcOOHKOHKOcck......",
"......kcOOOOOOOOcck......",
"....ddddddddddddddddd....",
"...dDDDDDDDDDDDDDDDDDd...",
"dddDDDDDDDDDDDDDDDDDDDddd",
"dDDdDDDDDDDDDDDDDDDDDdDDd",
"dDDdDDDDDDDrrrDDDDDDDdDDd",
"dDDdDDDDDDrrRrrDDDDDDdDDd",
"dDDdDDDDDDrrrrrDDDDDDdDDd",
"dDDdDDDDDDDrrrDDDDDDDdDDd",
"dDDdDDDDDDDDDDDDDDDDDdDDd",
"dDDddDDDDDDDDDDDDDDDddDDd",
"dddd.dDDDDDDDDDDDDDd.dddd",
"yLy...ddddddddddddd...yLy",
"yyy....dDDd...dDDd....yyy",
".......dDDd...dDDd.......",
".......ddd.....ddd.......",
"......dDDd.....dDDd......",
"......dDDd.....dDDd......",
".....dDDDDd...dDDDDd.....",
"....ddddddd...ddddddd....",])
_MECH_STEP=S(_MECH[:20]+[".......dDDd....dDDd......",".......dDDd....dDDd......",
                         "......dDDDDd..dDDDDd......","....dddddddd.dddddddd....",
                         "........................."][:len(_MECH)-20])
MECH={'idle':_MECH,'step':_MECH_STEP}
MECHPAL=dict(DEXPAL,c=(150,220,255),D=(150,156,170),d=(84,88,104),r=(230,40,40),R=(255,170,160),
             y=(250,210,60),L=(255,90,60))
CANNON=hand_at(_MECH,0,GROUND,False,24,17)                          # the right claw, relative to x

# ---- background: the secret lab ----------------------------------------------------------------
_LIGHTS=[]
def _lab(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(12+8*k),int(26+10*k),int(34+10*k)))
    d.rectangle([0,0,W,4],fill=(24,40,48))                         # ceiling pipes
    for x in range(0,W,9): d.line([x,0,x,4],fill=(36,58,66))
    d.line([0,7,W,7],fill=(40,70,80)); d.line([0,8,W,8],fill=(22,40,48))
    rr=random.Random(zlib.crc32(b'dexter-lab'))
    for x0,x1 in ((4,44),(126,181)):                               # computer banks
        d.rectangle([x0,18,x1,GROUND-1],fill=(52,64,80),outline=(30,38,48))
        for x in range(x0+3,x1-5,10):
            d.ellipse([x,22,x+6,28],outline=(150,160,176)); d.ellipse([x+2,24,x+4,26],fill=(30,38,48))   # tape reels
        for x in range(x0+3,x1-2,4):
            for y in (34,38,42):
                _LIGHTS.append((x,y,rr.random()))
                d.point((x,y),fill=(40,48,56))
        d.rectangle([x0+2,47,x1-2,49],fill=(30,38,48))
    d.rectangle([66,12,118,36],fill=(30,38,48),outline=(90,104,120))  # the big monitor
    d.rectangle([68,14,116,34],fill=(12,40,30))
    for y in range(15,34,2): d.line([69,y,115,y],fill=(16,52,38))
    pts=[(69+i*2,24+int(6*math.sin(i*0.7))) for i in range(24)]
    d.line(pts,fill=(80,240,140))
    d.rectangle([84,36,100,40],fill=(40,50,60))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(40,52,60))
register_bg(THEME, lambda v: (v//2+6,v+10,v+14), decor=_lab)

@fx('dex_lights')
def _fx_lights(d,im,e,f):
    """The blinking lights on the computer banks."""
    for x,y,p in _LIGHTS:
        on=(int(p*7)+f//5+x)%3!=0
        if on: d.point((x,y),fill=[(255,70,60),(90,240,120),(250,210,60),(110,180,255)][int(p*4)%4])

@fx('dex_laser')
def _fx_laser(d,im,e,f):
    _,x,y=e; x=int(x)
    d.line([x-8,y,x,y],fill=(255,60,80),width=3); d.line([x-6,y,x,y],fill=(255,220,220))

@fx('dex_lever')
def _fx_lever(d,im,e,f):
    _,x,down=e
    d.rectangle([x-2,GROUND-14,x+2,GROUND-10],fill=(70,80,96))
    ex,ey=(x+5,GROUND-8) if down else (x+5,GROUND-20)
    d.line([x,GROUND-12,ex,ey],fill=(180,180,190)); d.ellipse([ex-1,ey-1,ex+1,ey+1],fill=(230,40,40))

@fx('dex_blast')
def _fx_blast(d,im,e,f):
    """The mech blowing up, t frames old: a fireball of puffs, then a cloud of smoke that thins out."""
    _,x,y,t=e; rr=random.Random(zlib.crc32(b'blast'))
    for j in range(14):
        a=rr.random()*math.tau; dist=rr.random()*(4+t*1.6); r=3+rr.randint(0,4)+min(t,8)//2
        px,py=x+math.cos(a)*dist,y+math.sin(a)*dist*0.7-t*0.6
        if t<6: c=[(255,250,210),(255,210,90),(255,140,40)][min(2,(j+t)//5)]
        elif t<10: c=[(255,140,40),(200,70,30),(90,80,84)][j%3]
        else:
            c=(int(90-(t-10)*3),)*3; r=max(0,r-(t-10)//2)
        if r>0: d.ellipse([px-r,py-r,px+r,py+r],fill=c)

@fx('dex_alarm')
def _fx_alarm(d,im,e,f):
    """The red self-destruct alarm: the room flashes red."""
    _,a=e; im.paste(fade_to(im,(220,20,20),a))

@fx('dex_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('dex_say',txt,y,c,scale,outline))

# ---- the clip ----------------------------------------------------------------------------------
def mech_x(f):
    if f<96: return MX
    if f<144: return MX+((f-96)//12)*14+ez(0,14,((f-96)%12)/6)    # four stomps forward
    return MX+56

def clip_lab(f):
    s=scene(f,THEME); s['under'].append(('dex_lights',))
    cl=actor(DEX[guard_pose(f)],CX,pal=DEXPAL)
    dd=actor(dd_idle(f),VX,flip=True,pal=DDPAL)
    mech=None
    # 1) the title, Dee Dee's line, Claude's
    if 6<=f<24: banner(s,"CLAUDE'S LABORATORY",22,(255,255,255),2,(40,120,90))
    if 24<=f<44:
        shout(s,"OOOH! WHAT DOES THIS BUTTON DO?",(255,170,210))
        dd['spr']=DD['up'] if (f//4)%2 else dd_idle(f)
    if 44<=f<62:
        shout(s,"DEE DEE! GET OUT OF MY LABORATORY!",(255,220,120))
        cl['spr']=DEX['armsup']; cl['x']=CX+((f//2)%2)
    # 2) the lever, the mech drops around Claude
    s['under'].append(('dex_lever',8,62<=f<72))
    if 62<=f<72: cl.update(spr=DEX['punch'],x=16,flip=True)
    if 72<=f<80: cl.update(x=ez(16,MX,(f-72)/8))
    if 74<=f<84:
        mech=actor(MECH['idle'],MX,int(ez(-6,GROUND,(f-74)/8)),pal=MECHPAL)
        shout(s,"MECH, ACTIVATE!",(255,220,120))
    if f>=82: cl['vis']=False
    if f==82: s['shake']=rshake(3); s['fx'].append(('dust',MX-12,GROUND-1)); s['fx'].append(('dust',MX+12,GROUND-1))
    # 3) it stomps forward firing; Dee Dee pirouettes through every shot
    if 84<=f<196:
        x=mech_x(f); step=96<=f<144 and ((f-96)%12)<6
        mech=actor(MECH['step'] if step else MECH['idle'],x,GROUND,pal=MECHPAL)
        if 96<=f<144 and (f-96)%12==6: s['shake']=rshake(); s['fx'].append(('dust',x+8,GROUND-1))
    for k,f0 in enumerate((100,118,136)):                          # three shots
        if f0<=f<f0+10:
            x0=mech_x(f0)+CANNON[0]; t=(f-f0)/10
            s['fx'].append(('dex_laser',lerp(x0,190,t),CANNON[1]-1))
        if f==f0+6: s['fx'].append(('spark',182,CANNON[1]-1,4))
        if f0+2<=f<f0+10:
            dd.update(spr=DD['up'],flip=(f//2)%2==0,y=GROUND-int(12*math.sin(math.pi*(f-f0-2)/8)))
    if 104<=f<118: shout(s,"LA LA LA!",(255,170,210))
    # 4) she twirls up to the mech and presses the button
    BX=mech_x(150)+16
    if 150<=f<162:
        t=(f-150)/12; dd.update(spr=DD['up'],flip=(f//2)%2==0,x=lerp(VX,BX,t),y=GROUND-int(10*math.sin(math.pi*t)))
    if 162<=f<180: dd.update(spr=DD['attack'] if f<170 else dd_idle(f),x=BX)
    if 160<=f<176: shout(s,"OOOH! WHAT DOES THIS DO?",(255,170,210))
    if f==166: s['fx'].append(('spark',*hand_at(_MECH,mech_x(f),GROUND,False,12,11),3))
    # 5) SELF DESTRUCT
    if 170<=f<196:
        red=(f//3)%2==0
        if red: s['fx'].append(('dex_alarm',0.25))
        if mech: mech['pal']=dict(MECHPAL,r=(255,240,120) if red else (230,40,40))
        if f>=176: shout(s,"SELF DESTRUCT",(255,80,70),y=2)
    if 180<=f<192:
        t=(f-180)/12; dd.update(spr=DD['up'],flip=(f//2)%2==0,x=lerp(BX,VX,t),y=GROUND-int(14*math.sin(math.pi*t)))
    if 192<=f<196: dd['spr']=DD['up']
    EX=mech_x(190)
    if f==196:
        s['flash']=0.9; s['fc']=(EX,GROUND-14); s['flashc']=(255,240,200); s['shake']=rshake(3)
    if 196<=f<222: s['fx'].append(('dex_blast',EX,GROUND-14,f-196))
    if 196<=f<208:
        t=f-196
        s['shake']=rshake(2 if t<6 else 1)
        if t<8: banner(s,"KABOOM!",4,(255,220,80),3,(170,40,20))
        rr=random.Random(zlib.crc32(b'debris')+t)
        for j in range(10):
            a=j*0.63; s['fx'].append(('shard',EX+math.cos(a)*t*5,GROUND-14+math.sin(a)*t*3+t*t*0.2,(150,156,170)))
    # 6) in the smoke: Claude, black with soot
    if f>=196:
        soot=1 if f<236 else max(0,1-(f-236)/24)
        x=EX if f<244 else ez(EX,CX,(f-244)/24)
        pose='hurt' if f<204 else ('armsup' if 212<=f<230 else guard_pose(f))
        cl.update(vis=True,spr=DEX[pose],x=x,pal=sooty(soot),flip=244<=f<268)
        if 212<=f<230: cl['x']=x+((f//2)%2)
        if 196<=f<240:
            for j in range(4):
                k=((f-196)*0.06+j*0.25)%1
                s['fx'].append(('smoke',x-2+j*2+math.sin(k*6+j)*2,GROUND-14-k*16,1+int(k*3),(70,70,76)))
    if 212<=f<232: banner(s,"DEE DEEEE!",8,(255,220,120),2,(120,40,20))
    if 230<=f<244:
        shout(s,"BYE BYE!",(255,170,210))
        dd.update(spr=DD['up'] if (f//4)%2 else dd_idle(f),flip=True)
    s['actors']=[dd]+([mech] if mech else [])+[cl]
    return s

CLIPS = [clip('lab', N_, clip_lab)]
