import bpy
from ..utils import itools as itools
from ..utils import mesh as mesh
from ..utils.user_prefs import get_loop_tools_active, get_set_flow_active


class SmartModify(bpy.types.Operator):
    bl_idname = "mesh.smart_modify"
    bl_label = "Smart Modify"
    bl_description = "Context sensitive modification pie menu"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_modify(self):
        mode = itools.get_mode()
        if mode == 'OBJECT':
            bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_object")
        elif mode in ['VERT','EDGE','FACE']:
            bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_mesh")
        elif mode == 'EDIT_CURVE':
            bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_curve")
        elif mode == 'EDIT_LATTICE':
            bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_lattice")

    @classmethod
    def poll(cls, context):
        return get_loop_tools_active()

    def execute(self, context):
        self.smart_modify()
        return{'FINISHED'}
