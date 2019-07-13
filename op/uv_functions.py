import bpy


def selected_uv_verts_pos():
    bm = get_bmesh()
    uv_layer = bm.loops.layers.uv.verify()
    verts_loc = [loop[uv_layer].uv for face in bm.faces for loop in face.loops if loop[uv_layer].select]
    return verts_loc


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
    bl_description = "Edit pivot position and scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='Z')
        return{'FINISHED'}
