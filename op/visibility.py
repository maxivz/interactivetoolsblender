import bpy
from ..utils.itools import get_all_collections
class ViewportToRenderVisibility(bpy.types.Operator):
    bl_idname = "object.viewport_to_render_visibility"
    bl_label = "Viewport to Render Visibility"
    bl_description = "Matches collection and viewport visibility to render visibility"
    bl_options = {'REGISTER', 'UNDO'}

    def viewport_to_render_vis(self, context):
        for obj in context.scene.objects:
            obj.hide_render = obj.hide_viewport

        
        collections = get_all_collections()
        if not collections:
            return
        
        for col in collections:
            col.hide_render = col.hide_viewport


    def execute(self, context):
        self.viewport_to_render_vis(context)
        return{'FINISHED'}

#Register Classes
classes = [ViewportToRenderVisibility]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
   
    for cls in reversed(classes):
        unregister_class(cls)
