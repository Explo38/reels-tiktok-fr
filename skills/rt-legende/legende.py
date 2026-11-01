#!/usr/bin/env python3
"""
legende.py - vérifie une légende Instagram ou TikTok et montre exactement ce
que le fil affiche avant le "plus".

Le fil coupe la légende très tôt : environ 125 caractères sur Instagram,
environ 80 à 100 sur TikTok (ici 90 par défaut). Presque toutes les légendes
ratées se ratent là : l'accroche est en phrase trois, la première ligne est un
bonjour, ou tout commence par un hashtag. Le script affiche la partie visible
dans un cadre, comme la lit un inconnu qui fait défiler, puis vérifie les
points qui comptent.

La coupe est une approximation : elle bouge avec l'appareil, la taille de
police et les retours à la ligne. Garde de la marge plutôt qu'une légende
calculée pour finir pile à la coupe. Change-la avec --coupe pour tester.

Usage
  python3 legende.py legende.txt --plateforme tiktok
  python3 legende.py legende.txt --plateforme instagram --mots-cles "recherche d'emploi,alternance"
  python3 legende.py legende.txt --plateforme les-deux
  python3 legende.py legende.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

PLATEFORMES = {
    # limite dure, coupe approximative du fil, plafond de hashtags (5 sur les
    # deux plateformes en 2026)
    "instagram": {"nom": "Instagram", "limite": 2200, "coupe": 125, "hashtags": 5},
    "tiktok": {"nom": "TikTok", "limite": 4000, "coupe": 90, "hashtags": 5},
}

HASHTAG_RE = re.compile(r"(?:^|\s)(#[\wÀ-ÿœ]+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|fr|co|io|net|org|ai|app)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(
    r"\d|(?<!^)(?<![.!?]\s)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b|\b[A-Z]{2,5}\b"
    r"|(?i:\b(?:zéro|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|vingt|trente|cent|mille|euros?)\b)",
    re.MULTILINE)
GREETING_RE = re.compile(r"(?i)^\W*(?:salut|coucou|bonjour|hello|hey|yo|bienvenue)\b")

ASKS = [
    (re.compile(r"(?i)\b(?:commente|commentez|écris|écrivez|tape|tapez)\s+(?:le mot\s+)?[\"«]?\s?[A-ZÀ-Ý0-9]{2,}\b"), "commenter un mot-clé"),
    (re.compile(r"(?i)\b(?:écris|écrivez|envoie|envoyez)[- ]moi (?:en )?(?:dm|mp|message|privé)\b|\ben (?:dm|mp)\b"), "écrire en DM"),
    (re.compile(r"(?i)\b(?:enregistre|enregistrez|sauvegarde|sauvegardez|garde|gardez)[- ](?:la|le|ça|cette|ce)\b"), "enregistrer"),
    (re.compile(r"(?i)\b(?:partage|partagez)[- ](?:la|le|ça|cette|ce)\b|\b(?:envoie|envoyez)-(?:la|le)\b|\b(?:envoie|envoyez) (?:ça|cette vidéo|ce post) à\b|\bidentifie (?:quelqu|un|une|la|le)"), "partager"),
    (re.compile(r"(?i)\b(?:abonne|abonnez)[- ](?:toi|vous)\b|\bsuis[- ]moi\b|\bsuivez[- ]moi\b"), "s'abonner"),
    (re.compile(r"(?i)\blien (?:en|dans (?:ma|la)) bio\b"), "lien en bio"),
    (re.compile(r"(?i)\b(?:swipe|fais défiler|faites défiler|glisse|glissez)\b"), "faire défiler"),
    (re.compile(r"(?i)\bdis[- ]moi\b|\bdites[- ]moi\b|\btu ferais quoi\b|\blaquelle\b|\blequel\b|\bet toi\s?\?"), "répondre à une question"),
]

FILLER_TAGS = {"#viral", "#fyp", "#foryou", "#foryoupage", "#pourtoi", "#pourtoii",
               "#explore", "#explorepage", "#trending", "#tendance", "#instagood",
               "#love", "#follow", "#like4like", "#reels", "#reel", "#tiktok",
               "#reelsinstagram", "#viralreels", "#viraltiktok", "#instadaily", "#xyzbca"}


def visible_window(text, cut):
    """Ce que le fil affiche. Il coupe en plein mot, donc ici aussi."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, label, out=sys.stdout, width=52):
    print(f"\n  CE QUE LE FIL {label.upper()} AFFICHE", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... plus" if truncated else "(tout tient)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, plateforme="instagram", cut=None, keywords=None):
    p = PLATEFORMES[plateforme]
    limit, hashtag_limit = p["limite"], p["hashtags"]
    cut = cut or p["coupe"]
    stripped = text.strip()
    chars = len(stripped)
    first_line = stripped.split("\n")[0].strip() if stripped else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LONGUEUR", "ÉCHEC" if chars > limit else "OK",
        f"{chars} / {limit} caractères" + (f", {chars - limit} de trop" if chars > limit else ""))

    if not first_line:
        add("1RE LIGNE", "ÉCHEC", "la légende commence par une ligne vide")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("1RE LIGNE", "ÉCHEC",
            "commence par un hashtag ou une mention, la seule place qui mérite une phrase")
    elif GREETING_RE.search(first_line):
        add("1RE LIGNE", "ÉCHEC", "commence par une salutation, la place la plus chère gâchée")
    elif len(first_line) > cut:
        add("1RE LIGNE", "ALERTE",
            f"{len(first_line)} caractères, coupée à {cut} en pleine idée. "
            "OK si la coupe crée du suspense, mauvais si elle tombe sur une subordonnée")
    else:
        add("1RE LIGNE", "OK", f"{len(first_line)} caractères, visible en entier")

    n_concrete = len(CONCRETE_RE.findall(window))
    add("CONCRET", "OK" if n_concrete else "ALERTE",
        f"{n_concrete} chiffre(s) ou nom(s) dans la partie visible"
        + ("" if n_concrete else " - rien de vérifiable avant le clic"))

    if len(tags) > hashtag_limit:
        add("HASHTAGS", "ÉCHEC", f"{len(tags)} hashtags, au-dessus du plafond de {hashtag_limit} "
                                 f"sur {p['nom']}. Au-delà du 5e ils ne comptent pas")
    elif len(tags) == hashtag_limit and filler:
        add("HASHTAGS", "ALERTE", f"{len(tags)} hashtags, au plafond, dont {len(filler)} "
                                  "génériques. Garde les cinq places pour des sujets")
    elif filler:
        add("HASHTAGS", "ALERTE", f"{len(tags)} hashtags dont {len(filler)} génériques "
                                  f"({', '.join(filler[:3])}). Ils ne décrivent rien")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f" : {' '.join(tags)}" if tags else ""))

    if not tags:
        add("PLACE TAGS", "OK", "aucun hashtag à placer")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("PLACE TAGS", "ALERTE", "un hashtag est dans la partie visible, "
                                    "de la place du fil dépensée sur une étiquette")
    else:
        add("PLACE TAGS", "OK", "hashtags sous la coupe")

    add("LIENS", "ALERTE" if links else "OK",
        f"{len(links)} lien(s) dans la légende, et la légende n'est pas cliquable. "
        "Mets-le en bio ou en DM" if links else "pas de lien mort dans le texte")

    if len(asks) == 1:
        add("UNE DEMANDE", "OK", f"un seul appel à l'action : {asks[0]}")
    elif not asks:
        add("UNE DEMANDE", "ALERTE", "aucun appel à l'action. Décide à quoi sert ce post")
    else:
        add("UNE DEMANDE", "ALERTE", f"{len(asks)} demandes ({', '.join(asks)}). "
                                     "Deux demandes, c'est comme aucune")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "ALERTE" if density > 4 else "OK",
        f"{len(emoji)} emoji(s), {density:.1f} pour 100 caractères"
        + (" - ça fait déco" if density > 4 else ""))

    if keywords:
        low = stripped.lower().replace("’", "'")
        win = window.lower().replace("’", "'")
        kw = [k.lower().replace("’", "'") for k in keywords]
        found = [k for k, l in zip(keywords, kw) if l in low]
        missing = [k for k, l in zip(keywords, kw) if l not in low]
        in_window = [k for k, l in zip(keywords, kw) if l in win]
        status = "OK" if not missing else ("ALERTE" if found else "ÉCHEC")
        detail = (f"{len(found)}/{len(keywords)} présents"
                  + (f", {len(in_window)} dans la partie visible" if found else "")
                  + (f". Manquant : {', '.join(missing)}" if missing else ""))
        if plateforme == "tiktok":
            detail += ". Sur TikTok, dis-les aussi à l'oral ou affiche-les à l'écran"
        add("RECHERCHE", status, detail)

    fails = sum(1 for c in checks if c["status"] == "ÉCHEC")
    warns = sum(1 for c in checks if c["status"] == "ALERTE")
    verdict = "À CORRIGER" if fails else ("À RELIRE" if warns else "PRÊTE")

    return {
        "plateforme": p["nom"], "characters": chars, "limit": limit, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"LÉGENDE {a['plateforme'].upper()}  ·  {a['characters']} / {a['limit']} car.  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} demande(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], a["plateforme"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<6} {c['check']:<12} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VERDICT  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Vérifie une légende Instagram ou TikTok.")
    ap.add_argument("input", nargs="?", default="-", help="fichier légende, ou - pour stdin")
    ap.add_argument("--plateforme", choices=["instagram", "tiktok", "les-deux"], default="instagram")
    ap.add_argument("--coupe", "--truncate", dest="coupe", type=int,
                    help="caractères visibles avant 'plus' (défaut : 125 Instagram, 90 TikTok)")
    ap.add_argument("--mots-cles", "--keywords", dest="mots_cles", default="",
                    help="termes de recherche séparés par des virgules")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    cibles = ["instagram", "tiktok"] if args.plateforme == "les-deux" else [args.plateforme]
    results = [analyse(raw, c, args.coupe, args.mots_cles.split(",")) for c in cibles]
    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2, ensure_ascii=False))
    else:
        for a in results:
            render(a)
    sys.exit(0 if all(a["verdict"] == "PRÊTE" for a in results) else 1)


if __name__ == "__main__":
    main()
