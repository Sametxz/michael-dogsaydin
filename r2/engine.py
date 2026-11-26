"""Render motoru: SVG → sprite (rsvg, bir kez) → skia kompozit (kare başına) → ffmpeg."""
import hashlib, re as _re, os, subprocess, math, random
import skia

W, H, FPS = 1920, 1080, 30
CACHE = "/home/claude/r2/cache"; os.makedirs(CACHE, exist_ok=True)
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
INK = "#2A1D14"

class Sprite:
    def __init__(self, img, w, h, ax, ay, ss):
        self.img, self.w, self.h, self.ax, self.ay, self.ss = img, w, h, ax, ay, ss

_mem = {}
def sprite(body, w, h, ax=None, ay=None, ss=1.0, defs=""):
    """body: (0,0)-(w,h) kutusunda SVG içeriği. ss: süpersampling (yakınlaştırılacaksa >1)."""
    # art2.uid() her çağrıda yeni kırpma kimliği üretir; anahtar bunlardan bağımsız olsun (aynı çizim = aynı önbellek, bellek sızıntısı yok)
    norm = _re.sub(r'((?:id="|url\(#))([A-Za-z_]+?)(\d+)', r'\1\2#', body)
    key = hashlib.md5(f"{w}x{h}@{ss}|{defs}|{norm}".encode()).hexdigest()
    if key in _mem: return _mem[key]
    png = f"{CACHE}/{key}.png"
    if not os.path.exists(png):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(w*ss)}" height="{int(h*ss)}" viewBox="0 0 {w} {h}">'
               f'{defs}{body}</svg>')
        subprocess.run(["rsvg-convert", "-o", png + ".tmp"], input=svg.encode(), check=True)
        os.replace(png + ".tmp", png)
    img = skia.Image.open(png).makeRasterImage()
    sp = Sprite(img, w, h, w/2 if ax is None else ax, h/2 if ay is None else ay, ss)
    _mem[key] = sp
    return sp

def char_sprite(svg_g, ss=1.0, w=900, h=900, foot=820):
    """character() çıktısı: ayak tabanı (0,0). Sprite anchor = ayak."""
    return sprite(f'<g transform="translate({w/2},{foot})">{svg_g}</g>', w, h, ax=w/2, ay=foot, ss=ss)

def draw(c, sp, x, y, s=1.0, rot=0.0, a=1.0, sx=None, sy=None):
    if a <= 0.003 or s <= 0.001: return
    c.save(); c.translate(x, y)
    if rot: c.rotate(rot)
    kx = (sx if sx is not None else s) / sp.ss; ky = (sy if sy is not None else s) / sp.ss
    c.scale(kx, ky)
    paint = None
    if a < 0.999:
        paint = skia.Paint(); paint.setAlphaf(max(0.0, min(1.0, a)))
    c.drawImage(sp.img, -sp.ax * sp.ss, -sp.ay * sp.ss, SAMP, paint)
    c.restore()

# ───────── eğriler
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lin(t, t0, t1): return clamp((t - t0) / max(1e-6, t1 - t0))
def ease_io(p): p = clamp(p); return p*p*(3 - 2*p)
def ease_out(p): p = clamp(p); return 1 - (1 - p)**3
def ease_in(p): p = clamp(p); return p**3
def back(p):
    p = clamp(p); c1, c3 = 1.9, 2.9
    return 1 + c3 * (p - 1)**3 + c1 * (p - 1)**2
def pop(t, t0, d=0.32): return back(lin(t, t0, t0 + d)) if t >= t0 else 0.0
def fade(t, t0, d=0.25): return ease_io(lin(t, t0, t0 + d))
def wobble(t, f=1.0, a=1.0, ph=0.0): return a * math.sin(2*math.pi*f*t + ph)

def col(hexc, a=1.0):
    h = hexc.lstrip('#')
    if len(h) == 3: h = "".join(ch*2 for ch in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return skia.Color4f(r/255, g/255, b/255, a)

# ───────── canlı efektler
def vignette(c, strength=0.55, color="#000000"):
    sh = skia.GradientShader.MakeRadial((W/2, H/2), W*0.72, [col(color, 0).toColor(), col(color, 0).toColor(), col(color, strength).toColor()], [0, 0.55, 1.0])
    p = skia.Paint(Shader=sh); c.drawRect(skia.Rect(0, 0, W, H), p)

def glow(c, x, y, r, color, a=0.6):
    sh = skia.GradientShader.MakeRadial((x, y), r, [col(color, a).toColor(), col(color, 0).toColor()], [0, 1])
    p = skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus); c.drawCircle(x, y, r, p)

def rays(c, x, y, ang_deg, length, spread_deg, n, color, a=0.18, t=0.0):
    for i in range(n):
        ang = math.radians(ang_deg + (i - (n-1)/2) * spread_deg / max(1, n-1))
        w = math.radians(spread_deg / n * 0.45 * (1 + 0.3*math.sin(t*0.8 + i)))
        p1 = (x + length*math.cos(ang - w), y + length*math.sin(ang - w))
        p2 = (x + length*math.cos(ang + w), y + length*math.sin(ang + w))
        path = skia.Path(); path.moveTo(x, y); path.lineTo(*p1); path.lineTo(*p2); path.close()
        sh = skia.GradientShader.MakeLinear([(x, y), ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)],
                                            [col(color, a*(0.7+0.3*math.sin(t*1.3+i*1.7))).toColor(), col(color, 0).toColor()])
        c.drawPath(path, skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus, AntiAlias=True))

class Particles:
    def __init__(self, kind, n, seed=1, area=(0, 0, W, H), color="#FFD9A0", size=(2, 6), speed=40):
        rnd = random.Random(seed); self.kind = kind; self.color = color; self.area = area
        self.p = [(rnd.uniform(area[0], area[2]), rnd.uniform(area[1], area[3]), rnd.uniform(*size), rnd.uniform(0.5, 1.5), rnd.uniform(0, 6.28)) for _ in range(n)]
        self.speed = speed
    def draw(self, c, t, alpha=1.0):
        x0, y0, x1, y1 = self.area; hgt = y1 - y0; wid = x1 - x0
        paint = skia.Paint(AntiAlias=True)
        for (x, y, s, v, ph) in self.p:
            if self.kind == "ember":
                yy = y0 + (y - y0 - t * self.speed * v) % hgt; xx = x + 18*math.sin(t*1.3*v + ph)
                a = alpha * (0.5 + 0.5*math.sin(t*3*v + ph))
                glow(c, xx, yy, s*3.2, self.color, 0.35*a); paint.setColor4f(col(self.color, a)); c.drawCircle(xx, yy, s*0.6, paint)
            elif self.kind == "snow":
                yy = y0 + (y - y0 + t * self.speed * v) % hgt; xx = x0 + (x - x0 + 25*math.sin(t*0.9*v + ph) + t*12) % wid
                paint.setColor4f(col(self.color, alpha*0.85)); c.drawCircle(xx, yy, s, paint)
            elif self.kind == "dust":
                yy = y + 14*math.sin(t*0.4*v + ph); xx = x0 + (x - x0 + t * self.speed * v * 0.3) % wid
                a = alpha * (0.35 + 0.35*math.sin(t*1.1*v + ph)); paint.setColor4f(col(self.color, a)); c.drawCircle(xx, yy, s*0.7, paint)
            elif self.kind == "rain":
                yy = y0 + (y - y0 + t * self.speed * 10 * v) % hgt; xx = x - (t*120) % 60
                paint.setColor4f(col(self.color, alpha*0.5)); paint.setStrokeWidth(2.5); c.drawLine(xx, yy, xx - 10, yy + 34, paint)

def fill(c, color, a=1.0):
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col(color, a)))

# ───────── el çizimi ok (etiketler için)
def hand_arrow(c, x0, y0, x1, y1, bend=0.25, prog=1.0, color="#FFFFFF", w=6):
    mx, my = (x0 + x1)/2, (y0 + y1)/2; dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy*bend, my + dx*bend
    pts = []
    N = 30
    for i in range(int(N*clamp(prog)) + 1):
        tt = i / N
        pts.append(((1-tt)**2*x0 + 2*(1-tt)*tt*cx + tt*tt*x1, (1-tt)**2*y0 + 2*(1-tt)*tt*cy + tt*tt*y1))
    if len(pts) < 2: return
    path = skia.Path(); path.moveTo(*pts[0])
    for p in pts[1:]: path.lineTo(*p)
    for wid, cc in ((w + 7, INK), (w, color)):
        paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wid, Color4f=col(cc), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        c.drawPath(path, paint)
    if prog >= 0.98:
        ex, ey = pts[-1]; px, py = pts[-4]
        ang = math.atan2(ey - py, ex - px)
        for wid, cc in ((w + 7, INK), (w, color)):
            paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wid, Color4f=col(cc), StrokeCap=skia.Paint.kRound_Cap)
            for da in (2.55, -2.55):
                c.drawLine(ex, ey, ex + 26*math.cos(ang + da), ey + 26*math.sin(ang + da), paint)

# ───────── metin sprite'ları
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def label(text, size=64, font="Luckiest Guy", color="#FFFFFF", stroke=INK, sw=12, rot=0, sub=None, sub_size=30, weight="normal", ss=1.4):
    w = int(len(text) * size * 0.62 + 80); h = int(size * 1.5 + (sub_size * 1.4 if sub else 0) + 30)
    body = (f'<g transform="translate({w/2},{size*1.15}) rotate({rot})">'
            f'<text x="4" y="6" font-family="{font}" font-weight="{weight}" font-size="{size}" text-anchor="middle" fill="#000" opacity="0.28">{esc(text)}</text>'
            f'<text font-family="{font}" font-weight="{weight}" font-size="{size}" text-anchor="middle" fill="{color}" stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" stroke-linejoin="round">{esc(text)}</text>')
    if sub:
        body += f'<text y="{sub_size*1.25}" font-family="Caveat Brush" font-size="{sub_size}" text-anchor="middle" fill="{color}" stroke="{stroke}" stroke-width="7" paint-order="stroke">{esc(sub)}</text>'
    body += '</g>'
    return sprite(body, w, h, ss=ss)

def hand_label(text, size=54, color="#FFFFFF", rot=-3, ss=1.4):
    return label(text, size=size, font="Caveat Brush", color=color, sw=10, rot=rot, ss=ss)

def source_tag(text):
    w = int(len(text) * 17 + 70)
    body = (f'<rect x="2" y="2" width="{w-4}" height="50" rx="10" fill="#120D09" opacity="0.55"/>'
            f'<rect x="2" y="2" width="{w-4}" height="50" rx="10" fill="none" stroke="#D8B76A" stroke-opacity="0.6" stroke-width="2"/>'
            f'<text x="{w/2}" y="35" font-family="Alegreya SC" font-weight="bold" font-size="25" fill="#F1E3C2" text-anchor="middle" letter-spacing="1.5">{esc(text)}</text>')
    return sprite(body, w, 56, ax=w, ay=0, ss=1.5)

def chapter_title(num, name):
    w, h = 1100, 260
    body = (f'<defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity="0.75"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#cg)"/>'
            f'<text x="70" y="98" font-family="Cinzel" font-weight="700" font-size="52" fill="#D8B76A" letter-spacing="8">{esc(num)}</text>'
            f'<path d="M70,122 H520" stroke="#D8B76A" stroke-width="3"/>'
            f'<text x="66" y="212" font-family="Pirata One" font-size="96" fill="#F6ECD4">{esc(name)}</text>')
    return sprite(body, w, h, ax=0, ay=h, ss=1.3)

# ───────── ffmpeg çıktı
class Writer:
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                                   "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", path],
                                  stdin=subprocess.PIPE)
        self.info = skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType)
        self.buf = bytearray(W * H * 4)
    def write(self, surf):
        surf.readPixels(self.info, self.buf, W * 4); self.p.stdin.write(self.buf)
    def close(self):
        self.p.stdin.close(); self.p.wait()
