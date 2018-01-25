#!/usr/bin/python
# RSS Ribbonator by Edward Cree (soundnfury).  Released under the Simplified BSD License.
# Inspired by Moustachauve's Ribbon Generator for stock, and Ezriilc's version of same.
# All 'devices' and the ribbon texture are from Unistrut's ribbon set,
# but the colours for RSS ribbons are all my fault.

import sys
from PIL import Image

devices = {'a':'Aircraft',
           'A':'Atmosphere',
           'b':'Base',
           'B':'Base 2',
           'c':'Capsule',
           'C':'Closer Solar Orbit', #new! done!
           'd':'Double Dots', #new! done!
           'D':'Double Bars', #new! done!
           'e':'Equatorial',
           'E':'Extreme EVA',
           'f':'Flag or Monument',
           'F':'Flag device', #new! done!
           'g':'Geosynchronous',
           'i':'Impactor',
           'l':'Probe Lander',
           'k':'Caps Device', #new! done!
           'K':'Rendezvous Device', #new! done!
           'L':'Lander',
           'm':'Meteor',
           'M':'Multi-Part Ship',
           'n':'Land Nav',
           'o':'Orbit',
           'O':'Orbit Device', #new! done!
           'p':'Polar',
           'P':'Probe',
           'r':'Rendezvous',
           'R':'Rover',
           's':'Station',
           'v':'Probe Rover',
           'V':'Bevel', #new! done!
           'W':'Challenge Wreath',
           'X':'Kerbol Escape',
           'x':'Deep Atmosphere', #new! done!
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
collation = 'eprgoX^' + craft_devices + '|+' # used to sort devices in case they overlap

def load_device(d):
    f = 'Devices/%s.png'%(d,)
    return Image.open(f)

device_images = {k: load_device(d) for k,d in list(devices.items())}
layout = Image.open('RSS/Layout.png')
asteroid_layout = Image.open('RSS/Asteroids.png')

class CelestialBody(object):
    star = False # is the 'Escape' device valid?
    def __init__(self, name, x, y, surface, atmos, synch, wreath):
        self.name = name
        self.x, self.y = x, y # Where is it in layout.png, in ribbon-widths and ribbon-heights
        self.surface = surface # Does it have a surface?
        self.atmos = atmos # Does it have an atmosphere?
        self.synch = synch # is synchronous orbit within SOI?  Hint: for tidally-locked moons this will be false.  (Although you could argue that a Pluto lander is in synchronous Charon orbit...)
        self.wreath = wreath # string indicating what the Challenge on this body is, or None
        self.craft = None
        self.devices = []
    def copy(self):
        return self.__class__(self.name, self.x, self.y, self.surface, self.atmos, self.synch, self.wreath)
    def permit(self, c): # indicates what things add_device will accept.  For UIs
        if c not in devices:
            return False
        if c in surface_devices and not self.surface:
            return False
        if c in atmos_devices and not self.atmos:
            return False
        if c == 'W' and not self.wreath:
            return False
        if c == 'X' and not self.star:
            return False
        return True
    def add_device(self, c):
        if c not in devices:
            raise IndexError('Non-existent device', c, 'listed for', self.name)
        device = devices[c]
        if c in craft_devices:
            if self.craft is not None:
                raise ValueError('Multiple craft devices', devices.get(self.craft) + ",", device, 'on', self.name)
            self.craft = c
        if c in surface_devices and not self.surface:
            raise ValueError('Surface device', device, 'on body without surface', self.name)
        elif c in atmos_devices and not self.atmos:
            raise ValueError('Device', device, 'on airless body', self.name)
        elif c == 'W' and not self.wreath:
            raise ValueError('There is no Challenge Wreath for', self.name)
        elif c == 'X' and not self.star:
            raise ValueError('Device', device, 'on', self.name, 'only allowed on Stars')
        else:
            self.devices.append(c)
    def base_ribbon(self):
        x = self.x * 120
        y = self.y * 32
        return layout.crop((x, y, x+120, y+32))
    def generate(self):
        self.devices = sorted(self.devices, key=lambda d:collation.find(d)) # ensure correct covering
        base = self.base_ribbon()
        for d in self.devices:
            img = device_images[d]
            base.paste(img, img)
        return base

class Star(CelestialBody):
    star = True
class Planet(CelestialBody): pass
class Moon(CelestialBody):
    def __init__(self, parent, name, x, y, atmos, synch, wreath):
        # All moons have surfaces (there are no gas moons).  No real moons support synchronous orbits, but some stock moons do (e.g. Minmus, Gilly)
        super(Moon, self).__init__(name, x, y, True, atmos, synch, wreath)
        self.parent = parent # we don't actually use this anywhere
    def copy(self):
        return self.__class__(self.parent, self.name, self.x, self.y, self.atmos, self.synch, self.wreath)
class Asteroid(CelestialBody):
    mb = None
    def set_main_body(self, x, y):
        self.mb = (x, y)
    def base_ribbon(self):
        x = self.mb[0] * 120
        y = self.mb[1] * 32
        return asteroid_layout.crop((x, y, x+120, y+32))

sun = Star('Sol', 0, 0, False, True, True, None)
mercury = Planet('Mercury', 0, 1, True, False, False, None)
venus = Planet('Venus', 0, 2, True, True, False, "Reach orbit from the surface")
earth = Planet('Earth', 1, 0, True, True, True, "Single Stage to Orbit")
luna = Moon(earth, 'Luna', 1, 1, False, False, None)
mars = Planet('Mars', 2, 0, True, True, True, None)
phobos = Moon(mars, 'Phobos', 2, 1, False, False, None)
deimos = Moon(mars, 'Deimos', 2, 2,  False, False, None)
ceres = Planet('Ceres', 3, 0, True, False, True, None)
vesta = Planet('Vesta', 3, 1, True, False, True, None)
asteroid = Asteroid('Asteroid', 3, 2, True, False, False, None)
jupiter = Planet('Jupiter', 4, 0, False, True, True, None)
io = Moon(jupiter, 'Io', 4, 1, False, False, None)
europa = Moon(jupiter, 'Europa', 4, 2, False, False, None)
ganymede = Moon(jupiter, 'Ganymede', 5, 1, False, False, None)
callisto = Moon(jupiter, 'Callisto', 5, 2, False, False, None)
saturn = Planet('Saturn', 6, 0, False, True, True, None)
mimas = Moon(saturn, 'Mimas', 6, 1, False, False, None)
enceladus = Moon(saturn, 'Enceladus', 6, 2, False, False, None)
tethys = Moon(saturn, 'Tethys', 7, 0, False, False, None)
dione = Moon(saturn, 'Dione', 7, 1, False, False, None)
rhea = Moon(saturn, 'Rhea', 7, 2, False, False, None)
titan = Moon(saturn, 'Titan', 8, 1, True, False, None)
iapetus = Moon(saturn, 'Iapetus', 8, 2, False, False, None)
uranus = Planet('Uranus', 9, 0, False, True, True, None)
# note disruption of layout order here
miranda = Moon(uranus,'Miranda',8,0,False, False, None)
ariel = Moon(uranus,'Ariel',9,1,False, False, None)
umbriel = Moon(uranus,'Umbriel',9,2,False, False, None)
titania = Moon(uranus,'Titania',10,1,False, False, None)
oberon = Moon(uranus,'Oberon',10,2,False, False, None)
neptune = Planet('Neptune', 10, 0, False, True, True, None)
# note disruption of layout order again here
triton = Moon(neptune, 'Triton', 11, 0, True, False, None)
pluto = Planet('Pluto', 11, 1, True, True, True, None)
charon = Moon(pluto, 'Charon', 11, 2, False, False, None)

bodies = [sun, mercury, venus, earth, luna, mars, phobos, deimos, ceres, vesta, asteroid, jupiter, io, europa, ganymede, callisto, saturn, mimas, enceladus, tethys, dione, rhea, titan, iapetus, uranus, miranda, ariel, umbriel, titania, oberon, neptune, triton, pluto, charon]

def generate(l):
    grid = [[None, None, None] for x in range(12)]

    for line in l:
        body, _, merits = line.strip().partition(' ')
        body,_,mainbody = body.partition('-') # for Asteroid-MainBody
        for b in bodies:
            if b.name == body:
                break
        else:
            raise IndexError('No such body', body)
        b = b.copy()
        if isinstance(b, Asteroid):
            for mb in bodies:
                if mb.name == mainbody:
                    break
            else:
                raise IndexError('No such mainBody', mainbody)
            b.set_main_body(mb.x, mb.y)
        for d in merits:
            b.add_device(d)
        grid[b.x][b.y] = b.generate()

    height = 0
    for x in range(12):
        grid[x] = [g for g in grid[x] if g is not None]
        height = max(height, len(grid[x]))
    grid = [g for g in grid if g]
    width = len(grid)
    if not width:
        return Image.new('RGBA', (1, 1), 0)
    output = Image.new('RGBA', (width * 120, height * 32), 0)
    for x, column in enumerate(grid):
        for y, row in enumerate(column):
            output.paste(row, (x * 120, y * 32))
    return output

if __name__ == '__main__':
    output = generate(sys.stdin.readlines())
    if output is not None:
        output.save('out.png')
