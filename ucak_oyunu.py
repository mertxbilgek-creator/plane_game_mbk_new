# --- Oyunun ihtiyaç duyduğu modüller (senin importlarına dokunmaz) ---
import pygame
import random
import sys
import os
import json
import math
from datetime import datetime

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

try:
    KLASOR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    KLASOR = os.getcwd()
SKOR_DOSYASI = os.path.join(KLASOR, "skorlar.json")
AYAR_DOSYASI = os.path.join(KLASOR, "ayarlar.json")

pygame.init()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK), pygame.SCALED | pygame.FULLSCREEN)
saat = pygame.time.Clock()
kucuk_font = pygame.font.SysFont("arial", 16)
orta_font = pygame.font.SysFont("arial", 22)
font = pygame.font.SysFont("arial", 26, bold=True)
buyuk_font = pygame.font.SysFont("arial", 52, bold=True)
baslik_font = pygame.font.SysFont("arial", 64, bold=True)


# ---------------- Dil desteği ----------------
METINLER = {
    "tr": {
        "baslik": "GÖKYÜZÜ KAÇIŞI",
        "basla": "Oyuna Başla",
        "skorlar": "Skorlar",
        "dil_btn": "Dil: Türkçe",
        "cikis": "Çıkış",
        "en_yuksek": "En Yüksek Skor: {}",
        "ipucu_menu": "F11: Tam ekran  |  M: Ses  |  L: Dil",
        "skorlar_baslik": "SKORLAR",
        "en_yuksek_skorlar": "En Yüksek Skorlar",
        "son_oyunlar": "Son Oyunlar",
        "skor_yok": "Henüz skor yok, hadi uçmaya!",
        "puan_satir": "{} puan",
        "geri": "Geri",
        "puan": "Puan: {}",
        "duraklat_ipucu": "P / ESC: Duraklat",
        "duraklatildi": "DURAKLATILDI",
        "devam": "Devam Et",
        "yeniden": "Yeniden Başla",
        "ana_menu": "Ana Menü",
        "carptin": "ÇARPTIN!",
        "puanin": "Puanın: {}",
        "yeni_rekor": "YENİ REKOR!",
        "rekor": "Rekor: {}",
        "tekrar": "Tekrar Oyna",
        "atla": "Atlamak için ENTER",
        "yuzde": "%{}",
        "yukleme": [
            "Motorlar ısıtılıyor...",
            "Yakıt dolduruluyor...",
            "Bulutlar yerleştiriliyor...",
            "Skorlar yükleniyor...",
            "Kalkışa hazır!",
        ],
    },
    "en": {
        "baslik": "SKY ESCAPE",
        "basla": "Start Game",
        "skorlar": "Scores",
        "dil_btn": "Language: English",
        "cikis": "Quit",
        "en_yuksek": "High Score: {}",
        "ipucu_menu": "F11: Fullscreen  |  M: Sound  |  L: Language",
        "skorlar_baslik": "SCORES",
        "en_yuksek_skorlar": "Top Scores",
        "son_oyunlar": "Recent Games",
        "skor_yok": "No scores yet, let's fly!",
        "puan_satir": "{} pts",
        "geri": "Back",
        "puan": "Score: {}",
        "duraklat_ipucu": "P / ESC: Pause",
        "duraklatildi": "PAUSED",
        "devam": "Resume",
        "yeniden": "Restart",
        "ana_menu": "Main Menu",
        "carptin": "YOU CRASHED!",
        "puanin": "Your Score: {}",
        "yeni_rekor": "NEW RECORD!",
        "rekor": "Record: {}",
        "tekrar": "Play Again",
        "atla": "Press ENTER to skip",
        "yuzde": "{}%",
        "yukleme": [
            "Warming up engines...",
            "Refueling...",
            "Placing clouds...",
            "Loading scores...",
            "Ready for takeoff!",
        ],
    },
}


def ayarlari_yukle():
    try:
        with open(AYAR_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def ayarlari_kaydet():
    try:
        with open(AYAR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump({"dil": dil}, f)
    except OSError:
        pass


dil = ayarlari_yukle().get("dil", "tr")
if dil not in METINLER:
    dil = "tr"


def m(anahtar, *degerler):
    metin = METINLER[dil][anahtar]
    return metin.format(*degerler) if degerler else metin


def dil_degistir():
    global dil
    dil = "en" if dil == "tr" else "tr"
    pygame.display.set_caption(m("baslik"))
    ayarlari_kaydet()


pygame.display.set_caption(m("baslik"))


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
    try:
        with open(SKOR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(skorlar, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def en_iyi_skor():
    return max((s["puan"] for s in skorlari_yukle()), default=0)


# ---------------- Yardımcılar ----------------
def yazi_yaz(metin, f, renk, x, y):
    yuzey = f.render(metin, True, renk)
    ekran.blit(yuzey, yuzey.get_rect(center=(x, y)))


def golgeli_yazi(metin, f, renk, x, y):
    yazi_yaz(metin, f, (20, 30, 70), x + 3, y + 3)
    yazi_yaz(metin, f, renk, x, y)


def sag_ust_yazi(metin):
    yuzey = kucuk_font.render(metin, True, BEYAZ)
    ekran.blit(yuzey, (GENISLIK - yuzey.get_width() - 12, 15))


def muzik_olustur():
    from array import array

    ayar = pygame.mixer.get_init()
    if ayar is None:
        return None
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
    bas = ["C3", "A2", "F2", "G2"]

    nota_sure = 0.2
    n = int(frekans * nota_sure)
    olcu_uzunluk = n * 8
    veri = array("h")

    for i, nota in enumerate(melodi):
        f = notalar[nota]
        bf = notalar[bas[i // 8]]
        for s in range(n):
            t = s / frekans
            zarf = min(1, s / 200) * (1 - s / n)
            deger = 0
            if f:
                deger += math.sin(2 * math.pi * f * t) * 0.5 * zarf
                deger += math.sin(4 * math.pi * f * t) * 0.15 * zarf

            olcu_s = (i % 8) * n + s
            bas_zarf = min(1, olcu_s / 400) * min(1, (olcu_uzunluk - olcu_s) / 400)
            deger += math.sin(2 * math.pi * bf * olcu_s / frekans) * 0.25 * bas_zarf

            ornek = int(deger * 6000)
            veri.append(ornek)
            if kanal == 2:
                veri.append(ornek)

    return pygame.mixer.Sound(buffer=veri.tobytes())


muzik = None


def ortak_olaylar(olay):
    if olay.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if olay.type == pygame.KEYDOWN:
        if olay.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        if olay.key == pygame.K_m and muzik:
            muzik.set_volume(0 if muzik.get_volume() > 0 else 0.4)
        if olay.key == pygame.K_l:
            dil_degistir()


class Buton:
    def __init__(self, anahtar, x, y, genislik=280, yukseklik=50):
        self.anahtar = anahtar
        self.rect = pygame.Rect(0, 0, genislik, yukseklik)
        self.rect.center = (x, y)

    def ciz(self, yuzey):
        uzerinde = self.rect.collidepoint(pygame.mouse.get_pos())
        renk = ACIK_LACIVERT if uzerinde else LACIVERT
        pygame.draw.rect(yuzey, renk, self.rect, border_radius=12)
        pygame.draw.rect(yuzey, SARI if uzerinde else BEYAZ, self.rect, 3, border_radius=12)
        yazi = font.render(m(self.anahtar), True, BEYAZ)
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