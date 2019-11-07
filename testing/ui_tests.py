import nanome
import os
# from nanome import UI
import nanome.api.ui as UI
from nanome._internal._ui._serialization import _LayoutNodeSerializer, _UIBaseSerializer
from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
# from nanome.serialization.commands import ReceiveMenu, UpdateMenu
from testing.utilities import *

#testing structures
def test_ui():
    button = UI.Button()
    label = UI.Label()
    mesh = UI.Mesh()
    slider = UI.Slider()
    text_input = UI.TextInput()
    image = UI.Image()
    loading_bar = UI.LoadingBar()
    _list = UI.UIList()
    # ui_base = UI.UIBase()
    menu = UI.Menu()

def prefab_button_pressed_callback(btn):
    pass

def CreateMenu():
    value = UI.Menu()
    value = alter_object(value)
    value.root.name = "node"
    return value
def CreateButton():
    value = UI.Button()
    value = alter_object(value)
    return value
def CreateMesh():
    value = UI.Mesh()
    value = alter_object(value)
    return value
def CreateSlider():
    value = UI.Slider()
    value = alter_object(value)
    return value
def CreateTextInput():
    value = UI.TextInput()
    value = alter_object(value)
    return value
def CreateLabel():
    value = UI.Label()
    value = alter_object(value)
    return value
def CreateList():
    prefab = nanome.ui.LayoutNode()
    prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.vertical
    child1 = nanome.ui.LayoutNode()
    child1.sizing_type = nanome.ui.LayoutNode.SizingTypes.ratio
    child1.sizing_value = .3
    child1.name = "label"
    child1.forward_dist = .01
    child2 = nanome.ui.LayoutNode()
    child2.name = "button"
    child2.forward_dist =.01
    prefab.add_child(child1)
    prefab.add_child(child2)
    prefabLabel = nanome.ui.Label()
    prefabLabel.text_value = "Molecule Label"
    prefabButton = nanome.ui.Button()
    prefabButton.text.active = True
    prefabButton.text.value.set_all("Molecule Button")
    prefabButton.register_pressed_callback(prefab_button_pressed_callback)
    child1.set_content(prefabLabel)
    child2.set_content(prefabButton)

    list_content = []
    for _ in range(0, 10):
        clone = prefab.clone()
        list_content.append(clone)

    list = nanome.ui.UIList()
    list.display_columns = 1
    list.display_rows = 1
    list.total_columns = 1
    list.items = list_content
    return list
def CreateLayoutNode():
    value = UI.LayoutNode()
    value = alter_object(value)
    value.name = "node"
    return value

class FakeNetwork():
    def __init__(self, original):
        self.original = original
        pass
    def on_menu_received(self, menu):
        #del menu._root_id
        menu._id = 0
        self.original._id = 0
        assert(self.original != menu)
        assert_equal(self.original, menu)

# def test_menu_serialization():
#     obj_to_test = CreateMenu()
#     serializer = UpdateMenu()
#     deserializer = ReceiveMenu()
#     context_s = ContextSerialization()
#     serializer.serialize(obj_to_test, context_s)
#     context_d = ContextDeserialization(context_s.to_array())
#     result = deserializer.deserialize(context_d)
#     import nanome.core
#     import nanome.api.menu
#     nanome.api.menu.receive_menu(FakeNetwork(obj_to_test), result)



def check_multi(multi):
    check_property(multi, "idle")
    check_property(multi, "selected")
    check_property(multi, "highlighted")
    check_property(multi, "selected_highlighted")
    check_property(multi, "unusable")
    check_set_all(multi, rand_string())

def check_property(obj, property_name):
    v = rand_string()
    prop = get_property(obj, property_name)
    prop.fset(v)
    assert(prop.fget() == v)

def check_set_all(multi, value):
    multi.set_all(value)
    assert_multi(multi, value)

def assert_multi(multi, value):
    assert(multi.idle == value)
    assert(multi.selected == value)
    assert(multi.highlighted == value)
    assert(multi.selected_highlighted == value)
    assert(multi.unusable == value)

class FakeProperty(object):
    def __init__(self, fset, fget):
        self.fset = fset
        self.fget = fget

def get_property(obj, attr):
    from functools import partial
    import collections
    for it in [obj] + obj.__class__.mro():
        if attr in it.__dict__:
            prop = it.__dict__[attr]
            fset = partial(prop.fset, obj)
            fget = partial(prop.fget, obj)
            fp = FakeProperty(fset, fget)
            return fp
    raise AttributeError

#region deprecation testing
def test_deprecated_button():
    suspend_warning()
    button = UI.Button()
    test_multi_var(button.text.value, button.text, "value")
    test_multi_var(button.icon.value, button.icon, "value")
    test_multi_var(button.icon.color, button.icon, "color")
    value = "bolded1234"
    button.text.bolded = value
    assert_multi(button.text.bold, value)
    button.set_all_text(value)
    assert_multi(button.text.value, value)
    button.set_all_icon(value)
    assert_multi(button.icon.value, value)
    restore_warning()

def suspend_warning():
    global suspensions
    global warned

    if nanome.util.Logs.warning != confirm_warning:
        nanome.util.Logs.s_warning = nanome.util.Logs.warning
        nanome.util.Logs.warning = confirm_warning
        suspensions = 0
    warned = False
    suspensions += 1
    nanome.util.Logs.warning("suspended")

def restore_warning():
    global suspensions
    global warned
    suspensions -= 1
    if suspensions == 0:
        nanome.util.Logs.warning = nanome.util.Logs.s_warning

def confirm_warning(txt):
    global warned
    warned = True

def assert_warning():
    global warned
    assert(warned)
    warned = False

#tests that a multi-variable is equivalent to a collection of single-variables
#multi is the multi variable object
#obj is the base class for the single-variable properties
#base string of the base name of the property (ex: for value_idle base would be "value" )
#set_all is the set all function for the single properties
def test_multi_var(multi, obj, base):

    suspend_warning()
    #this compares the values of 1 of the values in the multi with a single
    def test_var(multi, single):
        single.fset("val1")
        assert_warning()
        assert(multi.fget() == single.fget())
        assert_warning()
    #this gets the property for us so we can test it.
    s_idle = get_property(obj, base + "_idle")
    m_idle = get_property(multi, "idle")
    test_var(m_idle, s_idle)
    s_selected = get_property(obj, base + "_selected")
    m_selected = get_property(multi, "selected")
    test_var(m_selected, s_selected)
    s_highlighted = get_property(obj, base + "_highlighted")
    m_highlighted = get_property(multi, "highlighted")
    test_var(m_highlighted, s_highlighted)
    s_selected_highlighted = get_property(obj, base + "_selected_highlighted")
    m_selected_highlighted = get_property(multi, "selected_highlighted")
    test_var(m_selected_highlighted, s_selected_highlighted)
    s_unusable = get_property(obj, base + "_unusable")
    m_unusable = get_property(multi, "unusable")
    test_var(m_unusable, s_unusable)
    restore_warning()
#endregion

def button_api_test():
    val1 = rand_string()
    val2 = rand_string()
    button = UI.Button(val1, val2)
    assert_multi(button.text.value, val1)
    assert_multi(button.icon.value, val2)
    text = button.text
    #text
    check_property(text, "active")
    check_multi(text.value)
    check_property(text, "auto_size")
    check_property(text, "min_size")
    check_property(text, "max_size")
    check_property(text, "size")
    check_property(text, "underlined")
    check_property(text, "ellipsis")
    check_multi(text.bold)
    check_multi(text.color)
    check_property(text, "padding_top")
    check_property(text, "padding_bottom")
    check_property(text, "padding_left")
    check_property(text, "padding_right")
    check_property(text, "line_spacing")
    check_property(text, "vertical_align")
    check_property(text, "horizontal_align")
    #icon
    icon = button.icon
    check_property(icon, "active")
    check_multi(icon.value)
    check_multi(icon.color)
    check_property(icon, "sharpness")
    check_property(icon, "size")
    check_property(icon, "ratio")
    check_property(icon, "position")
    check_property(icon, "rotation")
    #mesh
    mesh = button.mesh
    check_property(mesh, "active")
    check_multi(mesh.enabled)
    check_multi(mesh.color)
    #outline
    outline = button.outline
    check_property(outline, "active")
    check_multi(outline.size)
    check_multi(outline.color)
    #tooltip
    tooltip = button.tooltip
    check_property(tooltip, "title")
    check_property(tooltip, "content")
    check_property(tooltip, "bounds")
    check_property(tooltip, "positioning_target")
    check_property(tooltip, "positioning_origin")

def run(counter):
    options = TestOptions(ignore_vars=["_name", "icon", "_icon"])
    run_test(test_ui, counter)
    run_test(button_api_test, counter)
    run_test(test_deprecated_button, counter)
    run_test(create_test("button_test", test_serializer, (_UIBaseSerializer(), CreateButton(), options)), counter)
    run_test(create_test("mesh_test", test_serializer, (_UIBaseSerializer(), CreateMesh(), options)), counter)
    run_test(create_test("slider_test", test_serializer, (_UIBaseSerializer(), CreateSlider(), options)), counter)
    run_test(create_test("text_input_test", test_serializer, (_UIBaseSerializer(), CreateTextInput(), options)), counter)
    run_test(create_test("label_test", test_serializer, (_UIBaseSerializer(), CreateLabel(), options)), counter)
    run_test(create_test("list_and_clone_test", test_serializer, (_UIBaseSerializer(), CreateList(), options)), counter)
    test_node = CreateLayoutNode()
    test_node._child_ids = []
    test_node._content_id = None
    run_test(create_test("layout_test", test_serializer, (_LayoutNodeSerializer(), test_node)), counter)

    # run_test(test_menu_serialization, counter)