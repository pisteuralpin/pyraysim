import matplotlib.pyplot as plt
import numpy as np
import time

# Project modules
from raysim import *
from raysim.systems import Filter, Spectrometer
from raysim.photon import Photon

start_time = time.perf_counter()

# ---------------------------------------------------------------------------- #
#                            Initiate the simulation                           #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

playground = (-10, -10, 15, 10)							# Playground limits
dx = .01												# Step size

initial_rays = [										# Set rays
	Photon((-10, 4.5-.5*i), dir=0, wavelength=380 + 20*i, intensity=1)
	for i in range(20)
]

systems = [												# Set systems
	Filter((0, 2.5), 5, wavelength=475, bandwidth=150),
	Filter((5, 2.5), 5, wavelength=500, bandwidth=50),
	Filter((0, -2.5), 5, wavelength=700, bandwidth=150),
	Filter((5, -2.5), 5, wavelength=725, bandwidth=50),
	Spectrometer((10, 0), 10, passive=False)
]

print("--- Color Filters on rainbow ---")
print("Source position: x = -10")
print("Filters:")
for s in systems:
	if isinstance(s, Filter):
		print(f"   - {s.wavelength}nm ± {s.bandwidth/2}nm")
print("--------------------------------")

print(f"✔ Simulation initiated in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                               Simulate the rays                              #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

rays = simulate(initial_rays, systems, playground, dx = dx)

print(f"✔ Simulation completed in {time.perf_counter() - step_time:.2f}s.")
print(f"   {sum([len(r.positions) for r in rays])/(time.perf_counter() - step_time):.2f} step/s")
print(f"   {len(rays)/(time.perf_counter() - step_time):.2f} rays/s")

# ---------------------------------------------------------------------------- #
#                                Show the scene                                #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

display(rays, systems, playground, title="Color Filters")	# Display simulation

print(f"✔ Simulation plotted in {time.perf_counter() - step_time:.2f}s.")
print(f"   {len(rays)} rays plotted.")
print(f"   {len(systems)} systems plotted.")

# ---------------------------------------------------------------------------- #
#                             End of the simulation                            #
# ---------------------------------------------------------------------------- #

print(f"✅ Simulation completed in {time.perf_counter() - start_time:.2f}s.")

plt.show()												# Show plot