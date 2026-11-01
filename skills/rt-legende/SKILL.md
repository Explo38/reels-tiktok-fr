---
name: rt-legende
description: >-
  Écrit la légende Instagram ou TikTok : la ligne qui survit à la coupe "plus",
  le corps, la seule demande, les mots-clés de recherche et 5 hashtags maximum,
  puis la vérifie avant publication. À utiliser quand l'utilisateur dit "écris
  la légende", "légende pour ce reel", "description tiktok", "qu'est-ce que je
  mets en description", "quels hashtags", "mots-clés pour la recherche TikTok",
  ou qu'il a une vidéo ou un carrousel prêt et qu'il lui manque le texte.
---

# rt-legende

Un outil est dans ce dossier et il tourne :

```bash
python3 legende.py legende.txt --plateforme tiktok
python3 legende.py legende.txt --plateforme instagram
python3 legende.py legende.txt --plateforme tiktok --mots-cles "recherche d'emploi,lettre de motivation"
```

Il affiche la légende comme le fil l'affiche : la partie visible dans un cadre,
le reste derrière le "plus". Lis ce cadre avant tout le reste de ce que tu as
écrit.

## D'abord, la plateforme

Les deux coupent la légende, mais pas au même endroit :

| | visible avant "plus" | maximum |
| --- | --- | --- |
| **TikTok** | ~80 à 100 caractères | 4 000 |
| **Instagram** | ~125 caractères | 2 200 |

Demande où ça part. Si c'est sur les deux, écris une ligne 1 sous 90 caractères :
elle passe partout. Lance `legende.py --plateforme les-deux` : il vérifie les
deux coupes d'un coup.

## Ensuite, décide quel rôle a cette légende

C'est la décision qui ruine les légendes quand on la saute.

**Cas A : la vidéo les a déjà accrochés.** Une vidéo porte son propre hook dans
les deux premières secondes, dit et affiché. La légende n'est pas un second hook,
et concurrencer la vidéo, c'est perdre les deux. Son rôle : la demande, le
contexte qui rend la demande logique, et les mots que les gens tapent dans la
recherche.

**Cas B : la légende est le contenu.** Une photo, une image seule, une couverture
de carrousel qui ouvre une boucle. Là, la ligne 1 est le hook et elle fonctionne
exactement comme un hook vidéo : concrète, courte, coupée sur un suspense plutôt
qu'en plein milieu d'une proposition.

Demande lequel tu écris. Si l'utilisateur a une vidéo avec un hook fort, écris
le cas A et dis pourquoi.

## La forme

```
Ligne 1     l'espace visible (~90 TikTok, ~125 Instagram).
            Cas A : la demande, simplement. Cas B : le hook.
            Jamais un bonjour, jamais un hashtag, jamais un émoji en premier
            caractère.
Corps       paragraphes courts, une ligne vide entre chaque. Deux à six.
            C'est là que vivent les mots-clés de recherche.
La demande  une seule. Commenter un mot-clé, enregistrer, ou écrire en DM. Une.
Hashtags    cinq maximum, sur leur propre ligne en bas, ou aucun.
```

Presque rien n'a besoin des 2 200 caractères d'Instagram, et encore moins des
4 000 de TikTok. Une légende qui mérite le tap puis livre 600 caractères bat une
légende qui en livre 1 800.

## Les hashtags, honnêtement

Les hashtags ne sont plus un levier de portée, et les plateformes l'ont dit par
un changement de produit. **Instagram a plafonné les hashtags à cinq par
publication le 18 décembre 2025**, contre trente avant, en expliquant que
"quelques hashtags ciblés (5 maximum) plutôt que beaucoup de génériques"
fonctionnent mieux. Adam Mosseri avait déjà dit en février 2025 que les hashtags
n'augmentent pas la portée : c'est une étiquette, pas un levier de diffusion.
**TikTok limite aussi à cinq par publication.**

Donc : cinq maximum, précis, comme étiquettes de sujet, sur les deux. Si
l'utilisateur a un bloc de vingt hashtags dans ses notes, ce bloc est mort et
`legende.py` le fera échouer.

`#fyp`, `#pourtoi`, `#viral`, `#explore`, `#foryou` ne décrivent rien. Coupe-les.

## Les mots-clés comptent plus que les hashtags

**Instagram** lit le texte de la légende pour sa recherche. Le terme pour lequel
l'utilisateur veut être trouvé va dans la légende, comme une expression qu'un
humain taperait, dans une phrase normale. "Lettre de motivation" en toutes
lettres en ligne 3, pas "#lettredemotivation" dans un bloc en bas.

**TikTok** va plus loin : sa recherche lit la légende, le texte à l'écran **et**
ce qui est dit, parce qu'il transcrit l'audio. Le mot-clé doit donc être dit à
voix haute (par l'utilisateur ou par la voix off) ou affiché à l'écran, en plus
d'être dans la légende. Si la vidéo est déjà faite et que le mot-clé n'y est ni
dit ni écrit, signale-le : la légende seule fait moins.

Demande deux ou trois de ces termes, puis passe-les à `legende.py` :

```bash
python3 legende.py brouillon.txt --plateforme tiktok --mots-cles "recherche d'emploi,lettre de motivation"
```

## Règles

- **Pas de lien dans la légende.** Les légendes ne sont cliquables ni sur
  Instagram ni sur TikTok. Une URL dans le corps, c'est du texte mort qui dit
  "je ne connais pas cette appli". Bio ou DM.
- **Une seule demande.** Deux demandes, c'est zéro. `legende.py` les compte.
- **La demande par mot-clé a besoin d'un mot que les gens peuvent taper.** Un
  mot, sans espace, sans émoji, sans accent si possible, et dis-le aussi dans la
  vidéo. `Commente LETTRE` marche. `Commente "le modèle de lettre"`, non.
- **Écris le premier commentaire à part** s'il y a un lien ou un complément.
  Signale-le dans le récapitulatif. Sur TikTok, un commentaire fait 150
  caractères maximum.
- **Les émojis servent de ponctuation, pas de décoration.** `legende.py` signale
  tout ce qui dépasse 4 pour 100 caractères.
- **Le texte alternatif vaut 20 secondes.** Pour les carrousels et les photos,
  écris-le. Il est lu par les lecteurs d'écran et par la plateforme.

## La boucle

1. Fixe la plateforme, puis le cas A ou B, et dis lequel.
2. Rédige.
3. Passe-la à `/rt-humain`. Les légendes sont courtes, donc les tics IA s'y
   entendent plus que partout ailleurs dans le pack.
4. Lance `legende.py --plateforme ...` avec les mots-clés de l'utilisateur.
   Corrige chaque ÉCHEC. Pour chaque ALERTE, décide à voix haute plutôt qu'en
   silence.
5. Affiche le bloc prêt à copier, puis le récapitulatif :

```
LÉGENDE PRÊTE
plateforme : TikTok
cas :        A, la vidéo porte le hook
visible :    84 sur ~90 caractères avant la coupe
demande :    une, commente LETTRE
hashtags :   3
recherche :  "lettre de motivation" dite à 0:01, à l'écran carton 1, en ligne 1
             "recherche d'emploi" en ligne 3
legende.py : PRÊTE
```

Rien n'est publié. L'utilisateur colle le texte.
