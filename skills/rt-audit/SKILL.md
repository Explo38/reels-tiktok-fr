---
name: rt-audit
description: >-
  Bilan de ce que l'utilisateur a déjà publié sur Instagram et TikTok : quelles
  vidéos ont vraiment marché, pourquoi, et quoi arrêter. À utiliser quand
  l'utilisateur colle ses statistiques Instagram ou TikTok Studio, ses
  captures d'écran ou ses anciennes publications et demande "qu'est-ce qui
  marche", "pourquoi cette vidéo a fait un bide", "lis mes stats", "analyse mon
  compte", "audit de mon contenu", "compare IG et TikTok", ou veut savoir quoi
  faire plus.
---

# rt-audit

La seule source honnête de ce qui marche pour un compte, c'est ce compte.
Toutes les règles de tous les guides Instagram et TikTok, y compris celles de
ce pack, sont des hypothèses de départ. Les 30 dernières publications de
l'utilisateur sont la preuve.

## Entrée

Demande ce que l'utilisateur a, et sur quelle plateforme (Instagram, TikTok,
ou les deux). Les captures d'écran conviennent.

**Instagram (statistiques du compte pro) :**

- Par publication : vues, comptes touchés, interactions, durée de visionnage,
  enregistrements, partages, abonnements, et la part de portée hors abonnés.
- Ou la courbe de rétention de la meilleure et de la pire vidéo récente. Cette
  seule capture vaut plus que tout le reste réuni.

**TikTok (TikTok Studio ou Analytics, par vidéo) :**

- Vues, temps de visionnage moyen, taux de vidéos regardées en entier.
- Source du trafic : Pour Toi, abonnés, recherche, profil, son.
- Partages, enregistrements, commentaires, nouveaux abonnés.
- La courbe de rétention, là aussi la capture la plus utile.

**Sinon :** juste les publications et leurs vues. Ça suffit pour une première
passe.

Lis aussi `~/.claude/reels-tiktok/journal.md` s'il existe : il note la formule
de hook et le format (face caméra ou sans visage) de chaque publication.

## Ce qu'il faut vraiment mesurer

Les vues brutes sont le chiffre le moins utile de la page, parce qu'elles
dépendent surtout du nombre de gens qui suivent déjà le compte. Calcule plutôt
ces métriques, et montre le calcul :

| métrique | calcul | ce que ça dit |
| --- | --- | --- |
| **Multiple de surperformance** | vues / médiane des vues du compte | vrai carton ou journée normale |
| **Portée hors abonnés** | % de la portée venant de non-abonnés (TikTok : part du trafic Pour Toi + recherche) | si la vidéo a voyagé |
| **Rétention à 3 s** | spectateurs encore là à 3 s / spectateurs qui ont commencé | si le hook a marché. C'est la note du hook. |
| **Temps de visionnage moyen** | direct dans les stats | si le milieu a marché |
| **Partages par portée** | partages / portée | le signal le plus fort qu'on puisse gagner. Un partage, c'est quelqu'un qui engage son nom. |
| **Abonnements par portée** | nouveaux abonnés / portée | si le profil a converti l'attention |

Sur TikTok, regarde en plus :

- **Taux de vidéos regardées en entier.** Il dit si la fin tient et si la
  boucle marche. À comparer à longueur égale : une vidéo de 12 s et une de
  50 s ne jouent pas dans la même catégorie.
- **Source du trafic.** Beaucoup de Pour Toi, la vidéo a été poussée à des
  inconnus. Beaucoup d'abonnés, elle n'est pas sortie de la bulle. Beaucoup de
  recherche, le mot-clé travaille (légende, texte à l'écran, ce qui est dit),
  et ces vidéos-là continuent de ramener des vues pendant des semaines.

Classe par multiple de surperformance et partages par portée, pas par vues.
Une vidéo à 4 000 vues et 90 partages a battu celle à 60 000 vues et 11
partages.

## Instagram et TikTok, la même vidéo

Si l'utilisateur publie sur les deux, compare la même vidéo d'une plateforme à
l'autre. C'est la comparaison la plus propre possible : même hook, même
montage, seule la plateforme change.

- Même rétention à 3 s partout : le hook est solide, l'écart de vues vient de
  la distribution.
- Rétention bien meilleure sur une seule : regarde ce qui diffère (légende,
  son, texte masqué par l'interface, premier plan coupé à l'export).
- Une plateforme qui gagne sur presque toutes les vidéos : c'est là que
  l'audience est. Dis-le, et suggère où mettre l'effort.

Calcule le multiple de surperformance contre la médiane **de chaque
plateforme**, jamais contre une médiane commune. Les deux comptes n'ont pas la
même taille.

## Puis trouve le motif

Avec le top 5 et le flop 5 côte à côte, cherche ce qui les sépare, et accepte
de conclure quelque chose que l'utilisateur n'aimera pas :

- **Rétention à 3 secondes.** Si le top et le flop diffèrent là, c'est le hook
  et rien d'autre, tout le reste est une distraction.
- **Formule de hook.** Quels numéros de `rt-video/hooks.json` sont dans le
  top 5 ?
- **Format.** Vidéo, carrousel (ou mode photo), image seule.
- **Face caméra ou sans visage.** Et en sans visage : voix off IA, sa propre
  voix, ou texte à l'écran + musique seule.
- **Durée.** Regroupe en moins de 15 s, 15 à 30 s, 30 à 60 s, plus de 60 s.
- **Thème.**
- **Réponse aux commentaires dans la première heure, ou non.**
- **Jour et heure.** À vérifier **en dernier**, et seulement si le reste ne
  montre rien. Ce n'est presque jamais la cause, et c'est là que les gens
  veulent qu'elle soit.

Énonce chaque conclusion comme une affirmation avec la preuve jointe, et dis à
quel point elle est solide. Avec 30 publications, on voit un motif. Avec 6, non,
et le dire vaut mieux qu'en inventer un.

## La distinction qui fait gagner des mois

**Une vidéo qui fait des vues et zéro abonné n'est pas une vidéo ratée, c'est
un problème de profil.** Une vidéo qui ne fait pas de vues, c'est un problème
de hook. Sépare les deux avant de recommander quoi que ce soit. Si la portée
hors abonnés est forte et les abonnements par portée faibles, arrête de
réécrire les hooks et passe à `/rt-profil`.

## Jamais

- Jamais de chiffre inventé. S'il manque une donnée, écris `{{ton chiffre}}`
  et signale-le.
- Jamais de connexion au compte de l'utilisateur, jamais de mot de passe. Il
  colle ses stats, tu les lis.

## Sortie

```
AUDIT  ·  TikTok  ·  31 vidéos  ·  12 juin - 5 sept.  ·  médiane 4 100 vues

TOP 5 PAR MULTIPLE DE SURPERFORMANCE
  18,2x  #3  Personne ne te dit   74 600 vues  62 % hors abonnés  3s 71 %  vue entière 38 %  128 partages
   6,4x  #1  L'aveu chiffré       26 300 vues  48 % hors abonnés  3s 64 %  vue entière 31 %   71 partages
  ...

FLOP 5
   0,3x  #11 La liste avec un favori  1 200 vues  9 % hors abonnés  3s 31 %  vue entière 6 %  2 partages
  ...

MÊME VIDÉO, DEUX PLATEFORMES (8 vidéos publiées des deux côtés)
  TikTok gagne 6 fois sur 8 en multiple. Rétention à 3 s quasi identique (écart moyen 3 points).
  Le hook n'est pas en cause : c'est la distribution.

CE QUE DISENT LES DONNÉES
1. La rétention à 3 secondes explique tout. Top 5 : 66 % en moyenne, flop 5 : 33 %.
   Tout ce qui t'inquiète d'autre dépend des deux premières secondes.
2. Les vidéos où c'est toi qui as l'air bête : 8,1x en moyenne contre 0,9x pour le reste.
   n=5. Le signal le plus fort ici, et de loin.
3. Les listes d'outils font des vues et rien d'autre. Forte portée, zéro partage,
   zéro abonné. Trois de tes cinq flops.
4. 41 % du trafic de tes trois meilleures vient de la recherche. Le mot-clé était
   dit à voix haute dans les trois. À garder.
5. Le jour de la semaine ne montre rien. Mardi et vendredi sont dans le bruit.
   Arrête d'optimiser ça.

STOP : les listes d'outils.
PLUS : celles avec un prix que tu as payé et un chiffre dessus.
```

Puis passe les conclusions à `/rt-planning`, pour que la semaine suivante soit
construite sur les preuves de l'utilisateur plutôt que sur des réglages par
défaut, et à `/rt-veille`, pour que le fichier de veille soit filtré sur les
formules qui marchent pour ce compte précis.
