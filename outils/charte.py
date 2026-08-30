#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere charte.html.

Les rapports de contraste ne sont pas ecrits a la main : ils sont CALCULES
ici (formule WCAG 2.1) a partir des couleurs elles-memes. Un vert qu'on
retouche change le chiffre affiche dans la charte, sans intervention.
"""

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


# --- La palette -----------------------------------------------------------

BLANC = '#FFFFFF'
PAPIER = '#F7FAF8'
ENCRE = '#0B1F17'
VERT = '#006233'
VERT_VIF = '#0F8C4C'
VERT_PROFOND = '#04331F'

PRIMAIRES = [
	('Vert Algérie', VERT, 'La couleur de la marque. Logo, en-têtes, boutons '
	 'principaux, éléments actifs.'),
	('Blanc', BLANC, 'La respiration. Fond de toutes les pages de contenu et '
	 'des cartes.'),
	('Vert 2036', VERT_VIF, 'L’accent vivant : liens, sélection sur la carte, '
	 'états de survol, la fronde centrale du logo.'),
	('Vert profond', VERT_PROFOND, 'Bandeaux sombres, pied de page, fonds de '
	 'carte en mode nuit.'),
]

NEUTRES = [
	('Encre', ENCRE, 'Texte courant.'),
	('Ardoise', '#5B6B64', 'Texte secondaire, légendes, unités.'),
	('Trait', '#D8E2DC', 'Filets, bordures de tableaux, séparateurs.'),
	('Papier', PAPIER, 'Fond d’application, fond de carte clair.'),
	('Vert pâle', '#E6F4EC', 'Fonds de section, ligne de tableau survolée, '
	 'halo de sélection.'),
]

# Les couches de la carte. Regle : le vert de marque n'est JAMAIS une couche —
# sinon on ne distingue plus l'interface de la donnee.
COUCHES = [
	('Infrastructures', [
		('Ports & maritime', '#0B5FA5'),
		('Rail & routes', '#4A5A66'),
		('Numérique, fibre & data centers', '#00757E'),
		('Eau, barrages & dessalement', '#1A7E9C'),
	]),
	('Énergie', [
		('Solaire', '#A36200'),
		('Éolien', '#2E9BD6'),
		('Hydrogène vert', '#6B34C7'),
		('Énergie conventionnelle', '#8C6B3F'),
	]),
	('Économie', [
		('Zones franches', '#A8176F'),
		('Industrie & corridors', '#A8471C'),
		('Capital humain & universités', '#5B44B0'),
	]),
	('Territoire & environnement', [
		('Forêt & Barrage vert', '#3E7C2A'),
		('Agriculture', '#647D18'),
		('Urbanisme & villes', '#6E6259'),
		('Risques & contraintes', '#B32020'),
	]),
]

SCORES = [
	('0 – 39', 'Faible', '#B32020'),
	('40 – 59', 'Moyen', '#B36B00'),
	('60 – 79', 'Bon', VERT_VIF),
	('80 – 100', 'Élevé', VERT),
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
	('Ne pas recolorer', 'Vert Algérie, blanc, ou encre. Rien d’autre.'),
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
	('algerie2036-principal.svg', 'Principal — horizontal', 'clair', 64),
	('algerie2036-principal-blanc.svg', 'Principal — sur fond sombre', 'sombre', 64),
	('algerie2036-vertical.svg', 'Vertical', 'clair', 96),
	('algerie2036-arabe.svg', 'Arabe — الجزائر 2036', 'clair', 64),
	('algerie2036-marque.svg', 'Signe seul', 'clair', 84),
	('algerie2036-marque-noire.svg', 'Monochrome encre', 'clair', 84),
	('algerie2036-marque-blanche.svg', 'Monochrome blanc', 'sombre', 84),
	('algerie2036-pastille.svg', 'Pastille — favicon, application', 'clair', 84),
]


# --- Fabrication ----------------------------------------------------------

def note(r):
	"""Verdict WCAG mesure, pas devine."""
	if r >= 7.0:
		return 'AAA', 'ok'
	if r >= 4.5:
		return 'AA', 'ok'
	if r >= 3.0:
		return 'AA gros texte', 'moyen'
	return 'décoratif', 'non'


def case_couleur(nom, hexa, usage, fond=BLANC):
	r = contraste(hexa, fond)
	verdict, cls = note(r)
	rv, gv, bv = rgb(hexa)
	bordure = ' style="box-shadow:inset 0 0 0 1px #D8E2DC"' if contraste(hexa, BLANC) < 1.25 else ''
	return (
		'<div class="cc">'
		'<div class="cc-p" style="background:%s"%s></div>'
		'<div class="cc-t"><b>%s</b>'
		'<code>%s</code>'
		'<span class="mono">R %d · V %d · B %d</span>'
		'<span class="use">%s</span>'
		'<span class="ratio %s">%.2f:1 sur blanc — %s</span>'
		'</div></div>'
	) % (hexa, bordure, nom, hexa, rv, gv, bv, usage, cls, r, verdict)


def page():
	h = []
	a = h.append

	a('<!doctype html><html lang="fr"><head><meta charset="utf-8">')
	a('<meta name="viewport" content="width=device-width,initial-scale=1">')
	a('<title>ALGÉRIE 2036 — Charte graphique v1.0</title>')
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
:root{--vert:%s;--vif:%s;--profond:%s;--encre:%s;--ardoise:#5B6B64;
--trait:#D8E2DC;--papier:%s;--pale:#E6F4EC}
*{box-sizing:border-box}
body{margin:0;background:var(--papier);color:var(--encre);
font:400 16px/1.6 "Plex",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.mono,code{font-family:"PlexMono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
.env{max-width:1080px;margin:0 auto;padding:0 28px}
header{background:var(--profond);color:#fff;padding:56px 0 48px}
header .env{display:flex;align-items:flex-end;justify-content:space-between;gap:28px;flex-wrap:wrap}
header img{height:92px}
header .meta{font-size:13px;line-height:1.7;opacity:.82;text-align:right}
h1{font:600 13px/1.3 "Plex";letter-spacing:.14em;text-transform:uppercase;margin:0 0 6px;opacity:.7}
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
.g4{grid-template-columns:repeat(auto-fill,minmax(178px,1fr))}
.carte{background:#fff;border:1px solid var(--trait);border-radius:10px;padding:18px}
.logo-case{background:#fff;border:1px solid var(--trait);border-radius:10px;
padding:22px;text-align:center}
.logo-case.sombre{background:var(--profond);border-color:var(--profond)}
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
.ratio{font-family:"PlexMono";font-size:11px;margin-top:4px}
.ratio.ok{color:#0F6B3C}.ratio.moyen{color:#8A5A00}.ratio.non{color:#8C2020}
table{border-collapse:collapse;width:100%%;font-size:14px;background:#fff}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--trait);
vertical-align:top}
th{font:600 12px/1.3 "Plex";letter-spacing:.08em;text-transform:uppercase;
color:var(--ardoise);background:var(--pale)}
td.n{font-family:"PlexMono";font-variant-numeric:tabular-nums;white-space:nowrap}
.couche{display:flex;align-items:center;gap:10px;font-size:14px;padding:9px 0;
border-bottom:1px solid var(--trait)}
.couche:last-child{border:0}
.pip{width:22px;height:22px;border-radius:5px;flex:none}
.couche .h{margin-left:auto;font-family:"PlexMono";font-size:11px;color:var(--ardoise)}
.statut{border:1px solid var(--trait);border-radius:10px;overflow:hidden;background:#fff}
.statut .demo{height:96px}
.statut .txt{padding:15px}
.statut .txt b{display:block;font-size:15px}
.statut .txt span{font-size:13px;color:var(--ardoise);display:block;margin-top:5px}
.statut .txt .regle{font-family:"PlexMono";font-size:11px;color:var(--encre);
margin-top:9px;display:block}
.badge{display:inline-flex;align-items:center;gap:7px;border-radius:999px;
padding:5px 12px;font-size:12px;font-weight:600;letter-spacing:.04em}
.score{display:flex;align-items:center;gap:12px;background:#fff;
border:1px solid var(--trait);border-radius:10px;padding:14px}
.score .val{font-family:"PlexMono";font-weight:600;font-size:26px;color:#fff;
width:64px;height:64px;border-radius:12px;display:flex;align-items:center;
justify-content:center;flex:none}
.spec{background:#fff;border:1px solid var(--trait);border-radius:10px;
padding:18px 20px;margin-bottom:12px}
.spec .ex{display:block;color:var(--encre)}
.spec .det{font-family:"PlexMono";font-size:11px;color:var(--ardoise);margin-top:8px}
.ar{font-family:"PlexAr","Plex",sans-serif;direction:rtl;text-align:right}
.interdit{display:flex;gap:11px;font-size:14px;align-items:flex-start}
.interdit .x{color:#B32020;font-weight:600;flex:none}
.avert{background:#FFF6E8;border:1px solid #E8C98A;border-left:4px solid #B36B00;
border-radius:8px;padding:16px 18px;font-size:14px;max-width:74ch}
.avert b{display:block;margin-bottom:5px}
.zp{background:#fff;border:1px solid var(--trait);border-radius:10px;padding:26px;
display:flex;gap:34px;align-items:center;flex-wrap:wrap}
footer{padding:40px 0 64px;color:var(--ardoise);font-size:13px}
ul{max-width:70ch}li{margin:5px 0}
''' % (VERT, VERT_VIF, VERT_PROFOND, ENCRE, PAPIER))
	a('</style></head><body>')

	# --- En-tete
	a('<header><div class="env">'
	  '<div><img src="logo/algerie2036-principal-blanc.svg" alt="Algérie 2036">'
	  '</div>'
	  '<div class="meta">Charte graphique<br>Version 1.0 — 30 août 2026<br>'
	  'JNCORP INC.</div>'
	  '</div></header>')

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
	  '<div style="position:relative;padding:26px;background:var(--pale);'
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
	a('<p class="chapo">Vert et blanc, comme demandé. Le vert porte la marque, '
	  'le blanc porte la donnée : sur une carte à quinze couches, c’est le '
	  'blanc qui rend l’information lisible. Chaque rapport de contraste '
	  'ci-dessous est <b>calculé</b> à partir des couleurs elles-mêmes '
	  '(formule WCAG 2.1), il n’est pas estimé.</p>')

	a('<h3>Primaires</h3><div class="grille g2">')
	for nom, hexa, usage in PRIMAIRES:
		a(case_couleur(nom, hexa, usage))
	a('</div>')

	a('<h3>Neutres</h3><div class="grille g2">')
	for nom, hexa, usage in NEUTRES:
		a(case_couleur(nom, hexa, usage))
	a('</div>')

	a('<h3>Les couches de la carte</h3>')
	a('<p>Une règle tient tout le système : <b>le vert de marque n’est jamais '
	  'une couche</b>. Le vert appartient à l’interface — boutons, sélection, '
	  'en-têtes. Si le vert servait aussi à représenter une donnée, on ne '
	  'saurait plus, en regardant la carte, ce qui est le logiciel et ce qui '
	  'est le territoire.</p>')
	a('<div class="grille g2">')
	for famille, items in COUCHES:
		a('<div class="carte"><h3 style="margin:0 0 8px;font-size:13px;'
		  'letter-spacing:.08em;text-transform:uppercase;color:var(--ardoise)">'
		  '%s</h3>' % famille)
		for nom, hexa in items:
			r = contraste(hexa, BLANC)
			a('<div class="couche"><span class="pip" style="background:%s">'
			  '</span><span>%s</span><span class="h">%s · %.1f:1 · %s</span>'
			  '</div>'
			  % (hexa, nom, hexa, r,
			     'blanc' if r >= 4.5 else 'encre'))
		a('</div>')
	a('</div>')
	a('<p style="font-size:13px;color:var(--ardoise)">Le rapport indiqué est '
	  'celui de la couleur sur fond blanc, et le mot qui suit dit dans quelle '
	  'couleur s’écrit le texte <b>posé sur la pastille de légende</b> : blanc '
	  'au-dessus de 4,5:1, encre en dessous. Sur la carte elle-même, la règle '
	  'ne change jamais : <b>les libellés sont en Encre avec un halo blanc de '
	  '2 px</b>, jamais en blanc sur une couleur de couche — c’est la seule '
	  'façon qu’un nom de wilaya reste lisible quand quatre couches se '
	  'superposent.</p>')

	a('<div class="avert" style="margin-top:22px"><b>Impression</b>'
	  'Les valeurs données sont des valeurs écran (RVB / hexadécimal), '
	  'mesurées. Je ne donne pas d’équivalent CMJN ni de référence Pantone : '
	  'une conversion dépend du papier et du profil de l’imprimeur, et un '
	  'chiffre inventé ici deviendrait un vert faux sur la première brochure. '
	  'Votre imprimeur cale les équivalents sur ces valeurs et vous renvoie un '
	  'BAT — à ce moment-là je les ajoute à la charte.</div>')
	a('</section>')

	# --- 3. Typographie
	a('<section><h2><span class="num">03</span>La typographie</h2>')
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

	# --- 4. Statut de la donnee
	a('<section><h2><span class="num">04</span>Le statut de la donnée</h2>')
	a('<p class="chapo">C’est la partie de la charte qui protège le projet. '
	  'Votre cahier des charges pose la règle : '
	  '<b>FACTS ≠ TARGETS ≠ PROJECTIONS</b>. Une charte graphique doit la '
	  'rendre visible, sinon elle reste une intention. Trois états, et ils ne '
	  'se distinguent <b>jamais par la couleur seule</b> : forme, motif et mot '
	  'écrit. Un lecteur daltonien, une impression en noir et blanc, une '
	  'capture d’écran reprise ailleurs — dans les trois cas la différence '
	  'doit survivre.</p>')

	a('<div class="grille g3">')
	a('<div class="statut"><div class="demo" style="background:#0B5FA5"></div>'
	  '<div class="txt"><b>Fait</b>'
	  '<span>Donnée constatée. Elle porte obligatoirement sa source et sa '
	  'date.</span>'
	  '<span class="regle">aplat plein · bordure pleine · ● Fait</span>'
	  '</div></div>')
	a('<div class="statut"><div class="demo" style="background:#0B5FA5;'
	  'opacity:.30;border-bottom:1px solid var(--trait)"></div>'
	  '<div class="txt"><b>Objectif 2036</b>'
	  '<span>Cible publiquement adoptée. Ce n’est pas un constat, c’est une '
	  'intention datée.</span>'
	  '<span class="regle">aplat 30 % · bordure pleine · ◎ Objectif</span>'
	  '</div></div>')
	a('<div class="statut"><div class="demo" style="'
	  'background-image:repeating-linear-gradient(45deg,#0B5FA5 0 6px,'
	  '#ffffff 6px 13px);opacity:.62;'
	  'border-bottom:1px dashed #0B5FA5"></div>'
	  '<div class="txt"><b>Scénario</b>'
	  '<span>Hypothèse de travail. <b>N’a été adoptée par personne</b> et ne '
	  'doit jamais être présentée comme une décision.</span>'
	  '<span class="regle">hachures 45° · bordure tiretée · ◇ Scénario</span>'
	  '</div></div>')
	a('</div>')

	a('<h3>Les pastilles, telles qu’elles apparaissent</h3>')
	a('<p><span class="badge" style="background:#0B5FA5;color:#fff">'
	  '● Fait</span> &nbsp; '
	  '<span class="badge" style="background:#D3E2F0;color:#0A3C66">'
	  '◎ Objectif 2036</span> &nbsp; '
	  '<span class="badge" style="background:repeating-linear-gradient(45deg,'
	  '#E4EEF7 0 5px,#fff 5px 10px);color:#0A3C66;'
	  'box-shadow:inset 0 0 0 1px #9BBBD8">◇ Scénario</span></p>')

	a('<h3>La ligne de source</h3>')
	a('<p>Sous chaque chiffre publié, une ligne en 12 px Ardoise, dans cet '
	  'ordre exact :</p>')
	a('<div class="spec"><span class="ex mono">'
	  'Source — Nom de l’organisme · publié le JJ/MM/AAAA · relevé le JJ/MM/AAAA'
	  '</span><span class="det">Si la source manque, le champ affiche '
	  '« non renseigné » en Ardoise. Il ne reste jamais vide, et il ne se '
	  'remplit jamais d’une estimation.</span></div>')
	a('</section>')

	# --- 5. Les scores
	a('<section><h2><span class="num">05</span>Les scores sur 100</h2>')
	a('<p class="chapo">Data Center Readiness Score, Free Zone Potential '
	  'Score, Port-Digital Synergy Score : trois indicateurs, une seule '
	  'écriture. Le nombre est toujours écrit — la couleur ne remplace pas le '
	  'chiffre, elle l’accompagne.</p>')
	a('<div class="grille g4">')
	for plage, nom, coul in SCORES:
		val = plage.split('–')[1].strip()
		a('<div class="score"><div class="val" style="background:%s">%s</div>'
		  '<div><b>%s</b><div class="mono" style="font-size:12px;'
		  'color:var(--ardoise)">%s</div></div></div>' % (coul, val, nom, plage))
	a('</div>')
	a('<p style="margin-top:18px"><b>Et une règle de fond :</b> un score '
	  'affiché ouvre toujours le détail de son calcul — les critères, leur '
	  'poids, et la donnée manquante quand il y en a une. Un score dont les '
	  'critères ne sont pas consultables est un avis déguisé en mesure. '
	  'Quand un critère manque, le score n’est pas calculé « au mieux » : il '
	  'affiche <span class="mono">incomplet</span> et dit lequel manque.</p>')
	a('</section>')

	# --- 6. La carte
	a('<section><h2><span class="num">06</span>La carte</h2>')
	a('<p class="chapo">La carte est l’écran principal du produit ; sa mise en '
	  'forme fait donc partie de la charte, pas du développement.</p>')
	a('<ul>'
	  '<li><b>Fond neutre et désaturé.</b> Papier <code>#F7FAF8</code>, eau '
	  '<code>#E8F0F4</code>, frontières <code>#C9D6CF</code> en 1 px. Le fond '
	  'ne doit jamais concurrencer les couches.</li>'
	  '<li><b>Une couche = une couleur de la palette 04.</b> Traits à 2 px, '
	  'points à 8 px, aplats à 55 % d’opacité pour laisser lire le fond.</li>'
	  '<li><b>Sélection</b> en Vert 2036, halo Vert pâle de 4 px. Le vert ne '
	  'sert qu’à ça sur la carte.</li>'
	  '<li><b>Légende obligatoire et toujours visible.</b> Une couche activée '
	  'sans légende affichée est un bogue, pas un choix de mise en page.</li>'
	  '<li><b>Échelle et source du fond de carte</b> en bas à droite, en '
	  '12 px, sur toutes les vues, y compris les captures exportées.</li>'
	  '<li><b>Le mode nuit</b> reprend Vert profond en fond ; les couleurs de '
	  'couche s’éclaircissent de deux crans, elles ne changent pas de teinte.</li>'
	  '</ul>')
	a('</section>')

	# --- 7. Composants
	a('<section><h2><span class="num">07</span>Quelques composants</h2>')
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
	  'Il ne se remplit pas d’une estimation.</div></div>' % VERT_PROFOND)
	a('</div></section>')

	# --- 8. Accessibilite
	a('<section><h2><span class="num">08</span>Accessibilité</h2>')
	lignes = [
		('Encre sur blanc', ENCRE, BLANC),
		('Ardoise sur blanc', '#5B6B64', BLANC),
		('Blanc sur Vert Algérie', BLANC, VERT),
		('Blanc sur Vert profond', BLANC, VERT_PROFOND),
		('Vert Algérie sur blanc', VERT, BLANC),
		('Vert 2036 sur blanc', VERT_VIF, BLANC),
		('Blanc sur Vert 2036', BLANC, VERT_VIF),
		('Encre sur Vert pâle', ENCRE, '#E6F4EC'),
	]
	a('<table><thead><tr><th>Association</th><th>Rapport mesuré</th>'
	  '<th>Niveau WCAG 2.1</th><th>Verdict</th></tr></thead><tbody>')
	for nom, av, ar in lignes:
		r = contraste(av, ar)
		verdict, cls = note(r)
		a('<tr><td>%s</td><td class="n">%.2f:1</td><td class="n">%s</td>'
		  '<td class="ratio %s">%s</td></tr>'
		  % (nom, r, verdict,
		     cls, 'texte courant' if r >= 4.5 else
		     ('titres ≥ 24 px seulement' if r >= 3.0 else 'décoratif uniquement')))
	a('</tbody></table>')
	a('<p style="margin-top:16px">Le seul couple à surveiller est le '
	  '<b>Vert 2036 sur blanc</b>. Il est retenu pour les liens et les états '
	  'actifs, pas pour du texte courant ; en texte de lien, il est '
	  'systématiquement souligné, de sorte que le lien reste identifiable sans '
	  'la couleur.</p>')
	a('</section>')

	# --- 9. Fichiers
	a('<section><h2><span class="num">09</span>Ce qui est livré</h2>')
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
	  'contrastes sont calculés, pas saisis.</li>'
	  '</ul>')
	a('</section>')

	a('</div>')
	a('<footer><div class="env">ALGÉRIE 2036 — charte graphique v1.0 · '
	  '30 août 2026 · document de travail, à faire évoluer avec la plateforme.'
	  '</div></footer>')
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
