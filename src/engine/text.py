"""3x5 pixel font."""
from .core import *

FONT={'V':"101101101101010",'I':"111010010010111",'C':"111100100100111",'T':"111010010010010",'O':"111101101101111",
'R':"110101110101101",'Y':"101101010010010",'A':"010101111101101",'L':"100100100100111",'E':"111100110100111",' ':"000000000000000",
'0':"111101101101111",'1':"010110010010111",'2':"111001111100111",'3':"111001111001111",'4':"101101111001001",
'5':"111100111001111",'6':"111100111101111",'7':"111001001001001",'8':"111101111101111",'9':"111101111001111"}
FONT.update({
'A':"010101111101101",'B':"110101110101110",'C':"111100100100111",'D':"110101101101110",'E':"111100110100111",
'F':"111100110100100",'G':"111100101101111",'H':"101101111101101",'I':"111010010010111",'J':"001001001101111",
'K':"101101110101101",'L':"100100100100111",'M':"101111111101101",'N':"110101101101101",'O':"111101101101111",
'P':"111101111100100",'Q':"111101101111001",'R':"110101110101101",'S':"111100111001111",'T':"111010010010010",
'U':"101101101101111",'V':"101101101101010",'W':"101101111111101",'X':"101101010101101",'Y':"101101010010010",
'Z':"111001010100111",'!':"010010010000010",',':"000000000010110","'":"010010000000000",'?':"111001011000010",'-':"000000111000000",':':"000010000010000",'.':"000000000000010"})

FONT.update({
'¡':"010000010010010",'¿':"010000110100111",'/':"001001010100100",'(':"010100100100010",')':"010001001001010",
'+':"000010111010000",'"':"101101000000000",';':"000010000010100",'=':"000111000111000",'_':"000000000000111",
'<':"001010100010001",'>':"100010001010100",'*':"000101010101000",'#':"101111101111101",'%':"101001010100101",
'&':"010101010101011"})

# Accented letters: the letter's own glyph, with a mark two rows above it, a clear row between (so they keep
# their size; lines of text are 7 rows apart, so the mark lands in the gap).
MARKS = {'´':"010",'~':"111",'¨':"101"}
ACCENTED = {'Á':('A','´'),'É':('E','´'),'Í':('I','´'),'Ó':('O','´'),'Ú':('U','´'),'Ñ':('N','~'),'Ü':('U','¨')}

MISSING=set()       # characters asked for that the font doesn't have (drawn as spaces); a test checks it stays empty

def glyph(ch):
    """(the 3x5 bits, the 3 bits of a mark above or None) for a character; lower case draws as upper case."""
    if ch not in FONT and ch not in ACCENTED: ch=ch.upper()
    if ch in ACCENTED: base,mark=ACCENTED[ch]; return FONT[base],MARKS[mark]
    if ch not in FONT: MISSING.add(ch); return FONT[' '],None
    return FONT[ch],None

# A recorder for checks (scripts/check.py): while RECORD is a list, every text drawn on a full panel-sized
# canvas is noted there as (text, x0, y0, x1, y1), its box. Drawing is the same either way.
RECORD=None
_INNER=[False]                                                       # big_text's own text() call: not noted twice

def _note(txt,x0,y0,x1,y1,canvas):
    if RECORD is not None and not _INNER[0] and canvas==(W,H) and txt.strip(): RECORD.append((txt,x0,y0,x1,y1))

def text(d,txt,x,y,c,shadow=(0,0,0)):
    _note(txt,x,y-2 if any(glyph(ch)[1] for ch in txt) else y,x+len(txt)*4-2,y+4,getattr(d,'_image',None) and d._image.size)
    for i,ch in enumerate(txt):
        bits,mark=glyph(ch)
        if mark: bits=mark+'000'+bits; y0=y-2                       # the mark, a clear row, the letter
        else: y0=y
        for j,b in enumerate(bits):
            if b=='1':
                px,py=x+i*4+j%3,y0+j//3
                if shadow: d.point((px+1,py+1),fill=shadow)
                d.point((px,py),fill=c)

def big_text(im,txt,y,c,scale=2,cx=W//2,shadow=(0,0,0),outline=None):
    """Scaled text pasted onto im, centred at cx, with a drop shadow at +1,+1 (None: no shadow).
    outline: a colour pasted at the 4 neighbours and +1,+1, the shadow then goes to +2,+2.
    Returns the text box (x, y, w, h). Unknown chars render as spaces."""
    up=2 if any(glyph(ch)[1] for ch in txt) else 0                  # room for the accents above
    m=Image.new('L',(len(txt)*4,6+up),0); _INNER[0]=True
    try: text(ImageDraw.Draw(m),txt,0,up,255,shadow=None)
    finally: _INNER[0]=False
    m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2); y-=up*scale
    _note(txt,x,y,x+m.width-scale,y+m.height-scale,im.size)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)
    return x,y,m.width,m.height
