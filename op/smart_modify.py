import bpy
from ..utils import itools as itools
from ..utils import mesh as mesh
from ..utils.user_prefs import get_loop_tools_active, get_set_flow_active


class SmartModify(bpy.types.Operator):
    bl_idname = "mesh.smart_modify"
    bl_label = "Smart Modify"
    bl_description = "Context sensitive modification"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_modify(self):
        mode = itools.get_mode()

        if get_loop_tools_active():
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
                    if get_set_flow_active():
                        bpy.ops.mesh.set_edge_flow(tension=180, iterations=1)
                    else:
                        bpy.ops.mesh.looptools_space(influence=100, input='selected', interpolation='cubic', lock_x=False, lock_y=False, lock_z=False)


            # if Face is selected
            elif mode == 'FACE':
                bpy.ops.mesh.looptools_flatten()

    @classmethod
    def poll(cls, context):
        return get_loop_tools_active()

    def execute(self, context):
        self.smart_modify()
        return{'FINISHED'}
