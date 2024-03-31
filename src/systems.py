import numpy as np
import src.geometry as geo

class Miror:
	"""Mirror class.
	Photons are reflected by the mirror.

	Attributes:
	-----------
	pos: tuple
		position
	height: float
		height
	rot: float
		rotation in radians
	color: str
		color
	hitbox: np.ndarray
		hitbox
	"""
	
	def __init__(self, pos: tuple, height: float, rot: float = 0):
		"""Initialize a mirror object.

		Parameters:
		-----------
		pos: tuple
			position
		height: float
			height
		rot: float
			rotation in radians
		"""
		self.pos = pos
		self.height = height
		self.rot = rot
		self.color = 'blue'
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(height/.05))

	def touched(self, photon: any):
		"""Mirror interaction.
		Photon is reflected by the mirror.

		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		photon.dir = np.pi + photon.dir + 2 * (self.rot - photon.dir)


class Screen:
	"""Screen class.
	Photons are stopped by the screen.

	Attributes:
	-----------
	pos: tuple
		position
	height: float
		height
	rot: float
		rotation in radians
	color: str
		color
	hitbox: np.ndarray
		hitbox
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0):
		"""Initialize a screen object.

		Parameters:
		-----------
		pos: tuple
			position
		height: float
			height
		rot: float
			rotation in radians
		"""
		self.pos = pos
		self.height = height
		self.rot = rot
		self.color = 'black'
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(height/.05))
		
	def touched(self, photon):
		"""Screen interaction.
		Photon is stopped.
		
		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		photon.stopped = True
