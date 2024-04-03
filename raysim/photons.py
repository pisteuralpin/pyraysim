import numpy as np

import raysim.geometry as geo
	
def has_reached_sys(photon: any, systems: list[any]) -> bool:
	"""Check if the photon has reached a system.

	Parameters:
	-----------
	photon: any
		photon object
	systems: any
		systems list

	Returns:
	--------
	bool, True if the photon has reached a system, False otherwise
	"""
	for s in systems:
		if np.min(geo.distance(np.array(photon.pos), np.array(s.hitbox))) < .05:
			# When the photon reaches a system, return True
			return True
	return False

def touched_sys(photon: any, systems: list[any]) -> any:
	"""Return the system that the photon has reached.

	Parameters:
	-----------
	photon: any
		photon object
	systems: any
		systems list
		
	Returns:
	--------
	any, system object
	"""
	for s in systems:
		if np.min(geo.distance(np.array(photon.pos), np.array(s.hitbox)[:])) < .05:
			# When the photon reaches a system, return the system
			return s
	return None

def wavelength_to_color(wavelength: float):
	colors = {
		380: (41, 33, 85, '#292155'),
		440: (46, 39, 108, '#2e276c'),
		466: (33, 57, 117, '#213975'),
		478: (12, 71, 105, '#0c4769'),
		483: (18, 81, 99, '#125163'),
		490: (12, 115, 96, '#0c7360'),
		510: (39, 171, 109, '#27ab6d'),
		541: (98, 178, 46, '#62b22e'),
		573: (202, 179, 6, '#cab306'),
		575: (211, 169, 12, '#d3a90c'),
		579: (214, 147, 6, '#d69306'),
		584: (222, 132, 9, '#de8409'),
		588: (231, 120, 6, '#e77806'),
		593: (233, 83, 19, '#e95313'),
		605: (228, 11, 36, '#e40b24'),
		622: (121, 20, 38, '#791426')
	}
	latest_c = min(colors)
	for c in colors:
		if wavelength < c: return colors[latest_c]
		latest_c = c
	return colors[c]

def rgb_to_matplotlib(rgb):
	return (rgb[0]/255, rgb[1]/255, rgb[2]/255)

class Photon:
	"""Photon class.
	
	Attributes:
	-----------
	pos: tuple
		photon position
	dir: float
		photon direction in radians
	dx: float
		step size
	positions: list
		photon positions
	directions: list
		photon directions
	n: float
		refractive index
	stopped: bool
		photon status
	touching: any
		touched system

	Methods:
	--------
	move()
		Move the photon in the direction of its direction.
	"""
	def __init__(self, pos: tuple, dir: float, dx: float,
		n: float = 1, intensity: float = 1, touching: any = None, wavelength: int = 575,
		wavelengths: dict[int: float] = {}):
			"""Initialize a photon object.

		Parameters:
		-----------
		pos: tuple
			photon position
		dir: float
			photon direction in radians
		dx: float
			step size
		n: float, optional (default=1)
			refractive index
		"""
			self.pos = pos
			self.dir = dir
			self.dx = dx
			self.positions = [pos]
			self.directions = [dir]
			self.n = n
			self.intensity = intensity
			self.stopped = False
			self.touching = touching
			
			self.wavelength = wavelength
			self.wavelengths = wavelengths
			
			if wavelengths == {}:
				self.wavelengths = {self.wavelength: self.intensity}
			else:
				self.wavelength = np.average(list(self.wavelengths.keys()),
					weights = list(self.wavelengths.values()) )
			
			intensity_sum = sum(self.wavelengths.values())
			self.wavelengths = {
				key: value/intensity_sum
				for (key, value) in self.wavelengths.items() }
			
			self.color = wavelength_to_color(self.wavelength)[:3]
	
	def move(self):
		"""Move the photon in the direction of its direction.
		"""
		self.pos = geo.new_pos(self.dir, self.pos, self.dx)
		self.positions.append(self.pos)
