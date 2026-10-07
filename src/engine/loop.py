"""Time that loops: every clip's frame N must be its frame 0, so whatever keeps moving in a theme's
neutral pose (rain, a flame, a swaying cloak) has to come back to where it started exactly at N.

The engine knows N: clip() records it before each frame it renders, so effects can ask.
- frame(f): f wrapped into the clip (f % N). For anything random per frame (sparks, flicker, flames):
  inside the clip it's f itself (the frames don't change), and frame N is frame 0 again.
- period(p): the length closest to p that divides N, for anything that moves smoothly; phase(f, p)
  and wave(f, p) run on it, so they're back at the start at N, with no jump.
- rng(f, salt, p): a random.Random for this frame (or for this point of a p-frame cycle).
Outside a clip (N unknown) they just use f and p as given."""
import math, random

N = None                                                            # the length of the clip being rendered

def at(n):
    """Set the clip length (clip() calls this before every frame)."""
    global N
    N = n

def frame(f):
    """f, wrapped into the clip: frame N is frame 0."""
    return f % N if N else f

def period(p):
    """The whole number of frames closest to p that divides the clip's length (p itself outside a clip)."""
    p = max(1, int(round(p)))
    if not N: return p
    divs = [d for d in range(1, N + 1) if N % d == 0]
    return min(divs, key=lambda d: (abs(d - p), -d))

def phase(f, p):
    """Where frame f is in a cycle of about p frames, 0..1 (the cycle fits the clip a whole number of times)."""
    P = period(p); return (frame(f) % P) / P

def wave(f, p, offset=0.0):
    """sin() over a cycle of about p frames, -1..1, loop-safe."""
    return math.sin(2 * math.pi * phase(f, p) + offset)

def rng(f, salt=0, p=None):
    """A random.Random for frame f (or, with p, for its point in a cycle of about p frames)."""
    k = frame(f) % period(p) if p else frame(f)
    return random.Random(k * 1000003 + salt)
