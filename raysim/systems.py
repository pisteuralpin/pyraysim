import numpy as np
import copy

import raysim.geometry as geo

class Mirror:
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

	Methods:
	--------
	touched(photon)
		Mirror interaction.
	"""
	
	def __init__(self, pos: tuple, height: float, rot: float = 0,
		reflexion: float = 1):
		"""Initialize a mirror object.

		Parameters:
		-----------
		pos: tuple
			position
		height: float
			height
		rot: float
			rotation in radians
		reflexion: float
			reflexion coefficient [0,1]
		"""
		self.pos = pos
		self.height = height
		self.rot = rot
		self.reflexion = reflexion
		self.color = 'blue'
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(height/.05))

	def touched(self, photon: any, rays: list):
		"""Mirror interaction.
		Photon is reflected by the mirror.

		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		if self.reflexion != 1:
			through = copy.deepcopy(photon)
			through.positions = [photon.pos]
			through.intensity *= 1 - self.reflexion
			rays.append(through)
			
			reflected = copy.deepcopy(photon)
			reflected.positions = [photon.pos]
			reflected.intensity *= self.reflexion
			reflected.dir = np.pi + 2 * self.rot - photon.dir
			rays.append(reflected)
			
			photon.stopped = True
		else:
			photon.dir = np.pi + 2 * self.rot - photon.dir
			photon.intensity *= self.reflexion

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

	Methods:
	--------
	touched(photon)
		Screen interaction.
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
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] +
				np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] -
				np.cos(self.rot)*self.height/2],
			int(height/.05))
		
	def touched(self, photon: any, rays: list = None):
		"""Screen interaction.
		Photon is stopped.
		
		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		photon.stopped = True
