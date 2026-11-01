---
name: rt-carrousel
description: >-
  Construit un carrousel Instagram (1080x1350) ou un post en mode photo TikTok
  (1080x1920, avec musique) : la couverture qui fait glisser, le texte diapo par
  diapo, et les fichiers à importer. À utiliser quand l'utilisateur dit
  "carrousel", "slides", "diapos", "post à faire glisser", "mode photo tiktok",
  "transforme ça en carrousel", ou qu'il a une idée en liste ou en étapes qui
  mourrait en image seule.
---

# rt-carrousel

Le carrousel est le format où les gens restent le plus longtemps, parce qu'un
glissement est une interaction et un défilement ne l'est pas. Sur Instagram, il
a même une seconde chance : la plateforme peut remontrer un carrousel à partir
d'une diapo plus loin à quelqu'un qui n'a pas interagi la première fois. Donc
la diapo 2 doit aussi tenir seule.

Sur TikTok, l'équivalent s'appelle le **mode photo** : une suite d'images qu'on
fait glisser, avec un son par-dessus. Même logique, autre format.

Le format récompense une idée découpée en étapes. Il punit une légende coupée en
morceaux.

## Quand l'utiliser plutôt qu'une vidéo

Utilise un carrousel quand l'idée a **une suite et mérite d'être relue** : des
étapes, une méthode en plusieurs parties, un avant / après, une liste qu'on a
envie de capturer. Utilise une vidéo quand l'idée a du mouvement, un visage, ou
un payoff qu'il faut voir se produire.

Si l'idée tient en une affirmation, ce n'est ni l'un ni l'autre. Passe-la à
`/rt-video` et dis-le.

## D'abord, la plateforme

| | Instagram | TikTok (mode photo) |
| --- | --- | --- |
| format | 1080x1350 (4:5) | 1080x1920 (9:16) |
| maximum | 20 éléments | 35 images |
| son | facultatif | un son par-dessus, choisis-le |
| texte | loin des bords | dans la zone sûre : entre y=230 et y=1440, 140 px libres à droite, ~60 px à gauche |

Sur TikTok, le bas de l'écran est couvert par le nom, la légende et le son, la
colonne de droite par les boutons. Un texte posé là n'est pas lu.

Si c'est pour les deux, ne contente-toi pas d'étirer : une diapo 4:5 centrée sur
un fond 9:16 déborde de la zone sûre en bas. Refais la mise en page à 1080x1920
avec le texte dans la zone sûre. Même texte, deux mises en page.

## Structure

6 à 10 diapos sur les deux plateformes. Le plafond est à 20 sur Instagram et 35
sur TikTok, et les deux donnent un livre que personne ne finit. Sous 5, le
glissement ne démarre jamais.

```
1         COUVERTURE  le hook. 6 mots maximum, à une taille lisible en vignette
                      dans la grille. Une ligne de promesse en dessous.
2         L'ENJEU     pourquoi ça compte, en une phrase. Cette diapo est aussi
                      une seconde couverture, donc elle ne peut pas être de la mise
                      en place.
3 à N     UNE IDÉE PAR DIAPO. Un titre de 3 à 7 mots, 25 mots maximum en dessous.
                      Si une diapo demande un paragraphe, c'est deux diapos.
N+1       RÉCAP       tout le contenu en liste. C'est la diapo qu'on capture.
DERNIÈRE  DEMANDE     une seule action. Enregistrer, commenter un mot-clé, ou
                      suivre. Une.
```

## Règles du texte

- **La couverture fait l'essentiel du résultat.** Six mots. Gros. Rien dans la suite ne
  sauve une couverture que personne ne fait glisser.
- **Pense au recadrage de la grille.** Les deux grilles de profil recadrent en
  portrait, plus haut que large, et le ratio exact a déjà changé plusieurs fois.
  Sur Instagram, construis à 1080x1350 et garde le texte de couverture bien au
  milieu, à plus de 120 pixels de chaque bord. Sur TikTok, garde-le au centre de
  la zone sûre. Le recadrage ne compte plus.
- **Numérote les diapos** (3/8). Les gens vont plus loin quand ils voient la fin.
- **Aucune diapo n'est un paragraphe.** Si ça ne tient pas en 25 mots, coupe en
  deux.
- **La diapo récap est celle qu'on capture et qu'on envoie.** Les partages sont
  le signal le plus fort qu'on puisse obtenir. Fais-la autonome et lisible sans
  contexte.
- **Le pseudo sur chaque diapo**, petit, dans un coin bas (sur TikTok, en haut à
  gauche de la zone sûre, le bas est couvert). Les captures voyagent sans toi.
- **Le son sur TikTok** donne l'ambiance, pas le sens : le texte doit se
  comprendre sans. Un compte entreprise a souvent un catalogue restreint (en
  général la bibliothèque musicale commerciale), vérifie que le son choisi y est.
- **Texte alternatif au moins sur la couverture.** Il est lu par les lecteurs
  d'écran et par la plateforme.

## Construire les fichiers

Instagram veut du 1080x1350 (4:5), JPEG ou PNG, jusqu'à 20 éléments. TikTok veut
du 1080x1920 (9:16), jusqu'à 35 images. Construis en HTML et imprime chaque
diapo :

```bash
# une <section> par diapo, 1080x1350 (Instagram) ou 1080x1920 (TikTok),
# page-break-after: always
# puis Chrome headless --print-to-pdf, ou l'outil HTML vers image que tu as déjà
```

Écris le HTML avec `width:1080px; height:1350px` (ou `height:1920px`), une seule
couleur d'accent, et un texte jamais plus petit que 32px, parce que tout ça se
lit sur un téléphone au tiers de sa taille réelle. Si le projet a un skill de
marque ou un design system, utilise-le et n'invente pas de palette.

## Sortie

D'abord le texte diapo par diapo, en liste numérotée que l'utilisateur lit en
dix secondes et corrige avant tout rendu. Ensuite la **légende**, qui pour un
carrousel est le cas B de `/rt-legende` : la légende travaille ici, parce que la
couverture a déjà utilisé ses six mots. Sur TikTok, ajoute le son proposé.

Passe les deux par `/rt-humain`. Ne construis les fichiers qu'une fois le texte
validé par l'utilisateur.

```
CARROUSEL  ·  Instagram 1080x1350  ·  8 diapos

1  COUVERTURE  LA CLAUSE À 4 800 €
               Une ligne que je mets dans chaque devis.
2  ENJEU       Le client a validé. Neuf jours après, il voulait être remboursé.
3              CE QU'ELLE DIT
               Paiement à la livraison, pas à la validation.
...
7  RÉCAP       Les quatre lignes, dans l'ordre.
8  DEMANDE     Commente DEVIS et je t'envoie la clause complète.

Légende : cas B, hook en ligne 1, une demande, 3 hashtags.
Version TikTok : mêmes 8 diapos refaites en 1080x1920, texte dans la zone sûre,
son calme et sans paroles pour laisser lire.
```

Rien n'est importé. L'utilisateur publie.
