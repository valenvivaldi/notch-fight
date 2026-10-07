"""This Is Fine (KC Green's Gunshow): no fight. Claude as the dog in the little bowler hat, at the kitchen
table with a mug of coffee. A small flame in the corner; it climbs the walls, smoke gathers under the
ceiling, the pictures on the wall turn into terminal errors (BUILD FAILED, PROD IS DOWN, DEPLOY ON
FRIDAY) — and he keeps sipping. Close-up: the calm smile in the firelight, THIS IS FINE. IM OKAY WITH THE
EVENTS THAT ARE UNFOLDING CURRENTLY. The smoke fills the room, clears, and the kitchen is as it was."""
from engine import *

THEME = 'thisisfine'
N_ = 372                                                            # a multiple of 12
CX = 70                                                             # the dog at the table
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
# the dog: Claude's own orange, a brown bowler (dome, dark band, brim), long floppy ears on both sides,
# a pale muzzle with a black nose and a little smile
DPAL = {'1':(120,78,44),'2':(60,36,22),'3':(140,80,44),'4':(244,186,130),'5':(30,20,18)}
HAT = ["...1111.....","..111111....","..222222....",".11111111..."]

def _dog(spr):
    g=[list(r) for r in overlay(spr,HAT,0,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); w=len(g[0])
    def put(x,y,c,over='.Oo'):
        if 0<=y<len(g) and 0<=x<w and g[y][x] in over: g[y][x]=c
    for y in range(top,top+7): put(l-1,y,'3'); put(l,y,'3','O')          # the back ear, hanging long
    for y in range(top,top+4): put(r+1,y,'3')                             # the front ear, behind the face
    for x in range(r-3,r+1): put(x,top+4,'4','O'); put(x,top+5,'4','O')   # the muzzle...
    put(r+1,top+4,'5'); put(r,top+4,'5','O4')                             # ...its nose
    put(r-2,top+5,'5','4'); put(r-1,top+6,'5','O')                        # the smile
    return S([''.join(x) for x in g])
DOG=variant(_dog)
WALL, WALL_D = (236,206,120), (214,180,96)
SIGNS = ["BUILD FAILED","PROD IS DOWN","DEPLOY FRIDAY"]

# ---- background: the kitchen -------------------------------------------------------------------------
def _kitchen(d):
    d.rectangle([0,0,W,H],fill=WALL)                                 # yellow wallpaper with its stripes
    for x in range(0,W,6): d.line([x,0,x,46],fill=WALL_D)
    d.rectangle([0,0,W,3],fill=(200,170,100))
    d.rectangle([150,10,176,32],fill=(150,200,230),outline=(120,84,54),width=2)   # the window
    d.line([163,10,163,32],fill=(120,84,54)); d.line([150,21,176,21],fill=(120,84,54))
    d.rectangle([0,46,W,H],fill=(150,110,70))                         # wood floor
    for y in range(48,H,4): d.line([0,y,W,y],fill=(130,94,60))
    d.rectangle([0,44,W,46],fill=(200,170,110))                       # skirting board
register_bg(THEME, lambda v: (v+120,v+90,v+50), decor=_kitchen)

FRAMES=[(14,10),(46,16),(102,10)]                                    # (x, y) of the three pictures
BURNING=[(2,5),(60,17),(120,5)]                                       # the error signs are wider
@fx('tf_frames')
def _fx_frames(d,im,e,f):
    """The pictures on the wall: little landscapes, or (burning) the terminal's red errors."""
    _,burning=e
    for i,(x,y) in enumerate(FRAMES):
        if burning: x,y=BURNING[i]
        w=len(SIGNS[i])*4+5 if burning else 22
        d.rectangle([x-1,y-1,x+w+1,y+12],fill=(110,74,44))
        if not burning:
            d.rectangle([x,y,x+w,y+11],fill=(150,200,230)); d.polygon([(x,y+11),(x+8,y+4),(x+14,y+8),(x+22,y+3),(x+22,y+11)],fill=(90,150,90))
            d.ellipse([x+15,y+1,x+19,y+5],fill=(250,230,120))
        else:
            d.rectangle([x,y,x+w,y+11],fill=(16,16,20))
            text(d,SIGNS[i],x+3,y+4,(255,70,60) if (f//4+i)%3 else (255,200,90),shadow=None)

@fx('tf_table')
def _fx_table(d,im,e,f):
    """The table and the chair (drawn over the dog's legs: he is sitting)."""
    x=CX
    d.rectangle([x-12,GROUND-12,x-10,GROUND],fill=(120,80,46)); d.rectangle([x-12,GROUND-6,x-4,GROUND-5],fill=(120,80,46))   # chair
    d.rectangle([x+2,GROUND-8,x+34,GROUND-6],fill=(150,100,60)); d.line([x+4,GROUND-6,x+4,GROUND],fill=(120,80,46)); d.line([x+32,GROUND-6,x+32,GROUND],fill=(120,80,46))

@fx('tf_mug')
def _fx_mug(d,im,e,f):
    """His mug of coffee, steam curling off it."""
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x-2,y-3,x+2,y+1],fill=(240,240,236),outline=(150,150,150)); d.arc([x+1,y-2,x+4,y],270,90,fill=(150,150,150))
    d.line([x-1,y-3,x+1,y-3],fill=(90,50,20))
    for k in range(2): ph=(f+k*6)%12; d.point((x-1+k*2+int(math.sin(ph*0.5)),y-5-ph//2),fill=(250,250,250))

@fx('tf_fire')
def _fx_fire(d,im,e,f):
    """The fire: from the left corner across the floor and up the walls (k 0..1: how far it has gone)."""
    _,k=e
    if k<=0: return
    reach=int(W*k)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).rectangle([0,int(46-40*k),reach,H],fill=int(110*min(1,k*2)))
    im.paste((255,120,40),(0,0),g.filter(ImageFilter.GaussianBlur(6))); d=ImageDraw.Draw(im)
    rr=random.Random(f//2)
    for x in range(0,reach,7):                                       # flames along the floor
        FX['fire'](d,im,('fire',x+rr.randint(-2,2),46,2+int(3*k)+rr.randint(0,2)),f+x)
    if k>0.4:                                                       # and up the walls
        for x in range(4,reach,18): FX['fire'](d,im,('fire',x,30-int(10*k),1+int(2*k)),f+x*3)

@fx('tf_smoke')
def _fx_smoke(d,im,e,f):
    """Smoke gathering under the ceiling (a 0..1), or filling the whole room."""
    _,a=e
    if a<=0: return
    h=int(6+50*max(0,a-0.5)*2) if a>0.5 else int(6+14*a*2)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for x in range(0,W,10):
        r=8+int(4*math.sin(f*0.1+x)); md.ellipse([x-r,h-r-2,x+r,h+r-2],fill=int(200*min(1,a*1.4)))
    md.rectangle([0,0,W,h],fill=int(200*min(1,a*1.4)))
    im.paste((90,86,84),(0,0),m.filter(ImageFilter.GaussianBlur(3)))

@fx('tf_bubble')
def _fx_bubble(d,im,e,f):
    speech_bubble(d,*e[1:],fill=(250,250,250),ink=(30,30,30))                     # the engine's bubble (engine/people.py)

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_fine(t,f):
    """Primer plano: the dog's calm face, the hat, the flames all round — THIS IS FINE."""
    im=Image.new('RGB',(W,H),(200,80,30)); d=ImageDraw.Draw(im)
    rr=random.Random(f//2)
    for i in range(30):                                              # a wall of fire behind him
        x=rr.randint(-10,W+10); h=rr.randint(20,60)
        d.polygon([(x-8,H),(x+rr.randint(-4,4),H-h),(x+8,H)],fill=rr.choice([(255,140,40),(255,200,80),(230,80,30)]))
    for i in range(8): d.ellipse([i*26-10,-14,i*26+24,10],fill=(80,76,74))   # the smoke above
    ox=40
    for ex in (ox-12,ox+54):                                          # the two long ears
        d.polygon([(ex+6,16),(ex+16,18),(ex+14,58),(ex+8,64),(ex,56),(ex+2,24)],fill=DPAL['3'],outline=(90,50,26))
    d.rounded_rectangle([ox,14,ox+58,H+10],radius=14,fill=SKIN)          # the head
    d.rounded_rectangle([ox+52,14,ox+58,H],radius=4,fill=SKIN_D)
    d.ellipse([ox+20,38,ox+46,58],fill=DPAL['4'])                         # the muzzle
    d.ellipse([ox+29,37,ox+37,43],fill=DPAL['5']); d.point((ox+31,38),fill=(120,100,100))   # the nose
    d.arc([ox+24,44,ox+42,56],20,160,fill=INK,width=2)                     # the calm smile
    for ex in (ox+18,ox+42):                                          # eyes: two black ovals, a glint
        d.ellipse([ex-3,26,ex+3,34],fill=(24,14,12)); d.point((ex-1,28),fill=(255,220,160))
    d.ellipse([ox+10,-6,ox+48,16],fill=DPAL['1'],outline=(80,50,26))      # the bowler: the dome...
    d.rectangle([ox+10,9,ox+48,13],fill=DPAL['2'])                         # ...the band...
    d.rounded_rectangle([ox+2,13,ox+56,17],radius=2,fill=DPAL['1'],outline=(80,50,26))   # ...the brim
    mx,my=ox+66,46                                                   # the mug, up for a sip
    d.rectangle([mx-7,my-10,mx+7,my+6],fill=(240,240,236),outline=(120,120,120)); d.arc([mx+4,my-6,mx+12,my+2],270,90,fill=(120,120,120),width=2)
    d.ellipse([mx-12,my-2,mx-2,my+8],fill=SKIN,outline=SKIN_D)              # the paw round it
    for k in range(3): ph=(f+k*4)%12; d.point((mx-4+k*4+int(math.sin(ph*0.5)),my-12-ph),fill=(250,250,250))
    if t>=0.3:
        big_text(im,"THIS IS",8,(255,255,255),scale=2,cx=150,outline=(60,20,10))
        big_text(im,"FINE.",26,(255,255,255),scale=2,cx=150,outline=(60,20,10))
    if t<0.06: zoom_lines(d)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
HAND=(13,4)
def clip_fine(f):
    s=scene(f,THEME)
    pose=guard_pose(f)
    fire=0.0 if f<20 else min(1,(f-20)/120)
    if f>=270: fire=max(0,1-(f-270)/30)
    smoke=0.0 if f<40 else min(0.5,(f-40)/160)
    if 264<=f<300: smoke=0.5+0.5*(f-264)/36                            # it fills the room...
    if 300<=f<330: smoke=max(0,1-(f-300)/30)                            # ...and clears
    if f>=330: smoke=0.0
    s['under'].append(('tf_frames',90<=f<300))
    s['under'].append(('tf_fire',fire))
    hx,hy=hand_at(DOG[pose],CX,GROUND,False,*HAND,h=11)
    sip=(f%60)<14 and 30<=f<260                                         # a sip now and then
    mug=(hx+1,hy-3) if sip else (hx+3,GROUND-9)
    if 140<=f<200: s['image']=closeup_fine((f-140)/60,f); return s
    if 204<=f<272: s['fx'].append(('tf_bubble',["IM OKAY WITH THE EVENTS","THAT ARE UNFOLDING","CURRENTLY."],CX+8,12))
    s['actors']=[actor(DOG[pose],CX,pal=DPAL)]
    s['fx'].append(('tf_table',)); s['fx'].append(('tf_mug',)+mug)
    s['fx'].append(('tf_smoke',smoke))
    return s

CLIPS = [clip('fine', N_, clip_fine)]
