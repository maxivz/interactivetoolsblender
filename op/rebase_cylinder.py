import bpy
from .. utils import itools as itools
import math
import blf
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from ..utils.user_prefs import get_radsym_hide_pivot
from bpy.props import EnumProperty, IntProperty
import datetime


class RebaseCylinder(bpy.types.Operator):
    bl_idname = "mesh.rebase_cylinder"
    bl_label = "Rebase Cylinder"
    bl_description = "Reconstruct cylinder with a different number of sides"
    bl_options = {'REGISTER', 'UNDO', "GRAB_CURSOR", "BLOCKING"}

    mouse_x = 0.0
    initial_pos_x = 0.0
    sides_count = 0
    rebase_axis = 0
    merge_distance = 0.0
    initial_rebase_axis = 0
    initial_sides_count = 0
    initial_merge_distance = 0.0
    original_rebase_axis = 0
    original_sides_count = 0
    original_merge_distance = 0.0
    selection = "Empty"
    senitivity = 0.01
    modkey = 0
    using_settings = False
    ignore_initial_sym_count = False
    change_axis = False
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
        blf.draw(font_id, str(self.sides_count))

        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 100, 0)
        blf.draw(font_id, "Axis: ")

        blf.color(font_id, 0, .8, 1, 1)
        blf.position(font_id, width / 2, 100, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(self.ui_axis)[2])

        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 60, 0)
        blf.draw(font_id, "Merge Dist: ")

        blf.color(font_id, 0, .8, 1, 1)
        blf.position(font_id, width / 2 + 60, 60, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(self.merge_distance)[0:6])

    def setup_rebase(self, context, selection):
        if selection != []:
            # Separate Selected Edge
            bpy.ops.mesh.separate(type='SELECTED')
            new_selection = bpy.context.selected_objects
            mesh_to_select = list(filter(lambda x: x.name != selection.name, new_selection))
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[mesh_to_select[0].name].select_set(state=True)
            bpy.context.view_layer.objects.active = mesh_to_select[0]
            self.selection = mesh_to_select[0].name

            # Create modifier and assign name
            bpy.ops.object.modifier_add(type='SCREW')
            mod = bpy.context.object.modifiers["Screw"]
            mod.name = "Cylindrical Sides"
            mod.use_merge_vertices = True

            # Update both depsgraph and viewlayer
            bpy.context.view_layer.objects.active = selection
            bpy.context.view_layer.update()

            self.first_run = True

            dg = bpy.context.evaluated_depsgraph_get()
            dg.update()

    def calculate_iterations(self, context, selection):
        if self.change_iteration:
            if self.using_settings:
                self.sides_count = self.ui_count

            else:
                if self.ignore_initial_sym_count:
                    self.sides_count = int(((self.mouse_x - self.initial_pos_x) * self.senitivity))
                else:
                    self.sides_count = self.initial_sides_count + int(((self.mouse_x - self.initial_pos_x) * self.senitivity))

            if self.sides_count < 1:
                self.sides_count = 1
                self.initial_pos_x = self.mouse_x
                self.ignore_initial_sym_count = True

            bpy.context.view_layer.objects.active = selection

            selection.modifiers["Cylindrical Sides"].steps = self.sides_count
            self.change_iteration = False

    def calculate_axis(self, context, selection):
        if self.change_axis:
            self.rebase_axis = int((self.initial_rebase_axis + (self.mouse_x - self.initial_pos_x) * self.senitivity) % 3)

            if self.rebase_axis == 0:
                selection.modifiers["Cylindrical Sides"].axis = "X"

            elif self.rebase_axis == 1:
                selection.modifiers["Cylindrical Sides"].axis = "Y"

            elif self.rebase_axis == 2:
                selection.modifiers["Cylindrical Sides"].axis = "Z"

            self.change_axis = False

    def calculate_merge_distance(self, context, selection):
        if self.merge_distance == 0.01:
            self.merge_distance = 0.001

        elif self.merge_distance == 0.001:
            self.merge_distance = 0.0001

        else:
            self.merge_distance = 0.01

        selection.modifiers["Cylindrical Sides"].merge_threshold = self.merge_distance
        

    def sync_ui_settings(self):
        global axis
        # Use UI settings to drive parameters
        if self.using_settings:
            if 'X' in self.ui_axis:
                self.rebase_axis = 0

            elif 'Y' in self.ui_axis:
                self.rebase_axis = 1

            elif 'Z' in self.ui_axis:
                self.rebase_axis = 2

            self.sides_count = self.ui_count

            self.change_iteration = True
            self.change_rotation = True

        # Sync UI information
        else:
            if self.rebase_axis == 0:
                self.ui_axis = {'X'}

            elif self.rebase_axis == 1:
                self.ui_axis = {'Y'}

            elif self.rebase_axis == 2:
                self.ui_axis = {'Z'}

            self.ui_count = self.sides_count

    def recover_settings(self, context, selection):
        mod = selection.modifiers["Cylindrical Sides"]
        self.initial_sides_count = mod.steps
        self.initial_merge_distance = mod.merge_threshold

        if mod.axis == 'X':
            self.initial_rebase_axis = 0

        elif mod.axis == 'Y':
            self.initial_rebase_axis = 1

        elif mod.axis == 'Z':
            self.initial_rebase_axis = 2

        self.rebase_axis = self.initial_rebase_axis
        self.sides_count = self.initial_sides_count
        self.merge_distance = self.initial_merge_distance 

        if not self.first_run:
            self.original_rebase_axis = self.initial_rebase_axis
            self.original_sides_count = self.initial_sides_count
            self.original_merge_distance = self.initial_merge_distance


    def restore_settings(self, context, selection):
        mod = selection.modifiers["Cylindrical Sides"]
        mod.steps = self.original_sides_count

        if self.original_rebase_axis == 0:
            mod.axis = "X"

        elif self.original_rebase_axis == 1:
            mod.axis = "Y"

        elif self.original_rebase_axis == 2:
            mod.axis = "Z"
        
        mod.merge_threshold = self.original_merge_distance

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    @classmethod
    def poll(cls, context):
        if  bpy.context.object != None:
            return ((context.mode == 'OBJECT' and bpy.context.object.modifiers.find("Cylindrical Sides") > -1) or
                    bpy.context.mode == 'EDIT_MESH')
        else:
            return False

    def execute(self, context):
        self.sync_ui_settings()
        self.calculate_iterations(context, bpy.data.objects[self.selection])
        self.calculate_axis(context, bpy.data.objects[self.selection])

        return{'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            if event.ctrl:
                if self.modkey != 1:
                    self.modkey = 1
                    self.initial_pos_x = event.mouse_x
                    self.initial_sides_count = self.sides_count
                self.change_axis = True

            else:
                if self.modkey != 0:
                    self.modkey = 0
                    self.initial_pos_x = event.mouse_x
                    self.initial_rebase_axis = self.rebase_axis
                self.change_iteration = True

            self.mouse_x = event.mouse_x
            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            if event.value == 'RELEASE':
                self.using_settings = True
                context.area.header_text_set(text=None)
                bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')

                #Switch between modes to force update UI
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='OBJECT')
                return {'FINISHED'}

        elif event.type == 'M':  # Change Merge threshold
            if event.value == 'RELEASE':
                self.calculate_merge_distance(context, bpy.data.objects[self.selection])

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            if not self.first_run:
                self.restore_settings(context, bpy.data.objects[self.selection])

            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
            context.area.header_text_set(text=None)

            #Switch between modes to force update UI
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode='OBJECT')

            if self.first_run:
                bpy.ops.object.delete(use_global=False, confirm=False)
            return {'CANCELLED'}

        #Tooltip
        context.area.header_text_set("LMB: confirm, RMB:Cancel, Mouse Left/Right for number of instances, CTRL + Mouse Left/ Right to change Axis, M changes merge threshold precission")
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_pos_x = event.mouse_x
        self.selection = bpy.context.active_object.name

        if bpy.context.object.modifiers.find("Cylindrical Sides") < 0:
            self.setup_rebase(context, bpy.data.objects[self.selection])

        self.recover_settings(context, bpy.data.objects[self.selection])

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_ui, (self, context), 'WINDOW','POST_PIXEL')

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

"""
bpy.context.object.modifiers["Cylindrical Sides"].use_merge_vertices = True
bpy.context.object.modifiers["Cylindrical Sides"].merge_threshold = 0.001
"""