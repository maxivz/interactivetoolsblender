import bpy
from ..utils import itools as itools


class CSBevel(bpy.types.Operator):
    bl_idname = "itools.context_sensitive_bevel"
    bl_label = "CS Bevel"
    bl_description = "Context Sensitive Bevels and Inset"
    bl_options = {'REGISTER', 'UNDO'}

    def cs_bevel(self):

        context = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))

        if context == 'VERT':
            bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=True) 

        if context == 'EDGE':
            bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=False)  

        if context == 'FACE':
            bpy.ops.mesh.inset('INVOKE_DEFAULT')

    def execute(self, context):
        self.cs_bevel()
        return{'FINISHED'}


class ContextSensitiveSlide(bpy.types.Operator):
    bl_idname = "itools.context_sensitive_slide"
    bl_label = "Context Sensitive Slide"
    bl_description = "Slide vert or edge based on selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bm = get_bmesh()
        context = itools.get_mode()

        if context == 'VERT':
            bpy.ops.transform.vert_slide('INVOKE_DEFAULT')

        elif context == 'EDGE':
            bpy.ops.transform.edge_slide('INVOKE_DEFAULT')

        return{'FINISHED'}


class TargetWeldToggle(bpy.types.Operator):
    bl_idname = "itools.target_weld_toggle"
    bl_label = "Target Weld Toggle"
    bl_description = "Toggles snap to vertex and automerge editing on and off"
    bl_options = {'REGISTER', 'UNDO'}

    def toggle_target_weld(self, context):
        if context.scene.tool_settings.use_mesh_automerge and bpy.context.scene.tool_settings.use_snap:
            context.scene.tool_settings.use_mesh_automerge = False
            bpy.context.scene.tool_settings.use_snap = False
        else:
            context.scene.tool_settings.snap_elements |= {'VERTEX'}
            context.scene.tool_settings.use_mesh_automerge = True
            bpy.context.scene.tool_settings.use_snap = True

    def execute(self, context):
        self.toggle_target_weld(context)
        return{'FINISHED'}


class QuickModifierToggle(bpy.types.Operator):
    bl_idname = "itools.modifier_toggle"
    bl_label = "Modifier Toggle"
    bl_description = "Toggles the modifiers on and off for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def modifier_toggle(self, context):
        for obj in context.selected_objects:
            if all(modifier.show_in_editmode and modifier.show_viewport for modifier in obj.modifiers):
                for modifier in obj.modifiers:
                    modifier.show_in_editmode = False
                    modifier.show_viewport = False
            else:
                for modifier in obj.modifiers:
                    modifier.show_in_editmode = True
                    modifier.show_viewport = True

    def execute(self, context):
        self.modifier_toggle(context)
        return {'FINISHED'}


class QuickWireToggle(bpy.types.Operator):
    bl_idname = "itools.wire_toggle"
    bl_label = "Quick Wire Toggle"
    bl_description = "Toggles wire mode on and off on all objects"
    bl_options = {'REGISTER', 'UNDO'}

    def wire_toggle(self, context):
        if context.space_data.overlay.show_wireframes:
            context.space_data.overlay.show_wireframes = False
        else:
            context.space_data.overlay.show_wireframes = True

    def execute(self, context):
        self.wire_toggle(context)
        return{'FINISHED'}


class WireShadedToggle(bpy.types.Operator):
    bl_idname = "itools.wire_shaded_toggle"
    bl_label = "Wireframe / Shaded Toggle"
    bl_description = "Toggles between wireframe and shaded mode"
    bl_options = {'REGISTER', 'UNDO'}

    def wire_shaded_toggle(self, context):
        areas = context.workspace.screens[0].areas
        for area in areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.shading.type == 'WIREFRAME':
                        space.shading.type = 'SOLID'
                    else:
                        space.shading.type = 'WIREFRAME'

    def execute(self, context):
        self.wire_shaded_toggle(context)
        return{'FINISHED'}
