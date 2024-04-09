import numpy as np
import copy

import raysim.geometry as geo
import raysim.photons as ph
import raysim.color as col

class Mirror:
	"""Mirror class.
	Photons are reflected by the mirror.

	Attributes:
	-----------
	pos: tuple(float, float)
		position
	height: float
		height
	rot: float
		rotation in radians
	color: str
		color in hex
	line style: str
		line style
	reflexion: float
		reflexion coefficient [0,1]
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

		self.color = col.rbg_to_hex((0,12,135), reflexion**.5)
		self.style = '-'
		
		self.reflexion = reflexion
		
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(height/.05))

	def touched(self, photon: ph.Photon, rays: list[ph.Photon]):
		"""Mirror interaction.
		Photon is reflected by the mirror.

		Parameters:
		-----------
		photon: Photon
			photon object
		rays: list
			list of rays
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
		color in hex
	line style: str
		line style
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
		rot: float, optional (default=0)
			rotation in radians
		"""
		self.pos = pos
		self.height = height
		self.rot = rot

		self.color = 'black'
		self.style = '-'
		
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] +
				np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] -
				np.cos(self.rot)*self.height/2],
			int(height/.05))
		
	def touched(self, photon: ph.Photon, rays: list = None):
		"""Screen interaction.
		Photon is stopped.
		
		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		photon.stopped = True		

		
class Filter:
	"""Filter class.
	Photons wavelength is filtered by the filter.

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
	line style: str
		line style
	wavelength: float
		middle bandwidth wavelength
	bandwidth: float
		wavelength bandwidth
	hitbox: np.ndarray
		hitbox

	Methods:
	--------
	touched(photon)
		Screen interaction.
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0,
		wavelenth: float = 600, bandwidth: float = 50):
		"""Initialize a filter object.

		Parameters:
		-----------
		pos: tuple
			position
		height: float
			height
		rot: float, optional (default=0)
			rotation in radians
		wavelength: float, optional (default=600)
			middle bandwidth wavelength
		bandwidth: float, optional (default=50)
			wavelength bandwidth - only keep photons between wavelength - bandwidth/2 and wavelength + bandwidth/2
		"""
		self.pos = pos
		self.height = height
		self.rot = rot

		self.color = col.rbg_to_hex(col.wavelength_to_color(wavelenth))
		self.style = 'dashed'

		self.wavelength = wavelenth
		self.bandwidth = bandwidth

		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(height/.05))
		
	def touched(self, photon: ph.Photon, rays: list = None):
		"""Filter interaction.
		Photon wavelengths are filtered.
		
		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		if abs(photon.wavelength - self.wavelength) > self.bandwidth/2:
			photon.stopped = True
