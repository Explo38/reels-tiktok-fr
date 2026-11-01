# reels-tiktok-fr

17 skills Claude, en français, pour produire et piloter du contenu court sur
Instagram et TikTok. Vidéos face caméra ou sans visage (voix off IA, texte
animé, musique, captures de ton projet), carrousels, légendes, stories,
profil, planning, réponses, DM, audit, montage vidéo et programmation.
Gratuit, licence MIT.

**Pour commencer : `/rt-studio`.** Il te pose quelques questions et enchaîne
tous les autres skills tout seul, de l'analyse de tes comptes jusqu'à la
programmation des posts.

**Rien n'est publié sans ta validation**, et ton projet reste en lecture seule.

Adapté de [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
de Jake Schincariol (licence MIT).
Cette version est réécrite en français, étendue à TikTok et au contenu sans
visage, avec une commande de voix off en plus.

## Les 17 commandes

| commande | ce qu'elle fait |
| --- | --- |
| `/rt-studio` | **Le point d'entrée.** Analyse tes comptes, propose le plan de com, te demande formats et recette motion, capture ton projet en lecture seule, produit tous les posts, sort une planche de validation, puis programme ce que tu as validé. |
| `/rt-montage` | Fabrique la vidéo MP4 1080x1920 depuis un storyboard (texte animé, captures dans un téléphone, voix, musique, sous-titres) et les diapos des carrousels. Capture ton site et relève sa charte, en lecture seule. |
| `/rt-publication` | Programme les posts validés sur Instagram et TikTok aux meilleurs horaires : Metricool (connecteur officiel), planificateurs natifs, ou kit manuel. Rien ne part sans ton « oui ». |
| `/rt-video` | Une idée en vidéo (Reel ou TikTok). Trois hooks parmi 26 formules, notés, puis le script, le texte à l'écran et un minutage par séquence. Face caméra ou sans visage. |
| `/rt-veille` | Trouve ce qui marche dans ta niche, classe par multiple sur la médiane de chaque compte, nomme la formule, écrit le fichier de veille. |
| `/rt-legende` | La légende, vérifiée. Montre ce que le fil affiche avant "plus" (environ 125 caractères sur Instagram, 80 à 100 sur TikTok). |
| `/rt-carrousel` | Carrousel Instagram ou mode photo TikTok : la couverture qui donne envie de swiper, le texte de chaque slide, les bons formats. |
| `/rt-story` | La séquence de stories du jour, quel sticker pour quel rôle, et le tunnel DM qui démarre quand la personne bouge en premier. |
| `/rt-profil` | Note ton profil sur 100 avec une grille de 12 critères, puis réécrit dans l'ordre des corrections. |
| `/rt-planning` | La semaine : quoi publier, quel format, quand, sur quelle plateforme, et les 10 comptes avec qui interagir. |
| `/rt-humain` | Le nettoyeur anti-style IA. Deux scripts qui tournent vraiment. Tout passe par lui avant de t'être montré. |
| `/rt-commentaire` | Commentaires sous les publications des autres. Choisis selon ce qu'est vraiment la publication. Jamais "🔥🔥🔥". |
| `/rt-reponse` | Le fil sous ta propre publication : trie (mot-clé, prospect, fond, question, soutien, bruit) puis répond dans cet ordre. Sur TikTok, propose les réponses vidéo. |
| `/rt-dm` | La livraison après mot-clé, le premier message, la proposition de collab, et les deux relances. Deux. |
| `/rt-recyclage` | Une vidéo, un podcast ou une newsletter en une semaine de vidéos et de carrousels qui tiennent seuls. |
| `/rt-audit` | Bilan de ce que tu as publié, stats Instagram et TikTok Studio. Classe par multiple de surperformance et partages par portée, pas par vues. |
| `/rt-voix` | Voix off en français par synthèse vocale gratuite et locale, pour les vidéos sans visage. Enregistre tes réglages dans `voix.md`. |

## Les scripts

Python 3, sans réseau. Sans dépendance, sauf la voix (pocket-tts) et le montage (Pillow, ffmpeg, Playwright pour les captures). Ils tournent sur ta machine, sur ton
texte. Lance-les depuis le dossier du skill (`skills/rt-video/`, etc.).

```bash
# rt-video
python3 score_hook.py hooks.txt                 # classe tes hooks (un par ligne)
python3 score_hook.py --hook "une seule ligne"  # note un hook
python3 minutage.py script.txt --cible 30       # minute le script avant de tourner
python3 minutage.py script.txt --mpm 175        # avec ton rythme (défaut 160 mots/min)

# rt-legende
python3 legende.py legende.txt --plateforme tiktok
python3 legende.py legende.txt --plateforme instagram --mots-cles "recherche d'emploi,lettre de motivation"

# rt-humain
python3 humaniser.py brouillon.txt -o propre.txt --rapport   # nettoie, montre chaque changement
python3 detecter.py brouillon.txt                            # note le texte, 5 contrôles
python3 detecter.py avant.txt apres.txt                      # compare avant / après

# rt-veille
python3 veille.py capture.tsv --out ~/.claude/reels-tiktok/veille.md

# rt-video, vidéo sans voix (texte à l'écran + musique)
python3 minutage.py cartons.txt --lecture --cible 15

# rt-montage (vidéo et diapos ; Pillow + ffmpeg, Playwright pour les captures)
python3 capturer.py https://ton-site.fr --charte --sortie assets/
python3 rendre.py storyboard.json --sortie video.mp4 --brouillon
python3 rendre.py storyboard.json --sortie video.mp4
python3 rendre.py carrousel.json --diapos diapos/

# rt-studio (planche de validation)
python3 planche.py ~/.claude/reels-tiktok/campagnes/<campagne>/campagne.json

# rt-voix (voix off locale)
python3 preparer_texte.py script.txt -o voix.txt --rapport   # chiffres en lettres, sigles, une phrase par ligne
python3 generer_voix.py voix.txt --sortie voix_off.wav        # voix_off.wav + voix_off.srt
```

### La voix off : Kyutai Pocket TTS

`/rt-voix` utilise par défaut [Kyutai Pocket TTS](https://github.com/kyutai-labs/pocket-tts) :
gratuit, open source, tourne sur le processeur d'un portable, voix française
native « estelle ». Code MIT, poids CC-BY 4.0 : usage commercial permis avec
crédit (« Voix : Kyutai Pocket TTS (CC-BY 4.0) »). C'est le seul script du pack
qui a une dépendance :

```bash
pip install pocket-tts
python3 generer_voix.py voix.txt --moteur test   # vérifie la chaîne sans modèle
```

Le premier vrai lancement télécharge le modèle. Le skill liste aussi les
alternatives (voix d'homme, plus léger) et les moteurs à éviter pour une pub.

Ce qu'ils font, en bref :

- **score_hook.py** note un hook sur 5 contrôles (LONGUEUR, PRÉCISION, ENJEU,
  ATTAQUE, ADRESSE) et rend FORT, CORRECT ou FAIBLE. C'est une heuristique : il
  écarte les mauvais hooks (salutation, préambule, rien de concret), il ne
  départage pas deux bons. Pour ça, ta courbe de rétention fait foi.
- **minutage.py** estime la durée de chaque ligne, empile les timecodes et
  signale un hook trop long, une séquence où l'on décroche, et l'absence de
  boucle vers la première ligne. Pour une voix off IA, mets `--mpm` à la vitesse
  mesurée dans `voix.md`.
- **legende.py** affiche la partie visible avant "plus", vérifie la longueur,
  les 5 hashtags max et la présence de tes mots-clés de recherche.
- **humaniser.py** enlève les caractères invisibles, corrige la typographie
  (tirets longs compris) et remplace les tics IA listés dans `lexique.json`.
  **detecter.py** donne un score sur 5 contrôles (RAFALE, PRÉCISION, DENSITÉ
  CLICHÉS, EMPREINTE, VOIX) et un verdict OK, À REVOIR ou SIGNALÉ.
- **veille.py** classe des vidéos capturées à la main (colonnes TSV :
  `compte  plateforme  abonnes  mediane  vues  hook`) par multiple sur la
  médiane du compte et nomme la formule.

## Installation

**1. Depuis ton propre dépôt GitHub (Claude.ai, appli de bureau).**
Pousse ce dossier sur un dépôt GitHub à toi, puis dans Claude :
Personnaliser > Plugins > Ajouter une place de marché, et indique ton dépôt.

**2. Dans Claude Code.**

```
/plugin marketplace add <ton-compte>/reels-tiktok-fr
/plugin install reels-tiktok-fr
```

**3. Sans rien installer.** Colle un seul `SKILL.md` en haut d'une conversation
et il tourne comme un mode. Tu perds les scripts Python (l'essentiel de
`/rt-video` et `/rt-humain`), le reste marche.

## Tes fichiers : `~/.claude/reels-tiktok/`

Chaque campagne de `/rt-studio` a son dossier `campagnes/<date>-<nom>/` :
`campagne.json` (l'état de chaque post), `plan.md`, `assets/`, un dossier par
post, `revue.html` (la planche de validation) et `publication.csv`.


| fichier | rôle |
| --- | --- |
| `style.md` | ta façon de parler, ton format (face caméra ou sans visage), tes positions, tes preuves. À remplir en premier. |
| `veille.md` | le fichier de veille, écrit par `/rt-veille` |
| `journal.md` | ce que tu as publié, avec la formule de hook, lu par `/rt-audit` |
| `planning.md` | la semaine en cours, écrit par `/rt-planning` |
| `voix.md` | tes réglages de voix off (moteur, voix, vitesse), écrit par `/rt-voix` |

Pour démarrer : copie `templates/style.md` dans `~/.claude/reels-tiktok/` et
remplis-le, ou envoie trois de tes vidéos à Claude en disant "écris mon
style.md à partir de ça". Tous les skills le lisent.

## Ce que ça ne fait pas

- **Ça ne publie rien sans ta validation.** `/rt-publication` ne programme que
  les posts que tu as validés, après un récapitulatif auquel tu dis « oui ». Il
  passe par un outil officiel (Metricool, avec son connecteur Claude), par les
  planificateurs natifs (Meta Business Suite, TikTok Studio) ou te donne un kit
  pour publier toi-même. Jamais de mot de passe saisi, jamais de robot connecté
  à ton compte.
- **Ton projet reste en lecture seule.** Captures, couleurs, polices, logo :
  tout est lu et copié dans le dossier de campagne. Aucun fichier du projet
  n'est créé, modifié ou supprimé, aucune commande n'y écrit.
- **Pas de scraping, pas de DM en masse, pas de commentaires automatisés.** Ça
  viole les conditions d'utilisation d'Instagram et de TikTok et ça fait
  restreindre les comptes. Seule exception : les réponses automatiques par
  mot-clé prévues par les plateformes, qui ne partent qu'après que la personne a
  commenté. `/rt-dm` dit où est la limite.
- **`/rt-veille` lit, il n'aspire pas.** Quelques comptes, à vitesse humaine,
  c'est toi qui navigues.
- **Rien d'inventé.** Pas de faux chiffres, clients ou résultats sous ton nom.
  S'il manque un chiffre, le brouillon revient avec `{{ton chiffre}}` et un
  signalement.
- **Les contrôles anti-IA sont des heuristiques locales**, pas des détecteurs
  du commerce. Personne ne peut honnêtement te vendre de l'"indétectable".
- **Les règles des plateformes bougent.** Les limites indiquées (légendes,
  hashtags, formats) datent de novembre 2026. Si l'appli dit autre chose quand
  tu lis ça, l'appli a raison.

## Licence

MIT, comme l'original. Prends, modifie, publie.
