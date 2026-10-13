"""Deadpool: Claude as Deadpool vs Wolverine, in the Void (Deadpool & Wolverine).
SNIKT. Katanas vs claws; an arm pops off and a tiny one grows back. Then Deadpool turns to us, in his
yellow boxes: A NOTCH? SERIOUSLY? — and knocks on the top edge of the panel. Close-up: MAXIMUM EFFORT.
He offers a chimichanga; Wolverine takes it and leaves: BUB.
notchverse: a TVA door opens in the Void and Deadpool goes visiting the app's other themes: steals
Madara's gunbai in the Hidden Leaf (and leaves with his pants on fire), tells the Cyclops his name is
NOBODY and gets thrown out, stands in front of Cell's Kamehameha (close-up: OH NO.) — and comes home
charred, gunbai in hand: WORTH IT.
webcam: he notices the MacBook camera above the panel (WAIT. IS THAT A CAMERA?), presses his face to
the glass (fisheye close-up: HI MOM!), pushes the panel's edges (LET ME OUT!), gets bored watching
Claude think (STILL THINKING?) and falls asleep — the panel starts closing on him: HEY! NOT YET!
review: Claude's pull request on Etendo_schema_forge drops in as a
terminal; Deadpool reads the diff out loud, judges the Etendo rebrand in close-up (the yellow logo turns
the lime tile with the black < >: NEW LOGO. HUH? / EDGY. I DIG IT.), stamps it LGTM and merges it with a katana."""
from engine import *
# Crossover (an exception to one-theme-per-file): notchverse visits nrt, odyssey and dbz and uses their
# backgrounds, sprites and fx (nrt_clouds, nrt_fireball, nrt_gunbai_back, od_fire, od_cyclops, dbzc_ball);
# review uses the etendo theme's logos. Changing any of those changes these clips too: rebuild them
# (ONLY=deadpool) and check their sheets.
from themes.nrt import MADARA, MADARA_AURA      # notchverse: the other themes' worlds and casts
from themes.dbz import CE, CELL_KI
import themes.odyssey                             # registers the cave, the fire and the Cyclops
from themes.etendo import logo as etendo_logo, SZ as ETENDO_SZ, NAVY as ETENDO_NAVY, INK as ETENDO_INK   # review: the rebrand's logos

THEME = 'deadpool'
N_ = 376

RED, RED_D = (196,30,40), (128,16,26)
BOX, INK = (250,220,70), (20,16,16)
# Deadpool: red suit, black patches round white eyes, katana hilts over the shoulders
DPAL = {'r':RED, 'R':RED_D, 'x':(18,16,18), 'e':(250,250,250), 'h':(150,150,160), '9':(40,36,40), '7':(70,58,50), '8':(220,190,90)}
# Wolverine (Deadpool & Wolverine): yellow suit, blue, the mask's black wings
WPAL = {'y':(236,196,40), 'b':(44,74,160), 'P':(226,182,140), 'W':(250,250,250)}

EYES = {                     # which of the 2x2 eye pixels are white, per expression (top row, bottom row)
    'normal':  ('11','11'),
    'happy':   ('11','00'),
    'angry':   ('01','11'),  # the inner top pixel goes dark: a frown (mirrored for the other eye)
    'squint':  ('00','11'),
}

HILTS=["9.9...",".h.h..","..h.h."]                                  # two katana hilts over the back shoulder

def _deadpool(spr, mood='normal'):
    g=[list(r) for r in overlay(spr,HILTS,-2,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    ks=sorted((x,y) for y,row in enumerate(g) for x,c in enumerate(row) if c=='K')
    for y,row in enumerate(g):
        for x,c in enumerate(row):
            if c=='O': g[y][x]='R' if x==l else 'r'                     # the back of the mask in shadow
            elif c=='o': g[y][x]='R'
    def put(x,y,c,over='rR'):
        if 0<=y<len(g) and 0<=x<len(g[0]) and g[y][x] in over: g[y][x]=c
    for y in (top+5,top+6): put(l,y,'x'); put(l+1,y,'x')               # the black side panel
    for x in range(l,r+1): put(x,top+7,'7')                            # the belt...
    put((l+r)//2+1,top+7,'8'); put(l+1,top+8,'7')                       # ...its round buckle, a pouch
    if ks:
        cols=sorted({x for x,_ in ks}); y0=min(y for _,y in ks)
        tp,bt=EYES[mood]
        for i,cx in enumerate(cols):                                    # two patches, a red bridge between
            for dy in (-1,0,1,2):
                put(cx,y0+dy,'x'); put(cx-1,y0+dy,'x')
            if i==0: put(cx-2,y0-1,'x'); put(cx-2,y0,'x')                # the back one flares out at the top
            else: put(cx+1,y0-1,'x')
            t=tp if i==0 else tp[::-1]
            g[y0][cx]='e' if t[0]=='1' else 'x'
            g[y0+1][cx]='e' if bt[0]=='1' else 'x'
    return S([''.join(r) for r in g])
DP={mood:variant(lambda s,m=mood: _deadpool(s,m)) for mood in EYES}

def _no_arm(spr):
    """The guard pose with the raised arm gone (it popped off)."""
    g=[list(r) for r in spr]; w=len(g[0])
    for y in range(len(g)):
        for x in range(w-4,w):
            if g[y][x]=='R': g[y][x]='.'
    return S([''.join(r) for r in g])
ARMLESS={mood:_no_arm(DP[mood]['guard']) for mood in EYES}

# The "Bye Bye Bye" moves (the dance clip only): Claude's body (the guard's head, torso, legs) with the
# arms redrawn per move, painted like the others. Each move's pixels are listed in its own function.
_BODY=[ '...OOOOOOOO', '...OOOOOOOO', '...OOOOKOOK', '...OOOOKOOK', '...OOOOOOOO', '...OOOOOOOO',
        '...OOOOOOOO', '...OOOOOOOO', '...oOOOOOOo', '..oo.....oo', '.oo.......oo']
def _dance_pose(arms, lean=None, knees=None):
    """The body with `arms` ('o' cells, (x,y)); `lean` = (last row, columns) moves rows 0..last that many
    columns left (he leans back one pixel)."""
    g=[list(r.ljust(16,'.')) for r in _BODY]
    if lean:
        last,dx=lean
        for y in range(0,last+1):
            row=g[y]; g[y]=['.']*16
            for x,c in enumerate(row):
                if c!='.': g[y][x+dx]=c
    if knees:                                                          # the legs (rows 9, 10) redrawn
        for y,row in zip((9,10),knees): g[y]=list(row.ljust(16,'.'))
    for x,y in arms: g[y][x]='o'
    return S([''.join(r) for r in g])

def _seg(x0,y0,x1,y1):
    """The cells of a straight forearm from (x0,y0) to (x1,y1), one per column."""
    return [(x, round(y0+(x-x0)*(y1-y0)/(x1-x0))) for x in range(x0,x1+1,1 if x1>x0 else -1)]
_HAND_HIP=[(2,5),(1,6),(2,7)]                                       # the left arm: elbow out, fist on the hip
DANCE_POSE={
    # 'bye': the right arm straight out to the side, palm out (its hand a pixel up); left fist on the hip
    'bye': _dance_pose(_HAND_HIP+[(x,4) for x in range(11,16)]+[(14,3),(15,3)]),
    # 'push': both arms pushing out to the right at chest height; the body leans a pixel left
    'push': _dance_pose([(x,4) for x in range(10,16)]+[(x,6) for x in range(10,16)]+[(14,3),(15,3),(14,7),(15,7)],
                        lean=(7,-1)),
    # 'cross': the forearms crossed in an X in front of the chest, the elbows out
    'cross': _dance_pose(_seg(1,3,14,9)+_seg(14,3,1,9)),
    # 'hip': one hand on the hip, the other arm up and bent; the knees dip a pixel out
    'hip': _dance_pose(_HAND_HIP+[(11,4),(12,4),(12,3),(13,3),(12,2),(13,2),(12,1),(13,1),(12,0),(13,0)],
                       knees=('.oo.....oo','oo.......oo')),
}
for _mood in EYES:
    DP[_mood].update({k:_deadpool(v,_mood) for k,v in DANCE_POSE.items()})

WOLV=poses(S([
"..bb.......bb...","..bbb.....bbb...","...bbyyyyybb....","....ykWkWky.....","....yPPPPPy.....",
".....PPPPP......","......PkP.......","...bbyyyyybb....","..bbbyyyyybbb...","..PbyyyyyyybP...",
"..PyyybbbyyyP...","..P.yyybyyy.P...","....yyyyyyy.....","....bbbbbbb.....","....bb...bb.....",
"....bb...bb.....","....bb...bb.....","...kkk...kkk....",]),9,'P',4)

def _void(d):
    """The Void: dusty orange sky, dunes, a giant half-buried skull and wreckage."""
    for y in range(0,GROUND):
        v=int(34+30*y/GROUND); d.line([0,y,W,y],fill=(v+24,v,v//2))
    d.polygon([(0,GROUND),(0,48),(30,44),(70,50),(110,42),(150,48),(185,44),(185,GROUND)],fill=(92,62,40))
    d.ellipse([88,22,124,52],fill=(120,100,80)); d.rectangle([94,40,118,50],fill=(120,100,80))   # the skull
    d.ellipse([96,30,104,38],fill=(50,34,24)); d.ellipse([108,30,116,38],fill=(50,34,24))
    for x in range(98,116,4): d.rectangle([x,46,x+2,50],fill=(80,64,50))
    d.polygon([(150,48),(156,30),(160,31),(156,48)],fill=(70,60,56))                             # wreckage
    d.line([20,44,26,34],fill=(80,70,62)); d.line([26,34,34,36],fill=(80,70,62))
register_bg(THEME, lambda v: (v+20,v*2//3+10,v//3+6), decor=_void)

@fx('dp_box')
def _fx_box(d,im,e,f):
    """Deadpool's yellow caption boxes (one or more lines), centred at x."""
    _,lines,cx,y=e
    lines=[lines] if isinstance(lines,str) else lines
    w=max(len(l) for l in lines)*4+5; h=len(lines)*7+3; x=int(cx-w/2)
    x=max(1,min(W-w-1,x))
    d.rectangle([x,y,x+w,y+h],fill=BOX,outline=INK)
    for i,l in enumerate(lines): text(d,l,x+3,y+2+i*7,INK,shadow=None)

@fx('dp_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(250,250,250),ink=INK)                     # the engine's bubble (engine/people.py)

@fx('dp_katana')
def _fx_katana(d,im,e,f):
    _,hx,hy,a=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.line([hx-c*2,hy-s*2,hx,hy],fill=(40,40,44))
    d.line([hx+c,hy+s,hx+13*c,hy+13*s],fill=(214,220,236)); d.point((hx+13*c,hy+13*s),fill=(255,255,255))

@fx('dp_claws')
def _fx_claws(d,im,e,f):
    """Three adamantium claws out of the fist (pointing left: Wolverine faces left)."""
    _,x,y,L=e
    for k in (-2,0,2): d.line([x,y+k,x-L,y+k-1],fill=(200,206,220))

@fx('dp_arm')
def _fx_arm(d,im,e,f):
    """The arm that popped off, tumbling."""
    _,x,y,k=e; a=k*0.8; c,s=math.cos(a)*3,math.sin(a)*3
    d.line([x-c,y-s,x+c,y+s],fill=RED_D); d.point((x+c,y+s),fill=RED)

@fx('dp_tinyarm')
def _fx_tinyarm(d,im,e,f):
    _,x,y=e; d.point((x,y),fill=RED_D); d.point((x+1,y-1),fill=RED)

@fx('dp_chimi')
def _fx_chimi(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x,y-1,x+5,y+1],fill=(214,164,90)); d.line([x+1,y-1,x+4,y-1],fill=(240,200,130))

@fx('dp_dust')
def _fx_dust(d,im,e,f):
    """Dust falling from the top edge of the panel where Deadpool knocked."""
    _,x,k=e; rr=random.Random(515)
    for i in range(14):
        px=x+rr.uniform(-14,14); py=k*rr.uniform(0.8,1.6)+rr.uniform(0,3)
        if py<GROUND: d.point((int(px),int(py)),fill=(200,180,150) if i%2 else (150,130,110))

GRIP = {'punch':(16,5), 'dash':(16,5), 'charge':(15,5)}

def closeup_effort(t,f):
    """Primer plano: the mask; the eyes narrow; MAXIMUM / EFFORT."""
    im=Image.new('RGB',(W,H),(30,18,14)); d=ImageDraw.Draw(im)
    for i in range(0,64,4): d.line([0,i,W,i],fill=(40,24,18))
    d.rectangle([22,6,86,64],fill=RED); d.rectangle([80,6,86,64],fill=RED_D)
    d.line([54,6,54,64],fill=RED_D)                                           # the mask's seam
    sq=ease((t-0.25)/0.3)                                                     # the eyes narrow
    for x0,flip in ((30,False),(58,True)):
        d.polygon([(x0-2,20),(x0+22,20),(x0+20,42),(x0,42)],fill=(18,16,18))
        top=24+int(9*sq); bot=37
        if flip: d.polygon([(x0+3,top+3),(x0+17,top),(x0+17,bot),(x0+3,bot)],fill=(250,250,250))
        else:    d.polygon([(x0+3,top),(x0+17,top+3),(x0+17,bot),(x0+3,bot)],fill=(250,250,250))
    for j,w in enumerate(("MAXIMUM","EFFORT")):
        if t>=0.45+j*0.15: FX['big'](d,im,('big',w,14+j*18,(250,250,250) if j==0 else BOX,138),f)
    if t<0.06: zoom_lines(d)
    return im

WX=150

def clip_bub(f):
    """Text holds follow ~1 s + 0.3 s per word (min 1.5 s at 20 fps), so every line can be read."""
    s=scene(f,THEME)
    x,y,pose,mood,flip=30,GROUND,guard_pose(f),'normal',False
    wx,wpose,claws=None,'idle',0
    armless=False
    # 1) Wolverine walks in; SNIKT
    if 14<=f<338: wx=ez(210,WX,(f-14)/20) if f<34 else WX
    if 30<=f<54: callout(s,"SNIKT",c=(236,236,244)); mood='angry'
    if f>=32: claws=min(8,(f-32)*2)
    # 2) the fight; the arm pops off, a tiny one grows back
    if 40<=f<48: pose,x,mood='dash',ez(30,124,(f-40)/8),'angry'
    if 48<=f<66:
        x,mood=124,'angry'; k=(f-48)%8; pose='punch' if k<4 else 'guard'; wpose='attack' if 3<=k<7 else 'idle'
        if k in (2,3): s['fx'].append(('spark',136,GROUND-7,3+k))
    if 66<=f<72: x,pose,mood=124,'hurt','normal'
    if 66<=f<86: callout(s,"POP!",c=BOX)
    if 66<=f<110:
        k=min(14,f-66); p=k/14
        s['fx'].append(('dp_arm',lerp(128,70,p),GROUND-8-18*math.sin(p*math.pi) if f<80 else GROUND-2,k))
    if 72<=f<110:
        x,armless,mood=124,True,'squint'
        s['fx'].append(('dp_tinyarm',127,GROUND-7))
        if 76<=f<106: s['fx'].append(('dp_box','OH COME ON.',x,4))                       # 1.5 s
    if 106<=f<110: s['fx'].append(('twinkle',128,GROUND-8,2))
    # 3) the fourth wall
    if 110<=f<118: pose,x,flip=guard_pose(f),ez(124,70,(f-110)/8),True
    if 118<=f<228: x,mood=70,'happy'
    if 118<=f<158: s['fx'].append(('dp_box',["A NOTCH?","SERIOUSLY?"],x,4))                 # 2 s
    if 158<=f<168:
        p=(f-158)/10; pose='armsup'; y=GROUND-int(40*math.sin(p*math.pi)); mood='angry'
        if 162<=f<166: s['shake']=rshake(2); s['fx'].append(('spark',70,1,3))
    if 162<=f<182: s['fx'].append(('dp_dust',70,f-162))
    if 168<=f<228: s['fx'].append(('dp_box',["I AM LITERALLY","CLAUDE. IN A NOTCH."],x,4))   # 3 s
    if 118<=f<228 and wx is not None: s['fx'].append(('dp_bubble','...',WX,12))
    # 4) close-up
    if 228<=f<268: s['image']=closeup_effort((f-228)/40,f); return s
    # 5) two more blows, the chimichanga, BUB.
    if 268<=f<276: pose,x,mood='dash',ez(70,124,(f-268)/8),'angry'
    for c0 in (278,284):
        if c0<=f<c0+4:
            pose,x,wpose='punch',124,'attack'
            if f<c0+2: s['fx'].append(('spark',136,GROUND-7,4))
    if 276<=f<290 and pose not in ('punch','dash'): x,pose=124,guard_pose(f)
    chimi=None
    if 290<=f<322:
        x,pose,mood=124,'punch','happy'
        hx,hy=hand_at(DP[mood]['punch'],x,GROUND,False,16,5,h=11); chimi=(hx,hy-1)
        if f<320: s['fx'].append(('dp_box','CHIMICHANGA?',x,4))                           # 1.5 s
    if 322<=f<352:
        wx=ez(WX,215,(f-322)/24); wpose='idle'; chimi=(wx-10,GROUND-10)
        s['fx'].append(('dp_bubble','BUB.',wx,12))                                # 1.5 s
        x,pose,mood=124,guard_pose(f),'squint'
    if chimi: s['fx'].append(('dp_chimi',*chimi))
    # 6) wave, back to the neutral pose
    if 352<=f<364: x,flip,pose,mood=ez(124,30,(f-352)/12),True,guard_pose(f),'happy'
    if 364<=f<370: x,pose,mood,flip=30,'armsup','happy',False
    if f>=370: x,flip=30,False
    acts=[]
    if wx is not None and wx<W+10:
        acts.append(actor(WOLV[wpose],wx,flip=True,pal=WPAL))
        if claws: s['fx'].append(('dp_claws',wx-8-(4 if wpose=='attack' else 0),GROUND-9,claws))
    spr=ARMLESS[mood] if armless else DP[mood][pose]
    acts.append(actor(spr,x,y,flip=flip,pal=DPAL))
    if pose in GRIP and not armless and chimi is None:
        hx,hy=hand_at(DP[mood][pose],x,int(y),flip,*GRIP[pose],h=11)
        s['fx'].append(('dp_katana',hx,hy,180 if flip else 0))
    s['actors']=acts
    return s

# ==== notchverse ======================================================================================
TVA=(255,140,40)

@fx('dp_door')
def _fx_door(d,im,e,f):
    """A TVA time door: a glowing orange frame, the portal rippling inside (k 0..1: how open)."""
    _,x,k=e
    if k<=0: return
    x=int(x); h=int(28*k); top=GROUND-h
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).rectangle([x-10,top-4,x+10,GROUND+2],fill=120)
    im.paste(TVA,(0,0),g.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    d.rectangle([x-7,top,x+7,GROUND],fill=(255,190,90),outline=(255,240,200))
    for j in range(4):
        yy=top+((f*2+j*7)%max(1,h)); d.line([x-6,yy,x+6,yy],fill=(255,236,170))

@fx('dp_burn')
def _fx_burn(d,im,e,f):
    """Flames on the seat of his pants."""
    _,x,y=e; rr=random.Random(f)
    for _ in range(4): d.point((int(x)+rr.randint(-2,2),int(y)-rr.randint(0,4)),fill=rr.choice([(255,200,60),(255,120,30)]))

def closeup_ohno(t,f):
    """Primer plano: the mask lit blue from the right as the Kamehameha comes — OH NO."""
    im=Image.new('RGB',(W,H),(20,24,40)); d=ImageDraw.Draw(im)
    k=ease(t)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([W-40-100*k,-40,W+80,H+40],fill=int(60+170*k))
    im.paste(CELL_KI[0],(0,0),g.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    d.rectangle([22,6,86,64],fill=RED); d.rectangle([80,6,86,64],fill=RED_D); d.line([54,6,54,64],fill=RED_D)
    wide=ease((t-0.2)/0.2)
    for x0 in (30,58):                                              # the eyes go wide
        d.polygon([(x0-2,18),(x0+22,18),(x0+20,44),(x0,44)],fill=(18,16,18))
        r=int(6+4*wide); d.ellipse([x0+10-r,31-r,x0+10+r,31+r],fill=(250,250,250))
    if t>=0.15: FX['dp_box'](d,im,('dp_box',"OH NO.",140,26),f)
    if t<0.06: zoom_lines(d)
    if t>0.85: im=fade_to(im,(255,255,255),(t-0.85)/0.15)
    return im

DOOR_X=60
def clip_notchverse(f):
    kind=THEME
    if 70<=f<130: kind='nrt'
    elif 130<=f<196: kind='odyssey'
    elif 196<=f<280: kind='dbz'
    s=scene(f,kind)
    x,y,pose,mood,flip,show,tint=30,GROUND,guard_pose(f),'normal',False,True,None
    acts=[]; gunbai=None
    # 1) the Void: the door opens
    if 14<=f<70: s['under'].append(('dp_door',DOOR_X,min(1,(f-14)/8)))
    if 14<=f<70: s['fx'].append(('dp_box',["THIS APP HAS","50 OTHER THEMES."],30 if f<58 else x,4)); mood='happy'
    if 58<=f<70: x,pose=ez(30,DOOR_X,(f-58)/10),guard_pose(f)
    if 68<=f<70: show=False
    # 2) the Hidden Leaf: the gunbai, the Katon
    if kind=='nrt':
        s['under'].append(('nrt_clouds',)); s['under'].append(('dp_door',30,1 if f<76 or f>=120 else 0))
        mx,mpose,aura=152,'idle',None
        x=30
        if 74<=f<106: s['fx'].append(('dp_box',"OOH. NINJAS.",60,4)); mood='happy'
        if 92<=f<100: x,pose=ez(30,138,(f-92)/8),'dash'
        if 100<=f<106: x,pose,gunbai=138,'armsup',(140,GROUND-16)
        if 104<=f<126:
            mpose,aura='attack',(MADARA_AURA,1+(f%2)); mood='squint'
            x,flip,pose=ez(138,30,(f-106)/14),True,'dash'; gunbai=(x+2,GROUND-14)
            fx_=lerp(140,x+14,(f-106)/14); s['fx'].append(('nrt_fireball',fx_,GROUND-12,9))
            if f>=114: s['fx'].append(('dp_burn',x+3,GROUND-4))
            callout(s,"KATON!",c=(255,170,70))
        if f>=126: show=False
        acts.append(actor(MADARA[mpose],mx,flip=True,aura=aura))
        if gunbai is None: s['under'].append(('nrt_gunbai_back',mx,GROUND))
    # 3) the Cyclops' cave: NOBODY.
    if kind=='odyssey':
        s['under'].append(('od_fire',92)); s['under'].append(('dp_door',30,1))
        cpose,ck='stand',0.0
        x=30; gunbai=(x-6,GROUND-14)
        if 134<=f<172: s['fx'].append(('big',"WHO ARE YOU?",3,(236,214,180)))
        if 168<=f<198: s['fx'].append(('dp_box',"NOBODY.",x+10,18)); mood='happy'
        if 172<=f<196:
            cpose='reach'; ck=min(1,(f-172)/10)
            if f>=184: show=False                                  # in the fist...
            if 188<=f<196: ck=1-(f-188)/8                           # ...and thrown at the door
        s['under'].append(('od_cyclops',148,cpose,'open',ck))
        if f>=184: gunbai=None
    # 4) the Cell Games: KAMEHAMEHA; close-up: OH NO.
    if kind=='dbz':
        s['under'].append(('dp_door',30,1 if f>=266 else 0))
        x=60; gunbai=(x-6,GROUND-14); cpose='guard'
        if 200<=f<206: show=f>=202
        if 200<=f<230:
            cpose='charge'; s['fx'].append(('dbzc_ball',138,GROUND-10,2+(f-200)//6,CELL_KI))
            s['fx'].append(('big',"KAMEHAMEHA",3,CELL_KI[0]))
        if 230<=f<268: s['image']=closeup_ohno((f-230)/38,f); return s
        if 268<=f<280:
            cpose='charge'; s['fx'].append(('beam',0,136,GROUND-9,CELL_KI)); s['shake']=rshake(2)
            x,pose,tint=ez(60,30,(f-268)/7),'hurt',(40,30,30)
            if f>=276: show=False
        acts.append(actor(CE[cpose],150,flip=True))
    # 5) home: charred, gunbai in hand
    if 280<=f<366:
        s['under'].append(('dp_door',DOOR_X,1 if f<344 else max(0,1-(f-344)/8)))
        if 280<=f<296: x,pose,tint=ez(DOOR_X,44,(f-280)/10),'hurt',(40,30,30); s['fx'].append(('smoke',x+random.randint(-4,4),GROUND-12-random.randint(0,6),2,(80,80,86)))
        elif f<344: x,mood=44,'happy'
        if 296<=f<334: pose='armsup'; gunbai=(x+2,GROUND-20); s['fx'].append(('dp_box',"WORTH IT.",x+20,4))
        if 334<=f<344: p=(f-334)/10; s['fx'].append(('gunbai',lerp(x+2,DOOR_X,p),GROUND-20+10*math.sin(p*math.pi)))
        if 344<=f<354: x,pose=ez(44,30,(f-344)/10),guard_pose(f)
        if f>=354: x=30
    if gunbai: s['fx'].append(('gunbai',*gunbai))
    if show:
        acts.append(actor(DP[mood][pose],x,y,flip=flip,pal=DPAL,tint=tint))
        if pose in GRIP and tint is None and not gunbai:
            hx,hy=hand_at(DP[mood][pose],x,int(y),flip,*GRIP[pose],h=11)
            s['fx'].append(('dp_katana',hx,hy,180 if flip else 0))
    s['actors']=acts
    return s

# ==== webcam ==========================================================================================
def fisheye(src,k=0.55):
    """Barrel distortion round the centre: the middle swells, the edges squeeze (a webcam lens)."""
    sp=src.load(); out=Image.new('RGB',(W,H)); op=out.load(); cx,cy=W/2,H/2; R=W/2
    for y in range(H):
        for x in range(W):
            dx,dy=(x-cx)/R,(y-cy)/R; r=math.hypot(dx,dy); m=(1-k)+k*r*r
            sx,sy=int(cx+dx*m*R),int(cy+dy*m*R)
            op[x,y]=sp[min(W-1,max(0,sx)),min(H-1,max(0,sy))]
    return out

def closeup_webcam(t,f):
    """Primer plano, from inside the camera: his mask squashed on the glass, a waving glove — HI MOM!"""
    im=Image.new('RGB',(W,H),(60,40,30)); d=ImageDraw.Draw(im)
    d.rectangle([40,0,146,H],fill=RED); d.rectangle([40,0,48,H],fill=RED_D); d.line([93,0,93,H],fill=RED_D)
    for x0 in (56,100):
        d.polygon([(x0-6,10),(x0+30,10),(x0+28,40),(x0-4,40)],fill=(18,16,18))
        d.ellipse([x0+2,16,x0+22,34],fill=(250,250,250))
    d.ellipse([84,44,102,56],fill=(220,40,50))                      # the nose, squashed flat
    wave=int(6*math.sin(f*0.6))
    d.rectangle([146+wave,14,164+wave,36],fill=RED_D,outline=(18,16,18))   # the glove, waving
    for j in range(4): d.rectangle([146+wave+j*5,6,149+wave+j*5,16],fill=RED_D,outline=(18,16,18))
    for j in range(3): d.line([20+j*6,10,30+j*6,50],fill=(150,130,120))   # smudges on the glass
    im=fisheye(im,0.45); d=ImageDraw.Draw(im)
    for r in range(6):                                              # the lens vignette
        d.rounded_rectangle([r,r,W-1-r,H-1-r],radius=26,outline=tuple(int(v*(r/6)) for v in (20,20,24)))
    if (f//6)%2: d.ellipse([6,6,10,10],fill=(240,30,40))
    text(d,"REC",13,6,(240,240,240))
    if t>=0.3: FX['dp_box'](d,im,('dp_box',"HI MOM!",150,46),f)
    if t<0.05: im=fade_to(im,(255,255,255),0.8)
    return im

@fx('dp_edge')
def _fx_edge(d,im,e,f):
    """The panel's glass edge on one side, bulging out where he pushes (k 0..1)."""
    _,side,k,y0=e; x0=2 if side<0 else W-3
    pts=[(x0+side*int(2*k*math.exp(-((y-y0)/7)**2)),y) for y in range(0,H)]
    d.line(pts,fill=(220,230,255)); d.line([(px-side,py) for px,py in pts],fill=(120,130,160))
    if k>0.5:
        for j in (-6,0,6): d.line([x0-side*3,y0+j,x0-side*6,y0+j+(j//3)],fill=(220,230,255))

@fx('dp_term')
def _fx_term(d,im,e,f):
    """A little terminal hanging in the Void: Claude, THINKING..."""
    _,a=e
    if a<=0: return
    x0,y0,x1,y1=120,16,180,40
    d.rectangle([x0,y0,x1,y1],fill=(16,14,18),outline=(90,90,100))
    d.line([x0,y0+5,x1,y0+5],fill=(60,60,70))
    for c,cx in (((240,90,80),x0+3),((240,200,80),x0+6),((110,200,90),x0+9)): d.point((cx,y0+2),fill=c)
    text(d,"THINKING"+"."*((f//6)%4),x0+3,y0+8,(217,119,87),shadow=None)
    rr=random.Random(f//4)
    for j in range(3):
        d.line([x0+3,y0+16+j*4,x0+3+rr.randint(10,50),y0+16+j*4],fill=(90,110,90))

@fx('dp_bars')
def _fx_bars(d,im,e,f):
    """The panel closing: it shrinks up into the notch, its bottom edge rising (k 0..1)."""
    _,k=e; h=int(H*k)
    if h>0: d.rectangle([0,H-h,W,H],fill=(0,0,0)); d.line([0,H-h,W,H-h],fill=(70,70,80))

@fx('dp_z')
def _fx_z(d,im,e,f):
    _,x,y=e
    for j in range(3):
        ph=((f+j*10)%30)/30; text(d,"Z",int(x+ph*8),int(y-ph*12),(240,240,250) if ph<0.7 else (150,150,160))

def clip_webcam(f):
    s=scene(f,THEME)
    x,y,pose,mood,flip=30,GROUND,guard_pose(f),'normal',False
    # 1) WAIT. IS THAT A CAMERA?
    if 16<=f<66: s['fx'].append(('dp_box',["WAIT.","IS THAT A CAMERA?"],60,20)); mood='squint'
    if 30<=f<66: pose='armsup'
    # 2) up to the top edge, face to the glass
    if 66<=f<80:
        p=(f-66)/14; x,pose,mood=ez(30,92,p),'armsup','happy'; y=int(lerp(GROUND,16,math.sin(p*math.pi/2)))
    if 80<=f<140: s['image']=closeup_webcam((f-80)/60,f); return s
    if 140<=f<150: p=(f-140)/10; x,y,pose=92,int(lerp(16,GROUND,p*p)),'hurt'
    # 3) LET ME OUT!: the edges
    if 150<=f<214: s['fx'].append(('dp_box',"LET ME OUT!",92,4)); mood='angry'
    if 150<=f<160: x,flip,pose=ez(92,12,(f-150)/10),True,'dash'
    if 160<=f<180:
        x,flip,pose=12,True,'punch' if (f//4)%2 else 'guard'
        s['fx'].append(('dp_edge',-1,0.5+0.5*((f//4)%2),GROUND-8))
    if 180<=f<192: x,pose=ez(12,172,(f-180)/12),'dash'
    if 192<=f<214:
        x,pose=172,'punch' if (f//4)%2 else 'guard'
        s['fx'].append(('dp_edge',1,0.5+0.5*((f//4)%2),GROUND-8))
    # 4) waiting on Claude
    if 214<=f<226: x,flip,pose=ez(172,92,(f-214)/12),True,guard_pose(f)
    if 214<=f<336: s['under'].append(('dp_term',1))
    if 226<=f<318: x,mood=92,'squint'
    if 226<=f<276: s['fx'].append(('dp_box',["WHAT IS CLAUDE","EVEN DOING?"],60,4))
    if 276<=f<308: s['fx'].append(('dp_box',"STILL THINKING?",60,4))
    # 5) asleep; the panel starts to close on him
    if 300<=f<322: mood='happy'; s['fx'].append(('dp_z',x+4,GROUND-16))
    bars=0
    if 306<=f<322: bars=min(0.45,(f-306)/16*0.45)
    if 322<=f<336: bars=max(0,0.45-(f-324)/12*0.45)
    if bars: s['fx'].append(('dp_bars',bars))
    if 320<=f<360: s['fx'].append(('dp_box',"HEY! NOT YET!",80,4)); mood='angry'
    if 320<=f<330: x,pose=92,'armsup'                               # stamping it back down
    if 330<=f<360: x=92
    if 360<=f<372: x,flip,pose,mood=ez(92,30,(f-360)/12),True,guard_pose(f),'normal'
    if f>=372: x,flip=30,False
    if bars: y=min(y,H-int(H*bars)-1)                              # he rides up on the rising edge
    acts=[actor(DP[mood][pose],x,y,flip=flip,pal=DPAL)]
    if pose in GRIP:
        hx,hy=hand_at(DP[mood][pose],x,int(y),flip,*GRIP[pose],h=11)
        s['fx'].append(('dp_katana',hx,hy,180 if flip else 0))
    s['actors']=acts
    return s

# ==== review ==========================================================================================
ETENDO_GREEN = (190,240,80)                                          # the swipe: the new logo's lime
DIFF=[("+","EXPORT FUNCTION FORGE"),("-","IF A IF B IF C IF D"),("+","CONST THINGY2: ANY"),      # only what the font has
      ("+","TODO: FIX LATER. MAYBE."),("-","CONSOLE.LOG ASDFASDF"),("+","RETURN SCHEMA"),("+","TESTS: 412 PASSED")]

@fx('dp_term_pr')
def _fx_term_pr(d,im,e,f):
    """Claude's PR as a terminal window on the right: the title bar, the diff scrolling; k 0..1 slides it in,
    cut: once the katana goes through, the two halves fall apart."""
    _,k,scroll,stamp,cut=e
    x0,x1=74,182; y0=int(lerp(-50,4,ease(k))); y1=y0+46
    def window(dd,yy):
        dd.rectangle([x0,yy,x1,yy+46],fill=(18,18,24),outline=(90,90,104))
        dd.rectangle([x0,yy,x1,yy+6],fill=(40,40,52))
        for c,cx in (((240,90,80),x0+3),((240,200,80),x0+6),((110,200,90),x0+9)): dd.point((cx,yy+3),fill=c)
        text(dd,"ETENDO_SCHEMA_FORGE",x0+13,yy+1,(200,200,214),shadow=None)
        text(dd,"PR BY CLAUDE",x0+3,yy+8,(217,119,87),shadow=None)
        for i in range(5):
            j=(i+int(scroll))%len(DIFF); sign,line=DIFF[j]
            c=(110,210,120) if sign=='+' else (230,100,100)
            text(dd,sign+line[:25],x0+3,yy+15+i*6,c,shadow=None)
        if stamp>0:                                                   # LGTM, slammed on (it shrinks into place)
            sc=1 if stamp>=1 else 2; cx,cy=(x0+x1)//2,yy+26
            w,h=28*sc,10*sc
            dd.rectangle([cx-w,cy-h,cx+w,cy+h],fill=(16,40,22),outline=(90,220,110),width=2)
            big_text(dd._image,"LGTM",cy-5*sc,(90,220,110),scale=2*sc,cx=cx,shadow=None)
    if cut<=0: window(d,y0); return
    layer=Image.new('RGB',(W,H),(0,0,0)); m=Image.new('L',(W,H),0)
    window(ImageDraw.Draw(layer),y0); ImageDraw.Draw(m).rectangle([x0,y0,x1,y1],fill=255)
    tmp=im.copy(); tmp.paste(layer,(0,0),m)
    top=tmp.crop((x0,y0,x1+1,y0+23)); bot=tmp.crop((x0,y0+23,x1+1,y1+1))
    drop=int(cut*cut*60)
    im.paste(top.rotate(-6*cut,expand=False),(x0-int(10*cut),y0-drop//3))
    im.paste(bot.rotate(8*cut,expand=False),(x0+int(8*cut),y0+23+drop))
    if cut<0.3: ImageDraw.Draw(im).line([x0-4,y0+24,x1+4,y0+22],fill=(255,255,255),width=2)

def closeup_logo(t,f):
    """Primer plano: the Etendo logo on a card, Deadpool's mask peeking in from the right. The old yellow
    logo; a swipe; the new lime one with the black < > — NEW LOGO. HUH? / EDGY. I DIG IT."""
    im=Image.new('RGB',(W,H),(30,18,14)); d=ImageDraw.Draw(im)
    d.rectangle([6,8,132,58],fill=(250,250,250),outline=(200,200,200))
    new=t>=0.32
    sw=min(1,max(0,(t-0.3)/0.06))
    lg=etendo_logo('new' if new else 'old'); k=42                    # the etendo theme's own logos, 1.5x
    lg=lg.resize((k,k),Image.NEAREST); im.paste(lg,(12,12),lg); d=ImageDraw.Draw(im)
    big_text(im,"ETENDO",27,ETENDO_INK if new else ETENDO_NAVY,scale=2,cx=96,shadow=None)
    if 0<sw<1: d.rectangle([6,8,6+int(126*sw),58],fill=ETENDO_GREEN)           # the rebrand, swiped in
    d.rectangle([150,10,W+10,H],fill=RED); d.line([166,10,166,H],fill=RED_D)  # the mask, peeking in
    d.polygon([(154,20),(176,20),(174,40),(156,40)],fill=(18,16,18))
    sq=0.0 if t<0.5 else 0.5
    d.rectangle([160,24+int(6*sq),170,36],fill=(250,250,250))
    if 0.06<=t<0.5: FX['dp_box'](d,im,('dp_box',"NEW LOGO. HUH?",70,1),f)
    if t>=0.52: FX['dp_box'](d,im,('dp_box',"EDGY. I DIG IT.",70,1),f)
    if t<0.05: zoom_lines(d)
    return im

def clip_review(f):
    s=scene(f,THEME)
    x,y,pose,mood,flip=30,GROUND,guard_pose(f),'normal',False
    k,scroll,stamp,cut=0.0,0,0.0,0.0
    if 14<=f<330: k=min(1,(f-14)/12)
    if 18<=f<62: s['fx'].append(('dp_box',"OOH. A PULL REQUEST.",34,4)); mood='happy'
    if 62<=f<160: scroll=(f-62)/14
    if 66<=f<110: s['fx'].append(('dp_box',["WHO NAMED","THIS VARIABLE?"],34,4)); mood='squint'
    if 112<=f<160: s['fx'].append(('dp_box',["THREE NESTED","IFS? BOLD."],34,4)); mood='angry'
    if 160<=f<250: s['image']=closeup_logo((f-160)/90,f); return s
    if 250<=f<300:
        scroll=7; stamp=min(1,(f-256)/5) if f>=256 else 0
        if 256<=f<262: s['shake']=rshake(2)
        if 254<=f<262: pose='armsup'
        s['fx'].append(('dp_box',"LGTM.",34,4)); mood='happy'
    if 300<=f<330:
        scroll,stamp=7,1
        if f<310: x,pose=ez(30,96,(f-300)/10),'dash'
        else: x,pose=96,'punch'
        if f<316: callout(s,"MERGE.",y=52,c=(190,140,255))
        cut=0 if f<312 else (f-312)/18
    if 330<=f<354: callout(s,"MERGED",y=4,c=(190,140,255)); x,pose,mood=96,guard_pose(f),'happy'
    if 354<=f<366: x,flip,pose=ez(96,30,(f-354)/12),True,guard_pose(f)
    if f>=366: x,flip=30,False
    if 14<=f<330: s['under'].append(('dp_term_pr',k,scroll,stamp,cut))
    acts=[actor(DP[mood][pose],x,y,flip=flip,pal=DPAL)]
    if pose in GRIP:
        hx,hy=hand_at(DP[mood][pose],x,int(y),flip,*GRIP[pose],h=11)
        s['fx'].append(('dp_katana',hx,hy,180 if flip else 0))
    s['actors']=acts
    return s

# ==== byebyebye =======================================================================================
# The Deadpool & Wolverine opening: Deadpool dances to NSYNC's "Bye Bye Bye" (about 170 BPM, a beat every
# 7 frames at 20 fps) and the TVA squad rushes in from both sides; he takes them out on the beat.
BBB_N=300
BEAT0,BEAT=14,7
DANCE_X=92
TVA_L,TVA_R=58,126                                                 # where the agents stand, left and right
# a TVA agent: khaki suit (j), brown belt (b), short hair, no ears
TVA_SPEC={'name':'tva','w':18,'h':26,'c':9,'legs':9,'torso':7,'head':5,'hair':('hhhh',),'hair_x':-2,'hair_y':1,
          'body':{'color':'j','belt':'b'},'leg':{'color':'j'},'arm':{'hand':'s'},'eyes':(0,2)}
AGENT_PAL={'j':(196,170,110),'b':(96,64,36),'s':(226,182,140),'h':(60,40,30),'K':(20,16,16),'o':(255,140,40),
           'k':(30,24,20)}
_TVA_STAND=figure(TVA_SPEC,POSES['stand']); _TVA_JAB=figure(TVA_SPEC,POSES['jab']); _TVA_HURT=figure(TVA_SPEC,POSES['hurt'])
_TVA_FALL=S([''.join(r[i] for r in _TVA_STAND) for i in range(len(_TVA_STAND[0]))])        # lying flat: rotated
# (side, enter frame, kill frame, move, callout): every kill lands on a beat (BEAT0 + n*BEAT)
KILLS=[('L',50,77,'slash','SHLICK!'), ('R',54,91,'kick',None), ('L',88,105,'wave','BYE!'),
       ('R',92,119,'katana',None), ('L',150,175,'baton','WHACK!'), ('R',150,196,'wave','BYE BYE!')]

@fx('dp_blood')
def _fx_blood(d,im,e,f):
    """A burst of blood from a hit, k frames after it: 16 drops fly out (about 6 px) and fall."""
    _,x,y,k=e
    for i in range(16):
        rr=random.Random(i*31+int(x))
        px=x+rr.uniform(-1,1)*0.9*k; py=y+rr.uniform(-1.6,-0.4)*k+0.3*k*k
        if 0<=px<W-1 and 0<=py<GROUND-1:
            c=RED if i%3 else RED_D
            d.rectangle([int(px),int(py),int(px)+1,int(py)+1],fill=c)

@fx('dp_note')
def _fx_note(d,im,e,f):
    """A music note floating up off the dance, k frames old (it fades as it rises)."""
    _,x,y,k=e
    x,y=int(x),int(y-k*0.6); c=(250,250,250) if k<8 else (150,150,160)
    d.rectangle([x,y-3,x,y],fill=c); d.rectangle([x-1,y,x,y+1],fill=c)               # stem and head

@fx('dp_baton')
def _fx_baton(d,im,e,f):
    """The TVA agent's baton in Deadpool's hand: a dark stick with an orange tip."""
    _,hx,hy,a=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.line([hx,hy,hx+c*8,hy+s*8],fill=(40,30,26)); d.point((hx+c*8,hy+s*8),fill=AGENT_PAL['o'])

@fx('dp_agent_baton')
def _fx_agent_baton(d,im,e,f):
    """A TVA agent's baton, held in his hand (drawn while he swings)."""
    _,hx,hy,a=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.line([hx,hy,hx+c*7,hy+s*7],fill=(40,30,26)); d.point((hx+c*7,hy+s*7),fill=AGENT_PAL['o'])

def closeup_dance(t,f):
    """Primer plano: the MAXIMUM EFFORT mask (closeup_effort's), bopping on the beat, then OH HELL YEAH."""
    base=closeup_effort(min(t,0.44),f)
    ox=2 if ((f-BEAT0)//BEAT)%2==0 else -2                                   # the whole mask bops on the beat
    im=Image.new('RGB',(W,H),(30,18,14)); im.paste(base,(ox,0))
    d=ImageDraw.Draw(im)
    if t>=0.15: FX['dp_box'](d,im,('dp_box',"OH HELL YEAH",128,28),f)
    if t<0.05: zoom_lines(d)
    return im

def _strike(f,k,side,move):
    """Deadpool on the beat k: a lunge at the agent on `side` (x, pose, flip), the hit (k..k+2), the
    spring back (k+3..k+6). None outside those 13 frames."""
    L=side=='L'; tx=70 if L else 114
    if k-6<=f<k: return ez(DANCE_X,tx,(f-(k-6))/6),'dash',L
    if k<=f<k+3: return tx,('armsup' if move=='wave' else 'dash' if move=='kick' else 'punch'),L
    if k+3<=f<k+7: return ez(tx,DANCE_X,(f-k-3)/4),guard_pose(f),L
    return None

def _agent(f,side,enter,k):
    """A TVA agent (x, sprite, y, alpha): rushes in from its side from `enter`, swings, is hit on k: he
    drops flat on the hit and slides back (k..k+3), fades out (k+6..k+10). None when not on screen."""
    if not enter<=f<k+11: return None
    L=side=='L'; start,stop=(-16,TVA_L) if L else (W+16,TVA_R)
    if f<k:
        if f<enter+14:
            return ez(start,stop,(f-enter)/14), _TVA_STAND, GROUND-((f-enter)//3)%2, 1.0
        if k-12<=f<k-6: return stop, _TVA_JAB, GROUND, 1.0                    # they swing first
        return stop, _TVA_STAND, GROUND, 1.0
    d=-1 if L else 1
    if f<k+4: return stop+d*(f-k)*1.5, _TVA_FALL, GROUND, 1.0                  # drops flat on the hit, slides
    a=max(0.0,min(1.0,1-(f-k-6)/4))
    return stop+d*(4*1.5+(f-k-4)*0.6), _TVA_FALL, GROUND, a

DANCE_MOVES=('bye','push','cross','hip')
def dance_move(beat):
    """(pose, flip) for dance beat `beat`: the four moves in turn, and the mirror alternates each beat and
    each cycle, so bye goes out to one side, then the other."""
    return DANCE_MOVES[beat%4], (beat%2+beat//4)%2==1

def clip_byebyebye(f):
    s=scene(f,THEME)
    if 126<=f<166: s['image']=closeup_dance((f-126)/40,f); return s          # the mask, mid-dance
    x,y,pose,mood,flip=30,GROUND,guard_pose(f),'normal',False
    weapon=None
    # 1) the dance: Deadpool steps out of the neutral pose and hops on the beat, three moves in turn:
    #    bye, push, cross, hip (dance_move), one move on each beat
    if BEAT0<=f<262:
        beat=(f-BEAT0)//BEAT
        x=ez(30,DANCE_X,(f-BEAT0)/20) if f<34 else DANCE_X
        y=GROUND-int(3*math.sin(math.pi*((f-BEAT0)%BEAT)/BEAT))
        pose,flip=dance_move(beat); mood='happy'
    if cue(f,BEAT0,'BYE BYE BYE'): s['fx'].append(('dp_box','BYE BYE BYE',DANCE_X,4))   # 22 frames
    for bs in range(BEAT0,262,2*BEAT):                                                  # a note every other beat
        if (bs<77 or bs>=203) and 0<=f-bs<16:
            s['fx'].append(('dp_note',DANCE_X+(-30 if (bs//BEAT)%4<2 else 30),GROUND-26,f-bs))
    # 2) the TVA squad: each kill lands on a beat; the lunge, the hit, the spring back
    for n,(side,enter,k,move,txt) in enumerate(KILLS):
        st=_strike(f,k,side,move)
        if st:
            x,pose,flip=st; y=GROUND; mood='angry'
            if pose in GRIP and move in ('slash','katana','baton'): weapon='baton' if move=='baton' else 'katana'
        nxt=KILLS[n+1][2] if n+1<len(KILLS) else k+hold(txt or '')
        if txt and k<=f<min(k+hold(txt),nxt): callout(s,txt)                  # cut when the next hit lands
        if k<=f<k+9: s['fx'].append(('dp_blood',TVA_L if side=='L' else TVA_R,GROUND-9,f-k))
    # 3) the last agent down: he keeps dancing and waves bye, the arms crossing on each beat
    if 203<=f<262:
        pose,flip=dance_move((f-BEAT0)//BEAT+3); mood='happy'                  # bye lands on beat 29 (216)
    if cue(f,216,'BYE, TVA.'): s['fx'].append(('dp_box','BYE, TVA.',DANCE_X,4))
    # 4) back to the neutral pose
    if 262<=f<284: x,flip,pose,y,mood=ez(DANCE_X,30,(f-262)/22),True,guard_pose(f),GROUND,'normal'
    if f>=284: x,flip,pose,y,mood=30,False,guard_pose(f),GROUND,'normal'
    acts=[]
    for side,enter,k,move,txt in KILLS:
        a=_agent(f,side,enter,k)
        if a:
            ax,spr,ay,al=a
            acts.append(actor(spr,int(round(ax)),ay,flip=side=='R',pal=AGENT_PAL,alpha=al))
            if spr is _TVA_JAB and k-12<=f<k-6:
                hx,hy=figure_point(TVA_SPEC,POSES['jab'],'hand',int(round(ax)),ay,flip=side=='R')
                s['fx'].append(('dp_agent_baton',hx,hy,0 if side=='L' else 180))
    acts.append(actor(DP[mood][pose],x,y,flip=flip,pal=DPAL))
    if weapon:
        hx,hy=hand_at(DP[mood][pose],x,int(y),flip,*GRIP[pose],h=11)
        s['fx'].append(('dp_katana' if weapon=='katana' else 'dp_baton',hx,hy,180 if flip else 0))
    s['actors']=acts
    return s

CLIPS = [clip('bub', N_, clip_bub), clip('notchverse', 365, clip_notchverse), clip('webcam', 377, clip_webcam),
         clip('review', 377, clip_review), clip('byebyebye', BBB_N, clip_byebyebye)]
