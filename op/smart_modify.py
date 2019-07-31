import bpy
from ..utils import itools as itools
from ..utils import mesh as mesh
from ..utils.user_prefs import loop_tools_active, set_flow_active


class SmartModify(bpy.types.Operator):
    bl_idname = "mesh.smart_modify"
    bl_label = "Smart Modify"
    bl_description = "Context sensitive modification"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_modify(self):
        mode = itools.get_mode()

        if loop_tools_active():
            if mode == 'OBJECT':
                if len(itools.get_selected()) > 0:
                    bpy.ops.wm.call_menu_pie(name="mesh.ssc_duplicate_menu")

                else:
                    if set_flow_active():
                        bpy.ops.wm.call_menu_pie(name="mesh.ssc_new_obj_menu")

            # if Vertex is selected
            elif mode == 'VERT':
                bm = itools.get_bmesh()
                selection = itools.get_selected()
                bpy.ops.mesh.looptools_relax()

            # if Edge is selected
            elif mode == 'EDGE':
                bm = itools.get_bmesh()
                selection = itools.get_selected()

                if mesh.is_border(selection):
                    bpy.ops.mesh.looptools_circle()

                else:
                    if set_flow_active():
                        bpy.ops.mesh.set_edge_flow(tension=180, iterations=1)

            # if Face is selected
            elif mode == 'FACE':
                bpy.ops.mesh.looptools_flatten()

    @classmethod
    def poll(cls, context):
        return loop_tools_active()

    def execute(self, context):
        self.smart_modify()
        return{'FINISHED'}
