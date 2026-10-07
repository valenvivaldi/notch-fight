"""Fight Club: Claude as the Narrator (white shirt, the tie loosened, a black eye) in the basement of Lou's
Tavern: one bare bulb swinging on its cord, the crowd standing in a ring in the dark (a back row against
the bricks, a front row in silhouette). Clip `rules`, raw: THE FIRST RULE OF FIGHT CLUB IS... (and the rest
is crossed out); Tyler (the red leather jacket, the shades) steps into the ring and they trade bare-knuckle
punches, the blood landing on the concrete, his face getting worse. Close-up: the bloody grin, the pink bar
of Paper Street soap, I AM JACK'S SMIRKING REVENGE. Then Tyler flickers, and is gone: Claude alone in the
ring, hitting himself. The end: the window, the towers coming down one by one, holding Marla's hand —
WHERE IS MY MIND?
Clip `firstrule`, the same for laughs: the rules drop as signs and cross themselves out as he reads them, HIT ME
AS HARD AS YOU CAN (the ear), a cartoon brawl, and he was punching himself: WHY AM I HITTING MYSELF?"""
from engine import *

THEME = 'fightclub'
N_ = 384                                                            # a multiple of 12 and of 48 (the bulb)
CX, TX = 80, 98                                                     # Claude; Tyler, when he's there (in reach)
INK = (16,12,12)
BLOOD, BLOOD_D = (176,20,24), (110,10,14)
SOAP = (236,150,170)

# ---- the two of them: built from a pose, so they move alike --------------------------------------------
GW, GH, C = 28, 24, 12                                              # grid, centre column (they face right)
ARMS = {    # pose -> (back elbow, back fist, front elbow, front fist), from (C, shoulder row); lean; legs
 'guard': ((1,4),(4,-2),(3,4),(6,-3),0,'stance'),
 'guard2':((1,4),(4,-1),(3,4),(6,-2),0,'stance'),
 'jab':   ((1,4),(4,-2),(6,0),(11,-2),1,'lunge'),
 'hook':  ((4,-1),(10,-3),(3,4),(5,-1),2,'lunge'),
 'hurt':  ((-3,3),(-6,1),(1,5),(4,6),-2,'reel'),
 'self':  ((1,4),(4,-2),(7,2),(3,-4),-1,'stance'),
 'down':  ((0,6),(1,8),(2,6),(4,8),0,'stand'),
}
def _tie(g, at):                                                    # loosened, down the shirt
    for y in range(at['ty'], at['hip'] - 1): put(g, at['c'] + 1 + at['sh'](y), y, 't')
def _shirt(g, at):                                                  # under the open jacket
    for y in range(at['ty'], at['hip'] - 1):
        for dx in (0, 1): put(g, at['c'] + dx + at['sh'](y), y, 'u')
def _shades(g, at):
    o = at['sh'](at['hy'])
    for x in range(at['c'] - 2 + o, at['c'] + 3 + o): put(g, x, at['hy'] + 2, 'G')
def _bruise(g, at):                                                 # the black eye
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for x, y in ((c + 1, hy + 1), (c + 2, hy + 2), (c + 2, hy + 3)): put(g, x + o, y, 'v')
def _blood(g, at):                                                  # the brow, the nose, the mouth, the shirt
    c, hy, ty, o = at['c'], at['hy'], at['ty'], at['sh'](at['hy'])
    for x, y in ((c + 2, hy + 1), (c + 2, hy + 4), (c + 1, hy + 4), (c + 2, hy + 3), (c, hy + 4), (c + 1, ty + 1))[:at['flags'].get('blood', 0) * 2]:
        put(g, x + o, y, 'r')

def build(who, pose, blood=0):
    """A fighter in a pose (ARMS), with blood 0..3: engine/people.py's figure()."""
    return figure(who, ARMS[pose], **({'blood': blood} if blood else {}))

_FIGHTER = dict(w=GW, h=GH, c=C, legs=9, torso=7, eyes=(-1, 1), leg=dict(back='P'), body=dict(top='w', belt='b'),
                arm=dict(sleeve='a', back_sleeve='A', fore='a', back_fore='A', fist=2))
NARRATOR = dict(_FIGHTER, name='narr', hair=["..hhhh.", "hhhhhhh", "hh....."], hair_y=2,
                paint={'body': [_tie], 'head': [_bruise], 'face': [_blood]})
TYLER    = dict(_FIGHTER, name='tyler', hair=["h.h.h..", "hhhhhh.", "hhhhhhh", "hh....."], hair_y=3,
                paint={'body': [_shirt], 'head': [_shades], 'face': [_blood]})
CPAL = {'s':(232,192,160),'K':INK,'h':(70,46,32),'j':(232,228,216),'w':(250,248,240),'A':(200,196,186),'a':(232,228,216),
        't':(110,24,28),'b':(40,30,26),'p':(64,64,70),'P':(50,50,56),'k':(24,20,20),'f':(232,192,160),'v':(110,60,120),'r':BLOOD}
TPAL = {'s':(232,196,166),'K':INK,'G':(12,12,14),'h':(204,170,110),'j':(168,40,30),'w':(120,24,18),'A':(130,28,20),'a':(168,40,30),
        'u':(214,180,90),'b':(40,30,26),'p':(70,84,120),'P':(56,68,100),'k':(30,26,24),'f':(232,196,166),'r':BLOOD}

# ---- the basement -------------------------------------------------------------------------------------
def _basement(d):
    d.rectangle([0,0,W,H],fill=(26,20,18))
    for y in range(0,42,4):                                          # the bricks, barely there
        for x in range((y//4)%2*6,W,12): d.rectangle([x,y,x+10,y+2],fill=(36,28,24))
    d.line([0,5,W,5],fill=(46,40,36)); d.line([0,7,W,7],fill=(40,34,30))   # a pipe along the ceiling
    d.rectangle([0,42,W,H],fill=(44,42,40))                          # the concrete
    for x in range(-40,W+40,22): d.line([92+(x-92)*0.4,42,x,H],fill=(38,36,34))
register_bg(THEME, lambda v: (v+20,v+18,v+16), decor=_basement)

def bulb_x(f): return 92+6*math.sin(2*math.pi*(f%48)/48)

@fx('fc_light')
def _fx_light(d,im,e,f):
    """The bulb on its cord, the cone and the pool of light on the floor (it swings)."""
    bx=bulb_x(f); m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    md.polygon([(bx-3,12),(bx+3,12),(bx+60,H),(bx-60,H)],fill=46)
    md.ellipse([bx-58,46,bx+58,H+8],fill=70)
    im.paste((255,214,150),(0,0),m.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    d.line([92,0,bx,9],fill=(20,20,20)); d.rectangle([bx-1,8,bx+1,9],fill=(60,60,60))
    d.ellipse([bx-2,10,bx+2,14],fill=(255,240,200))

@fx('fc_crowd')
def _fx_crowd(d,im,e,f):
    """The ring: a back row against the wall, lit along the tops of their heads; or the front row, in silhouette."""
    _,row=e; rr=random.Random(5 if row=='back' else 6)
    if row=='back':
        for i in range(17):
            x=4+i*11+rr.randint(-2,2); y=30+rr.randint(-2,2)+((f//24+i)%4==0)
            d.rectangle([x-4,y+5,x+4,46],fill=(14,12,12)); d.ellipse([x-3,y,x+3,y+6],fill=(18,14,14))
            d.line([x-2,y,x+2,y],fill=(110,86,60))
    else:
        for x,y in ((6,46),(20,49),(170,48),(182,46)):
            d.ellipse([x-8,y,x+8,y+14],fill=(8,6,6)); d.rectangle([x-12,y+10,x+12,H],fill=(8,6,6))

@fx('fc_floorblood')
def _fx_floorblood(d,im,e,f):
    """Blood on the concrete: n spatters so far."""
    _,n=e; rr=random.Random(32)
    for i in range(n):
        x=rr.randint(60,128); y=rr.randint(54,62); r=rr.randint(1,3)
        d.ellipse([x-r,y-r*0.5,x+r,y+r*0.5],fill=BLOOD_D); d.point((x+r+1,y),fill=BLOOD_D)

@fx('fc_spray')
def _fx_spray(d,im,e,f):
    """Drops flying off a punch (k frames old), going dir."""
    _,x,y,k,dr=e; rr=random.Random(int(x)*3+int(y))
    for _ in range(6):
        vx=rr.uniform(0.6,1.8)*dr; vy=rr.uniform(-1.6,-0.3)
        px=x+vx*k; py=y+vy*k+0.18*k*k
        if py<GROUND: d.point((int(px),int(py)),fill=BLOOD); d.point((int(px)+1,int(py)),fill=BLOOD_D)

# ---- the card, the close-up, the window -----------------------------------------------------------------
def card_rules(t,f):
    """THE FIRST RULE OF FIGHT CLUB IS... and the rest, crossed out before it's said."""
    im=Image.new('RGB',(W,H),(8,6,6)); d=ImageDraw.Draw(im)
    big_text(im,"THE FIRST RULE",4,(236,232,220),scale=2,shadow=None)
    if t>=0.15: big_text(im,"OF FIGHT CLUB IS...",20,(236,232,220),scale=2,shadow=None)
    if t>=0.5:
        text(d,"YOU DO NOT TALK ABOUT FIGHT CLUB",W//2-64,44,(200,190,176),shadow=None)
        k=min(1,(t-0.6)/0.15)
        if k>0: d.line([W//2-67,46,W//2-67+int(134*k),46],fill=BLOOD); d.line([W//2-67,47,W//2-67+int(134*k),47],fill=BLOOD_D)
    if (f//2)%7==0: d.point((random.Random(f).randint(0,W-1),random.Random(f+1).randint(0,H-1)),fill=(80,80,80))   # film grain
    return im

def closeup_soap(t,f):
    """Primer plano: the grin with blood in the teeth, the bruised eye; the pink bar of soap, PAPER STREET
    SOAP CO.; then I AM JACK'S SMIRKING REVENGE."""
    im=Image.new('RGB',(W,H),(30,24,20)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([-30,-30,110,90],fill=90); im.paste((255,210,150),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    d.rectangle([4,6,66,H+4],fill=CPAL['s'],outline=INK)            # his face, big
    d.rectangle([60,6,66,H],fill=(200,156,124)); d.rectangle([4,0,66,9],fill=CPAL['h'],outline=INK)
    d.rectangle([18,18,22,28],fill=INK); d.rectangle([42,18,46,28],fill=INK)   # the eyes
    d.ellipse([36,13,54,32],outline=(110,60,120),width=3)            # the black eye
    d.line([16,13,26,15],fill=BLOOD,width=2); d.line([24,15,22,24],fill=BLOOD)  # the split brow, running
    d.rectangle([14,40,54,48],fill=(250,246,236),outline=INK)        # the grin
    for x in range(20,54,6): d.line([x,40,x,48],fill=INK)
    for x in (26,38): d.rectangle([x-2,41,x+2,47],fill=BLOOD)        # blood in the teeth
    d.line([34,30,35,40],fill=BLOOD,width=2); d.line([48,48,50,60],fill=BLOOD,width=2)   # the nose, the chin
    if t<0.45:                                                       # the soap, held up
        sx=lerp(W+10,92,ease(min(1,t/0.15)))
        d.rounded_rectangle([sx,18,sx+76,50],radius=8,fill=SOAP,outline=(170,90,110))
        d.rounded_rectangle([sx+4,22,sx+72,46],radius=6,outline=(214,124,148))
        text(d,"PAPER STREET",int(sx)+14,28,(176,86,108),shadow=None); text(d,"SOAP CO.",int(sx)+22,36,(176,86,108),shadow=None)
        d.rectangle([sx-6,40,sx+4,56],fill=CPAL['s'],outline=INK)  # the thumb
    else:
        big_text(im,"I AM JACK'S",6,(236,232,220),scale=2,cx=126,shadow=INK)
        big_text(im,"SMIRKING",24,(236,232,220),scale=2,cx=126,shadow=INK)
        big_text(im,"REVENGE.",42,BLOOD,scale=2,cx=126,shadow=INK)
    if t<0.04: zoom_lines(d,(255,214,150))
    return im

def window(t,f):
    """The end: the dark office, the big window, the towers coming down one by one; the two of them from
    behind, holding hands. WHERE IS MY MIND?"""
    im=Image.new('RGB',(W,H),(14,16,30)); d=ImageDraw.Draw(im)
    for y in range(44): d.line([0,y,W,y],fill=(int(18+20*y/44),int(20+14*y/44),int(44+20*y/44)))
    towers=((10,16,22),(30,8,16),(50,20,18),(74,4,20),(100,14,16),(122,10,22),(150,6,18),(170,18,14))
    for i,(x,top,w) in enumerate(towers):
        start=0.12+0.08*i; k=max(0,min(1,(t-start)/0.18))
        y0=top+int(k*(48-top))                                     # it sinks into its own dust
        if y0<46:
            d.rectangle([x,y0,x+w,46],fill=(30,32,44))
            rr=random.Random(i)
            for wy in range(y0+3,46,4):
                for wx in range(x+2,x+w-1,3):
                    if rr.random()<0.5: d.point((wx,wy),fill=(240,210,120))
        raw=(t-start)/0.18
        if 0<raw<1.6:                                                # its dust, rising and thinning
            a=1-abs(raw-0.6)/1.0
            for j in range(5):
                r=3+raw*3; cx=x+j*w/4; cy=44-raw*6-j%2*3
                d.ellipse([cx-r,cy-r*0.7,cx+r,cy+r*0.7],fill=tuple(int(lerp(c0,c1,max(0,a))) for c0,c1 in zip((24,26,42),(96,92,96))))
        if start<=t<start+0.03: d.rectangle([x-2,0,x+w+2,46],outline=(255,200,120))   # the flash
    d.rectangle([0,44,W,H],fill=(10,10,14))
    for x in (0,62,124,184): d.rectangle([x-1,0,x+1,46],fill=(8,8,10))   # the mullions
    d.rectangle([0,44,W,47],fill=(8,8,10))
    for x,hair in ((84,False),(100,True)):                           # the two of them, from behind
        d.ellipse([x-4,30,x+4,40],fill=(6,6,8)); d.rectangle([x-6,38,x+6,H],fill=(6,6,8))
        if hair: d.ellipse([x-6,28,x+6,38],fill=(6,6,8))
    d.line([90,48,94,48],fill=(6,6,8),width=2)                       # their hands
    if t>=0.15: big_text(im,"WHERE IS MY MIND?",6,(236,232,220),scale=2,shadow=INK)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
HITS = ((100,'tyler','jab'),(114,'claude','jab'),(126,'tyler','hook'),(140,'claude','hook'),(152,'tyler','jab'),(162,'claude','hook'))

def clip_rules(f):
    s=scene(f,THEME)
    if 14<=f<80: s['image']=card_rules((f-14)/66,f); return s
    if 170<=f<250: s['image']=closeup_soap((f-170)/80,f); return s
    if 296<=f<352: s['image']=window((f-296)/56,f); return s
    if 352<=f<366: s['image']=fade_to(window(1.0,f),(0,0,0),(f-352)/14); return s
    s['under']+=[('fc_crowd','back'),('fc_light',)]
    g=guard_pose(f); pose,tpose='guard' if g=='guard' else 'guard2','guard' if g=='guard2' else 'guard2'
    cx,tx=CX,None; blood=0; spatters=0
    fight=80<=f<296
    if 80<=f<170:
        tx=lerp(W+14,TX,ease((f-80)/18))
        for hf,who,kind in HITS:
            if f>=hf+2 and who=='tyler': blood=min(3,blood+1)
            if f>=hf+2: spatters+=2
            if hf<=f<hf+7:                                           # the punch: a step in, it lands
                if who=='tyler': tpose=kind; tx-=3
                else: pose=kind; cx+=3
            if hf+2<=f<hf+10:                                        # the head snaps back
                if who=='tyler': pose='hurt'; cx-=2
                else: tpose='hurt'; tx+=2
            if hf+2<=f<hf+16:
                k=f-hf-2
                if who=='tyler': s['fx'].append(('fc_spray',cx+1,GROUND-19,k,-1))
                else: s['fx'].append(('fc_spray',tx-1,GROUND-19,k,1))
                if k<2: s['shake']=rshake(1)
    if 250<=f<296:
        blood,spatters=3,12
        if f<262 and (f//2)%3==0: tx=TX                              # Tyler flickers... and is gone
        if f>=262:
            k=(f-262)%12; pose='self' if k<5 else ('hurt' if k<9 else 'guard')
            if k==3: s['shake']=rshake(1)
            if 3<=k<10: s['fx'].append(('fc_spray',cx+2,GROUND-19,k-3,-1))
    if fight: s['under'].append(('fc_floorblood',spatters))
    acts=[]
    if tx is not None: acts.append(actor(build(TYLER,tpose),tx,flip=True,pal=TPAL))
    acts.append(actor(build(NARRATOR,pose,blood),cx,pal=CPAL))
    s['actors']=acts
    s['fx'].append(('fc_crowd','front'))
    return s

# ---- clip 2: firstrule — the same, for laughs: no blood, and he's still fighting himself ----------------
N_FIRST = 480                                                       # a multiple of 12 and of 48 (the bulb)
SIGN_X = 140
RULES = ((14,84,["RULE 1:","DON'T TALK ABOUT","FIGHT CLUB."]),
         (84,144,["RULE 2:","DON'T TALK ABOUT","FIGHT CLUB."]),
         (144,204,["RULE 8: FIRST NIGHT?","YOU HAVE TO","FIGHT."]))

@fx('fc_sign')
def _fx_sign(d,im,e,f):
    """A cardboard sign on two strings from the ceiling: y its top, x crossed (0..1), an arrow down."""
    _,lines,y,cross,arrow=e; y=int(y); x0,w,h=SIGN_X-42,84,len(lines)*7+5
    for sx in (x0+8,x0+w-8): d.line([sx,0,sx,y],fill=(70,64,56))
    d.rectangle([x0,y,x0+w,y+h],fill=(214,196,160),outline=(90,74,50))
    for i,l in enumerate(lines): text(d,l,SIGN_X-len(l)*2,y+3+i*7,INK,shadow=None)
    if cross>0:                                                      # it crosses itself out
        k=min(1,cross*2); d.line([x0+2,y+2,x0+2+(w-4)*k,y+2+(h-4)*k],fill=BLOOD,width=2)
        if cross>0.5: k=min(1,(cross-0.5)*2); d.line([x0+w-2,y+2,x0+w-2-(w-4)*k,y+2+(h-4)*k],fill=BLOOD,width=2)
    if arrow:                                                        # pointing at him
        ax,ay=x0-2,y+h-2; bx,by=CX+8,y+h+10
        d.line([ax,ay,bx,by],fill=BLOOD,width=2); d.polygon([(bx-4,by-1),(bx+1,by-4),(bx-1,by+2)],fill=BLOOD)

@fx('fc_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(240,236,226),ink=INK)                     # the engine's bubble (engine/people.py)

@fx('fc_brawl')
def _fx_brawl(d,im,e,f):
    """The cartoon fight: a rolling dust cloud, fists and shoes poking out, stars, POW and BONK."""
    _,x,y=e; rr=random.Random(f//2)
    for i in range(9):
        a=i*0.7+f*0.3; r=rr.randint(6,9)
        cx,cy=x+math.cos(a)*12,y+math.sin(a)*6
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(170,164,156),outline=(110,104,98))
    for i in range(3):                                               # a fist, a shoe, a fist
        a=rr.uniform(0,2*math.pi); ex,ey=x+math.cos(a)*20,y+math.sin(a)*10
        d.line([x+math.cos(a)*12,y+math.sin(a)*6,ex,ey],fill=(232,228,216) if i!=1 else (64,64,70),width=2)
        d.rectangle([ex-2,ey-2,ex+2,ey+1],fill=(232,192,160) if i!=1 else (24,20,20),outline=INK)
    for k in range(3): spark(d,int(x+rr.randint(-20,20)),int(y+rr.randint(-14,4)),2,(255,230,90))
    word=("POW!","BONK!","WHAM!")[(f//8)%3]; text(d,word,int(x-8+rr.randint(-14,14)),int(y-18),(255,230,90))

def closeup_myself(t,f):
    """Primer plano: his own fist coming at his own face, eyes wide — WHY AM I HITTING MYSELF?"""
    im=Image.new('RGB',(W,H),(30,24,20)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([-30,-30,110,90],fill=90); im.paste((255,210,150),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    d.rectangle([4,6,66,H+4],fill=CPAL['s'],outline=INK); d.rectangle([60,6,66,H],fill=(200,156,124))
    d.rectangle([4,0,66,9],fill=CPAL['h'],outline=INK)
    for ex in (16,40): d.ellipse([ex,16,ex+12,30],fill=(250,248,240),outline=INK); d.rectangle([ex+5,21,ex+7,25],fill=INK)   # eyes wide
    d.ellipse([28,34,40,42],fill=(90,30,30),outline=INK)             # the mouth, open
    k=(f//4)%2                                                       # the uppercut, again and again
    fy=lerp(H+20,46,ease(min(1,t/0.2)))+(0 if k else 8)
    if fy+10<H+10: d.rectangle([26,fy+10,44,H+10],fill=CPAL['j'],outline=INK)   # his own sleeve, from below
    d.rounded_rectangle([24,fy-2,46,fy+12],radius=4,fill=CPAL['s'],outline=INK)
    for j in range(3): d.line([28+j*5,fy-2,28+j*5,fy+4],fill=(180,130,100))
    if not k and t>0.2: spark(d,35,int(fy-4),4,(255,230,90))
    if t>=0.1:
        big_text(im,"WHY AM I",8,(236,232,220),scale=2,cx=126,shadow=INK)
        big_text(im,"HITTING",26,(236,232,220),scale=2,cx=126,shadow=INK)
        big_text(im,"MYSELF?",44,(255,230,90),scale=2,cx=126,shadow=INK)
    if t<0.04: zoom_lines(d,(255,214,150))
    return im

def clip_firstrule(f):
    s=scene(f,THEME)
    if 366<=f<426: s['image']=closeup_myself((f-366)/60,f); return s
    s['under']+=[('fc_crowd','back'),('fc_light',)]
    g=guard_pose(f); pose='guard' if g=='guard' else 'guard2'
    cx,tx,tpose,talpha=CX,None,'guard',1.0
    # the signs: each one drops, he reads it out loud... and it crosses itself out
    for i,(a,b,lines) in enumerate(RULES):
        if a<=f<b:
            t=f-a
            y=lerp(-30,4,ease(min(1,t/10)))+(2*math.sin(t*0.9)*max(0,1-(t-10)/10) if t>=10 else 0)
            if t>=b-a-8: y=lerp(4,-34,(t-(b-a-8))/8)
            cross=0 if i==2 else max(0,min(1,(t-30)/12))
            s['under'].append(('fc_sign',lines,y,cross,i==2 and t>=24))
            if i<2 and 12<=t<30: s['fx'].append(('fc_bubble',lines[0]+" "+lines[1].split(' ')[0]+"..." if i==0 else "ISN'T THAT RULE 1?",56,18,cx+2))
            if i<2 and 30<=t<b-a-4: pose='self'; s['fx'].append(('dmg',"BZZT!",SIGN_X-10,34,BLOOD))     # a hand over his mouth
            if i==2 and 24<=t<b-a: s['fx'].append(('fc_bubble',"...ME?",cx-14,18,cx+2))
    # Tyler: HIT ME AS HARD AS YOU CAN. — and the ear
    if 204<=f<350:
        tx=lerp(W+14,TX,ease((f-204)/14))
        if 210<=f<266: s['fx'].append(('fc_bubble',["HIT ME AS HARD","AS YOU CAN."],TX,8,TX-2))
        if 262<=f<270: pose='hook'; cx+=3
        if 266<=f<314:
            tpose='hurt' if f<290 else 'self'                         # a hand to his ear
            if f<268: s['shake']=rshake(1)
            s['fx'].append(('fc_bubble',["OW! IN THE","EAR, MAN?"],TX,8,TX-2))
    # the brawl: a cloud with everything in it
    if 314<=f<350:
        tx=None; cx=None; s['fx'].append(('fc_brawl',(CX+TX)//2,GROUND-12))
    # the dust clears: only him, punching himself
    if 350<=f<366: tx=None; cx=CX; pose='self' if (f//4)%2 else 'hurt'
    if 426<=f<468:
        pose='hurt' if f<440 else pose; s['fx'].append(('dizzy',CX+1,GROUND-24))
        if 432<=f<466:                                               # Tyler, there all along (or not)
            tx,tpose,talpha=TX,'guard',min(1,(f-432)/6)*max(0,min(1,(466-f)/6))
            s['fx'].append(('fc_bubble',"FIRST RULE.",TX,8,TX-2))
    acts=[]
    if tx is not None: acts.append(actor(build(TYLER,tpose),tx,flip=True,pal=TPAL,alpha=talpha))
    if cx is not None: acts.append(actor(build(NARRATOR,pose),cx,pal=CPAL))
    s['actors']=acts
    s['fx'].append(('fc_crowd','front'))
    return s

CLIPS = [clip('rules', N_, clip_rules), clip('firstrule', N_FIRST, clip_firstrule)]
