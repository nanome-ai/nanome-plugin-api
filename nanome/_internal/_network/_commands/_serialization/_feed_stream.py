from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _StringSerializer
from nanome.util.enums import StreamDataType
import nanome

class _FeedStream(_TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer(_StringSerializer)

    def version(self):
        return 2

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        data_type = value[2]
        if version > 0:
            context.write_byte(data_type)
        if data_type == StreamDataType.byte:
            context.write_byte_array(value[1])
        elif data_type == StreamDataType.string:
            context.write_using_serializer(value[1])
        else:
            context.write_float_array(value[1])

    def deserialize(self, version, context):
        id = context.read_uint()
        type = StreamDataType.float
        if version > 0:
            type = StreamDataType.float(context.read_byte())

        if type == StreamDataType.byte:
            data = context.read_byte_array()
        elif type == StreamDataType.string:
            data = context.read_using_serializer(self._array)
        else:
            data = context.read_float_array()

        return (id, data, type)
