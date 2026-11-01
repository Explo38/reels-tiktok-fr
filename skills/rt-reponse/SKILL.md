---
name: rt-reponse
description: >-
  Gère les commentaires sous les propres vidéos et posts de l'utilisateur sur
  Instagram et TikTok : trie ceux qui méritent une réponse et rédige les
  réponses. À utiliser quand l'utilisateur colle ses commentaires, dit
  "réponds à ces commentaires", "gère mes commentaires", "quelqu'un m'a dit
  X sous ma vidéo", "j'ai un rageux", "comment je réponds à ça", ou doit
  gérer un critique, un troll ou un client potentiel dans les commentaires.
---

# rt-reponse

Le fil de commentaires sous ta propre vidéo, c'est là que se décide la
portée. Chaque réponse est une interaction de plus sur la publication, les
réponses de la première heure comptent le plus, et une réponse peut
aussi être une vidéo : c'est natif sur TikTok (répondre à un commentaire par
une vidéo, le commentaire s'affiche en autocollant) et ça existe aussi sur
Instagram avec les Reels de réponse. C'est le geste le plus sous-utilisé des
deux plateformes.

Mais tous les commentaires ne se valent pas, donc ce skill trie avant
d'écrire.

## Entrée

L'utilisateur colle les commentaires, si possible avec les identifiants, et
dit de quelle plateforme ils viennent. Les captures conviennent. Ne parcours
pas le fil avec un outil de navigation.

## Trie d'abord

Range chaque commentaire dans une des six catégories et annonce les comptes :

| catégorie | ce que c'est | ce que ça reçoit |
| --- | --- | --- |
| **MOT-CLÉ** | le mot que tu as demandé de commenter | la chose promise, envoyée à la main ou par ton outil autorisé |
| **PROSPECT** | quelqu'un qui décrit le problème que tu résous | une vraie réponse en public, puis une porte |
| **FOND** | ajoute une donnée, contredit, prolonge | la réponse la plus longue du fil |
| **QUESTION** | une question que beaucoup de gens se posent | celle-là devient une vidéo, pas seulement une réponse |
| **SOUTIEN** | "🔥", "trop bien", une identification | un like, et 3 à 8 mots au plus |
| **BRUIT** | pub, spam, mauvaise foi, appât | rien, ou une ligne et basta |

Écris dans cet ordre et arrête-toi quand la valeur s'arrête.

## Le geste que la plupart des gens ratent

Si une question dans les commentaires est une question que trente autres
personnes se posent aussi, **réponds-y avec une vidéo**. TikTok et Instagram
attachent le commentaire à la nouvelle vidéo sous forme d'autocollant, la
personne qui a posé la question reçoit une notification, et une question avec
une vraie demande derrière devient une vidéo dont le hook est déjà écrit.
Repère chaque QUESTION qui s'y prête et passe-la à `/rt-video` avec la
formule #16 La question mot pour mot.

Sur TikTok, c'est le format le plus rapide à produire de toute la semaine :
pas d'idée à trouver, le hook est à l'écran. En mode sans visage, ça marche
pareil : l'autocollant du commentaire, du texte à l'écran ou une voix off IA
qui répond, et la démonstration.

## Comment répondre

- **Réponds à la vraie question.** Si quelqu'un demande comment, dis-lui
  comment, dans la réponse. Ne l'envoie pas en DM pour entendre une réponse
  qu'il aurait pu lire là.
- **Utilise son prénom une fois**, au début, sans point d'exclamation.
- **Aligne-toi sur sa longueur.** Un commentaire de quatre mots ne reçoit pas
  quatre lignes. Sur TikTok, 150 caractères maximum de toute façon.
- **À un critique :** concède d'abord la partie vraie, avec ses mots, puis
  tiens ta position. Ne supprime jamais, ne te mets jamais sur la défensive,
  ne réponds jamais deux fois dans le même fil.
- **À un troll :** rien. Une réponse, c'est de la portée, et la portée c'est
  ce qu'il est venu chercher. Masque ou supprime le commentaire s'il est
  injurieux, et utilise les filtres de mots-clés. Les deux applis ont des
  outils de modération des commentaires, et s'en servir n'est pas perdre.
- **À un prospect :** réponds complètement en public. La porte, c'est une
  phrase à la fin, et c'est une offre d'aide, pas un argumentaire. La réponse
  publique, c'est ce qui donne envie à la personne suivante de t'écrire en DM.

## Commentaires mot-clé

Si la publication demandait de commenter un mot-clé, ces commentaires sont
toute la raison d'être de la publication. Chacun, c'est quelqu'un qui a levé
la main. Réponds à chacun, puis envoie ce qui était promis. Si l'utilisateur a
une automatisation en place via les outils officiels d'Instagram ou de TikTok
ou un partenaire autorisé, dis-le et laisse-la tourner ; sinon, les réponses
sont manuelles et c'est très bien à ce volume. N'envoie jamais de DM en masse
à des gens qui n'ont pas commenté.

## Sortie

Un seul bloc, groupé par catégorie, chaque réponse prête à copier et déjà
passée par `/rt-humain` :

```
RÉPONSES  ·  TikTok  ·  84 commentaires  ·  41 MOT-CLÉ, 2 PROSPECT, 3 FOND, 2 QUESTION, 34 SOUTIEN, 2 BRUIT

MOT-CLÉ  (41)  envoie le modèle de relance. Une ligne chacun, même chaleur, pas du copier-coller.

PROSPECT
@camille.rh - "on a exactement ce souci depuis la rentrée"
> Ce qui a tout changé chez nous, c'est de couper la relance du devis et de
> l'envoyer à J+3 fixe. Je peux t'envoyer la formulation si ça t'aide.

QUESTION -> VIDÉO
@theo_lgd - "et si le recruteur répond jamais même après la relance ?"
  34 likes sur ce commentaire. C'est une vidéo, pas une réponse. Formule #16 La question mot pour mot.

BRUIT  (2)  ignorés. Leur répondre leur donne de la portée.
```

Puis la barrière : rien n'est publié tant que l'utilisateur n'a pas dit oui.
C'est lui qui colle les réponses.
