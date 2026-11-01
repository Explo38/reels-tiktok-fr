---
name: rt-publication
description: >-
  Programme et publie sur Instagram et TikTok les posts que l'utilisateur a
  validés : choix des jours, meilleurs horaires, programmation en masse via
  Metricool (connecteur officiel) ou via les planificateurs natifs (Meta
  Business Suite, TikTok Studio), sinon kit de publication manuel. À utiliser
  quand l'utilisateur dit "publie", "programme mes posts", "planifie la
  publication", "poste en auto", "meilleurs horaires", "quand poster", ou
  quand /rt-studio arrive à l'étape de publication.
---

# rt-publication

La dernière étape. Elle ne touche qu'à des posts **validés** par
l'utilisateur, et elle passe par des outils autorisés par les plateformes.

## Garde-fous, non négociables

1. **Rien ne part sans validation explicite.** Avant de programmer, montre le
   récapitulatif complet (tableau ci-dessous) et attends un « oui » clair de
   l'utilisateur pour CE lot précis. Un « oui » ne couvre que les posts listés,
   tels qu'ils sont listés.
2. **Un post modifié après validation redevient un brouillon.** Changement de
   légende, de vidéo, d'horaire ou de plateforme : redemande.
3. **Pas d'automatisation interdite.** Pas de robot qui se connecte au compte,
   pas de publication par script non officiel, pas de mot de passe demandé ni
   saisi. Les CGU d'Instagram et de TikTok interdisent ces méthodes et
   restreignent les comptes qui les utilisent. Seules voies : un outil
   partenaire officiel (Metricool), le planificateur natif de la plateforme,
   ou l'utilisateur qui publie lui-même.
4. **Étiquette IA.** Si la vidéo contient une voix de synthèse ou des images
   générées, active l'étiquette « contenu généré par IA » de la plateforme
   (ou de l'outil, s'il la propose). Si l'outil ne la propose pas, signale
   que l'utilisateur doit l'ajouter dans l'appli.
5. **Crédit voix.** Si la voix vient de Kyutai Pocket TTS, le crédit « Voix :
   Kyutai Pocket TTS (CC-BY 4.0) » doit être présent (légende ou bio).

## Les trois voies, dans l'ordre

### Voie A : Metricool (recommandée)

Outil de gestion des réseaux sociaux qui publie automatiquement sur Instagram
et TikTok par les API officielles. Il existe un connecteur Claude
« Metricool Social Media Management » (outils `createScheduledPost`,
`getScheduledPosts`, `updateScheduledPost`, `getBestTimeToPostByNetwork`,
`getBrandSettings`...).

- Vérifie d'abord que le connecteur est actif dans la session. S'il ne l'est
  pas, dis à l'utilisateur qu'il peut l'ajouter depuis les connecteurs de
  claude.ai, et qu'il doit y relier ses comptes Instagram (professionnel) et
  TikTok depuis Metricool.
- Offre gratuite (à vérifier sur le site au moment de l'inscription) : une
  marque, un nombre limité de publications par mois. L'accès API est réservé
  aux offres payantes : si le connecteur refuse une action à cause de l'offre,
  dis-le simplement et passe à la voie B.
- Lis le schéma réel des outils avant de les appeler : les champs (texte,
  réseaux, date, fuseau, médias) font foi, pas ce fichier. Si un outil demande
  une URL de média publique et que la vidéo n'est que sur l'ordinateur,
  propose à l'utilisateur de l'importer dans la médiathèque de Metricool, puis
  continue.
- Programme **un post par appel**, puis relis la liste avec
  `getScheduledPosts` et compare au récapitulatif validé.

### Voie B : les planificateurs natifs

- **Instagram** : la programmation intégrée d'Instagram (comptes
  professionnels) ou le planificateur de Meta Business Suite.
- **TikTok** : TikTok Studio sur ordinateur (comptes Créateur ou Entreprise).
  La programmation n'y va pas loin dans le temps (environ 10 jours d'après les
  guides de 2026), alors programme par vagues.

Avec un outil de navigateur dans la session, tu peux préparer chaque post
dans le planificateur : importer le fichier, coller la légende, régler la
date. L'utilisateur reste présent, connecté lui-même, et **tu demandes une
confirmation avant le clic final « Programmer »** de chaque post. Si un
écran demande un mot de passe, un code ou des conditions à accepter, c'est
l'utilisateur qui le fait.

### Voie C : le kit manuel

Pour chaque post : le fichier, la légende à copier, la date et l'heure, les
réglages (étiquette IA, son à ajouter, couverture). L'utilisateur publie ou
programme lui-même. C'est aussi la voie pour ajouter un son tendance, qui ne
passe par aucun outil externe.

## Les horaires

Dans l'ordre de fiabilité :

1. **Les données du compte** : `getBestTimeToPostByNetwork` (Metricool),
   ou l'onglet audience des statistiques Instagram et TikTok Studio (heures
   d'activité des abonnés), ou `/rt-audit` sur les posts passés.
2. **Faute de données** (compte neuf) : une hypothèse de départ selon
   l'audience, présentée comme une hypothèse à tester. Pour des étudiants et
   jeunes diplômés : pause de midi en semaine et début de soirée. Pour des
   professionnels : début de matinée et midi. Varie les créneaux les deux
   premières semaines, puis garde ceux qui marchent.
3. **Le rappel qui compte** : l'heure pèse beaucoup moins que les deux
   premières secondes de la vidéo. Ne passe pas une heure sur les horaires.

Règles de calendrier : pas deux posts du même type d'affilée, au moins
quelques heures entre deux posts sur la même plateforme, une même vidéo
peut sortir sur Instagram et TikTok le même jour avec une légende adaptée à
chacune (`/rt-legende --plateforme les-deux`). Tout est en heure de Paris
sauf si l'audience est ailleurs.

## Le récapitulatif à valider

Écris-le dans `publication.csv` du dossier de campagne et montre-le :

```
PUBLICATION  ·  campagne "lancement-novembre"  ·  8 posts  ·  voie A (Metricool)

#  date        heure  plateforme  format     fichier                    légende (début)                       IA
1  mar 04/11   12:30  TikTok      vidéo      post-01_tiktok.mp4         "Une lettre de motivation me pren..."  oui
1  mar 04/11   18:30  Instagram   reel       post-01_reel.mp4           "Commente LETTRE et je t'envoie l..."  oui
2  jeu 06/11   12:15  Instagram   carrousel  post-02_slide-01..07.png   "Ton CV est lu en 7 secondes. Voi..."  non
...

Réponds "oui" pour programmer ces 8 publications telles quelles, ou dis ce que tu changes.
```

Après programmation, donne le statut réel de chaque ligne (programmé, en
erreur, à faire à la main) et mets à jour `campagne.json` (`statut` :
`programmé`, `publié`, `à faire`).

## Ce que ce skill ne fait pas

- Il ne publie jamais un post que l'utilisateur n'a pas validé.
- Il ne crée pas de compte, n'accepte pas de conditions, ne saisit pas de mot
  de passe.
- Il ne paie rien et ne lance pas de publicité payante.
