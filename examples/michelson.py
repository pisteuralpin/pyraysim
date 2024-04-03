import matplotlib.pyplot as plt
import numpy as np

# Project modules
from raysim.systems import Screen, Mirror
from raysim.photons import Photon
import raysim.photons as ph
import raysim.simulation as sim

playground = (-20, -15, 20, 15)							# Playground limits
dx = .01												# Step size

source = (-10, 0)											# Source position
rays = [												# Set rays
	Photon(source, .1, dx)
]

systems = [												# Set systems
	Mirror((0, 0), 10, rot = 3*np.pi/4, reflexion = 0.5),
	Mirror((5, 0), 10, 0),
	Mirror((0, 7), 10, np.pi/2),
]

plt.figure()

sim.simulate(rays, systems, playground, dx = dx)

for p in rays:
	plt.plot(np.array(p.positions)[:,0], np.array(p.positions)[:,1], 
		color= list(ph.rgb_to_matplotlib(p.color)) + [p.intensity])	# Plot ray


# Plot systems
for s in systems:
	plt.plot(
		[s.pos[0] + np.sin(s.rot)*s.height/2, s.pos[0] - np.sin(s.rot)*s.height/2],
		[s.pos[1] - np.cos(s.rot)*s.height/2, s.pos[1] + np.cos(s.rot)*s.height/2],
		color=s.color )

plt.plot(source[0], source[1], '*')						# Plot source

plt.axis('equal')										# Equal aspect ratio
plt.grid()												# Grid on
plt.xlim(playground[0], playground[2])					# Set x limits
plt.ylim(playground[1], playground[3])					# Set y limits
plt.xticks(np.arange(playground[0], playground[2]+1, 5))	# Set x ticks
plt.yticks(np.arange(playground[1], playground[3]+1, 5))	# Set y ticks
plt.show()									# Show plot
