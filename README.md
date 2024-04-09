# pyraysim
Rays simulation in python.

## Systems
- Miror
    > Reflects rays.
- Screen
    > Stops rays.
- Color filter
    > Only lets rays of a certain color pass.

## Examples
- Michelson interferometer
  <br/><img src="./docs/img/michelson.png?raw=True" style="display: block; height: 15rem;" />
- Color filter
  <br/><img src="./docs/img/color_filter.png?raw=True" style="display: block; height: 15rem;" />

## Usage
```python
import numpy as np
import matplotlib.pyplot as plt

from raysim import *
from raysim.systems import *
from raysim.photon import Photon
import raysim.color as color

playground = (-20, -10, 15, 10)

rays = [
    Photon((-0.5, 0), np.pi/2, wavelength=400),
    Photon((0, 0), np.pi/2, wavelength=500),
    Photon((0.5, 0), np.pi/2, wavelength=700),
]

systems = [
    Mirror((0, 5), height=2, rot=3*np.pi/4),
    Filter((5, 5), height=2, rot=0, wavelength=500, bandwidth=50),
    Screen((10, 5), height=2, rot=0)
]

simulate(rays, systems, playground, dx=.01)

for ray in rays:
    plt.plot(np.array(ray.positions)[:,0], np.array(ray.positions)[:,1], 
		color= color.rbg_to_hex(ray.color, ray.intensity))

for s in systems:
	plt.plot(
		[s.pos[0] + np.sin(s.rot)*s.height/2, s.pos[0] - np.sin(s.rot)*s.height/2],
		[s.pos[1] - np.cos(s.rot)*s.height/2, s.pos[1] + np.cos(s.rot)*s.height/2],
		color=s.color, linestyle=s.style, linewidth=3)

plt.axis('equal')
plt.show()
```
Result:
<br/><img src="./docs/img/example.png?raw=True" style="display: block; height: 20rem;" />
