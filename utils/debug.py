import bpy
from .. utils import itools as itools
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
        print("Debug")
        return {'FINISHED'}
