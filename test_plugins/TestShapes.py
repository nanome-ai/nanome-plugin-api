from nanome.util.vector3 import Vector3
import nanome
import random
import itertools
from nanome.api.shapes import Sphere, Line, Anchor

# Config

NAME = "Test Shapes"
DESCRIPTION = "Tests for plugin shapes API"
CATEGORY = "Tests"
HAS_ADVANCED_OPTIONS = False


class TestShapes(nanome.PluginInstance):
    def start(self):
        sf = TestShapes.SphereFactory
        sf.parent = self
        lf = TestShapes.LineFactory
        lf.parent = self
        self.menu = nanome.ui.Menu()
        menu = self.menu
        menu.title = "Shapes"
        menu.width = 0.5
        menu.height = 0.5

        left = nanome.ui.LayoutNode()
        left.layout_orientation = nanome.util.enums.LayoutTypes.vertical

        ln_label = left.create_child_node()
        label = ln_label.add_new_label()
        label.text_value = "spheres"
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Add to workspace")
        btn.register_pressed_callback(sf.create_in_workspace)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Add to random complex")
        btn.register_pressed_callback(sf.create_in_complex)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Add to random atom")
        btn.register_pressed_callback(sf.create_in_atom)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Change anchor last created")
        btn.register_pressed_callback(sf.change_anchor)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Delete last created")
        btn.register_pressed_callback(sf.delete_last)

        right = nanome.ui.LayoutNode()
        right.layout_orientation = nanome.util.enums.LayoutTypes.vertical

        ln_label = right.create_child_node()
        label = ln_label.add_new_label()
        label.text_value = "lines"
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Add to workspace")
        btn.register_pressed_callback(lf.create_in_workspace)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Add to random complex")
        btn.register_pressed_callback(lf.create_in_complex)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Add to random atom")
        btn.register_pressed_callback(lf.create_in_atom)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Change anchor last created")
        btn.register_pressed_callback(lf.change_anchor)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Delete last created")
        btn.register_pressed_callback(lf.delete_last)

        menu.root.layout_orientation = nanome.util.enums.LayoutTypes.horizontal
        menu.root.add_child(left)
        menu.root.add_child(right)

    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    class SphereFactory():
        spheres = []
        parent = None

        @classmethod
        def create_in_workspace(cls, button):
            sphere = cls.create_random_sphere()

            def done(success):
                cls.spheres.append(sphere)
            sphere.upload(done)

        @classmethod
        def create_in_complex(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)

                sphere = cls.create_random_sphere()
                sphere.anchor = nanome.util.enums.ShapeAnchorType.Complex
                sphere.target = workspace.complexes[c].index

                def done(success):
                    cls.spheres.append(sphere)
                sphere.upload(done)

            cls.parent.request_workspace(received)

        @classmethod
        def create_in_atom(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)
                atom_count = 0
                for _ in workspace.complexes[c].atoms:
                    atom_count += 1
                a = random.randrange(0, atom_count - 1)

                sphere = cls.create_random_sphere()
                sphere.anchor = nanome.util.enums.ShapeAnchorType.Atom
                if a == 0:
                    atom = next(workspace.complexes[c].atoms)
                else:
                    atom = next(itertools.islice(workspace.complexes[c].atoms, a, None))
                sphere.target = atom.index
                sphere.position = nanome.util.Vector3()

                def done(success):
                    cls.spheres.append(sphere)
                sphere.upload(done)

            cls.parent.request_workspace(received)

        @classmethod
        def change_anchor(cls, button):
            if len(cls.spheres) == 0:
                return
            shape = cls.spheres[-1]
            shape.anchor = (shape.anchor + 1) % len(nanome.util.enums.ShapeAnchorType)
            shape.upload()

        @classmethod
        def delete_last(cls, button):
            if len(cls.spheres) == 0:
                return
            shape = cls.spheres.pop()
            shape.destroy()

        @classmethod
        def create_random_sphere(cls):
            sphere = Sphere()
            sphere.radius = random.uniform(0.5, 2.0)
            sphere.position = nanome.util.Vector3(random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0))
            sphere.color = nanome.util.Color(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), random.randrange(100, 255))
            return sphere

    class LineFactory():
        queued_anchor = None
        lines = []
        parent = None

        @classmethod
        def create_in_workspace(cls, button):
            cls.create_anchor(0, nanome.util.enums.ShapeAnchorType.Workspace)

        @classmethod
        def create_in_complex(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)

                cls.create_anchor(workspace.complexes[c].index, nanome.util.enums.ShapeAnchorType.Complex)

            cls.parent.request_workspace(received)

        @classmethod
        def create_in_atom(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)
                atom_count = 0
                for _ in workspace.complexes[c].atoms:
                    atom_count += 1
                a = random.randrange(0, atom_count - 1)

                if a == 0:
                    atom = next(workspace.complexes[c].atoms)
                else:
                    atom = next(itertools.islice(workspace.complexes[c].atoms, a, None))
                
                cls.create_anchor(atom.index, nanome.util.enums.ShapeAnchorType.Atom)

            cls.parent.request_workspace(received)

        @classmethod
        def change_anchor(cls, button):
            if len(cls.lines) == 0:
                return
            shape = cls.lines[-1]
            shape.anchor = (shape.anchor + 1) % len(nanome.util.enums.ShapeAnchorType)
            shape.upload()

        @classmethod
        def delete_last(cls, button):
            if len(cls.lines) == 0:
                return
            shape = cls.lines.pop()
            shape.destroy()

        @classmethod
        def create_anchor(cls, target, a_type):
            anchor = Anchor()
            anchor.target = target
            anchor.offset = nanome.util.Vector3(random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0))
            anchor.anchor_type = a_type
            if cls.queued_anchor == None:
                cls.queued_anchor = anchor
            else:
                cls.create_line(cls.queued_anchor, anchor)
                cls.queued_anchor = None

        @classmethod
        def create_line(cls, anchor1, anchor2):
            line = Line()
            line.thickness = random.uniform(0.5, 2.0)
            line.anchors = [anchor1, anchor2]
            def done(success):
                cls.lines.append(line)
            line.upload(done)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, TestShapes)
