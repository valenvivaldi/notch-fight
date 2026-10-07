"""Argentina sub-theme "arg-alejo": Alejo y Valentina (LocoArts), no fight. The living room of the pixel-art
reference: the pink wall, the brown floor, the brown couch, the old TV on its stand, the framed CUADRITO.
Claude as Carlitox (the green hair everywhere, a pale face with big round eyes, the navy tank top, dark
grey trousers) on the couch next to Alejo (black hair, purple t-shirt); Valentina (long black hair, pink)
standing by. Clip `patas`: MIRA COMO REVOLEO LAS PATAS — and he does, his legs spinning from the hip like
a fan, faster and faster; close-up: the grin and the blur, HOLA, VENGO A REVOLEAR LAS PATAS!; Alejo and
Valentina just look. The look of the series: thick black outlines, flat colours, nothing shaded.
The cast (CARLITOX_UP, CAST, carlitox_face) is shared with arg-alejo-flotar."""
from engine import *

THEME = 'arg-alejo'
N_ = 288                                                            # a multiple of 12
PINK, FLOOR = (246,196,200), (90,58,20)
COUCH, COUCH_D = (150,100,58), (110,72,40)
INK = (20,20,20)
VX, AX, CX, TVX = 40, 84, 112, 160                                  # Valentina, Alejo, Carlitox, the TV
HIP = GROUND-5                                                      # where they sit: hips on the seat

# the cast: 1/2 green hair, p pale skin, w eye white, K pupil, n navy tank top, g dark grey trousers, k shoes,
# h black hair, v purple t-shirt, m pink top, r mouth
CAST = {'1':(80,200,70),'2':(46,150,50),'p':(240,226,214),'w':(255,255,255),'K':INK,'n':(34,44,96),
        'g':(70,70,78),'k':(30,30,34),'h':(24,22,26),'v':(130,60,180),'m':(240,120,170),'r':(200,70,70)}
CARLITOX_UP = S([                                                  # floating: arms out, legs hanging
"...1.1.2.1.1...","..11112111211..",".1121111112111.",".11ppppppppp11.","..1pwwwpwwwp1..",
"..1pwKwpwKwp1..","...pwwwpwwwp...","...ppppppppp...","....pKKKKKp....",".....ppppp.....",
"pp..nnnnnnn..pp",".pppnnnnnnnppp.","....nnnnnnn....","....nnnnnnn....","....ggggggg....",
"....ggg.ggg....","....ggg.ggg....","....ggg.ggg....","...kkkk.kkkk...",])
CARLITOX_SIT = S(CARLITOX_UP[:10]+[                                 # sitting: hands on the seat, no legs
"....nnnnnnn....","...pnnnnnnnp...","...pnnnnnnnp...","...pnnnnnnnp...","....ggggggg....",])
CARLITOX_WAVE = S(CARLITOX_UP[:10]+[                                # arms flung up while the legs go
"pp..nnnnnnn..pp",".p..nnnnnnn..p.","....nnnnnnn....","....nnnnnnn....","....ggggggg....",])
ALEJO = S([                                                         # sitting, thighs forward, shins down
"...hhhhhhh....","..hhhhhhhhh...","..hpppppphh...","..pwwwpwwwp...","..pwKwpwKwp...","..ppppppppp...",
"...ppKKKpp....","....ppppp.....","..vvvvvvvvv...",".pvvvvvvvvvp..",".pvvvvvvvvvp..","..vvvvvvvvv...",
"..ggggggggggg.","..ggggggggggg.","..........gg..","..........gg..","..........gg..","..........kkk.",])
VALENTINA = S([
"...hhhhhhh...","..hhhhhhhhh..","..hpppppphh..",".hpwwwpwwwph.",".hpwKwpwKwph.",".hppppppppph.",
".hhpprrrpphh.",".hh.ppppp.hh.",".hhmmmmmmmhh.","..pmmmmmmmp..","..pmmmmmmmp..","...mmmmmmm...",
"...mmmmmmm...","....pp.pp....","....pp.pp....","....pp.pp....","...kkk.kkk...",])

# ---- the living room -------------------------------------------------------------------------------------
def _living(d):
    d.rectangle([0,0,W,H],fill=PINK)
    d.rectangle([0,GROUND+1,W,H],fill=FLOOR); d.line([0,GROUND+1,W,GROUND+1],fill=INK)
    d.rectangle([14,8,48,18],fill=(170,210,240),outline=INK)             # the CUADRITO
    d.line([31,4,20,8],fill=INK); d.line([31,4,42,8],fill=INK)
    text(d,"CUADRITO",16,11,INK,shadow=None)
    x=TVX                                                               # the TV on its stand
    d.rectangle([x-14,GROUND-12,x+14,GROUND],fill=(130,80,40),outline=INK); d.rectangle([x-12,GROUND-8,x+2,GROUND-3],fill=(80,50,24))
    d.rectangle([x-12,GROUND-30,x+12,GROUND-12],fill=(90,90,96),outline=INK); d.rectangle([x-9,GROUND-27,x+5,GROUND-15],fill=(60,64,70),outline=INK)
    text(d,"T.V",x-6,GROUND-24,(20,20,20),shadow=None)
    d.line([x,GROUND-30,x-5,GROUND-37],fill=INK); d.line([x,GROUND-30,x+6,GROUND-36],fill=INK)
    d.rectangle([62,GROUND-26,134,HIP-1],fill=COUCH,outline=INK)         # the couch: back...
    for x in (86,110): d.line([x,GROUND-25,x,HIP-2],fill=COUCH_D)
    d.rectangle([62,HIP-1,134,GROUND-2],fill=COUCH_D,outline=INK)        # ...and seat
    for lx in (64,132): d.line([lx,GROUND-2,lx,GROUND],fill=INK)
register_bg(THEME, lambda v: (v+40,v+30,v+10), decor=_living)

@fx('av_arms')
def _fx_arms(d,im,e,f):
    """The couch's arms, in front of the two at the ends."""
    for ax in (56,132): d.rectangle([ax,GROUND-16,ax+6,GROUND-2],fill=COUCH,outline=INK)

@fx('av_legs')
def _fx_legs(d,im,e,f):
    """Carlitox's legs from the hip: sitting (thighs forward, shins down), or spinning like a fan (angle a)."""
    _,x,y,a,blur=e; x,y=int(x),int(y)
    grey,shoe=CAST['g'],CAST['k']
    if a is None:
        for dy in (0,2):
            d.line([x,y+dy,x+8,y+dy],fill=grey,width=2); d.line([x+8,y+dy,x+8,y+dy+5],fill=grey,width=2)
            d.line([x+8,y+dy+6,x+11,y+dy+6],fill=shoe,width=2)
        return
    for k in range(int(blur)):                                       # motion arcs behind the spin
        d.arc([x-12,y-12,x+12,y+12],math.degrees(a)-70-k*25,math.degrees(a)-45-k*25,fill=(150,140,140))
        d.arc([x-12,y-12,x+12,y+12],math.degrees(a)+110-k*25,math.degrees(a)+135-k*25,fill=(150,140,140))
    for s in (0,math.pi):
        ex,ey=x+math.cos(a+s)*11,y+math.sin(a+s)*11
        d.line([x,y,ex,ey],fill=INK,width=4); d.line([x,y,ex,ey],fill=grey,width=2)
        d.ellipse([ex-2,ey-2,ex+2,ey+2],fill=shoe)
    d.ellipse([x-2,y-2,x+2,y+2],fill=grey,outline=INK)

@fx('av_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(255,255,255),ink=INK)                     # the engine's bubble (engine/people.py)

# ---- close-up -------------------------------------------------------------------------------------------
def carlitox_face(d,ox):
    """Carlitox's face for close-ups (x ox..ox+56): the green hair everywhere, the big round eyes, the grin."""
    rr=random.Random(2)
    for k in range(24):
        a=rr.uniform(math.pi*0.95,math.pi*2.05); L=rr.randint(18,32)
        d.line([ox+28,26,ox+28+math.cos(a)*L*1.2,26+math.sin(a)*L],fill=CAST['1'] if k%3 else CAST['2'],width=4)
    d.ellipse([ox+6,8,ox+50,58],fill=CAST['p'],outline=INK,width=2)
    for ex in (ox+18,ox+38):
        d.ellipse([ex-6,20,ex+6,34],fill=(255,255,255),outline=INK,width=2); d.ellipse([ex-2,25,ex+2,30],fill=INK)
    d.chord([ox+16,38,ox+42,52],0,180,fill=(255,255,255),outline=INK,width=2)

def closeup_patas(t,f):
    """Primer plano: Carlitox's grin, the legs a blur below — HOLA, VENGO A REVOLEAR LAS PATAS!"""
    im=Image.new('RGB',(W,H),PINK); d=ImageDraw.Draw(im)
    carlitox_face(d,14)
    for k in range(3):
        a=f*0.9+k*0.6; d.arc([24,48,60,H+20],math.degrees(a),math.degrees(a)+50,fill=(90,90,96),width=3)
    if t>=0.2:
        big_text(im,"HOLA, VENGO A",8,INK,scale=2,cx=128,shadow=None)
        big_text(im,"REVOLEAR",24,INK,scale=2,cx=128,shadow=None)
        big_text(im,"LAS PATAS!",40,INK,scale=2,cx=128,shadow=None)
    if t<0.05: zoom_lines(d,INK)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
def spin_angle(f):
    """How far the legs have turned by frame f: they spin up and down again between 60 and 230."""
    return sum(0.15+0.85*math.sin(math.pi*min(1,((g-60)/170)*1.1)) for g in range(60,f))*0.9

def clip_patas(f):
    s=scene(f,THEME)
    legs=(None,0); carl=CARLITOX_SIT
    if 14<=f<64: s['fx'].append(('av_bubble',"MIRA COMO REVOLEO LAS PATAS",CX,4,CX))
    if 60<=f<230:
        speed=0.15+0.85*math.sin(math.pi*min(1,((f-60)/170)*1.1))
        legs=(spin_angle(f),min(3,speed*4))
        if speed>0.6: carl=CARLITOX_WAVE if (f//5)%2 else CARLITOX_SIT; s['shake']=rshake(1) if f%3==0 else (0,0)
    if 120<=f<180: s['image']=closeup_patas((f-120)/60,f); return s
    if 196<=f<236: s['fx'].append(('av_bubble',"...",AX,8,AX))
    s['actors']=[actor(VALENTINA,VX,pal=CAST),actor(ALEJO,AX,pal=CAST),actor(carl,CX,y=HIP+1,pal=CAST)]
    s['fx'].append(('av_legs',CX+1,HIP,legs[0],legs[1]))
    s['fx'].append(('av_arms',))
    return s

CLIPS = [clip('patas', N_, clip_patas)]
