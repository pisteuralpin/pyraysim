def wavelength_to_color(wavelength: float) -> tuple[int]:
	"""Convert wavelength to color.
	Credits: work of Dan Bruton, http://www.physics.sfasu.edu/astro/color/spectra.html

	Parameters:
	-----------
	wavelength: float
		wavelength in nm

	Returns:
	--------
	color: tuple
		rgb color
	"""
	color = (0, 0, 0)
	if 380 <= wavelength < 440:
		color = (-(wavelength - 440) / (440 - 380), 0.0, 1.0)
	elif 440 <= wavelength < 490:
		color = (0.0, (wavelength - 440) / (490 - 440), 1.0)
	elif 490 <= wavelength < 510:
		color = (0.0, 1.0, -(wavelength - 510) / (510 - 490))
	elif 510 <= wavelength < 580:
		color = ((wavelength - 510) / (580 - 510), 1.0, 0.0)
	elif 580 <= wavelength < 645:
		color = (1.0, -(wavelength - 645) / (645 - 580), 0.0)
	elif 645 <= wavelength < 781:
		color = (1.0, 0.0, 0.0)
	else:
		color = (0.0, 0.0, 0.0)

	if 380 <= wavelength < 420:
		factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
	elif 420 <= wavelength < 701:
		factor = 1.0
	elif 701 <= wavelength < 781:
		factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
	else:
		factor = 0.0
	color = tuple(int(255 * x * factor) for x in color)
	return color

def rgb_to_matplotlib(rgb: tuple[int]) -> tuple[float]:
	"""Convert rgb to matplotlib color.

	Parameters:
	-----------
	rgb: tuple
		rgb color
	
	Returns:
	--------
	matplotlib_color: tuple
		matplotlib color
	"""
	return (rgb[0]/255, rgb[1]/255, rgb[2]/255)

def rbg_to_hex(rgb, alpha = None) -> str:
	"""Convert rgb to hex.
	
	Parameters:
	-----------
	rgb: tuple
		rgb color
	alpha: float, optional (default=None)
		alpha value
	
	Returns:
	--------
	hex: str
		hex color
	"""
	if alpha == None:
		return '#' + ''.join(['%02x'%rgb[i] for i in range(3)])
	else:
		return '#' + ''.join(['%02x'%rgb[i] for i in range(3)]) + '%02x'%int(alpha*255)
