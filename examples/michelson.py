import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import time

# Project modules
from raysim import simulate, display
from raysim.systems import Screen, Mirror
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

e = 2

source = (-10, 0)										# Source position
initial_rays = [										# Set rays
	Photon(source, .1, dx)
]

systems = [												# Set systems
	Mirror((0, 0), 10, rot = 3*np.pi/4, reflexion = 0.5),
	Mirror((5+e, 0), 10, 0),
	Mirror((0, 5), 10, np.pi/2)
]

print("--- Michelson Interferometer ---")
print("Source position:", source)
print("d = 2")
print("Incidence angle: 0.1 rad")
print("--------------------------------")


print(f"✔ Simulation initiated in {time.perf_counter() - step_time:.2f}s.")

# ---------------------------------------------------------------------------- #
#                               Simulate the rays                              #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

rays = simulate(initial_rays, systems, playground, dx = dx)

# ---------------------------------------------------------------------------- #
#                                Show the scene                                #
# ---------------------------------------------------------------------------- #

step_time = time.perf_counter()

fig, ax = plt.subplots()								# Create figure and axis

display(ax, rays, systems, playground, source)			# Display the scene

# ax.plot((5, systems[1].pos[0]), (0, 0), 'k--')			# Plot the path difference
ax.annotate("e", xy=(5 + (systems[1].pos[0] - 5)/2 - .3, .5))	# Annotate the path difference
ax.annotate("", xy=(4.9, 0), xytext=(systems[1].pos[0]+.1, 0), arrowprops=dict(arrowstyle="<->"))	# Annotate the path difference

plt.title("Michelson Interferometer")					# Set title

fig.subplots_adjust(bottom=0.25)
e_ax = fig.add_axes([0.18, 0.1, 0.65, 0.03])
e_slider = Slider(e_ax, 'e', 0, 5, valinit=2)

def update(val):
	e = e_slider.val
	systems[1].move((5+e, 0))
	rays = simulate(initial_rays, systems, playground, dx = dx, resimulate=True)
	display(ax, rays, systems, playground, source)
	ax.annotate("e", xy=(5 + (systems[1].pos[0] - 5)/2 - .3, .5))	# Annotate the path difference
	ax.annotate("", xy=(4.9, 0), xytext=(systems[1].pos[0]+.1, 0), arrowprops=dict(arrowstyle="<->"))	# Annotate the path difference

e_slider.on_changed(update)

print(f"✔ Simulation plotted in {time.perf_counter() - step_time:.2f}s.")
print(f"   ✔ {len(rays)} rays plotted.")
print(f"   ✔ {len(systems)} systems plotted.")

# ---------------------------------------------------------------------------- #
#                             End of the simulation                            #
# ---------------------------------------------------------------------------- #

print(f"✅ Simulation completed in {time.perf_counter() - start_time:.2f}s.")

plt.show()									# Show plot
