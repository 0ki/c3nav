import operator
from functools import reduce

from django.core import checks
from shapely import speedups

if speedups.available:
    speedups.enable()


try:
    import rtree
except OSError:
    rtree_index = False

    class Index:
        def __init__(self):
            self.objects = {}

        def insert(self, value, geometry):
            self.objects[value] = geometry

        def delete(self, value):
            self.objects.pop(value)

        def intersection(self, geometry):
            return self.objects.values()
else:
    rtree_index = True

    class Index:
        def __init__(self):
            self._index = rtree.index.Index()
            self._bounds = {}

        def insert(self, value, geometry):
            try:
                geoms = geometry.geoms
            except AttributeError:
                self._bounds.setdefault(value, []).append(geometry.bounds)
                self._index.insert(value, geometry.bounds)
            else:
                for geom in geoms:
                    self.insert(value, geom)

        def delete(self, value):
            for bounds in self._bounds.pop(value):
                self._index.delete(value, bounds)

        def intersection(self, geometry):
            try:
                geoms = geometry.geoms
            except AttributeError:
                return set(self._index.intersection(geometry.bounds))
            else:
                return reduce(operator.__or__, (self.intersection(geom) for geom in geoms), set())


@checks.register()
def check_svg_renderer(app_configs, **kwargs):
    errors = []
    if not rtree_index:
        errors.append(
            checks.Warning(
                'The libspatialindex_c library is missing. This will drastically slow down c3nav rendering.',
                obj='rtree.index.Index',
                id='c3nav.mapdata.W001',
            )
        )
    return errors
