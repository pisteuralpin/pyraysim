import raysim.constants as const

class Source:
    def __init__(self, position, wavelength, power: float = 15):
        self.position = position
        self.wavelength = wavelength
        self.power = power

    def __str__(self):
        return f"Source at {self.position}"
    
    def __repr__(self):
        return f"Source(position={self.position}, wavelength={self.wavelength}, power={self.power})"