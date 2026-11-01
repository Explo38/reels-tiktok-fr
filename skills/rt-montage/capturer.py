#!/usr/bin/env python3
"""
capturer.py - prend des captures d'écran d'un site (format téléphone ou
ordinateur) et relève sa charte (couleurs, polices, logo), en LECTURE SEULE.

Il ne fait que charger des pages et lire ce qu'elles affichent. Il n'écrit
rien dans le projet, ne remplit aucun formulaire, ne se connecte à rien.
Tout ce qu'il produit va dans le dossier --sortie (le dossier de campagne),
jamais dans le dossier du projet.

Dépendance : Playwright (pip install playwright && playwright install chromium).
Sans Playwright, prends les captures avec l'outil de navigateur de la session.

Usage
  python3 capturer.py https://exemple.fr https://exemple.fr/tarifs --sortie assets/
  python3 capturer.py https://exemple.fr --ordinateur --pleine-page --sortie assets/
  python3 capturer.py https://exemple.fr --charte --sortie assets/   # écrit aussi charte.json
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

JS_CHARTE = r"""
() => {
  const count = (m, k) => { if (!k) return; m[k] = (m[k] || 0) + 1; };
  const colors = {}, bgs = {}, fonts = {};
  const els = Array.from(document.querySelectorAll('body *')).slice(0, 4000);
  for (const el of els) {
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) continue;
    const s = getComputedStyle(el);
    if (el.childNodes.length && el.innerText && el.innerText.trim()) count(colors, s.color);
    if (s.backgroundColor && !s.backgroundColor.includes('rgba(0, 0, 0, 0)')) count(bgs, s.backgroundColor);
    count(fonts, s.fontFamily.split(',')[0].replace(/["']/g, '').trim());
  }
  const btn = document.querySelector('a[class*="btn"], button, a[class*="button"]');
  const btnStyle = btn ? getComputedStyle(btn) : null;
  const logo = Array.from(document.querySelectorAll('header img, nav img, img[alt*="logo" i], img[src*="logo" i], svg[class*="logo" i]'))[0];
  const icon = document.querySelector('link[rel*="icon"]');
  return {
    titre: document.title,
    couleurs_texte: colors, couleurs_fond: bgs, polices: fonts,
    bouton: btnStyle ? {fond: btnStyle.backgroundColor, texte: btnStyle.color} : null,
    logo: logo && logo.src ? logo.src : null,
    icone: icon ? icon.href : null,
    theme_color: (document.querySelector('meta[name="theme-color"]') || {}).content || null
  };
}
"""


def rgb_to_hex(v):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", v or "")
    return "#%02X%02X%02X" % tuple(int(x) for x in m.groups()) if m else None


def top(d, n=5):
    return [k for k, _ in sorted(d.items(), key=lambda kv: -kv[1])[:n]]


def slug(url):
    p = urlparse(url)
    s = (p.netloc + p.path).strip("/").replace("/", "_") or "page"
    return re.sub(r"[^\w.-]", "-", s)[:80]


def main():
    ap = argparse.ArgumentParser(description="Captures d'écran et charte d'un site, en lecture seule.")
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--sortie", default="assets", help="dossier de campagne où écrire les images")
    ap.add_argument("--ordinateur", action="store_true", help="format 1440x900 au lieu d'un téléphone")
    ap.add_argument("--pleine-page", action="store_true", help="capture toute la page, pas seulement l'écran")
    ap.add_argument("--charte", action="store_true", help="relève couleurs, polices, logo -> charte.json")
    ap.add_argument("--attendre", type=float, default=1.5, help="secondes d'attente après chargement")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright manque : pip install playwright && playwright install chromium\n"
                 "Sinon, prends les captures avec l'outil de navigateur de la session.")

    os.makedirs(args.sortie, exist_ok=True)
    charte = None
    with sync_playwright() as p:
        browser = p.chromium.launch()
        if args.ordinateur:
            ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        else:
            ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3,
                                      is_mobile=True, has_touch=True,
                                      user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                                                 "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                                                 "Mobile/15E148 Safari/604.1")
        page = ctx.new_page()
        for url in args.urls:
            try:
                page.goto(url, wait_until="networkidle", timeout=45000)
            except Exception as e:  # page lente : on capture quand même
                print(f"  {url} : chargement incomplet ({e.__class__.__name__})", file=sys.stderr)
            page.wait_for_timeout(int(args.attendre * 1000))
            out = os.path.join(args.sortie, f"capture_{slug(url)}{'_ordi' if args.ordinateur else ''}.png")
            page.screenshot(path=out, full_page=args.pleine_page)
            print(f"  capture : {out}", file=sys.stderr)
            if args.charte and charte is None:
                raw = page.evaluate(JS_CHARTE)
                charte = {
                    "source": url,
                    "titre": raw.get("titre"),
                    "couleurs_texte": [c for c in (rgb_to_hex(x) for x in top(raw["couleurs_texte"])) if c],
                    "couleurs_fond": [c for c in (rgb_to_hex(x) for x in top(raw["couleurs_fond"])) if c],
                    "polices": top(raw["polices"], 3),
                    "bouton": {k: rgb_to_hex(v) for k, v in (raw.get("bouton") or {}).items()},
                    "theme_color": raw.get("theme_color"),
                    "logo_url": raw.get("logo"),
                    "icone_url": raw.get("icone"),
                }
        browser.close()

    if charte:
        path = os.path.join(args.sortie, "charte.json")
        json.dump(charte, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  charte : {path}", file=sys.stderr)
        print(json.dumps(charte, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
