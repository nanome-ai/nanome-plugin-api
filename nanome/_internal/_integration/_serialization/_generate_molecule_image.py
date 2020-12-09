from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer, _ByteSerializer
from nanome._internal._structure._serialization import _ResidueSerializer, _AtomSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _GenerateMoleculeImage(_TypeSerializer):
    def __init__(self):
        temp = _ArraySerializer()
        temp.set_type(_ResidueSerializer())
        self.res_serializer = _ArraySerializer()
        self.res_serializer.set_type(temp)

        temp = _ArraySerializer()
        temp.set_type(_ByteSerializer())
        self.byte_array = _ArraySerializer()
        self.byte_array.set_type(temp)

        self.dict = _DictionarySerializer()
        self.dict.set_types(_LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "GenerateMoleculeImage"

    def serialize(self, version, value, context):
        context.write_using_serializer(value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        return context.read_using_serializer(self.res_serializer)