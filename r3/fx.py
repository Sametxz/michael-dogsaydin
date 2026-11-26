"""Sinematik efektler: kenar ışığı, derinlik bulanıklığı, renk düzenleme, yağmur, sis, ışık şaftı."""
import math, random
import skia
from engine import W, H, col, Sprite, SAMP, draw, clamp

_cache = {}
def _derive(sp, key, paint):
    k = (id(sp), key)
    if k in _cache: return _cache[k]
    w, h = sp.img.width(), sp.img.height(); pad = 60
    surf = skia.Surface(w + pad*2, h + pad*2); c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    c.drawImage(sp.img, pad, pad, SAMP, paint)
    img = surf.makeImageSnapshot().makeRasterImage()
    out = Sprite(img, sp.w + pad*2/sp.ss, sp.h + pad*2/sp.ss, sp.ax + pad/sp.ss, sp.ay + pad/sp.ss, sp.ss)
    _cache[k] = out; return out

def tinted(sp, color):
    return _derive(sp, ("tint", color), skia.Paint(ColorFilter=skia.ColorFilters.Blend(col(color).toColor(), skia.BlendMode.kSrcIn)))

def blurred(sp, sigma):
    return _derive(sp, ("blur", sigma), skia.Paint(ImageFilter=skia.ImageFilters.Blur(sigma, sigma)))

def rim(c, sp, x, y, s, color="#CFE6FF", dx=-5, dy=-3, a=0.9, sy=None):
    """Kenar ışığı: açık renge boyanmış kopya hafif kaydırılmış olarak arkaya."""
    draw(c, tinted(sp, color), x + dx, y + dy, s, a=a, sy=sy)

def shadow_drop(c, sp, x, y, s, color="#000000", a=0.35, skew=0.0):
    t = tinted(sp, color); c.save(); c.translate(x, y); c.skew(skew, 0); c.scale(1, -0.25); draw(c, t, 0, 0, s, a=a); c.restore()

def grade(c, color, a=0.35, mode="multiply"):
    bm = {"multiply": skia.BlendMode.kMultiply, "screen": skia.BlendMode.kScreen, "overlay": skia.BlendMode.kOverlay,
          "color": skia.BlendMode.kColor, "soft": skia.BlendMode.kSoftLight}[mode]
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col(color, a), BlendMode=bm))

def gradient_grade(c, top, bottom, a=0.4, mode="soft"):
    bm = {"multiply": skia.BlendMode.kMultiply, "screen": skia.BlendMode.kScreen, "overlay": skia.BlendMode.kOverlay, "soft": skia.BlendMode.kSoftLight}[mode]
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [col(top, a).toColor(), col(bottom, a).toColor()])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh, BlendMode=bm))

class Rain:
    def __init__(self, n=420, seed=3, angle=12, speed=1900, length=(28, 60), color="#D6E4F0", layers=3):
        r = random.Random(seed); self.drops = []
        for i in range(n):
            layer = i % layers
            self.drops.append((r.uniform(-200, W + 200), r.uniform(0, H), r.uniform(*length) * (0.6 + 0.4 * layer), r.uniform(0.7, 1.0) * (0.5 + 0.5 * layer), layer))
        self.ang = math.radians(angle); self.speed = speed; self.color = color; self.layers = layers
    def draw(self, c, t, alpha=1.0):
        dx, dy = math.sin(self.ang), math.cos(self.ang)
        for (x, y, L, v, layer) in self.drops:
            yy = (y + t * self.speed * v) % (H + 100) - 50; xx = x + (yy - y) * dx / dy * 0 + yy * dx / dy * 0.2
            p = skia.Paint(AntiAlias=True, StrokeWidth=1.2 + layer * 0.9, Color4f=col(self.color, alpha * (0.25 + 0.2 * layer)), StrokeCap=skia.Paint.kRound_Cap)
            c.drawLine(xx, yy, xx - L * dx, yy - L * dy, p)
    def splashes(self, c, t, y0, y1, n=40, seed=5, alpha=0.7):
        r = random.Random(seed); p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2)
        for i in range(n):
            ph = r.uniform(0, 1); per = r.uniform(0.4, 0.8); x = r.uniform(0, W); y = r.uniform(y0, y1)
            k = ((t / per) + ph) % 1
            p.setColor4f(col(self.color, alpha * (1 - k))); c.drawOval(skia.Rect(x - 18 * k, y - 4 * k, x + 18 * k, y + 4 * k), p)

def fog(c, t, y, color="#C8D4DE", a=0.35, n=6, seed=2, speed=14, h=140):
    r = random.Random(seed)
    for i in range(n):
        x0 = r.uniform(-400, W); w = r.uniform(600, 1100); yy = y + r.uniform(-h * 0.4, h * 0.4)
        x = (x0 + t * speed * (0.6 + 0.4 * (i % 3))) % (W + 1200) - 600
        sh = skia.GradientShader.MakeRadial((x + w / 2, yy), w / 2, [col(color, a).toColor(), col(color, 0).toColor()], [0, 1])
        c.save(); c.scale(1, 0.25); c.drawCircle(x + w / 2, yy * 4, w / 2, skia.Paint(Shader=sh)); c.restore()

def light_shaft(c, x_top, w_top, x_bot, w_bot, color="#FFF2C8", a=0.35, t=0.0, y_top=-50, y_bot=H):
    path = skia.Path(); path.moveTo(x_top - w_top / 2, y_top); path.lineTo(x_top + w_top / 2, y_top); path.lineTo(x_bot + w_bot / 2, y_bot); path.lineTo(x_bot - w_bot / 2, y_bot); path.close()
    aa = a * (0.85 + 0.15 * math.sin(t * 1.3))
    sh = skia.GradientShader.MakeLinear([(0, y_top), (0, y_bot)], [col(color, aa).toColor(), col(color, aa * 0.25).toColor()])
    c.drawPath(path, skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kScreen, AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)))

def bloom_spot(c, x, y, r, color="#FFF6D8", a=0.5):
    sh = skia.GradientShader.MakeRadial((x, y), r, [col(color, a).toColor(), col(color, 0).toColor()], [0, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kScreen))

def letterbox(c, k=1.0, h=90):
    p = skia.Paint(Color4f=col("#000000")); c.drawRect(skia.Rect(0, 0, W, h * k), p); c.drawRect(skia.Rect(0, H - h * k, W, H), p)

def chromatic_flash(c, a):
    if a > 0: c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#FFFFFF", a)))
