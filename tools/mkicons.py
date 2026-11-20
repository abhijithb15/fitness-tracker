# Draws icon-192.png and icon-512.png into the current folder (run by the Pages workflow).
from PIL import Image, ImageDraw, ImageFont
def font(px):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        try: return ImageFont.truetype(p, px)
        except OSError: pass
    return ImageFont.load_default(size=px)
def icon(n, path):
    s = 4*n
    im = Image.new("RGB", (s, s), (27, 67, 50))
    d = ImageDraw.Draw(im)
    w = s*0.12; gap = s*0.05; base = s*0.74; x0 = s*0.2
    for i, h in enumerate([0.22, 0.34, 0.46, 0.58]):
        x = x0 + i*(w+gap)
        d.rounded_rectangle([x, base - s*h, x+w, base], radius=s*0.02, fill=(183, 228, 199))
    pts = [(s*0.18, s*0.40), (s*0.40, s*0.30), (s*0.56, s*0.34), (s*0.82, s*0.16)]
    d.line(pts, fill=(255, 255, 255), width=int(s*0.035), joint="curve")
    r = s*0.04
    d.ellipse([pts[-1][0]-r, pts[-1][1]-r, pts[-1][0]+r, pts[-1][1]+r], fill=(255, 255, 255))
    f = font(int(s*0.11)); t = "FIT"; tw = d.textlength(t, font=f)
    d.text(((s-tw)/2, s*0.79), t, font=f, fill=(255, 255, 255))
    im.resize((n, n), Image.LANCZOS).save(path)
icon(192, "icon-192.png"); icon(512, "icon-512.png")
