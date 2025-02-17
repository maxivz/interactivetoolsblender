import bpy
import bmesh
from mathutils import Vector



def fit_to_view_scale_handlers(scene):
    """Handler that triggers fit to view on new object creation"""

    pass


def load_handlers():
    bpy.app.handlers.depsgraph_update_post.append(fit_to_view_scale_handlers)
    pass

def unload_handlers():
    bpy.app.handlers.depsgraph_update_post.remove(fit_to_view_scale_handlers)

