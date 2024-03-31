import numpy as np

import src.geometry as geo
	
def has_reached_sys(photon: any, systems: any) -> bool:
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

def touched_sys(photon: any, systems: any) -> any:
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
	"""
	Photon class.
	
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
	"""
	def __init__(self, pos: tuple, dir: float, dx: float, n: float = 1):
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
		self.stopped = False
		self.touching = None
	
	def move(self):
		"""Move the photon in the direction of its direction.
		"""
		self.pos = geo.new_pos(self.dir, self.pos, self.dx)
		self.positions.append(self.pos)
