---
name: rt-profil
description: >-
  Note un profil Instagram, TikTok ou les deux sur 100 avec une grille de 12
  critères, puis réécrit ce qui perd des points : champ nom, bio, lien, temps
  forts ou playlists, les trois épingles, la grille. À utiliser quand
  l'utilisateur dit "optimise mon profil", "corrige ma bio", "note mon
  Insta", "note mon TikTok", "pourquoi personne ne s'abonne", "ma bio est
  nulle", ou colle son profil en demandant ce que ça donne.
---

# rt-profil

Presque tout le monde optimise la mauvaise chose ici. Le profil n'est pas une
vitrine qu'on parcourt. C'est un **écran de décision**, atteint depuis une
seule vidéo, et il a environ trois secondes pour répondre à une question : il
y a d'autres vidéos comme ça ici, et c'est pour moi ?

C'est vrai sur Instagram et encore plus sur TikTok, où beaucoup de visites
de profil viennent du fil Pour Toi, d'une personne qui ne connaissait pas le
compte dix secondes avant.

## Entrée

Demande d'abord la plateforme : Instagram, TikTok ou les deux. Si c'est les
deux, note chaque profil séparément, ils ne perdent pas des points aux mêmes
endroits.

Demande à l'utilisateur de coller ou de faire une capture de : le champ nom,
l'identifiant, la bio, la cible du lien, les noms des temps forts (Instagram)
ou des playlists (TikTok), ce qui est épinglé, et les neuf premières
couvertures de la grille. Une capture du haut du profil plus les deux
premières rangées de la grille suffit pour un premier passage.

Ne te connecte jamais au compte à sa place, ne demande aucun mot de passe.

## Note-le

Lis `grille.json` dans ce dossier. Douze critères, 100 points, chacun avec ce
que vaut la note pleine et la façon dont il échoue d'habitude, et la valeur
Instagram ou TikTok quand elles diffèrent. Note chaque critère, montre le
tableau, donne le total. Sois honnête. La plupart des profils font entre 30 et
50 au premier passage, et une note généreuse ne sert à rien.

```
NOTE PROFIL  TikTok @lea.cv  38/100

  champ nom         2/12   prénom seul, aucun mot que quelqu'un cherche
  bio ligne 1       3/12   trois noms communs et un emoji café
  épingles          0/10   rien d'épinglé
  playlists         2/8    "Vidéos", "Divers", une playlist vide
  grille lisible    4/8    six couvertures sur neuf sans texte
  ...
```

## Puis réécris, dans cet ordre

Corrige par ordre de points perdus. Ne réécris pas tout d'un coup :
l'utilisateur doit aller changer chaque champ à la main.

**1. Le champ nom (30 caractères).** La ligne en gras, pas l'identifiant.
C'est le champ que la recherche Instagram et la recherche TikTok comparent à
ce que les gens tapent, et la plupart des comptes y mettent un prénom et rien
d'autre. Format qui marche : `{Prénom} | {ce que tu fais, en mots cherchés}`.
Donne trois options.

**2. La première ligne de bio.** À qui c'est destiné et ce qui change pour
cette personne. Pas un intitulé de poste, pas d'adjectifs, pas une liste
d'identités séparées par des barres. Sur Instagram, le reste des 150
caractères porte une preuve ou une offre simple. Sur TikTok, 80 caractères en
tout : une ligne, plus une demi-ligne au mieux. Si le compte est sur les deux,
écris la version TikTok d'abord et rallonge-la pour Instagram, pas l'inverse.

**3. Les trois épingles.** Trois places sur les deux applis, trois rôles : la
meilleure preuve, l'explication la plus claire de l'offre, la meilleure
présentation de la personne ou de la marque. C'est la correction qui rapporte
le plus sur tout le profil, et elle prend quatre taps. Une grille sans
épingle montre la dernière publication, autant jouer à pile ou face.

**4. Temps forts (Instagram) ou playlists (TikTok).** Quatre à six, nommés
d'après les questions qu'un acheteur se pose : Tarifs, Résultats, Comment ça
marche, Qui je suis. Pas "Divers". Supprime le reste. Sur TikTok, si les
playlists ne sont pas disponibles sur le compte, saute cette étape et
renforce les épingles.

**5. Le lien.** Une destination qui tient ce que la bio vient de promettre.
Instagram en autorise cinq ; deux, c'est déjà un menu, et un menu convertit
moins bien qu'une porte. Sur TikTok, le lien en bio n'est pas disponible pour
tous les comptes : s'il manque, dis-le, et propose de faire porter l'appel par
la bio et les épingles en attendant.

**6. Les couvertures de la grille.** Les neuf premières, en vignette. Les
couvertures se choisissent, elles ne restent pas sur la première image venue.
Trois ou quatre mots de texte sur la couverture rendent une grille lisible
d'un coup d'œil. Pour un compte sans visage (motion design, texte à l'écran,
voix off IA), c'est encore plus vrai : sans texte, neuf écrans animés se
ressemblent tous.

## Sortie

Le tableau de notes, puis les réécritures en blocs prêts à copier, dans
l'ordre des corrections, chacune passée par `/rt-humain`. Renote à la fin et
montre l'écart honnêtement. Si la réécriture arrive à 84 et pas à 98, dis 84,
et dis ce qui manque, en général une grille, une habitude de stories ou de
publication, et une vidéo épinglée qui n'existe pas encore. Rien de tout ça
n'est une réécriture.

Ce skill ne modifie rien sur Instagram ni sur TikTok. L'utilisateur change
chaque champ lui-même.
