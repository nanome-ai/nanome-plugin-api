from nanome.util.file import FileMeta
from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _DirectoryEntrySerializer
from nanome.util import DirectoryErrorCode

from nanome._internal._util._serializers import _TypeSerializer

class _FileMeta(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "FileMeta"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value.name)
        context.write_int(value.size)
        context.write_using_serializer(self.__string, value.date_modified)
        context.write_bool(value.is_directory)

    def deserialize(self, version, context):
        result = FileMeta()
        result.name = context.read_using_serializer(self.__string())
        result.size = context.read_int()
        result.date_modified = context.read_using_serializer(self.__string())
        result.is_directory = context.read_bool()
        return result