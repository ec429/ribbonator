#!/usr/bin/python
# RSS Ribbonator by Edward Cree (soundnfury).  Released under the Simplified BSD License.
# Inspired by Moustachauve's Ribbon Generator for stock, and Ezriilc's version of same.
# All 'devices' and the ribbon texture are from Unistrut's ribbon set,
# but the colours for RSS ribbons are all my fault.

import sys

devices = {'a':'Aircraft',
           'A':'Atmosphere',
           'b':'Base',
           'B':'Base 2',
           'c':'Capsule',
           'e':'Equatorial',
           'E':'Extreme EVA',
           'f':'Flag or Monument',
           'g':'Geosynchronous',
           'i':'Impactor',
           'l':'Probe Lander',
           'L':'Lander',
           'm':'Meteor',
           'M':'Multi-Part Ship',
           'n':'Land Nav',
           'o':'Orbit',
           'p':'Polar',
           'P':'Probe',
           'r':'Rendezvous',
           'R':'Rover',
           's':'Station',
           'v':'Probe Rover',
           'X':'Kerbol Escape',
           '?':'Anomaly',
           '*':'Armada',
           '#':'Armada 2',
           '|':'Kerbal Lost',
           '+':'Kerbal Saved',
           '$':'Resource',
           '^':'Return Chevron',
           }
craft_devices = 'abBcEfilLmMPRsv*#$' # only one of these is allowed
surface_devices = 'bBEfilLnRv?$' # these should not be possible for a planet without a surface
atmos_devices = 'Am' # these should not be possible for an airless body

class CelestialBody(object):
    def __init__(self, name, x, y, surface, atmos, synch, wreath):
        self.name = name
        self.coords = (x, y) # Where is it in layout.png, in ribbon-widths and ribbon-heights
        self.surface = surface # Does it have a surface?
        self.atmos = atmos # Does it have an atmosphere?
        self.synch = synch # is synchronous orbit within SOI?  Hint: for tidally-locked moons this will be false.  (Although you could argue that a Pluto lander is in synchronous Charon orbit...)
        self.wreath = wreath # string indicating what the Challenge on this body is, or None
        self.craft = None
        self.devices = []
    def add_device(self, c):
        if c not in devices:
            raise IndexError('Non-existent device', c, 'listed for', self.name)
        device = devices[c]
        if c in craft_devices:
            if self.craft is not None:
                raise ValueError('Multiple craft devices', self.craft, device, 'on', self.name)
            self.craft = device
        elif c in surface_devices and not self.surface:
            raise ValueError('Surface device', device, 'on body without surface', self.name)
        elif c in atmos_devices and not self.atmos:
            raise ValueError('Device', device, 'on airless body', self.name)
        else:
            self.devices.append(devices[c])

class Planet(CelestialBody): pass
class Moon(CelestialBody):
    def __init__(self, parent, name, x, y, atmos, wreath):
        # All moons have surfaces (there are no gas moons), and none support synchronous orbit
        super(Moon, self).__init__(name, x, y, True, atmos, False, wreath)
        self.parent = parent
class Asteroid(CelestialBody): pass

sun = CelestialBody('Sol', 0, 0, False, True, True, None)
mercury = Planet('Mercury', 0, 1, True, False, False, None)
venus = Planet('Venus', 0, 2, True, True, False, "Reach orbit from the surface")
earth = Planet('Earth', 1, 0, True, True, True, "Single Stage to Orbit")
luna = Moon(earth, 'Luna', 1, 1, False, None)
asteroid = Asteroid('Asteroid', 1, 2, True, False, False, None)
mars = Planet('Mars', 2, 0, True, True, True, None)
phobos = Moon(mars, 'Phobos', 2, 1, False, None)
deimos = Moon(mars, 'Deimos', 2, 2,  False, None)
jupiter = Planet('Jupiter', 3, 0, False, True, True, None)
io = Moon(jupiter, 'Io', 3, 1, False, None)
europa = Moon(jupiter, 'Europa', 3, 2, False, None)
ganymede = Moon(jupiter, 'Ganymede', 4, 0, False, None)
callisto = Moon(jupiter, 'Callisto', 4, 1, False, None)
# note disruption of layout order here
saturn = Planet('Saturn', 5, 0, False, True, True, None)
mimas = Moon(saturn, 'Mimas', 4, 2, False, None)
titan = Moon(saturn, 'Titan', 5, 1, True, None)
iapetus = Moon(saturn, 'Iapetus', 5, 2, False, None)
enceladus = Moon(saturn, 'Enceladus', 6, 0, False, None)
tethys = Moon(saturn, 'Tethys', 6, 1, False, None)
dione = Moon(saturn, 'Dione', 6, 2, False, None)
rhea = Moon(saturn, 'Rhea', 7, 0, False, None)
uranus = Planet('Uranus', 7, 1, False, True, True, None)
neptune = Planet('Neptune', 7, 2, False, True, True, None)
# note disruption of layout order again here
triton = Moon(neptune, 'Triton', 8, 2, False, None)
pluto = Planet('Pluto', 8, 0, True, False, True, None)
charon = Moon(pluto, 'Charon', 8, 1, False, None)

bodies = [sun, mercury, venus, earth, luna, asteroid, mars, phobos, deimos, jupiter, io, europa, ganymede, callisto, saturn, mimas, titan, iapetus, enceladus, tethys, dione, rhea, uranus, neptune, triton, pluto, charon]

for line in sys.stdin.readlines():
    body, merits = line.strip().split(None, 1)
    for b in bodies:
        if b.name == body:
            break
    else:
        raise IndexError('No such body', body)
    for d in merits:
        b.add_device(d)
