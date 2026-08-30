#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporte les logos en PNG a fond transparent.

Le SVG reste le fichier de reference : ces PNG existent pour les outils qui
ne savent pas lire un SVG (traitement de texte, presentation, reseaux
sociaux). La hauteur demandee est respectee au pixel — le navigateur mesure
la boite reelle apres rendu, on ne calcule pas la largeur a la main.
"""

import os
import sys

from playwright.sync_api import sync_playwright

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, 'logo', 'png')

# (fichier SVG, hauteurs voulues)
EXPORTS = [
	('algerie2036-principal.svg', [200, 600]),
	('algerie2036-principal-blanc.svg', [200, 600]),
	('algerie2036-vertical.svg', [300, 900]),
	('algerie2036-marque.svg', [256, 1024]),
	('algerie2036-marque-blanche.svg', [256, 1024]),
	('algerie2036-arabe.svg', [200, 600]),
	('algerie2036-pastille.svg', [256, 512]),
]


def main():
	os.makedirs(SORTIE, exist_ok=True)
	faits = []
	with sync_playwright() as p:
		nav = p.chromium.launch()
		page = nav.new_page()
		gabarit = os.path.join(RACINE, 'logo', '_export.html')
		for fichier, hauteurs in EXPORTS:
			for h in hauteurs:
				# La page est ECRITE SUR LE DISQUE puis ouverte en file://.
				# Avec set_content(), l'origine est about:blank et Chromium
				# refuse les sous-ressources file:// : l'image ne charge pas,
				# et la boite mesuree devient un carre trompeur.
				with open(gabarit, 'w') as f:
					f.write('<!doctype html><meta charset="utf-8">'
					        '<body style="margin:0;background:transparent">'
					        '<img id="l" src="%s" style="height:%dpx;'
					        'display:block"></body>' % (fichier, h))
				page.set_viewport_size({'width': 1600, 'height': 1200})
				page.goto('file://' + gabarit)
				page.wait_for_selector('#l')
				page.wait_for_timeout(220)
				naturelle = page.evaluate(
					"() => { const i = document.getElementById('l');"
					" return i.naturalWidth }")
				if not naturelle:
					raise SystemExit('image non chargee : ' + fichier)
				boite = page.locator('#l').bounding_box()
				nom = '%s-%dpx.png' % (fichier[:-4], h)
				chemin = os.path.join(SORTIE, nom)
				page.screenshot(path=chemin, omit_background=True, clip={
					'x': boite['x'], 'y': boite['y'],
					'width': boite['width'], 'height': boite['height']})
				faits.append((nom, int(boite['width']), int(boite['height']),
				              os.path.getsize(chemin)))
		nav.close()
	if os.path.exists(gabarit):
		os.remove(gabarit)
	for nom, l, h, taille in faits:
		print('%5d x %-5d %8d o  %s' % (l, h, taille, nom))
	return 0


if __name__ == '__main__':
	sys.exit(main())
