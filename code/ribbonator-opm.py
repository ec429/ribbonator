#!/usr/bin/python
# RSS Ribbonator by Edward Cree (soundnfury).  Released under the Simplified BSD License.
# Inspired by Moustachauve's Ribbon Generator for stock, and Ezriilc's version of same.
# All 'devices' and the ribbon texture are from Unistrut's ribbon set,
# but the colours for RSS ribbons are all my fault.

import sys
from PIL import Image
import ribbonator

ribbonator.layout = Image.open('OPM/Layout.png')
ribbonator.asteroid_layout = Image.open('OPM/Asteroids.png')

sun = ribbonator.Star('Sun', 0, 0, False, True, True, None)
moho = ribbonator.Planet('Moho', 0, 1, True, False, False, None)
asteroid = ribbonator.Asteroid('Asteroid', 0, 2, True, False, False, None)
eve = ribbonator.Planet('Eve', 1, 0, True, True, True, "Reach orbit from the surface")
gilly = ribbonator.Moon(eve, 'Gilly', 1, 1, False, True, None)
kerbin = ribbonator.Planet('Kerbin', 2, 0, True, True, True, "Single Stage to Orbit")
mun = ribbonator.Moon(kerbin, 'Mun', 2, 1, False, False, None)
minmus = ribbonator.Moon(kerbin, 'Minmus', 2, 2, False, True, None)
duna = ribbonator.Planet('Duna', 3, 0, True, True, True, None)
ike = ribbonator.Moon(duna, 'Ike', 3, 1, False, False, None)
dres = ribbonator.Planet('Dres',3, 2, True, False, True, None)
jool = ribbonator.Planet('Jool', 4, 0, False, True, True, None)
laythe = ribbonator.Moon(jool, 'Laythe', 4, 1, True, False, None)
tylo = ribbonator.Moon(jool, 'Tylo', 4, 2, False, False, "Land and return to orbit safely")
vall = ribbonator.Moon(jool, 'Vall', 5, 0, False, False, None)
bop = ribbonator.Moon(jool, 'Bop', 5, 1, False, False, None)
pol = ribbonator.Moon(jool, 'Pol', 5, 2,  False, False, None)
sarnus = ribbonator.Planet('Sarnus', 6, 0, False, True, True, None)
hale = ribbonator.Moon(sarnus, 'Hale', 6, 1, False, False, None)
ovok = ribbonator.Moon(sarnus, 'Ovok', 6, 2, False, False, None)
eeloo = ribbonator.Moon(sarnus, 'Eeloo', 7, 0, False, True, None)
slate = ribbonator.Moon(sarnus, 'Slate', 7, 1, False, False, None)
tekto = ribbonator.Moon(sarnus, 'Tekto', 7, 2,  True, False, None)
urlum = ribbonator.Planet('Urlum', 8, 0, False, True, True, None)
polta = ribbonator.Moon(urlum, 'Polta', 8, 1, False, False, None)
priax = ribbonator.Moon(urlum, 'Priax', 8, 2, False, False, None)
wal = ribbonator.Moon(urlum, 'Wal', 9, 1, False, False, None)
tal = ribbonator.Moon(wal, 'Tal', 9, 2,  False, False, None)
neidon = ribbonator.Planet('Neidon', 10, 0, False, True, True, None)
thatmo = ribbonator.Moon(neidon, 'Thatmo', 10, 1, True, False, None)
nissee = ribbonator.Moon(neidon, 'Nissee', 10, 2, False, False, None)
plock = ribbonator.Planet('Plock', 11, 0, True, False, True, None)
karen = ribbonator.Moon(plock, 'Karen', 11, 1, False, False, None)

ribbonator.bodies = [sun, moho, asteroid, eve, gilly, dres, kerbin, mun, minmus, duna, ike, vall, jool, laythe, tylo, bop, pol, sarnus, hale, ovok, eeloo, slate, tekto, urlum, polta, priax, wal, tal, neidon, thatmo, nissee, plock, karen]

if __name__ == '__main__':
    output = ribbonator.generate(sys.stdin.readlines())
    if output is not None:
        output.save('out.png')
