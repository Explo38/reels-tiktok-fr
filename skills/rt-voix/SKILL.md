---
name: rt-voix
description: >-
  Transforme un script de Reel ou de TikTok en voix off française générée en
  local et gratuitement (Kyutai Pocket TTS par défaut), avec les sous-titres
  .srt calés dessus, sans utiliser la voix de l'utilisateur. Utilise-le quand
  l'utilisateur dit "voix off", "mets une voix", "voix IA", "je veux pas
  mettre ma voix", "génère l'audio", "text to speech", "TTS", "sous-titres de
  la voix", ou quand /rt-video sort un script en mode sans visage avec voix off.
---

# rt-voix

La voix off, sans prêter sa voix. Le script vient de `/rt-video` (ou de
l'utilisateur), ce skill le rend lisible par une voix de synthèse, génère
l'audio en local et écrit les sous-titres calés sur la vraie durée de chaque
phrase.

Deux outils vivent dans ce dossier et ils tournent vraiment :

```bash
python3 preparer_texte.py script.txt -o voix.txt --rapport   # écrit voix.txt + voix.affichage.txt
python3 generer_voix.py voix.txt --sortie voix_off.wav        # écrit voix_off.wav + voix_off.srt
python3 generer_voix.py voix.txt --moteur test                # vérifie la chaîne sans rien installer
```

## Le moteur, et pourquoi celui-là

Par défaut : **Kyutai Pocket TTS** (github.com/kyutai-labs/pocket-tts).

- Gratuit, open source, tourne sur le processeur d'un portable (Mac, Windows,
  Linux). Pas de carte graphique, pas de compte, pas d'abonnement.
- Modèle français natif, voix prédéfinie **estelle** (féminine). Le fichier
  source de cette voix est publié par Kyutai en CC0.
- Code sous licence MIT, poids du modèle en **CC-BY 4.0** : usage commercial
  permis, à condition de créditer. Mets « Voix : Kyutai Pocket TTS (CC-BY
  4.0) » dans la légende, la bio ou les mentions du site.
- `--langue french_24l` donne une meilleure qualité, plus lentement.

Installation (une fois, sur la machine de l'utilisateur) :

```bash
pip install pocket-tts
# Linux sans GPU, version CPU de torch plus légère :
# pip install pocket-tts --extra-index-url https://download.pytorch.org/whl/cpu
```

Le premier lancement télécharge les poids depuis Hugging Face.

### Les autres options, dans l'ordre

| besoin | moteur | voix | licence |
| --- | --- | --- | --- |
| voix d'homme, meilleure qualité | Kyutai TTS 1.6B en_fr (github.com/kyutai-labs/delayed-streams-modeling) | une voix `cml-tts/fr/...` du dépôt kyutai/tts-voices, choisie à l'écoute | poids CC-BY 4.0, voix cml-tts CC BY 4.0. GPU NVIDIA ou Mac Apple Silicon (MLX) |
| le plus léger possible | Piper (`pip install piper-tts`) | `fr_FR-mls-medium` | CC BY 4.0. Plus robotique |

Avec Kyutai TTS 1.6B, passe **toujours** `--voice` : la voix par défaut des
scripts vient d'un jeu de données non commercial.

### À ne pas utiliser pour une pub

- Coqui XTTS-v2 : licence non commerciale, sorties audio comprises.
- F5-TTS : poids non commerciaux.
- edge-tts : utilise le service en ligne de Microsoft sans licence commerciale.
- Piper `fr_FR-tom` (AGPL), `fr_FR-siwis` et `fr_FR-upmc` (filiation avec des
  données non commerciales).
- Les voix Pocket TTS `cosette` et `jean`, et tout le dossier `expresso/` ou
  `ears/` de kyutai/tts-voices : CC BY-NC.
- Toute voix clonée d'une vraie personne sans son accord écrit.

Les autres voix prédéfinies de Pocket TTS existent pour le modèle français mais
viennent d'anglophones : accent garanti. Estelle reste le choix par défaut.

## Avant d'écrire : la fiche voix.md

Lis `~/.claude/reels-tiktok/voix.md` s'il existe : moteur, voix choisie,
vitesse, débit mesuré en mots par minute, mots ajoutés à la prononciation. S'il
n'existe pas, crée-le après la première génération réussie :

```
# voix.md
moteur:   pocket
voix:     estelle
langue:   french
vitesse:  1.0
débit:    {mesuré par generer_voix.py} mots/min
crédit:   Voix : Kyutai Pocket TTS (CC-BY 4.0)
prononciation perso: ~/.claude/reels-tiktok/prononciation.json
```

Le débit mesuré sert ensuite à `minutage.py --mpm` dans `/rt-video`, pour que
le conducteur colle à la vraie voix et pas à une moyenne.

## Écrire pour une voix de synthèse

Un script écrit pour être dit par un humain ne passe pas tel quel. La synthèse
lit ce qui est écrit, pas ce qu'on voulait dire.

- **Une phrase par ligne.** Chaque ligne devient un plan et un sous-titre.
- **Phrases courtes.** Au-delà de 15 mots, l'intonation s'aplatit.
- **La ponctuation, c'est la respiration.** Une virgule = une micro-pause, un
  point = une vraie pause. Pas de parenthèses, pas de tiret, pas de barre
  oblique : `preparer_texte.py` les réécrit, mais mieux vaut ne pas les écrire.
- **Les chiffres** sont convertis en lettres par le script (2 400 € devient
  « deux mille quatre cents euros »). Vérifie le rapport : une année, un
  numéro ou un code peut demander une autre lecture.
- **Les sigles et les marques** passent par `prononciation.json`. Une marque
  mal prononcée dans une pub, c'est la seule chose dont on se souvient.
  Ajoute-la dans `~/.claude/reels-tiktok/prononciation.json` et passe ce
  fichier avec `--prononciation` (la version perso passe avant celle du
  plugin, mais seulement si tu la passes).
- **Pas d'emoji, pas de hashtag, pas de lien** : ils sont retirés, ne compte
  pas dessus pour faire passer une info.
- **Garde le ton de style.md**, mais pas les tics oraux qui sonnent faux en
  synthèse : « euh », « genre » et les phrases inachevées marchent mal.

## La boucle

1. **Récupère le script.** Celui de `/rt-video`, déjà passé par `/rt-humain`.
   Sinon demande-le. Si la vidéo est sans voix (musique seule), ce skill ne
   sert pas : dis-le et renvoie vers `minutage.py --lecture`.
2. **Prépare le texte.** `preparer_texte.py script.txt -o voix.txt --rapport`
   (ajoute `--prononciation ~/.claude/reels-tiktok/prononciation.json` si le
   fichier perso existe).
   Montre à l'utilisateur les conversions du rapport (nombres, prononciation)
   et corrige ce qui sonnerait faux.
3. **Génère.** `generer_voix.py voix.txt --sortie voix_off.wav`. Le script
   sort aussi `voix_off.srt` avec le texte d'affichage (« CV », pas « cé vé »).
4. **Écoute avant tout.** Demande à l'utilisateur d'écouter le .wav en
   entier. Pour chaque mot raté : ajoute-le à la prononciation perso et
   régénère. Pour une intonation ratée sur une ligne : reformule cette ligne
   (plus courte, ponctuation différente) et régénère.
5. **Recale le conducteur.** Relance `minutage.py` avec `--mpm` = le débit
   mesuré. Si la durée dépasse la cible, coupe des mots, ne monte pas la
   vitesse au-delà de 1.15 : ça s'entend.
6. **Rends le bloc :**

```
VOIX OFF PRÊTE
moteur :      Pocket TTS, voix estelle (french)
fichiers :    voix_off.wav  ·  voix_off.srt
durée :       27.4 s pour 9 lignes  ·  débit 171 mots/min
prononciation : 3 ajouts (CV, LinkedIn, le nom de la marque)
crédit :      Voix : Kyutai Pocket TTS (CC-BY 4.0), à mettre en légende ou en bio
étiquette IA : à activer sur TikTok et Instagram (voir ci-dessous)

Montage : importe le .wav sous la musique (musique à -18 / -20 dB sous la voix),
importe le .srt dans CapCut ou l'éditeur, garde les sous-titres dans la zone sûre.
```

## Montage : ce qui change avec une voix off

- **Musique sous la voix**, jamais au même niveau. Baisse la musique pendant
  la voix (ducking), remonte-la sur les plans sans texte.
- **Sous-titres incrustés** à partir du .srt : beaucoup regardent sans le son
  au début. Garde-les entre y=230 et y=1440 sur 1080x1920, loin des 140 px de
  droite.
- **Le texte à l'écran ne recopie pas la voix.** Le carton du hook garde ses
  six mots ; les sous-titres portent le reste.
- **Sons tendance TikTok** : une voix off par-dessus un son tendance est
  possible, mais un compte entreprise n'a pas accès à toute la bibliothèque
  musicale. Vérifie le son avant de monter.

## Étiquette IA : à dire franchement

Une voix de synthèse réaliste est du contenu généré par IA.

- **Publicité TikTok** : coche l'option de contenu généré par IA dans le
  gestionnaire de pubs quand l'audio est généré par IA.
- **Publication normale TikTok** : l'étiquette est obligatoire pour ce qui
  peut passer pour réel. Pour une voix off qui n'imite personne, la règle est
  floue : active l'étiquette « contenu généré par IA », ça ne coûte rien et ça
  protège le compte.
- **Instagram** : Meta demande de signaler un audio réaliste créé ou modifié
  numériquement. Active l'étiquette IA proposée au moment de publier.
- **Jamais** de voix qui imite une personne réelle, connue ou non.

Les règles bougent. Si la plateforme affiche autre chose au moment de publier,
c'est elle qui a raison.

## Ce que ce skill ne fait pas

- Il ne clone pas de voix et ne prend jamais la voix de quelqu'un sans accord.
- Il n'envoie rien en ligne : la génération tourne sur la machine de
  l'utilisateur.
- Il ne publie rien. Il produit un .wav et un .srt, l'utilisateur monte et
  publie.
