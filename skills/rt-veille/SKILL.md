---
name: rt-veille
description: >-
  Va chercher les vidéos qui marchent vraiment en ce moment dans la niche de
  l'utilisateur, sur Instagram et TikTok, les classe selon l'écart avec la
  médiane de leur propre compte, nomme la formule de hook de chacune et en fait
  un fichier de veille dont il peut tirer ses prochaines vidéos. À utiliser quand
  l'utilisateur dit "trouve-moi des vidéos virales", "qu'est-ce qui marche en ce
  moment", "qu'est-ce qui se poste dans ma niche", "analyse ce compte",
  "fais-moi une veille", "pourquoi ce tiktok cartonne", "tendances TikTok", ou
  demande quoi faire ensuite sans aucune preuve pour répondre.
---

# rt-veille

Le skill de recherche. Tout le reste du pack écrit ; celui-ci va regarder. Lance-le
une fois par mois, pas tous les jours. Une formule tient une saison.

Un outil est dans ce dossier et il tourne :

```bash
python3 veille.py capture.tsv --out ~/.claude/reels-tiktok/veille.md
```

## La seule idée qui rend ce travail utile

**Les vues brutes ne prouvent rien.** Un compte à deux millions d'abonnés qui
fait 400 000 vues a eu un mardi calme. Un compte à quatre mille abonnés qui fait
400 000 vues a trouvé quelque chose, et ce quelque chose se copie.

Donc tout ici se classe sur **le multiple d'écart** : les vues divisées par la
médiane récente de ce même compte. Au-dessus de 3x, c'est un signal. Sous 1,5x,
c'est la journée normale du compte et ça n'apprend rien, même si le chiffre a
l'air énorme.

Prends des comptes **à 10x maximum de la taille de l'utilisateur**. Une formule
qui marche à 2 millions d'abonnés marche souvent parce qu'elle est à 2 millions
d'abonnés.

Sur TikTok, c'est encore plus vrai : le fil Pour Toi pousse des vidéos de petits
comptes à des inconnus, donc les gros écarts y sont fréquents et très parlants.

## Étape 1 : choisir les comptes

Demande à l'utilisateur 6 à 12 comptes, ou propose-les et fais valider. Mélange
les deux plateformes si l'utilisateur publie sur les deux.

- **4 directs** : même niche, même offre, un peu devant.
- **4 voisins** : autre niche, même public. C'est là qu'on emprunte des formats
  avant que la niche les ait.
- **2 à 4 surdimensionnés** : comptes bien plus gros, pour le format seulement,
  jamais pour le rythme de publication ni le ton.

Demande-lui aussi d'ouvrir ses **Enregistrés** sur Instagram et ses **Favoris**
sur TikTok. C'est le corpus le plus rapide et le plus pertinent qui existe, et
il est déjà filtré par son goût.

## Étape 2 : aller regarder

Utilise l'outil de navigation que cette session a vraiment : un navigateur
intégré, une extension connectée au Chrome de l'utilisateur, ou un outil de
contrôle de l'ordinateur. Il n'y a pas d'API pour ça et il n'en faut pas : le
volume est assez petit pour être lu.

**Règles non négociables :**

- **Ne te connecte jamais à Instagram ou TikTok à la place de l'utilisateur et
  ne demande jamais de mot de passe.** Si une page demande une connexion, c'est
  l'utilisateur qui est déjà connecté. Pilote son navigateur en sa présence, ou
  demande-lui de coller les infos.
- **C'est de la lecture, pas du scraping.** Dix comptes, une douzaine de vidéos
  chacun, à vitesse humaine. La collecte automatisée en volume viole les CGU
  d'Instagram et de TikTok et fait bloquer les comptes. Ne construis pas de
  robot d'exploration, n'utilise pas de service de scraping, et ne fais pas
  tourner ça en tâche de fond.
- **Copie la formule, jamais la vidéo.** La forme du hook, la structure, la
  durée, le rythme des coupes. Pas leur script, pas leur voix, pas leur montage.
  Attribue chaque ligne du fichier de veille au compte d'où elle vient.

**Ce qu'il faut relever par vidéo**, avec les mots du créateur :

| champ | notes |
| --- | --- |
| compte | le pseudo |
| plateforme | `instagram`, `tiktok` ou `youtube` |
| abonnés | sur le profil |
| médiane | regarde les 12 dernières vidéos et prends le nombre de vues du milieu |
| vues | cette vidéo |
| hook | la première ligne, dite ou à l'écran, mot pour mot, fautes comprises |
| à l'écran | le premier carton, s'il est différent |
| durée | en secondes |
| demande | ce qu'ils demandent à la fin |

La médiane est le champ qui compte. Sans elle, on revient à classer par nombre
d'abonnés, exactement ce que ce skill doit empêcher.

**Sur TikTok, la médiane est facile.** La grille du profil affiche le nombre de
vues sous chaque vidéo. Douze vignettes, tu lis les chiffres, tu prends celui
du milieu. Ignore les vidéos épinglées en haut : elles sont là parce qu'elles
ont cartonné, elles faussent la médiane.

**Sur Instagram**, l'onglet Reels du profil affiche aussi les vues, mais les
Reels épinglés et les collaborations brouillent la lecture. Même règle : sors
les épinglés.

**Le Creative Center de TikTok** (le centre créatif de TikTok for Business) est
public et donne les publicités qui performent, les hashtags, les sons et les
créateurs en tendance, filtrables par pays et par secteur. Sers-t'en pour deux
choses : voir quels sons montent en France (et s'ils sont dans la bibliothèque
commerciale si le compte est pro), et voir quels hooks les annonceurs de la
niche paient pour diffuser. Une pub qui tourne depuis des semaines, c'est
souvent un hook qui convertit. Ces lignes n'ont pas de médiane de compte : note-les à part,
elles ne passent pas dans `veille.py`.

**Quand les plateformes ne montrent pas assez :** la même grammaire de hook
tourne sur YouTube Shorts, où les vues et les transcriptions sont publiques et
sans connexion. C'est un second corpus légitime, et le hook parlé y est plus
facile à récupérer :

```bash
# nombre de vues des shorts d'une chaîne
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@PSEUDO/shorts" > chaine.json

# la première ligne dite d'un short, depuis ses sous-titres auto
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "fr.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=ID_VIDEO"
```

Prends tous les mots des sous-titres avec un horodatage sous 3,0 secondes. C'est
le hook tel qu'il est dit, pas tel qu'il est écrit.

## Étape 3 : classer

Remplis un fichier séparé par des tabulations, avec une ligne d'en-tête, et lance
le script :

```
compte	plateforme	abonnes	mediane	vues	hook
@quelquun	tiktok	48000	11000	412000	personne te dit que tes 30 premières vidéos sont censées faire un flop
```

```bash
python3 veille.py capture.tsv --out ~/.claude/reels-tiktok/veille.md
```

Il calcule le multiple d'écart, nomme la formule de hook parmi les 26 formules
dont `/rt-video` se sert, note chaque hook avec `score_hook.py`, et affiche ce
qui sépare le tiers du haut du tiers du bas.

## Étape 4 : dire ce que ça veut dire, prudemment

Rapporte trois choses, pas plus :

1. **Quelles formules sur-représentées** dans le tiers du haut, avec les
   comptes. Deux formules qui reviennent quatre fois chacune sur six comptes,
   c'est un résultat. Une qui revient deux fois, non.
2. **Ce que le tiers du haut a en commun structurellement** et que le tiers du
   bas n'a pas : longueur du hook, payoff visuel ou non, première image qui
   bouge ou non, place de la demande. Si les deux plateformes sont dans
   l'échantillon, dis si l'écart tient sur chacune ou seulement sur une.
3. **Les lignes non classées.** Chaque hook que le classifieur n'a pas su nommer
   est soit du bruit, soit une formule qui n'est pas encore dans `hooks.json`.
   Lis-les à la main. C'est la colonne la plus précieuse de la sortie, et c'est
   pour ça que le script en affiche le nombre.

Puis donne la taille de l'échantillon et le niveau de confiance en mots simples.
Quarante vidéos sur six comptes soutiennent une affirmation. Douze, non, et le
dire, c'est la différence entre de la recherche et un horoscope.

## Étape 5 : en faire quelque chose à tourner

Pour les trois formules du haut, écris **la version de l'utilisateur** : son
histoire, son chiffre, dans la forme qui marche. Passe chacune à `/rt-video`
avec le numéro de formule déjà choisi.

Ne rends jamais "fais une vidéo comme celle-là". Rends une ligne de hook qu'il
pourrait dire (ou faire dire à sa voix off) demain.

## Sortie

```
VEILLE  ·  38 vidéos  ·  7 comptes (4 TikTok, 3 Instagram)  ·  base : médiane du compte

ÉCARTS (au-dessus de 3x)
  38,4x  hook 86  #3  Personne ne te dit   @compte_a  tiktok     412 000  (médiane 10 700)
  11,2x  hook 79  #9  Pique-le             @compte_c  instagram  180 000  (médiane 16 100)
  ...

CE QUI SUR-PERFORME
  #3 Personne ne te dit   x5 dans le tiers du haut, 0 en bas
  #2 L'ordre négatif      x4
  longueur médiane du hook   8 mots en haut, 19 en bas
  l'écart tient sur TikTok, trop peu de lignes Instagram pour conclure

NON CLASSÉES (6)
  Deux ont la même forme et elle n'est pas dans hooks.json : un hook qui
  s'ouvre sur le commentaire de quelqu'un lu à voix haute. À ajouter.

CREATIVE CENTER (à part, sans médiane)
  2 pubs de la niche tournent depuis plus de 3 semaines, toutes deux en #5

TA VERSION
  #3  "Personne te dit que tes 20 premières candidatures sont censées échouer."
  ...
```

Écris le fichier de veille dans `~/.claude/reels-tiktok/veille.md`. `/rt-video`
et `/rt-planning` le lisent tous les deux, et c'est tout l'intérêt : après un
premier passage, le reste du pack travaille à partir des preuves de
l'utilisateur au lieu des valeurs par défaut.

Ce skill ne publie rien, ne suit personne, ne like rien et n'envoie aucun
message. Il lit.
