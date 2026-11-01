---
name: rt-video
description: >-
  Écrit une vidéo courte (Reel Instagram et/ou TikTok) à partir d'une idée brute :
  trois hooks tirés de 26 formules et notés, le script parlé (ou le texte de voix
  off IA), le texte à l'écran et un minutage temps par temps, dans le style de
  l'utilisateur. Gère le mode face caméra et le mode sans visage (motion design,
  texte à l'écran, musique, voix off IA). À utiliser dès que l'utilisateur dit
  "écris un tiktok", "fais-moi un reel", "script vidéo", "un hook pour ma vidéo",
  "texte de voix off", "vidéo sans visage", "qu'est-ce que je dis dans cette
  vidéo", ou qu'il va tourner et n'a pas encore sa première phrase.
---

# rt-video

Transforme une idée brute en vidéo courte que les gens regardent jusqu'au bout.
Reel Instagram, TikTok, ou les deux avec le même fichier.

Deux outils sont dans ce dossier et ils tournent vraiment. Sers-t'en. Ne juge
pas le hook à l'œil et ne devine pas la durée.

```bash
python3 score_hook.py hooks.txt              # classe tes options de hook
python3 score_hook.py --hook "une ligne"     # note un seul hook
python3 minutage.py script.txt --cible 30    # minutage temps par temps avant de tourner
python3 minutage.py script.txt --cible 30 --mpm 175   # avec la vitesse d'une voix IA
```

## Avant d'écrire

1. **Lis `~/.claude/reels-tiktok/style.md` s'il existe.** C'est le profil de
   style de l'utilisateur : sa façon de parler, ce qu'il ne dit jamais, à qui il
   s'adresse. S'il n'existe pas, demande **trois de ses propres vidéos** (ou,
   en mode sans visage, trois textes qu'il a écrits : légendes, cartons, posts),
   transcris-les ou lis-les, déduis le style et écris le fichier à partir du
   modèle `templates/style.md` du plugin. Un script dans le mauvais style est
   inutilisable : il faut le dire à voix haute, ou le faire dire par une voix
   qui doit sonner comme lui.
2. **Lis `hooks.json` dans ce dossier.** 26 formules, chacune avec un modèle, un
   exemple rempli, la version à l'écran, à quoi elle sert et comment on la rate.
   Quatre d'entre elles sont là parce qu'elles revenaient sans cesse dans de
   vrais hooks, pas pour compléter une liste.
3. **Si l'idée est mince, ne la gonfle pas.** Pose une seule question groupée :
   qu'est-ce qui s'est passé, pour qui, et combien ça a coûté ou rapporté. Une
   vidéo a besoin d'une chose précise et vraie. Obtiens-la avant d'écrire.
4. **Si `~/.claude/reels-tiktok/veille.md` existe, lis-le.** `/rt-veille` écrit
   ce fichier : ce sont les preuves de l'utilisateur sur les formules qui
   marchent dans sa niche en ce moment. Elles priment sur les valeurs par défaut
   de ce fichier.
5. **Fixe la plateforme et le mode.** Demande ou déduis :
   - plateforme : Instagram, TikTok, ou les deux ;
   - mode : **face caméra**, ou **sans visage** (avec voix off IA, ou sans voix
     du tout, juste texte à l'écran et musique).
   Si `~/.claude/reels-tiktok/voix.md` existe, l'utilisateur a déjà une voix off
   réglée : propose le mode sans visage avec voix off par défaut et récupère la
   vitesse mesurée pour `minutage.py`.

## La forme

Une vidéo courte se joue dans les deux premières secondes et se garde dans les
cinq suivantes. C'est vrai sur les deux plateformes.

```
0:00 - 0:02   HOOK        l'affirmation. Ligne parlée et ligne à l'écran, écrites
                          séparément. Du mouvement dès la première image, pas un
                          visage figé ni un fond uni.
0:02 - 0:07   L'ENJEU     pourquoi ça compte pour la personne qui regarde. Une ligne.
0:07 - ...    LE CORPS    une idée par temps, et l'image change à chaque temps.
3 DERN. s     LE PAYOFF   livre ce que le hook a promis, puis la seule demande.
DERN. LIGNE   LA BOUCLE   reprends un mot du hook pour que la relecture s'enchaîne.
```

**Durée.** 15 à 45 secondes, c'est la plage de travail sur les deux. Sur TikTok,
ce qui marche le mieux en général tourne autour de 20 à 35 secondes. TikTok
accepte 10 minutes en appli et Instagram 20 minutes pour un Reel : presque
personne ne devrait s'en servir. Sous 7 secondes, les boucles gonflent le
compteur et rien d'autre.

## Le mode sans visage

Beaucoup de comptes ne montrent jamais personne : motion design, captures
d'écran, plans de coupe, texte à l'écran, musique, et de plus en plus une voix
off de synthèse. La forme ne change pas. Ce qui change :

- **Avec voix off IA** : le script parlé devient le texte de la voix off. Écris-le
  pour qu'une machine le lise bien : chiffres écrits comme ils se disent
  ("deux heures", pas "2h"), pas d'abréviations, pas de sigles qu'elle va
  épeler de travers, la ponctuation pour placer les pauses. Le réglage de la
  voix et la génération se font avec `/rt-voix`, pas ici. Pour le minutage,
  passe la vitesse mesurée dans `voix.md` à `--mpm`, sinon le défaut de 160
  mots par minute (débit français parlé) faussera tout.
- **Sans voix off** : le texte à l'écran porte tout. Il n'y a plus de "script
  parlé" à écrire, seulement les cartons. Chaque carton doit tenir seul, et il
  en faut plus. Laisse chaque carton assez longtemps pour être lu (compte au
  moins 1,5 seconde, plus pour les cartons de plus de cinq mots). La musique
  donne le rythme des coupes, pas le sens.
  Pour minuter les cartons, écris-en un par ligne et lance
  `python3 minutage.py cartons.txt --lecture --cible 15` : chaque ligne est
  comptée comme un texte à lire (environ 3 mots par seconde, 1,5 s minimum).
- **Le mouvement dès la première image** reste obligatoire : un texte qui
  s'anime, un curseur qui bouge, une capture qui défile. Un fond uni avec une
  phrase posée dessus, c'est un balayage assuré.
- **La musique.** Un compte entreprise a souvent un catalogue restreint, en
  général la bibliothèque musicale commerciale (sur TikTok comme sur
  Instagram). Vérifie que le son prévu est utilisable avant d'écrire autour.
- **Les mots-clés sur TikTok.** TikTok transcrit l'audio et lit le texte à
  l'écran pour sa recherche. Avec voix off, fais dire le mot-clé. Sans voix,
  affiche-le sur un carton.

## La boucle de travail

**1. Choisis trois hooks, pas un.** Passe l'idée dans `hooks.json`, choisis trois
formules qui collent vraiment, et écris pour chacune la ligne parlée (ou de voix
off) et la ligne à l'écran. Trois formules différentes, pas trois réécritures de
la même.

**2. Note-les.** Mets les trois lignes parlées dans un fichier, une par ligne, et
lance `score_hook.py`. En mode sans voix, note les lignes à l'écran. Montre le
classement à l'utilisateur. Si le premier est sous 50, tu n'as pas encore le
hook, et aucune retouche ne réglera ça.

**3. Écris le script** sur le hook gagnant. Langue parlée, comme l'utilisateur
parle vraiment. Phrases courtes. Aucune phrase qu'il faudrait répéter avant de
la dire. En mode voix off, même règle : une voix IA qui lit une phrase écrite,
ça s'entend encore plus.

**4. Minute-le.** Lance `minutage.py script.txt --cible {durée}` (avec `--mpm`
si voix off IA). Corrige chaque alerte : un hook qui dépasse 3 secondes, un temps
de plus de 4 secondes, une suite de temps sans rien de concret, pas de boucle.
Relance jusqu'à ce que ce soit propre.

**5. Passe-le à `/rt-humain`** avant de le montrer. Une ligne qui sonne écrit se
repère dès qu'on la dit à voix haute.

**6. Affiche le bloc.** Le script dans un bloc de code, le texte à l'écran dans
une liste séparée avec les minutages, puis :

```
VIDÉO PRÊTE
plateforme : TikTok + Instagram (même export, publié nativement sur chaque appli)
mode :       sans visage, motion design + voix off IA
hook :       #5 Le temps écrasé, score 79 FORT
durée :      27,6 s sur 9 temps à 175 mpm (vitesse de voix.md)
à l'écran :  7 cartons
humain :     4 tics retirés, score humain 81 OK
voix off :   lance /rt-voix
légende :    lance /rt-legende ensuite

Réponds "oui" pour l'ajouter au journal, ou dis-moi quoi changer.
```

En mode face caméra, la ligne `voix off` disparaît. En mode sans voix, elle
devient `voix off : aucune, le texte à l'écran porte tout`.

**7. Ne publie jamais.** Ce skill produit un script. L'utilisateur tourne (ou
monte) et publie. Sur "oui", ajoute une ligne à `~/.claude/reels-tiktok/journal.md`
avec la date, la plateforme, le mode, la formule de hook utilisée et la première
ligne, pour que `/rt-audit` ait un historique plus tard.

## Le texte à l'écran est un script à part

Écris-le séparément, à chaque fois. Il est lu avant d'être entendu.

- **Six mots maximum par carton.** Il est lu à bout de bras par quelqu'un qui
  n'écoute pas encore. En mode sans voix, le carton du hook reste à six mots ;
  les cartons du corps peuvent aller un peu au-delà s'ils restent assez
  longtemps à l'écran.
- **Le carton du hook est là dès la première image**, pas après un temps de
  silence.
- **Reste dans la zone sûre.** Sur une image 1080x1920, garde le texte et les
  éléments clés entre y=230 et y=1440, laisse libres les 140 pixels de droite
  et environ 60 pixels à gauche. Cette zone couvre l'interface des deux applis :
  nom, légende et son en bas, boutons à droite.
- **Jamais le hook là où se trouve la légende.** C'est le bas de l'image, il est
  recouvert sur les deux plateformes.
- **Sous-titres incrustés pour le corps.** Beaucoup de gens regardent d'abord
  sans le son.

## Les règles qui font la différence

- **Une idée par vidéo.** Si le script en a deux, tu as deux vidéos. Dis-le.
- **Des chiffres plutôt que des adjectifs.** "4 200 €" bat "beaucoup". Si
  l'utilisateur n'a pas donné de chiffre, demande-le plutôt que d'écrire
  autour du trou.
- **Coupe l'intro.** Pas de bonjour, pas de "dans cette vidéo", pas de prénom,
  pas de logo animé. La vidéo commence à la phrase que tu dirais normalement à
  la sixième seconde.
- **Change d'image à chaque temps.** Un plan fixe pendant 8 secondes, c'est là
  que les gens partent, et `minutage.py` le signalera.
- **Une seule demande à la fin.** Commenter un mot-clé, enregistrer, ou suivre.
  Une.
- **N'invente jamais.** Pas de métriques, de clients, de chiffre d'affaires ou
  de résultats inventés au nom de l'utilisateur, même en exemple provisoire. Si
  un chiffre manque, laisse `{{ton chiffre}}` dans le script et signale-le.
- **N'écris pas un script autour d'un son tendance que l'utilisateur ne peut pas
  utiliser.** Si l'idée a besoin de sa voix (ou d'une voix off), dis-le.
- **Deux plateformes, un fichier propre.** Pour publier sur les deux, exporte le
  montage sans filigrane et publie-le nativement sur chaque appli. Jamais une
  vidéo téléchargée de TikTok avec son filigrane sur Instagram, ni l'inverse.

## Exemple

```
/rt-video on a fait passer la rédaction d'une lettre de motivation de 2 heures à 10 minutes
```

```
PLATEFORME  TikTok + Instagram  ·  MODE  sans visage, voix off IA

HOOKS  (notés)
  87  FORT     #2  L'ordre négatif  "Arrête d'écrire tes lettres de motivation en partant de zéro."
                                    à l'écran : ARRÊTE ÇA
  79  FORT     #5  Le temps écrasé  "Ta lettre de motivation, c'était deux heures. Dix minutes maintenant."
                                    à l'écran : 2 H -> 10 MIN
  47  FAIBLE   #9  Pique-le         "Pique la méthode qui sort une lettre en dix minutes."
                                    à l'écran : PIQUE ÇA

Les deux premiers sont FORT, le script ne les départage pas.
On part sur le #5 : le rapport est crédible, il se lit d'un coup d'œil à
l'écran, les chiffres viennent de toi, et la voix off dit "lettre de
motivation" dès la première seconde, donc la recherche TikTok peut la capter.
```
