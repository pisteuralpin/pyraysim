import matplotlib.pyplot as plt
import numpy as np
import time

# Project modules
from raysim import simulate
from raysim.systems import Mirror, Screen
from raysim.photon import Photon
import raysim.photon as ph
import raysim.color as col

start_time = time.perf_counter()

# ---------------------------------------------------------------------------- #
#                            Initiate the simulation                           #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

playground = (-20, -10, 15, 10)							# Playground limits
dx = .01												# Step size

source = (-5, 0)										# Source position
rays = [												# Set rays
	Photon(source, 0, dx)
]

systems = [												# Set systems
	Mirror((-10, 0), 5),
	Mirror((0, 0), 5, reflexion = 0.9),
	Mirror((-5,2.5), 10, rot=np.pi/2),
	Mirror((-5,-2.5), 10, rot=np.pi/2),
	Screen((10, 0), 5, measure=True)
]

plt.figure()

print("---- Laser simulation ----")
print(f"Reflexion coefficient: {systems[1].reflexion}")
print("--------------------------")


print(f"✔ Simulation initiated in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                               Simulate the rays                              #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

rays = simulate(rays, systems, playground, dx = dx, max_rays = 100)

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
	

plt.plot(source[0], source[1], '*')						# Plot source

plt.title("Michelson Interferometer")					# Set title

plt.axis('equal')										# Equal aspect ratio
plt.grid()												# Grid on
plt.xlim(playground[0], playground[2])					# Set x limits
plt.ylim(playground[1], playground[3])					# Set y limits
plt.xticks(np.arange(playground[0], playground[2]+1, 5))	# Set x ticks
plt.yticks(np.arange(playground[1], playground[3]+1, 5))	# Set y ticks

print(f"✔ Simulation plotted in {time.perf_counter() - step_time:.2f}s.")
print(f"   ✔ {len(rays)} rays plotted.")
print(f"   ✔ {len(systems)} systems plotted.")

# ---------------------------------------------------------------------------- #
#                             End of the simulation                            #
# ---------------------------------------------------------------------------- #

print(f"✅ Simulation completed in {time.perf_counter() - start_time:.2f}s.")

plt.show()									# Show plot
