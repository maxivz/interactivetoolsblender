import bpy
from .. utils import itools as itools
from .. utils import mesh as mesh
from .. utils import user_prefs as up
from .. utils import dictionaries as dic
from .. op.super_smart_create import SuperSmartCreate
from .. op import selection as sel


class MaxivzToolsDebug_PT_Panel(bpy.types.Panel):
    bl_idname = "MaxivzToolsDebug_PT_Panel"
    bl_label = "Debug"
    bl_category = "Maxivz Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        row0.operator('itools.debug', text="Debug")


class DebugOp(bpy.types.Operator):
    bl_idname = "itools.debug"
    bl_label = "Debug"
    bl_description = "Debug Button"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prop = up.get_keymaps_by_key()
        print("Preference Settings : ", prop)
        return {'FINISHED'}


class DebugOpModal(bpy.types.Operator):
    bl_idname = "itools.debug_modal"
    bl_label = "Debug Modal"
    bl_description = "Debug Button Modal"
    bl_options = {'REGISTER', 'UNDO'}

    mode = 0

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        context.object.location.x = self.value / 100.0
        return {'FINISHED'}

    def modal(self, context, event):
        value = get_property("activate_debug")
        if value:
            print("Option Active")
        else:
            print("Option Not Active")
        return {'FINISHED'}
        if event.type == 'MOUSEMOVE':  # Apply
            self.value = event.mouse_x
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            context.object.location.x = self.init_loc_x
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        return {'RUNNING_MODAL'}
