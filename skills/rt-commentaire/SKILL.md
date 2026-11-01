---
name: rt-commentaire
description: >-
  Écrit des commentaires sous les Reels, posts et TikTok des autres qui
  sonnent comme une personne avec un avis, pas comme un bot. À utiliser
  quand l'utilisateur colle une vidéo ou un post et veut un commentaire, dit
  "commente ça", "je mets quoi en commentaire", "réponds sous cette vidéo",
  "interagis avec ce compte", ou veut une série de commentaires pour sa
  tournée d'interactions du jour.
---

# rt-commentaire

Commenter, ce sont les vingt minutes qui rapportent le plus sur Instagram et
TikTok, et les plus faciles à rater. Un commentaire en haut d'une vidéo à
40 000 vues est vu par plus de monde que la plupart des publications du
compte lui-même, et c'est le seul endroit où un inconnu peut taper
directement vers un profil. Sur TikTok, les commentaires les plus aimés
remontent souvent en tête et y restent longtemps.

Un commentaire générique est pire que rien. Il coûte un tap qui ne mène
nulle part, et il range le compte dans la case "pod d'engagement" aux yeux de
la seule personne dont l'avis comptait : le créateur.

## Entrée

L'utilisateur colle le texte de la vidéo ou du post, ou une capture, avec le
nom du compte et la plateforme. S'il donne un lien que tu ne peux pas ouvrir,
demande-lui de coller le contenu. N'utilise pas d'outil de navigation pour
parcourir le fil, et ne publie rien.

## Les neuf types de commentaire

Choisis selon ce qu'est vraiment la publication. Ne prends jamais le type 1
par défaut.

| # | type | quand | forme |
| --- | --- | --- | --- |
| 1 | **Ajoute une donnée** | la publication avance un point que tu peux appuyer d'un chiffre | "Pareil chez nous : 40 % des..." |
| 2 | **Ajoute le cas manquant** | c'est juste mais incomplet | "Ça tient jusqu'à ce que {condition}." |
| 3 | **Désaccord respectueux** | tu penses vraiment que c'est faux | dis d'abord sur quoi tu es d'accord, puis où ça bifurque |
| 4 | **Prolonge une ligne** | une ligne en particulier est la bonne | cite-la, construis dessus |
| 5 | **Pose la vraie question** | la publication a sauté la partie difficile | une question, précise |
| 6 | **Le vécu** | tu as fait ce qu'il décrit | ce qui s'est passé, deux phrases |
| 7 | **La correction** | il y a une erreur factuelle | aie raison, sois bref, sois aimable, sois sûr |
| 8 | **Le recadrage** | bons faits, mauvais cadre | "Autre façon de le voir :" |
| 9 | **La phrase courte** | la publication n'a besoin de rien, tu veux être présent | moins de 10 mots, drôle ou vrai |

## Règles

- **Une à trois phrases.** Les commentaires se lisent dans une colonne
  étroite sous une vidéo. Un paragraphe se replie derrière "plus" et personne
  ne tape dessus.
- **Longueur maximale.** TikTok : 150 caractères, c'est une limite dure de
  l'appli. Compte-les. Instagram : la limite est bien plus large, mais la
  règle des trois phrases s'applique quand même. Si le commentaire doit
  servir sur les deux, écris-le pour TikTok.
- **N'ouvre jamais par** "Super post", "J'adore", "Tellement vrai", "Ça 👏",
  "J'avais besoin de ça aujourd'hui", "Trop bien", ou le prénom du créateur
  avec un point d'exclamation. Tout ça est invisible.
- **Pas de commentaire fait que d'emojis**, et pas d'emoji en premier
  caractère.
- **Ne résume jamais la vidéo.** Tous ceux qui la regardent viennent de la
  voir.
- **Une seule idée.** Un commentaire à deux idées ressemble à une prise
  d'otage du fil.
- **Dis la chose précise.** Si le commentaire pourrait aller sous n'importe
  quelle vidéo sur le sujet, ce n'est pas un commentaire, c'est du bruit.
- **Jamais de vente.** Ni l'offre, ni le lien, ni "va voir mon profil". C'est
  le moyen le plus rapide de se faire bloquer par la personne qu'on voulait
  justement toucher.
- **Tôt, ça compte plus ici que partout ailleurs.** Un commentaire posté dans
  la première heure sur une vidéo qui décolle est emporté avec elle.

## Sortie

Donne **deux options de types différents**, étiquetées, plus une ligne sur
celle que tu posterais et pourquoi. Passe les deux par `/rt-humain` avant :
les commentaires sont courts, donc un tiret long ou une formule toute faite
s'y entend plus que dans une légende. Pour TikTok, indique le nombre de
caractères.

```
OPTIONS DE COMMENTAIRE  (sous le TikTok de @compte sur les relances après entretien)

[6 · Vécu]  129 car.
J'ai relancé à J+5 au lieu d'attendre, poste décroché. La recruteuse m'a dit
que j'étais le seul des 4 finalistes à l'avoir fait.

[3 · Désaccord respectueux]  125 car.
D'accord sur le délai. Par contre le mail de relance de 10 lignes, non : deux
phrases, une question, c'est tout ce qu'on lit.

Poste le premier. Il a un chiffre et un résultat, et il ne contredit personne.
```

## Mode série

Pour une tournée d'interactions, demande les 5 à 10 publications en texte
collé dans un seul message, rends un commentaire par publication dans un seul
bloc, avec la plateforme et le nombre de caractères pour TikTok, et tiens une
note dans `~/.claude/reels-tiktok/journal.md` des comptes déjà commentés
cette semaine. Commenter les trois mêmes comptes tous les jours se voit, et
ça ressemble exactement à ce que c'est.

## Jamais

Ne publie jamais automatiquement, n'automatise pas les commentaires, et
n'utilise pas d'outil de navigation pour publier à la place de
l'utilisateur. L'engagement automatisé enfreint les conditions d'utilisation
d'Instagram et de TikTok, et fait bloquer les comptes. Ce skill écrit le
commentaire. L'utilisateur le poste.
