import numpy as np

import raysim.geometry as geo
import raysim.color as col
from raysim.source import Source
	
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
	def __init__(self, source: Source | tuple[float], pos: tuple[float] = None, dir: float = 0, dx: float = .01,
		n: float = 1, intensity: float = 1, touching: any = None, wavelength: int = 650, virtual_source: tuple[float] = None):
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
			self.dir = dir

			if isinstance(source, Source):
				self.source = source
			elif isinstance(source, tuple):
				self.source = Source(source, wavelength, intensity)
			else:
				raise ValueError("Source must be a Source or a tuple.")
			
			if pos == None:
				self.pos = self.source.position
			else:
				self.pos = pos

			self.dx = dx
			self.positions = [self.pos]
			self.directions = [self.dir]
			if virtual_source == None:
				self.virtual_source = self.pos
			else:
				self.virtual_source = virtual_source
			
			self.n = n
			self.intensity = intensity
			self.stopped = False
			self.touching = touching
			
			self.wavelength = wavelength
			
			self.color = col.wavelength_to_color(wavelength)
	
	def __str__(self) -> str:
		"""Return the string representation of the photon.
		"""
		return f"Photon at {self.pos}"
	
	def __repr__(self) -> str:
		"""Return the string representation of the photon.
		"""
		return f"Photon(pos={self.pos}, dir={self.dir}, dx={self.dx}, n={self.n}, intensity={self.intensity}, touching={self.touching}, wavelength={self.wavelength})"
	
	def move(self):
		"""Move the photon in the direction of its direction.
		"""
		self.pos = geo.new_pos(self.dir, self.pos, self.dx)
		self.positions.append(self.pos)