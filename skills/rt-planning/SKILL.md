---
name: rt-planning
description: >-
  Construit la semaine sur Instagram et TikTok : quoi publier, quel format,
  quand, sur quelle plateforme, et avec qui interagir. À utiliser quand
  l'utilisateur dit "planifie ma semaine", "je publie quoi", "calendrier de
  contenu", "planning de la semaine", "j'ai rien à poster", "je sais pas
  quoi faire comme vidéo", ou veut un rythme de publication et une liste de
  comptes avec qui interagir.
---

# rt-planning

La salle de contrôle. Tous les autres skills du pack exécutent ; celui-ci
décide de ce qui s'exécute. Lance-le une fois par semaine, le même jour.

## Entrée

Si `~/.claude/reels-tiktok/style.md`, `veille.md` et `journal.md` existent,
lis-les. La veille, c'est la preuve que l'utilisateur a récoltée lui-même avec
`/rt-veille` sur les formules qui marchent dans sa niche en ce moment, et elle
passe avant tout ce qui est écrit ici. Le journal empêche le planning de
reprendre un thème des quinze derniers jours.

S'ils n'existent pas, demande cinq choses et note-les :

1. Ce que l'utilisateur vend, et à qui.
2. Les trois ou quatre thèmes pour lesquels il veut être reconnu.
3. Ce qui s'est vraiment passé cette semaine : un appel client, un chiffre,
   une erreur, un truc construit, un désaccord. C'est de là que viennent les
   vidéos.
4. Dix comptes auprès desquels être visible.
5. La plateforme : Instagram, TikTok ou les deux, et le mode de tournage :
   face caméra, ou sans visage (motion design, texte à l'écran, musique, voix
   off IA). Le mode change ce qui est faisable dans la semaine.

## Quoi publier

**Instagram : quatre à cinq publications par semaine, dont au moins trois
Reels.** Les Reels sont le seul format d'Instagram qui touche de façon fiable
des gens qui ne suivent pas le compte. Les carrousels vont en profondeur avec
ceux qui suivent déjà. Les stories sont quotidiennes et se planifient à part.

**TikTok : le rythme peut monter.** Cinq à sept vidéos par semaine, une par
jour si l'utilisateur tient la cadence sans baisser la qualité des hooks.
TikTok juge chaque vidéo sur ses premiers spectateurs, donc plus de vidéos,
c'est plus de tirages. Mais une vidéo bâclée ne compte pas comme un tirage,
elle compte comme un mauvais signal. Mieux vaut quatre bonnes que sept molles.

**Les deux : une même vidéo peut aller sur les deux plateformes**, à
condition d'exporter le fichier propre depuis le montage et de le publier
nativement sur chaque appli, avec le texte placé dans la zone sûre commune
(entre y=230 et y=1440 sur 1080x1920, 140 px libres à droite). Jamais une
vidéo téléchargée depuis TikTok avec le filigrane sur Instagram, ni
l'inverse. La légende, elle, se réécrit pour chaque plateforme avec
`/rt-legende`. En pratique : la base commune sur les deux, et deux ou trois
vidéos en plus réservées à TikTok.

Varie sur la semaine, jamais deux fois le même type d'affilée :

| type | part | rôle |
| --- | --- | --- |
| **Preuve** | 1 par semaine | quelque chose qui s'est passé, avec un chiffre. Vidéo. |
| **Leçon** | 1 à 2 par semaine | une chose que le spectateur peut faire aujourd'hui. Vidéo ou carrousel. |
| **Opinion** | 1 par semaine | une position qui peut faire perdre des abonnés. Vidéo. |
| **Récit** | 1 tous les 15 jours | une scène avec un coût. Vidéo. |
| **Offre** | 1 tous les 15 jours | ce que tu vends, dit simplement, sans t'excuser. Carrousel ou stories. |

Sur TikTok, les créneaux en plus vont en priorité aux Leçons et aux réponses
vidéo à des commentaires (voir `/rt-reponse`) : ce sont les plus rapides à
produire et elles ont déjà une demande derrière elles.

Pour chaque créneau, donne : le thème, l'angle précis tiré de ce qui s'est
passé cette semaine, le format, la plateforme, et le numéro de formule de hook
dans `rt-video/hooks.json` avec son nom. Pas un sujet, un angle. "L'IA" n'est
pas un planning. "Le devis qu'on a perdu parce que le brouillon sentait
ChatGPT" est une vidéo.

En mode sans visage, vérifie que chaque créneau tient sans tournage : texte à
l'écran, enregistrement d'écran, motion design, voix off IA. Si un angle
demande absolument un visage, dis-le et propose une autre forme.

## Quand publier

Publie quand l'audience est réveillée et pas au travail. Pour la plupart des
audiences grand public, c'est en début de soirée heure locale ; pour une
audience pro, tôt le matin ou à la pause de midi.

Mais dis-le clairement : **l'heure compte beaucoup moins que les deux
premières secondes.** Instagram et TikTok continuent de montrer une vidéo
pendant des jours si elle tient, et enterrent une vidéo bien programmée qui
ne tient pas. Si l'utilisateur optimise ses horaires avant que ses hooks
marchent, il polit la mauvaise chose, et tu dois le lui dire.

Cale les horaires sur le fuseau de l'audience, pas sur celui de
l'utilisateur, s'ils diffèrent. Les statistiques des deux applis (TikTok
Studio, statistiques Instagram) montrent quand les abonnés sont en ligne :
demande les chiffres plutôt que de deviner.

## La tournée d'interactions, qui n'est pas optionnelle

20 minutes par jour, avant de publier, pas après. Construis une liste de 10 :

- **5 visibilité** : des comptes dont l'audience intéresse l'utilisateur, où
  un bon commentaire se voit. Commenter tôt, avant que le fil fasse 200
  commentaires.
- **3 pairs** : même taille, même domaine. C'est le groupe qui rend la
  pareille.
- **2 acheteurs** : des gens qui pourraient vraiment acheter. Commenter
  pendant des semaines avant tout DM, et ne jamais vendre dans un commentaire.

Indique la plateforme de chaque compte. Passe la liste à `/rt-commentaire`.

## Sortie

```
SEMAINE DU 16 NOVEMBRE  ·  Instagram + TikTok  ·  sans visage, voix off IA

LUN  12h30  TT        VIDÉO     LEÇON    #7  Mauvaise façon, bonne façon  - l'objet de mail de candidature
MAR  18h30  IG + TT   VIDÉO     PREUVE   #5  Le temps écrasé              - 3 h de lettre de motivation à 12 min
MER  12h30  TT        VIDÉO     RÉPONSE  #16 La question mot pour mot     - "on met sa photo sur un CV ?"
             IG        stories seulement + interactions
JEU  18h00  IG        CARROUSEL LEÇON    les 5 lignes du CV qu'un recruteur lit vraiment
             TT        mode photo, même contenu en 9:16
VEN  18h30  IG + TT   VIDÉO     OPINION  #2  L'ordre négatif              - arrête d'envoyer 50 candidatures par jour
SAM  11h00  TT        VIDÉO     LEÇON    #11 La liste avec un favori      - 3 sites d'offres, dont un que personne n'utilise
DIM  18h00  IG + TT   VIDÉO     RÉCIT    #21 En pleine phrase             - le refus reçu à 23 h

STORIES IG  tous les jours, 3 à 5 écrans, boîte à questions jeudi.

INTERACTIONS  (5 visibilité / 3 pairs / 2 acheteurs)
  ...

Dis "écris mardi" et je rédige.
```

Écris le planning dans `~/.claude/reels-tiktok/planning.md` pour que les
autres skills puissent le lire.

Ce skill ne programme rien et ne publie rien. Si l'utilisateur veut
programmer à l'avance, il peut le faire lui-même avec TikTok Studio (sur
ordinateur) et Meta Business Suite pour Instagram. C'est un planning, et
c'est l'utilisateur qui le suit.
