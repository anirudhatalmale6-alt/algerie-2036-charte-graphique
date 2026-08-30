#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere charte.html — version 1.1, vert et blanc exclusivement.

Les rapports de contraste ne sont pas ecrits a la main : ils sont CALCULES
ici (formule WCAG 2.1) a partir des couleurs elles-memes. Un vert qu'on
retouche change le chiffre affiche dans la charte, sans intervention.

v1.1 : la palette ne contient plus qu'UNE teinte, le vert. Les quinze
couches de la carte ne se distinguent donc plus par la couleur mais par le
MOTIF, la VALEUR et un CODE ecrit. C'est la seule facon de tenir « vert et
blanc exclusivement » sur une carte multi-couches sans la rendre illisible.
"""

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERSION = '1.1'
DATE = '30 août 2026'


# --- Contraste ------------------------------------------------------------

def _canal(c):
	c = c / 255.0
	return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexa):
	h = hexa.lstrip('#')
	r, v, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
	return 0.2126 * _canal(r) + 0.7152 * _canal(v) + 0.0722 * _canal(b)


def contraste(a, b):
	la, lb = luminance(a), luminance(b)
	if la < lb:
		la, lb = lb, la
	return (la + 0.05) / (lb + 0.05)


def rgb(hexa):
	h = hexa.lstrip('#')
	return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# --- La palette : une seule teinte -----------------------------------------
#
# Tout ce qui suit est du vert ou du blanc. Les « neutres » sont des verts
# desatures, pas des gris : le gris pur introduirait une seconde teinte.

BLANC = '#FFFFFF'
NUIT = '#04241A'        # V1 — le plus sombre
FORET = '#00432A'       # V2
VERT = '#006233'        # V3 — Vert Algerie, la couleur de la marque
VIF = '#0F8C4C'         # V4 — Vert 2036
CLAIR = '#63B98C'       # V5
PALE = '#BFE0CE'        # V6
VOILE = '#E9F4EE'       # V7
PAPIER = '#F6FAF8'      # fond d'application
ENCRE = '#0A2019'       # texte courant — un vert si sombre qu'il lit noir
ARDOISE = '#54685E'     # texte secondaire
TRAIT = '#D3E2D9'       # filets

PRIMAIRES = [
	('Vert Algérie', VERT, 'La couleur de la marque. Logo, en-têtes, boutons '
	 'principaux, éléments actifs.'),
	('Blanc', BLANC, 'La respiration. Fond de toutes les pages de contenu et '
	 'des cartes.'),
	('Vert 2036', VIF, 'L’accent vivant : liens, sélection sur la carte, états '
	 'de survol, la fronde centrale du logo.'),
	('Vert nuit', NUIT, 'Bandeaux sombres, pied de page, fond de carte en mode '
	 'nuit.'),
]

NEUTRES = [
	('Encre', ENCRE, 'Texte courant. C’est un vert, pas un noir : il se pose '
	 'sur le blanc sans jurer avec la marque.'),
	('Ardoise', ARDOISE, 'Texte secondaire, légendes, unités, sources.'),
	('Trait', TRAIT, 'Filets, bordures de tableaux, séparateurs.'),
	('Papier', PAPIER, 'Fond d’application, fond de carte clair.'),
	('Voile', VOILE, 'Fonds de section, ligne de tableau survolée, halo de '
	 'sélection.'),
]

VALEURS = [
	('V1', NUIT, 'Vert nuit'),
	('V2', FORET, 'Vert forêt'),
	('V3', VERT, 'Vert Algérie'),
	('V4', VIF, 'Vert 2036'),
	('V5', CLAIR, 'Vert clair'),
	('V6', PALE, 'Vert pâle'),
	('V7', VOILE, 'Voile'),
]


# --- Les motifs -----------------------------------------------------------
#
# Quinze motifs distincts, tous construits avec la MEME couleur passee en
# parametre. C'est ce qui remplace les quinze teintes de la v1.0.

def motif(nom, c):
	"""Renvoie le CSS de fond du motif `nom` dessine dans la couleur `c`."""
	m = {
		'plein':
			'background:%s' % c,
		'vagues':
			'background-image:repeating-radial-gradient(circle at 50%% 100%%,'
			'rgba(0,0,0,0) 0 4px,%s 4px 5.6px,rgba(0,0,0,0) 5.6px 12px);'
			'background-size:12px 12px' % c,
		'rails':
			'background-image:repeating-linear-gradient(0deg,%s 0 2px,'
			'rgba(0,0,0,0) 2px 4px,%s 4px 6px,rgba(0,0,0,0) 6px 18px)' % (c, c),
		'grille':
			'background-image:repeating-linear-gradient(0deg,%s 0 1px,'
			'rgba(0,0,0,0) 1px 6px),repeating-linear-gradient(90deg,%s 0 1px,'
			'rgba(0,0,0,0) 1px 6px)' % (c, c),
		'gouttes':
			'background-image:radial-gradient(%s 2px,rgba(0,0,0,0) 2.4px);'
			'background-size:10px 10px' % c,
		'rayons':
			'background-image:repeating-linear-gradient(45deg,%s 0 4px,'
			'rgba(0,0,0,0) 4px 11px)' % c,
		'chevrons':
			'background-image:repeating-linear-gradient(45deg,%s 0 3px,'
			'rgba(0,0,0,0) 3px 9px),repeating-linear-gradient(-45deg,%s 0 3px,'
			'rgba(0,0,0,0) 3px 9px);background-size:100%% 50%%,100%% 50%%;'
			'background-position:0 0,0 100%%;background-repeat:repeat-x' % (c, c),
		'croisillons':
			'background-image:repeating-linear-gradient(45deg,%s 0 2px,'
			'rgba(0,0,0,0) 2px 9px),repeating-linear-gradient(-45deg,%s 0 2px,'
			'rgba(0,0,0,0) 2px 9px)' % (c, c),
		'briques':
			'background-image:repeating-linear-gradient(0deg,%s 0 1.5px,'
			'rgba(0,0,0,0) 1.5px 8px),repeating-linear-gradient(90deg,%s 0 1.5px,'
			'rgba(0,0,0,0) 1.5px 16px)' % (c, c),
		'verticales':
			'background-image:repeating-linear-gradient(90deg,%s 0 3px,'
			'rgba(0,0,0,0) 3px 10px)' % c,
		'semis':
			'background-image:radial-gradient(%s 1.1px,rgba(0,0,0,0) 1.5px);'
			'background-size:5px 5px' % c,
		# Trois densites de points, jamais deux motifs de points identiques :
		# « pois » (gros, en quinconce), « gouttes » (moyens, alignes),
		# « semis » (fins). C'est une rampe de densite, lisible a petite taille.
		'pois':
			'background-image:radial-gradient(%s 3px,rgba(0,0,0,0) 3.4px),'
			'radial-gradient(%s 3px,rgba(0,0,0,0) 3.4px);'
			'background-size:16px 16px,16px 16px;'
			'background-position:0 0,8px 8px' % (c, c),
		'sillons':
			'background-image:repeating-linear-gradient(0deg,%s 0 3px,'
			'rgba(0,0,0,0) 3px 10px)' % c,
		'damier':
			'background-image:repeating-conic-gradient(%s 0 25%%,'
			'rgba(0,0,0,0) 0 50%%);background-size:11px 11px' % c,
		# 135° et non 45° : « rayons » occupe deja le 45°, et deux motifs
		# diagonaux dans le meme sens se confondent en legende.
		'barres':
			'background-image:repeating-linear-gradient(135deg,%s 0 5px,'
			'rgba(0,0,0,0) 5px 8px,%s 8px 9.5px,rgba(0,0,0,0) 9.5px 17px)' % (c, c),
	}
	return m[nom]


# Les couches de la carte : (code, nom, motif, valeur).
# Regle inchangee depuis la v1.0 : le vert de marque n'est jamais SEUL a
# porter une couche — c'est le motif qui identifie, la valeur qui hierarchise.
COUCHES = [
	('Infrastructures', [
		('PT', 'Ports & maritime', 'vagues', VERT),
		('RR', 'Rail & routes', 'rails', FORET),
		('NU', 'Numérique, fibre & data centers', 'grille', VIF),
		('EA', 'Eau, barrages & dessalement', 'gouttes', CLAIR),
	]),
	('Énergie', [
		('SO', 'Solaire', 'rayons', VIF),
		('EO', 'Éolien', 'chevrons', CLAIR),
		('H2', 'Hydrogène vert', 'croisillons', VERT),
		('EC', 'Énergie conventionnelle', 'briques', FORET),
	]),
	('Économie', [
		('ZF', 'Zones franches', 'plein', VERT),
		('IN', 'Industrie & corridors', 'verticales', FORET),
		('CH', 'Capital humain & universités', 'semis', VIF),
	]),
	('Territoire & environnement', [
		('FO', 'Forêt & Barrage vert', 'pois', VERT),
		('AG', 'Agriculture', 'sillons', VIF),
		('UR', 'Urbanisme & villes', 'damier', CLAIR),
		('RQ', 'Risques & contraintes', 'barres', NUIT),
	]),
]

# Les scores : la valeur porte le niveau, mais elle ne le porte pas SEULE —
# le nombre est toujours ecrit et une jauge a quatre crans le double.
SCORES = [
	('0 – 39', 'Faible', VOILE, ENCRE, 1),
	('40 – 59', 'Moyen', PALE, ENCRE, 2),
	('60 – 79', 'Bon', VIF, BLANC, 3),
	('80 – 100', 'Élevé', VERT, BLANC, 4),
]

ECHELLE = [
	('Affichage', 44, 1.1, 600, 'Plex Sans', 'Titre de page d’accueil.'),
	('Titre 1', 32, 1.2, 600, 'Plex Sans', 'Titre de section.'),
	('Titre 2', 24, 1.25, 600, 'Plex Sans', 'Sous-section, nom de wilaya.'),
	('Titre 3', 19, 1.3, 600, 'Plex Sans', 'Bloc de fiche.'),
	('Corps', 16, 1.6, 400, 'Plex Sans', 'Texte courant. Jamais en dessous.'),
	('Corps réduit', 14, 1.55, 400, 'Plex Sans', 'Notes, aides de saisie.'),
	('Étiquette', 12, 1.35, 500, 'Plex Sans', 'Majuscules, interlettrage '
	 '+0,06 em. Légendes de carte.'),
	('Chiffre', 16, 1.3, 400, 'Plex Mono', 'Scores, surfaces, distances, '
	 'coordonnées. Chiffres à chasse fixe.'),
]

INTERDITS = [
	('Ne pas déformer', 'Le rapport hauteur / largeur est fixe.'),
	('Ne pas recolorer', 'Vert Algérie, blanc, ou encre. Aucune autre teinte, '
	 'nulle part.'),
	('Ne pas ajouter d’ombre', 'Ni contour, ni relief, ni dégradé.'),
	('Ne pas poser sur une photo chargée',
	 'Sur image : la pastille pleine, ou un aplat vert derrière.'),
	('Ne pas accoler l’emblème de l’État',
	 'Ni drapeau, ni sceau, ni armoiries : la plateforme n’est pas un '
	 'organisme public.'),
	('Ne pas réécrire le nom',
	 '« ALGÉRIE 2036 ». Pas « Algerie 2036 », pas « Algeria 2036 » dans les '
	 'versions française et arabe.'),
]

LOGOS = [
	('algerie2036-principal-blanc.svg', 'Principal — sur fond vert', 'sombre', 64),
	('algerie2036-principal.svg', 'Principal — sur fond blanc', 'clair', 64),
	('algerie2036-vertical.svg', 'Vertical', 'clair', 96),
	('algerie2036-arabe.svg', 'Arabe — الجزائر 2036', 'clair', 64),
	('algerie2036-marque.svg', 'Signe seul', 'clair', 84),
	('algerie2036-marque-noire.svg', 'Monochrome encre', 'clair', 84),
	('algerie2036-marque-blanche.svg', 'Monochrome blanc', 'sombre', 84),
	('algerie2036-pastille.svg', 'Pastille — favicon, application', 'clair', 84),
]


# --- Fabrication ----------------------------------------------------------

def note(r):
	"""Verdict WCAG mesure, pas devine. Le signe remplace la couleur d'alerte."""
	if r >= 7.0:
		return 'AAA', '✓'
	if r >= 4.5:
		return 'AA', '✓'
	if r >= 3.0:
		return 'AA gros texte', '△'
	return 'décoratif', '✕'


def case_couleur(nom, hexa, usage, fond=BLANC):
	r = contraste(hexa, fond)
	verdict, signe = note(r)
	rv, gv, bv = rgb(hexa)
	bordure = (' style="box-shadow:inset 0 0 0 1px %s"' % TRAIT
	           if contraste(hexa, BLANC) < 1.25 else '')
	return (
		'<div class="cc">'
		'<div class="cc-p" style="background:%s"%s></div>'
		'<div class="cc-t"><b>%s</b>'
		'<code>%s</code>'
		'<span class="mono">R %d · V %d · B %d</span>'
		'<span class="use">%s</span>'
		'<span class="ratio"><span class="sg">%s</span> %.2f:1 sur blanc — %s'
		'</span></div></div>'
	) % (hexa, bordure, nom, hexa, rv, gv, bv, usage, signe, r, verdict)


def page():
	h = []
	a = h.append

	a('<!doctype html><html lang="fr"><head><meta charset="utf-8">')
	a('<meta name="viewport" content="width=device-width,initial-scale=1">')
	a('<title>ALGÉRIE 2036 — Charte graphique v%s</title>' % VERSION)
	a('<style>')
	for poids in (400, 500, 600, 700):
		a('@font-face{font-family:"Plex";font-weight:%d;font-style:normal;'
		  'font-display:swap;src:url("polices/IBMPlexSans-%d.ttf") format("truetype")}'
		  % (poids, poids))
		a('@font-face{font-family:"PlexAr";font-weight:%d;font-style:normal;'
		  'font-display:swap;src:url("polices/IBMPlexSansArabic-%d.ttf") format("truetype")}'
		  % (poids, poids))
	for poids in (400, 600):
		a('@font-face{font-family:"PlexMono";font-weight:%d;font-style:normal;'
		  'font-display:swap;src:url("polices/IBMPlexMono-%d.ttf") format("truetype")}'
		  % (poids, poids))
	a('''
:root{--nuit:%s;--foret:%s;--vert:%s;--vif:%s;--clair:%s;--pale:%s;
--voile:%s;--papier:%s;--encre:%s;--ardoise:%s;--trait:%s}
*{box-sizing:border-box}
body{margin:0;background:var(--papier);color:var(--encre);
font:400 16px/1.6 "Plex",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.mono,code{font-family:"PlexMono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
.env{max-width:1080px;margin:0 auto;padding:0 28px}
header{background:var(--nuit);color:#fff;padding:56px 0 48px}
header .env{display:flex;align-items:flex-end;justify-content:space-between;gap:28px;flex-wrap:wrap}
header img{height:92px}
header .meta{font-size:13px;line-height:1.7;opacity:.82;text-align:right}
section{padding:52px 0;border-bottom:1px solid var(--trait)}
section:last-of-type{border:0}
h2{font:600 30px/1.2 "Plex";margin:0 0 6px;letter-spacing:-.01em}
h2 .num{color:var(--vert);font-family:"PlexMono";font-size:20px;margin-right:14px}
.chapo{color:var(--ardoise);max-width:64ch;margin:0 0 30px}
h3{font:600 19px/1.3 "Plex";margin:34px 0 12px}
p{max-width:70ch}
.grille{display:grid;gap:16px}
.g2{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
.g3{grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(186px,1fr))}
.carte{background:#fff;border:1px solid var(--trait);border-radius:10px;padding:18px}
.logo-case{background:#fff;border:1px solid var(--trait);border-radius:10px;
padding:22px;text-align:center}
.logo-case.sombre{background:var(--nuit);border-color:var(--nuit)}
.logo-case img{max-width:100%%;width:auto;height:auto}
.logo-case .lab{margin-top:16px;font-size:12px;color:var(--ardoise);
letter-spacing:.04em}
.logo-case.sombre .lab{color:#9FBDAF}
.cc{display:flex;gap:14px;align-items:flex-start;background:#fff;
border:1px solid var(--trait);border-radius:10px;padding:14px}
.cc-p{width:64px;height:64px;border-radius:8px;flex:none}
.cc-t{font-size:13px;line-height:1.5;display:flex;flex-direction:column;gap:2px}
.cc-t b{font-weight:600;font-size:15px}
.cc-t code{font-size:12px;color:var(--ardoise)}
.cc-t .mono{font-size:11px;color:var(--ardoise)}
.cc-t .use{color:var(--ardoise);margin-top:4px}
.ratio{font-family:"PlexMono";font-size:11px;margin-top:4px;color:var(--encre)}
.sg{font-family:"Plex",sans-serif;font-weight:600}
table{border-collapse:collapse;width:100%%;font-size:14px;background:#fff}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--trait);
vertical-align:top}
th{font:600 12px/1.3 "Plex";letter-spacing:.08em;text-transform:uppercase;
color:var(--ardoise);background:var(--voile)}
td.n{font-family:"PlexMono";font-variant-numeric:tabular-nums;white-space:nowrap}
.ech{display:flex;gap:0;border:1px solid var(--trait);border-radius:8px;
overflow:hidden}
.ech div{flex:1;height:58px;display:flex;align-items:flex-end;
justify-content:center;padding-bottom:6px;font:600 10px "PlexMono";
letter-spacing:.04em}
.couche{display:flex;align-items:center;gap:11px;font-size:14px;padding:9px 0;
border-bottom:1px solid var(--trait)}
.couche:last-child{border:0}
.sw{width:34px;height:26px;border-radius:5px;flex:none;
box-shadow:inset 0 0 0 1px var(--trait);background-color:#fff}
.code{font-family:"PlexMono";font-size:10px;font-weight:600;letter-spacing:.06em;
background:var(--voile);color:var(--encre);border-radius:4px;padding:3px 5px;
flex:none}
.couche .h{margin-left:auto;font-family:"PlexMono";font-size:11px;
color:var(--ardoise);white-space:nowrap}
.statut{border:1px solid var(--trait);border-radius:10px;overflow:hidden;background:#fff}
.statut .demo{height:96px;background-color:#fff}
.statut .txt{padding:15px}
.statut .txt b{display:block;font-size:15px}
.statut .txt span{font-size:13px;color:var(--ardoise);display:block;margin-top:5px}
.statut .txt .regle{font-family:"PlexMono";font-size:11px;color:var(--encre);
margin-top:9px;display:block}
.badge{display:inline-flex;align-items:center;gap:7px;border-radius:999px;
padding:5px 12px;font-size:12px;font-weight:600;letter-spacing:.04em}
.score{display:flex;align-items:center;gap:12px;background:#fff;
border:1px solid var(--trait);border-radius:10px;padding:14px}
.score .val{font-family:"PlexMono";font-weight:600;font-size:24px;
width:60px;height:60px;border-radius:12px;display:flex;align-items:center;
justify-content:center;flex:none;box-shadow:inset 0 0 0 1px var(--trait)}
.jauge{display:flex;gap:2px;margin-top:5px}
.jauge i{width:11px;height:7px;border-radius:2px;background:var(--trait);
display:block}
.jauge i.on{background:var(--vert)}
.spec{background:#fff;border:1px solid var(--trait);border-radius:10px;
padding:18px 20px;margin-bottom:12px}
.spec .ex{display:block;color:var(--encre)}
.spec .det{font-family:"PlexMono";font-size:11px;color:var(--ardoise);margin-top:8px}
.ar{font-family:"PlexAr","Plex",sans-serif;direction:rtl;text-align:right}
.interdit{display:flex;gap:11px;font-size:14px;align-items:flex-start}
.interdit .x{color:var(--vert);font-weight:600;flex:none}
.avert{background:var(--voile);border:1px solid var(--pale);
border-left:4px solid var(--vert);border-radius:8px;padding:16px 18px;
font-size:14px;max-width:74ch}
.avert>b:first-child{display:block;margin-bottom:5px}
.zp{background:#fff;border:1px solid var(--trait);border-radius:10px;padding:26px;
display:flex;gap:34px;align-items:center;flex-wrap:wrap}
footer{padding:40px 0 64px;color:var(--ardoise);font-size:13px}
ul{max-width:70ch}li{margin:5px 0}
''' % (NUIT, FORET, VERT, VIF, CLAIR, PALE, VOILE, PAPIER, ENCRE, ARDOISE, TRAIT))
	a('</style></head><body>')

	# --- En-tete
	a('<header><div class="env">'
	  '<div><img src="logo/algerie2036-principal-blanc.svg" alt="Algérie 2036">'
	  '</div>'
	  '<div class="meta">Charte graphique<br>Version %s — %s<br>'
	  'Vert et blanc exclusivement<br>JNCORP INC.</div>'
	  '</div></header>' % (VERSION, DATE))

	a('<div class="env">')

	# --- 1. La marque
	a('<section><h2><span class="num">01</span>La marque</h2>')
	a('<p class="chapo">Trois frondes montent d’un socle commun et se '
	  'rejoignent en pointe. C’est l’abstraction du monument d’Alger que vous '
	  'm’avez envoyé — pas son dessin. Les trois branches se lisent aussi '
	  'comme trois pales, ce qui rattache le signe au volet énergies '
	  'renouvelables de la plateforme, et le fût central comme une colonne qui '
	  's’élève : la donnée qui monte du territoire.</p>')

	a('<div class="avert"><b>Une précaution, et elle est sérieuse.</b>'
	  'Le monument dont vient la silhouette est un mémorial national. Le signe '
	  'livré est une abstraction géométrique, redessinée au trait — aucune '
	  'photographie, aucun décalque. Il ne doit jamais être accolé au drapeau, '
	  'au sceau ou aux armoiries de l’État, et la plateforme ne doit jamais se '
	  'présenter comme un site officiel. Si un jour Algérie 2036 se rapproche '
	  'd’une institution publique, l’usage du signe devra être validé par elle '
	  'avant toute diffusion.</div>')

	a('<h3>Les déclinaisons</h3>')
	a('<p style="font-size:14px;color:var(--ardoise);margin:-4px 0 14px">'
	  'La version que vous avez entourée — le signe blanc sur aplat vert — est '
	  'la <b>version de référence</b> : c’est elle qui ouvre ce document, et '
	  'c’est elle par défaut en en-tête de site, en couverture de document et '
	  'en avatar.</p>')
	a('<div class="grille g3">')
	for f, lab, fond, haut in LOGOS:
		a('<div class="logo-case %s">'
		  '<div style="height:%dpx;display:flex;align-items:center;'
		  'justify-content:center">'
		  '<img src="logo/%s" alt="%s" style="max-height:%dpx">'
		  '</div><div class="lab">%s</div></div>'
		  % ('sombre' if fond == 'sombre' else '', haut, f, lab, haut, lab))
	a('</div>')
	a('<p style="font-size:13px;color:var(--ardoise);margin-top:14px">'
	  'Tous les fichiers sont en SVG, texte compris : le nom est converti en '
	  'tracés, donc le logo s’affiche à l’identique sur une machine où la '
	  'police n’est pas installée. Le signe seul pèse '
	  '<span class="mono">%d</span> octets.</p>'
	  % os.path.getsize(os.path.join(RACINE, 'logo', 'algerie2036-marque.svg')))

	a('<h3>Zone de protection et tailles minimales</h3>')
	a('<div class="zp">'
	  '<div style="position:relative;padding:26px;background:var(--voile);'
	  'border-radius:8px"><img src="logo/algerie2036-marque.svg" '
	  'style="height:104px;display:block"></div>'
	  '<div style="font-size:14px;max-width:46ch">'
	  '<p style="margin:0 0 10px"><b>Zone de protection :</b> un quart de la '
	  'hauteur du signe, sur les quatre côtés. Rien n’entre dedans — ni texte, '
	  'ni filet, ni bord de page.</p>'
	  '<p style="margin:0"><b>Tailles minimales :</b> signe seul '
	  '<span class="mono">24</span> px à l’écran et '
	  '<span class="mono">8</span> mm à l’impression ; verrou horizontal '
	  '<span class="mono">140</span> px ; en dessous, on passe à la pastille, '
	  'qui reste lisible à <span class="mono">16</span> px.</p>'
	  '</div></div>')

	a('<h3>Ce qu’on ne fait pas</h3><div class="grille g2">')
	for titre, det in INTERDITS:
		a('<div class="carte interdit"><span class="x">✕</span><span>'
		  '<b>%s</b><br><span style="color:var(--ardoise)">%s</span></span></div>'
		  % (titre, det))
	a('</div></section>')

	# --- 2. Couleurs
	a('<section><h2><span class="num">02</span>Les couleurs</h2>')
	a('<p class="chapo">Vert et blanc <b>exclusivement</b>. Il n’y a qu’une '
	  'teinte dans toute la charte : le vert. Ce que vous prendrez pour des '
	  'gris — le texte, les filets, les fonds de section — sont des verts '
	  'désaturés, pas des gris neutres ; un gris pur introduirait une seconde '
	  'teinte et le système ne serait plus vrai. Chaque rapport de contraste '
	  'ci-dessous est <b>calculé</b> à partir des couleurs elles-mêmes '
	  '(formule WCAG 2.1), il n’est pas estimé.</p>')

	a('<h3>Primaires</h3><div class="grille g2">')
	for nom, hexa, usage in PRIMAIRES:
		a(case_couleur(nom, hexa, usage))
	a('</div>')

	a('<h3>Neutres — qui sont des verts</h3><div class="grille g2">')
	for nom, hexa, usage in NEUTRES:
		a(case_couleur(nom, hexa, usage))
	a('</div>')

	a('<h3>L’échelle de valeurs</h3>')
	a('<p>Puisqu’il n’y a qu’une teinte, c’est la <b>valeur</b> — le clair et '
	  'le sombre — qui hiérarchise. Sept crans, nommés V1 à V7, et c’est le '
	  'vocabulaire utilisé partout ailleurs dans ce document.</p>')
	a('<div class="ech">')
	for code, hexa, nom in VALEURS:
		clair = contraste(BLANC, hexa) >= 4.5
		a('<div style="background:%s;color:%s">%s</div>'
		  % (hexa, BLANC if clair else ENCRE, code))
	a('</div>')
	a('<table style="margin-top:14px"><thead><tr><th>Cran</th><th>Nom</th>'
	  '<th>Hex</th><th>Sur blanc</th><th>Texte posé dessus</th></tr></thead>'
	  '<tbody>')
	for code, hexa, nom in VALEURS:
		r = contraste(hexa, BLANC)
		sur = contraste(BLANC, hexa)
		a('<tr><td class="n">%s</td><td>%s</td><td class="n">%s</td>'
		  '<td class="n">%.2f:1</td><td class="n">%s</td></tr>'
		  % (code, nom, hexa, r, 'blanc' if sur >= 4.5 else 'encre'))
	a('</tbody></table>')

	a('<div class="avert" style="margin-top:22px"><b>Une exception à décider — '
	  'et c’est votre décision, pas la mienne.</b>'
	  'Une contrainte « vert et blanc exclusivement » supprime le rouge. Sur '
	  'une page vitrine, aucun problème. Dans un formulaire, le rouge est le '
	  'signal universel d’une saisie refusée, et un utilisateur pressé le '
	  'cherche. La charte tient donc la règle : <b>pas de rouge</b>, et une '
	  'erreur se signale par un cadre en Vert nuit épaissi à 2 px, un signe '
	  '<span class="mono">✕</span>, et la phrase qui dit quoi corriger — '
	  'jamais par la couleur seule, ce qui est de toute façon la bonne '
	  'pratique. Si vous préférez rouvrir une couleur d’alerte unique, dites-le '
	  'et je l’ajoute comme <b>exception écrite</b>, réservée aux erreurs de '
	  'formulaire et aux actions destructrices, interdite en communication.'
	  '</div>')

	a('<div class="avert" style="margin-top:14px"><b>Impression</b>'
	  'Les valeurs données sont des valeurs écran (RVB / hexadécimal), '
	  'mesurées. Je ne donne pas d’équivalent CMJN ni de référence Pantone : '
	  'une conversion dépend du papier et du profil de l’imprimeur, et un '
	  'chiffre inventé ici deviendrait un vert faux sur la première brochure. '
	  'Votre imprimeur cale les équivalents sur ces valeurs et vous renvoie un '
	  'BAT — à ce moment-là je les ajoute à la charte.</div>')
	a('</section>')

	# --- 3. Les couches de la carte
	a('<section><h2><span class="num">03</span>Les quinze couches de la carte</h2>')
	a('<p class="chapo">C’est le point dur de la contrainte, et il vaut d’être '
	  'expliqué. Une carte à quinze couches se lit normalement par la '
	  '<b>teinte</b> : le bleu pour les ports, l’orange pour le solaire. Une '
	  'charte vert et blanc supprime cette possibilité — et quinze verts '
	  'différents seraient indistinguables, surtout superposés à 55 % '
	  'd’opacité.</p>')
	a('<p>La solution retenue : chaque couche est identifiée par un '
	  '<b>motif</b>, pas par une couleur. Quinze motifs distincts, un '
	  '<b>code de deux lettres</b> et le <b>nom écrit</b> dans la légende. La '
	  'valeur (V1 à V5) ne sert qu’à hiérarchiser, jamais à identifier seule : '
	  'deux couches peuvent partager une valeur, jamais un motif.</p>')
	a('<p><b>Ce que ça gagne :</b> le système survit à l’impression noir et '
	  'blanc, à un photocopieur, à un lecteur daltonien et à une capture '
	  'd’écran dégradée. Une carte thématique en monochrome n’est pas un '
	  'pis-aller — c’est la tradition cartographique la plus ancienne, et la '
	  'plus robuste.</p>')

	a('<div class="grille g2">')
	for famille, items in COUCHES:
		a('<div class="carte"><h3 style="margin:0 0 8px;font-size:13px;'
		  'letter-spacing:.08em;text-transform:uppercase;color:var(--ardoise)">'
		  '%s</h3>' % famille)
		for code, nom, mot, coul in items:
			cran = dict((c, k) for k, c, _n in VALEURS)[coul]
			a('<div class="couche">'
			  '<span class="sw" style="%s"></span>'
			  '<span class="code">%s</span>'
			  '<span>%s</span>'
			  '<span class="h">%s · %s</span>'
			  '</div>' % (motif(mot, coul), code, nom, mot, cran))
		a('</div>')
	a('</div>')
	a('<p style="font-size:13px;color:var(--ardoise);margin-top:12px">'
	  'Sur la carte, la règle des libellés ne change jamais : <b>les noms de '
	  'lieux sont en Encre avec un halo blanc de 2 px</b>, jamais en blanc sur '
	  'une couche — c’est la seule façon qu’un nom de wilaya reste lisible '
	  'quand quatre couches se superposent.</p>')

	a('<h3>Trois règles de superposition</h3><ul>'
	  '<li><b>Une seule couche est « active » à la fois.</b> Elle se dessine en '
	  'V3 ou V4 à pleine opacité ; les autres couches allumées retombent en V6 '
	  'à 45 %. Sans cette règle, quatre motifs à la même force donnent une '
	  'texture illisible.</li>'
	  '<li><b>Trois couches simultanées au maximum.</b> Au-delà, l’interface '
	  'propose la comparaison côte à côte plutôt que la superposition. Ce n’est '
	  'pas une limite technique, c’est une limite de lecture.</li>'
	  '<li><b>La légende affiche le motif, le code et le nom</b> — les trois, '
	  'toujours. Une couche allumée sans sa ligne de légende est un bogue.</li>'
	  '</ul>')
	a('</section>')

	# --- 4. Typographie
	a('<section><h2><span class="num">04</span>La typographie</h2>')
	a('<p class="chapo">Une seule famille pour les trois langues : '
	  '<b>IBM Plex</b>. Sa version arabe est dessinée par les mêmes auteurs et '
	  'au même rythme que la latine — l’arabe n’est donc pas une police de '
	  'remplacement posée à côté, c’est la même voix. Licence libre (OFL), '
	  'donc hébergeable sur vos serveurs : aucune requête vers un service '
	  'extérieur à chaque page.</p>')

	a('<div class="grille g3" style="margin-bottom:26px">')
	for nom, ex, style in [
		('IBM Plex Sans', 'Wilaya · Port · Corridor', 'font:600 26px "Plex"'),
		('IBM Plex Sans Arabic', 'الجزائر · ميناء · ولاية',
		 'font:600 26px "PlexAr";direction:rtl'),
		('IBM Plex Mono', '58 wilayas · 87/100', 'font:400 22px "PlexMono"'),
	]:
		a('<div class="carte"><div style="%s">%s</div>'
		  '<div style="font-size:12px;color:var(--ardoise);margin-top:12px">%s</div>'
		  '</div>' % (style, ex, nom))
	a('</div>')

	a('<h3>L’échelle</h3><table><thead><tr><th>Rôle</th><th>Taille</th>'
	  '<th>Interligne</th><th>Graisse</th><th>Famille</th><th>Emploi</th>'
	  '</tr></thead><tbody>')
	for role, taille, inter, poids, fam, emploi in ECHELLE:
		a('<tr><td><b>%s</b></td><td class="n">%d px</td><td class="n">%s</td>'
		  '<td class="n">%d</td><td>%s</td><td>%s</td></tr>'
		  % (role, taille, inter, poids, fam, emploi))
	a('</tbody></table>')

	a('<h3>Trois règles</h3><ul>'
	  '<li><b>Tout chiffre destiné à être comparé passe en Plex Mono</b>, '
	  'chiffres à chasse fixe. Une colonne de surfaces ou de scores doit '
	  's’aligner à la virgule : sinon l’œil compare des longueurs, pas des '
	  'valeurs.</li>'
	  '<li><b>Le corps ne descend jamais sous 16 px</b> dans les pages, ni sous '
	  '12 px dans les légendes de carte.</li>'
	  '<li><b>En arabe, la page entière passe en <code>dir="rtl"</code></b>, '
	  'y compris la carte : légende, panneau de couches et fiche territoire '
	  'basculent à droite. On utilise les propriétés logiques du CSS '
	  '(<code>margin-inline-start</code>, <code>padding-inline</code>) pour '
	  'qu’une seule feuille de style serve les trois langues.</li>'
	  '</ul>')
	a('<div class="carte ar" style="margin-top:16px">'
	  '<div style="font:600 21px \'PlexAr\'">الجزائر 2036 — منصة الاستشراف الوطني</div>'
	  '<div style="font-size:14px;color:var(--ardoise);margin-top:6px">'
	  'ولاية · ميناء · مركز بيانات · منطقة حرة · طاقات متجددة</div></div>')
	a('</section>')

	# --- 5. Statut de la donnee
	a('<section><h2><span class="num">05</span>Le statut de la donnée</h2>')
	a('<p class="chapo">C’est la partie de la charte qui protège le projet. '
	  'Votre cahier des charges pose la règle : '
	  '<b>FACTS ≠ TARGETS ≠ PROJECTIONS</b>. Une charte graphique doit la '
	  'rendre visible, sinon elle reste une intention. Trois états, et ils ne '
	  'se distinguent <b>jamais par la couleur seule</b> : motif, bordure, '
	  'signe et mot écrit. C’était vrai en v1.0 ; en vert et blanc, ça devient '
	  'la seule mécanique possible — donc elle est encore plus solide.</p>')

	a('<div class="grille g3">')
	a('<div class="statut"><div class="demo" style="background:%s"></div>'
	  '<div class="txt"><b>Fait</b>'
	  '<span>Donnée constatée. Elle porte obligatoirement sa source et sa '
	  'date.</span>'
	  '<span class="regle">aplat plein · bordure pleine · ● Fait</span>'
	  '</div></div>' % VERT)
	a('<div class="statut"><div class="demo" style="background:%s;'
	  'border-bottom:1px solid %s"></div>'
	  '<div class="txt"><b>Objectif 2036</b>'
	  '<span>Cible publiquement adoptée. Ce n’est pas un constat, c’est une '
	  'intention datée.</span>'
	  '<span class="regle">aplat V6 · bordure pleine · ◎ Objectif</span>'
	  '</div></div>' % (PALE, VERT))
	a('<div class="statut"><div class="demo" style="%s;'
	  'border-bottom:1px dashed %s"></div>'
	  '<div class="txt"><b>Scénario</b>'
	  '<span>Hypothèse de travail. <b>N’a été adoptée par personne</b> et ne '
	  'doit jamais être présentée comme une décision.</span>'
	  '<span class="regle">hachures 45° · bordure tiretée · ◇ Scénario</span>'
	  '</div></div>' % (motif('rayons', VERT), VERT))
	a('</div>')

	a('<h3>Les pastilles, telles qu’elles apparaissent</h3>')
	a('<p><span class="badge" style="background:%s;color:#fff">'
	  '● Fait</span> &nbsp; '
	  '<span class="badge" style="background:%s;color:%s">'
	  '◎ Objectif 2036</span> &nbsp; '
	  '<span class="badge" style="%s;background-color:#fff;color:%s;'
	  'box-shadow:inset 0 0 0 1px %s">◇ Scénario</span></p>'
	  % (VERT, PALE, ENCRE, motif('rayons', PALE), ENCRE, CLAIR))

	a('<h3>La ligne de source</h3>')
	a('<p>Sous chaque chiffre publié, une ligne en 12 px Ardoise, dans cet '
	  'ordre exact :</p>')
	a('<div class="spec"><span class="ex mono">'
	  'Source — Nom de l’organisme · publié le JJ/MM/AAAA · relevé le JJ/MM/AAAA'
	  '</span><span class="det">Si la source manque, le champ affiche '
	  '« non renseigné » en Ardoise. Il ne reste jamais vide, et il ne se '
	  'remplit jamais d’une estimation.</span></div>')
	a('</section>')

	# --- 6. Les scores
	a('<section><h2><span class="num">06</span>Les scores sur 100</h2>')
	a('<p class="chapo">Data Center Readiness Score, Free Zone Potential '
	  'Score, Port-Digital Synergy Score : trois indicateurs, une seule '
	  'écriture. Sans le rouge et le orange, le niveau ne peut plus être porté '
	  'par la teinte — il l’est par la <b>valeur</b>, doublée d’une '
	  '<b>jauge à quatre crans</b> et du <b>nombre toujours écrit</b>. Trois '
	  'signaux pour une information : c’est volontaire.</p>')
	a('<div class="grille g4">')
	for plage, nom, fond, texte, crans in SCORES:
		val = plage.split('–')[1].strip()
		jauge = ''.join('<i class="%s"></i>' % ('on' if i < crans else '')
		                for i in range(4))
		a('<div class="score"><div class="val" style="background:%s;color:%s">'
		  '%s</div><div><b>%s</b><div class="mono" style="font-size:12px;'
		  'color:var(--ardoise)">%s</div><div class="jauge">%s</div></div>'
		  '</div>' % (fond, texte, val, nom, plage, jauge))
	a('</div>')
	a('<p style="margin-top:18px"><b>Et une règle de fond :</b> un score '
	  'affiché ouvre toujours le détail de son calcul — les critères, leur '
	  'poids, et la donnée manquante quand il y en a une. Un score dont les '
	  'critères ne sont pas consultables est un avis déguisé en mesure. '
	  'Quand un critère manque, le score n’est pas calculé « au mieux » : il '
	  'affiche <span class="mono">incomplet</span> et dit lequel manque.</p>')
	a('</section>')

	# --- 7. La carte
	a('<section><h2><span class="num">07</span>La carte</h2>')
	a('<p class="chapo">La carte est l’écran principal du produit ; sa mise en '
	  'forme fait donc partie de la charte, pas du développement.</p>')
	a('<ul>'
	  '<li><b>Fond blanc, presque vide.</b> Papier <code>%s</code>, eau '
	  '<code>%s</code>, frontières <code>%s</code> en 1 px. En monochrome, le '
	  'fond doit être encore plus discret qu’en couleur : c’est lui qui donne '
	  'aux motifs la place de se lire.</li>'
	  '<li><b>Une couche = un motif</b>, jamais une teinte. Traits à 2 px, '
	  'points à 8 px, aplats à 55 %% d’opacité pour la couche active, 45 %% '
	  'pour les couches secondaires.</li>'
	  '<li><b>Sélection</b> en Vert 2036, halo Voile de 4 px, plus un liseré '
	  'de 2 px. Le survol ajoute le liseré seul — jamais un changement de '
	  'motif, qui ferait croire à un changement de nature.</li>'
	  '<li><b>Légende obligatoire et toujours visible</b>, avec motif + code + '
	  'nom.</li>'
	  '<li><b>Échelle et source du fond de carte</b> en bas à droite, en '
	  '12 px, sur toutes les vues, y compris les captures exportées.</li>'
	  '<li><b>Le mode nuit</b> inverse : fond Vert nuit, motifs en V6 et blanc. '
	  'Les motifs ne changent pas — seule la valeur s’inverse, sinon la carte '
	  'de nuit et celle de jour ne se lisent plus de la même façon.</li>'
	  '</ul>' % (PAPIER, VOILE, TRAIT))
	a('</section>')

	# --- 8. Composants
	a('<section><h2><span class="num">08</span>Quelques composants</h2>')
	a('<div class="grille g2">')
	a('<div class="carte"><h3 style="margin-top:0">Boutons</h3>'
	  '<p style="margin:0 0 12px"><span style="display:inline-block;'
	  'background:%s;color:#fff;border-radius:8px;padding:11px 20px;'
	  'font-weight:600;font-size:14px">Analyser ce territoire</span>&nbsp;&nbsp;'
	  '<span style="display:inline-block;background:#fff;color:%s;'
	  'border:1px solid %s;border-radius:8px;padding:10px 19px;'
	  'font-weight:600;font-size:14px">Comparer</span></p>'
	  '<div class="mono" style="font-size:11px;color:var(--ardoise)">'
	  'rayon 8 px · hauteur 44 px · libellé 14 px / 600<br>'
	  'zone tactile minimale 44 × 44 px</div></div>' % (VERT, VERT, VERT))
	a('<div class="carte"><h3 style="margin-top:0">Fiche territoire</h3>'
	  '<div style="border:1px solid var(--trait);border-radius:8px;'
	  'overflow:hidden">'
	  '<div style="background:%s;color:#fff;padding:12px 14px;font-weight:600">'
	  'Wilaya — <span style="opacity:.75;font-weight:400">nom</span></div>'
	  '<div style="padding:12px 14px;font-size:13px">'
	  '<div style="display:flex;justify-content:space-between;'
	  'border-bottom:1px solid var(--trait);padding:7px 0">'
	  '<span style="color:var(--ardoise)">Population</span>'
	  '<span class="mono">non renseigné</span></div>'
	  '<div style="display:flex;justify-content:space-between;padding:7px 0">'
	  '<span style="color:var(--ardoise)">Puissance disponible</span>'
	  '<span class="mono">non renseigné</span></div>'
	  '</div></div>'
	  '<div class="mono" style="font-size:11px;color:var(--ardoise);'
	  'margin-top:10px">Un champ sans donnée s’écrit « non renseigné ».<br>'
	  'Il ne se remplit pas d’une estimation.</div></div>' % NUIT)
	a('<div class="carte"><h3 style="margin-top:0">Champ en erreur — '
	  'sans rouge</h3>'
	  '<div style="border:2px solid %s;border-radius:8px;padding:10px 12px;'
	  'font-size:14px;color:var(--ardoise)">contact@…</div>'
	  '<div style="margin-top:8px;font-size:13px;color:%s">'
	  '<b class="sg">✕</b> Adresse incomplète — il manque le domaine '
	  'après le <span class="mono">@</span>.</div>'
	  '<div class="mono" style="font-size:11px;color:var(--ardoise);'
	  'margin-top:10px">bordure 2 px V1 · signe ✕ · phrase qui dit quoi '
	  'corriger.<br>Trois signaux, aucun n’est la couleur.</div></div>'
	  % (NUIT, ENCRE))
	a('<div class="carte"><h3 style="margin-top:0">Légende de carte</h3>')
	for code, nom, mot, coul in [COUCHES[0][1][0], COUCHES[1][1][0],
	                             COUCHES[2][1][0]]:
		a('<div class="couche"><span class="sw" style="%s"></span>'
		  '<span class="code">%s</span><span>%s</span></div>'
		  % (motif(mot, coul), code, nom))
	a('<div class="mono" style="font-size:11px;color:var(--ardoise);'
	  'margin-top:10px">Motif, code, nom. Les trois, toujours.</div></div>')
	a('</div></section>')

	# --- 9. Accessibilite
	a('<section><h2><span class="num">09</span>Accessibilité</h2>')
	lignes = [
		('Encre sur blanc', ENCRE, BLANC),
		('Ardoise sur blanc', ARDOISE, BLANC),
		('Blanc sur Vert Algérie', BLANC, VERT),
		('Blanc sur Vert nuit', BLANC, NUIT),
		('Blanc sur Vert forêt', BLANC, FORET),
		('Vert Algérie sur blanc', VERT, BLANC),
		('Vert 2036 sur blanc', VIF, BLANC),
		('Blanc sur Vert 2036', BLANC, VIF),
		('Encre sur Voile', ENCRE, VOILE),
		('Encre sur Vert pâle', ENCRE, PALE),
	]
	a('<table><thead><tr><th>Association</th><th>Rapport mesuré</th>'
	  '<th>Niveau WCAG 2.1</th><th>Verdict</th></tr></thead><tbody>')
	for nom, av, ar in lignes:
		r = contraste(av, ar)
		verdict, signe = note(r)
		a('<tr><td>%s</td><td class="n">%.2f:1</td><td class="n">%s</td>'
		  '<td><span class="sg">%s</span> %s</td></tr>'
		  % (nom, r, verdict, signe,
		     'texte courant' if r >= 4.5 else
		     ('titres ≥ 24 px seulement' if r >= 3.0 else 'décoratif uniquement')))
	a('</tbody></table>')
	a('<p style="margin-top:16px">Le seul couple à surveiller est le '
	  '<b>Vert 2036 sur blanc</b>. Il est retenu pour les liens et les états '
	  'actifs, pas pour du texte courant ; en texte de lien, il est '
	  'systématiquement souligné, de sorte que le lien reste identifiable sans '
	  'la couleur. Le verdict de chaque ligne est doublé d’un signe '
	  '<span class="mono">✓ △ ✕</span> : dans un document vert et blanc, un '
	  'verdict ne peut pas être porté par une couleur d’alerte, il n’y en a '
	  'plus.</p>')
	a('<p><b>Une conséquence directe de la contrainte, et elle est bonne :</b> '
	  'un système monochrome est par construction inaccessible au daltonisme… '
	  'ou totalement accessible, selon qu’il s’appuie ou non sur la teinte. '
	  'Comme rien ici ne repose sur la teinte — ni les couches, ni les statuts, '
	  'ni les scores, ni les erreurs — la charte v%s est plus robuste que la '
	  'v1.0 sur ce point précis.</p>' % VERSION)
	a('</section>')

	# --- 10. Fichiers
	a('<section><h2><span class="num">10</span>Ce qui est livré</h2>')
	a('<ul>'
	  '<li><code>logo/</code> — 10 fichiers SVG (horizontal, vertical, arabe, '
	  'signe seul, monochromes, pastille), texte converti en tracés.</li>'
	  '<li><code>logo/png/</code> — les mêmes en PNG à fond transparent, pour '
	  'les outils qui ne lisent pas le SVG. Le SVG reste la référence.</li>'
	  '<li><code>polices/</code> — IBM Plex Sans, Sans Arabic et Mono, sous '
	  'licence OFL, à héberger sur le serveur.</li>'
	  '<li><code>charte.html</code> — ce document, à ouvrir dans un navigateur '
	  'ou à imprimer en PDF.</li>'
	  '<li><code>outils/marque.py</code> — le générateur du logo. Le tracé des '
	  'trois frondes est écrit une seule fois ; toutes les déclinaisons en '
	  'découlent.</li>'
	  '<li><code>outils/charte.py</code> — le générateur de ce document. Les '
	  'contrastes sont calculés, pas saisis, et les quinze motifs de carte y '
	  'sont définis une seule fois : ils sont donc reproductibles à '
	  'l’identique dans le code du site.</li>'
	  '</ul>')
	a('</section>')

	a('</div>')
	a('<footer><div class="env">ALGÉRIE 2036 — charte graphique v%s · %s · '
	  'vert et blanc exclusivement · document de travail, à faire évoluer avec '
	  'la plateforme.</div></footer>' % (VERSION, DATE))
	a('</body></html>')
	return '\n'.join(h)


def main():
	sortie = os.path.join(RACINE, 'charte.html')
	contenu = page()
	with open(sortie, 'w') as f:
		f.write(contenu)
	print('%s — %d octets' % (sortie, len(contenu)))
	return 0


if __name__ == '__main__':
	sys.exit(main())
