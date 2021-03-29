from . import IntEnum
#TODO normalize styling

class AtomRenderingMode(IntEnum):
    """
    | Enumerates shape types an atom can be rendered as.
    | To be used with atom.atom_mode
    """
    BallStick = 0
    Stick = 1
    Wire = 2
    VanDerWaals = 3
    Point = 4
    BFactor = 5
    Adaptive = 6

class Kind(IntEnum):
    """
    | Enumerates bond types.
    | To be used with bond.kind and elements of bond.kinds
    """
    Unknown = 0
    CovalentSingle = 1
    CovalentDouble = 2
    CovalentTriple = 3
    Aromatic = 4

class RibbonMode(IntEnum):
    """
    | Enumerates ribbon display modes.
    | To be used with structure.Residue().ribbon_mode
    """
    SecondaryStructure = 0
    AdaptiveTube = 1
    Coil = 2

class SecondaryStructure(IntEnum):
    """
    | Enumerates secondary structure types.
    | To be used with structure.Residue().secondary_structure
    """
    Unknown = 0
    Coil = 1
    Sheet = 2
    Helix = 3

class PaddingTypes(IntEnum):
    """
    | Enumerates UI padding types.
    | To be used with ui.LayoutNode().padding_type
    """
    fixed = 0
    ratio = 1

class PluginListButtonType(IntEnum):
    """
    | Enumerates buttons on the plugin list, modifiable by the plugin itself.
    | To be used with plugin_instance.set_plugin_list_button
    """
    run = 0
    advanced_settings = 1

class SizingTypes(IntEnum):
    """
    | Enumerates ways in which a Layout Node can be sized within a UI layout.
    | To be used with ui.LayoutNode().sizing_type
    """
    expand = 0
    fixed = 1
    ratio = 2

class LayoutTypes(IntEnum):
    """
    | Enumerates orientation modes for Layout Nodes.
    | To be used with ui.LayoutNode().layout_orientation
    """
    vertical = 0
    horizontal = 1

class ScalingOptions(IntEnum):
    """
    | Enumerates ways for an image to scale.
    | To be used with ui.Image().scaling_option
    """
    stretch = 0
    fill = 1
    fit = 2

class NotificationTypes(IntEnum):
    """
    | Enumerates types of user notifications.
    | Each value exists as a method on nanome.util.Logs
    """
    message = 0
    success = 1
    warning = 2
    error = 3

class HorizAlignOptions(IntEnum):
    """
    | Enumerates horizontal alignment modes for text.
    | To be used with ui.Label().text_horizontal_align and ui.Button().horizontal_align
    """
    Left = 0
    Middle = 1
    Right = 2

class VertAlignOptions(IntEnum):
    """
    | Enumerates vertical alignment modes for text.
    | To be used with ui.Label().text_vertical_align and ui.Button().vertical_align
    """
    Top = 0
    Middle = 1
    Bottom = 2

class ToolTipPositioning(IntEnum):
    """
    | Enumerates ways in which a tooltip can appear on top of its Layout Node.
    | To be used with ui.Button().tooltip.positioning_target
    """
    top_right = 0
    top = 1
    top_left = 2
    left = 3
    bottom_left = 4
    bottom = 5
    bottom_right = 6
    right = 7
    center = 8

class StreamType(IntEnum):
    """
    | Enumerates object attributes and sets of attributes that can be streamed to Nanome.
    | To be used with plugin_instance.create_writing_stream and plugin_instance.create_reading_stream
    """
    position = 0
    color = 1
    scale = 2
    label = 3
    complex_position_rotation = 4
    shape_position_rotation = 5
    shape_color = 6
    sphere_shape_radius = 7

class StreamDataType(IntEnum):
    """
    | Enumerates stream datatypes.
    | Used internally
    """
    float = 0
    byte = 1
    string = 2

class StreamDirection(IntEnum):
    """
    | Enumerates stream directions (reading and writing).
    | Used internally
    """
    writing = 0
    reading = 1

class LoadFileErrorCode(IntEnum):
    """
    | An enumeration for errors when loading files into Nanome.
    | Accessible via the first parameter of the 'done' callback for plugin_instance.send_files_to_load
    """
    no_error = 0
    loading_failed = 1

class VolumeType(IntEnum):
    """
    | Enumerates volume types visible within a complex.
    | To be used with _internal._volumetric._VolumeData()._type
    """
    default = 0
    density = 1
    density_diff = 2
    cryo_em = 3
    electrostatic = 4

class VolumeVisualStyle(IntEnum):
    """
    | Enumerates ways that a complex's volume can be displayed.
    | To be used with _internal._volumetric._VolumeProperties()._style
    """
    Mesh = 0
    FlatSurface = 1
    SmoothSurface = 2

class ExportFormats(IntEnum):
    """
    | Enumerates file export formats.
    | To be used with plugin_instance.request_export
    """
    Nanome = 0
    PDB = 1
    SDF = 2
    MMCIF = 3
    SMILES = 4

class ShapeType(IntEnum):
    """
    | Enumerates types of shapes that can be created within Nanome.
    | Used internally
    """
    Sphere = 0

class ShapeAnchorType(IntEnum):
    """
    | An enumeration to represent which object type to anchor to.
    | To be used with shapes.Shape().anchors
    """
    Workspace = 0
    Complex = 1
    Atom = 2

class ColorScheme(IntEnum):
    """
    | Enumerates color schemes for all structure representations.
    | To be used with plugin_instance.apply_color_scheme
    """
    #None = 0 this one is on nanome but does nothing
    Residue = 1
    Occupancy = 2
    BFactor = 3
    Element = 4
    Rainbow = 5
    Chain = 6
    DonorAcceptor = 7
    SecondaryStructure = 8
    Monochrome = 9
    YRBHydrophobicity = 10
    Hydrophobicity = 11
    IMGT = 12
    Kabat = 13
    Chothia = 14

class ColorSchemeTarget(IntEnum):
    """
    | Enumerates structure representations.
    | To be used with plugin_instance.apply_color_scheme
    """
    AtomBond = 0
    Ribbon = 1
    Surface = 2
    All = 3

class SkyBoxes(IntEnum):
    """
    | Enumerates preset skyboxes to show in a Nanome room
    | To be used with plugin_instance.room.set_skybox
    """
    Unknown = -1
    BlueSkyAndClouds = 0
    Sunset = 1
    BlueSkyAndGround = 2
    Black = 3
    White = 4
    Graydient = 5
