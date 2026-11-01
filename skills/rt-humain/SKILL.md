---
name: rt-humain
description: >-
  Retire l'empreinte machine d'un brouillon (tirets longs, tics d'écriture
  IA, caractères invisibles) et le note avec cinq contrôles avant qu'il
  sorte. À utiliser dès qu'un texte doit sonner humain, quand l'utilisateur
  dit "humanise", "ça fait IA ?", "ça sonne ChatGPT", "enlève les tirets",
  "rends ça naturel", "ça fait robot", et avant de montrer toute légende,
  script, texte à l'écran, commentaire, réponse ou DM pour Instagram ou
  TikTok.
---

# rt-humain

Deux outils vivent dans ce dossier et ils tournent vraiment. Utilise-les. Ne
juge pas à l'œil.

```bash
python3 humaniser.py brouillon.txt -o propre.txt --rapport   # nettoie, montre ce qui a changé
python3 detecter.py brouillon.txt                           # note, cinq contrôles
python3 detecter.py avant.txt apres.txt                     # prouve l'écart
```

Les deux lisent `lexique.json` : des mots et expressions toutes faites avec
leur remplacement en français simple, les classes de caractères invisibles,
les substitutions typographiques et les tics de structure. Le dernier bloc de
chaque liste est propre à Reels et TikTok, le vocabulaire qu'on ne trouve que
dans les légendes et les voix off. Le fichier est fait pour être modifié. Si
l'utilisateur emploie toujours un mot que le lexique supprime, retire-le du
fichier.

## Pourquoi ça compte plus sur Reels et TikTok qu'il n'y paraît

Les légendes sont courtes et les scripts sont dits à voix haute. Une phrase
qui sent l'écrit dans une légende de 600 caractères pèse plus lourd que la
même phrase dans un long article, et une voix off que personne ne dirait
naturellement s'entend dès la première prise. Le signal n'est pas un
détecteur qui repère la vidéo. Le signal, c'est quelqu'un qui scrolle devant
un texte qui sonne comme une marque, ou un créateur qui trébuche sur son
propre script.

## Ce qui est corrigé automatiquement

**1. Les caractères invisibles.** Espaces et liants de largeur nulle,
liants de mots, traits d'union conditionnels, marques d'ordre d'octet,
caractères d'étiquette Unicode, séparateurs invisibles, espaces insécables
et espaces fines. Un clavier ne produit pas ça (à part l'insécable, voir plus
bas). Ils survivent au copier-coller, ils sont invisibles dans tous les
éditeurs, et c'est la trace la plus mécanique d'un texte généré.
`humaniser.py` les supprime tous (les espaces insécables et fines deviennent
des espaces simples), y compris tout caractère de format Unicode restant qu'il
ne connaît pas par son nom.

**2. La typographie.** Tiret long vers virgule, tiret moyen vers trait
d'union, apostrophes et guillemets courbes vers droits, guillemets « » vers
" ", points de suspension vers trois points, puce vers trait d'union. Le
passage sur le tiret long est celui qui compte : il remplace le tiret par une
virgule puis nettoie la double ponctuation et les points orphelins qui
restent.

**Cas français à connaître.** En français, l'espace insécable avant ; ! ? :
est la norme typographique, pas une trace d'IA. `humaniser.py` la remplace
par une espace simple pour que le texte passe partout (certaines applis
affichent mal l'insécable), mais ne la compte pas comme une faute et ne le
signale pas à l'utilisateur comme un tic machine. Même chose pour « » : ce
sont de vrais guillemets français, convertis en " " seulement parce que c'est
ce que tape un clavier de téléphone.

**3. Le lexique.** Les tics d'écriture IA en français : "il est important de
noter", "dans un monde en constante évolution", "n'hésitez pas", "plongeons
dans", "en somme", "véritable", "incontournable", "booster", "game changer",
"force est de constater", "à l'ère du numérique", et le reste de la liste.
Plus le bloc Reels/TikTok : "arrête de scroller", "dans cette vidéo",
"abonne-toi pour plus", "l'algorithme adore". Chacun est remplacé par un mot simple ou supprimé, majuscules
conservées, URL intactes.

## Ce qui n'est PAS corrigé automatiquement

Les tics de structure sont **signalés, pas réécrits**, parce que changer la
forme d'une phrase demande du jugement :

- "Ce n'est pas juste X, c'est Y" et "non seulement X mais aussi Y"
- Les triades en série de trois
- Les questions rhétoriques d'un mot sur leur ligne : "Le résultat ?"
- Le préambule vidéo : "dans cette vidéo je vais te montrer"
- Les listes à puces en emojis
- Trois mots ou plus en majuscules d'affilée
- Les murs de hashtags
- L'appât réflexe : "abonne-toi pour plus", "identifie quelqu'un qui",
  "double tape si", "like si t'es d'accord"

Cette liste, c'est ton travail. Réécris chaque ligne signalée à la main en
gardant le sens, puis relance `detecter.py`. C'est cette partie qui fait
passer la note de À REVOIR à OK, et c'est celle qu'un script ne sait pas
faire.

## Les cinq contrôles

`detecter.py` note cinq signaux de 0 à 100, plus haut veut dire plus
humain :

| contrôle | ce qu'il mesure | une machine, ça donne |
| --- | --- | --- |
| RAFALE | la variation de longueur des phrases | toutes les phrases de la même longueur |
| PRÉCISION | chiffres, noms, repères concrets pour 100 mots | des noms abstraits, aucun chiffre |
| DENSITÉ CLICHÉS | occurrences du lexique pour 100 mots | du vocabulaire tout fait |
| EMPREINTE | caractères invisibles, tirets longs, guillemets courbes pour 1 000 caractères | une typographie parfaite |
| VOIX | élisions et tournures orales ("t'as", "j'sais pas", "y'a"), personne grammaticale, tics de structure | aucune élision, des révélations mises en scène |

Le verdict pèse la moyenne à 60 % et **le contrôle le plus faible** à 40 %,
parce qu'un seul signal suffit. OK demande une note globale de 70 ou plus et
aucun contrôle sous 55. Entre 50 et 70, c'est À REVOIR. En dessous, SIGNALÉ.

## Dis-le honnêtement

Ce sont cinq heuristiques locales, calquées sur les signaux que les
détecteurs publics regardent. Elles tournent entièrement sur la machine de
l'utilisateur et rien n'est envoyé nulle part. Ce ne sont **pas** GPTZero,
Originality, Copyleaks, Winston, Compilatio ou Turnitin, elles n'appellent pas
leurs API, et elles ne peuvent pas garantir leur verdict. Corriger ce
qu'elles mesurent fait en général bouger ces chiffres, parce qu'elles
mesurent les mêmes choses de fond. C'est ça l'affirmation. N'en fais pas une
plus grosse à la place de l'utilisateur, et ne lui dis jamais que son texte
est indétectable.

## Texte destiné à une voix off IA

Si le texte va être lu par une synthèse vocale (voix off IA, voix intégrée à
TikTok, outil externe), le passage par ce skill ne suffit pas. Relis-le
ensuite avec `/rt-voix` : la synthèse prononce mal les sigles, les chiffres,
les montants en €, les anglicismes et les abréviations, et un "CV" ou un
"2 500 €" mal lu s'entend tout de suite. `/rt-humain` rend le texte naturel à
lire, `/rt-voix` le rend naturel à entendre.

## Ordre des opérations

1. `humaniser.py brouillon.txt -o propre.txt --rapport`
2. Lis les signalements de structure. Réécris ces lignes toi-même.
3. `detecter.py brouillon.txt propre.txt` pour montrer l'avant et l'après.
4. Si le verdict n'est pas OK, corrige le contrôle le plus faible indiqué
   dans la sortie et recommence. Deux tours, c'est normal. Cinq tours, c'est
   que le brouillon a été écrit à la formule, et la solution est un autre
   brouillon, pas plus de passages.
5. Si le texte part en voix off IA, passe-le à `/rt-voix`.
6. Montre à l'utilisateur le texte nettoyé et la note. Jamais la note seule.
