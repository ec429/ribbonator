#!/usr/bin/python
# RSS Ribbonator by Edward Cree (soundnfury).  Released under the Simplified BSD License.
# Inspired by Moustachauve's Ribbon Generator for stock, and Ezriilc's version of same.
# All 'devices' and the ribbon texture are from Unistrut's ribbon set,
# but the colours for RSS ribbons are all my fault.

import sys
import os
from PIL import Image
import ribbonator


if __name__ == '__main__':
	devsNereid = ['mV','CkV','xV','dLV','dkV','dV','DmV','DCkV','DdLV','DdkV','DdV','DLV','DOkV','DOkKV','DdFLV','DdRV','LV','OkV','OkKV','dFLV','dRV','V']
	devsNereidSolar = ['CkV','DCkV']
	devsNereidSurf = ['dLV','DdLV','DLV','DdFLV','DdRV','LV','dFLV','dRV']
	devsNereidAtmo = ['mV','xV','DmV']
	devsNereidNames = {'mV':'Atmosphere','CkV':'CloserSolarOrbit','xV':'DeepAtmosphere','dLV':'EvaGround','dkV':'EvaOrbit','dV':'EvaSpace','DmV':'FirstAtmosphere','DCkV':'FirstCloserSolarOrbit','DdLV':'FirstEvaGround','DdkV':'FirstEvaOrbit','DdV':'FirstEvaSpace','DLV':'FirstLanding','DOkV':'FirstOrbitCapsule','DOkKV':'FirstOrbitCapsuleDocked','DdFLV':'FirstPlantFlag','DdRV':'FirstRover','LV':'Landing','OkV':'OrbitCapsule','OkKV':'OrbitCapsuleDocked','dFLV':'PlantFlag','dRV':'Rover','V':'SphereOfInfluence'}
	for bd in ribbonator.bodies:
		if bd.name != 'Asteroid':
			for devN in devsNereid:
				if not (devN in devsNereidSurf and not bd.surface):
					if not (devN in devsNereidAtmo and not bd.atmos):
						if not (devN in devsNereidSolar and not bd.star):
							rib = '%s %s\n'%(bd.name,devN)
							#print([rib])
							output = ribbonator.generate([rib])
							if output is not None:
								f = 'Ribbons/%s/%s.png'%(bd.name,devsNereidNames[devN])
								os.makedirs(os.path.dirname(f), exist_ok=True)
								output.save(f)
