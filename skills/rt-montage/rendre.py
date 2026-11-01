#!/usr/bin/env python3
"""
rendre.py - fabrique une vidéo motion verticale (Reel / TikTok) à partir d'un
storyboard JSON : fonds, textes animés, captures d'écran dans un téléphone,
voix off, musique et sous-titres incrustés. Sortie MP4 H.264 1080x1920.

Dépendances : Python 3, Pillow (pip install pillow), ffmpeg dans le PATH.
Aucun réseau, tout tourne en local.

Le storyboard (voir exemple_storyboard.json) :

{
  "format": {"largeur": 1080, "hauteur": 1920, "fps": 30},
  "charte": {"fond": "#0F172A", "texte": "#FFFFFF", "accent": "#22C55E",
             "police": "chemin/vers/police-bold.ttf (facultatif)",
             "police_texte": "chemin/vers/police-regular.ttf (facultatif)"},
  "audio": {"voix": "voix_off.wav", "musique": "musique.mp3",
            "volume_musique": 0.18, "sous_titres": "voix_off.srt"},
  "scenes": [
    {"duree": 2.5, "fond": "#0F172A",
     "titre": "2 H -> 10 MIN", "sous_titre": "par lettre de motivation",
     "animation": "monte"},
    {"duree": 4, "image": "assets/capture_accueil.png", "cadre": "telephone",
     "zoom": "lent", "titre": "Colle l'offre", "position": "haut"}
  ]
}

Champs d'une scène (tous facultatifs sauf duree) :
  fond         couleur "#RRGGBB" ou chemin d'image (remplit l'écran)
  degrade      ["#couleur1", "#couleur2"] dégradé vertical à la place de fond
  image        image posée au centre (capture, logo...)
  cadre        "telephone" (coque arrondie + ombre), "carte" (coins arrondis),
               "aucun"
  zoom         "lent" (zoom avant doux), "aucun"
  titre        texte principal (gros). Mets un mot entre *étoiles* pour
               l'afficher en couleur d'accent.
  sous_titre   texte secondaire
  position     "haut", "centre", "bas" pour le bloc de texte (zone sûre)
  animation    "monte" (glisse vers le haut + fondu), "fondu", "pop", "aucune"
  couleur_texte "#RRGGBB" pour cette scène (sinon contraste automatique :
               texte clair sur fond sombre, "texte_sombre" de la charte sur fond clair)
  taille_titre taille en px (défaut auto)

Usage
  python3 rendre.py storyboard.json --sortie video.mp4
  python3 rendre.py storyboard.json --sortie apercu.mp4 --brouillon   # 540x960, rapide
  python3 rendre.py storyboard.json --vignette couverture.jpg          # image de la scène 1
  python3 rendre.py carrousel.json --diapos diapos/                    # une image par scène

Pour un carrousel Instagram, mets "format": {"largeur": 1080, "hauteur": 1350}
(TikTok mode photo : 1080x1920). Pas d'audio, une scène = une diapo.
"""

import argparse
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit("Pillow manque : pip install pillow")

# Zone sûre commune Reels + TikTok sur 1080x1920 (voir CONVENTIONS).
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT = 230, 1440, 140, 60

FONT_CANDIDATES_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_CANDIDATES_REGULAR = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


# ---------------------------------------------------------------- utilitaires

def hex_rgb(value, default=(15, 23, 42)):
    if not isinstance(value, str) or not re.fullmatch(r"#?[0-9a-fA-F]{6}", value.strip()):
        return default
    v = value.strip().lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def find_font(explicit, candidates):
    if explicit and os.path.exists(os.path.expanduser(explicit)):
        return os.path.expanduser(explicit)
    for c in candidates:
        if os.path.exists(c):
            return c
    found = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
    return found[0] if found else None


_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size) if path else ImageFont.load_default()
    return _font_cache[key]


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_back(t):
    t = max(0.0, min(1.0, t))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def resolve(path, base):
    if not path:
        return None
    p = os.path.expanduser(path)
    if not os.path.isabs(p):
        p = os.path.join(base, p)
    return p if os.path.exists(p) else None


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


# ---------------------------------------------------------------- texte

def parse_accent(text):
    """'Ton CV est lu *7 secondes*' -> [(mot, accent?)...]"""
    tokens = []
    for part in re.split(r"(\*[^*]+\*)", text):
        if not part:
            continue
        acc = part.startswith("*") and part.endswith("*")
        for w in part.strip("*").split():
            tokens.append((w, acc))
    return tokens


def wrap_tokens(tokens, fnt, max_w, draw):
    lines, cur, cur_w = [], [], 0
    space = draw.textlength(" ", font=fnt)
    for w, acc in tokens:
        ww = draw.textlength(w, font=fnt)
        if cur and cur_w + space + ww > max_w:
            lines.append(cur)
            cur, cur_w = [], 0
        cur_w += (space if cur else 0) + ww
        cur.append((w, acc, ww))
    if cur:
        lines.append(cur)
    return lines


def text_block(text, fnt_path, size, color, accent, max_w, align="center", shadow=90):
    """Rend un bloc de texte sur un calque transparent. Renvoie l'image."""
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fnt = font(fnt_path, size)
    lines = wrap_tokens(parse_accent(text), fnt, max_w, probe)
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * 1.12)
    space = probe.textlength(" ", font=fnt)
    h = lh * len(lines) + 20
    img = Image.new("RGBA", (max_w + 40, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        lw = sum(ww for _, _, ww in line) + space * (len(line) - 1)
        x = (img.width - lw) / 2 if align == "center" else 20
        y = 10 + i * lh
        for w, acc, ww in line:
            # légère ombre pour la lisibilité sur image
            if shadow:
                d.text((x + 3, y + 4), w, font=fnt, fill=(0, 0, 0, shadow))
            d.text((x, y), w, font=fnt, fill=accent if acc else color)
            x += ww + space
    return img


def auto_title_size(text, W):
    n = len(text.replace("*", ""))
    base = int(W * 0.105)
    if n > 40:
        base = int(W * 0.075)
    elif n > 24:
        base = int(W * 0.088)
    return base


# ---------------------------------------------------------------- scènes

def luminance(img):
    b = img.convert("RGB").resize((8, 8)).tobytes()
    px = [(b[i], b[i + 1], b[i + 2]) for i in range(0, len(b), 3)]
    return sum(0.2126 * r + 0.7152 * g + 0.0722 * bl for r, g, bl in px) / (64 * 255)


class Scene:
    def __init__(self, data, cfg, base, W, H, has_subs=False):
        self.d = data
        self.has_subs = has_subs
        k0 = W / 1080.0
        self.vertical = H / W > 1.6           # 9:16 (Reel, TikTok) ou 4:5 (carrousel)
        if self.vertical:
            self.zone_top = SAFE_TOP * k0
            self.zone_bot = (1150 if has_subs else SAFE_BOTTOM) * k0
        else:                                 # carrousel : 120 px de marge partout
            self.zone_top = 120 * k0
            self.zone_bot = H - 120 * k0
        self.W, self.H = W, H
        self.k = W / 1080.0
        self.dur = float(data.get("duree", 3))
        ch = cfg.get("charte", {})
        self.col_text = hex_rgb(ch.get("texte"), (255, 255, 255))
        self.col_accent = hex_rgb(ch.get("accent"), (34, 197, 94))
        self.font_bold = cfg["_font_bold"]
        self.font_reg = cfg["_font_reg"]

        # fond
        self.bg = Image.new("RGB", (W, H), hex_rgb(ch.get("fond")))
        grad = data.get("degrade")
        bg_val = data.get("fond")
        bg_img = resolve(bg_val, base) if isinstance(bg_val, str) and not bg_val.startswith("#") else None
        if grad and len(grad) == 2:
            c1, c2 = hex_rgb(grad[0]), hex_rgb(grad[1])
            g = Image.new("RGB", (1, H))
            for y in range(H):
                t = y / max(1, H - 1)
                g.putpixel((0, y), tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
            self.bg = g.resize((W, H))
        elif bg_img:
            im = Image.open(bg_img).convert("RGB")
            r = max(W / im.width, H / im.height)
            im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
            left, top = (im.width - W) // 2, (im.height - H) // 2
            self.bg = im.crop((left, top, left + W, top + H))
            # assombrit pour garder le texte lisible
            self.bg = Image.blend(self.bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.35)
        elif bg_val:
            self.bg = Image.new("RGB", (W, H), hex_rgb(bg_val))

        # couleur du texte : celle de la scène, sinon contraste automatique
        if data.get("couleur_texte"):
            self.col_text = hex_rgb(data["couleur_texte"], self.col_text)
        self.shadow = 90
        if not data.get("couleur_texte") and luminance(self.bg) > 0.6:
            self.col_text = hex_rgb(ch.get("texte_sombre"), (15, 23, 42))
            self.shadow = 0
            if ch.get("accent_sombre"):
                self.col_accent = hex_rgb(ch["accent_sombre"])
            elif sum(self.col_accent) / 765 > 0.45:     # accent trop clair sur fond clair
                self.col_accent = tuple(int(c * 0.62) for c in self.col_accent)

        # image centrale
        self.fg = None
        img_path = resolve(data.get("image"), base)
        if data.get("image") and not img_path:
            print(f"  attention : image introuvable : {data.get('image')}", file=sys.stderr)
        if img_path:
            self.fg = self._frame_image(Image.open(img_path).convert("RGBA"), data.get("cadre", "telephone"))

        # textes
        side = (SAFE_LEFT + SAFE_RIGHT) if self.vertical else 240
        max_w = int(W - side * self.k - 40 * self.k)
        self.title = None
        if data.get("titre"):
            size = int(data.get("taille_titre") or auto_title_size(data["titre"], W))
            self.title = text_block(data["titre"], self.font_bold, size, self.col_text,
                                    self.col_accent, max_w, shadow=self.shadow)
        self.sub = None
        if data.get("sous_titre"):
            self.sub = text_block(data["sous_titre"], self.font_reg, int(W * 0.05),
                                  self.col_text, self.col_accent, max_w, shadow=self.shadow)
        self.pos = data.get("position") or ("haut" if self.fg else "centre")
        self.anim = data.get("animation", "monte")
        self.zoom = data.get("zoom", "lent" if self.fg else "aucun")

    def _frame_image(self, im, cadre):
        W, H, k = self.W, self.H, self.k
        if cadre == "telephone":
            target_h = int(H * (0.46 if self.has_subs else 0.56))
            r = target_h / im.height
            tw = int(im.width * r)
            if tw > W * 0.62:
                r = (W * 0.62) / im.width
            im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
            bezel = int(18 * k)
            rad = int(46 * k)
            body = Image.new("RGBA", (im.width + 2 * bezel, im.height + 2 * bezel), (0, 0, 0, 0))
            ImageDraw.Draw(body).rounded_rectangle([0, 0, body.width - 1, body.height - 1],
                                                    radius=rad + bezel, fill=(18, 18, 20, 255))
            screen = Image.new("RGBA", im.size)
            screen.paste(im, (0, 0))
            body.paste(screen, (bezel, bezel), rounded_mask(im.size, rad))
            return self._shadow(body, rad + bezel)
        if cadre == "carte":
            maxw, maxh = W * 0.8, H * 0.5
            r = min(maxw / im.width, maxh / im.height)
            im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
            rad = int(28 * k)
            card = Image.new("RGBA", im.size, (0, 0, 0, 0))
            card.paste(im, (0, 0), rounded_mask(im.size, rad))
            return self._shadow(card, rad)
        maxw, maxh = W * 0.8, H * 0.5
        r = min(maxw / im.width, maxh / im.height, 1.0 if im.width < 400 else 10)
        return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)

    def _shadow(self, im, rad):
        pad = int(60 * self.k)
        sh = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        m = rounded_mask(im.size, rad)
        blk = Image.new("RGBA", im.size, (0, 0, 0, 150))
        sh.paste(blk, (pad, pad + int(20 * self.k)), m)
        sh = sh.filter(ImageFilter.GaussianBlur(int(28 * self.k)))
        sh.alpha_composite(im, (pad, pad))
        return sh

    def _place(self, layer, frame, t_local, delay, y_center):
        """Anime l'entrée d'un calque et le colle sur frame."""
        t = (t_local - delay) / 0.45
        if t <= 0 and self.anim != "aucune":
            return
        a = ease_out(t) if self.anim != "aucune" else 1.0
        dy, scale = 0.0, 1.0
        if self.anim == "monte":
            dy = (1 - a) * 70 * self.k
        elif self.anim == "pop":
            scale = 0.6 + 0.4 * ease_back(t)
        lay = layer
        if scale != 1.0:
            lay = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))))
        if a < 1.0:
            alpha = lay.getchannel("A").point(lambda v: int(v * a))
            lay = lay.copy()
            lay.putalpha(alpha)
        x = (self.W - lay.width) // 2
        y = int(y_center - lay.height / 2 + dy)
        frame.alpha_composite(lay, (x, y))

    def render(self, t):
        W, H, k = self.W, self.H, self.k
        frame = self.bg.convert("RGBA")
        zone_top, zone_bot = self.zone_top, self.zone_bot

        # mise en page du bloc texte
        blocks = [b for b in (self.title, self.sub) if b is not None]
        gap = int(18 * k)
        total = sum(b.height for b in blocks) + gap * (len(blocks) - 1) if blocks else 0
        pos = self.pos if self.fg is not None or self.pos != "centre" else "centre"
        if self.fg is not None and pos == "centre":
            pos = "haut"
        if pos == "haut":
            y0 = zone_top + 10 * k
        elif pos == "bas":
            y0 = zone_bot - total - 10 * k
        else:
            y0 = zone_top + (zone_bot - zone_top - total) / 2

        # image centrale, ajustée à la place libre
        if self.fg is not None:
            if not blocks:
                r_top, r_bot = zone_top, zone_bot
            elif pos == "bas":
                r_top, r_bot = zone_top, y0 - 20 * k
            else:
                r_top, r_bot = y0 + total + 20 * k, zone_bot
            fit = min(1.0, (r_bot - r_top) / self.fg.height, (W * 0.92) / self.fg.width)
            s = fit * (1.0 + (0.05 * (t / max(self.dur, 0.1)) if self.zoom == "lent" else 0))
            intro = ease_out(t / 0.5) if self.anim != "aucune" else 1
            s *= 0.92 + 0.08 * intro
            fg = self.fg.resize((max(1, int(self.fg.width * s)), max(1, int(self.fg.height * s))))
            if intro < 1:
                fg = fg.copy()
                fg.putalpha(fg.getchannel("A").point(lambda v: int(v * intro)))
            cy = (r_top + r_bot) / 2
            frame.alpha_composite(fg, ((W - fg.width) // 2, int(cy - fg.height / 2)))

        y = y0
        for i, b in enumerate(blocks):
            self._place(b, frame, t, 0.08 + i * 0.18, y + b.height / 2)
            y += b.height + gap
        return frame.convert("RGB")


# ---------------------------------------------------------------- sous-titres

def parse_srt(path):
    cues = []
    if not path or not os.path.exists(path):
        return cues
    raw = open(path, encoding="utf-8").read().replace("\r", "")
    for block in raw.strip().split("\n\n"):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1])
        if not m:
            continue
        g = list(map(int, m.groups()))
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append((a, b, " ".join(lines[2:])))
    return cues


def subtitle_layer(text, cfg, W):
    k = W / 1080.0
    max_w = int(W - (SAFE_LEFT + SAFE_RIGHT) * k - 80 * k)
    fnt = font(cfg["_font_bold"], int(48 * k))
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = wrap_tokens([(w, False) for w in text.split()], fnt, max_w, probe)[:3]
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * 1.15)
    space = probe.textlength(" ", font=fnt)
    widths = [sum(ww for _, _, ww in l) + space * (len(l) - 1) for l in lines]
    pw, ph = int(max(widths) + 48 * k), int(lh * len(lines) + 28 * k)
    img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=int(18 * k), fill=(0, 0, 0, 170))
    for i, l in enumerate(lines):
        x = (pw - widths[i]) / 2
        for w, _, ww in l:
            d.text((x, 14 * k + i * lh), w, font=fnt, fill=(255, 255, 255, 255))
            x += ww + space
    return img


# ---------------------------------------------------------------- principal

def build(cfg, base, out, draft=False, thumb=None, slides_dir=None):
    fmt = cfg.get("format", {})
    W, H = int(fmt.get("largeur", 1080)), int(fmt.get("hauteur", 1920))
    fps = int(fmt.get("fps", 30))
    if draft:
        W, H, fps = W // 2, H // 2, 24
    ch = cfg.get("charte", {})
    cfg["_font_bold"] = find_font(resolve(ch.get("police"), base) or ch.get("police"), FONT_CANDIDATES_BOLD)
    cfg["_font_reg"] = find_font(resolve(ch.get("police_texte"), base) or ch.get("police_texte"),
                                 FONT_CANDIDATES_REGULAR) or cfg["_font_bold"]
    if not cfg["_font_bold"]:
        print("attention : aucune police TrueType trouvée, rendu de secours", file=sys.stderr)

    audio = cfg.get("audio", {})
    srt_path = resolve(audio.get("sous_titres"), base)
    has_subs = bool(srt_path) and audio.get("incruster_sous_titres", True)
    scenes = [Scene(s, cfg, base, W, H, has_subs) for s in cfg.get("scenes", [])]
    if not scenes:
        sys.exit("storyboard sans scène")

    if thumb:
        scenes[0].render(min(1.2, scenes[0].dur)).save(thumb, quality=92)
        print(f"vignette : {thumb}", file=sys.stderr)
        return

    if slides_dir:
        os.makedirs(slides_dir, exist_ok=True)
        for i, sc in enumerate(scenes, 1):
            sc.anim = "aucune"
            path = os.path.join(slides_dir, f"diapo-{i:02d}.png")
            sc.render(sc.dur).save(path)
            print(f"  diapo : {path}", file=sys.stderr)
        print(f"\n{len(scenes)} diapos {W}x{H} dans {slides_dir}", file=sys.stderr)
        return

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg introuvable. Installe-le (brew install ffmpeg / apt install ffmpeg).")

    audio = cfg.get("audio", {})
    voice = resolve(audio.get("voix"), base)
    music = resolve(audio.get("musique"), base)
    srt = resolve(audio.get("sous_titres"), base)
    cues = parse_srt(srt) if audio.get("incruster_sous_titres", True) else []

    total = sum(s.dur for s in scenes)
    # Si la voix est plus longue que les scènes, prolonge la dernière scène.
    if voice:
        try:
            dur_v = float(subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice],
                capture_output=True, text=True).stdout.strip())
            if dur_v > total:
                scenes[-1].dur += dur_v - total + 0.4
                total = sum(s.dur for s in scenes)
                print(f"  dernière scène prolongée : voix de {dur_v:.1f} s", file=sys.stderr)
        except ValueError:
            pass

    tmp_video = out + ".tmp.mp4"
    preset = "ultrafast" if draft else "veryfast"
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-preset", preset, "-crf", "20", "-pix_fmt", "yuv420p", tmp_video],
        stdin=subprocess.PIPE)

    sub_cache = {}
    n_frames = int(round(total * fps))
    starts, acc = [], 0.0
    for s in scenes:
        starts.append(acc)
        acc += s.dur
    fade = 0.25
    k = W / 1080.0
    for i in range(n_frames):
        t = i / fps
        idx = max(j for j in range(len(scenes)) if starts[j] <= t + 1e-9)
        sc = scenes[idx]
        frame = sc.render(t - starts[idx])
        # fondu enchaîné court entre deux scènes
        if idx + 1 < len(scenes):
            t_end = starts[idx] + sc.dur
            if t > t_end - fade:
                nxt = scenes[idx + 1].render(0.0)
                frame = Image.blend(frame, nxt, (t - (t_end - fade)) / fade)
        if cues:
            cur = next((c for c in cues if c[0] <= t < c[1]), None)
            if cur:
                if cur[2] not in sub_cache:
                    sub_cache[cur[2]] = subtitle_layer(cur[2], cfg, W)
                lay = sub_cache[cur[2]]
                rgba = frame.convert("RGBA")
                y = int(1180 * k + (SAFE_BOTTOM * k - 1180 * k - lay.height) / 2)
                rgba.alpha_composite(lay, ((W - lay.width) // 2, y))
                frame = rgba.convert("RGB")
        enc.stdin.write(frame.tobytes())
        if i % (fps * 2) == 0:
            print(f"  {t:5.1f} / {total:.1f} s", file=sys.stderr)
    enc.stdin.close()
    if enc.wait() != 0:
        sys.exit("échec de l'encodage vidéo")

    # mixage audio
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_video]
    filters, maps = [], []
    n = 1
    vol_m = float(audio.get("volume_musique", 0.18 if voice else 0.9))
    if voice:
        cmd += ["-i", voice]
        filters.append(f"[{n}:a]aresample=48000,volume=1.0[v]")
        maps.append("[v]")
        n += 1
    if music:
        cmd += ["-stream_loop", "-1", "-i", music]
        filters.append(f"[{n}:a]aresample=48000,volume={vol_m},"
                       f"afade=t=out:st={max(0, total - 1.2):.2f}:d=1.2[m]")
        maps.append("[m]")
        n += 1
    if maps:
        if len(maps) == 2:
            filters.append("[v][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]")
            out_label = "[a]"
        else:
            out_label = maps[0]
        cmd += ["-filter_complex", ";".join(filters), "-map", "0:v", "-map", out_label,
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}",
                "-movflags", "+faststart", out]
        subprocess.run(cmd, check=True)
        os.remove(tmp_video)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_video, "-c", "copy",
                        "-movflags", "+faststart", out], check=True)
        os.remove(tmp_video)

    print(f"\nVIDÉO PRÊTE", file=sys.stderr)
    print(f"  fichier : {out}", file=sys.stderr)
    print(f"  format :  {W}x{H}, {fps} i/s, {total:.1f} s, {len(scenes)} scènes", file=sys.stderr)
    print(f"  audio :   voix {'oui' if voice else 'non'}, musique {'oui' if music else 'non'}, "
          f"sous-titres {'incrustés' if cues else 'non'}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Rend une vidéo motion verticale depuis un storyboard JSON.")
    ap.add_argument("storyboard", help="fichier storyboard .json")
    ap.add_argument("--sortie", "-o", default="video.mp4")
    ap.add_argument("--brouillon", action="store_true", help="540x960, 24 i/s, rapide")
    ap.add_argument("--vignette", help="écrit seulement une image de la scène 1 (couverture)")
    ap.add_argument("--diapos", help="carrousel : écrit une image PNG par scène dans ce dossier")
    args = ap.parse_args()
    cfg = json.load(open(args.storyboard, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(args.storyboard))
    build(cfg, base, args.sortie, draft=args.brouillon, thumb=args.vignette, slides_dir=args.diapos)


if __name__ == "__main__":
    main()
