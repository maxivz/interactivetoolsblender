import bpy
import random

from .. utils.itools import get_collection_top_level_parent

COLLECTION_COLOR = "Collection Color"

#TODO: Make this into an option for the tool
# Option to use the parent collection's color if it exists
USE_PARENT_COLLECTION_COLOR = False 

def get_collection_color(collection):
    """Returns the color of a collection, if it has a tag it uses that one, if it doesnt it assigns one"""
    if collection is None:
        return (1, 1, 1, 1) 
    
    if USE_PARENT_COLLECTION_COLOR:
        parent_collection = get_collection_top_level_parent(collection)
        if parent_collection: 
            return get_collection_color(parent_collection)
        

    if collection.color_tag != 'NONE':
        color_map = {
            'COLOR_01': (1.0, 0.0, 0.0, 1.0),
            'COLOR_02': (1.0, 0.7, 0.4, 1.0),
            'COLOR_03': (1.0, 0.95, 0.5, 1.0),
            'COLOR_04': (0.48, 0.8, 0.48, 1.0),
            'COLOR_05': (0.36, 0.71, 0.91, 1.0),
            'COLOR_06': (0.55, 0.35, 0.85, 1.0),
            'COLOR_07': (0.77, 0.45, 0.72, 1.0),
            'COLOR_08': (0.47, 0.33, 0.25, 1.0),
        }
        
        return color_map.get(collection.color_tag, 1)


    if not collection.get(COLLECTION_COLOR):
        collection[COLLECTION_COLOR] = (random.random(), random.random(), random.random(), 1)

    return collection[COLLECTION_COLOR]

def assign_object_collection_colors():
    """Assigns viewport display colors to objects based on their collections."""
    for obj in bpy.data.objects:
        if obj.type not in {'MESH', 'CURVE'}:
            continue  

        collection = next((col for col in bpy.data.collections if obj.name in col.objects), None)
        
        if collection:
            color = get_collection_color(collection)
            obj.color = color

class ColorObjsByCollection(bpy.types.Operator):
    bl_idname = "collection.color_objs_by_collection"
    bl_label = "Color Objects By Collection"
    bl_description = "Renames all objects in collection to reflect the collection name"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        assign_object_collection_colors()
        return {'FINISHED'}


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
    