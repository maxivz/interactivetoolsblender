import bpy
import bmesh
from ..utils.materials import get_material
from ..utils.user_prefs import get_quickconvex_prefix
from ..utils.constants import CONVEXHULL_MAT_COLOR, COLLISION_PREFIXES, COLLISION, DESCRIPTION_DIC, COLLISION_COLLECTION_UPDATE

def get_collision_collection():
    """Returns collision collection, if it doesnt exist it creates it and returns it"""
    if COLLISION in bpy.data.collections:
        return bpy.data.collections[COLLISION]
    
    col = bpy.data.collections.new(COLLISION)
    col.color_tag = "COLOR_04"
    bpy.context.scene.collection.children.link(col)
    return col

def update_global_collision_collection():
    """Adds collision objs into global collision collection"""
    collision_col = get_collision_collection()

    for obj in bpy.context.scene.objects:
        if not obj.name.startswith(tuple(COLLISION_PREFIXES)):
            continue
        
        
        if obj.name in collision_col.objects:
            continue

        collision_col.objects.link(obj)
    
    #Remove objs from collision colection that no longer posses a proper prefix
    for obj in list(collision_col.objects):
        if obj.name.startswith(tuple(COLLISION_PREFIXES)):
            continue

        collision_col.objects.unlink(obj)
        collection_count = sum(1 for col in bpy.data.collections if obj.name in col.objects)

        #If its in no other collection link it to the parent scene so obj is not lost
        if collection_count > 0:
            bpy.context.scene.objects.link(obj)



class CollisionCollectionUpdate(bpy.types.Operator):
    bl_idname = "itools.collision_collection_update"
    bl_label = "Collision Collection Update"
    bl_description = DESCRIPTION_DIC[COLLISION_COLLECTION_UPDATE]
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update_global_collision_collection()
        return {'FINISHED'}

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
            convex_hull.parent = obj

            for col in og_active.users_collection:
                if convex_hull.name not in col.objects:
                    col.objects.link(convex_hull)

            self.assign_collision_mat(convex_hull)

            if edit_mode:
                bpy.ops.object.mode_set(mode="EDIT")

        return {'FINISHED'}