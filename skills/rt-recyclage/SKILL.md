---
name: rt-recyclage
description: >-
  Transforme une source longue (vidéo YouTube, podcast, live, newsletter,
  article de blog, appel client, webinaire) en une semaine de vidéos Instagram
  et TikTok et de carrousels. À utiliser quand l'utilisateur dit "recycle ça",
  "découpe cette vidéo", "fais-en des reels", "fais-en des tiktoks", "j'ai une
  vidéo / un podcast / une transcription", "tire des posts de cet article", ou
  colle un texte long et veut le sortir sur Instagram ou TikTok.
---

# rt-recyclage

Une bonne source longue contient quatre à six publications. La plupart des gens
en sortent une et jettent le reste.

## Entrée

Une transcription, un article, une newsletter, un script, un compte rendu
d'appel, un live. Si l'utilisateur donne une URL et que la session a un outil
de transcription, utilise-le ; sinon demande-lui de coller le texte. Lis tout
avant d'extraire quoi que ce soit.

Si la source est une vidéo qui appartient à l'utilisateur, demande aussi le
fichier. Une vidéo montée avec ses vrais extraits bat une vidéo où il relit ses
propres phrases.

Demande (ou déduis) aussi :

- **La plateforme** : Instagram, TikTok, ou les deux.
- **Le format** : face caméra, ou sans visage (voix off IA via `/rt-voix`, ou
  texte à l'écran + musique). Lis `~/.claude/reels-tiktok/style.md` s'il
  existe, la réponse y est souvent.

## Extraire, pas résumer

Le résumé d'une vidéo n'est pas une vidéo. Personne ne veut le résumé. Parcours
la source et sors ce qui tient debout tout seul :

| à sortir | ce que c'est |
| --- | --- |
| **Affirmations** | chaque phrase qui lancerait un débat |
| **Chiffres** | chaque montant, coût, durée, pourcentage |
| **Histoires** | chaque moment avec une personne, une scène et un prix payé |
| **Mécanismes** | chaque "en fait, ça marche comme ça..." |
| **Erreurs** | chaque aveu de quelque chose qui a mal tourné |
| **Phrases** | chaque phrase déjà citable telle quelle |

Liste ce que tu as trouvé, avec les comptes, avant d'écrire quoi que ce soit.
Si la source donne moins de quatre éléments, elle est maigre, et quatre
publications tirées d'elle seront maigres aussi. Dis-le.

## Puis choisis le format pour chaque extrait

Tout ne devient pas une vidéo.

- **Affirmation, erreur, histoire** : une vidéo (Reel ou TikTok). Il leur faut
  une voix et un visage, ou à défaut une voix off et des images qui portent
  l'émotion.
- **Mécanisme, liste numérotée** : un carrousel (carrousel Instagram ou mode
  photo TikTok). Il faut pouvoir les relire.
- **Une phrase citable** : un écran de story, pas une publication.

## Puis construis la semaine

Chaque extrait devient une publication, et chaque publication tient
complètement seule. Le spectateur n'a pas vu la source et ne la verra jamais.
N'écris jamais "comme je le disais dans ma dernière vidéo". La publication,
c'est la chose.

Attribue à chacune une formule de hook tirée de `rt-video/hooks.json` et varie.
Cinq publications d'une même source avec la même forme de hook, ça sent l'usine
à contenu, parce que c'en est une.

Si la source est une vidéo de l'utilisateur, **utilise les vrais extraits**.
Le passage où il a dit la chose, avec la vraie réaction dedans, bat un
re-tournage à chaque fois. Coupe sur la phrase, pas sur la respiration. Donne
le minutage exact de chaque extrait (début et fin) pour qu'il le retrouve dans
son logiciel de montage.

En mode sans visage, l'extrait audio peut quand même servir : sa vraie voix
sur du motion design ou du texte à l'écran. Sinon, réécris la phrase pour une
voix off IA (`/rt-voix`) et garde le sens exact, pas une paraphrase molle.

Ordonne la semaine pour que l'affirmation la plus forte sorte en premier,
l'histoire en milieu de semaine, et le mécanisme en dernier, quand ceux qui ont
aimé les premières l'attendent.

## Une vidéo, deux plateformes

Une même vidéo peut sortir sur Instagram et sur TikTok. Trois règles :

- **Exporte le fichier propre** depuis ton montage et publie-le nativement sur
  chaque appli. Jamais une vidéo téléchargée de TikTok avec le filigrane sur
  Instagram, ni l'inverse.
- **Garde la zone sûre commune** : sur 1080x1920, texte et éléments clés entre
  y=230 et y=1440, et les 140 px de droite libres (environ 60 px à gauche).
  Ça couvre l'interface des deux applis.
- **Adapte la légende à chacune.** Instagram : environ 125 caractères visibles
  avant "plus". TikTok : environ 80 à 100. Sur TikTok, le mot-clé de recherche
  doit être dans la légende, le texte à l'écran et ce qui est dit. 5 hashtags
  max des deux côtés. Passe chaque légende par `/rt-legende` avec la bonne
  `--plateforme`.

Les carrousels ne se recyclent pas tels quels : 1080x1350 (4:5) sur Instagram,
1080x1920 (9:16) recommandé en mode photo TikTok. Prévois deux exports.

## Sortie

```
SOURCE  "Pourquoi on a arrêté les appels découverte" (podcast 42 min, 8 900 mots)
PLATEFORMES  Instagram + TikTok   FORMAT  face caméra (extraits du podcast)

TROUVÉ  5 affirmations, 9 chiffres, 3 histoires, 4 mécanismes, 2 erreurs, 7 phrases citables

SEMAINE
MAR  VIDÉO      #2  L'ordre négatif   Arrête les appels découverte
                                      extrait 14:20 à 14:48, il rit à la fin
                                      IG + TikTok, même fichier, deux légendes
MER  CARROUSEL  légende = contenu     Le formulaire en 4 questions qui a remplacé l'appel
                                      export 4:5 pour IG, 9:16 pour TikTok
VEN  VIDÉO      #21 En pleine phrase  "...et il a demandé un remboursement neuf jours après"
                                      extrait 27:05 à 27:31
DIM  VIDÉO      #5  Le temps écrasé   Six heures par semaine récupérées, un lien supprimé
                                      extrait 33:40 à 34:12

Dis "écris mardi" et je le rédige.
```

Puis rédige à la demande, une à la fois, chacune via `/rt-video` et
`/rt-humain`. Ne balance pas quatre scripts finis d'un coup. Ils sonneront tous
pareil et l'utilisateur n'en tournera aucun.
