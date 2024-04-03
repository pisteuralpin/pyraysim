import raysim.photons as ph
import raysim.geometry as geo

def simulate(rays, systems, playground, max_iterations = 10000, dx = 0.01):
	# Simulate rays and calculate interactions
	for p in rays:
		while not p.stopped and len(p.positions) < max_iterations:
			p.move()
			if ph.has_reached_sys(p, systems) and p.touching == None:
				p.touching = ph.touched_sys(p, systems)
				p.touching.touched(p, rays = rays)
			elif not ph.has_reached_sys(p, systems) and p.touching != None:
				p.touching = None
			if not geo.is_in(p.pos, playground):
				p.stopped = True
