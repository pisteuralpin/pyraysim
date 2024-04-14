import matplotlib.pyplot as plt
import numpy as np
import time

# Project modules
from raysim import *
from raysim.systems import Mirror, Screen
from raysim.photon import Photon
from raysim.source import Source

start_time = time.perf_counter()

# ---------------------------------------------------------------------------- #
#                            Initiate the simulation                           #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

playground = (-20, -10, 15, 10)							# Playground limits
dx = .01												# Step size

sources = [												# Set sources
	Source((-5, 0), 575, 1e-3)
]


rays = [												# Set rays
	Photon(sources[0], dir=0)
]

systems = [												# Set systems
	Mirror((-10, 0), 5),
	Mirror((0, 0), 5, reflexion = 0.9),
	Mirror((-5,2.5), 10, rot=np.pi/2),
	Mirror((-5,-2.5), 10, rot=np.pi/2),
	Screen((10, 0), 5)
]

print("---- Laser simulation ----")
print(f"Reflexion coefficient: {systems[1].reflexion}")
print("--------------------------")


print(f"✔ Simulation initiated in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                               Simulate the rays                              #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

rays = simulate(rays, systems, playground, dx = dx, max_rays = 20)

# ---------------------------------------------------------------------------- #
#                                Show the scene                                #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

display(rays, systems, playground, sources, title="Laser")			# Display simulation

print(f"✔ Simulation plotted in {time.perf_counter() - step_time:.2f}s.")
print(f"   ✔ {len(rays)} rays plotted.")
print(f"   ✔ {len(systems)} systems plotted.")

# ---------------------------------------------------------------------------- #
#                             End of the simulation                            #
# ---------------------------------------------------------------------------- #

print(f"✅ Simulation completed in {time.perf_counter() - start_time:.2f}s.")

plt.show()												# Show plot
