import numpy as np

def new_pos(dir: float, pos: tuple, dx: float) -> tuple:
	"""Calculate the new position of a point.

	Parameters:
	-----------
	dir: float
		direction in radians
	pos: tuple
		position
	dx: float
		step size

	Returns:
	--------
	tuple, new position
	"""
	return np.array(pos) + np.array([np.cos(dir), np.sin(dir)]) * dx
	
def distance(a: tuple, b: float) -> float:
	"""Calculate the distance between two points.

	Parameters:
	-----------
	a: tuple
		first point
	b: tuple
		second point

	Returns:
	--------
	float, distance
	"""
	return np.sqrt(np.sum((b-a)**2, axis=1))
	
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
		if np.min(distance(np.array(photon.pos), np.array(s.hitbox))) < .05:
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
		if np.min(distance(np.array(photon.pos), np.array(s.hitbox)[:])) < .05:
			# When the photon reaches a system, return the system
			return s
	return None	

def is_in(pos: tuple, box: tuple) -> bool:
	"""Check if a point is inside a box.

	Parameters:
	-----------
	pos: tuple
		point
	box: tuple
		box

	Returns:
	--------
	bool, True if the point is inside the box, False otherwise
	"""
	return box[0] < pos[0] < box[2] and box[1] < pos[1] < box[3]


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
		self.pos = new_pos(self.dir, self.pos, self.dx)
		self.positions.append(self.pos)
