import bpy
import bmesh
from ..utils.materials import get_material
from ..utils.user_prefs import get_quickconvex_prefix
from ..utils.constants import CONVEXHULL_MAT_COLOR


class QuickConvexHull(bpy.types.Operator):
    bl_idname = "mesh.quick_convex_hull"
    bl_label = "Quick Convex Hull"
    bl_description = "Makes a quick convex hull from selection, parents it to selected object and adds the desired prefix"
    bl_options = {'REGISTER', 'UNDO'}

    def assign_collision_mat(self, obj):
        # Get collision material and assign green color, create it if its missing
        get_material("Collision")
        mat = bpy.data.materials.get("Collision")
        mat.diffuse_color = CONVEXHULL_MAT_COLOR
        obj.data.materials.append(mat)

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        edit_mode = False
        hull_prefix = get_quickconvex_prefix()
        og_selection = context.selected_objects
        og_active = context.view_layer.objects.active

        for obj in og_selection:
            if og_active.mode == 'EDIT':
                edit_mode = True
                bpy.ops.object.mode_set(mode="OBJECT")

                
            depsgraph = bpy.context.evaluated_depsgraph_get()
            bm = bmesh.new()
            bm.from_object(obj, depsgraph)

            selected_verts = []

            if edit_mode:
                selected_verts = [v for v in bm.verts if v.select]

            else:
                selected_verts = [v for v in bm.verts]
                
            if not selected_verts:
                print("ERROR: No elements selected, please make a selection")
                return {'FINISHED'}

            
            op_data = bmesh.ops.convex_hull(bm, input=selected_verts, use_existing_faces=True)
            delete_verts = [v for v in bm.verts if v not in selected_verts]
            delete_verts += op_data["geom_interior"] + op_data["geom_unused"]  
            
            if delete_verts:
                bmesh.ops.delete(bm, geom=delete_verts)

            # Finish up, write the bmesh into a new mesh
            new_bmesh = bpy.data.meshes.new(f"{hull_prefix}_{og_selection[0].name}")
            bm.to_mesh(new_bmesh)
            bm.free()

            convex_hull = bpy.data.objects.new(f"{hull_prefix}_{og_selection[0].name}", new_bmesh)
            bpy.context.collection.objects.link(convex_hull)
                # Parent the convex hull to the original object and copy transforms
            convex_hull.parent = obj

            self.assign_collision_mat(convex_hull)

            if edit_mode:
                bpy.ops.object.mode_set(mode="EDIT")

        return {'FINISHED'}