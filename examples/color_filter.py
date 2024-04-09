import matplotlib.pyplot as plt
import numpy as np
import time

# Project modules
from raysim.systems import Filter
from raysim.photons import Photon
import raysim.photons as ph
import raysim.simulation as sim
import raysim.color as col

start_time = time.perf_counter()

# ---------------------------------------------------------------------------- #
#                            Initiate the simulation                           #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

playground = (-20, -15, 20, 15)							# Playground limits
dx = .01												# Step size

rays = [												# Set rays
	Photon((-10, 4.5-.5*i), 0, dx, wavelength=380 + 20*i, intensity=1)
	for i in range(20)
]

systems = [												# Set systems
	Filter((10, 0), 10, wavelenth=500, bandwidth=50),
	Filter((5, 0), 10, wavelenth=475, bandwidth=150),
]

print("--- Color Filter on rainbow ---")
print("Source position: x = -10")
print("First filter: 500nm +/- 25nm")
print("Second filter: 475nm +/- 75nm")
print("-------------------------------")

plt.figure()

print(f"✔ Simulation initiated in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                               Simulate the rays                              #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

sim.simulate(rays, systems, playground, dx = dx)

print(f"✔ Simulation completed in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                                Show the scene                                #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

for p in rays:
	plt.plot(np.array(p.positions)[:,0], np.array(p.positions)[:,1], 
		color= col.rbg_to_hex(p.color, p.intensity))	# Plot ray
	
print(f"\t {len(rays)} rays plotted.")

# Plot systems
for s in systems:
	plt.plot(
		[s.pos[0] + np.sin(s.rot)*s.height/2, s.pos[0] - np.sin(s.rot)*s.height/2],
		[s.pos[1] - np.cos(s.rot)*s.height/2, s.pos[1] + np.cos(s.rot)*s.height/2],
		color=s.color, linestyle=s.style, linewidth=3)
	
print(f"\t {len(systems)} systems plotted.")


plt.axis('equal')										# Equal aspect ratio
plt.grid()												# Grid on
plt.xlim(playground[0], playground[2])					# Set x limits
plt.ylim(playground[1], playground[3])					# Set y limits
plt.xticks(np.arange(playground[0], playground[2]+1, 5))	# Set x ticks
plt.yticks(np.arange(playground[1], playground[3]+1, 5))	# Set y ticks

print(f"✔ Simulation plotted in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                             End of the simulation                            #
# ---------------------------------------------------------------------------- #

print(f"✅ Simulation completed in {time.perf_counter() - start_time:.2f}s.")

plt.show()												# Show plot