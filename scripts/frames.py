"""A clip's (or transition's) frames, as build.py leaves them: frames.png, every frame packed in a grid of
10 columns row by row, and count, how many. Older builds had them loose, as NNN.png; both are read.

    python3 scripts/frames.py unpack <frames dir> <out dir>   # writes NNN.png (skips it when up to date)"""
import os, shutil, sys
from PIL import Image

COLS = 10                                                           # build.py's SHEET_COLS

def load(src):
    """The frames in folder src, as RGB images, in order."""
    count = os.path.join(src, 'count')
    if os.path.exists(count):
        n = int(open(count).read()); cols = min(COLS, n); rows = (n + cols - 1) // cols
        sheet = Image.open(os.path.join(src, 'frames.png')).convert('RGB')
        w, h = sheet.width // cols, sheet.height // rows
        return [sheet.crop(((i % cols) * w, (i // cols) * h, (i % cols + 1) * w, (i // cols + 1) * h)) for i in range(n)]
    names = sorted(n for n in os.listdir(src) if n.endswith('.png') and n[:3].isdigit())
    return [Image.open(os.path.join(src, n)).convert('RGB') for n in names]

def stamp(src):
    """When src's frames last changed (the pack, or the first loose frame)."""
    for f in ('frames.png', '000.png'):
        p = os.path.join(src, f)
        if os.path.exists(p): return os.stat(p).st_mtime
    return 0

def unpack(src, out):
    """src's frames as out/NNN.png; nothing to do when out is already newer than src."""
    out = out.rstrip('/')
    if os.path.exists(os.path.join(out, '000.png')) and os.stat(os.path.join(out, '000.png')).st_mtime >= stamp(src):
        return
    tmp = out + '.tmp'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i, im in enumerate(load(src)): im.save(os.path.join(tmp, f'{i:03d}.png'))
    shutil.rmtree(out, ignore_errors=True); os.replace(tmp, out)    # never half a folder

if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] != 'unpack': sys.exit(__doc__)
    unpack(sys.argv[2], sys.argv[3])
