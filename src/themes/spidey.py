"""Spider-Verse (Into the Spider-Verse): Claude as Miles Morales vs the Prowler, in Brooklyn at night.
The Prowler drops in; Miles camouflages — the screen splits into comic panels as the claws cut empty
air — then a kick sends him flying. Close-up: A LEAP OF FAITH. From a rooftop he jumps and the city
turns upside down, its lights streaking as he falls "up"; THWIP. He swings back, webs the Prowler to
a wall and finishes him with a venom blast (ZZAKT!); police lights, and the Prowler is gone.
The Spider-Verse look lives here for the sub-themes: characters animate on twos (a new pose every
other frame) while effects run on ones; magenta/cyan rim light; halftone shadows; misregistered
red/blue on big hits; comic panels, sound effects and a narration caption."""
from PIL import ImageChops
from engine import *

THEME = 'spidey'
N_ = 329

VENOM, VENOM_HI = (255,210,60), (255,250,200)
CAPTION = (255,214,80)
MAGENTA, CYAN = (255,70,190), (70,220,255)
GREEN = (120,255,150)
# Miles: black suit, faint web lines, red spider, red gloves and soles, big white eyes
MPAL = {'s':(38,38,48), 'w':(66,66,82), 'r':(220,36,48), 'e':(250,250,250)}
# the Prowler: hood and cape, purple armour, green eyes and gauntlets
PPAL = {'p':(112,62,156), 'q':(150,96,196), 'k':(26,24,34), 'v':GREEN}

def twos(f): return f-f%2       # characters move on twos: the Spider-Verse stutter (coraline uses it too)

def _miles(spr):
    g=[list(r) for r in spr]
    top,l,r=body_box(spr); h=len(g); w=len(g[0])
    for y in range(h):
        for x in range(w):
            c=g[y][x]
            if c=='O': g[y][x]='w' if (x*2+y)%6==0 and y<top+8 else 's'           # the suit, a web pattern
            elif c=='o':                                                            # arms and legs
                edge=(x==0 or g[y][x-1]=='.') or (x==w-1 or g[y][x+1]=='.')
                g[y][x]='r' if (y>=h-1 or (y<top+8 and edge and (x<l or x>r))) else 's'   # red soles and gloves
            elif c=='K': g[y][x]='e'
    cx=(l+r)//2
    for dx,dy in ((0,4),(0,5),(-1,5),(1,5),(0,6),(-1,7),(1,7)):                     # the red spider
        if 0<=top+dy<h and g[top+dy][cx+dx] in 'sw': g[top+dy][cx+dx]='r'
    return S([''.join(x) for x in g])
MILES=variant(_miles)

PROWLER=poses(S([
"......kkkk........",".....kppppk.......","....kppqppk.......","....kpvvpvvk......","....kppppppk......",
".....kppppk.......","...kkkkkkkkkk.....","..kkkpqkkqpkkk....",".kkkppqkkqppkkk...",".kkvkppkkppkvkk...",
".kkv.kkkkkk.vkk...",".kk..kkkkkk..kk...",".k...pp..pp...k...",".....pp..pp.......",".....kk..kk.......",
".....kk..kk.......","....kkk..kkk......",]),9,'v',4)

GRIP = {'punch':(16,5), 'dash':(16,5), 'charge':(15,5), 'armsup':(12,0), 'guard':(13,4), 'guard2':(13,4)}
def hand(pose,x,feet,flip=False):
    col,row=GRIP[pose]; return hand_at(MILES[pose],x,int(feet),flip,col,row,h=11)

# ---------------------------------------------------------------- Brooklyn
def _halftone(d,x0,y0,x1,y1,c,dens=1.0):
    for y in range(y0,y1,2):
        for x in range(x0+(y//2)%2,x1,3):
            if (x*7+y*13)%10<6*dens: d.point((x,y),fill=c)

def _brooklyn(d):
    """Brooklyn at night: halftone sky, brick walls with tags, fire escapes, a street lamp, the B."""
    _halftone(d,0,0,W,30,(46,38,92),0.7)
    blds=[(0,18,34,(40,22,34)),(34,10,30,(30,26,50)),(64,22,36,(44,26,30)),(100,6,30,(30,26,50)),(130,16,55,(40,22,34))]
    for x0,top,w,c in blds:
        d.rectangle([x0,top,x0+w,GROUND],fill=c)
        for y in range(top+3,GROUND,4):                                         # brick courses
            d.line([x0,y,x0+w,y],fill=tuple(max(0,v-10) for v in c))
            for x in range(x0+((y//4)%2)*4,x0+w,8): d.point((x,y+1),fill=tuple(max(0,v-12) for v in c))
        for wy in range(top+5,GROUND-16,8):
            for wx in range(x0+4,x0+w-4,8):
                if (wx*13+wy*7)%9<4: d.rectangle([wx,wy,wx+2,wy+3],fill=(250,196,96))
        _halftone(d,x0,GROUND-14,x0+w,GROUND,(16,12,24),0.8)
    for y in range(24,GROUND-8,10):                                             # a fire escape
        d.line([70,y,94,y],fill=(90,90,110)); d.line([70,y-4,94,y-4],fill=(70,70,86))
        d.line([74 if (y//10)%2 else 90,y,90 if (y//10)%2 else 74,y+10],fill=(90,90,110))
    for tag,x,c in (("NYC",6,MAGENTA),("BK",40,CYAN),("ART",136,(250,210,60))):    # tags on the walls
        text(d,tag,x+1,GROUND-11,(0,0,0),shadow=None); text(d,tag,x,GROUND-12,c,shadow=None)
    d.line([118,GROUND,118,24],fill=(70,70,86)); d.line([118,24,124,24],fill=(70,70,86))   # street lamp
    d.rectangle([123,24,126,26],fill=(255,236,170))
    d.ellipse([160,GROUND-26,168,GROUND-18],fill=(240,140,40)); text(d,"B",163,GROUND-24,(20,20,20),shadow=None)
register_bg(THEME, lambda v: (v//2+6,v//3+4,v//2+18), decor=_brooklyn)

# ---------------------------------------------------------------- the Spider-Verse look
@fx('sv_lamp')
def _fx_lamp(d,im,e,f):
    """The street lamp's cone of light (blended)."""
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).polygon([(122,27),(127,27),(140,GROUND),(108,GROUND)],fill=34)
    im.paste((255,230,160),(0,0),L)

@fx('sv_rim')
def _fx_rim(d,im,e,f):
    """Rim light: magenta on the sprite's left edge, cyan on its right edge (Spider-Verse lighting)."""
    _,key,x,feet,flip,alpha=e
    spr=MILES[key]; px=im.load(); ox,oy=origin(spr,x,int(feet)); w=len(spr[0])
    for yy,row in enumerate(spr):
        cells=[xx for xx,ch in enumerate(row) if ch!='.']
        if not cells: continue
        for xx,c in ((cells[0],MAGENTA),(cells[-1],CYAN)):
            sx=ox+((w-1-xx) if flip else xx)
            if flip: c=CYAN if c==MAGENTA else MAGENTA
            blend(px,sx,oy+yy,c,0.75*alpha)

@fx('sv_split')
def _fx_split(d,im,e,f):
    """Misregistered print: red and blue channels pushed n px apart."""
    _,n=e; r,g,b=im.split()
    im.paste(Image.merge('RGB',(ImageChops.offset(r,-n,0),g,ImageChops.offset(b,n,0))))

@fx('sv_sfx')
def _fx_sfx(d,im,e,f):
    """Comic sound effect: big letters with a black outline, wobbling a little."""
    _,txt,cx,y,c=e; big_text(im,txt,y+(f%4<2),c,cx=int(cx),shadow=(0,0,0),outline=(0,0,0))

@fx('sv_caption')
def _fx_caption(d,im,e,f):
    """Narration caption box (Miles' inner voice)."""
    _,txt,cx,y=e; w=len(txt)*4+6; x=max(1,min(W-w-2,int(cx-w/2)))
    d.rectangle([x+1,y+1,x+w+1,y+10],fill=(0,0,0)); d.rectangle([x,y,x+w,y+9],fill=CAPTION,outline=(20,16,16))
    text(d,txt,x+3,y+2,(20,16,16),shadow=None)

@fx('sv_web')
def _fx_web(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(240,240,250)); d.point((x1,y1),fill=(255,255,255))

@fx('sv_glob')
def _fx_glob(d,im,e,f):
    """A web glob pinning something: a white splat with strands."""
    _,x,y=e
    for a in (-30,0,30):                                                        # strands back to the wall
        d.line([x,y,x+8,y+a/10],fill=(210,210,224))
    d.ellipse([x-2,y-2,x+2,y+1],fill=(236,236,244))

@fx('sv_claw')
def _fx_claw(d,im,e,f):
    """The Prowler's claws cutting the air: three green arcs that fade."""
    _,x,y,k=e
    if k>=6: return
    for j in (-3,0,3): d.arc([x-8,y-8+j,x+8,y+8+j],200+k*10,300+k*10,fill=GREEN if k<3 else (60,140,80))

@fx('sv_trail')
def _fx_trail(d,im,e,f):
    """The gauntlets' green trail as the Prowler lunges."""
    _,x0,x1,y=e
    for x in range(int(min(x0,x1)),int(max(x0,x1)),2): d.point((x,y+(x%3)-1),fill=(70,170,100))

@fx('sv_venom')
def _fx_venom(d,im,e,f):
    """Venom blast: jagged yellow arcs from the hand to the target, and a ring at the impact."""
    _,x0,y0,x1,y1,k=e; rr=random.Random(f*11)
    for n in range(4):
        pts=[(x0,y0)]
        for j in range(1,7):
            t=j/7; pts.append((lerp(x0,x1,t)+rr.randint(-2,2),lerp(y0,y1,t)+rr.randint(-5,5)))
        pts.append((x1,y1)); d.line(pts,fill=VENOM if n else VENOM_HI,width=1)
    r=4+k*3; d.ellipse([x1-r,y1-r*0.7,x1+r,y1+r*0.7],outline=VENOM if k%2 else VENOM_HI)
    d.ellipse([x1-3,y1-3,x1+3,y1+3],fill=VENOM_HI)

@fx('sv_charge')
def _fx_charge(d,im,e,f):
    """Hands crackling before the blast."""
    _,x,y=e; rr=random.Random(f)
    for _ in range(4):
        a=rr.random()*6.28; d.line([x,y,x+math.cos(a)*4,y+math.sin(a)*4],fill=VENOM)

@fx('sv_streaks')
def _fx_streaks(d,im,e,f):
    """The fall: the city's lights stretch into coloured streaks."""
    rr=random.Random(f*3)
    for _ in range(22):
        x=rr.randint(0,W); y=rr.randint(-10,H); L=rr.randint(8,22)
        c=rr.choice(((250,196,96),MAGENTA,CYAN,(236,236,244)))
        d.line([x,y,x,y+L],fill=c)

@fx('sv_roof')
def _fx_roof(d,im,e,f):
    """The rooftop: a ledge with a cornice, a water tower, the street far below."""
    d.rectangle([0,40,74,H],fill=(40,24,34)); d.rectangle([0,38,78,40],fill=(80,60,70))
    for y in range(44,H,4): d.line([0,y,74,y],fill=(34,20,28))
    d.rectangle([10,20,26,34],fill=(60,40,40)); d.polygon([(8,20),(18,12),(28,20)],fill=(70,46,44))
    for x in (12,24): d.line([x,34,x,38],fill=(60,40,40))
    for x in range(84,W,6): d.point((x,GROUND+2),fill=(250,196,96))

@fx('sv_police')
def _fx_police(d,im,e,f):
    """Police lights washing the right edge."""
    L=Image.new('L',(W,H),0); ImageDraw.Draw(L).rectangle([150,0,W,H],fill=40)
    im.paste((230,40,50) if (f//4)%2 else (50,90,255),(0,0),L)

def comic_panels(base,f,t):
    """The screen splits into three comic panels: Miles fading out, the claws in empty air, the
    Prowler's eyes. base: the scene as it is now."""
    im=Image.new('RGB',(W,H),(250,250,250)); pw=(W-8)//3
    for i,(x0,y0,x1,y1) in enumerate(((4,18,64,62),(20,18,80,62))):
        im.paste(base.crop((x0,y0,x1,y1)).resize((pw,H-4),Image.NEAREST),(2+i*(pw+2),2))
    p3=Image.new('RGB',(pw,H-4),PPAL['p']); d3=ImageDraw.Draw(p3)                 # the Prowler's eyes
    _halftone(d3,0,0,pw,H-4,(80,40,110),1)
    for ex in (10,32):
        d3.polygon([(ex,26),(ex+16,22),(ex+14,30),(ex,31)],fill=(12,10,16))
        d3.polygon([(ex+2,27),(ex+13,24),(ex+12,29),(ex+2,30)],fill=GREEN)
    im.paste(p3,(2+2*(pw+2),2))
    d=ImageDraw.Draw(im)
    for i in range(3): d.rectangle([1+i*(pw+2),1,2+i*(pw+2)+pw,H-2],outline=(0,0,0))
    FX['sv_sfx'](d,im,('sv_sfx',"SWSH!",2+pw+2+pw//2,4,GREEN),f)
    if t<0.1: FX['sv_split'](d,im,('sv_split',1),f)
    return im

def closeup_mask(t,f):
    """Primer plano: the mask with rim light, red web lines, the lenses narrowing; A LEAP OF FAITH."""
    im=Image.new('RGB',(W,H),(14,12,30)); d=ImageDraw.Draw(im)
    _halftone(d,0,0,W,H,(34,28,70),1)
    d.rectangle([40,4,144,64],fill=MPAL['s'])
    d.line([40,4,40,64],fill=MAGENTA); d.line([41,4,41,64],fill=MAGENTA)          # rim light
    d.line([144,4,144,64],fill=CYAN); d.line([143,4,143,64],fill=CYAN)
    for k in range(9):
        a=math.pi*(0.05+k*0.1125); d.line([92,40,92+math.cos(a)*70,40-math.sin(a)*50],fill=(150,24,34))
    for r in (14,26,38): d.arc([92-r*1.4,40-r,92+r*1.4,40+r],200,340,fill=(150,24,34))
    sq=ease((t-0.2)/0.3)
    for x0,sgn in ((52,1),(100,-1)):
        top=18+int(8*sq)
        pts=[(x0,top+(0 if sgn>0 else 6)),(x0+32,top+(6 if sgn>0 else 0)),(x0+28,44),(x0+4,44)]
        d.polygon(pts,fill=(12,12,16)); d.polygon([(p[0]+(2 if i in (0,3) else -2),p[1]+(2 if i<2 else -2)) for i,p in enumerate(pts)],fill=(250,250,250))
    if t>=0.2: FX['sv_caption'](d,im,('sv_caption',"A LEAP OF FAITH.",92,52),f)
    if t<0.06: zoom_lines(d)
    if t<0.1: FX['sv_split'](d,im,('sv_split',1),f)
    return im

# ---------------------------------------------------------------- the clip
PX=150; WALL=168      # the Prowler's spot, and where the webs pin him

def _actors(s,m,p):
    """Build the actors (Prowler behind Miles) and Miles' rim light. m/p: (x, feet, pose, flip, alpha)."""
    acts=[]
    px,py,ppose,pflip,palpha=p
    if px is not None and px<W+10 and palpha>0: acts.append(actor(PROWLER[ppose],px,py,flip=pflip,pal=PPAL,alpha=palpha))
    mx,my,mpose,mflip,malpha=m
    acts.append(actor(MILES[mpose],mx,my,flip=mflip,pal=MPAL,alpha=malpha))
    s['fx'].append(('sv_rim',mpose,mx,my,mflip,malpha))
    return acts

def clip_leap(f):
    g=twos(f)                                   # characters on twos, effects on ones
    s=scene(f,THEME)
    s['under'].append(('sv_lamp',))
    mx,my,mpose,mflip,malpha=30,GROUND,guard_pose(g),False,1.0
    px,py,ppose,pflip,palpha=None,GROUND,'idle',True,1.0
    web=None; flipped=False; panels=None
    # 1) the Prowler drops in
    if 14<=f<96: px=PX
    if 14<=g<28: py=lerp(-8,GROUND,((g-14)/14)**2)
    if 28<=f<32: s['shake']=rshake(2); s['fx'].append(('dust',PX-6,GROUND-1)); s['fx'].append(('dust',PX+6,GROUND-1))
    if 20<=f<50: callout(s,"PROWLER",c=GREEN)
    # 2) camouflage; comic panels as the claws cut the air; the kick
    if 40<=g<48: px,ppose=ez(PX,52,(g-40)/8),'attack'; s['under'].append(('sv_trail',PX,px,GROUND-9))
    if 44<=g<80: malpha=0.2+0.12*(g%4<2)
    if 48<=g<80: px,ppose=52,'attack' if g<60 else 'idle'
    if 48<=f<56: s['fx'].append(('sv_claw',40,GROUND-10,f-48))
    if 50<=f<80: panels=(f-50)/30
    if 80<=g<86: mx,mpose,malpha=100,'punch',1.0; px,pflip,ppose=52,False,'idle'
    if 86<=g<96: mx,my,mpose=ez(100,172,(g-86)/10),GROUND-10*math.sin((g-86)/10*math.pi),'hurt'; px,ppose,pflip=52,'attack',False
    if 86<=f<90: s['shake']=rshake(2)
    if 86<=f<96: s['fx'].append(('sv_sfx',"WHAM!",120,6,MAGENTA))
    # 3) close-up
    if 96<=f<140: s['image']=closeup_mask((f-96)/44,f); return s
    # 4) the leap of faith: rooftop, jump, the city turns over, streaks, THWIP
    if 140<=f<208:
        s['under'].append(('sv_roof',)); px=None
        if g<152: mx,my,mpose=48,38,'guard' if g<146 else 'charge'
        elif g<164:
            p=(g-152)/12; mx,my,mpose=lerp(48,96,p),38-12*math.sin(p*math.pi*0.6)+p*p*14,'armsup'
        elif g<190:
            p=(g-164)/26; mx,my,mpose=96+p*10,30+p*14,'armsup'; flipped=True
            s['fx'].append(('sv_streaks',))
        else:
            p=(g-190)/18; mx,my,mpose=lerp(106,64,p),GROUND-24*math.sin(p*math.pi)-4,'armsup'; web=(92,0)
        if 190<=f<194: s['flash']=0.9; s['fc']=(96,20); s['flashc']=(255,255,255)
        if 190<=f<220: s['fx'].append(('sv_sfx',"THWIP",140,6,(250,250,250)))
    # 5) back down: two webs pin the Prowler to the wall, then the venom blast
    if 208<=f<312: px,pflip=PX,True
    if 208<=g<220: p=(g-208)/12; mx,my,mpose=lerp(30,90,p),GROUND-20*math.sin(p*math.pi),'armsup'; web=(lerp(50,90,p),0)
    if 220<=g<238:
        mx,mpose=96,'punch'
        for k,t0 in enumerate((220,228)):
            if t0<=f<t0+4:
                hx,hy=hand('punch',96,GROUND); s['fx'].append(('sv_web',hx,hy,lerp(hx,WALL-6,(f-t0)/4),GROUND-10-k*6))
    if 224<=f<312:
        px=WALL
        s['fx'].append(('sv_glob',WALL+5,GROUND-6))
        if f>=232: s['fx'].append(('sv_glob',WALL+5,GROUND-13))
        if f<240: py=GROUND+(1 if f%4<2 else 0)                                     # struggling
    if 222<=f<246: s['fx'].append(('sv_sfx',"THWP!",120,6,(250,250,250)))
    if 238<=g<246: mx,mpose=108,'charge'; s['fx'].append(('sv_charge',*hand('charge',108,GROUND)))
    if 246<=g<272: mx,mpose=108,'punch'
    if 246<=f<266:
        hx,hy=hand('punch',108,GROUND); s['fx'].append(('sv_venom',hx,hy,WALL-4,GROUND-12,f-246)); ppose='hurt'
        if f<252: s['flash']=0.7; s['fc']=(WALL,GROUND-12); s['flashc']=VENOM_HI; s['shake']=rshake(2)
    if 246<=f<276: s['fx'].append(('sv_sfx',"ZZAKT!",96,6,VENOM))
    if 266<=f<312: ppose='hurt'; s['fx'].append(('dizzy',WALL,GROUND-20))
    # 6) police lights; the Prowler is taken away; back to the neutral pose
    if 280<=f<320: s['under'].append(('sv_police',))
    if 296<=f<312: palpha=max(0,1-(f-296)/16)
    if 272<=g<300: mx,mflip,mpose=ez(108,30,(g-272)/28),True,guard_pose(g)
    if g>=300: mx,mflip=30,False
    acts=_actors(s,(mx,my,mpose,mflip,malpha),(px,py,ppose,pflip,palpha))
    s['actors']=acts
    if panels is not None: s['image']=comic_panels(render(s,f),f,panels); return s
    if web: hx,hy=hand(mpose,mx,my,mflip); s['fx'].append(('sv_web',hx,hy,web[0],web[1]))
    if 246<=f<254 or 86<=f<90: s['fx'].append(('sv_split',1))
    if flipped: s['image']=render(s,f).transpose(Image.FLIP_TOP_BOTTOM)   # the city turns upside down
    return s

CLIPS = [clip('leap', N_, clip_leap)]
