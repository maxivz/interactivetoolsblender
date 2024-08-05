import bpy
from bpy_extras.view3d_utils import region_2d_to_location_3d
from mathutils import Vector


def mouse_2d_to_3d(context, event):
    x, y = event.mouse_region_x, event.mouse_region_y
    location = region_2d_to_location_3d(context.region, context.space_data.region_3d, (x, y), (0, 0, 0))
    return Vector(location)

class CSMove(bpy.types.Operator):
    bl_idname = "mesh.cs_move"
    bl_label = "CS Move"
    bl_description = "Context Sensitive Move Tool"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_move(self,context):
        area = bpy.context.area
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            # Make sure active tool is set to select
            context_override = bpy.context.copy()
            context_override["space_data"] = area.spaces[0]
            context_override["area"] = area

            with context.temp_override(**context_override):
                bpy.ops.wm.tool_set_by_id(name="builtin.select_box")

            if space.show_gizmo_object_translate:
                bpy.ops.transform.translate('INVOKE_DEFAULT')
            else:
                space.show_gizmo_object_translate = True
                space.show_gizmo_object_rotate = False
                space.show_gizmo_object_scale = False

    def execute(self, context):
        self.smart_move(context)
        return{'FINISHED'}


class CSRotate(bpy.types.Operator):
    bl_idname = "mesh.cs_rotate"
    bl_label = "CS Rotate"
    bl_description = "Context Sensitive Rotate Tool"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_rotate(self, context):
        
        area = bpy.context.area
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            # Make sure active tool is set to select
            context_override = bpy.context.copy()
            context_override["space_data"] = area.spaces[0]
            context_override["area"] = area

            with context.temp_override(**context_override):
                bpy.ops.wm.tool_set_by_id(name="builtin.select_box")

            if space.show_gizmo_object_rotate:
                bpy.ops.transform.rotate('INVOKE_DEFAULT')
            else:
                space.show_gizmo_object_translate = False
                space.show_gizmo_object_rotate = True
                space.show_gizmo_object_scale = False

    def execute(self, context):
        self.smart_rotate(context)
        return{'FINISHED'}

#TODO: Optimize CSMove, Rotate and Scale into a single class with inheritance
class CSScale(bpy.types.Operator):
    bl_idname = "mesh.cs_scale"
    bl_label = "CS Scale"
    bl_description = "Context Sensitive Scale Tool"
    bl_options = {'REGISTER', 'UNDO'}

    def smart_scale(self, context):
        areas = bpy.context.workspace.screens[0].areas

        area = bpy.context.area
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            # Make sure active tool is set to select
            context_override = bpy.context.copy()
            context_override["space_data"] = area.spaces[0]
            context_override["area"] = area

            with context.temp_override(**context_override):
                bpy.ops.wm.tool_set_by_id(name="builtin.select_box")

            if space.show_gizmo_object_scale:
                bpy.ops.transform.resize('INVOKE_DEFAULT')
            else:
                space.show_gizmo_object_translate = False
                space.show_gizmo_object_rotate = False
                space.show_gizmo_object_scale = True

    def execute(self, context):
        self.smart_scale(context)
        return{'FINISHED'}


class SmartTranslate(bpy.types.Operator):
    bl_idname = "mesh.smart_translate_modal"
    bl_label = "Smart Translate Legacy"
    bl_description = "Smart Translate Tool, Legacy feature use at own risk"
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

        elif event.type == 'MIDDLEMOUSE':  # Confirm
            if event.value == 'RELEASE':
                return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Confirm
            bpy.ops.transform.translate(value=-self.translation_accumulator, orient_type='GLOBAL')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_mouse_pos = mouse_2d_to_3d(context, event)
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
