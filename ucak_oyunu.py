import pygame
print("Pygame sürümü:", pygame.version.ver, "Pygame başariyla yüklendi!")
import random
print("Random modülü yüklendi!")
import sys
print("Sistem modülü yüklendi!")
import os
print("OS modülü yüklendi!")
import json
print("JSON modülü yüklendi!")
import math
print("Math modülü yüklendi!")
from datetime import datetime
print("Datetime modülü yüklendi!")


# --- Ayarlar ---
GENISLIK, YUKSEKLIK = 800, 500
FPS = 60

BEYAZ = (255, 255, 255)
GOK = (120, 190, 255)
YESIL = (60, 170, 80)
KOYU_YESIL = (40, 120, 55)
KIRMIZI = (220, 50, 50)
SARI = (255, 210, 60)
LACIVERT = (25, 45, 110)
ACIK_LACIVERT = (50, 80, 170)
GRI = (150, 155, 165)
KOYU_GRI = (90, 95, 105)
CAM = (40, 60, 90)

# Skor dosyası kodun olduğu klasöre otomatik kaydedilir
SKOR_DOSYASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skorlar.json")

pygame.init()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Gökyüzü Kaçışı")
saat = pygame.time.Clock()
kucuk_font = pygame.font.SysFont("arial", 16)
orta_font = pygame.font.SysFont("arial", 22)
font = pygame.font.SysFont("arial", 26, bold=True)
buyuk_font = pygame.font.SysFont("arial", 52, bold=True)
baslik_font = pygame.font.SysFont("arial", 64, bold=True)


# ---------------- Skor işlemleri ----------------
def skorlari_yukle():
    try:
        with open(SKOR_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def skor_kaydet(puan):
    skorlar = skorlari_yukle()
    skorlar.append({"puan": puan, "tarih": datetime.now().strftime("%d.%m.%Y %H:%M")})
    skorlar = skorlar[-50:]
    with open(SKOR_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(skorlar, f, ensure_ascii=False, indent=2)


def en_iyi_skor():
    return max((s["puan"] for s in skorlari_yukle()), default=0)


# ---------------- Yardımcılar ----------------
def yazi_yaz(metin, f, renk, x, y):
    yuzey = f.render(metin, True, renk)
    ekran.blit(yuzey, yuzey.get_rect(center=(x, y)))


def golgeli_yazi(metin, f, renk, x, y):
    yazi_yaz(metin, f, (20, 30, 70), x + 3, y + 3)
    yazi_yaz(metin, f, renk, x, y)


def muzik_olustur():
    from array import array  # Sadece burada kullanılıyor, üstteki importlara dokunmaz

    ayar = pygame.mixer.get_init()
    if ayar is None:
        return None  # Ses kartı yoksa müziksiz devam et
    frekans, _, kanal = ayar

    notalar = {
        "F2": 87.31, "G2": 98.00, "A2": 110.00, "C3": 130.81,
        "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25, "-": 0,
    }
    melodi = [
        "C5", "E5", "G4", "E5", "A4", "C5", "E5", "D5",
        "C5", "G4", "A4", "B4", "C5", "-", "G4", "-",
        "F4", "A4", "C5", "A4", "G4", "B4", "D5", "B4",
        "C5", "E5", "D5", "B4", "C5", "-", "-", "-",
    ]
    bas = ["C3", "A2", "F2", "G2"]  # Her 8 notada bir değişir

    nota_sure = 0.2
    n = int(frekans * nota_sure)
    olcu_uzunluk = n * 8
    veri = array("h")

    for i, nota in enumerate(melodi):
        f = notalar[nota]
        bf = notalar[bas[i // 8]]
        for s in range(n):
            t = s / frekans
            # Nota başında yumuşak giriş, sonunda sönme
            zarf = min(1, s / 200) * (1 - s / n)
            deger = 0
            if f:
                deger += math.sin(2 * math.pi * f * t) * 0.5 * zarf
                deger += math.sin(4 * math.pi * f * t) * 0.15 * zarf

            # Bas, ölçü başı ve sonunda yumuşak geçişli
            olcu_s = (i % 8) * n + s
            bas_zarf = min(1, olcu_s / 400) * min(1, (olcu_uzunluk - olcu_s) / 400)
            deger += math.sin(2 * math.pi * bf * olcu_s / frekans) * 0.25 * bas_zarf

            ornek = int(deger * 6000)
            veri.append(ornek)
            if kanal == 2:
                veri.append(ornek)

    return pygame.mixer.Sound(buffer=veri.tobytes())


def muzik_olustur():
    from array import array  # Sadece burada kullanılıyor, üstteki importlara dokunmaz

    ayar = pygame.mixer.get_init()
    if ayar is None:
        return None  # Ses kartı yoksa müziksiz devam et
    frekans, _, kanal = ayar

    notalar = {
        "F2": 87.31, "G2": 98.00, "A2": 110.00, "C3": 130.81,
        "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25, "-": 0,
    }
    melodi = [
        "C5", "E5", "G4", "E5", "A4", "C5", "E5", "D5",
        "C5", "G4", "A4", "B4", "C5", "-", "G4", "-",
        "F4", "A4", "C5", "A4", "G4", "B4", "D5", "B4",
        "C5", "E5", "D5", "B4", "C5", "-", "-", "-",
    ]
    bas = ["C3", "A2", "F2", "G2"]  # Her 8 notada bir değişir

    nota_sure = 0.2
    n = int(frekans * nota_sure)
    olcu_uzunluk = n * 8
    veri = array("h")

    for i, nota in enumerate(melodi):
        f = notalar[nota]
        bf = notalar[bas[i // 8]]
        for s in range(n):
            t = s / frekans
            # Nota başında yumuşak giriş, sonunda sönme
            zarf = min(1, s / 200) * (1 - s / n)
            deger = 0
            if f:
                deger += math.sin(2 * math.pi * f * t) * 0.5 * zarf
                deger += math.sin(4 * math.pi * f * t) * 0.15 * zarf

            # Bas, ölçü başı ve sonunda yumuşak geçişli
            olcu_s = (i % 8) * n + s
            bas_zarf = min(1, olcu_s / 400) * min(1, (olcu_uzunluk - olcu_s) / 400)
            deger += math.sin(2 * math.pi * bf * olcu_s / frekans) * 0.25 * bas_zarf

            ornek = int(deger * 6000)
            veri.append(ornek)
            if kanal == 2:
                veri.append(ornek)

    return pygame.mixer.Sound(buffer=veri.tobytes())


def muzik_olustur():
    from array import array  # Sadece burada kullanılıyor, üstteki importlara dokunmaz

    ayar = pygame.mixer.get_init()
    if ayar is None:
        return None  # Ses kartı yoksa müziksiz devam et
    frekans, _, kanal = ayar

    notalar = {
        "F2": 87.31, "G2": 98.00, "A2": 110.00, "C3": 130.81,
        "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25, "-": 0,
    }
    melodi = [
        "C5", "E5", "G4", "E5", "A4", "C5", "E5", "D5",
        "C5", "G4", "A4", "B4", "C5", "-", "G4", "-",
        "F4", "A4", "C5", "A4", "G4", "B4", "D5", "B4",
        "C5", "E5", "D5", "B4", "C5", "-", "-", "-",
    ]
    bas = ["C3", "A2", "F2", "G2"]  # Her 8 notada bir değişir

    nota_sure = 0.2
    n = int(frekans * nota_sure)
    olcu_uzunluk = n * 8
    veri = array("h")

    for i, nota in enumerate(melodi):
        f = notalar[nota]
        bf = notalar[bas[i // 8]]
        for s in range(n):
            t = s / frekans
            # Nota başında yumuşak giriş, sonunda sönme
            zarf = min(1, s / 200) * (1 - s / n)
            deger = 0
            if f:
                deger += math.sin(2 * math.pi * f * t) * 0.5 * zarf
                deger += math.sin(4 * math.pi * f * t) * 0.15 * zarf

            # Bas, ölçü başı ve sonunda yumuşak geçişli
            olcu_s = (i % 8) * n + s
            bas_zarf = min(1, olcu_s / 400) * min(1, (olcu_uzunluk - olcu_s) / 400)
            deger += math.sin(2 * math.pi * bf * olcu_s / frekans) * 0.25 * bas_zarf

            ornek = int(deger * 6000)
            veri.append(ornek)
            if kanal == 2:
                veri.append(ornek)

    return pygame.mixer.Sound(buffer=veri.tobytes())


def muzik_olustur():
    from array import array  # Sadece burada kullanılıyor, üstteki importlara dokunmaz

    ayar = pygame.mixer.get_init()
    if ayar is None:
        return None  # Ses kartı yoksa müziksiz devam et
    frekans, _, kanal = ayar

    notalar = {
        "F2": 87.31, "G2": 98.00, "A2": 110.00, "C3": 130.81,
        "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25, "-": 0,
    }
    melodi = [
        "C5", "E5", "G4", "E5", "A4", "C5", "E5", "D5",
        "C5", "G4", "A4", "B4", "C5", "-", "G4", "-",
        "F4", "A4", "C5", "A4", "G4", "B4", "D5", "B4",
        "C5", "E5", "D5", "B4", "C5", "-", "-", "-",
    ]
    bas = ["C3", "A2", "F2", "G2"]  # Her 8 notada bir değişir

    nota_sure = 0.2
    n = int(frekans * nota_sure)
    olcu_uzunluk = n * 8
    veri = array("h")

    for i, nota in enumerate(melodi):
        f = notalar[nota]
        bf = notalar[bas[i // 8]]
        for s in range(n):
            t = s / frekans
            # Nota başında yumuşak giriş, sonunda sönme
            zarf = min(1, s / 200) * (1 - s / n)
            deger = 0
            if f:
                deger += math.sin(2 * math.pi * f * t) * 0.5 * zarf
                deger += math.sin(4 * math.pi * f * t) * 0.15 * zarf

            # Bas, ölçü başı ve sonunda yumuşak geçişli
            olcu_s = (i % 8) * n + s
            bas_zarf = min(1, olcu_s / 400) * min(1, (olcu_uzunluk - olcu_s) / 400)
            deger += math.sin(2 * math.pi * bf * olcu_s / frekans) * 0.25 * bas_zarf

            ornek = int(deger * 6000)
            veri.append(ornek)
            if kanal == 2:
                veri.append(ornek)

    return pygame.mixer.Sound(buffer=veri.tobytes())


def muzik_olustur():
    from array import array  # Sadece burada kullanılıyor, üstteki importlara dokunmaz

    ayar = pygame.mixer.get_init()
    if ayar is None:
        return None  # Ses kartı yoksa müziksiz devam et
    frekans, _, kanal = ayar

    notalar = {
        "F2": 87.31, "G2": 98.00, "A2": 110.00, "C3": 130.81,
        "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25, "-": 0,
    }
    melodi = [
        "C5", "E5", "G4", "E5", "A4", "C5", "E5", "D5",
        "C5", "G4", "A4", "B4", "C5", "-", "G4", "-",
        "F4", "A4", "C5", "A4", "G4", "B4", "D5", "B4",
        "C5", "E5", "D5", "B4", "C5", "-", "-", "-",
    ]
    bas = ["C3", "A2", "F2", "G2"]  # Her 8 notada bir değişir

    nota_sure = 0.2
    n = int(frekans * nota_sure)
    olcu_uzunluk = n * 8
    veri = array("h")

    for i, nota in enumerate(melodi):
        f = notalar[nota]
        bf = notalar[bas[i // 8]]
        for s in range(n):
            t = s / frekans
            # Nota başında yumuşak giriş, sonunda sönme
            zarf = min(1, s / 200) * (1 - s / n)
            deger = 0
            if f:
                deger += math.sin(2 * math.pi * f * t) * 0.5 * zarf
                deger += math.sin(4 * math.pi * f * t) * 0.15 * zarf

            # Bas, ölçü başı ve sonunda yumuşak geçişli
            olcu_s = (i % 8) * n + s
            bas_zarf = min(1, olcu_s / 400) * min(1, (olcu_uzunluk - olcu_s) / 400)
            deger += math.sin(2 * math.pi * bf * olcu_s / frekans) * 0.25 * bas_zarf

            ornek = int(deger * 6000)
            veri.append(ornek)
            if kanal == 2:
                veri.append(ornek)

    return pygame.mixer.Sound(buffer=veri.tobytes())


def ortak_olaylar(olay):
    if olay.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if olay.type == pygame.KEYDOWN:
        if olay.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        # M tuşu: müziği aç / kapat
        if olay.key == pygame.K_m and muzik:
            muzik.set_volume(0 if muzik.get_volume() > 0 else 0.4)
    
class Buton:
    def __init__(self, metin, x, y, genislik=260, yukseklik=50):
        self.metin = metin
        self.rect = pygame.Rect(0, 0, genislik, yukseklik)
        self.rect.center = (x, y)

    def ciz(self, yuzey):
        uzerinde = self.rect.collidepoint(pygame.mouse.get_pos())
        renk = ACIK_LACIVERT if uzerinde else LACIVERT
        pygame.draw.rect(yuzey, renk, self.rect, border_radius=12)
        pygame.draw.rect(yuzey, SARI if uzerinde else BEYAZ, self.rect, 3, border_radius=12)
        yazi = font.render(self.metin, True, BEYAZ)
        yuzey.blit(yazi, yazi.get_rect(center=self.rect.center))

    def tiklandi(self, olay):
        return (olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1
                and self.rect.collidepoint(olay.pos))


# ---------------- Oyun nesneleri ----------------
class Ucak:
    def __init__(self):
        self.x = 140
        self.y = YUKSEKLIK // 2
        self.max_hiz = 5
        self.dikey_hiz = 0
        self.aci = 0

    def hareket(self, tuslar):
        hedef = 0
        if tuslar[pygame.K_UP]:
            hedef = -self.max_hiz
        if tuslar[pygame.K_DOWN]:
            hedef = self.max_hiz

        self.dikey_hiz += (hedef - self.dikey_hiz) * 0.12
        self.y += self.dikey_hiz

        if self.y < 35:
            self.y = 35
            self.dikey_hiz = 0
        if self.y > YUKSEKLIK - 25:
            self.y = YUKSEKLIK - 25
            self.dikey_hiz = 0

        self.aci = -self.dikey_hiz * 3.5

    def rect(self):
        return pygame.Rect(self.x - 50, self.y - 14, 100, 26)

    def ciz(self, yuzey):
        govde = pygame.Surface((140, 90), pygame.SRCALPHA)
        x, y = 70, 45

        pygame.draw.polygon(govde, LACIVERT, [(x - 46, y - 6), (x - 60, y - 32), (x - 46, y - 32), (x - 28, y - 6)])
        pygame.draw.line(govde, SARI, (x - 55, y - 26), (x - 40, y - 10), 3)
        pygame.draw.polygon(govde, GRI, [(x - 42, y + 2), (x - 58, y + 9), (x - 36, y + 6)])
        pygame.draw.rect(govde, BEYAZ, (x - 50, y - 10, 90, 20), border_radius=10)
        pygame.draw.ellipse(govde, BEYAZ, (x + 26, y - 10, 28, 20))
        pygame.draw.rect(govde, LACIVERT, (x - 46, y + 3, 92, 4), border_radius=2)
        for i in range(10):
            pygame.draw.circle(govde, CAM, (x - 34 + i * 7, y - 3), 2)
        pygame.draw.polygon(govde, CAM, [(x + 40, y - 7), (x + 48, y - 7), (x + 45, y - 2), (x + 38, y - 2)])
        kanat = [(x + 8, y + 2), (x - 18, y + 24), (x - 6, y + 24), (x + 20, y + 2)]
        pygame.draw.polygon(govde, GRI, kanat)
        pygame.draw.polygon(govde, KOYU_GRI, kanat, 1)
        pygame.draw.ellipse(govde, KOYU_GRI, (x - 4, y + 12, 20, 9))
        pygame.draw.ellipse(govde, GRI, (x + 12, y + 13, 5, 7))

        donmus = pygame.transform.rotate(govde, self.aci)
        yuzey.blit(donmus, donmus.get_rect(center=(int(self.x), int(self.y))))


class Engel:
    def __init__(self, x, bosluk):
        self.x = x
        self.genislik = 70
        self.bosluk = bosluk
        self.ust_boy = random.randint(50, YUKSEKLIK - bosluk - 50)
        self.gecildi = False

    def guncelle(self, hiz):
        self.x -= hiz

    def rectler(self):
        ust = pygame.Rect(self.x, 0, self.genislik, self.ust_boy)
        alt_y = self.ust_boy + self.bosluk
        alt = pygame.Rect(self.x, alt_y, self.genislik, YUKSEKLIK - alt_y)
        return ust, alt

    def ciz(self, yuzey):
        for r in self.rectler():
            pygame.draw.rect(yuzey, YESIL, r)
            pygame.draw.rect(yuzey, KOYU_YESIL, r, 4)


class Bulut:
    def __init__(self, x=None):
        self.x = x if x is not None else GENISLIK + random.randint(0, 200)
        self.y = random.randint(20, YUKSEKLIK - 60)
        self.hiz = random.uniform(0.5, 1.5)

    def guncelle(self):
        self.x -= self.hiz
        if self.x < -100:
            self.__init__()

    def ciz(self, yuzey):
        x, y = int(self.x), self.y
        for dx, dy, r in [(0, 0, 18), (20, -8, 22), (42, 0, 18)]:
            pygame.draw.circle(yuzey, (235, 245, 255), (x + dx, y + dy), r)


bulutlar = [Bulut(random.randint(0, GENISLIK)) for _ in range(6)]


def arka_plan(hareket_etsin=True):
    ekran.fill(GOK)
    for b in bulutlar:
        if hareket_etsin:
            b.guncelle()
        b.ciz(ekran)


def karart(seffaflik=140):
    katman = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
    katman.fill((0, 0, 0, seffaflik))
    ekran.blit(katman, (0, 0))


# ---------------- Ekranlar ----------------
def yukleme_ekrani(sure=2700):
    mesajlar = [
        "İmport Yapılıyor...",
        "Bilgisayar kodu okuyor...",
        "Bulutlar yerleştiriliyor...",
        "Skorlar yükleniyor...",
        "Kalkışa hazır!",
    ]
    ucak = Ucak()
    bar_x, bar_y, bar_gen, bar_yuk = 150, 300, 500, 22
    baslangic = pygame.time.get_ticks()

    while True:
        saat.tick(FPS)
        for olay in pygame.event.get():
            ortak_olaylar(olay)
            if olay.type == pygame.KEYDOWN and olay.key in (pygame.K_RETURN, pygame.K_SPACE):
                return

        gecen = pygame.time.get_ticks() - baslangic
        oran = min(gecen / sure, 1)
        oran = oran * oran * (3 - 2 * oran)

        arka_plan()
        karart(90)
        golgeli_yazi("GÖKYÜZÜ KAÇIŞI", baslik_font, BEYAZ, GENISLIK // 2, 140)

        # Yükleme çubuğu
        pygame.draw.rect(ekran, LACIVERT, (bar_x, bar_y, bar_gen, bar_yuk), border_radius=11)
        dolu = int(bar_gen * oran)
        if dolu > 0:
            pygame.draw.rect(ekran, SARI, (bar_x, bar_y, dolu, bar_yuk), border_radius=11)
        pygame.draw.rect(ekran, BEYAZ, (bar_x, bar_y, bar_gen, bar_yuk), 3, border_radius=11)

        # Çubuğun üstünde ilerleyen uçak
        ucak.x = bar_x + dolu
        ucak.y = bar_y - 30
        ucak.aci = math.sin(gecen / 150) * 4
        ucak.ciz(ekran)

        yazi_yaz(f"%{int(oran * 100)}", font, BEYAZ, bar_x + bar_gen + 45, bar_y + bar_yuk // 2)

        mesaj = mesajlar[min(int(oran * len(mesajlar)), len(mesajlar) - 1)]
        yazi_yaz(mesaj, orta_font, BEYAZ, GENISLIK // 2, 360)
        yazi_yaz("Atlamak için ENTER", kucuk_font, BEYAZ, GENISLIK // 2, YUKSEKLIK - 20)

        pygame.display.flip()

        if gecen >= sure:
            pygame.time.wait(300)
            return


def ana_menu():
    ucak = Ucak()
    ucak.x = GENISLIK // 2
    basla = Buton("Oyuna Başla", GENISLIK // 2, 250)
    skorlar = Buton("Skorlar", GENISLIK // 2, 315)
    cikis = Buton("Çıkış", GENISLIK // 2, 380)
    rekor = en_iyi_skor()

    while True:
        saat.tick(FPS)
        for olay in pygame.event.get():
            ortak_olaylar(olay)
            if olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "oyun"
                if olay.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if basla.tiklandi(olay):
                return "oyun"
            if skorlar.tiklandi(olay):
                return "skorlar"
            if cikis.tiklandi(olay):
                pygame.quit()
                sys.exit()

        arka_plan()

        t = pygame.time.get_ticks() / 500
        ucak.y = 160 + math.sin(t) * 8
        ucak.aci = math.cos(t) * 6
        ucak.ciz(ekran)

        golgeli_yazi("GÖKYÜZÜ KAÇIŞI", baslik_font, BEYAZ, GENISLIK // 2, 75)
        basla.ciz(ekran)
        skorlar.ciz(ekran)
        cikis.ciz(ekran)
        golgeli_yazi(f"En Yüksek Skor: {rekor}", orta_font, SARI, GENISLIK // 2, 445)
        yazi_yaz("F11: Tam ekran", kucuk_font, BEYAZ, GENISLIK - 70, YUKSEKLIK - 15)

        pygame.display.flip()


def skorlar_ekrani():
    geri = Buton("Geri", GENISLIK // 2, 445, 200)
    skorlar = skorlari_yukle()
    en_yuksek = sorted(skorlar, key=lambda s: s["puan"], reverse=True)[:5]
    son_oyunlar = list(reversed(skorlar))[:5]

    while True:
        saat.tick(FPS)
        for olay in pygame.event.get():
            ortak_olaylar(olay)
            if olay.type == pygame.KEYDOWN and olay.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                return "menu"
            if geri.tiklandi(olay):
                return "menu"

        arka_plan()
        karart(110)
        golgeli_yazi("SKORLAR", buyuk_font, BEYAZ, GENISLIK // 2, 55)

        sol_x, sag_x = GENISLIK // 4 + 20, GENISLIK * 3 // 4 - 20
        yazi_yaz("En Yüksek Skorlar", font, SARI, sol_x, 125)
        yazi_yaz("Son Oyunlar", font, SARI, sag_x, 125)

        if not skorlar:
            yazi_yaz("Henüz skor yok, hadi uçmaya!", orta_font, BEYAZ, GENISLIK // 2, 250)
        else:
            for i, s in enumerate(en_yuksek):
                yazi_yaz(f"{i + 1}.  {s['puan']} puan  -  {s['tarih']}", orta_font, BEYAZ, sol_x, 175 + i * 40)
            for i, s in enumerate(son_oyunlar):
                yazi_yaz(f"{s['puan']} puan  -  {s['tarih']}", orta_font, BEYAZ, sag_x, 175 + i * 40)

        geri.ciz(ekran)
        pygame.display.flip()


def oyun():
    ucak = Ucak()
    engeller = []
    puan = 0
    engel_hizi = 4
    bosluk = 190
    sayac = 0
    durum = "oynuyor"
    onceki_rekor = en_iyi_skor()
    yeni_rekor = False

    devam_btn = Buton("Devam Et", GENISLIK // 2, 220)
    yeniden_btn = Buton("Yeniden Başla", GENISLIK // 2, 285)
    menu_btn = Buton("Ana Menü", GENISLIK // 2, 350)
    tekrar_btn = Buton("Tekrar Oyna", GENISLIK // 2, 330)
    bitis_menu_btn = Buton("Ana Menü", GENISLIK // 2, 395)

    while True:
        saat.tick(FPS)

        for olay in pygame.event.get():
            ortak_olaylar(olay)

            if olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_ESCAPE, pygame.K_p):
                    if durum == "oynuyor":
                        durum = "duraklatildi"
                    elif durum == "duraklatildi":
                        durum = "oynuyor"
                    elif durum == "bitti" and olay.key == pygame.K_ESCAPE:
                        return "menu"
                if durum == "bitti" and olay.key == pygame.K_r:
                    return "oyun"

            if durum == "duraklatildi":
                if devam_btn.tiklandi(olay):
                    durum = "oynuyor"
                elif yeniden_btn.tiklandi(olay):
                    return "oyun"
                elif menu_btn.tiklandi(olay):
                    return "menu"
            elif durum == "bitti":
                if tekrar_btn.tiklandi(olay):
                    return "oyun"
                elif bitis_menu_btn.tiklandi(olay):
                    return "menu"

        if durum == "oynuyor":
            ucak.hareket(pygame.key.get_pressed())

            sayac += 1
            if sayac >= 90:
                engeller.append(Engel(GENISLIK, bosluk))
                sayac = 0

            for e in engeller[:]:
                e.guncelle(engel_hizi)

                for r in e.rectler():
                    if ucak.rect().colliderect(r):
                        durum = "bitti"

                if not e.gecildi and e.x + e.genislik < ucak.x:
                    e.gecildi = True
                    puan += 1
                    if puan % 5 == 0:
                        engel_hizi += 0.5
                        bosluk = max(130, bosluk - 10)

                if e.x + e.genislik < 0:
                    engeller.remove(e)

            if durum == "bitti":
                skor_kaydet(puan)
                yeni_rekor = puan > onceki_rekor and puan > 0

        arka_plan(hareket_etsin=(durum == "oynuyor"))
        for e in engeller:
            e.ciz(ekran)
        ucak.ciz(ekran)

        ekran.blit(font.render(f"Puan: {puan}", True, BEYAZ), (15, 10))
        ekran.blit(kucuk_font.render("P / ESC: Duraklat", True, BEYAZ), (GENISLIK - 140, 15))

        if durum == "duraklatildi":
            karart()
            golgeli_yazi("DURAKLATILDI", buyuk_font, BEYAZ, GENISLIK // 2, 130)
            devam_btn.ciz(ekran)
            yeniden_btn.ciz(ekran)
            menu_btn.ciz(ekran)
        elif durum == "bitti":
            karart()
            golgeli_yazi("ÇARPTIN!", buyuk_font, KIRMIZI, GENISLIK // 2, 140)
            yazi_yaz(f"Puanın: {puan}", font, BEYAZ, GENISLIK // 2, 205)
            if yeni_rekor:
                yazi_yaz("YENİ REKOR!", font, SARI, GENISLIK // 2, 250)
            else:
                yazi_yaz(f"Rekor: {onceki_rekor}", orta_font, SARI, GENISLIK // 2, 250)
            tekrar_btn.ciz(ekran)
            bitis_menu_btn.ciz(ekran)

        pygame.display.flip()


# ---------------- Ana döngü ----------------

try:
    muzik = muzik_olustur()
except Exception:
    muzik = None

if muzik:
    muzik.set_volume(0.4)
    muzik.play(loops=-1)  # Sonsuz döngüde çal

yukleme_ekrani()
durum = "menu"
while True:
    if durum == "menu":
        durum = ana_menu()
    elif durum == "skorlar":
        durum = skorlar_ekrani()
    elif durum == "oyun":
        durum = oyun()