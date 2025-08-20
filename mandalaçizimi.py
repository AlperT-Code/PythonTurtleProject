# Ultra Mandala – Turtle ile Çok Katmanlı, Renk Geçişli Sanat
# Alper için özenle hazırlandı. 🖤
# Özellikler:
# - Çok katmanlı mandala/petal yapısı
# - HSV -> RGB ile pürüzsüz renk geçişleri
# - Hızlı çizim (tracer ve update optimizasyonları)
# - İnce "glow" efekti (çoklu çizgi katmanı)
# - Bitince otomatik PNG olarak kaydeder (mandala.png)

import turtle as tr
import random, math, os
from colorsys import hsv_to_rgb
from datetime import datetime

# ------------------ Genel Ayarlar ------------------
W, H = 1100, 1100            # tuval boyutu (px)
BG = "#0b0f14"               # arka plan (koyu mavi-siyah)
SEED = 42                    # sabit sonuç için; rastgele istersen None yap
SAVE_PNG = True              # çizim bitince PNG kaydet
FILENAME = "mandala.png"     # kayıt adı

# ------------------ Yardımcı Fonksiyonlar ------------------
def rgb255(r, g, b):
    return (int(r * 255), int(g * 255), int(b * 255))

def set_color_hsv(h, s=0.85, v=1.0):
    r, g, b = hsv_to_rgb(h % 1.0, max(0,min(1,s)), max(0,min(1,v)))
    tr.pencolor(rgb255(r, g, b))

def go(t, x, y):
    t.up(); t.goto(x, y); t.down()

def poly_arc(t, r, extent, steps):
    # Daire yerine çokgen yay: daha kontrollü çizim
    step_ang = extent / steps
    step_len = 2 * math.pi * r * (abs(step_ang) / 360)  # yaklaşık yay uzunluğu
    step_len /= steps
    for _ in range(int(steps)):
        t.left(step_ang)
        t.forward(step_len)

def draw_petal(t, radius, open_angle=55, curve_steps=40, mirror=True):
    # Yaprak/petal: iki simetrik yay
    poly_arc(t, radius, open_angle, curve_steps)
    t.left(180 - open_angle)
    if mirror:
        poly_arc(t, radius, open_angle, curve_steps)
        t.left(180 - open_angle)

def ring_of_petals(t, cx, cy, base_r, n_petals, hue_start, hue_span,
                   pen_base=4, glow=3, open_angle=60, scale=1.0):
    """
    Bir halka üzerinde N adet petal çizer.
    glow: her petal için kalınlıktan inceliğe doğru ekstra katman sayısı
    hue_span: halkanın baştan sona renk farkı (0..1)
    """
    angle_step = 360 / n_petals
    for i in range(n_petals):
        theta = math.radians(i * angle_step)
        # Petalin merkezi için halka yarıçapı:
        orbit_r = base_r * scale
        px = cx + orbit_r * math.cos(theta)
        py = cy + orbit_r * math.sin(theta)
        heading = math.degrees(theta) - 90

        # Renk ayarı
        h = (hue_start + hue_span * (i / n_petals)) % 1.0

        # Glow katmanları (kalın -> ince)
        for g in range(glow, -1, -1):
            pen = pen_base + g * 1.8
            tr.width(pen)
            # Glow katmanlarında doygunluğu ve parlaklığı biraz azalt
            s = 0.82 - g * 0.06
            v = 1.0 - g * 0.05
            r, g_, b = hsv_to_rgb(h, max(0.0, s), max(0.0, v))
            tr.pencolor(rgb255(r, g_, b))

            t.up()
            t.goto(px, py)
            t.setheading(heading)
            t.down()
            # Yaprak boyu ve açısı, halkaya göre dinamik ölçeklensin
            petal_len = base_r * 0.55 * (0.9 + 0.2 * math.sin(i * 0.7))
            open_ang = open_angle * (0.9 + 0.1 * math.cos(i * 0.31))
            draw_petal(t, petal_len, open_angle=open_ang, curve_steps=36, mirror=True)

def starfield(t, n=220, r_min=260, r_max=520, cx=0, cy=0):
    # Arkaplanda minik yıldız taneleri
    t.up()
    for _ in range(n):
        ang = random.random() * 2 * math.pi
        rr = r_min + (r_max - r_min) * (random.random() ** 0.8)
        x = cx + rr * math.cos(ang)
        y = cy + rr * math.sin(ang)
        t.goto(x, y)
        t.down()
        size = 1 if random.random() < 0.85 else 2
        val = 0.75 + random.random() * 0.25
        r,g,b = hsv_to_rgb(0.62, 0.05, val)  # soğuk beyaz
        tr.pencolor(rgb255(r,g,b))
        tr.width(size)
        t.forward(0.0001)  # tek piksel gibi

def radial_orbits(t, cx, cy, base_r, rings=6, hue_base=0.62):
    # Halkalar arası bağlayıcı ince çizgiler (orbital hissi)
    for i in range(1, rings+1):
        rr = base_r * (i / rings)
        steps = max(80, int(2 * math.pi * rr / 6))
        tr.width(1)
        set_color_hsv(hue_base + i * 0.07, 0.25, 0.35)
        t.up(); t.goto(cx, cy - rr); t.setheading(0); t.down()
        # Kapalı halka
        for _ in range(steps):
            t.circle(rr, extent=360/steps)

def signature(t, text="Alper • Ultra Mandala"):
    t.up()
    t.goto(0, -H//2 + 35)
    t.setheading(0)
    tr.width(1)
    set_color_hsv(0.6, 0.15, 0.9)
    t.write(text, align="center", font=("Arial", 14, "normal"))

# ------------------ Ana Çizim ------------------
def draw_mandala():
    if SEED is not None:
        random.seed(SEED)

    tr.setup(W, H)
    tr.colormode(255)
    tr.bgcolor(BG)
    tr.title("Ultra Mandala – Turtle")
    tr.tracer(0, 0)  # maksimum hız

    t = tr.Turtle(visible=False)
    t.speed(0)
    t.hideturtle()

    cx, cy = 0, 0
    base = min(W, H) * 0.32

    # Arka plan yıldızlar
    starfield(t, n=260, r_min=base*0.9, r_max=base*1.9, cx=cx, cy=cy)
    tr.update()

    # İnce orbit çizgileri
    radial_orbits(t, cx, cy, base_r=base*1.35, rings=7, hue_base=0.58)
    tr.update()

    # Ana mandala katmanları
    layers = [
        # (halkanın yarıçap ölçeği, petal sayısı, hue start, hue span, kalem, glow, açı)
        (0.15,  18, 0.00, 0.18, 3, 2, 70),
        (0.26,  24, 0.10, 0.20, 3, 3, 62),
        (0.38,  28, 0.18, 0.25, 3, 3, 58),
        (0.50,  34, 0.28, 0.30, 3, 4, 56),
        (0.64,  40, 0.42, 0.36, 3, 4, 54),
        (0.80,  46, 0.58, 0.42, 2, 3, 52),
        (0.98,  52, 0.74, 0.46, 2, 3, 50),
        (1.18,  58, 0.88, 0.52, 2, 2, 48),
        (1.40,  64, 0.04, 0.58, 2, 2, 46),
    ]

    for scale, n, h0, hspan, pen, glow, ang in layers:
        ring_of_petals(
            t, cx, cy,
            base_r=base,
            n_petals=n,
            hue_start=h0,
            hue_span=hspan,
            pen_base=pen,
            glow=glow,
            open_angle=ang,
            scale=scale
        )
        tr.update()

    # Ortadaki “göz” / rozet
    t.up(); t.goto(cx, cy); t.down()
    for k in range(22, 3, -2):
        tr.width(k)
        set_color_hsv(0.62 + k*0.01, 0.4, 1.0 - k*0.02)
        t.circle(base * 0.08 + (22-k)*0.6)

    signature(t)

    tr.update()

    if SAVE_PNG:
        # Tk canvas'ı PNG'ye dönüştürme: önce .eps alıp PIL yoksa system kullanımı yapacağız.
        # Çoğu ortamda doğrudan .eps çıkarmak mümkün.
        # Eğer PIL yoksa EPS kaydı yine de saklanır.
        try:
            cv = tr.getcanvas()
            eps_name = "mandala.eps"
            cv.postscript(file=eps_name, colormode="color")
            # PIL ile PNG'ye çevir
            try:
                from PIL import Image
                img = Image.open(eps_name)
                img.load(scale=4)  # biraz daha keskin
                img.save(FILENAME, "PNG")
                # EPS kalabilir; istersen sil:
                # os.remove(eps_name)
                print(f"PNG kaydedildi: {FILENAME}")
            except Exception as e:
                print("PIL bulunamadı veya PNG kaydedilemedi. EPS olarak kaydedildi:", eps_name, e)
        except Exception as e:
            print("Kaydetme aşamasında hata:", e)

    # Pencereyi tıklayana kadar açık tut
    tr.done()

if __name__ == "__main__":
    draw_mandala()
