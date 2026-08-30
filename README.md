# ALGÉRIE 2036 — charte graphique

Identité visuelle de la plateforme *Algérie 2036* : le signe, les couleurs, la
typographie, et le système qui distingue **un fait, un objectif et un
scénario**.

Ouvrir **`charte.html`** dans un navigateur. Le document est autonome : les
polices et les logos sont dans le dossier, aucune requête vers l'extérieur.

---

## Le signe

Trois frondes montent d'un socle commun et se rejoignent en pointe —
l'abstraction du monument d'Alger, redessinée au trait. Les trois branches se
lisent aussi comme trois pales, ce qui rattache le signe au volet énergies
renouvelables ; le fût central se lit comme une colonne qui s'élève.

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
| 01 | La marque : 10 déclinaisons, zone de protection, tailles minimales, interdits |
| 02 | Les couleurs : primaires, neutres, et **15 couleurs de couches** pour la carte |
| 03 | La typographie : IBM Plex Sans / Sans Arabic / Mono, échelle, règles RTL |
| 04 | **Le statut de la donnée** : Fait / Objectif 2036 / Scénario |
| 05 | Les scores sur 100 |
| 06 | La carte : fond, couches, sélection, légende |
| 07 | Boutons, fiche territoire |
| 08 | Accessibilité : contrastes mesurés |
| 09 | Les fichiers livrés |

---

## Deux choix qui méritent une explication

**Le vert de marque n'est jamais une couche de la carte.** Le vert appartient à
l'interface : boutons, sélection, en-têtes. S'il servait aussi à représenter
une donnée, on ne saurait plus, en regardant la carte, ce qui est le logiciel
et ce qui est le territoire.

**Rien n'est distingué par la couleur seule.** Un fait, un objectif et un
scénario se différencient par le motif (aplat, aplat clair, hachures), par la
bordure (pleine, pleine, tiretée), par une pastille et par le **mot écrit**. En
noir et blanc, en impression, pour un lecteur daltonien, ou dans une capture
d'écran reprise ailleurs, la différence survit.

C'est la traduction graphique de la règle posée au § 16 du cahier des charges :
`FACTS ≠ TARGETS ≠ PROJECTIONS`.

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
rien. `apercus.py` a besoin de Playwright.

---

## Licences

Le logo et la charte appartiennent à JNCORP INC.

Les polices IBM Plex sont sous **SIL Open Font License 1.1**
(`polices/LICENCE-IBM-Plex.txt`) : elles peuvent être hébergées sur vos
serveurs et embarquées dans vos documents.
