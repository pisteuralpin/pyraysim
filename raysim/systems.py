import numpy as np
import copy
from json import dumps

import raysim.geometry as geo
import raysim.photon as ph
import raysim.color as col

# ---------------------------------------------------------------------------- #
#                                    Systems                                   #
# ---------------------------------------------------------------------------- #

class System:
	"""System class.
	Abstract class for optical systems.

	Attributes:
	-----------
	Methods:
	--------
	touched(photon)
		System interaction.
	move(new_pos, rot=None)
		Move the system.
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0):
		"""Initialize a system object."""
		self.pos = pos
		self.height = height
		self.rot = rot
		
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(height/.05))

	def __str__(self):
		return f"{type(self).__name__} at {self.pos}"

	def move(self, new_pos: tuple[float], rot: float = None):
		"""Move the system.

		Parameters:
		-----------
		new_pos: tuple
			new position
		rot: float, optional
			new rotation
		"""
		self.pos = new_pos
		if rot != None:
			self.rot = rot
		self.hitbox = np.linspace(
			[self.pos[0] - np.sin(self.rot)*self.height/2, self.pos[1] + np.cos(self.rot)*self.height/2],
			[self.pos[0] + np.sin(self.rot)*self.height/2, self.pos[1] - np.cos(self.rot)*self.height/2],
			int(self.height/.05))

class Mirror(System):
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
	move(new_pos, rot=None)
		Move the mirror.
	reset()
		Reset the mirror: not used.
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
		super().__init__(pos, height, rot)

		self.color = col.rbg_to_hex((0,12,135), reflexion**.5)
		self.style = '-'
		
		self.reflexion = reflexion

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

class Screen(System):
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
	measure: bool
		Does the screen measure intensities
	measures: dict
		measures
	hitbox: np.ndarray
		hitbox

	Methods:
	--------
	touched(photon)
		Screen interaction.
	move(new_pos, rot=None)
		Move the screen.
	reset()
		Reset the screen: clear measures.
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0, measure: bool = False):
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
		super().__init__(pos, height, rot)
		
		self.color = 'black'
		self.style = '-'

		self.measure = measure
		self.measures = {}
		
	def touched(self, photon: ph.Photon, rays: list = None):
		"""Screen interaction.
		Photon is stopped.
		
		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		photon.stopped = True
		if self.measure:
			if photon.wavelength not in self.measures:
				self.measures[photon.wavelength] = 0
			self.measures[photon.wavelength] += photon.intensity
		
	def reset(self):
		"""Reset the screen."""
		self.measures = {}

	def print_measures(self):
		"""Print measures."""
		print(f"   {self} :")
		print("      " + str(self.measures))


class Filter(System):
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
	move(new_pos, rot=None)
		Move the filter.
	reset()
		Reset the filter: not used.
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0,
		wavelength: float = 600, bandwidth: float = 50):
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
		super().__init__(pos, height, rot)

		self.color = col.rbg_to_hex(col.wavelength_to_color(wavelength))
		self.style = 'dashed'

		self.wavelength = wavelength
		self.bandwidth = bandwidth
		
	def __str__(self):
		return f"Filter at {self.pos}"
		
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


# ---------------------------------------------------------------------------- #
#                                Instrumentation                               #
# ---------------------------------------------------------------------------- #

class Instrumentation(System):
	"""Instrumentation class.
	Abstract class for optical instrumentation.

	Attributes:
	-----------
	Methods:
	--------
	touched(photon)
		Instrumentation interaction.
	move(new_pos, rot=None)
		Move the instrumentation.
	
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0, passive: bool = True):
		"""Initialize an instrumentation object."""
		super().__init__(pos, height, rot)

		self.passive = passive
		self.measures = {}
		
	def print_measures(self):
		"""Print measures."""
		print(f"- {self}:")
		print(dumps(self.measures, indent=4))
		
	def reset(self):
		"""Reset the instrumentation."""
		self.measures = {}


class Spectrometer(Instrumentation):
	"""Spectrometer class.
	Photons wavelength is measured by the spectrometer.

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
	measures: dict
		measures
	hitbox: np.ndarray
		hitbox

	Methods:
	--------
	touched(photon)
		Spectrometer interaction.
	move(new_pos, rot=None)
		Move the spectrometer.
	reset()
		Reset the spectrometer.
	"""

	def __init__(self, pos: tuple, height: float, rot: float = 0, passive: bool = True):
		"""Initialize a spectrometer object.

		Parameters:
		-----------
		pos: tuple
			position
		height: float
			height
		rot: float, optional (default=0)
			rotation in radians
		"""
		super().__init__(pos, height, rot, passive)
		
		self.color = 'black'
		self.style = '-'
		
	def touched(self, photon: ph.Photon, rays: list = None):
		"""Spectrometer interaction.
		Photon wavelength is measured.
		
		Parameters:
		-----------
		photon: Photon
			photon object
		"""
		if photon.wavelength not in self.measures:
			self.measures[photon.wavelength] = 0
		self.measures[photon.wavelength] += photon.intensity
		if not self.passive:
			photon.stopped = True