from nanome._internal._structure._io._mmcif.structure import structure
import nanome
import os
import tempfile
import ntpath
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode
from nanome.util.logs import Logs
from nanome.util.file import FileError
from . import FileExplorer

class BasicFileExplorer(nanome.PluginInstance):
    def __init__(self):
        self.FileExplorer = FileExplorer()
        self.FileExplorer.on_up_pressed = self.on_up_pressed
        self.FileExplorer.on_directory_pressed = self.on_directory_pressed
        self.FileExplorer.on_select_pressed = self.on_select_pressed
        self.FileExplorer.on_quick_access = self.on_quick_access
        self.FileExplorer.set_quick_access_list([])

        self.temp_dir = tempfile.mkdtemp()


    def on_up_pressed(self):
        self.files.cd("..", self.directory_changed)

    def on_directory_pressed(self, entry):
        self.files.cd(entry.name, self.directory_changed)

    def on_select_pressed(self, entry):
        self.files.get(entry.name, os.path.join(self.temp_dir, str(self.__path_leaf(entry.name))), self.file_fetched)

    def file_fetched(self, error, path):
        if error == nanome.util.FileError.no_error:
            Logs.debug(path)
            self.send_files_to_load(path)
        else:
            Logs.debug(error)

    def on_quick_access(self, name):
        pass

    def directory_changed(self, *args):
        if FileError.no_error == args[0]:
            self.files.pwd(self.FileExplorer.set_working_directory)
            self.files.ls(".", self.FileExplorer.set_directory_contents)
        else:
            Logs.error(args[0])

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)