import matplotlib.pyplot as plt
import numpy as np

# Project modules
from src.systems import Screen, Miror
from src.photons import Photon
import src.photons as t

plt.ion()												# Interactive mode on

playground = (-15, -15, 15, 15)							# Playground limits
dx = .01												# Step size

source = (0, 0)											# Source position
rays = [												# Set rays
	Photon(source, 0, dx)
]

systems = [												# Set systems
	Miror((10, 0), 5, 3*np.pi/4),
	Miror((10, 7.5), 5, np.pi/4),
	Screen((0, 7.5), 5, 0)
]

plt.figure()
plt.plot(source[0], source[1], '*')						# Plot source

# Plot systems
for s in systems:
	plt.plot([s.pos[0] + np.sin(s.rot)*s.height/2, s.pos[0] - np.sin(s.rot)*s.height/2], [s.pos[1] - np.cos(s.rot)*s.height/2, s.pos[1] + np.cos(s.rot)*s.height/2], color=s.color)

# Simulate rays and calculate interactions
for p in rays:
	while not p.stopped:
		p.move()
		if t.has_reached_sys(p, systems):
			if p.touching == None:
				p.touching = t.touched_sys(p, systems)
				p.touching.touched(p)
		else: p.touching = None
		if not t.is_in(p.pos, playground):
			p.stopped = True
	plt.plot(np.array(p.positions)[:,0], np.array(p.positions)[:,1], 'y')		# Plot ray

plt.axis('equal')										# Equal aspect ratio
plt.grid()												# Grid on
plt.xlim(playground[0], playground[2])					# Set x limits
plt.ylim(playground[1], playground[3])					# Set y limits
plt.xticks(np.arange(playground[0], playground[2]+1, 5))	# Set x ticks
plt.yticks(np.arange(playground[1], playground[3]+1, 5))	# Set y ticks
plt.show(block=True)									# Show plot