"""Packs one clip (or transition) for the Claude Code mod's cell modes. Every frame is shrunk to
`columns*2` x `rows*h` pixels, and each cell's 2 x h pixels drawn as one block character in the two
colours that fit them best (a cell holds only a foreground and a background):
- quad (raster mode, h=2): the 16 quadrant characters (▘▝▀▖▌▞▛▗▚▐▜▄▙▟█ and space)
- sextant (sextant mode, h=3): the 64 sextants (U+1FB00..1FB3B, plus space ▌▐█), 50% more rows
- octant (octant mode, h=4): the 256 octants (U+1CD00..1CDE5, Unicode 16, plus the 26 older blocks
  Unicode reuses), twice the rows of quad
9 bytes a cell: the character's code point (u24, little endian), the foreground's RGB, the
background's RGB; row-major, frames back to back. The mod reads files of 4 MB at most, so the
frames go into chunks in <out dir>: 000.cells, 001.cells, ... holding chunk_frames() frames each.

    python3 scripts/mod_cells.py <frames dir> <columns> <rows> <out dir> [quad|sextant|octant]"""
import os, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frames                                                   # a folder's frames, packed or loose

# the quadrant character for each mask of foreground pixels: bit 1 top left, 2 top right,
# 4 bottom left, 8 bottom right
QUAD = [0x20, 0x2598, 0x259D, 0x2580, 0x2596, 0x258C, 0x259E, 0x259B,
        0x2597, 0x259A, 0x2590, 0x259C, 0x2584, 0x2599, 0x259F, 0x2588]

def sextant(mask):
    """The sextant for a mask of foreground pixels, bit i = pixel i (row-major, 2 a row). Unicode
    skips the four that already exist as blocks: empty, left half, right half, full."""
    if mask == 0: return 0x20
    if mask == 0b010101: return 0x258C
    if mask == 0b101010: return 0x2590
    if mask == 0b111111: return 0x2588
    return 0x1FB00 + mask - 1 - (mask > 0b010101) - (mask > 0b101010)

# the octant patterns Unicode left out because an older block already draws them; bit i = pixel i
# (row-major, 2 a row, 4 rows)
OCTANT_REUSED = {
    0x00: 0x20, 0x01: 0x1CEA8, 0x02: 0x1CEAB, 0x03: 0x1FB82, 0x05: 0x2598, 0x0A: 0x259D, 0x0F: 0x2580,
    0x14: 0x1FBE6, 0x28: 0x1FBE7, 0x3F: 0x1FB85, 0x40: 0x1CEA3, 0x50: 0x2596, 0x55: 0x258C, 0x5A: 0x259E,
    0x5F: 0x259B, 0x80: 0x1CEA0, 0xA0: 0x2597, 0xA5: 0x259A, 0xAA: 0x2590, 0xAF: 0x259C, 0xC0: 0x2582,
    0xF0: 0x2584, 0xF5: 0x2599, 0xFA: 0x259F, 0xFC: 0x2586, 0xFF: 0x2588}

def octants():
    """The octant for every mask: the BLOCK OCTANTs follow the masks in order, skipping the reused."""
    table, nxt = [], 0x1CD00
    for mask in range(256):
        if mask in OCTANT_REUSED: table.append(OCTANT_REUSED[mask])
        else: table.append(nxt); nxt += 1
    return table

GLYPHS = {'quad': (2, QUAD), 'sextant': (3, [sextant(m) for m in range(64)]), 'octant': (4, octants())}

_SPLITS = {}

def splits(n):
    """Every split of n pixels into two groups (mask and ~mask are the same split), as index lists."""
    if n not in _SPLITS:
        _SPLITS[n] = [(mask, [i for i in range(n) if mask >> i & 1], [i for i in range(n) if not mask >> i & 1])
                      for mask in range(1, 1 << (n-1))]
    return _SPLITS[n]

def cell(px, table):
    """The (code point, fg, bg) whose two colours best match the cell's pixels (row-major). Two flat
    colours leave sum(p^2) - |sum fg|^2/|fg| - |sum bg|^2/|bg|: the split maximising the subtracted
    part fits best."""
    if len(set(px)) == 1: return table[0], px[0], px[0]
    total = [sum(p[c] for p in px) for c in range(3)]
    best = None
    for mask, fi, bi in splits(len(px)):
        f = [sum(px[i][c] for i in fi) for c in range(3)]
        b = [total[c]-f[c] for c in range(3)]
        score = (f[0]*f[0]+f[1]*f[1]+f[2]*f[2])/len(fi) + (b[0]*b[0]+b[1]*b[1]+b[2]*b[2])/len(bi)
        if best is None or score > best[0]: best = (score, mask, f, b, len(fi), len(bi))
    _, mask, f, b, nf, nb = best
    return table[mask], tuple(v//nf for v in f), tuple(v//nb for v in b)

CHUNK_BYTES = 3_000_000      # under the mod's 4 MB read limit; register.tsx uses the same number

def chunk_frames(columns, rows):
    return max(1, CHUNK_BYTES // (columns*rows*9))

def main(src, columns, rows, out, glyphs='quad'):
    h, table = GLYPHS[glyphs]
    ims = frames.load(src)
    per = chunk_frames(columns, rows)
    tmp = out+'.tmp'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    data = bytearray(); memo = {}
    for k, im in enumerate(ims):
        im = im.resize((columns*2, rows*h), Image.BOX)
        px = im.load()
        for y in range(0, rows*h, h):
            for x in range(0, columns*2, 2):
                key = tuple(px[x+dx, y+dy] for dy in range(h) for dx in range(2))
                if key not in memo:
                    cp, f, b = cell(key, table); memo[key] = cp.to_bytes(3, 'little')+bytes(f)+bytes(b)
                data += memo[key]
        if (k+1) % per == 0 or k+1 == len(ims):
            open(os.path.join(tmp, f'{k//per:03d}.cells'), 'wb').write(data); data = bytearray()
    shutil.rmtree(out, ignore_errors=True); os.replace(tmp, out)   # the mod never reads half a pack
    print(len(ims))

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], *sys.argv[5:6])
