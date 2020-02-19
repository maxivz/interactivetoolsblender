import bpy
from ..utils import itools as itools
from ..utils import mesh as mesh


class SmartModify(bpy.types.Operator):
    bl_idname = "mesh.smart_modify"
    bl_label = "Smart Modify Pie"
    bl_description = "Context sensitive modification pie menu"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_modify(self):
        context = bpy.context.area.ui_type

        if context == 'UV':
            bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_uv")
        else:
            mode = itools.get_mode()
            if mode == 'OBJECT':
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_object")
            elif mode in ['VERT', 'EDGE', 'FACE']:
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_mesh")
            elif mode == 'EDIT_CURVE':
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_curve")
            elif mode == 'EDIT_LATTICE':
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_SM_lattice")

    def execute(self, context):
        self.smart_modify()
        return{'FINISHED'}
