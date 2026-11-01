#!/usr/bin/env python3
"""
preparer_texte.py - prépare un script pour une voix off de synthèse en français.

Une voix de synthèse lit ce qu'on lui donne, pas ce qu'on voulait dire. Elle
bute sur les chiffres, les sigles, les symboles, les emojis et les hashtags.
Ce script réécrit le texte pour l'oreille :

  - chiffres en toutes lettres : 2 400 € -> deux mille quatre cents euros,
    48e -> quarante-huitième, 75 % -> soixante-quinze pour cent,
    2 h -> deux heures, 10 min -> dix minutes, 2,5 -> deux virgule cinq
  - sigles et mots difficiles via prononciation.json (à compléter à l'écoute)
  - emojis, hashtags, mentions, liens et mise en forme retirés
  - une phrase par ligne (chaque ligne = un plan et un sous-titre)

Usage
  python3 preparer_texte.py script.txt -o voix.txt     # écrit aussi voix.affichage.txt
  python3 preparer_texte.py script.txt --rapport
  python3 preparer_texte.py script.txt --prononciation ~/.claude/reels-tiktok/prononciation.json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRONON = os.path.join(HERE, "prononciation.json")

UNITS = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
         "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize"]
TENS = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def _below_100(n):
    if n <= 16:
        return UNITS[n]
    if n < 20:
        return "dix-" + UNITS[n - 10]
    t, u = divmod(n, 10)
    if t in (7, 9):                       # 70-79 et 90-99 : base 60 / 80 + 10..19
        base = "soixante" if t == 7 else "quatre-vingt"
        rest = n - (60 if t == 7 else 80)
        if t == 7 and rest == 11:
            return "soixante et onze"
        return base + "-" + _below_100(rest)
    if t == 8:
        return "quatre-vingts" if u == 0 else "quatre-vingt-" + UNITS[u]
    word = TENS[t]
    if u == 0:
        return word
    if u == 1:
        return word + " et un"
    return word + "-" + UNITS[u]


def _below_1000(n, final=True):
    h, r = divmod(n, 100)
    parts = []
    if h:
        if h == 1:
            parts.append("cent")
        else:
            parts.append(UNITS[h] + (" cents" if r == 0 and final else " cent"))
    if r or not h:
        parts.append(_below_100(r))
    return " ".join(parts)


def nombre(n):
    """Entier positif ou nul -> lettres (orthographe traditionnelle)."""
    if n < 0:
        return "moins " + nombre(-n)
    if n < 1000:
        return _below_1000(n)
    parts = []
    for value, name in ((10 ** 9, "milliard"), (10 ** 6, "million")):
        q, n = divmod(n, value)
        if q:
            parts.append(f"{nombre(q)} {name}" + ("s" if q > 1 else ""))
    q, n = divmod(n, 1000)
    if q:
        g = _below_1000(q, final=False)
        if g.endswith("quatre-vingts"):        # "vingt" ne prend pas de s devant mille
            g = g[:-1]
        parts.append("mille" if q == 1 else g + " mille")
    if n:
        parts.append(_below_1000(n))
    return " ".join(parts)


def ordinal(n):
    if n == 1:
        return "premier"
    w = nombre(n)
    if w.endswith("cinq"):
        w += "u"
    elif w.endswith("neuf"):
        w = w[:-1] + "v"
    elif w.endswith("e"):
        w = w[:-1]
    elif w.endswith("quatre-vingts") or w.endswith(" cents"):
        w = w[:-1]
    return w + "ième"


def to_int(s):
    return int(re.sub(r"[\s  .]", "", s))


def decimal_words(s):
    """'2,5' -> 'deux virgule cinq' ; '12' -> 'douze'."""
    s = s.replace(".", ",") if re.fullmatch(r"\d+\.\d{1,2}", s) else s
    if "," in s:
        a, b = s.split(",", 1)
        b_words = nombre(int(b)) if not b.startswith("0") else " ".join(nombre(int(c)) for c in b)
        return f"{nombre(to_int(a))} virgule {b_words}"
    return nombre(to_int(s))


NUM = r"\d{1,3}(?:[\s  .]\d{3})+|\d+(?:,\d+)?"

RULES = [
    # 2 400 € / 2400€ / 12 k€ / 3 M€
    (re.compile(r"(" + NUM + r")\s?k€"), lambda m: f"{decimal_words(m.group(1))} mille euros"),
    (re.compile(r"(" + NUM + r")\s?M€"), lambda m: f"{decimal_words(m.group(1))} millions d'euros"),
    (re.compile(r"(" + NUM + r")\s?(?:€|euros?\b)"),
     lambda m: decimal_words(m.group(1)) + (" euro" if m.group(1) in ("1", "0") else " euros")),
    (re.compile(r"(" + NUM + r")\s?%"), lambda m: f"{decimal_words(m.group(1))} pour cent"),
    (re.compile(r"\b(\d+)\s?h\s?(\d{2})\b"),
     lambda m: f"{nombre(int(m.group(1)))} heure{'s' if int(m.group(1)) > 1 else ''} {nombre(int(m.group(2)))}"),
    (re.compile(r"\b(\d+)\s?h\b"),
     lambda m: f"{nombre(int(m.group(1)))} heure{'s' if int(m.group(1)) > 1 else ''}"),
    (re.compile(r"\b(\d+)\s?min\b"),
     lambda m: f"{nombre(int(m.group(1)))} minute{'s' if int(m.group(1)) > 1 else ''}"),
    (re.compile(r"\b(\d+)\s?s\b"),
     lambda m: f"{nombre(int(m.group(1)))} seconde{'s' if int(m.group(1)) > 1 else ''}"),
    (re.compile(r"\b1er\b|\b1re\b|\b1ère\b"), lambda m: "premier" if m.group(0) == "1er" else "première"),
    (re.compile(r"\b(\d+)(?:e|ème|eme)\b"), lambda m: ordinal(int(m.group(1)))),
    (re.compile(r"\bx(\d+)\b"), lambda m: f"fois {nombre(int(m.group(1)))}"),
    (re.compile(r"\b(\d+)x\b"), lambda m: f"{nombre(int(m.group(1)))} fois"),
    (re.compile(r"\bbac\s?\+\s?(\d)\b", re.IGNORECASE), lambda m: f"bac plus {nombre(int(m.group(1)))}"),
    (re.compile(r"\+"), lambda m: " plus "),
    (re.compile(r"(?<!\w)(?<!\d,)(" + NUM + r")(?!\w)(?!,\d)"), lambda m: decimal_words(m.group(1))),
]

EMOJI_RE = re.compile(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍]")
CLEAN = [
    (re.compile(r"https?://\S+|www\.\S+"), ""),
    (re.compile(r"(?:^|\s)#[\wÀ-ÿ]+"), ""),
    (re.compile(r"(?:^|\s)@[\w.]+"), ""),
    (re.compile(r"[*_`~>]+"), ""),
    (re.compile(r"\s*[—–]\s*"), ", "),
    (re.compile(r"\s*->\s*|\s*→\s*"), ", "),
    (re.compile(r"[«»“”\"]"), ""),
    (re.compile(r"[’‘]"), "'"),
    (re.compile(r"…"), "..."),
    (re.compile(r"\(([^)]*)\)"), r", \1,"),
    (re.compile(r"\s*/\s*"), " ou "),
    (re.compile(r"&"), " et "),
]


def load_pronunciations(path):
    try:
        d = json.load(open(os.path.expanduser(path), encoding="utf-8"))
        return {k: v for k, v in d.items() if not k.startswith("_")}
    except FileNotFoundError:
        return {}


def apply_pronunciations(text, table, hits):
    for word in sorted(table, key=len, reverse=True):
        pattern = re.compile(r"(?<![\wÀ-ÿ])" + re.escape(word) + r"(?![\wÀ-ÿ])")
        n = len(pattern.findall(text))
        if n:
            hits.append(f"{n}x  {word} -> {table[word]}")
            text = pattern.sub(table[word], text)
    return text


def split_lines(text):
    out = []
    for para in text.splitlines():
        para = para.strip()
        if not para:
            continue
        for s in re.findall(r"[^.!?]+(?:[.!?]+|$)", para):
            s = s.strip(" ,")
            if s:
                out.append(s[0].upper() + s[1:])
    return out


def tidy(text):
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([,.])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r",\s*([.!?])", r"\1", text)
    return text.strip()


def prepare(text, table):
    """Renvoie (lignes lues, lignes affichées, rapport). Même nombre de lignes :
    la ligne affichée sert aux sous-titres, la ligne lue à la voix."""
    report = {"nettoyage": 0, "nombres": [], "prononciation": []}
    before = len(EMOJI_RE.findall(text))
    text = EMOJI_RE.sub("", text)
    report["nettoyage"] += before
    for pattern, repl in CLEAN:
        text, n = pattern.subn(repl, text)
        report["nettoyage"] += n
    display = [tidy(l) for l in split_lines(tidy_lines(text))]
    display = [l for l in display if l]
    spoken = []
    for line in display:
        line = apply_pronunciations(line, table, report["prononciation"])
        for pattern, fn in RULES:
            def sub(m, fn=fn):
                new = fn(m)
                report["nombres"].append(f"{m.group(0).strip()} -> {new.strip()}")
                return new
            line = pattern.sub(sub, line)
        line = tidy(line)
        spoken.append(line[0].upper() + line[1:] if line else line)
    return spoken, display, report


def tidy_lines(text):
    return "\n".join(tidy(l) for l in text.splitlines())


def main():
    ap = argparse.ArgumentParser(description="Prépare un script pour une voix off de synthèse.")
    ap.add_argument("input", nargs="?", default="-", help="script, ou - pour stdin")
    ap.add_argument("-o", "--sortie", dest="out", help="écrit le texte prêt à lire ici")
    ap.add_argument("--prononciation", default=PRONON, help="table de prononciation JSON")
    ap.add_argument("--rapport", action="store_true", help="affiche les changements (stderr)")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    table = load_pronunciations(PRONON)
    if args.prononciation != PRONON:
        table.update(load_pronunciations(args.prononciation))   # la table perso gagne
    spoken, display, report = prepare(raw, table)
    text = "\n".join(spoken) + "\n"
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        disp = os.path.splitext(args.out)[0] + ".affichage.txt"
        open(disp, "w", encoding="utf-8").write("\n".join(display) + "\n")
        print(f"écrit : {args.out} (lu) et {disp} (sous-titres)", file=sys.stderr)
    else:
        sys.stdout.write(text)
    if args.rapport:
        print(f"\nPRÉPARATION VOIX OFF : {len(spoken)} ligne(s), "
              f"{report['nettoyage']} élément(s) retiré(s)", file=sys.stderr)
        for title, key in (("NOMBRES", "nombres"), ("PRONONCIATION", "prononciation")):
            if report[key]:
                print(f"\n{title}", file=sys.stderr)
                for h in report[key]:
                    print(f"  {h}", file=sys.stderr)
        print("\nÉcoute le résultat. Tout mot mal prononcé va dans prononciation.json.\n",
              file=sys.stderr)


if __name__ == "__main__":
    main()
