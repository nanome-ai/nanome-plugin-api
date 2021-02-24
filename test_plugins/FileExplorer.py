from nanome._internal._structure._io._mmcif.structure import structure
import nanome
import os
import tempfile
import ntpath
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode
from nanome.util.logs import Logs
from nanome.util.file import FileError

NAME = "File Explorer"
DESCRIPTION = "Allows you to browse your files"
CATEGORY = ""
HAS_ADVANCED_OPTIONS = False

test_assets = os.getcwd() + ("/testing/test_assets")


class Icon():
    up = "test_assets/PluginIcons/Up.png"
    folder = "test_assets/PluginIcons/Folder.png"
    image = "test_assets/PluginIcons/Image.png"
    pdf = "test_assets/PluginIcons/PDF.png"
    structure = "test_assets/PluginIcons/Structures.png"
    workspace = "test_assets/PluginIcons/Workspace.png"


class FileExplorer(nanome.PluginInstance):

    def start(self):
        self.running = False
        self.item_prefab = LayoutNode.io.from_json(test_assets + "/File.json")
        self.menu = Menu.io.from_json(test_assets + "/FileExplorer.json")
        self.grid = self.menu.root.find_node("Grid", True).get_content()
        self.path_text = self.menu.root.find_node("path", True).get_content()
        self.load_button = self.menu.root.find_node("LoadButton", True).get_content()
        self.load_button.register_pressed_callback(self.load_pressed)
        self.save_button = self.menu.root.find_node("SaveButton", True).get_content()
        self.save_button.register_pressed_callback(self.save_pressed)
        self.back_button = self.menu.root.find_node("back", True).get_content()
        self.back_button.icon.value.set_all(Icon.up)
        self.back_button.register_pressed_callback(self.back_pressed)
        self.selected_button = None
        self.fetch_children()
        # self.fetch_wd()
        self.files.cd("~", self.directory_changed)
        self.temp_dir = tempfile.mkdtemp()
        # self.test_path = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\file.jpg"
        # self.test_path1 = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\1.jpg"
        # self.test_path2 = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\2.jpg"
        # self.test_path3 = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\3.jpg"
        # self.files.cp(self.test_path, self.test_path1, self.cp_done)
        # self.files.put(self.test_path, self.test_path2, self.put_done)
        # self.files.mv(self.test_path, self.test_path3, self.mv_done)

    def cp_done(self, *args):
        Logs.debug("cp done")

    def put_done(self, *args):
        Logs.debug("put done")

    def mv_done(self, *args):
        Logs.debug("mv done")

    def on_run(self):
        self.running = True
        self.update_menu(self.menu)

    def fetch_wd(self):
        self.wd = "."
        self.files.pwd(self.__set_dir)

    def __set_dir(self, error, wd):
        self.wd = wd
        self.path_text.text_value = wd
        if self.running:
            self.update_content(self.path_text)

    def fetch_children(self):
        self.files.ls(".", self.__set_children)

    def __set_children(self, error, files):
        if error != nanome.util.FileError.no_error:  # If API couldn't access directory, display error
            nanome.util.Logs.error("Directory request error:", str(error))
            return
        self.grid.items = []
        for file in files:
            item = self.create_file_rep(file)
            if item != None:
                self.grid.items.append(item)
        if self.running:
            self.update_content(self.grid)

    def create_file_rep(self, entry):
        extension = os.path.splitext(entry.name)[1].lower()
        icon = ""
        if extension == "":
            icon = Icon.folder
        elif extension == ".pdf":
            icon = Icon.pdf
        elif extension == ".jpeg" or extension == ".jpg" or extension == ".png":
            icon = Icon.image
        elif extension == ".nanome":
            icon = Icon.workspace
#region structure formats
        elif extension == ".pdb" or extension == ".pdb1" or extension == ".pdb2" or extension == ".pdb3" or extension == ".pdb4" or extension == ".pdb5":
            icon = Icon.structure
        elif extension == ".sd" or extension == ".sdf" or extension == ".mol" or extension == ".mol2":
            icon = Icon.structure
        elif extension == ".cif" or extension == ".mmcif" or extension == ".pdbx":
            icon = Icon.structure
        elif extension == ".smiles" or extension == ".smi":
            icon = Icon.structure
        elif extension == ".xyz" or extension == ".pqr" or extension == ".gro":
            icon = Icon.structure
        elif extension == ".moe" or extension == ".mae" or extension == ".pse":
            icon = Icon.structure
#endregion
#region misc formats
        elif extension == ".dcd" or extension == ".xtc" or extension == ".trr" or extension == ".psf":
            icon = Icon.structure
        elif extension == ".ccp4" or extension == ".dsn6":
            icon = Icon.structure
        elif extension == ".dx" or extension == ".map":
            icon = Icon.structure
        else:
            return None
#endregion

        item = self.item_prefab.clone()
        button = item.find_node("Button", True).get_content()
        button.text.value.set_all(entry.name)
        button.register_pressed_callback(self.entry_pressed)
        button.entry = entry
        button.text.value.set_all(self.path_leaf(entry.name))
        button.text.size = .3
        button.text.ellipsis = True
        button.icon.value.set_all(icon)
        return item

    def entry_pressed(self, button):
        if button.entry.is_directory:
            self.files.cd(button.entry.name, self.directory_changed)
            return
        to_update = []
        button.selected = True
        if self.selected_button is not None:
            self.selected_button.selected = False
            to_update.append(self.selected_button)
        if self.selected_button == button:
            self.selected_button = None
        else:
            self.selected_button = button
            to_update.append(self.selected_button)

        self.save_button.unusable = self.selected_button == None
        to_update.append(self.save_button)
        self.load_button.unusable = self.selected_button == None
        to_update.append(self.load_button)
        self.update_content(to_update)

    def load_pressed(self, button):
        entry = self.selected_button.entry
        if not entry.is_directory:
            self.files.get(entry.name, os.path.join(self.temp_dir, str(self.path_leaf(entry.name))), self.file_fetched)

    def file_fetched(self, error, path):
        if error == nanome.util.FileError.no_error:
            Logs.debug(path)
            self.send_files_to_load(path)
        else:
            Logs.debug(error)

    def save_pressed(self, button):
        pass

    def back_pressed(self, button):
        self.files.cd("..", self.directory_changed)

    def directory_changed(self, *args):
        if FileError.no_error == args[0]:
            self.fetch_wd()
            self.fetch_children()
        else:
            Logs.error(args[0])

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, FileExplorer)
