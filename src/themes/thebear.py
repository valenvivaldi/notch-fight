"""The Bear: Claude as Carmy (white tee, the blue apron, a towel on the shoulder) at the pass, in the kitchen
with the blue LED clock and its EVERY SECOND COUNTS plaque on the wall over the line. The printer starts spitting tickets (ORDERS IN!);
the brigade (Sydney, Marcus, Tina, Richie) answers YES CHEF!; a pan goes up in flames, BEHIND!, a plate
smashes, the clock racing through a whole day. Close-up: the clock and the plaque, glowing with every second. Carmy
plates the last one with his tweezers (HANDS!), the printer stops, the kitchen goes quiet — YES CHEF."""
from engine import *
from themes.arg import PLAYER                                       # the generic people, in kitchen whites

THEME = 'thebear'
N_ = 384                                                            # a multiple of 12: the guard pose loops
CX = 30                                                             # Carmy at the pass
STEEL, STEEL_D = (186,190,196), (130,134,142)
# Carmy: dark curls, the white tee, the blue apron
CPAL = {'1':(40,30,26),'2':(242,242,242),'3':(44,74,130),'4':(200,200,206)}
CURLS = ["..1.1.1.1...",".11111111...","1111111111.."]
BRIGADE = [('Sydney',72,{'j':(244,244,244),'J':(244,244,244),'s':(150,100,70),'h':(36,26,22),'p':(40,40,46),'k':(30,30,34)}),
           ('Marcus',106,{'j':(244,244,244),'J':(244,244,244),'s':(120,80,56),'h':(24,24,28),'p':(60,60,70),'k':(30,30,34)}),
           ('Tina',140,{'j':(244,244,244),'J':(244,244,244),'s':(200,150,110),'h':(30,24,22),'p':(40,40,46),'k':(30,30,34)}),
           ('Richie',168,{'j':(30,40,70),'J':(30,40,70),'s':(230,190,160),'h':(60,44,34),'p':(30,30,36),'k':(20,20,24)})]

def _carmy(spr):
    g=[list(r) for r in overlay(spr,CURLS,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=top+5: g[y][x]='3' if y>=top+6 and l+2<=x<=r-1 else '2'   # tee, apron over it
            elif c=='o' and top+5<=y<top+8 and x<l: g[y][x]='4'                       # the towel on the arm
    return S([''.join(x) for x in g])
CARMY=variant(_carmy)

# ---- background: the kitchen -------------------------------------------------------------------------
def _kitchen(d):
    d.rectangle([0,0,W,H],fill=(230,230,224))                       # subway tiles
    for y in range(0,44,4):
        d.line([0,y,W,y],fill=(206,206,200))
        for x in range((y//4)%2*4,W,8): d.line([x,y,x,y+3],fill=(206,206,200))
    d.polygon([(118,0),(178,0),(172,16),(124,16)],fill=STEEL_D); d.rectangle([124,16,172,18],fill=STEEL)   # the hood
    d.rectangle([4,22,56,24],fill=STEEL_D)                            # the ticket rail over the pass
    for x0 in (8,30): d.rectangle([x0,26,x0+16,28],fill=(80,80,86)); d.rectangle([x0+2,28,x0+14,29],fill=(255,170,80))   # heat lamps
    d.rectangle([0,38,58,42],fill=STEEL); d.line([0,38,58,38],fill=(230,232,236))       # the pass
    d.rectangle([60,40,W,46],fill=STEEL_D); d.line([60,40,W,40],fill=STEEL)            # the line
    for bx in (128,146,164): d.ellipse([bx-5,38,bx+5,42],fill=(40,40,44)); d.ellipse([bx-3,39,bx+3,41],fill=(70,70,80))   # burners
    for x,y in ((70,30),(84,28),(98,30)): d.ellipse([x-5,y-3,x+5,y+3],fill=(110,110,118))   # pans on the shelf
    d.line([64,34,104,34],fill=STEEL_D)
    d.rectangle([0,46,W,H],fill=(150,140,130))                        # the floor
    for x in range(0,W,10): d.line([x,46,x,H],fill=(136,126,118))
register_bg(THEME, lambda v: (v+100,v+96,v+90), decor=_kitchen)

LED, LED_DIM, PLAQUE = (90,170,255), (18,22,30), (22,40,66)
SEGS={'0':'abcdef','1':'bc','2':'abged','3':'abgcd','4':'fgbc','5':'afgcd','6':'afgedc','7':'abc','8':'abcdefg','9':'abcdfg'}
def seven(d,x,y,w,h,ch,c,t=1):
    """One seven-segment LED digit, top-left at (x,y), w x h, segments t px thick."""
    m=h//2; on=SEGS.get(ch,'')
    seg={'a':(x+t,y,x+w-t,y+t-1),'g':(x+t,y+m-t//2,x+w-t,y+m+(t-1)-t//2),'d':(x+t,y+h-t+1,x+w-t,y+h),
         'f':(x,y+t,x+t-1,y+m-1),'b':(x+w-t+1,y+t,x+w,y+m-1),'e':(x,y+m+1,x+t-1,y+h-t),'c':(x+w-t+1,y+m+1,x+w,y+h-t)}
    for k,r in seg.items(): d.rectangle(r,fill=c if k in on else LED_DIM)

def wall_unit(d,x0,y0,hhmm,flash=0.0,scale=1):
    """The clock over the plaque, as on the wall in the show: blue LED digits, EVERY SECOND COUNTS."""
    k=scale; cw,ch=44*k,15*k
    d.rectangle([x0,y0,x0+cw,y0+ch],fill=(14,14,18),outline=(70,70,78))
    c=tuple(int(lerp(v,255,flash)) for v in LED)
    dw,dh=5*k,9*k; xs=[x0+4*k,x0+12*k,x0+25*k,x0+33*k]
    for i,chd in enumerate(hhmm.replace(':','')): seven(d,xs[i],y0+3*k,dw,dh,chd,c,max(1,k))
    for dy in (5*k,9*k): d.rectangle([x0+21*k,y0+dy,x0+21*k+k-1,y0+dy+k-1],fill=c)
    px0,pw,py0=x0-18*k,80*k,y0+ch+2*k
    d.rectangle([px0,py0,px0+pw,py0+9*k],fill=PLAQUE,outline=(50,70,100))
    if k==1: text(d,"EVERY SECOND COUNTS",px0+3,py0+2,(240,244,250),shadow=None)

@fx('tb_wall')
def _fx_wall(d,im,e,f):
    _,hhmm,flash=e
    if flash>0:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).rectangle([70,0,116,18],fill=int(90*flash))
        im.paste(LED,(0,0),g.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    wall_unit(d,71,1,hhmm,flash)

def clock_at(f):
    """08:17 at rest; during the service it races through one whole day and lands on 08:17 again."""
    m=8*60+17
    if 16<=f<236: m+=int(24*60*ease((f-16)/220))
    m%=24*60; return f"{m//60:02d}:{m%60:02d}"

@fx('tb_tickets')
def _fx_tickets(d,im,e,f):
    """Tickets hanging off the rail (n of them), and the printer spitting one out (printing)."""
    _,n,printing=e
    for i in range(n):
        x=6+i*5; d.rectangle([x,24,x+4,31],fill=(250,250,244),outline=(200,200,190))
        for k in range(3): d.line([x+1,26+k*2,x+3,26+k*2],fill=(120,120,120))
    d.rectangle([44,31,54,37],fill=(50,50,56))                         # the printer
    if printing:
        L=2+(f%6); d.rectangle([47,31-L,51,31],fill=(250,250,244)); d.point((52,33),fill=(90,220,110))

@fx('tb_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(250,250,250),ink=(30,30,30))                     # the engine's bubble (engine/people.py)

@fx('tb_plate')
def _fx_plate(d,im,e,f):
    """A plate: whole (on the pass, with its food) or smashed (pieces on the floor)."""
    _,x,y,state=e; x,y=int(x),int(y)
    if state=='whole':
        d.ellipse([x-6,y-2,x+6,y+1],fill=(250,250,250),outline=(190,190,190))
        d.ellipse([x-2,y-3,x+2,y-1],fill=(150,80,50)); d.point((x+1,y-4),fill=(80,170,70)); d.point((x-2,y-2),fill=(240,200,80))
    else:
        rr=random.Random(4)
        for _ in range(7): px=x+rr.randint(-9,9); d.line([px,y,px+rr.randint(1,3),y-rr.randint(0,1)],fill=(240,240,240))

@fx('tb_tweezers')
def _fx_tweezers(d,im,e,f):
    _,x,y=e; d.line([x,y,x+5,y-6],fill=(200,200,210)); d.line([x+1,y,x+6,y-5],fill=(160,160,170))

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_sign(t,f):
    """Primer plano: the clock and the plaque, as on the wall; every second the digits jump and glow."""
    tick=(f%20)<3
    im=Image.new('RGB',(W,H),(214,216,214)); d=ImageDraw.Draw(im)
    for y in range(0,H,12): d.line([0,y,W,y],fill=(190,192,190))
    for y in range(0,H,12):
        for x in range((y//12)%2*24,W,48): d.line([x,y,x,y+11],fill=(190,192,190))
    secs=17+int(t*3)                                                # 08:17, 08:18, 08:19: one per second
    hhmm=f"08:{secs:02d}"
    k=2; x0=(W-44*k)//2+(random.Random(f).randint(-1,1) if tick else 0); y0=2
    if tick:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).rectangle([x0-6,y0-4,x0+44*k+6,y0+15*k+4],fill=110)
        im.paste(LED,(0,0),g.filter(ImageFilter.GaussianBlur(6))); d=ImageDraw.Draw(im)
    wall_unit(d,x0,y0,hhmm,0.35 if tick else 0.0,scale=k)
    big_text(im,"EVERY SECOND COUNTS",y0+15*k+8,(240,244,250),scale=1,cx=W//2,shadow=None)
    if t<0.05: zoom_lines(d,LED)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def clip_service(f):
    s=scene(f,THEME)
    pose=guard_pose(f)
    rush=16<=f<236
    n=0 if not rush else min(9,(f-16)//8+1)
    if 200<=f<236: n=max(0,9-(f-200)//4)                               # the last ones coming down
    s['under'].append(('tb_wall',clock_at(f),0.5 if rush and (f%20)<2 else 0.0))   # it pulses with every second
    s['under'].append(('tb_tickets',n,16<=f<120))
    bposes=['idle']*4
    if 18<=f<50: s['fx'].append(('tb_bubble',"ORDERS IN!",CX-2,12,CX+4))
    if 50<=f<88:
        for i,(name,x,_) in enumerate(BRIGADE[:3]):
            if (f//10+i)%2==0: s['fx'].append(('tb_bubble',"YES CHEF!",x,18+(i%2)*2))
    if rush: bposes=['attack' if (f//6+i)%2 else 'idle' for i in range(4)]
    # the pan goes up; BEHIND!; a plate on the floor
    if 86<=f<124: s['fx'].append(('fire',146,38,3+(f%3))); s['fx'].append(('smoke',146,24-(f-86)//6,3,(160,160,166)))
    if 90<=f<124: s['fx'].append(('tb_bubble',"BEHIND!",BRIGADE[3][1],14))
    rx=BRIGADE[3][1] if not 90<=f<124 else lerp(168,96,(f-90)/34)
    if 116<=f<128: s['fx'].append(('tb_plate',rx-8,GROUND-1,'smashed')); s['shake']=rshake(1) if f<120 else (0,0)
    if 116<=f<124: s['fx'].append(('dmg',"CRASH",rx-16,GROUND-12,(200,40,40)))
    # close-up: the sign
    if 128<=f<188: s['image']=closeup_sign((f-128)/60,f); return s
    # the last plate: tweezers, HANDS!
    if 188<=f<236:
        pose='punch' if (f//4)%2 and f<212 else pose
        s['fx'].append(('tb_plate',CX+14,38,'whole'))
        if f<212: s['fx'].append(('tb_tweezers',CX+16,34))
        if 202<=f<236: s['fx'].append(('tb_bubble',"HANDS!",CX+10,18))
    # silence; YES CHEF.
    if 240<=f<272: s['fx'].append(('tb_bubble',"...",CX+4,20))
    if 276<=f<310: s['fx'].append(('tb_bubble',"YES CHEF.",BRIGADE[0][1],18))
    acts=[]
    for i,(name,x,pal) in enumerate(BRIGADE):
        bx=rx if name=='Richie' else x
        acts.append(actor(PLAYER[bposes[i]],bx,flip=name=='Richie' and 90<=f<124,pal=pal))
    acts.append(actor(CARMY[pose],CX,pal=CPAL))
    s['actors']=acts
    return s

CLIPS = [clip('service', N_, clip_service)]
