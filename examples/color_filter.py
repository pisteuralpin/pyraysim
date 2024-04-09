import matplotlib.pyplot as plt
import numpy as np
import time

# Project modules
from raysim import simulate
from raysim.systems import Filter
from raysim.photon import Photon
import raysim.photon as ph
import raysim.color as col

start_time = time.perf_counter()

# ---------------------------------------------------------------------------- #
#                            Initiate the simulation                           #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

playground = (-10, -10, 15, 10)							# Playground limits
dx = .01												# Step size

rays = [												# Set rays
	Photon((-10, 4.5-.5*i), 0, dx, wavelength=380 + 20*i, intensity=1)
	for i in range(20)
]

systems = [												# Set systems
	Filter((0, 2.5), 5, wavelength=475, bandwidth=150),
	Filter((5, 2.5), 5, wavelength=500, bandwidth=50),
	Filter((0, -2.5), 5, wavelength=700, bandwidth=150),
	Filter((5, -2.5), 5, wavelength=725, bandwidth=50),
]

print("--- Color Filters on rainbow ---")
print("Source position: x = -10")
print("Filters:")
for s in systems:
	print(f"   - {s.wavelength}nm ± {s.bandwidth/2}nm")
print("-------------------------------")

plt.figure()

print(f"✔ Simulation initiated in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                               Simulate the rays                              #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

simulate(rays, systems, playground, dx = dx)

print(f"✔ Simulation completed in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                                Show the scene                                #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

for p in rays:
	plt.plot(np.array(p.positions)[:,0], np.array(p.positions)[:,1], 
		color= col.rbg_to_hex(p.color, p.intensity))	# Plot ray

# Plot systems
for s in systems:
	plt.plot(
		[s.pos[0] + np.sin(s.rot)*s.height/2, s.pos[0] - np.sin(s.rot)*s.height/2],
		[s.pos[1] - np.cos(s.rot)*s.height/2, s.pos[1] + np.cos(s.rot)*s.height/2],
		color=s.color, linestyle=s.style, linewidth=3)

plt.title("Color Filters on rainbow")

plt.axis('equal')										# Equal aspect ratio
plt.grid()												# Grid on
plt.xlim(playground[0], playground[2])					# Set x limits
plt.ylim(playground[1], playground[3])					# Set y limits
plt.xticks(np.arange(playground[0], playground[2]+1, 5))	# Set x ticks
plt.yticks(np.arange(playground[1], playground[3]+1, 5))	# Set y ticks

print(f"✔ Simulation plotted in {time.perf_counter() - step_time:.2f}s.")
print(f"   {len(rays)} rays plotted.")
print(f"   {len(systems)} systems plotted.")

# ---------------------------------------------------------------------------- #
#                             End of the simulation                            #
# ---------------------------------------------------------------------------- #

print(f"✅ Simulation completed in {time.perf_counter() - start_time:.2f}s.")

plt.show()												# Show plot