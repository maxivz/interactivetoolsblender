import bpy
from bpy_extras.view3d_utils import region_2d_to_location_3d
from ..utils import itools as itools
from ..utils.mesh import is_border_edge
from .smart_transform import mouse_2d_to_3d
from mathutils import Vector


class SmartExtrudeModal(bpy.types.Operator):
    bl_idname = "mesh.smart_extrude_modal"
    bl_label = "Smart Extrude Legacy"
    bl_description = "Context Sensitive Extrude operation, Legacy feature use at own risk"
    bl_options = {'REGISTER', 'UNDO'}

    initial_mouse_pos = Vector((0, 0, 0))
    translation_accumulator = Vector((0, 0, 0))
    initial_pos = Vector((0, 0, 0))
    sensitivity = 1

    def calculate_translation(self, context, event):
        translation = Vector((0, 0, 0))
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                new_mouse_pos = mouse_2d_to_3d(context, event)

            else:
                new_mouse_pos = self.initial_mouse_pos

        increment = (new_mouse_pos - self.initial_mouse_pos) * self.sensitivity
        increment_abs = [abs(value) for value in increment]
        axis = list(increment_abs).index(max(increment_abs))

        if axis == 0:
            translation[0] = increment[0] - self.translation_accumulator[0]
            translation[1] = -self.translation_accumulator[1]
            translation[2] = -self.translation_accumulator[2]

        elif axis == 1:
            translation[0] = -self.translation_accumulator[0]
            translation[1] = increment[1] - self.translation_accumulator[1]
            translation[2] = -self.translation_accumulator[2]

        elif axis == 2:
            translation[0] = -self.translation_accumulator[0]
            translation[1] = -self.translation_accumulator[1]
            translation[2] = increment[2] - self.translation_accumulator[2]

        self.translation_accumulator += translation
        bpy.ops.transform.translate(value=translation, orient_type='GLOBAL')
        return True

    def context_sensitive_extend(self, context):
        if context.mode == 'OBJECT':
            if len(context.selected_objects) > 0:
                initial_pos = context.selected_objects[0].location
                bpy.ops.object.duplicate()
            else:
                return {'FINISHED'}

        elif context.mode == 'EDIT_MESH':
            bm = itools.get_bmesh()
            mode = itools.get_mode()
            if mode == 'EDGE':
                selection = itools.get_selected('EDGE', item=True)
                if all(is_border_edge(edge) for edge in selection):
                    bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv=None, TRANSFORM_OT_translate=None)
                else:
                    return {'FINISHED'}
            else:
                bpy.ops.mesh.duplicate(mode=1)
        elif context.mode == 'EDIT_CURVE':
            bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode": 'TRANSLATION'},
                                       TRANSFORM_OT_translate={"value": (0, 0, 0)})

    def __init__(self):
        self.initial_mouse_pos = Vector((0, 0, 0))
        self.translation_accumulator = Vector((0, 0, 0))
        self.initial_pos = Vector((0, 0, 0))
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.calculate_translation(context, event)
            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            if event.value == 'RELEASE':
                return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Confirm
            bpy.ops.transform.translate(value=(Vector((0, 0, 0)) - self.translation_accumulator),
                                        orient_type='GLOBAL')
            SmartDelete.smart_delete(context)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_mouse_pos = mouse_2d_to_3d(context, event)
        self.context_sensitive_extend(context)
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SmartExtrude(bpy.types.Operator):
    bl_idname = "mesh.smart_extrude"
    bl_label = "Smart Extrude"
    bl_description = "Context Sensitive Extrude operation"
    bl_options = {'REGISTER', 'UNDO'}

    def context_sensitive_extrude(self, context):
        if context.mode == 'OBJECT':
            if len(context.selected_objects) > 0:
                initial_pos = context.selected_objects[0].location
                bpy.ops.object.duplicate()

        elif context.mode == 'EDIT_MESH':
            bm = itools.get_bmesh()
            mode = itools.get_mode()
            if mode == 'EDGE':
                selection = itools.get_selected('EDGE', item=True)
                if all(is_border_edge(edge) for edge in selection):
                    bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv=None, TRANSFORM_OT_translate=None)
                else:
                    return {'FINISHED'}
            else:
                bpy.ops.mesh.duplicate(mode=1)
        elif context.mode == 'EDIT_CURVE':
            bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode": 'TRANSLATION'},
                                       TRANSFORM_OT_translate={"value": (0, 0, 0)})


        active_tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode, create=False).idname
        areas = bpy.context.workspace.screens[0].areas

        for area in areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.show_gizmo_object_translate or active_tool == 'builtin.move':
                        bpy.ops.transform.translate('INVOKE_DEFAULT')

                    elif space.show_gizmo_object_rotate or active_tool == 'builtin.rotate':
                        bpy.ops.transform.rotate('INVOKE_DEFAULT')

                    elif space.show_gizmo_object_scale or active_tool == 'builtin.scale':
                        bpy.ops.transform.resize('INVOKE_DEFAULT')

    def execute(self, context):
        self.context_sensitive_extrude(context)
        return {'FINISHED'}
