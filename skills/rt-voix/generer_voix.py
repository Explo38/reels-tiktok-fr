#!/usr/bin/env python3
"""
generer_voix.py - génère la voix off d'un script préparé (une phrase par
ligne), en local et gratuitement, et écrit les sous-titres .srt calés dessus.

Moteurs :
  pocket  Kyutai Pocket TTS (défaut). Tourne sur le processeur d'un portable.
          Voix française native : "estelle". Code MIT, poids CC-BY 4.0.
          pip install pocket-tts
  piper   Piper, ultra léger, plus robotique. Voix conseillée :
          fr_FR-mls-medium (CC BY 4.0, entraînée de zéro).
          pip install piper-tts
          python3 -m piper.download_voices fr_FR-mls-medium
  test    pas de modèle : un bip par ligne, d'une durée réaliste. Sert à
          vérifier la chaîne (assemblage, sous-titres) sans rien installer.

Sorties : le .wav (mono, 16 bits), un .srt à côté (une ligne = un
sous-titre, avec le texte de voix.affichage.txt : "CV" et pas "cé vé"), et dans le terminal la durée totale et le débit mesuré en mots
par minute, à reporter dans ~/.claude/reels-tiktok/voix.md et à passer à
minutage.py --mpm.

Usage
  python3 generer_voix.py voix.txt --sortie voix_off.wav
  python3 generer_voix.py voix.txt --moteur pocket --voix estelle --pause 0.25
  python3 generer_voix.py voix.txt --moteur piper --modele fr_FR-mls-medium.onnx
  python3 generer_voix.py voix.txt --moteur test
  python3 generer_voix.py voix.txt --vitesse 1.1      # accélère (ffmpeg requis)
"""

import argparse
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import wave

WORD_RE = re.compile(r"[\wÀ-ÿœŒ'’-]+")

# Voix prédéfinies de Pocket TTS dont la source est sous licence non
# commerciale (jeux de données expresso et ears, CC BY-NC 4.0). À ne pas
# utiliser pour une publicité ou un compte qui vend quelque chose.
VOIX_NON_COMMERCIALES = {"cosette", "jean"}


# ---------- moteurs ----------------------------------------------------------

class PocketEngine:
    def __init__(self, voix, langue):
        try:
            from pocket_tts import TTSModel
        except ImportError:
            sys.exit("pocket-tts n'est pas installé. Lance : pip install pocket-tts")
        if voix in VOIX_NON_COMMERCIALES:
            print(f"ATTENTION : la voix « {voix} » vient d'un jeu de données non commercial "
                  "(CC BY-NC). Ne l'utilise pas pour une pub.", file=sys.stderr)
        print("Chargement du modèle (le premier lancement télécharge les poids)...", file=sys.stderr)
        self.model = TTSModel.load_model(language=langue)
        self.state = self.model.get_state_for_audio_prompt(voix)
        self.rate = self.model.sample_rate

    def synth(self, text):
        audio = self.model.generate_audio(self.state, text)
        samples = audio.detach().cpu().flatten().clamp(-1, 1).tolist()
        return [int(s * 32767) for s in samples]


class PiperEngine:
    def __init__(self, modele):
        try:
            from piper import PiperVoice
        except ImportError:
            sys.exit("piper-tts n'est pas installé. Lance : pip install piper-tts")
        if not modele or not os.path.exists(modele):
            sys.exit("Donne le fichier de voix .onnx avec --modele (ex. fr_FR-mls-medium.onnx).\n"
                     "Téléchargement : python3 -m piper.download_voices fr_FR-mls-medium")
        self.voice = PiperVoice.load(modele)
        self.rate = None

    def synth(self, text):
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.close()
        with wave.open(tmp.name, "wb") as wf:
            self.voice.synthesize_wav(text, wf)
        rate, samples = read_wav(tmp.name)
        os.unlink(tmp.name)
        self.rate = rate
        return samples


class TestEngine:
    """Un bip doux par ligne, à ~160 mots/min. Aucune dépendance."""

    def __init__(self):
        self.rate = 24000

    def synth(self, text):
        n_words = max(1, len(WORD_RE.findall(text)))
        dur = n_words / (160 / 60)
        n = int(dur * self.rate)
        return [int(3000 * math.sin(2 * math.pi * 440 * i / self.rate)) for i in range(n)]


# ---------- audio ------------------------------------------------------------

def read_wav(path):
    with wave.open(path, "rb") as wf:
        rate, width, ch = wf.getframerate(), wf.getsampwidth(), wf.getnchannels()
        raw = wf.readframes(wf.getnframes())
    if width != 2:
        sys.exit(f"format inattendu ({width * 8} bits) dans {path}")
    samples = list(struct.unpack("<%dh" % (len(raw) // 2), raw))
    if ch > 1:
        samples = samples[::ch]
    return rate, samples


def write_wav(path, rate, samples):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(struct.pack("<%dh" % len(samples), *samples))


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def change_speed(path, factor):
    if not shutil.which("ffmpeg"):
        print("ffmpeg absent : vitesse inchangée.", file=sys.stderr)
        return False
    tmp = path + ".tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path,
                    "-filter:a", f"atempo={factor}", tmp], check=True)
    os.replace(tmp, path)
    return True


# ---------- principal --------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Génère une voix off française locale + sous-titres.")
    ap.add_argument("input", help="texte préparé, une phrase par ligne (sortie de preparer_texte.py)")
    ap.add_argument("--sortie", "-o", default="voix_off.wav", help="fichier .wav de sortie")
    ap.add_argument("--moteur", choices=["pocket", "piper", "test"], default="pocket")
    ap.add_argument("--voix", default="estelle", help="voix Pocket TTS (défaut : estelle)")
    ap.add_argument("--langue", default="french",
                    help="modèle Pocket TTS : french (rapide) ou french_24l (meilleur, plus lent)")
    ap.add_argument("--modele", help="fichier .onnx pour Piper")
    ap.add_argument("--affichage", help="texte des sous-titres, même nombre de lignes "
                    "(défaut : <entrée>.affichage.txt s'il existe)")
    ap.add_argument("--pause", type=float, default=0.25, help="silence entre deux lignes, en s")
    ap.add_argument("--vitesse", type=float, default=1.0, help="facteur de vitesse (0.8 à 1.3)")
    args = ap.parse_args()

    lines = [l.strip() for l in open(args.input, encoding="utf-8") if l.strip()]
    if not lines:
        sys.exit("texte vide")
    shown = lines
    disp_path = args.affichage or os.path.splitext(args.input)[0] + ".affichage.txt"
    if os.path.exists(disp_path):
        d = [l.strip() for l in open(disp_path, encoding="utf-8") if l.strip()]
        if len(d) == len(lines):
            shown = d
        else:
            print(f"note : {disp_path} n'a pas le même nombre de lignes, sous-titres = texte lu.",
                  file=sys.stderr)

    if args.moteur == "pocket":
        engine = PocketEngine(args.voix, args.langue)
    elif args.moteur == "piper":
        engine = PiperEngine(args.modele)
    else:
        engine = TestEngine()

    all_samples, cues, clock = [], [], 0.0
    for i, line in enumerate(lines, 1):
        print(f"  [{i}/{len(lines)}] {line}", file=sys.stderr)
        s = engine.synth(line)
        rate = engine.rate
        dur = len(s) / rate
        cues.append((clock, clock + dur, shown[i - 1]))
        all_samples += s
        gap = int(args.pause * rate) if i < len(lines) else 0
        all_samples += [0] * gap
        clock += dur + gap / rate

    write_wav(args.sortie, rate, all_samples)
    total = clock

    if abs(args.vitesse - 1.0) > 0.01 and change_speed(args.sortie, args.vitesse):
        cues = [(a / args.vitesse, b / args.vitesse, t) for a, b, t in cues]
        total /= args.vitesse

    srt_path = os.path.splitext(args.sortie)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as fh:
        for i, (a, b, t) in enumerate(cues, 1):
            fh.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n\n")

    words = sum(len(WORD_RE.findall(l)) for l in lines)
    speech = sum(b - a for a, b, _ in cues)
    mpm = words / (speech / 60) if speech else 0
    print(f"\nVOIX OFF PRÊTE", file=sys.stderr)
    print(f"  fichier :     {args.sortie}", file=sys.stderr)
    print(f"  sous-titres : {srt_path}", file=sys.stderr)
    print(f"  moteur :      {args.moteur}" + (f", voix {args.voix}" if args.moteur == "pocket" else ""),
          file=sys.stderr)
    print(f"  durée :       {total:.1f} s pour {len(lines)} ligne(s)", file=sys.stderr)
    print(f"  débit :       {mpm:.0f} mots/min (à mettre dans voix.md et à passer à minutage.py --mpm)",
          file=sys.stderr)
    if args.moteur == "pocket":
        print("  crédit :      Voix : Kyutai Pocket TTS (CC-BY 4.0)", file=sys.stderr)


if __name__ == "__main__":
    main()
