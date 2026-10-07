"""A contact sheet of a clip, to look at it while making it: the frames you ask for, enlarged, in a grid,
each one labelled with its number. Renders straight from the theme's code (no build needed).

    python3 scripts/sheet.py <theme> [clip] [frames] [-o out.png] [--scale 3] [--cols 3]

frames: '0,20,40' (those), '0-100/10' (every 10th from 0 to 100), 'end' (the last few and frame 0, to see
the loop close), or nothing (12 spread over the clip). The sheet goes to build/sheets/<theme>__<clip>.png
unless -o says otherwise; its path is printed."""
import argparse, os, random, sys, zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from engine import Image, ImageDraw, W, H, big_text   # noqa: E402
from themes import load_themes                   # noqa: E402

def pick(spec, n):
    """The frame numbers a spec names, for a clip of n frames."""
    if not spec: return sorted({round(i * (n - 1) / 11) for i in range(12)})
    if spec == 'end': return list(range(max(0, n - 8), n)) + [0]
    out = []
    for part in spec.split(','):
        if '-' in part:
            rng, _, step = part.partition('/'); a, b = rng.split('-')
            out += list(range(int(a), min(int(b), n - 1) + 1, int(step or 1)))
        else: out.append(int(part))
    return [f for f in out if 0 <= f <= n]

def render(fn, name, frames):
    """Frames rendered the way build.py does: seeded per clip, every frame up to the last one asked for in
    order (some clips keep state from frame to frame)."""
    random.seed(zlib.crc32(name.encode())); want, got = set(frames), {}
    for f in range(max(frames) + 1):
        im = fn(f)
        if f in want: got[f] = im.convert('RGB')
    return [got[f] for f in frames]

def sheet(images, labels, scale=3, cols=3):
    rows = (len(images) + cols - 1) // cols; gap = 6
    out = Image.new('RGB', (cols * W * scale + (cols - 1) * gap, rows * H * scale + (rows - 1) * gap), (60, 60, 60))
    for i, (im, lab) in enumerate(zip(images, labels)):
        tile = im.resize((W * scale, H * scale), Image.NEAREST); d = ImageDraw.Draw(tile)
        w = len(lab) * 8 + 5; d.rectangle([0, 0, w, 13], fill=(0, 0, 0))
        big_text(tile, lab, 2, (255, 255, 120), scale=2, cx=3 + len(lab) * 4, shadow=None)
        out.paste(tile, ((i % cols) * (W * scale + gap), (i // cols) * (H * scale + gap)))
    return out

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('theme'); ap.add_argument('clip', nargs='?'); ap.add_argument('frames', nargs='?')
    ap.add_argument('-o', '--out'); ap.add_argument('--scale', type=int, default=3); ap.add_argument('--cols', type=int, default=3)
    a = ap.parse_args(argv)
    themes = load_themes()
    if a.theme not in themes: sys.exit(f"unknown theme '{a.theme}'. Known: {', '.join(sorted(themes))}")
    clips = themes[a.theme]
    if a.clip and not any(c[0] == a.clip for c in clips):   # `sheet.py hp 0,20` : a frames spec in the clip's place
        if a.frames is None and (a.clip[0].isdigit() or a.clip == 'end'): a.frames, a.clip = a.clip, None
        else: sys.exit(f"unknown clip '{a.clip}' in {a.theme}. Its clips: {', '.join(c[0] for c in clips)}")
    name, n, fn, _ = next(c for c in clips if c[0] == (a.clip or clips[0][0]))
    frames = pick(a.frames, n)
    out = a.out or os.path.join(ROOT, 'build', 'sheets', f'{a.theme}__{name}.png')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet(render(fn, name, frames), [str(f) for f in frames], a.scale, a.cols).save(out)
    print(out)

if __name__ == '__main__':
    main()
