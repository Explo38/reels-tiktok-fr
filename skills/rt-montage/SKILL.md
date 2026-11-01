---
name: rt-montage
description: >-
  Fabrique la vidéo motion finale d'un Reel ou d'un TikTok (MP4 vertical
  1080x1920) à partir d'un storyboard : textes animés, captures du site ou de
  l'app dans un téléphone, voix off, musique et sous-titres incrustés. Prend
  aussi les captures d'écran et relève la charte (couleurs, polices) d'un site
  en lecture seule. À utiliser quand l'utilisateur dit "monte la vidéo",
  "fais le motion", "génère la vidéo", "rends le mp4", "fais des captures de
  mon site", ou quand /rt-studio arrive à l'étape de production.
---

# rt-montage

Le script et la voix sont écrits ailleurs (`/rt-video`, `/rt-voix`). Ce skill
les transforme en fichier vidéo prêt à publier.

Deux outils vivent dans ce dossier et ils tournent vraiment :

```bash
python3 capturer.py https://site.fr https://site.fr/tarifs --charte --sortie assets/
python3 rendre.py storyboard.json --sortie video.mp4 --brouillon   # aperçu rapide 540x960
python3 rendre.py storyboard.json --sortie video.mp4               # final 1080x1920
python3 rendre.py storyboard.json --vignette couverture.jpg        # image de couverture
```

Dépendances : Python 3, Pillow, ffmpeg. `capturer.py` demande en plus
Playwright (`pip install playwright && playwright install chromium`). Sans
Playwright, prends les captures avec l'outil de navigateur de la session.

## Règle absolue : le projet est en lecture seule

Le projet de l'utilisateur (site, app, dossier de code, dépôt) sert de
**source**. Il n'est jamais modifié.

- **Interdit** : écrire, créer, déplacer ou supprimer un fichier dans le
  dossier du projet ; lancer une commande qui écrit dedans (install, build,
  format, git commit, git push, migrations) ; remplir un formulaire ou se
  connecter sur le site ; ouvrir une pull request.
- **Autorisé** : lire des fichiers, charger des pages, prendre des captures,
  relever des couleurs et des polices, copier un asset (logo, image,
  illustration) **vers le dossier de campagne**.
- Tout ce qui est produit va dans le dossier de campagne
  `~/.claude/reels-tiktok/campagnes/<campagne>/` (ou le dossier de sortie que
  l'utilisateur a désigné), jamais à côté du code.
- Si une étape demanderait d'écrire dans le projet, arrête-toi et dis-le.

## Récupérer les assets

1. **Captures d'écran** : `capturer.py` en format téléphone (390x844 en x3,
   ce qui donne une image nette dans le cadre téléphone). Capture les écrans
   qui montrent la promesse : accueil, résultat, avant / après. Pas
   d'écran de connexion, pas de données personnelles, pas de faux contenu.
2. **La charte** : `--charte` écrit `charte.json` (couleurs de texte et de
   fond les plus utilisées, couleur des boutons, polices, logo). Reporte-la
   dans le bloc `charte` du storyboard. Si le projet a déjà un design system
   (variables CSS, tokens, fichier de thème), lis-le plutôt : c'est plus juste.
3. **Polices** : si la police du site est installée sur la machine, passe son
   fichier .ttf ou .otf dans `charte.police`. Sinon le script prend une
   police système lisible (Arial, Inter ou DejaVu).
4. **Logo et images** : copie-les dans `assets/` de la campagne.

## Le storyboard

Un fichier JSON par vidéo. Voir `exemple_storyboard.json`. Une scène par
temps du conducteur de `/rt-video` (`minutage.py`), même durée.

| champ | rôle |
| --- | --- |
| `duree` | secondes à l'écran (la dernière scène s'allonge si la voix est plus longue) |
| `fond` / `degrade` | couleur, dégradé de deux couleurs, ou image plein écran |
| `image` + `cadre` | capture dans un `telephone`, une `carte`, ou `aucun` cadre |
| `titre` | texte principal. `*mot*` passe le mot en couleur d'accent |
| `sous_titre` | texte secondaire |
| `position` | `haut`, `centre`, `bas` (toujours dans la zone sûre) |
| `animation` | `monte`, `fondu`, `pop`, `aucune` |
| `zoom` | `lent` sur les captures pour qu'il y ait du mouvement |
| `couleur_texte` | force la couleur, sinon contraste automatique |

Bloc `audio` : `voix` (le .wav de `/rt-voix`), `sous_titres` (son .srt),
`musique` (fichier audio dont l'utilisateur a les droits), `volume_musique`
(0.15 sous une voix, 0.9 sans voix).

Règles de mise en forme :

- **Le hook est la scène 1**, à l'écran dès la première image, 6 mots max,
  `animation: pop` ou `monte`.
- **Une idée par scène**, une scène toutes les 2 à 4 secondes. Le mouvement
  (zoom lent, entrée du texte) évite l'image fixe.
- **Zone sûre** : le script garde tout entre y=230 et y=1440 et laisse les
  140 px de droite libres. Avec sous-titres, l'image se réduit pour laisser la
  bande basse aux sous-titres.
- **Dernière scène = la demande** (commenter un mot-clé, lien en bio...) et
  un mot repris du hook pour la boucle.

## La musique

- Le script n'invente pas de musique. Il faut un fichier dont l'utilisateur a
  les droits : sa propre musique, une bibliothèque libre de droits avec une
  licence qui couvre l'usage commercial (lis la licence), ou rien.
- **Sons tendance TikTok ou Instagram** : ils s'ajoutent dans l'application au
  moment de publier, pas dans le fichier. Dans ce cas, rends la vidéo sans
  musique (ou avec la voix seule) et note « son à ajouter dans l'appli » dans
  la fiche du post. Un compte professionnel n'a accès qu'à une partie de la
  bibliothèque musicale.

## La boucle

1. Écris le storyboard à partir du conducteur et de la recette motion choisie
   (voix / texte / musique / captures).
2. Rends un **brouillon** (`--brouillon`, 540x960). Extrais 4 ou 5 images
   (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 image.png`) et **regarde-les** :
   texte lisible, rien hors zone sûre, pas de texte sur une capture chargée,
   sous-titres qui ne masquent rien. Corrige le storyboard.
3. Rends la version finale et la vignette de couverture.
4. Rends la fiche :

```
MONTAGE PRÊT
fichier :     post-03_tiktok.mp4  (1080x1920, 27,4 s, 9 scènes)
couverture :  post-03_couverture.jpg
audio :       voix estelle + musique (-18 dB) + sous-titres incrustés
assets :      3 captures du site (lecture seule), logo
à faire :     son tendance à ajouter dans l'appli TikTok (optionnel)
```

Rien n'est publié par ce skill. La publication, c'est `/rt-publication`,
après validation.
