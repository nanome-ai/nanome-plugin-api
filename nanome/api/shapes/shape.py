from nanome._internal._network._commands._callbacks import _Messages
from nanome.util import Vector3, Color, Logs
from nanome.util.enums import SetShapeResult
import nanome

class Sphere(object):
    def __init__(self, network):
        self.__network = network
        self.__index = -1
        self.__position = Vector3()
        self.__color = Color()
        self.__scale = 1

    def set(self, position=None, color=None, scale=None, done_callback=None):
        """
        | Set properties on the Sphere and send them to Nanome to create/update a Sphere

        :param position: Position in the workspace
        :type position: :class:`~nanome.util.vector3.Vector3`
        :param color: Color to display
        :type color: :class:`~nanome.util.color.Color`
        :param scale: Scale
        :type scale: float
        :param done_callback: Callback to get update's result. Parameter is success, if false, the shape doesn't exist in Nanome
        :type done_callback: fct with a bool parameter
        """
        if position != None:
            self.__position = position
        if color != None:
            self.__color = color
        if scale != None:
            self.__scale = scale

        if done_callback == None:
            done_callback = lambda _ : None

        def set_callback(result):
            if self.__index != -1 and result[0] != self.__index:
                Logs.error("SetShapeCallback received for the wrong shape")
            self.__index = result[0]
            done_callback(result[1] == SetShapeResult.Success)

        id = self.__network._send(_Messages.set_arbitrary_sphere, (self.__index, self.__position, self.__scale, self.__color))
        nanome.PluginInstance._save_callback(id, set_callback)

    def destroy(self):
        callback = lambda _, _1 : None

        id = self.__network._send(_Messages.delete_arbitrary_volume, (self.__index))
        nanome.PluginInstance._save_callback(id, callback)