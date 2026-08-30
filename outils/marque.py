#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere les fichiers du logo Algerie 2036.

Le trace de la marque est ecrit UNE SEULE FOIS ici (FRONDES). Toutes les
declinaisons — couleur, blanc, noir, favicon, verticale, horizontale — sont
produites a partir de ces memes chemins : une correction de dessin se fait a
un seul endroit et se propage partout.

Les textes sont convertis en CHEMINS, jamais laisses en <text> : un logo qui
depend d'une police installee sur la machine du lecteur n'est pas un logo.
L'arabe est mis en forme par HarfBuzz avant conversion, sinon les lettres
sortent isolees et dans le mauvais sens.
"""

import os
import sys

import uharfbuzz as hb
from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICES = os.path.join(RACINE, 'polices')
SORTIE = os.path.join(RACINE, 'logo')

# --- Couleurs -------------------------------------------------------------

VERT = '#006233'        # Vert Algerie — couleur primaire
VERT_VIF = '#0F8C4C'    # Vert 2036 — la fronde centrale, les liens, les boutons
BLANC = '#FFFFFF'
ENCRE = '#0B1F17'

# --- Le dessin ------------------------------------------------------------
#
# Trois frondes qui montent d'un socle commun et se rejoignent en pointe :
# l'abstraction du memorial, et aussi trois pales — le volet renouvelables.
# Repere 120 x 120, sol a y = 112, axe a x = 60.

FRONDE_GAUCHE = ('M54,12 C46,58 34,96 6,112 L34,112 C46,92 52,52 54,12 Z')
FRONDE_DROITE = ('M66,12 C74,58 86,96 114,112 L86,112 C74,92 68,52 66,12 Z')
FRONDE_CENTRE = ('M60,4 C57,40 55,76 52,112 L68,112 C65,76 63,40 60,4 Z')

BOITE = 120.0
SOL = 112.0


def marque(couleur_laterale, couleur_centre):
	"""Les trois frondes, dans le repere 120 x 120."""
	return (
		'<path d="%s" fill="%s"/>'
		'<path d="%s" fill="%s"/>'
		'<path d="%s" fill="%s"/>'
	) % (FRONDE_GAUCHE, couleur_laterale, FRONDE_DROITE, couleur_laterale,
	     FRONDE_CENTRE, couleur_centre)


# --- Texte -> chemin ------------------------------------------------------

_CACHE = {}


def _police(nom):
	if nom not in _CACHE:
		chemin = os.path.join(POLICES, nom)
		octets = open(chemin, 'rb').read()
		face = hb.Face(octets)
		fonte = hb.Font(face)
		fonte.scale = (face.upem, face.upem)
		hb.ot_font_set_funcs(fonte)
		tt = TTFont(chemin)
		_CACHE[nom] = (fonte, face.upem, tt.getGlyphSet(), tt.getGlyphOrder())
	return _CACHE[nom]


def texte(nom_police, chaine, taille, tracking=0.0, direction=None):
	"""Renvoie (chemin SVG, largeur). Ligne de base a y = 0, texte vers le haut."""
	fonte, upem, glyphes, ordre = _police(nom_police)
	tampon = hb.Buffer()
	tampon.add_str(chaine)
	tampon.guess_segment_properties()
	if direction:
		tampon.direction = direction
	hb.shape(fonte, tampon)
	k = taille / float(upem)
	x = 0.0
	morceaux = []
	for info, pos in zip(tampon.glyph_infos, tampon.glyph_positions):
		nom = ordre[info.codepoint]
		plume = SVGPathPen(glyphes)
		t = Transform(k, 0, 0, -k, x + pos.x_offset * k, -pos.y_offset * k)
		glyphes[nom].draw(TransformPen(plume, t))
		d = plume.getCommands()
		if d:
			morceaux.append(d)
		x += pos.x_advance * k + tracking * taille
	# Le tracking ajoute apres le dernier signe n'appartient pas au mot.
	if tampon.glyph_infos:
		x -= tracking * taille
	return ' '.join(morceaux), x


PLEX = 'IBMPlexSans-%d.ttf'
PLEX_AR = 'IBMPlexSansArabic-%d.ttf'


# --- Assemblage des declinaisons -----------------------------------------

def enveloppe(largeur, hauteur, corps, titre):
	return (
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" '
		'width="%s" height="%s" role="img" aria-label="%s">'
		'<title>%s</title>%s</svg>\n'
	) % (_n(largeur), _n(hauteur), _n(largeur), _n(hauteur), titre, titre, corps)


def _n(v):
	return ('%.2f' % v).rstrip('0').rstrip('.')


def ecrire(nom, contenu):
	chemin = os.path.join(SORTIE, nom)
	with open(chemin, 'w') as f:
		f.write(contenu)
	return chemin, len(contenu)


def bloc_mot(taille, couleur_mot, couleur_annee, tracking=0.10):
	"""« ALGÉRIE » puis « 2036 » sur deux lignes, deja converties en chemins."""
	d1, l1 = texte(PLEX % 600, 'ALGÉRIE', taille, tracking)
	# L'annee est plus legere et plus espacee que le mot : elle se lit comme
	# une date, pas comme la suite du nom.
	d2, l2 = texte(PLEX % 400, '2036', taille, tracking * 1.55)
	interligne = taille * 1.16
	corps = (
		'<g transform="translate(0,0)"><path d="%s" fill="%s"/></g>'
		'<g transform="translate(0,%s)"><path d="%s" fill="%s"/></g>'
	) % (d1, couleur_mot, _n(interligne), d2, couleur_annee)
	return corps, max(l1, l2), interligne


def principal(nom, couleur_laterale, couleur_centre, couleur_mot, couleur_annee):
	"""Lockup horizontal : marque a gauche, deux lignes de texte a droite."""
	h_marque = 96.0
	k = h_marque / BOITE
	ecart = 26.0
	taille = 30.0
	corps_mot, largeur_mot, interligne = bloc_mot(taille, couleur_mot, couleur_annee)

	# La hauteur des capitales sert d'alignement optique, pas la boite du texte.
	cap = taille * 0.698  # hauteur de capitale IBM Plex Sans
	hauteur_texte = interligne + cap
	x_texte = h_marque * (BOITE / BOITE) * 0 + BOITE * k + ecart
	haut = max(h_marque, hauteur_texte)
	y_marque = (haut - h_marque) / 2.0
	y_base = (haut - hauteur_texte) / 2.0 + cap

	corps = (
		'<g transform="translate(0,%s) scale(%s)">%s</g>'
		'<g transform="translate(%s,%s)">%s</g>'
	) % (_n(y_marque), _n(k), marque(couleur_laterale, couleur_centre),
	     _n(x_texte), _n(y_base), corps_mot)
	largeur = x_texte + largeur_mot
	return ecrire(nom, enveloppe(largeur, haut, corps, 'Algérie 2036'))


def vertical(nom, couleur_laterale, couleur_centre, couleur_mot, couleur_annee):
	h_marque = 120.0
	k = h_marque / BOITE
	taille = 26.0
	d1, l1 = texte(PLEX % 600, 'ALGÉRIE', taille, 0.10)
	d2, l2 = texte(PLEX % 400, '2036', taille, 0.155)
	ecart_mots = taille * 0.55
	largeur_mot = l1 + ecart_mots + l2
	largeur = max(BOITE * k, largeur_mot)
	ecart = 26.0
	cap = taille * 0.698
	haut = h_marque + ecart + cap
	x_mot = (largeur - largeur_mot) / 2.0
	corps = (
		'<g transform="translate(%s,0) scale(%s)">%s</g>'
		'<g transform="translate(%s,%s)"><path d="%s" fill="%s"/>'
		'<g transform="translate(%s,0)"><path d="%s" fill="%s"/></g></g>'
	) % (_n((largeur - BOITE * k) / 2.0), _n(k),
	     marque(couleur_laterale, couleur_centre),
	     _n(x_mot), _n(haut), d1, couleur_mot,
	     _n(l1 + ecart_mots), d2, couleur_annee)
	return ecrire(nom, enveloppe(largeur, haut, corps, 'Algérie 2036'))


def arabe(nom, couleur_laterale, couleur_centre, couleur_mot, couleur_annee):
	"""Verrou arabe : « الجزائر 2036 ». La marque se place a DROITE.

	Les deux morceaux sont mis en forme SEPAREMENT et poses a la main :
	HarfBuzz ne fait pas le bidi. Une seule passe en « rtl » sur la chaine
	entiere retournait le nombre — 2036 sortait « 6302 ».
	"""
	h_marque = 96.0
	k = h_marque / BOITE
	taille = 34.0
	d_mot, l_mot = texte(PLEX_AR % 600, 'الجزائر', taille, 0.0, 'rtl')
	d_an, l_an = texte(PLEX % 400, '2036', taille, 0.10, 'ltr')
	ecart_mots = taille * 0.42
	ecart = 28.0
	haut = h_marque
	# En arabe la lecture va de droite a gauche : le nombre se pose a gauche,
	# le mot a sa droite, et la marque tout a droite.
	x_mot = l_an + ecart_mots
	largeur = x_mot + l_mot + ecart + BOITE * k
	corps = (
		'<g transform="translate(0,%s)"><path d="%s" fill="%s"/></g>'
		'<g transform="translate(%s,%s)"><path d="%s" fill="%s"/></g>'
		'<g transform="translate(%s,0) scale(%s)">%s</g>'
	) % (_n(haut * 0.63), d_an, couleur_annee,
	     _n(x_mot), _n(haut * 0.63), d_mot, couleur_mot,
	     _n(x_mot + l_mot + ecart), _n(k),
	     marque(couleur_laterale, couleur_centre))
	return ecrire(nom, enveloppe(largeur, haut, corps, 'الجزائر 2036'))


def seule(nom, couleur_laterale, couleur_centre):
	return ecrire(nom, enveloppe(BOITE, BOITE,
	                             marque(couleur_laterale, couleur_centre),
	                             'Algérie 2036'))


def favicon(nom):
	"""Pastille : la marque en blanc sur un carre vert a coins arrondis."""
	marge = 18.0
	k = (BOITE - 2 * marge) / BOITE
	corps = (
		'<rect width="120" height="120" rx="26" fill="%s"/>'
		'<g transform="translate(%s,%s) scale(%s)">%s</g>'
	) % (VERT, _n(marge), _n(marge), _n(k), marque(BLANC, BLANC))
	return ecrire(nom, enveloppe(BOITE, BOITE, corps, 'Algérie 2036'))


def main():
	os.makedirs(SORTIE, exist_ok=True)
	faits = []
	faits.append(principal('algerie2036-principal.svg', VERT, VERT_VIF, ENCRE, VERT))
	faits.append(principal('algerie2036-principal-blanc.svg', BLANC, BLANC, BLANC, BLANC))
	faits.append(vertical('algerie2036-vertical.svg', VERT, VERT_VIF, ENCRE, VERT))
	faits.append(vertical('algerie2036-vertical-blanc.svg', BLANC, BLANC, BLANC, BLANC))
	faits.append(arabe('algerie2036-arabe.svg', VERT, VERT_VIF, ENCRE, VERT))
	faits.append(arabe('algerie2036-arabe-blanc.svg', BLANC, BLANC, BLANC, BLANC))
	faits.append(seule('algerie2036-marque.svg', VERT, VERT_VIF))
	faits.append(seule('algerie2036-marque-blanche.svg', BLANC, BLANC))
	faits.append(seule('algerie2036-marque-noire.svg', ENCRE, ENCRE))
	faits.append(favicon('algerie2036-pastille.svg'))
	for chemin, taille in faits:
		print('%6d o  %s' % (taille, os.path.basename(chemin)))
	return 0


if __name__ == '__main__':
	sys.exit(main())
