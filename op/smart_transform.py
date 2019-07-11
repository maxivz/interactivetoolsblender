import bpy
from bpy_extras.view3d_utils import region_2d_to_location_3d
from mathutils import Vector


def mouse_2d_to_3d(context, event):
    x, y = event.mouse_region_x, event.mouse_region_y
    location = region_2d_to_location_3d(context.region, context.space_data.region_3d, (x, y), (0, 0, 0))
    return Vector(location)


class SmartTranslate(bpy.types.Operator):
    bl_idname = "mesh.smart_translate_modal"
    bl_label = "Smart Translate"
    bl_description = "Smart Translate Tool"
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


class SmartRotate(bpy.types.Operator):
    bl_idname = "mesh.smart_rotate_modal"
    bl_label = "Smart Rotate"
    bl_description = "Smart Rotation Tool"
    bl_options = {'REGISTER', 'UNDO'}

    initial_mouse_pos = Vector((0, 0, 0))
    translation_accumulator = Vector((0, 0, 0))
    initial_pos = Vector((0, 0, 0))
    sensitivity = 1

    def calculate_rotation(self, context, event):
        translation = Vector((0, 0, 0))
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                new_mouse_pos = mouse_2d_to_3d(context, event)

            else:
                new_mouse_pos = self.initial_mouse_pos

        increment = (new_mouse_pos - self.initial_mouse_pos) * self.sensitivity * 0.1
        increment_abs = [abs(value) for value in increment]
        axis = list(increment_abs).index(max(increment_abs))

        if axis == 0:
            translation[0] = increment[0] - self.translation_accumulator[0]
            translation[1] = -self.translation_accumulator[1]
            translation[2] = -self.translation_accumulator[2]
            rot_axis = 'Y'
            translation_axis = increment[0] - self.translation_accumulator[0] * -1

        elif axis == 1:
            translation[0] = -self.translation_accumulator[0]
            translation[1] = increment[1] - self.translation_accumulator[1]
            translation[2] = -self.translation_accumulator[2]
            rot_axis = 'Z'
            translation_axis = increment[1] - self.translation_accumulator[1] 

        elif axis == 2:
            translation[0] = -self.translation_accumulator[0]
            translation[1] = -self.translation_accumulator[1]
            translation[2] = increment[2] - self.translation_accumulator[2]
            rot_axis = 'X'
            translation_axis = increment[2] - self.translation_accumulator[2]

        self.translation_accumulator += translation
        bpy.ops.transform.rotate(value=translation[0], orient_axis='X', orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=translation[1], orient_axis='Z', orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=translation[2], orient_axis='Y', orient_type='GLOBAL')
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
            self.calculate_rotation(context, event)
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


class SmartScale(bpy.types.Operator):
    bl_idname = "mesh.smart_scale_modal"
    bl_label = "Smart Scale"
    bl_description = "Smart Scale Tool"
    bl_options = {'REGISTER', 'UNDO'}

    initial_mouse_pos = Vector((0, 0, 0))
    new_mouse_pos = Vector((0, 0, 0))
    scale_accumulator = Vector((0, 0, 0))
    initial_pos = Vector((0, 0, 0))
    sensitivity = 1

    def update_mouse_pos(self, context, event):
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                self.new_mouse_pos = mouse_2d_to_3d(context, event)

            else:
                self.new_mouse_pos = self.initial_mouse_pos

    def calculate_scale(self, context):
        translation = Vector((0, 0, 0))
        increment = (self.new_mouse_pos - self.initial_mouse_pos) * self.sensitivity
        increment_abs = [abs(value) for value in increment]
        axis = list(increment_abs).index(max(increment_abs))

        if axis == 0:
            translation[0] = increment[0] - self.scale_accumulator[0]
            translation[1] = -self.scale_accumulator[1]
            translation[2] = -self.scale_accumulator[2]

        elif axis == 1:
            translation[0] = -self.scale_accumulator[0]
            translation[1] = increment[1] - self.scale_accumulator[1]
            translation[2] = -self.scale_accumulator[2]

        elif axis == 2:
            translation[0] = -self.scale_accumulator[0]
            translation[1] = -self.scale_accumulator[1]
            translation[2] = increment[2] - self.scale_accumulator[2]

        self.scale_accumulator += translation
        bpy.ops.transform.resize(value=Vector((1.0, 1.0, 1.0)) + translation, orient_type='GLOBAL')
        return True

    def __init__(self):
        self.initial_mouse_pos = Vector((0, 0, 0))
        self.scale_accumulator = Vector((0, 0, 0))
        self.initial_pos = Vector((0, 0, 0))
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        self.calculate_scale(context)
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.update_mouse_pos(context, event)
            self.execute(context)

        elif event.type == 'MIDDLEMOUSE':  # Confirm
            if event.value == 'RELEASE':
                return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Confirm
            bpy.ops.transform.resize(value=Vector((1.0, 1.0, 1.0)) - self.scale_accumulator, orient_type='GLOBAL')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_mouse_pos = mouse_2d_to_3d(context, event)
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}