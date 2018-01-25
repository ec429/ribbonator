#!/usr/bin/python
# RSS Ribbonator by Edward Cree (soundnfury).  Released under the Simplified BSD License.
# Inspired by Moustachauve's Ribbon Generator for stock, and Ezriilc's version of same.
# All 'devices' and the ribbon texture are from Unistrut's ribbon set,
# but the colours for RSS ribbons are all my fault.

import sys
from PIL import Image
import ribbonator

ribbonator.layout = Image.open('Stock/Layout.png')
ribbonator.asteroid_layout = Image.open('Stock/Asteroids.png')

sun = ribbonator.Star('Sun', 0, 0, False, True, True, None)
moho = ribbonator.Planet('Moho', 0, 1, True, False, False, None)
asteroid = ribbonator.Asteroid('Asteroid', 0, 2, True, False, False, None)
eve = ribbonator.Planet('Eve', 1, 0, True, True, True, "Reach orbit from the surface")
gilly = ribbonator.Moon(eve, 'Gilly', 1, 1, False, True, None)
dres = ribbonator.Planet('Dres',1, 2, True, False, True, None)
kerbin = ribbonator.Planet('Kerbin', 2, 0, True, True, True, "Single Stage to Orbit")
mun = ribbonator.Moon(kerbin, 'Mun', 2, 1, False, False, None)
minmus = ribbonator.Moon(kerbin, 'Minmus', 2, 2, False, True, None)
duna = ribbonator.Planet('Duna', 3, 0, True, True, True, None)
ike = ribbonator.Moon(duna, 'Ike', 3, 1, False, False, None)
jool = ribbonator.Planet('Jool', 4, 0, False, True, True, None)
#Mind the order
vall = ribbonator.Moon(jool, 'Vall', 3, 2, False, False, None)
laythe = ribbonator.Moon(jool, 'Laythe', 4, 1, True, False, None)
tylo = ribbonator.Moon(jool, 'Tylo', 4, 2, False, False, "Land and return to orbit safely")
bop = ribbonator.Moon(jool, 'Bop', 5, 1, False, False, None)
pol = ribbonator.Moon(jool, 'Pol', 5, 2,  False, False, None)
#Mind the order
eeloo = ribbonator.Planet('Eeloo', 5, 0, True, False, True, None)

ribbonator.bodies = [sun, moho, asteroid, eve, gilly, dres, kerbin, mun, minmus, duna, ike, vall, jool, laythe, tylo, eeloo, bop, pol]

if __name__ == '__main__':
    output = ribbonator.generate(sys.stdin.readlines())
    if output is not None:
        output.save('out.png')
