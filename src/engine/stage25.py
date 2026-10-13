"""2.5D scenes: a floor seen at an angle, with depth. A point on it is (wx, z, h): world x, depth z (0 = the
far side, 1 = the near side) and height above the floor. A Stage turns that into the screen and does the
rest every 2.5D theme needs: the size of a figure at its depth (far ones drawn smaller, maybe faded), its
shadow, drawing everything back to front, lines and areas on the floor, and paths through the space.

Three ways to see the floor, all one Stage:
- a vanishing point (vp_x): x converges towards it with depth, as a court seen from the side
  (haikyuu);
- a camera (cam) with parallax: the far side moves a little slower than the near one as the camera
  follows the play (arg-86);
- neither: x is the screen x and only the feet line and the size change with depth, as a dance floor
  seen from the front (arg-cordoba), with ring() for paths around an ellipse on it.

    st = Stage(far_y=33, near_y=62, vp_x=40, far_scale=0.62)
    x, y = st.proj(wx, z, h)                     # screen point
    a = st.place(spr, wx, z, h, flip=..., pal=...)   # an actor, shrunk / faded if far
    a = st.place_at(spr, x, y)                       # the same, at a screen point (depth from its y)
    s['actors'] = st.back_to_front([(z, a), ...])
"""
import math
from PIL import Image, ImageDraw
from .core import W, H, lerp
from .people import shrink as _shrink
from .render import actor

class Stage:
    def __init__(self, far_y, near_y, vp_x=None, far_scale=1.0, parallax=0.0,
                 far_below=0.5, far_k=0.8, far_alpha=1.0, round_feet=False):
        """far_y / near_y: the feet line at z 0 / 1. vp_x: the vanishing x (None: x stays the world x).
        far_scale: how big things are at z 0 (1 at z 1), for x around vp_x and heights. parallax: how much
        slower the far side follows the camera (0: not at all; 0.1: the far side moves at 0.9).
        far_below / far_k / far_alpha: figures with z under far_below are drawn at far_k size and
        far_alpha opacity. round_feet: whole-pixel feet lines (as some themes were drawn)."""
        self.far_y, self.near_y, self.vp_x, self.far_scale = far_y, near_y, vp_x, far_scale
        self.parallax, self.far_below, self.far_k, self.far_alpha = parallax, far_below, far_k, far_alpha
        self.round_feet = round_feet

    # ---- the projection ------------------------------------------------------------------------------
    def scale(self, z):
        """How big something is at depth z (1 at the near side)."""
        return lerp(self.far_scale, 1.0, z)

    def feet(self, z):
        """The screen y of the floor at depth z."""
        y = lerp(self.far_y, self.near_y, z)
        return int(y) if self.round_feet else y

    def x(self, wx, z, cam=0):
        """The screen x of world x at depth z (with the camera at cam)."""
        if self.vp_x is not None: wx = self.vp_x + (wx - self.vp_x) * self.scale(z)
        return wx - cam * lerp(1 - self.parallax, 1.0, z) if cam else wx

    def proj(self, wx, z, h=0, cam=0):
        """(screen x, screen y) of a point h above the floor."""
        return self.x(wx, z, cam), self.feet(z) - h * self.scale(z)

    def depth(self, y):
        """The depth whose feet line is at screen y (the inverse of feet())."""
        return (y - self.far_y) / (self.near_y - self.far_y)

    # ---- figures -------------------------------------------------------------------------------------
    def is_far(self, z): return z < self.far_below

    def sized(self, spr, z):
        """The sprite as it is drawn at depth z: smaller on the far side."""
        return _shrink(spr, self.far_k) if self.is_far(z) else spr

    def place(self, spr, wx, z, h=0, cam=0, flip=False, pal=None, alpha=1.0, **kw):
        """An actor standing at (wx, z), h above the floor: positioned, sized and faded for its depth."""
        x, y = self.proj(wx, z, h, cam)
        far = self.is_far(z)
        if far and self.far_alpha != 1.0: kw['alpha'] = alpha * self.far_alpha
        elif alpha != 1.0: kw['alpha'] = alpha
        return actor(self.sized(spr, z), x, y, flip=flip, pal=pal, **kw)

    def place_at(self, spr, x, y, flip=False, pal=None, alpha=1.0, **kw):
        """An actor whose feet are at screen (x, y), sized and faded for the depth of that y: for scenes laid
        out on the screen (an ellipse in screen coordinates, a stage at a fixed height). Its depth is
        depth(y), for back_to_front()."""
        z = self.depth(y)
        if self.is_far(z) and self.far_alpha != 1.0: kw['alpha'] = alpha * self.far_alpha
        elif alpha != 1.0: kw['alpha'] = alpha
        return actor(self.sized(spr, z), x, y, flip=flip, pal=pal, **kw)

    @staticmethod
    def back_to_front(items):
        """[(z, thing), ...] -> the things, far first (stable: equal depths keep their order)."""
        return [t for _, t in sorted(items, key=lambda zt: zt[0])]

    # ---- on the floor --------------------------------------------------------------------------------
    def shadow(self, im, wx, z, w, color, strength=80, cam=0, scaled=True):
        """A soft flat shadow on the floor under (wx, z), w wide (scaled by depth unless scaled=False)."""
        x, y = self.x(wx, z, cam), self.feet(z)
        if scaled: w *= self.scale(z)
        L = Image.new('L', (W, H), 0); ImageDraw.Draw(L).ellipse([x - w, y - 1, x + w, y + 1], fill=strength)
        im.paste(color, (0, 0), L)

    def quad(self, d, wx0, wx1, z0, z1, color, cam=0):
        """A rectangle of floor from (wx0, z0) to (wx1, z1): a court, a rug, a stage."""
        d.polygon([self.proj(wx0, z0, 0, cam), self.proj(wx1, z0, 0, cam),
                   self.proj(wx1, z1, 0, cam), self.proj(wx0, z1, 0, cam)], fill=color)

    def line(self, d, a, b, color, cam=0, width=1):
        """A line between two (wx, z[, h]) points: court lines, a net's tape, a rail."""
        d.line([self.proj(*a, cam=cam) if len(a) == 3 else self.proj(*a, 0, cam),
                self.proj(*b, cam=cam) if len(b) == 3 else self.proj(*b, 0, cam)], fill=color, width=width)

    def ring(self, cx, cz, rx, rz, a):
        """(wx, z) at angle a on an ellipse on the floor centred at (cx, cz): a ronda, a circle of fighters.
        a = 0 is the right end; sin(a) > 0 is the near half."""
        return cx + rx * math.cos(a), cz + rz * math.sin(a)

def arc(p0, p1, peak, t):
    """(wx, z, h) along a throw from p0 to p1 (each (wx, z, h)), rising `peak` above the straight line at
    its middle (negative: dips). t from 0 to 1, clamped."""
    t = max(0, min(1, t))
    return (lerp(p0[0], p1[0], t), lerp(p0[1], p1[1], t), lerp(p0[2], p1[2], t) + 4 * peak * t * (1 - t))

__all__ = ['Stage', 'arc']
