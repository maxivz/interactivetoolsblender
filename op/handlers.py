import bpy
from ..utils.constants import COLLISION_COLORS_UPDATE, COLLISION_COLLECTION_UPDATE
from ..utils.custom_data import itools_data_get
from .collection_ops import collection_colors_assign_to_objects
from .collision_ops import update_global_collision_collection

def update_collection_colors(scene):
    if itools_data_get(COLLISION_COLORS_UPDATE):
        collection_colors_assign_to_objects()

def update_collision_collection(scene):
    if itools_data_get(COLLISION_COLLECTION_UPDATE):
        update_global_collision_collection()


def register():
    bpy.app.handlers.depsgraph_update_post.append(update_collection_colors)
    bpy.app.handlers.depsgraph_update_post.append(update_collision_collection)
    print("Itools: Loading Handlers")


def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(update_collection_colors)
    bpy.app.handlers.depsgraph_update_post.remove(update_collision_collection)
    print("Itools: Unloading Handlers")
