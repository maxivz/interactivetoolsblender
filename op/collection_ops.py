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
    

class EditCollectionOffset(bpy.types.Operator):
    bl_idname = "collection.edit_collection_offset_toggle"
    bl_label = "Edit Collection Offset"
    bl_description = "Spawns a locator to edit the offset of the collection"
    bl_options = {'REGISTER', 'UNDO'}

    def edit_collection_offset_toggle(self, collection, context):
        locator_name = collection.name + "_origin"
        locator = bpy.data.objects.get(locator_name)
        
        if not locator:
            if collection.objects:
                locator = bpy.data.objects.new(locator_name, None)
                locator.empty_display_type = 'ARROWS'
                
                collection.objects.link(locator)
                locator.select_set(True)
                locator.location = collection.instance_offset
                context.view_layer.objects.active = locator

        else:
            # Set the collection offset to the locator location and delete it
            collection.instance_offset = locator.location
            bpy.data.objects.remove(locator)
            

    def execute(self, context):
        active_col = bpy.context.collection
        self.edit_collection_offset_toggle(active_col, context)
        return {'FINISHED'}
    

