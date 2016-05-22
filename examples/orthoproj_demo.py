#
# Copyright (c) 2016 Alessandro Pietro Bardelli
#

"""
Demonstrates making an Orthogonal Projection graph using OrthoProj class
"""

import numpy as np
from orthoproj import OrthoProj
from matplotlib import cm

# #################################
# Functions to generate sample data
# #################################


def cube_data(edge=1, offset=(0, 0, 0)):
    x = np.asarray([[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0],
                    [0, 0, 1, 1], [1, 1, 0, 0], [1, 1, 1, 1]]) * edge + offset[0]
    y = np.asarray([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1],
                    [0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 0, 0]]) * edge + offset[1]
    z = np.asarray([[0, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 1],
                    [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1]]) * edge + offset[2]
    return x, y, z


def ellipsoid_data(a=1, b=1, c=1, offset=(0, 0, 0)):
    u, v = np.mgrid[0: (2 * np.pi): 40j, 0: np.pi: 20j]  # pylint: disable=E1127
    x = a * np.cos(u) * np.sin(v) + offset[0]
    y = b * np.sin(u) * np.sin(v) + offset[1]
    z = c * np.cos(v) + offset[2]
    return x, y, z


def helix_data(radius=1, offset=(0, 0, 0)):
    t = np.linspace(0., 5 * 2 * np.pi, 1000)
    x = radius * np.sin(t) + offset[0]
    y = radius * np.cos(t) + offset[1]
    z = t / (20 * np.pi) + offset[2]
    return x, y, z


def archimedes_spiral_data(a=0, b=0.1, c=2, max_theta=4 * np.pi, offset=(0, 0, 0)):
    theta = np.linspace(-max_theta, max_theta, 1000)
    r = a + b * (theta ** c)
    x = r * np.sin(theta) + offset[0]
    y = r * np.cos(theta) + offset[1]
    z = theta + offset[2]
    return x, y, z


def sample_data():
    base = np.arange(-5, 5, 0.2)
    X, Y = np.meshgrid(base, base)
    R = 2 * np.sqrt(X**2 + Y**2)
    Z = np.sin(R) / np.sqrt(R) - (X / 10)**2
    ang_rot = -15 * np.pi / 180.
    Xrot = X * np.cos(ang_rot) - Y * np.sin(ang_rot)
    Yrot = X * np.sin(ang_rot) + Y * np.cos(ang_rot)
    return Xrot, Yrot, Z


# create an OrthoProj object
example = OrthoProj(title="Example")

# get a sphere
X, Y, Z = ellipsoid_data()

# compute colors
colortuple = ('y', 'b', 'g', 'r')
colors = np.empty(X.shape, dtype=str)
for y in range(X.shape[1]):
    for x in range(X.shape[0]):
        colors[x, y] = colortuple[(x + y) % len(colortuple)]

# plot as a surface
example.plot_surface(X, Y, Z, kwargsShared={"color": "k"},
                     kwargs3D={'alpha': 0.25, 'rstride': 1, 'cstride': 1,
                               'antialiased': False, 'facecolors': colors})

# plot an Archimede' spiral as scatter
x, y, z = archimedes_spiral_data(a=-5, offset=(0.5, -10, 0.))
example.scatter(x / 10, y / 5, z / 12.,
                kwargsShared={"alpha": 0.9, "c": z, "cmap": cm.jet, "lw": 0})

# plot an Helix as regular plot
x, y, z = helix_data(radius=0.25, offset=(0, 0, 1))
example.plot(x, y, z, kwargsShared={"linewidth": 2, "alpha": 0.9, "color": "r"})

# plot a cube as collection of faces
x, y, z = cube_data(0.5, offset=(-0.25, -0.25, 0.25))
faces = 6.
for i in range(int(faces)):
    example.plot_collection(x[i], y[i], z[i],
                            kwargsXZ={'zorder': -min(y[i])},
                            kwargsYZ={'zorder': -min(x[i])},
                            kwargsXY={'zorder': max(z[i])},
                            kwargsShared={"facecolor": cm.jet(i / faces)})

# not blocking show
example.show(block=False)

# another wireframe example
wireframe = OrthoProj("Wireframe")
X, Y, Z = sample_data()
wireframe.plot_wireframe(X, Y, Z, kwargs3D={'rstride': 1, 'cstride': 1},
                         kwargsShared={'color': 'k'})

# a blocking show
wireframe.show(block=True)
