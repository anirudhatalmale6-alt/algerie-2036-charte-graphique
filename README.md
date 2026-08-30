# ALGÉRIE 2036 — charte graphique

Identité visuelle de la plateforme *Algérie 2036* : le signe, les couleurs, la
typographie, et le système qui distingue **un fait, un objectif et un
scénario**.

**Version 1.1 — vert et blanc exclusivement.**

Ouvrir **`charte.html`** dans un navigateur. Le document est autonome : les
polices et les logos sont dans le dossier, aucune requête vers l'extérieur.

---

## Le signe

Trois frondes montent d'un socle commun et se rejoignent en pointe —
l'abstraction du monument d'Alger, redessinée au trait. Les trois branches se
lisent aussi comme trois pales, ce qui rattache le signe au volet énergies
renouvelables ; le fût central se lit comme une colonne qui s'élève.

La version de référence est **le signe blanc sur aplat vert**.

**Une précaution, écrite aussi dans la charte :** le monument dont vient la
silhouette est un mémorial national. Le signe est une abstraction géométrique,
pas une photographie ni un décalque. Il ne doit jamais être accolé au drapeau,
au sceau ou aux armoiries de l'État, et la plateforme ne doit jamais se
présenter comme un site officiel. Si le projet se rapproche un jour d'une
institution publique, l'usage du signe devra être validé par elle.

---

## Ce que la charte contient

| § | Contenu |
|---|---|
| 01 | La marque : 8 déclinaisons montrées, 10 fichiers, zone de protection, tailles minimales, interdits |
| 02 | Les couleurs : une seule teinte, sept crans de valeur V1 → V7 |
| 03 | **Les quinze couches de la carte**, identifiées par le motif et non par la couleur |
| 04 | La typographie : IBM Plex Sans / Sans Arabic / Mono, échelle, règles RTL |
| 05 | **Le statut de la donnée** : Fait / Objectif 2036 / Scénario |
| 06 | Les scores sur 100 |
| 07 | La carte : fond, couches, sélection, légende, mode nuit |
| 08 | Boutons, fiche territoire, champ en erreur sans rouge, légende |
| 09 | Accessibilité : contrastes mesurés |
| 10 | Les fichiers livrés |

---

## Ce que « vert et blanc exclusivement » a changé depuis la v1.0

La v1.0 portait quinze **teintes** pour les quinze couches de la carte : bleu
pour les ports, orange pour le solaire, violet pour l'hydrogène. La contrainte
supprime cette possibilité, et quinze verts différents seraient
indistinguables — surtout superposés à 55 % d'opacité.

Chaque couche est donc identifiée par un **motif**, un **code de deux lettres**
et le **nom écrit**. La valeur (V1 → V5) ne sert qu'à hiérarchiser : deux
couches peuvent partager une valeur, jamais un motif.

Les motifs sont définis **une seule fois**, dans la fonction `motif()` de
`outils/charte.py`, et prennent la couleur en paramètre. Ils sont donc
reproductibles à l'identique dans le code du site.

**Vérifié, pas supposé :** les onze captures du dossier `apercus/` ont été
analysées pixel par pixel — **0 pixel coloré hors de la bande verte sur
13 721 600**. `apercus/11-preuve-noir-et-blanc.png` est la même planche de
couches convertie en niveaux de gris : les quinze motifs restent
distinguables.

---

## Deux choix qui méritent une explication

**Les « neutres » sont des verts, pas des gris.** Le texte, les filets et les
fonds de section sont des verts désaturés. Un gris neutre introduirait une
seconde teinte et le système ne serait plus vrai.

**Rien n'est distingué par la couleur seule.** Un fait, un objectif et un
scénario se différencient par le motif, la bordure, une pastille et le **mot
écrit**. C'était déjà vrai en v1.0 ; en monochrome, c'est la seule mécanique
possible — donc elle est plus solide.

C'est la traduction graphique de la règle posée au § 16 du cahier des charges :
`FACTS ≠ TARGETS ≠ PROJECTIONS`.

---

## Une décision qui vous revient : le rouge

« Vert et blanc exclusivement » supprime le rouge. Sur une page vitrine, aucun
problème. Dans un formulaire, le rouge est le signal universel d'une saisie
refusée.

La charte tient la règle — **pas de rouge** — et signale une erreur par un
cadre en Vert nuit épaissi à 2 px, un signe `✕`, et la phrase qui dit quoi
corriger. Trois signaux, aucun n'est la couleur, ce qui est de toute façon la
bonne pratique.

Si vous préférez rouvrir une couleur d'alerte unique, elle sera ajoutée comme
**exception écrite**, réservée aux erreurs de formulaire et aux actions
destructrices, interdite en communication.

---

## Les chiffres de ce document sont calculés, pas saisis

`outils/charte.py` calcule chaque rapport de contraste (formule WCAG 2.1) à
partir des couleurs elles-mêmes. Si un vert est retouché, le chiffre affiché
dans la charte change tout seul — il n'y a pas de valeur recopiée à la main qui
pourrait devenir fausse.

Même principe pour le logo : `outils/marque.py` contient le tracé des trois
frondes **une seule fois**, et les dix fichiers en découlent. Les textes sont
convertis en tracés — un logo qui dépend d'une police installée sur la machine
du lecteur n'est pas un logo. L'arabe est mis en forme par HarfBuzz avant
conversion ; sans cela les lettres sortent isolées, et une seule passe en
« rtl » sur `الجزائر 2036` retournait le nombre en `6302`.

---

## Ce que la charte ne fait pas

Elle ne contient **aucune donnée sur l'Algérie**. Pas une population, pas une
profondeur de port, pas une capacité électrique, pas un mégawatt. La valeur de
la plateforme sera la qualité de ses sources ; un chiffre inventé pour remplir
une maquette est un chiffre qui finit en ligne. Les composants montrés dans la
charte affichent donc `non renseigné`, et c'est l'état par défaut d'un champ
tant qu'une source datée n'est pas fournie.

Elle ne donne pas non plus d'équivalents CMJN ni de références Pantone : une
conversion dépend du papier et du profil de l'imprimeur. L'imprimeur cale sur
les valeurs RVB données ici et renvoie un BAT ; les références sont ajoutées à
ce moment-là.

---

## Régénérer

```
python3 outils/marque.py     # les 10 fichiers SVG du logo
python3 outils/png.py        # les mêmes en PNG transparent, dans logo/png/
python3 outils/charte.py     # charte.html
python3 outils/apercus.py    # les captures du dossier apercus/
```

`marque.py` a besoin de `uharfbuzz` et `fonttools`. `charte.py` n'a besoin de
rien. `png.py` et `apercus.py` ont besoin de Playwright.

`apercus.py` lance Chromium avec `--disable-lcd-text` : sans ce drapeau,
l'anticrénelage sous-pixel pose des franges **orange et bleues** sur chaque
lettre, et la capture censée prouver « vert et blanc » contient alors des
dizaines de milliers de pixels qui ne le sont pas.

---

## Licences

Le logo et la charte appartiennent à JNCORP INC.

Les polices IBM Plex sont sous **SIL Open Font License 1.1**
(`polices/LICENCE-IBM-Plex.txt`) : elles peuvent être hébergées sur vos
serveurs et embarquées dans vos documents.
