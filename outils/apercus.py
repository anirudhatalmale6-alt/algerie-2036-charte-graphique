#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Photographie la charte, section par section, pour l'envoi au client.

Jamais de capture pleine page : on cadre la section demandee, viewport fixe.
"""

import os
import sys

from playwright.sync_api import sync_playwright

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, 'apercus')

# (fichier, selecteur d'ancrage, decalage vertical, hauteur de fenetre)
VUES = [
	('01-marque.png', 'header', 0, 980),
	('02-declinaisons.png', 'section:nth-of-type(1) h3', -40, 940),
	('03-couleurs.png', 'section:nth-of-type(2)', 0, 1000),
	('04-valeurs.png', 'section:nth-of-type(2) h3:nth-of-type(3)', -30, 1000),
	('05-couches.png', 'section:nth-of-type(3)', 0, 1000),
	('06-couches-suite.png', 'section:nth-of-type(3) .grille', -30, 1000),
	('07-statut.png', 'section:nth-of-type(5)', 0, 980),
	('08-scores.png', 'section:nth-of-type(6)', 0, 900),
	('09-composants.png', 'section:nth-of-type(8)', 0, 940),
	('10-accessibilite.png', 'section:nth-of-type(9)', 0, 980),
]


def main():
	os.makedirs(SORTIE, exist_ok=True)
	url = 'file://' + os.path.join(RACINE, 'charte.html')
	faits = []
	with sync_playwright() as p:
		# --disable-lcd-text : sans ca, Chromium fait de l'anticrenelage
		# sous-pixel et pose des franges ORANGE et BLEUES sur chaque lettre.
		# Sur une charte « vert et blanc exclusivement », la capture
		# contredirait le document qu'elle est censee prouver — mesure faite :
		# 45 849 pixels colores hors de la bande verte sur une seule vue.
		nav = p.chromium.launch(args=['--disable-lcd-text',
		                              '--force-color-profile=srgb'])
		page = nav.new_page()
		for nom, sel, dy, haut in VUES:
			# La fenetre reste sous 2000 px dans les deux sens.
			page.set_viewport_size({'width': 1280, 'height': min(haut, 1400)})
			page.goto(url)
			page.wait_for_timeout(500)
			y = page.evaluate(
				"s => { const e = document.querySelector(s);"
				" return e ? e.getBoundingClientRect().top + window.scrollY : 0 }",
				sel)
			page.evaluate('y => window.scrollTo(0, y)', max(0, y + dy))
			page.wait_for_timeout(350)
			chemin = os.path.join(SORTIE, nom)
			page.screenshot(path=chemin)
			faits.append((nom, os.path.getsize(chemin)))
		nav.close()
	for nom, taille in faits:
		print('%8d o  %s' % (taille, nom))
	return 0


if __name__ == '__main__':
	sys.exit(main())
