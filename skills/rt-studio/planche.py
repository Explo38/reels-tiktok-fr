#!/usr/bin/env python3
"""
planche.py - fabrique la planche de validation d'une campagne : une page HTML
avec chaque post (vidéo ou diapos, couverture, légendes par plateforme,
créneau prévu, statut), à ouvrir dans un navigateur pour tout relire d'un coup.

Lit campagne.json (voir modele_campagne.json) et écrit revue.html à côté.
Les chemins des fichiers sont relatifs au dossier de campagne.

Usage
  python3 planche.py ~/.claude/reels-tiktok/campagnes/lancement-novembre/campagne.json
  python3 planche.py campagne.json --sortie revue.html
"""

import argparse
import html
import json
import os
import sys

STATUTS = {
    "brouillon": ("#64748B", "Brouillon"),
    "à revoir": ("#D97706", "À revoir"),
    "validé": ("#16A34A", "Validé"),
    "programmé": ("#2563EB", "Programmé"),
    "publié": ("#7C3AED", "Publié"),
    "à faire": ("#DC2626", "À faire à la main"),
}

CSS = """
:root{--bg:#F8FAFC;--card:#fff;--txt:#0F172A;--mut:#64748B;--line:#E2E8F0}
@media (prefers-color-scheme:dark){:root{--bg:#0B1120;--card:#111827;--txt:#F1F5F9;--mut:#94A3B8;--line:#1F2937}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.5 -apple-system,BlinkMacSystemFont,Inter,Segoe UI,Roboto,sans-serif}
header{padding:24px 16px 8px;max-width:1200px;margin:auto}h1{margin:0 0 4px;font-size:24px}.mut{color:var(--mut)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px;padding:16px;max-width:1200px;margin:auto}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:10px}
.top{display:flex;justify-content:space-between;align-items:center;gap:8px}.id{font-weight:700}
.badge{color:#fff;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:600;white-space:nowrap}
video,img.cover{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:12px;background:#000}
.slides{display:flex;gap:6px;overflow-x:auto}.slides img{height:220px;border-radius:8px}
.chips span{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;margin:0 4px 4px 0;font-size:12px}
details{border-top:1px solid var(--line);padding-top:6px}summary{cursor:pointer;font-weight:600}
pre{white-space:pre-wrap;font:13px/1.45 ui-monospace,Menlo,monospace;background:var(--bg);padding:8px;border-radius:8px;margin:6px 0}
.todo{color:#DC2626;font-size:13px}.recap{max-width:1200px;margin:auto;padding:0 16px}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:6px;text-align:left}
"""


def e(x):
    return html.escape(str(x or ""))


def media(post, base):
    f = post.get("fichiers", {})
    out = []
    if f.get("video"):
        poster = f' poster="{e(f.get("couverture"))}"' if f.get("couverture") else ""
        out.append(f'<video controls preload="metadata" playsinline src="{e(f["video"])}"{poster}></video>')
    elif f.get("slides"):
        imgs = "".join(f'<img src="{e(s)}" alt="diapo {i + 1}">' for i, s in enumerate(f["slides"]))
        out.append(f'<div class="slides">{imgs}</div>')
    elif f.get("couverture"):
        out.append(f'<img class="cover" src="{e(f["couverture"])}" alt="couverture">')
    missing = [v for k, v in f.items() if isinstance(v, str) and not os.path.exists(os.path.join(base, v))]
    if missing:
        out.append(f'<div class="todo">Fichier introuvable : {e(", ".join(missing))}</div>')
    return "".join(out)


def card(post, base):
    color, label = STATUTS.get(post.get("statut", "brouillon"), STATUTS["brouillon"])
    plats = post.get("plateformes", [])
    chips = "".join(f"<span>{e(x)}</span>" for x in
                    [post.get("format")] + plats + ([f"formule #{post['formule']}"] if post.get("formule") else []))
    legs = "".join(
        f"<details{' open' if i == 0 else ''}><summary>Légende {e(p)}</summary><pre>{e(t)}</pre></details>"
        for i, (p, t) in enumerate((post.get("legendes") or {}).items()))
    slots = post.get("creneaux") or {}
    slot_txt = " · ".join(f"{e(p)} {e(v)}" for p, v in slots.items()) or "créneau à choisir"
    todo = "".join(f'<div class="todo">À faire : {e(t)}</div>' for t in post.get("a_faire", []))
    ia = "Étiquette IA : oui" if post.get("etiquette_ia") else "Étiquette IA : non"
    script = f"<details><summary>Script / cartons</summary><pre>{e(post.get('script'))}</pre></details>" \
        if post.get("script") else ""
    com = f'<div class="mut">Note : {e(post["commentaire"])}</div>' if post.get("commentaire") else ""
    return f"""<article class="card">
<div class="top"><span class="id">{e(post.get('id'))} · {e(post.get('theme'))}</span>
<span class="badge" style="background:{color}">{label}</span></div>
<div class="mut">Hook : « {e(post.get('hook'))} »</div>
{media(post, base)}
<div class="chips">{chips}</div>
<div class="mut">{slot_txt} · {ia}</div>{todo}{com}
{legs}{script}
</article>"""


def recap(posts):
    rows = []
    for p in posts:
        for plat in p.get("plateformes", []):
            rows.append(f"<tr><td>{e(p.get('id'))}</td><td>{e((p.get('creneaux') or {}).get(plat, '-'))}</td>"
                        f"<td>{e(plat)}</td><td>{e(p.get('format'))}</td>"
                        f"<td>{e(STATUTS.get(p.get('statut', 'brouillon'), ('', p.get('statut')))[1])}</td></tr>")
    return ("<section class='recap'><h2>Calendrier</h2><table><tr><th>Post</th><th>Créneau</th>"
            "<th>Plateforme</th><th>Format</th><th>Statut</th></tr>" + "".join(rows) + "</table></section>")


def main():
    ap = argparse.ArgumentParser(description="Planche de validation d'une campagne.")
    ap.add_argument("campagne", help="chemin de campagne.json")
    ap.add_argument("--sortie", help="fichier HTML (défaut : revue.html à côté)")
    args = ap.parse_args()
    path = os.path.expanduser(args.campagne)
    c = json.load(open(path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(path))
    posts = c.get("posts", [])
    counts = {}
    for p in posts:
        counts[p.get("statut", "brouillon")] = counts.get(p.get("statut", "brouillon"), 0) + 1
    summary = " · ".join(f"{n} {STATUTS.get(s, ('', s))[1].lower()}" for s, n in counts.items())
    doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Revue de campagne</title>
<style>{CSS}</style></head><body>
<header><h1>{e(c.get('nom', 'Campagne'))}</h1>
<div class="mut">{len(posts)} posts · {summary}</div></header>
<main class="grid">{''.join(card(p, base) for p in posts)}</main>
{recap(posts)}
<p class="mut" style="text-align:center;padding:24px">Valide dans la conversation : « je valide 1, 2, 4 » ou « refais le 3 avec un autre hook ».</p>
</body></html>"""
    out = args.sortie or os.path.join(base, "revue.html")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"planche : {out}  ({len(posts)} posts, {summary})", file=sys.stderr)


if __name__ == "__main__":
    main()
