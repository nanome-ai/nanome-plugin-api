from nanome._internal._shapes._sphere import _Sphere
from nanome.util.enums import ShapeType
from . import Shape

class Sphere(Shape):
    """
    | Represents a sphere. Can display a sphere in Nanome App.
    """
    def __init__(self, network):
        super().__init__(network, ShapeType.Sphere)

        self._radius = 1.0

    @property
    def radius(self):
        """
        | Radius of the sphere

        :param value: Radius of the sphere
        :type value: float
        """
        return self._radius
    @radius.setter
    def radius(self, value):
        self._radius = value
_Sphere._create = Sphere