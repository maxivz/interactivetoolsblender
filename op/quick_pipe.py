import bpy
import math
import blf
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from ..utils.user_prefs import get_radsym_hide_pivot
from ..utils import itools as itools
from bpy.props import EnumProperty, IntProperty


class QuickPipe(bpy.types.Operator):
    bl_idname = "mesh.quick_pipe"
    bl_label = "Quick Pipe"
    bl_description = "Generates a Pipe from selection"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', "BLOCKING"}

    mouse_x = 0.0
    mouse_mult = 1.0
    initial_pos_x = 0.0
    depth = 0
    resolution = 0
    initial_resolution = 0
    initial_depth = 0
    original_resolution = 0
    original_depth = 0
    selection = "Empty"
    senitivity = 0.01
    modkey = 0
    using_settings = False
    ignore_initial_depth = False
    ignore_initial_resolution = False
    change_resolution = False
    change_depth = False
    first_run = False

    def draw_ui(self, context, event):
        width = bpy.context.area.width

        font_id = 0
        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 140, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, "Depth: ")

        blf.color(font_id, 0, 0.8, 1, 1)
        blf.position(font_id, width / 2, 140, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(self.depth)[0:4])

        blf.color(font_id, 1, 1, 1, 1)
        blf.position(font_id, width / 2 - 100, 100, 0)
        blf.draw(font_id, "Resolution: ")

        blf.color(font_id, 0, .8, 1, 1)
        blf.position(font_id, width / 2 + 40, 100, 0)
        blf.size(font_id, 25)
        blf.draw(font_id, str(self.resolution))


    def setup_pipe(self, context, selection):
        if selection != []:
            #Select object:
            itools.set_mode('OBJECT')
            base_obj = itools.get_selected('OBJECT')

            #Separate edge:
            itools.set_mode('EDGE')
            bpy.ops.mesh.duplicate_move()
            bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.mesh.delete(type='EDGE')
            itools.set_mode('OBJECT')
            new_sel = itools.get_selected('OBJECT')
            pipe_obj = new_sel[1]

            #Convert to curve
            itools.select(pipe_obj.name, mode='OBJECT', item=False, replace=True)
            context.view_layer.objects.active = pipe_obj
            bpy.ops.object.convert(target='CURVE')
            pipe_obj.data.bevel_depth = 0.5
            bpy.ops.object.shade_smooth()
            pipe_obj.name = 'Pipe'

            self.selection = pipe_obj.name

            self.first_run = True


            dg = bpy.context.evaluated_depsgraph_get()
            dg.update()

    def calculate_depth(self, context, selection):
        if self.change_depth:
            if self.using_settings:
                self.depth = self.ui_count

            else:
                if self.ignore_initial_depth:
                    self.depth = ((self.mouse_x - self.initial_pos_x) * self.senitivity * self.mouse_mult)
                else:
                    self.depth = self.initial_depth + ((self.mouse_x - self.initial_pos_x) * self.senitivity * self.mouse_mult)

            if self.depth < 0:
                self.depth = 0
                self.initial_pos_x = self.mouse_x
                self.ignore_initial_depth = True

            bpy.context.view_layer.objects.active = selection

            bpy.context.object.data.bevel_depth = self.depth
            self.change_depth = False
    
    def calculate_resolution(self, context, selection):
        if self.change_resolution:
            if self.using_settings:
                self.resolution = self.ui_count

            else:
                if self.ignore_initial_resolution:
                    self.resolution = int(((self.mouse_x - self.initial_pos_x) * self.senitivity))
                else:
                    self.resolution = self.initial_resolution + int(((self.mouse_x - self.initial_pos_x) * self.senitivity))

            if self.resolution < 1:
                self.resolution = 1
                self.initial_pos_x = self.mouse_x
                self.ignore_initial_resolution = True

            bpy.context.view_layer.objects.active = selection
            bpy.context.object.data.bevel_resolution = self.resolution
            self.change_resolution = False

    def recover_settings(self, context, selection):
        self.initial_resolution = bpy.context.object.data.bevel_resolution
        self.initial_depth = bpy.context.object.data.bevel_depth

        self.resolution = self.initial_resolution
        self.depth = self.initial_depth

        if not self.first_run:
            self.original_resolution = self.initial_resolution
            self.original_depth = self.initial_depth

    def restore_settings(self, context, selection):
        bpy.context.object.data.bevel_resolution = self.original_resolution
        bpy.context.object.data.bevel_depth = self.original_depth

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    """
    @classmethod
    def poll(cls, context):
        return ((context.mode == 'OBJECT' and bpy.context.object.modifiers.find("Cylindrical Sides") > -1) or
                bpy.context.mode == 'EDIT_MESH')
    """

    def execute(self, context):
        #self.sync_ui_settings()
        self.calculate_depth(context, bpy.data.objects[self.selection])
        self.calculate_resolution(context, bpy.data.objects[self.selection])

        return{'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            if event.ctrl:
                if self.modkey != 1:
                    self.modkey = 1
                    self.initial_pos_x = event.mouse_x
                    self.initial_resolution = self.resolution
                self.change_resolution = True

            else:
                if self.modkey != 0:
                    self.modkey = 0
                    self.initial_pos_x = event.mouse_x
                    self.initial_depth = self.depth
                if event.shift:
                     self.mouse_mult = 0.5
                else:
                    self.mouse_mult = 1.0


                self.change_depth = True

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
        context.area.header_text_set("LMB: confirm, RMB:Cancel, Mouse Left/Right for depth, CTRL + Mouse Left/ Right to change resolution, Shift for Precision Mode")
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_pos_x = event.mouse_x
        self.selection = bpy.context.active_object.name

        if not "Pipe" in self.selection:
            self.setup_pipe(context, bpy.data.objects[self.selection])

        self.recover_settings(context, bpy.data.objects[self.selection])

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_ui, (self, context), 'WINDOW','POST_PIXEL')

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
