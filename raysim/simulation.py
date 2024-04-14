import numpy as np
from matplotlib.pyplot import Axes, subplots
import copy
import time

import raysim.photon as ph
import raysim.geometry as geo
import raysim.color as col
from raysim.systems import System, Instrumentation
import raysim.source as src

def simulate(initial_rays: list[ph.Photon], systems: list[System], playground: tuple, dx: float = 0.01, max_iterations: int = 10000, max_rays: int = 20, resimulate: bool = False, print_status: bool = True, print_measures: bool = True, print_stats: bool = True) -> list[ph.Photon]:
	"""Simulate the rays.

	Parameters:
	-----------
	initial_rays: list
		list of rays
	systems: list
		list of systems
	playground: tuple
		playground limits
	dx: float, optional (default = 0.01)
		step size
	max_iterations: int, optional (default = 10000)
		maximum number of iterations
	max_rays: int, optional (default = 20)
		maximum number of rays
	resimulate: bool, optional (default = False)
		resimulate the rays
	print_status: bool, optional (default = True)
		print status messages
	print_measures: bool, optional (default = True)
		print measures of systems
	print_stats: bool, optional (default = True)
		print simulation statistics
	
	Returns:
	--------
	rays: list
		list of rays
	"""

	start_time = time.perf_counter()
	# Simulate rays and calculate interactions
	rays = copy.deepcopy(initial_rays)

	if print_status and resimulate:
		print("---")
		print("⚙️  Resimulating...")

	# Reset systems
	for s in systems:
		if isinstance(s, Instrumentation):
			s.reset()

	# Simulate rays
	for p in rays:
		p.dx = dx
		while not p.stopped and len(p.positions) <= max_iterations:
			p.move()
			if ph.has_reached_sys(p, systems) and p.touching == None:
				p.touching = ph.touched_sys(p, systems)
				p.touching.touched(p, rays = rays)
			elif not ph.has_reached_sys(p, systems) and p.touching != None:
				p.touching = None
			if not geo.is_in(p.pos, playground):
				p.stopped = True
		if len(rays) > max_rays:
			break

	# Print measures
	if print_measures:
		for s in systems:
			if isinstance(s, Instrumentation):
				print("--- Measures ---")
				s.print_measures()
				print("----------------")

	if print_status:
		if resimulate:
			print(f"✅ Resimulation calculated in {time.perf_counter() - start_time:.2f}s.")
		else:
			print(f"✔ Simulation calculated in {time.perf_counter() - start_time:.2f}s.")
	if print_stats:
		print(f"   {sum([len(r.positions) for r in rays])/(time.perf_counter() - start_time):.2f} step/s")
		print(f"   {len(rays)/(time.perf_counter() - start_time):.2f} rays/s")

	return rays


def display(rays: list[ph.Photon], systems: list[any], playground: tuple, sources: list[src.Source] | tuple[float] = None, ax: Axes = None, title: str = None) -> None:
	"""Display the simulation.

	Parameters:
	-----------
	rays: list
		list of rays
	systems: list
		list of systems
	playground: tuple
		playground limits
	source: tuple
		source position
	ax: matplotlib.pyplot.Axes object, optional (default = subplots()[1])
		axis
	"""
	if ax == None:
		fig, ax = subplots(num=title)					# Create figure and axis
	
	ax.clear()											# Clear axis
	# Plot rays
	for p in rays:
		ax.plot(np.array(p.positions)[:,0], np.array(p.positions)[:,1], 
			color= col.rbg_to_hex(p.color, p.intensity))	# Plot ray

	# Plot systems
	for s in systems:
		ax.plot(
			[s.pos[0] - np.sin(s.rot)*s.height/2, s.pos[0] + np.sin(s.rot)*s.height/2],
			[s.pos[1] + np.cos(s.rot)*s.height/2, s.pos[1] - np.cos(s.rot)*s.height/2],
			color = s.color, linestyle = s.style
		)

	if sources != None and isinstance(sources, list):
		sources_pos = np.array([s.position for s in sources])
		ax.plot(sources_pos[:,0], sources_pos[:,1], '*', color = 'black')	# Plot sources
	elif sources != None and isinstance(sources, tuple):
		ax.plot(sources[0], sources[1], '*', color = 'black')

	ax.axis('equal')									# Equal aspect ratio
	ax.grid()											# Grid on
	ax.set_xlim(playground[0], playground[2])			# Set x limits
	ax.set_ylim(playground[1], playground[3])			# Set y limits
	ax.set_xticks(np.arange(playground[0], playground[2]+1, 5))	# Set x ticks
	ax.set_yticks(np.arange(playground[1], playground[3]+1, 5))	# Set y ticks
	ax.set_title(title)									# Set title