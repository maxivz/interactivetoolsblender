import bpy
import math
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from ..utils.user_prefs import get_radsym_hide_pivot
from ..utils import itools as itools
from bpy.props import EnumProperty, IntProperty


class QuickPipe(bpy.types.Operator):
    bl_idname = "mesh.quick_pipe"
    bl_label = "Quick Pipe"
    bl_description = "Generates a Pipe from selection"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR'}

    mouse_x = 0.0
    initial_pos_x = 0.0
    bevel_size = 0
    pipe_obj = "Empty"
    pipe_resolution = 12
    senitivity = 0.01
    modkey = 0
    change_resolution = False
    symmetry_center = ""

    def setup_pipe(self, context):
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
        print([pipe_obj])

        #Convert to curve
        itools.select(pipe_obj.name, mode='OBJECT', item=False, replace=True)
        context.view_layer.objects.active = pipe_obj
        bpy.ops.object.convert(target='CURVE')
        pipe_obj.data.bevel_depth = 0.5
        bpy.ops.object.shade_smooth()
        pipe_obj.name = 'Pipe'
        bpy.ops.wm.context_modal_mouse('INVOKE_DEFAULT',
                                           data_path_iter='selected_editable_objects',
                                           data_path_item='data.bevel_depth',
                                           input_scale=0.02000000149011612,
                                           header_text='Pipe Thickness %.f')

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    @classmethod
    def poll(cls, context):
        return itools.get_mode() == 'EDGE'

    def execute(self, context):
        self.setup_pipe(context)
        return{'FINISHED'}
