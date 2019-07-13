import bpy
import bmesh
from ..utils import itools as itools


def selected_uv_verts_pos():
    bm = get_bmesh()
    uv_layer = bm.loops.layers.uv.verify()
    verts_loc = [loop[uv_layer].uv for face in bm.faces for loop in face.loops if loop[uv_layer].select]
    return verts_loc


def sharp_to_seams(context):
    mode = itools.get_mode()
    me = context.object.data
    if mode == 'OBJECT':
        itools.set_mode('EDGE')

    if mode in ['VERT', 'EDGE', 'FACE']:
        bm = itools.get_bmesh()
        for edge in bm.edges:
            edge.seam = False

        for edge in bm.edges:
            if not edge.smooth:
                edge.seam = True

        itools.set_mode('OBJECT')
        itools.set_mode(mode)


class QuickRotateUv90Pos(bpy.types.Operator):
    bl_idname = "uv.rotate_90_pos"
    bl_label = "Rotate UV 90 Pos"
    bl_description = "Rotate Uvs +90 degrees"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        original_pos = selected_uv_verts_pos()
        print(original_pos)
        bpy.ops.transform.rotate(value=math.radians(90), orient_axis='Z')
        new_pos = selected_uv_verts_pos()
        return{'FINISHED'}


class QuickRotateUv90Neg(bpy.types.Operator):
    bl_idname = "uv.rotate_90_neg"
    bl_label = "Rotate Uvs -90 degrees"
    bl_description = "Rotate Uvs -90 degrees"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='Z')
        return{'FINISHED'}


class SeamsFromSharps(bpy.types.Operator):
    bl_idname = "uv.seams_from_sharps"
    bl_label = "Convets hard edges to seams"
    bl_description = "Convets hard edges to seams"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sharp_to_seams(context)
        return{'FINISHED'}


class UvsFromSharps(bpy.types.Operator):
    bl_idname = "uv.uvs_from_sharps"
    bl_label = "Convets hard edges to uv seams and unwraps the model"
    bl_description = "Convets hard edges to seams and unwraps the model"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        itools.set_mode('FACE')
        sharp_to_seams(context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.02)
        return{'FINISHED'}
