import bpy
import math
import blf
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from ..utils.user_prefs import get_radsym_hide_pivot
from bpy.props import EnumProperty, IntProperty
import datetime


class QuickRadialSymmetry(bpy.types.Operator):
    bl_idname = "mesh.radial_symmetry"
    bl_label = "Radial Symmetry"
    bl_description = "Setup a Quick Radial Symmetry"
    bl_options = {'REGISTER', 'UNDO',  "GRAB_CURSOR", "BLOCKING"}

    """
    Editing menu disabled until I figure out solution to bug
    ui_axis: EnumProperty(
        name="Symmetry Axis:",
        description="Axis to use for the symmetry",
        items=(
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ),
        options={'ENUM_FLAG'},
    )

    ui_count: IntProperty(
        name="Number :",
        description="Number of iterations",
        default=1,
        min=1,
    )
    """

    mouse_x = 0.0
    initial_pos_x = 0.0
    sym_count = 0
    sym_axis = 0
    initial_sym_axis = 0
    initial_sym_count = 0
    original_sym_axis = 0
    original_sym_count = 0
    offset_obj = "Empty"
    selection = "Empty"
    senitivity = 0.01
    modkey = 0
    using_settings = False
    ignore_initial_sym_count = False
    change_axis = False
    change_rotation = False
    change_iteration = False
    symmetry_center = ""
    first_run = False

    def draw_ui(self, context, event):
        width = bpy.context.area.width

        font_id = 0
        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 140, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, "Count: ")

        blf.color(font_id, 0, 0.8, 1, 1)
        blf.position(font_id, width / 2, 140, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(self.sym_count))

        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 100, 0)
        blf.draw(font_id, "Axis: ")

        blf.color(font_id, 0, .8, 1, 1)
        blf.position(font_id, width / 2, 100, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(self.ui_axis)[2])

        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 60, 0)
        blf.draw(font_id, "Show Origin: ")

        blf.color(font_id, 0, .8, 1, 1)
        blf.position(font_id, width / 2 + 60, 60, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(not bpy.data.objects[self.offset_obj].hide_viewport))

    def setup_symmetry(self, context, selection):
        if selection != []:
            sel_pivot = selection.location
            new_obj = bpy.data.objects.new('new_obj', None)
            bpy.ops.object.empty_add(type='ARROWS', location=sel_pivot)
            self.symmetry_center = bpy.context.active_object
            self.symmetry_center.rotation_euler = (0, 0, math.radians(120))
            self.symmetry_center.name = selection.name + ".SymmetryPivot"
            self.symmetry_center.select_set(False)

            #Parent the pivot to the object and manage visibility
            self.symmetry_center.parent = selection
            self.symmetry_center.hide_viewport = get_radsym_hide_pivot()
            selection.select_set(True)

            #Clear Pivot Transform
            self.symmetry_center.location = (0,0,0)

            # Create modifier and assign name
            mod = selection.modifiers.new(name="Radial Symmetry", type='ARRAY')
            mod.relative_offset_displace[0] = 0
            mod.count = 3
            mod.offset_object = bpy.data.objects[self.symmetry_center.name]
            mod.use_object_offset = True

            # Update both depsgraph and viewlayer
            bpy.context.view_layer.objects.active = selection
            bpy.context.view_layer.update()

            dg = bpy.context.evaluated_depsgraph_get()
            dg.update()

    def calculate_iterations(self, context, selection):
        if self.change_iteration:
            if self.using_settings:
                self.sym_count = self.ui_count

            else:
                if self.ignore_initial_sym_count:
                    self.sym_count = int(((self.mouse_x - self.initial_pos_x) * self.senitivity))
                else:
                    self.sym_count = self.initial_sym_count + int(((self.mouse_x - self.initial_pos_x) * self.senitivity))

            if self.sym_count < 1:
                self.sym_count = 1
                self.initial_pos_x = self.mouse_x
                self.ignore_initial_sym_count = True

            bpy.context.view_layer.objects.active = selection

            selection.modifiers["Radial Symmetry"].count = self.sym_count
            self.change_iteration = False

    def calculate_axis(self, context):
        if self.change_axis:
            self.sym_axis = int((self.initial_sym_axis + (self.mouse_x - self.initial_pos_x) * self.senitivity) % 3)
            self.change_axis = False

    def calculate_rotation(self, axis):
        if self.change_rotation:
            if axis == 0:
                bpy.data.objects[self.offset_obj].rotation_euler = (math.radians(360 / self.sym_count), 0, 0)

            elif axis == 1:
                bpy.data.objects[self.offset_obj].rotation_euler = (0, math.radians(360 / self.sym_count), 0)

            elif axis == 2:
                bpy.data.objects[self.offset_obj].rotation_euler = (0, 0, math.radians(360 / self.sym_count))
            self.change_rotation = False

    def sync_ui_settings(self):
        global axis
        # Use UI settings to drive parameters

        if self.using_settings:
            if 'X' in self.ui_axis:
                self.sym_axis = 0

            elif 'Y' in self.ui_axis:
                self.sym_axis = 1

            elif 'Z' in self.ui_axis:
                self.sym_axis = 2

            self.sym_count = self.ui_count

            self.change_iteration = True
            self.change_rotation = True

        # Sync UI information
        else:
            if self.sym_axis == 0:
                self.ui_axis = {'X'}

            elif self.sym_axis == 1:
                self.ui_axis = {'Y'}

            elif self.sym_axis == 2:
                self.ui_axis = {'Z'}

            self.ui_count = self.sym_count

    def recover_settings(self, context, selection):
        mod = selection.modifiers["Radial Symmetry"]
        self.initial_sym_count = mod.count
        self.offset_obj = mod.offset_object.name
        rotation = mod.offset_object.rotation_euler

        if rotation[0] > 0:
            self.initial_sym_axis = 0

        elif rotation[1] > 0:
            self.initial_sym_axis = 1

        elif rotation[2] > 0:
            self.initial_sym_axis = 2

        self.sym_axis = self.initial_sym_axis
        self.sym_count = self.initial_sym_count

        if not self.first_run:
            self.original_sym_axis = self.initial_sym_axis
            self.original_sym_count = self.initial_sym_count

    def restore_settings(self, context, selection):
        selection.modifiers["Radial Symmetry"].count = self.original_sym_count

        if self.original_sym_axis == 0:
                bpy.data.objects[self.offset_obj].rotation_euler = (math.radians(360 / self.original_sym_count), 0, 0)

        elif self.original_sym_axis == 1:
            bpy.data.objects[self.offset_obj].rotation_euler = (0, math.radians(360 / self.original_sym_count), 0)

        elif self.original_sym_axis == 2:
            bpy.data.objects[self.offset_obj].rotation_euler = (0, 0, math.radians(360 / self.original_sym_count))

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 0

    def execute(self, context):
        self.sync_ui_settings()
        self.calculate_iterations(context, bpy.data.objects[self.selection])
        self.calculate_axis(context)
        self.calculate_rotation(self.sym_axis)
        return{'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            if event.ctrl:
                if self.modkey != 1:
                    self.modkey = 1
                    self.initial_pos_x = event.mouse_x
                    self.initial_sym_count = self.sym_count
                self.change_axis = True

            else:
                if self.modkey != 0:
                    self.modkey = 0
                    self.initial_pos_x = event.mouse_x
                    self.initial_sym_axis = self.sym_axis
                self.change_iteration = True

            self.mouse_x = event.mouse_x
            self.execute(context)
            self.change_rotation = True

        elif event.type in {'H', 'Z'}:  # Show Pivot
            if event.value == 'RELEASE':
                if bpy.data.objects[self.offset_obj].hide_viewport:
                    bpy.data.objects[self.offset_obj].hide_viewport = False
                else:
                    bpy.data.objects[self.offset_obj].hide_viewport = True

        elif event.type == 'LEFTMOUSE':  # Confirm
            if event.value == 'RELEASE':
                self.using_settings = True
                context.area.header_text_set(text=None)
                bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')

                #Switch between modes to force update UI
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='OBJECT')
                return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            if not self.first_run:
                self.restore_settings(context, bpy.data.objects[self.selection])
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
            context.area.header_text_set(text=None)

            #Switch between modes to force update UI
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode='OBJECT')

            if self.first_run:
                bpy.ops.object.modifier_remove(modifier="Radial Symmetry")

            return {'CANCELLED'}

        #Tooltip
        context.area.header_text_set("LMB: confirm, RMB:Cancel, Mouse Left/Right for number of instances, CTRL + Mouse Left/ Right to change Symmetry Axis H: Show / Hide Origin")
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_pos_x = event.mouse_x
        self.selection = bpy.context.active_object.name

        if bpy.data.objects[self.selection].modifiers.find("Radial Symmetry") < 0:
            self.setup_symmetry(context, bpy.data.objects[self.selection])
            self.first_run = True

        self.recover_settings(context, bpy.data.objects[self.selection])

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_ui, (self, context), 'WINDOW','POST_PIXEL')

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    """
    Editing menu disabled until I figure out solution to bug
    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row1 = col.row()
        row1.label(text="Count")
        row1.prop(self, "ui_count", text="")

        row2 = col.row()
        row2.label(text="Axis")
        row2.prop(self, "ui_axis")
    """
