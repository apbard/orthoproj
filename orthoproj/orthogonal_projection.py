# Copyright (c) 2016 Alessandro Pietro Bardelli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Module containing OrthoProj, a class which can create an Orthogonal Projection
of 3D data with full axes synchronisation.
"""
# pylint: disable=undefined-variable, invalid-name, eval-used
import types
import itertools
from textwrap import dedent
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import PolyCollection
from six.moves import input

# This generates all sync_A_with_B(self, axis) functions that are used to
# synchronise the axis of two plots
for src, trg in itertools.product(['x', 'y', 'z'], repeat=2):
    eval(compile(dedent("""
        def sync_{0}_with_{1}(self, axis):
            if((axis.get_{1}lim()[0] > axis.get_{1}lim()[1]) !=
               (self.get_{0}lim()[0] > self.get_{0}lim()[1])):
                self.set_{0}lim(axis.get_{1}lim()[::-1], emit=False)
            else:
                self.set_{0}lim(axis.get_{1}lim(), emit=False)
        """).format(src, trg), '<string>', 'exec'))


def _merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        if dictionary is not None:
            result.update(dictionary)
    return result


class OrthoProj():
    """
    Orthogonal Projection object.
    """

    _fig = None
    _locked = None
    _axisXZ = None
    _axisYZ = None
    _axisXY = None
    _axis3D = None

    def __init__(self, title=None):
        """
        Build an :class:`OrthoProj` object

        Args:
            title (string). The title string for the orthogonal projection figure.
            Default: None, i.e., default naming

        """

        fig = plt.figure(title)
        axisXZ = fig.add_subplot(221, title="Vertical Plane - XZ")
        axisYZ = fig.add_subplot(222, title="Lateral Plane - YZ")
        axisXY = fig.add_subplot(223, title="Horizontal Plane - XY")
        axis3D = fig.add_subplot(224, title="3D view - XYZ", projection="3d")

        for ax in [axisXZ, axisYZ, axisXY, axis3D]:
            ax.sync_x_with_x = types.MethodType(sync_x_with_x, ax)
            ax.sync_x_with_y = types.MethodType(sync_x_with_y, ax)
            ax.sync_x_with_z = types.MethodType(sync_x_with_z, ax)
            ax.sync_y_with_x = types.MethodType(sync_y_with_x, ax)
            ax.sync_y_with_y = types.MethodType(sync_y_with_y, ax)
            ax.sync_y_with_z = types.MethodType(sync_y_with_z, ax)

        axis3D.sync_z_with_x = types.MethodType(sync_z_with_x, axis3D)
        axis3D.sync_z_with_y = types.MethodType(sync_z_with_y, axis3D)
        axis3D.sync_z_with_z = types.MethodType(sync_z_with_z, axis3D)

        # Connect XY subplot
        axisXY.callbacks.connect('xlim_changed', axisXZ.sync_x_with_x)
        axisXY.callbacks.connect('xlim_changed', axis3D.sync_x_with_x)
        axisXY.callbacks.connect('ylim_changed', axisYZ.sync_x_with_y)
        axisXY.callbacks.connect('ylim_changed', axis3D.sync_y_with_y)

        # Connect XZ subplot
        axisXZ.callbacks.connect('xlim_changed', axisXY.sync_x_with_x)
        axisXZ.callbacks.connect('xlim_changed', axis3D.sync_x_with_x)
        axisXZ.callbacks.connect('ylim_changed', axisYZ.sync_y_with_y)
        axisXZ.callbacks.connect('ylim_changed', axis3D.sync_z_with_y)

        # Connect YZ subplot
        axisYZ.callbacks.connect('xlim_changed', axisXY.sync_y_with_x)
        axisYZ.callbacks.connect('xlim_changed', axis3D.sync_y_with_x)
        axisYZ.callbacks.connect('ylim_changed', axisXZ.sync_y_with_y)
        axisYZ.callbacks.connect('ylim_changed', axis3D.sync_z_with_y)

        # Connect 3D subplot
        axis3D.callbacks.connect('xlim_changed', axisXY.sync_x_with_x)
        axis3D.callbacks.connect('xlim_changed', axisXZ.sync_x_with_x)
        axis3D.callbacks.connect('ylim_changed', axisXY.sync_y_with_y)
        axis3D.callbacks.connect('ylim_changed', axisYZ.sync_x_with_y)
        axis3D.callbacks.connect('zlim_changed', axisXZ.sync_y_with_z)
        axis3D.callbacks.connect('zlim_changed', axisYZ.sync_y_with_z)

        # invert the x axis in the YX subplot
        axisYZ.invert_xaxis()

        # set labels for 3D plot
        axis3D.set_xlabel('X axis')
        axis3D.set_ylabel('Y axis')
        axis3D.set_zlabel('Z axis')

        self._fig = fig
        self._axisXZ = axisXZ
        self._axisYZ = axisYZ
        self._axisXY = axisXY
        self._axis3D = axis3D

    def plot(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None,
             kwargs3D=None, kwargsShared=None):
        '''
        Plot a scatter.

        Args:
            x, y, z (1D array). Positions of data points.

            kwargsXZ, kwargsYZ, kwargsXY, kwargs3D (dictionary). Extra keyword
                arguments to be passed to the single plotting functions.
                Internally :func:`~mpl_toolkits.mplot3d.art3d.Axes3D.scatter`
                is used for the 3D plot and standard
                :func:`~matplotlib.axes.Axes.plot` for 2D plots.

            kwargsShared (dictionary). Extra keyword arguments common to all plots.
                Arguments specified via specific kwargs will always have the
                precedence and won't be overwritten.

        '''
        kwargsXZ = _merge_dicts(kwargsShared, kwargsXZ)
        kwargsYZ = _merge_dicts(kwargsShared, kwargsYZ)
        kwargsXY = _merge_dicts(kwargsShared, kwargsXY)
        kwargs3D = _merge_dicts(kwargsShared, kwargs3D)

        self._plot2DGraphs(x, y, z, kwargsXZ, kwargsYZ, kwargsXY)
        if kwargs3D is None:
            self._axis3D.plot(x, y, z)
        else:
            self._axis3D.plot(x, y, z, **kwargs3D)

    def scatter(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None,
                kwargs3D=None, kwargsShared=None):
        '''
        Plot a scatter.

        Args:
            x, y, z (1D array). Positions of data points.

            kwargsXZ, kwargsYZ, kwargsXY, kwargs3D (dictionary). Extra keyword
                arguments to be passed to the single plotting functions.
                Internally :func:`~mpl_toolkits.mplot3d.art3d.Axes3D.scatter`
                is used for the 3D plot and standard
                :func:`~matplotlib.axes.Axes.scatter` for 2D plots.

            kwargsShared (dictionary). Extra keyword arguments common to all plots.
                Arguments specified via specific kwargs will always have the
                precedence and won't be overwritten.
        '''

        kwargsXZ = _merge_dicts(kwargsShared, kwargsXZ)
        kwargsYZ = _merge_dicts(kwargsShared, kwargsYZ)
        kwargsXY = _merge_dicts(kwargsShared, kwargsXY)
        kwargs3D = _merge_dicts(kwargsShared, kwargs3D)

        self._scatter2DGraphs(x, y, z, kwargsXZ, kwargsYZ, kwargsXY)
        if kwargs3D is None:
            self._axis3D.scatter(x, y, z)
        else:
            self._axis3D.scatter(x, y, z, **kwargs3D)

    def plot_trisurf(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None,
                     kwargs3D=None, kwargsShared=None):
        '''
        Plot a trisurf
        '''
        raise NotImplementedError("plot_trisurf: Not Implemented Yet")

    def plot_surface(self, X, Y, Z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None,
                     kwargs3D=None, kwargsShared=None):
        '''
        Plot a surface.

        Args:
            X, Y, Z (2D array). Data values as 2D arrays.

            kwargsXZ, kwargsYZ, kwargsXY, kwargs3D (dictionary). Extra keyword
                arguments to be passed to the single plotting functions.
                Internally :func:`~mpl_toolkits.mplot3d.art3d.Axes3D.plot_surface`
                is used for the 3D plot and standard :func:`~matplotlib.axes.Axes.plot`
                for 2D plots.

            kwargsShared (dictionary). Extra keyword arguments common to all plots.
                Arguments specified via specific kwargs will always have the
                precedence and won't be overwritten.
        '''

        kwargsXZ = _merge_dicts(kwargsShared, kwargsXZ)
        kwargsYZ = _merge_dicts(kwargsShared, kwargsYZ)
        kwargsXY = _merge_dicts(kwargsShared, kwargsXY)
        kwargs3D = _merge_dicts(kwargsShared, kwargs3D)

        self._plot2DGraphs(X, Y, Z, kwargsXZ, kwargsYZ, kwargsXY)
        self._plot2DGraphs(X.T, Y.T, Z.T, kwargsXZ, kwargsYZ, kwargsXY)
        if kwargs3D is None:
            self._axis3D.plot_surface(X, Y, Z)
        else:
            self._axis3D.plot_surface(X, Y, Z, **kwargs3D)

    def plot_wireframe(self, X, Y, Z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None,
                       kwargs3D=None, kwargsShared=None):
        '''
        Plot a wireframe.

        Args:
            X, Y, Z (2D array). Data values as 2D arrays.

            kwargsXZ, kwargsYZ, kwargsXY, kwargs3D (dictionary). Extra keyword
                arguments to be passed to the single plotting functions.
                Internally :func:`~mpl_toolkits.mplot3d.art3d.Axes3D.plot_wireframe`
                is used for the 3D plot and standard :func:`~matplotlib.axes.Axes.plot`
                for 2D plots.

            kwargsShared (dictionary). Extra keyword arguments common to all plots.
                Arguments specified via specific kwargs will always have the
                precedence and won't be overwritten.
        '''

        kwargsXZ = _merge_dicts(kwargsShared, kwargsXZ)
        kwargsYZ = _merge_dicts(kwargsShared, kwargsYZ)
        kwargsXY = _merge_dicts(kwargsShared, kwargsXY)
        kwargs3D = _merge_dicts(kwargsShared, kwargs3D)

        self._plot2DGraphs(X, Y, Z, kwargsXZ, kwargsYZ, kwargsXY)
        self._plot2DGraphs(X.T, Y.T, Z.T, kwargsXZ, kwargsYZ, kwargsXY)
        if kwargs3D is None:
            self._axis3D.plot_wireframe(X, Y, Z)
        else:
            self._axis3D.plot_wireframe(X, Y, Z, **kwargs3D)

    def plot_collection(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None,
                        kwargs3D=None, kwargsShared=None):
        '''
        Plot a collection.

        Args:
            x, y, z (1D array). Arrays containing the vertices of the collection object.
                Internally :func:`~mpl_toolkits.mplot3d.art3d.Poly3DCollection`
                and :func:`~matplotlib.collections.PolyCollection` are used
                to create the collections.

            kwargsXZ, kwargsYZ, kwargsXY, kwargs3D (dictionary).
                Extra keyword arguments to be passed to the single plotting
                functions. Internally :func:`add_collection3d` and
                :func:`add_collection` are called.

            kwargsShared (dictionary). Extra keyword arguments common to all plots.
                Arguments specified via specific kwargs will always have the
                precedence and won't be overwritten.
        '''
        kwargsXZ = _merge_dicts(kwargsShared, kwargsXZ)
        kwargsYZ = _merge_dicts(kwargsShared, kwargsYZ)
        kwargsXY = _merge_dicts(kwargsShared, kwargsXY)
        kwargs3D = _merge_dicts(kwargsShared, kwargs3D)

        self._collection2DGraphs(x, y, z, kwargsXZ, kwargsYZ, kwargsXY)
        verts = [list(zip(x, y, z))]
        if kwargs3D is None:
            self._axis3D.add_collection3d(Poly3DCollection(verts))
        else:
            self._axis3D.add_collection3d(Poly3DCollection(verts, **kwargs3D))

    def show(self, block=False):
        """
        Display the figure.

        Args:
            block (bool). If True the computation is blocked waiting for
                user's input. Default: False
        """
        self._fig.show()
        if block:
            input("Press any key to continue")

    # ###############
    # Private Methods
    # ###############

    def _plot2DGraphs(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None):
        """
        Function that plot data on the 2D axis as a simple plot
        """
        if kwargsXZ is None:
            self._axisXZ.plot(x, z)
        else:
            self._axisXZ.plot(x, z, **kwargsXZ)

        if kwargsYZ is None:
            self._axisYZ.plot(y, z)
        else:
            self._axisYZ.plot(y, z, **kwargsYZ)

        if kwargsXY is None:
            self._axisXY.plot(x, y)
        else:
            self._axisXY.plot(x, y, **kwargsXY)

    def _scatter2DGraphs(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None):
        """
        Function that plot data on the 2D axis as a scatter plot
        """
        if kwargsXZ is None:
            self._axisXZ.scatter(x, z)
        else:
            self._axisXZ.scatter(x, z, **kwargsXZ)

        if kwargsYZ is None:
            self._axisYZ.scatter(y, z)
        else:
            self._axisYZ.scatter(y, z, **kwargsYZ)

        if kwargsXY is None:
            self._axisXY.scatter(x, y)
        else:
            self._axisXY.scatter(x, y, **kwargsXY)

    def _collection2DGraphs(self, x, y, z, kwargsXZ=None, kwargsYZ=None, kwargsXY=None):
        """
        Function that plot data on the 2D axis as collections
        """

        vertxy = [list(zip(x, y))]
        vertxz = [list(zip(x, z))]
        vertyz = [list(zip(y, z))]

        if kwargsXY is None:
            self._axisXY.add_collection(PolyCollection(vertxy))
        else:
            self._axisXY.add_collection(PolyCollection(vertxy, **kwargsXY))
        if kwargsXZ is None:
            self._axisXZ.add_collection(PolyCollection(vertxz))
        else:
            self._axisXZ.add_collection(PolyCollection(vertxz, **kwargsXZ))
        if kwargsYZ is None:
            self._axisYZ.add_collection(PolyCollection(vertyz))
        else:
            self._axisYZ.add_collection(PolyCollection(vertyz, **kwargsYZ))
