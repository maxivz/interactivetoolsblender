import bpy
from ..utils import itools as itools


class TransformModeCycle(bpy.types.Operator):
    bl_idname = "mesh.transform_mode_cycle"
    bl_label = "Transform Mode Cycle"
    bl_description = "Cycle between Move/Rotate/Scale modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        areas = bpy.context.workspace.screens[0].areas

        for area in areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.show_gizmo_object_translate:
                        space.show_gizmo_object_translate = False
                        space.show_gizmo_object_rotate = True

                    elif space.show_gizmo_object_rotate:
                        space.show_gizmo_object_rotate = False
                        space.show_gizmo_object_scale = True

                    elif space.show_gizmo_object_scale:
                        space.show_gizmo_object_scale = False
                        space.show_gizmo_object_translate = True

                    else:
                        space.show_gizmo_object_translate = True

        return{'FINISHED'}


class CSBevel(bpy.types.Operator):
    bl_idname = "mesh.context_sensitive_bevel"
    bl_label = "CS Bevel"
    bl_description = "Context Sensitive Bevels and Inset"
    bl_options = {'REGISTER', 'UNDO'}

    def cs_bevel(self):

        mode = itools.get_mode()

        if mode == 'VERT':
            bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=True)

        if mode == 'EDGE':
            bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=False)

        if mode == 'FACE':
            bpy.ops.mesh.inset('INVOKE_DEFAULT')

    def execute(self, context):
        self.cs_bevel()
        return{'FINISHED'}


class ContextSensitiveSlide(bpy.types.Operator):
    bl_idname = "mesh.context_sensitive_slide"
    bl_label = "Context Sensitive Slide"
    bl_description = "Slide vert or edge based on selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bm = itools.get_bmesh()
        mode = itools.get_mode()

        if mode == 'VERT':
            bpy.ops.transform.vert_slide('INVOKE_DEFAULT')

        elif mode == 'EDGE':
            bpy.ops.transform.edge_slide('INVOKE_DEFAULT')

        return{'FINISHED'}


class TargetWeldToggle(bpy.types.Operator):
    bl_idname = "mesh.target_weld_toggle"
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
    bl_idname = "mesh.modifier_toggle"
    bl_label = "Modifier Toggle"
    bl_description = "Toggles the modifiers on and off for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def modifier_toggle(self, context):
        mode = itools.get_mode()

        if mode in ['VERT', 'EDGE', 'FACE']:
            itools.set_mode('OBJECT')

        selected = itools.get_selected()

        for obj in selected:
            if all(modifier.show_in_editmode and modifier.show_viewport for modifier in obj.modifiers):
                for modifier in obj.modifiers:
                    modifier.show_in_editmode = False
                    modifier.show_viewport = False

            else:
                for modifier in obj.modifiers:
                    modifier.show_in_editmode = True
                    modifier.show_viewport = True

        if mode in ['VERT', 'EDGE', 'FACE']:
            itools.set_mode(mode)

    def execute(self, context):
        self.modifier_toggle(context)
        return {'FINISHED'}


class QuickWireToggle(bpy.types.Operator):
    bl_idname = "mesh.wire_toggle"
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
    bl_idname = "mesh.wire_shaded_toggle"
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
