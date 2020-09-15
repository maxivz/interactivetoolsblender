import bpy
from ..utils import itools as itools
from ..utils import mesh as mesh
from ..utils.user_prefs import get_enable_dissolve_faces, get_enable_dissolve_verts


class SmartDelete(bpy.types.Operator):
    bl_idname = "mesh.smart_delete"
    bl_label = "Smart Delete"
    bl_description = "Context Sensitive Deletion"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_delete(cls, context):
        mode = itools.get_mode()

        if mode == 'OBJECT':
            bpy.ops.object.delete()

        elif mode in ['VERT', 'EDGE', 'FACE']:
            bm = itools.get_bmesh()

            if mode == 'VERT':
                selection = itools.get_selected()
                verts_connectivity2 = [vert for vert in selection if len([edge for edge in vert.link_edges]) == 2]

                if len(verts_connectivity2) == len(selection):
                    bpy.ops.mesh.dissolve_verts()

                else:
                    if get_enable_dissolve_verts():
                        bpy.ops.mesh.dissolve_verts()
                    else:
                        bpy.ops.mesh.delete(type='VERT')

            elif mode == 'EDGE':
                selection = itools.get_selected()
                if get_enable_dissolve_faces():
                    if mesh.is_border(selection):
                        for edge in selection:
                            for face in edge.link_faces:
                                face.select = 1
                        bpy.ops.mesh.delete(type='FACE')

                    else:
                        bpy.ops.mesh.dissolve_edges()

                else:
                    for edge in selection:
                            for face in edge.link_faces:
                                face.select = 1
                            bpy.ops.mesh.delete(type='FACE')

            elif mode == 'FACE':
                bpy.ops.mesh.delete(type='FACE')

        elif mode == 'EDIT_CURVE':
            bpy.ops.curve.delete(type='VERT')

        return{'FINISHED'}

    def execute(self, context):
        self.smart_delete(context)
        return {'FINISHED'}
