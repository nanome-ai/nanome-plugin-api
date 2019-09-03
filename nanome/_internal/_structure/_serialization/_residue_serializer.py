from nanome._internal._util._serializers import _ArraySerializer, _StringSerializer, _ColorSerializer
from . import _AtomSerializerID
from . import _BondSerializer
from .. import _Residue
from nanome.util import Logs

from nanome._internal._util._serializers import _TypeSerializer

cast_failed_warning = False

class _ResidueSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.atom = _AtomSerializerID()
        self.bond = _BondSerializer()
        self.color = _ColorSerializer()
        self.string = _StringSerializer()

    def version(self):
        #Version 0 corresponds to Nanome release 1.10
        return 1

    def name(self):
        return "Residue"

    def serialize(self, version, value, context):
        context.write_long(value._index)

        self.array.set_type(self.atom)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._atoms)
        self.array.set_type(self.bond)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._bonds)
        context.write_bool(value._ribboned)
        context.write_float(value._ribbon_size)
        context.write_int(value._ribbon_mode.value)
        context.write_using_serializer(self.color, value._ribbon_color)
        if (version > 0):
            context.write_bool(value._labeled)
            context.write_using_serializer(self.string, value._label_text)

        context.write_using_serializer(self.string, value._type)
        context.write_int(value._serial)
        context.write_using_serializer(self.string, value._name)
        context.write_int(value._secondary_structure.value)

    def deserialize(self, version, context):
        global cast_failed_warning

        residue = _Residue._create()
        residue._index = context.read_long()

        self.array.set_type(self.atom)
        residue._atoms = context.read_using_serializer(self.array)
        self.array.set_type(self.bond)
        residue._bonds = context.read_using_serializer(self.array)
        
        residue._ribboned = context.read_bool()
        residue._ribbon_size = context.read_float()
        mode = context.read_int()
        try:
            residue._ribbon_mode = _Residue.RibbonMode(mode)
        except ValueError:
            if cast_failed_warning == False:
                cast_failed_warning = True
                Logs.warning("Received an unknown ribbon display mode. Library might outdated")
            residue._ribbon_mode = _Residue.RibbonMode(mode)
        residue._ribbon_color = context.read_using_serializer(self.color)
        if (version > 0):
            residue._labeled = context.read_bool()
            residue._label_text = context.read_using_serializer(self.string)

        residue._type = context.read_using_serializer(self.string)
        residue._serial = context.read_int()
        residue._name = context.read_using_serializer(self.string)
        secondary = context.read_int()
        try:
            residue._secondary_structure = _Residue.SecondaryStructure(secondary)
        except ValueError:
            if cast_failed_warning == False:
                cast_failed_warning = True
                Logs.warning("Received an unknown residue secondary structure type. Library might outdated")
            residue._secondary_structure = _Residue.SecondaryStructure(secondary)
        return residue