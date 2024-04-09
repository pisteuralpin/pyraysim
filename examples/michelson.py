import matplotlib.pyplot as plt
import numpy as np
import time

# Project modules
from raysim.systems import Screen, Mirror
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

source = (-10, 0)										# Source position
rays = [												# Set rays
	Photon(source, .1, dx)
]

systems = [												# Set systems
	Mirror((0, 0), 10, rot = 3*np.pi/4, reflexion = 0.5),
	Mirror((5, 0), 10, 0),
	Mirror((0, 7), 10, np.pi/2),
]

plt.figure()

print("--- Michelson Interferometer ---")
print("Source position:", source)
print("d = 2")
print("--------------------------------")


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
	
print(f"\t✔ {len(rays)} rays plotted.")

# Plot systems
for s in systems:
	plt.plot(
		[s.pos[0] + np.sin(s.rot)*s.height/2, s.pos[0] - np.sin(s.rot)*s.height/2],
		[s.pos[1] - np.cos(s.rot)*s.height/2, s.pos[1] + np.cos(s.rot)*s.height/2],
		color=s.color, linestyle=s.style, linewidth=3)
	
print(f"\t✔ {len(systems)} systems plotted.")

plt.plot(source[0], source[1], '*')						# Plot source

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

plt.show()									# Show plot
