from . import _ContextSerialization, _ContextDeserialization
from .._commands import _callbacks as CommandCallbacks
from .._commands import _serialization as CommandSerializers
from nanome._internal._util import _serializers as Serializers
from nanome.util import Logs
import struct, traceback

MESSAGE_VERSION_KEY = "ToClientProtocol"
packet_debugging = False

class Serializer(object):
    _commands = dict()
    _messages = dict()
    _command_callbacks = dict()

    def serialize_message(self, request_id, message_type, arg, version_table, expects_response):
        context = _ContextSerialization(self._plugin_id, version_table, packet_debugging)
        context.write_uint(request_id)
        command_hash = CommandCallbacks._Hashes.MessageHashes[message_type]
        context.write_uint(command_hash)
        if version_table != None:
            if version_table.get(MESSAGE_VERSION_KEY, 0) >= 1:
                context.write_bool(expects_response)

        if arg != None:
            command = None
            try:
                command = Serializer._messages[command_hash]
            except KeyError:
                Logs.warning("Trying to serialize an unregistered message type:", message_type)
            if command != None:
                context.write_using_serializer(command, arg)
                return context.to_array()
        return context.to_array()

    def deserialize_command(self, payload, version_table):
        context = _ContextDeserialization(payload, version_table, packet_debugging)
        try:
            request_id = context.read_uint()
            command_hash = context.read_uint()
            command = Serializer._commands[command_hash]
        except KeyError:
            if self.try_register_session(payload) == True:
                Logs.error("A session is trying to connect even though it is already connected")
            else:
                Logs.error("Received an unregistered command:", command_hash)
            return (None, None, None)
        except BufferError as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)
        except struct.error as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)

        try:
            received_object = context.read_using_serializer(command)
        except BufferError as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)
        except struct.error as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)
        return received_object, command_hash, request_id

    def try_register_session(self, payload):
        context = _ContextDeserialization(payload, None, packet_debugging)
        context.read_uint() # Read the request ID
        command_hash = context.read_uint()
        return command_hash == CommandCallbacks._Hashes.CommandHashes[CommandCallbacks._Commands.connect]

    def __init__(self):
        self._plugin_id = 0

#-------------Commands-----------#
# Commands are incoming (nanome -> plugin)

def add_command(command, serializer, callback):
    Serializer._commands[CommandCallbacks._Hashes.CommandHashes[command]] = serializer
    Serializer._command_callbacks[CommandCallbacks._Hashes.CommandHashes[command]] = callback

#control
add_command(CommandCallbacks._Commands.connect, CommandSerializers._Connect(), CommandCallbacks._connect)
add_command(CommandCallbacks._Commands.run, CommandSerializers._Run(), CommandCallbacks._run)
add_command(CommandCallbacks._Commands.advanced_settings, CommandSerializers._AdvancedSettings(), CommandCallbacks._advanced_settings)

#workspace
add_command(CommandCallbacks._Commands.workspace_response, CommandSerializers._ReceiveWorkspace(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.complex_add, CommandSerializers._ComplexAddedRemoved(), CommandCallbacks._complex_added)
add_command(CommandCallbacks._Commands.complex_remove, CommandSerializers._ComplexAddedRemoved(), CommandCallbacks._complex_removed)
add_command(CommandCallbacks._Commands.complex_list_response, CommandSerializers._ReceiveComplexList(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.complexes_response, CommandSerializers._ReceiveComplexes(), CommandCallbacks._receive_complexes)
add_command(CommandCallbacks._Commands.structures_deep_update_done, CommandSerializers._UpdateStructuresDeepDone(), CommandCallbacks._simple_callback_no_arg)
add_command(CommandCallbacks._Commands.add_to_workspace_done, CommandSerializers._AddToWorkspace(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.position_structures_done, CommandSerializers._PositionStructuresDone(), CommandCallbacks._simple_callback_no_arg)
add_command(CommandCallbacks._Commands.dssp_add_done, CommandSerializers._AddDSSP(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.bonds_add_done, CommandSerializers._AddBonds(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.complex_updated, CommandSerializers._ComplexUpdated(), CommandCallbacks._complex_updated)
add_command(CommandCallbacks._Commands.selection_changed, CommandSerializers._SelectionChanged(), CommandCallbacks._selection_changed)
add_command(CommandCallbacks._Commands.compute_hbonds_done, CommandSerializers._ComputeHBonds(), CommandCallbacks._simple_callback_no_arg)

#Volume
add_command(CommandCallbacks._Commands.upload_cryo_em_done, CommandSerializers._UploadCryoEMDone(), CommandCallbacks._simple_callback_no_arg)

#ui
add_command(CommandCallbacks._Commands.menu_toggle, CommandSerializers._MenuCallback(), CommandCallbacks._menu_toggled)
add_command(CommandCallbacks._Commands.button_press, CommandSerializers._ButtonCallback(), CommandCallbacks._button_pressed)
add_command(CommandCallbacks._Commands.button_hover, CommandSerializers._ButtonCallback(), CommandCallbacks._button_hover)
add_command(CommandCallbacks._Commands.slider_release, CommandSerializers._SliderCallback(), CommandCallbacks._slider_released)
add_command(CommandCallbacks._Commands.slider_change, CommandSerializers._SliderCallback(), CommandCallbacks._slider_changed)
add_command(CommandCallbacks._Commands.text_submit, CommandSerializers._TextInputCallback(), CommandCallbacks._text_submit)
add_command(CommandCallbacks._Commands.text_change, CommandSerializers._TextInputCallback(), CommandCallbacks._text_changed)
add_command(CommandCallbacks._Commands.image_press, CommandSerializers._ImageCallback(), CommandCallbacks._image_pressed)
add_command(CommandCallbacks._Commands.image_hold, CommandSerializers._ImageCallback(), CommandCallbacks._image_held)
add_command(CommandCallbacks._Commands.image_release, CommandSerializers._ImageCallback(), CommandCallbacks._image_released)
add_command(CommandCallbacks._Commands.menu_transform_response, CommandSerializers._GetMenuTransformResponse(), CommandCallbacks._simple_callback_arg_unpack)

#file
add_command(CommandCallbacks._Commands.directory_response, CommandSerializers._DirectoryRequest(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.file_response, CommandSerializers._FileRequest(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.file_save_done, CommandSerializers._FileSave(), CommandCallbacks._simple_callback_arg)

#streams
add_command(CommandCallbacks._Commands.stream_create_done, CommandSerializers._CreateStreamResult(), CommandCallbacks._receive_create_stream_result)
add_command(CommandCallbacks._Commands.stream_feed, CommandSerializers._FeedStream(), CommandCallbacks._feed_stream)
add_command(CommandCallbacks._Commands.stream_interrupt, CommandSerializers._InterruptStream(), CommandCallbacks._receive_interrupt_stream)
add_command(CommandCallbacks._Commands.stream_feed_done, CommandSerializers._FeedStreamDone(), CommandCallbacks._simple_callback_no_arg)

#macros
add_command(CommandCallbacks._Commands.get_macros_response, CommandSerializers._GetMacrosResponse(), CommandCallbacks._simple_callback_arg)

# Presenter
add_command(CommandCallbacks._Commands.presenter_info_response, CommandSerializers._GetPresenterInfoResponse(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.presenter_change, CommandSerializers._PresenterChange(), CommandCallbacks._presenter_change)
add_command(CommandCallbacks._Commands.controller_transforms_response, CommandSerializers._GetControllerTransformsResponse(), CommandCallbacks._simple_callback_arg_unpack)

#others
add_command(CommandCallbacks._Commands.load_file_done, CommandSerializers._LoadFileDone(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks._Commands.integration, CommandSerializers._Integration(), CommandCallbacks._integration)

#-------------Messages-----------#
# Messages are outgoing (plugin -> nanome)

def add_message(command, serializer):
    Serializer._messages[CommandCallbacks._Hashes.MessageHashes[command]] = serializer

Serializers._type_serializer._TypeSerializer.register_string_raw(MESSAGE_VERSION_KEY, 1)
#control
add_message(CommandCallbacks._Messages.connect, CommandSerializers._Connect())

#workspace
add_message(CommandCallbacks._Messages.workspace_update, CommandSerializers._UpdateWorkspace())
add_message(CommandCallbacks._Messages.structures_deep_update, CommandSerializers._UpdateStructures(False))
add_message(CommandCallbacks._Messages.structures_shallow_update, CommandSerializers._UpdateStructures(True))
add_message(CommandCallbacks._Messages.workspace_request, CommandSerializers._RequestWorkspace())
add_message(CommandCallbacks._Messages.complex_list_request, CommandSerializers._RequestComplexList())
add_message(CommandCallbacks._Messages.add_to_workspace, CommandSerializers._AddToWorkspace())
add_message(CommandCallbacks._Messages.complexes_request, CommandSerializers._RequestComplexes())
add_message(CommandCallbacks._Messages.bonds_add, CommandSerializers._AddBonds())
add_message(CommandCallbacks._Messages.dssp_add, CommandSerializers._AddDSSP())
add_message(CommandCallbacks._Messages.structures_zoom, CommandSerializers._PositionStructures())
add_message(CommandCallbacks._Messages.structures_center, CommandSerializers._PositionStructures())
add_message(CommandCallbacks._Messages.hook_complex_updated, CommandSerializers._ComplexUpdatedHook())
add_message(CommandCallbacks._Messages.hook_selection_changed, CommandSerializers._SelectionChangedHook())
add_message(CommandCallbacks._Messages.compute_hbonds, CommandSerializers._ComputeHBonds())

#volume
add_message(CommandCallbacks._Messages.upload_cryo_em, CommandSerializers._UploadCryoEM())

#ui
add_message(CommandCallbacks._Messages.menu_update, CommandSerializers._UpdateMenu())
add_message(CommandCallbacks._Messages.content_update, CommandSerializers._UpdateContent())
add_message(CommandCallbacks._Messages.node_update, CommandSerializers._UpdateNode())
add_message(CommandCallbacks._Messages.menu_transform_set, CommandSerializers._SetMenuTransform())
add_message(CommandCallbacks._Messages.menu_transform_request, CommandSerializers._GetMenuTransform())
add_message(CommandCallbacks._Messages.notification_send, CommandSerializers._SendNotification())
add_message(CommandCallbacks._Messages.hook_ui_callback, CommandSerializers._UIHook())

#file
add_message(CommandCallbacks._Messages.directory_request, CommandSerializers._DirectoryRequest())
add_message(CommandCallbacks._Messages.file_request, CommandSerializers._FileRequest())
add_message(CommandCallbacks._Messages.file_save, CommandSerializers._FileSave())
add_message(CommandCallbacks._Messages.plugin_list_button_set, CommandSerializers._SetPluginListButton())

#macros
add_message(CommandCallbacks._Messages.run_macro, CommandSerializers._RunMacro())
add_message(CommandCallbacks._Messages.save_macro, CommandSerializers._SaveMacro())
add_message(CommandCallbacks._Messages.delete_macro, CommandSerializers._DeleteMacro())
add_message(CommandCallbacks._Messages.get_macros, CommandSerializers._GetMacros())
add_message(CommandCallbacks._Messages.stop_macro, CommandSerializers._StopMacro())

#streams
add_message(CommandCallbacks._Messages.stream_create, CommandSerializers._CreateStream())
add_message(CommandCallbacks._Messages.stream_feed, CommandSerializers._FeedStream())
add_message(CommandCallbacks._Messages.stream_destroy, CommandSerializers._DestroyStream())

# Presenter
add_message(CommandCallbacks._Messages.presenter_info_request, CommandSerializers._GetPresenterInfo())
add_message(CommandCallbacks._Messages.controller_transforms_request, CommandSerializers._GetControllerTransforms())

#others
add_message(CommandCallbacks._Messages.open_url, CommandSerializers._OpenURL())
add_message(CommandCallbacks._Messages.load_file, CommandSerializers._LoadFile())
