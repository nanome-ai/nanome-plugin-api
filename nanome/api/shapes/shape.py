import nanome
from nanome._internal._shapes._shape import _Shape

class Shape(_Shape):
    def __init__(self, network, shape_type):
        _Shape.__init__(self, network, shape_type)

    @property
    def index(self):
        return self._index

    @property
    def shape_type(self):
        return self._shape_type

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value

    def upload(self, done_callback=None):
        self._upload(done_callback)

    def destroy(self):
        self._destroy()
_Shape._create = Shape