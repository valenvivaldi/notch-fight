"""Coraline (2009): Claude as Coraline vs the Other Mother (the Beldam), in the Pink Palace.
Stop-motion: characters move on twos with a small hand-animated wobble. The little door opens onto the
pulsing tunnel; in the warm Other World the Other Mother offers a box with two buttons and a needle:
WE ONLY WANT YOU TO STAY. — NO. The world drains to grey and cobwebs and she stretches into her spider
form. Close-up: through the seeing stone, the ghost children's eyes light up one by one. Coraline runs,
the cat ahead of her, the needle hand behind; she slams the little door and turns the button key: CLICK."""
import zlib
from engine import *
from themes.spidey import twos      # characters on twos, like the Spider-Verse look (changing it in spidey changes this clip)

THEME = 'coraline'
N_ = 336

INK = (20,16,16)
# Coraline: yellow raincoat, blue hair with the dragonfly clip, yellow boots
CPAL = {'b':(58,96,226), 'B':(34,62,170), 'y':(250,210,40), 'Y':(206,164,24), 'g':(120,230,160)}
# the Other Mother: black hair, pale skin, button eyes with white thread, a too-wide red smile, maroon dress
BPAL = {'k':(18,16,20), 'P':(232,210,196), 'X':(10,8,10), 'W':(236,236,236), 'r':(190,30,40), 'd':(110,30,46)}

HAIR = [".bbbbbbbbbb.", "bbbbbbbbbbbb", "bBbbbbbbbBbg"]

def _coraline(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(top,min(top+3,h)):                                   # hair down the sides of the face
        for x in (l-1,r+1):
            if 0<=x<len(g[0]) and g[y][x]=='.': g[y][x]='b'
    for y in range(top+5,h):                                            # the raincoat and the boots
        for x in range(len(g[0])):
            if g[y][x]=='O': g[y][x]='y' if y<top+8 else 'Y'
            elif g[y][x]=='o' and y>=h-2: g[y][x]='y'
    return S([''.join(x) for x in g])
CORA=variant(_coraline)

BELDAM=poses(S([
"....kkkkk.....","...kkkkkkk....","..kkPPPPPkk...","..kPXWPXWPk...","..kPXXPXXPk...","..kPPPPPPPk...",
"...PrrrrrP....","....PPPPP.....",".....PPP......","...ddddddd....","..ddddddddd...","..PdddddddP...",
"..Pddd.dddP...","..P.ddddd.P...","....ddddd.....","...ddddddd....","...ddddddd....","..ddddddddd...",
"..ddddddddd...","...kk...kk....","...kk...kk....",]),11,'P',4)

def wobble(g,who):
    """Stop-motion: a 1 px nudge on some poses, as if the puppet was moved by hand."""
    g%=N_                                                            # the same nudges every loop
    return (zlib.crc32(f'{who}{g}'.encode())%5==0)*(1 if (g//2)%2 else -1)

# ---------------------------------------------------------------- the room, in three worlds
WORLDS = {  # wallpaper, stripes, floor
    'real':  ((70,78,96),(60,68,86),(52,44,44)),
    'other': ((168,78,64),(190,100,76),(96,52,40)),
    'grey':  ((56,56,60),(48,48,52),(36,34,34)),
}
DOOR=(60,72,40)       # the little door: x0, x1, top

register_bg(THEME, lambda v: (v//2+10,v//2+8,v//2+10))     # the room itself is drawn by cor_room

def _mix(a,b,t): return tuple(int(lerp(a[i],b[i],t)) for i in range(3))

@fx('cor_room')
def _fx_room(d,im,e,f):
    """The drawing room: striped wallpaper, a window, the little door; w0 -> w1 by t."""
    _,w0,w1,t,door_open=e
    wall,stripe,floor=(_mix(WORLDS[w0][i],WORLDS[w1][i],t) for i in range(3))
    d.rectangle([0,0,W,GROUND],fill=wall)
    for x in range(0,W,8): d.line([x,0,x,GROUND],fill=stripe)
    d.rectangle([0,GROUND-3,W,GROUND],fill=floor)
    d.rectangle([118,8,150,34],fill=_mix((24,30,44),(236,190,120),t if w1=='other' else 0),outline=(40,34,34))
    d.line([134,8,134,34],fill=(40,34,34)); d.line([118,21,150,21],fill=(40,34,34))
    x0,x1,top=DOOR
    if door_open: d.rectangle([x0,top,x1,GROUND-3],fill=(20,14,40))
    else:
        d.rectangle([x0,top,x1,GROUND-3],fill=stripe,outline=_mix(stripe,(0,0,0),0.4))
        d.point((x1-2,top+10),fill=(200,170,90))
    if w1=='grey' and t>0.3:                                              # cobwebs in the corners
        c=(150,150,156)
        for cx,cy,sx,sy in ((0,0,1,1),(W-1,0,-1,1)):
            for k in range(5): d.line([cx,cy,cx+sx*(28-k*5),cy+sy*k*5],fill=c)
            for r in (8,16,24): d.arc([cx-r,cy-r,cx+r,cy+r],0 if sx>0 else 90,90 if sx>0 else 180,fill=c)

@fx('cor_rain')
def _fx_rain(d,im,e,f):
    rr=random.Random((f%48)*5)                                       # a 48-frame cycle: it loops
    for _ in range(8):
        x=rr.randint(119,149); y=rr.randint(9,30); d.line([x,y,x-1,y+3],fill=(140,160,200))

@fx('cor_tunnel')
def _fx_tunnel(d,im,e,f):
    """The tunnel beyond the little door: pulsing violet-blue rings."""
    x0,x1,top=DOOR; cx,cy=(x0+x1)//2,(top+GROUND-3)//2
    for k in range(4):
        r=((f*0.5+k*3)%12)+1
        d.ellipse([cx-r*0.5,cy-r*0.8,cx+r*0.5,cy+r*0.8],outline=(120,90,230) if k%2 else (80,150,240))

@fx('cor_box')
def _fx_box(d,im,e,f):
    """The little box: two black buttons, a needle, black thread."""
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x,y,x+8,y+4],fill=(120,70,50),outline=(60,30,20))
    for bx in (x+2,x+5): d.rectangle([bx,y+1,bx+1,y+2],fill=(10,8,10))
    d.line([x+1,y-3,x+7,y-5],fill=(200,200,210)); d.point((x+7,y-5),fill=(255,255,255))

@fx('cor_balloon')
def _fx_balloon(d,im,e,f):
    """Speech balloon, kept inside the panel, tail down to the speaker."""
    _,txt,cx,y=e; w=len(txt)*4+5; x=max(1,min(W-w-2,int(cx-w/2))); tx=max(x+3,min(x+w-3,cx))
    d.rectangle([x,y,x+w,y+9],fill=(245,242,236),outline=INK); d.polygon([(tx-2,y+9),(tx+2,y+9),(tx+2,y+13)],fill=(245,242,236))
    text(d,txt,x+3,y+2,INK,shadow=None)

@fx('cor_spider')
def _fx_spider(d,im,e,f):
    """The Beldam's spider form: needle legs, a thin black body, the cracked face with button eyes,
    needle fingers reaching left. alpha 0..1 (it grows in over her)."""
    _,x,alpha,reach=e
    L=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(L); a=int(255*alpha)
    blk=(14,12,16,a); needle=(200,204,214,a)
    for k,(fx_,fy) in enumerate(((-22,GROUND),(-10,GROUND),(12,GROUND),(24,GROUND))):   # needle legs
        kx=x+fx_*0.6; ky=GROUND-30-(k%2)*4
        dd.line([x,GROUND-26,kx,ky],fill=blk,width=2); dd.line([kx,ky,x+fx_,fy],fill=blk,width=1)
        dd.point((x+fx_,fy),fill=needle)
    dd.polygon([(x-5,GROUND-30),(x+5,GROUND-30),(x+2,GROUND-12),(x-2,GROUND-12)],fill=blk)     # body
    dd.ellipse([x-6,GROUND-44,x+6,GROUND-30],fill=(236,226,220,a))                             # face
    dd.line([x-2,GROUND-44,x+1,GROUND-38],fill=(40,30,30,a)); dd.line([x+1,GROUND-38,x-1,GROUND-33],fill=(40,30,30,a))
    for ex in (x-3,x+2): dd.rectangle([ex,GROUND-40,ex+2,GROUND-38],fill=(10,8,10,a)); dd.point((ex+1,GROUND-39),fill=(236,236,236,a))
    dd.line([x-4,GROUND-34,x+4,GROUND-34],fill=(170,20,30,a))
    hx=x-8-reach                                                                              # the arm and needle fingers
    dd.line([x-4,GROUND-28,hx,GROUND-24],fill=blk,width=1)
    for k in (-2,0,2): dd.line([hx,GROUND-24,hx-6,GROUND-24+k],fill=needle)
    im.paste(L,(0,0),L)

@fx('cor_cat')
def _fx_cat(d,im,e,f):
    """The black cat, running (legs alternate)."""
    _,x,y=e; x,y=int(x),int(y); c=(16,14,18)
    d.rectangle([x-4,y-4,x+3,y-2],fill=c); d.rectangle([x-6,y-6,x-3,y-3],fill=c)
    d.point((x-6,y-7),fill=c); d.point((x-4,y-7),fill=c); d.point((x-5,y-5),fill=(120,200,120))
    d.line([x+3,y-3,x+6,y-6],fill=c)
    k=(f//2)%2
    for lx in ((x-4,x+2) if k else (x-3,x+1)): d.line([lx,y-2,lx+(1 if k else -1),y],fill=c)

@fx('cor_key')
def _fx_key(d,im,e,f):
    """The button key in the lock, turning."""
    _,x,y,k=e; d.ellipse([x-2,y-2,x+2,y+2],fill=(14,12,16)); d.point((x,y),fill=(90,90,96))
    a=min(1,k/6)*math.pi/2; d.line([x,y,x+math.cos(a)*4,y+math.sin(a)*4],fill=(14,12,16))

@fx('cor_sfx')
def _fx_sfx(d,im,e,f):
    _,txt,cx,y,c=e; big_text(im,txt,y,c,cx=int(cx),shadow=(0,0,0),outline=(0,0,0))

def closeup_stone(t,f):
    """Primer plano: Coraline's eye behind the seeing stone; through its hole, the ghost children's eyes
    light up one by one. No text."""
    im=Image.new('RGB',(W,H),(30,30,34)); d=ImageDraw.Draw(im)
    for x in range(0,W,8): d.line([x,0,x,H],fill=(38,38,42))
    d.rectangle([0,0,40,H],fill=(217,119,87))                                             # her face, in profile
    hair=[(0,0),(34,0),(38,6),(30,10),(36,18),(26,22),(32,32),(22,36),(26,46),(14,50),(0,50)]
    d.polygon(hair,fill=CPAL['b'])
    for a,b2 in (((6,4),(24,30)),((14,2),(28,20)),((4,20),(16,44))): d.line([a,b2],fill=CPAL['B'])
    d.polygon([(0,50),(40,52),(52,H),(0,H)],fill=CPAL['y']); d.line([0,54,44,56],fill=CPAL['Y'])   # the raincoat
    d.point((30,4),fill=CPAL['g']); d.point((31,3),fill=CPAL['g']); d.point((29,3),fill=CPAL['g'])  # the dragonfly clip
    d.polygon([(40,60),(92,2),(144,60)],fill=(92,110,96),outline=(60,72,62))              # the seeing stone
    for k in range(6): d.line([54+k*12,58,70+k*10,30],fill=(80,96,84))
    cx,cy,r=92,40,12
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(16,16,22))
    for i,(ex,ey) in enumerate(((cx-6,cy-3),(cx+5,cy-5),(cx,cy+5))):                    # the ghost eyes
        if t>=0.25+i*0.18:
            glow=(200,236,255) if (f//3+i)%3 else (140,200,255)
            d.ellipse([ex-2,ey-1,ex+2,ey+1],fill=glow); d.point((ex,ey),fill=(255,255,255))
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(60,72,62))
    for k,fy in enumerate((50,54,58)):                                                   # her fingers on the stone
        d.rounded_rectangle([40+k*2,fy,54+k*2,fy+3],radius=1,fill=(217,119,87),outline=(168,80,54))
    if t<0.06: zoom_lines(d,(200,200,210))
    return im

# ---------------------------------------------------------------- the clip
BX=140                # where the Other Mother stands

def clip_buttons(f):
    g=twos(f)
    s=scene(f,THEME)
    world=('real','real',0.0); door_open=False
    cx_,cy_,cpose,cflip,calpha=30,GROUND,guard_pose(g),False,1.0
    bx,bpose,bvis=None,'idle',True
    spider=None
    # 1) the little door opens; through the tunnel into the Other World
    if 14<=f<50: door_open=f>=18; s['under'].append(('cor_tunnel',)) if f>=18 else None
    if 20<=g<36: cx_,cpose=ez(30,66,(g-20)/16),'dash'
    if 36<=g<44: cx_,calpha=66,max(0,1-(g-36)/8)
    if 44<=f<50: world=('real','other',(f-44)/6); s['flash']=0.4; s['fc']=(66,GROUND-10); s['flashc']=(170,130,250)
    if 44<=g<56: cx_,calpha=66,min(1,(g-44)/8)
    if 50<=f<110: world=('other','other',1.0)
    if 56<=g<70: cx_=ez(66,96,(g-56)/14)
    if g>=70: cx_=96
    # 2) the offer: the box with the buttons and the needle; NO.
    if 50<=f<150: bx=BX
    if 60<=f<120: s['fx'].append(('cor_box',BX-14,GROUND-12)); bpose='attack' if f<104 else 'idle'
    if 60<=f<120: s['fx'].append(('cor_balloon',"WE ONLY WANT YOU TO STAY.",BX,4))          # 3 s
    if 104<=f<134: s['fx'].append(('cor_balloon',"NO.",96,20)); cpose='guard'               # 1.5 s
    # 3) the world drains; she stretches into the spider
    if 110<=f<150: world=('other','grey',min(1,(f-110)/24))
    if 120<=f<150:
        p=min(1,(f-120)/20); spider=(BX,p,0); bvis=(g//2)%2==0 if p<1 else False
        if f<132 and f%3==0: s['shake']=rshake(1)
    # 4) close-up: the seeing stone
    if 150<=f<195: s['image']=closeup_stone((f-150)/45,f); return s
    # 5) the escape: the cat ahead, the needle hand behind; the door, the key, CLICK
    if 195<=f<280: world=('grey','grey',1.0)
    if 195<=f<238:
        spider=(ez(BX,110,(f-195)/40),1,min(40,(f-195)*1.4)); bvis=False
        cx_,cflip,cpose=ez(96,66,(g-195)/30),True,'dash'
        s['fx'].append(('cor_cat',ez(90,56,(f-195)/24),GROUND))
        if g>=226: calpha=max(0,1-(g-226)/10)
        door_open=True
    if 238<=f<280:                                                            # the real side of the door
        world=('real','real',1.0); spider=None; bvis=False
        cx_,cflip,cpose=76,True,'punch' if f<250 else guard_pose(g)
        door_open=f<244
        if 238<=f<246:
            for k in (-2,0,2): s['fx'].append(('mote',DOOR[0]+6-(246-f),GROUND-14+k,(210,214,224)))  # needles at the gap
        if 244<=f<264: s['fx'].append(('cor_key',DOOR[1]-2,GROUND-14,f-244))
        if 244<=f<248: s['shake']=rshake(2)
        if 246<=f<276: s['fx'].append(('cor_sfx',"CLICK.",96,6,(245,242,236)))                  # 1.5 s
    # 6) back in the real room, rain; to the neutral pose
    if f>=280: world=('real','real',1.0)
    if 280<=g<306: cx_,cflip,cpose=ez(76,30,(g-280)/26),True,guard_pose(g)
    if g>=306: cx_,cflip=30,False
    s['under'].insert(0,('cor_room',world[0],world[1],world[2],door_open))
    if world[1]=='real' and world[2]>=1 or f<44: s['under'].insert(1,('cor_rain',))
    if door_open and (f<50 or 195<=f<244): s['under'].append(('cor_tunnel',))
    acts=[]
    if bx is not None and bvis: acts.append(actor(BELDAM[bpose],bx+wobble(g,'b'),flip=True,pal=BPAL))
    if spider: s['fx'].insert(0,('cor_spider',*spider))
    if calpha>0: acts.append(actor(CORA[cpose],cx_+wobble(g,'c'),cy_,flip=cflip,pal=CPAL,alpha=calpha))
    s['actors']=acts
    return s

CLIPS = [clip('buttons', N_, clip_buttons)]
