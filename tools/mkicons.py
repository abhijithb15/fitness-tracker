# Draws icon-192.png and icon-512.png into the current folder (run by the Pages workflow).
# Design: deep night gradient, a coral-to-amber progress ring (about 80% closed),
# and a white heartbeat line through the middle. Content stays inside the
# maskable safe zone so Android can crop it to a circle or squircle.
import math
from PIL import Image, ImageDraw, ImageFilter


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def icon(n, path):
    s = 4 * n
    top, bot = (40, 40, 56), (6, 6, 10)
    grad = Image.new("RGB", (1, 256))
    for y in range(256):
        grad.putpixel((0, y), lerp(top, bot, y / 255))
    im = grad.resize((s, s), Image.BILINEAR)
    d = ImageDraw.Draw(im)

    cx = cy = s / 2
    R = s * 0.27          # ring centre-line radius (inside the maskable safe zone)
    w = s * 0.085         # ring thickness
    d.ellipse([cx - R - w / 2, cy - R - w / 2, cx + R + w / 2, cy + R + w / 2], outline=(64, 30, 42), width=int(w))

    # gradient arc from -90deg sweeping 290deg
    c0, c1 = (255, 55, 95), (255, 170, 20)
    start, sweep, steps = -90, 290, 600
    for i in range(steps):
        t = i / (steps - 1)
        a = math.radians(start + sweep * t)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        col = lerp(c0, c1, t)
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)

    # heartbeat line
    lw = int(s * 0.034)
    pts = [(-0.17, 0.0), (-0.07, 0.0), (-0.035, -0.085), (0.01, 0.10), (0.05, -0.04), (0.075, 0.0), (0.17, 0.0)]
    pts = [(cx + px_ * s, cy + py_ * s) for px_, py_ in pts]
    glow = Image.new("L", (s, s), 0)
    ImageDraw.Draw(glow).line(pts, fill=110, width=lw * 3, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(s * 0.02))
    im.paste((255, 120, 80), mask=glow)
    d = ImageDraw.Draw(im)
    d.line(pts, fill=(255, 255, 255), width=lw, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - lw / 2, p[1] - lw / 2, p[0] + lw / 2, p[1] + lw / 2], fill=(255, 255, 255))

    im.resize((n, n), Image.LANCZOS).save(path)


icon(192, "icon-192.png")
icon(512, "icon-512.png")
