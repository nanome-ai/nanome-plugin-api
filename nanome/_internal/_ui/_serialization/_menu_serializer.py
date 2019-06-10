from nanome._internal._util._serializers import _StringSerializer
from .. import _Menu
from . import _LayoutNodeSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _MenuSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
    
    def version(self):
        return 0

    def name(self):
        return "Menu"

    def serialize(self, version, value, context):
        context.write_bool(value.enabled)
        context.write_int(value._id)
        context.write_using_serializer(self.string, value.title)
        context.write_bool(value.locked)
        context.write_float(value._width)
        context.write_float(value._height)
        context.write_int(value.root._id)

    def deserialize(self, version, context):
        menu = _Menu._create()
        menu.enabled = context.read_bool()
        menu._id = context.read_int()
        menu.title = context.read_using_serializer(self.string)
        menu.locked= context.read_bool()
        menu._width = context.read_float()
        menu._height = context.read_float()
        menu._root_id = context.read_int()
        return menu