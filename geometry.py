import numpy as np

	
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

def polygon_mesh(poly: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
	"""Create a meshgrid from a polygon.

	Parameters:
	-----------
	poly: np.ndarray
		polygon

	Returns:
	--------
	np.ndarray, np.ndarray
		meshgrid
	"""
	X = np.linspace(np.min(poly[:,0]), np.max(poly[:, 0]))
	Y = np.linspace(np.min(poly[:,1]), np.max(poly[:, 1]))
	return np.meshgrid(X, Y)
	
def is_on_segment(pt: tuple, p1: tuple, p2: tuple, tolerance: float = .1) -> bool:
	"""Check if a point is on a segment.

	Parameters:
	-----------
	pt: tuple
		point
	p1: tuple
		first point of the segment
	p2: tuple
		second point of the segment
	tolerance: float
		tolerance
		
	Returns:
	--------
	bool, True if the point is on the segment, False otherwise
	"""
	return distance(np.array(pt), np.array(p1)) + distance(np.array(pt), np.array(p2)) - distance(np.array(p1), np.array(p2)) < tolerance

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