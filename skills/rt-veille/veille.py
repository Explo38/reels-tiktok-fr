#!/usr/bin/env python3
"""
veille.py - classe des vidéos relevées à la main (Reels et TikTok) selon leur
multiple de surperformance, nomme la formule de hook de chacune et écrit le
fichier de veille.

Les vues brutes ne prouvent rien. Un compte à 2 millions d'abonnés qui fait
400 000 vues a eu un mardi calme. Un compte à 4 000 abonnés qui fait 400 000
vues a trouvé quelque chose. Le multiple = vues / médiane récente du compte.
Au-dessus de 3x, c'est un signal. Sous 1,5x, c'est un jour normal.

Entrée : un fichier séparé par des tabulations, avec une ligne d'en-tête :

  compte	plateforme	abonnes	mediane	vues	hook
  @quelquun	tiktok	48000	11000	412000	personne ne te dit que tes 30 premières vidéos vont flopper

Colonnes obligatoires : vues, hook. La médiane est fortement conseillée ; sans
elle, le script retombe sur le nombre d'abonnés, ce qui est bien moins fiable.
Les en-têtes anglais (account, platform, followers, median, views, hook) sont
acceptés aussi.

Usage
  python3 veille.py capture.tsv
  python3 veille.py capture.tsv --out ~/.claude/reels-tiktok/veille.md
  python3 veille.py capture.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "rt-video", "hooks.json")
WORD_RE = re.compile(r"[\wÀ-ÿœŒ$€%+'’-]+")

ALIASES = {
    "compte": "account", "account": "account",
    "plateforme": "platform", "platform": "platform",
    "abonnes": "followers", "abonnés": "followers", "followers": "followers",
    "mediane": "median", "médiane": "median", "median": "median",
    "vues": "views", "views": "views",
    "hook": "hook", "accroche": "hook",
}

try:                                              # facultatif : noter les hooks aussi
    sys.path.insert(0, os.path.join(HERE, "..", "rt-video"))
    from score_hook import run as score_hook      # noqa: E402
except Exception:                                 # rt-veille copié seul
    score_hook = None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "non classé"
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "non classé"


def to_int(value):
    """'412 000', '412k', '1,2M' -> entier."""
    v = (value or "").strip().lower().replace(" ", "").replace(" ", "").replace(" ", "")
    m = re.match(r"^(\d+(?:[.,]\d+)?)(k|m)$", v)
    if m:
        n = float(m.group(1).replace(",", "."))
        return int(n * (1000 if m.group(2) == "k" else 1_000_000))
    digits = re.sub(r"[^\d]", "", v)
    return int(digits) if digits else None


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [ALIASES.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "platform", "followers", "median", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = to_int(r.get("views")) or 0
        for k in ("followers", "median"):
            r[k] = to_int(r.get(k))
        r["platform"] = (r.get("platform") or "").lower() or "?"
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    platforms = {}
    for r in ranked:
        platforms[r["platform"]] = platforms.get(r["platform"], 0) + 1
    return {
        "baseline": "médiane du compte" if used_median else "nombre d'abonnés",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "platforms": platforms,
        "videos": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "non classé"),
    }


def fmt(n):
    return f"{n:,}".replace(",", " ")


def render(a, out=sys.stdout):
    plats = ", ".join(f"{k} {v}" for k, v in a["platforms"].items())
    head = (f"VEILLE  ·  {a['n']} vidéos ({plats})  ·  {a['accounts']} comptes  ·  "
            f"base : {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["videos"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        plat = {"tiktok": "TT", "instagram": "IG", "youtube": "YT"}.get(r["platform"], "? ")
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:22]:<22} {plat} "
              f"{r.get('account', '')[:16]:<16} {fmt(r['views']):>11}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("CE QUI MARCHE DANS CE LOT", file=out)
    if a["top_formulas"]:
        print("  tiers du haut :        "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  score hook médian :    haut {a['top_hook_score']:.0f}  "
              f"contre bas {a['bottom_hook_score']:.0f}", file=out)
    print(f"  longueur hook médiane : haut {a['top_words']} mots  "
          f"contre bas {a['bottom_words']} mots", file=out)
    print(f"  non classés :          {a['unclassified']} sur {a['n']}. Lis-les à la main, "
          "c'est là que se cache une formule que tu n'as pas encore.", file=out)
    if a["baseline"] != "médiane du compte":
        print("\n  Attention : pas de médiane, le classement se fait sur les abonnés. "
              "C'est bien moins fiable.", file=out)
    print("\n  Un lot relevé à la main est un indice, pas une preuve. Douze vidéos ne montrent "
          "rien ;\n  quarante sur six comptes montrent quelque chose. Relève plus avant d'y croire.\n",
          file=out)


def to_markdown(a):
    lines = ["# Veille", "",
             f"{a['n']} vidéos sur {a['accounts']} comptes. "
             f"Classées par multiple sur la {a['baseline']}.", ""]
    for r in a["videos"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        fid = f"#{r['formula_id']} " if r["formula_id"] else ""
        lines += [f"## {mult}  {fid}{r['formula']}  ({r.get('account', '')}, {r['platform']})",
                  f"- vues : {fmt(r['views'])}  base : {fmt(r['baseline'])}",
                  f"- score hook : {r['hook_score']}  mots : {r['words']}",
                  f"- hook : \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Classe des vidéos relevées par multiple de surperformance.")
    ap.add_argument("input", nargs="?", default="-", help="fichier TSV, ou - pour stdin")
    ap.add_argument("--hooks", default=HOOKS, help="chemin de rt-video/hooks.json")
    ap.add_argument("--out", "--sortie", dest="out", help="écrit aussi le fichier de veille en markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("aucune ligne exploitable. Il faut un fichier séparé par tabulations avec au moins "
              "vues et hook.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("note : hooks.json introuvable, formules non nommées. Passe --hooks.", file=sys.stderr)
    if score_hook is None:
        print("note : score_hook.py introuvable, scores de hook ignorés.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"écrit : {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
