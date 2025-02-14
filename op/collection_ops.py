import bpy

class RenameObjsByCollection(bpy.types.Operator):
    bl_idname = "collection.rename_objs_by_collection"
    bl_label = "Rename Objects By Collection"
    bl_description = "Renames all objects in collection to reflect the collection name"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_col = bpy.context.collection
        for obj_num, obj in enumerate(active_col.objects):
            obj.name = f"{active_col.name}_{obj_num}"
        return {'FINISHED'}