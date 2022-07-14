import bpy
from ..utils import itools as itools
from ..utils.user_prefs import get_enable_legacy_origin
# Needs optimization pass, possibly merge both into one. Make them proper operators


class QuickPivot(bpy.types.Operator):
    bl_idname = "mesh.quick_pivot"
    bl_label = "Quick Origin"
    bl_description = "Quick Pivot Setup based on selection"
    bl_options = {'REGISTER', 'UNDO'}

    def quick_pivot(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        elif context.mode == 'EDIT_MESH':
            cl = context.scene.cursor.location
            pos2 = (cl[0], cl[1], cl[2])
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.editmode_toggle()
            context.scene.cursor.location = (pos2[0], pos2[1], pos2[2])

    def execute(self, context):
        self.quick_pivot(context)
        return{'FINISHED'}


class QuickEditPivot(bpy.types.Operator):
    bl_idname = "mesh.simple_edit_pivot"
    bl_label = "Edit Origin"
    bl_description = "Edit pivot position and scale"
    bl_options = {'REGISTER', 'UNDO'}

    def create_pivot(self, context, obj):
        bpy.ops.object.empty_add(type='ARROWS', location=obj.location)
        pivot = bpy.context.active_object
        pivot.name = obj.name + ".PivotHelper"
        pivot.location = obj.location
        print("Pivot")

    def get_pivot(self, context, obj):
        pivot = obj.name + ".PivotHelper"
        if bpy.data.objects.get(pivot) is None:
            return False
        else:
            bpy.data.objects[obj.name].select_set(False)
            bpy.data.objects[pivot].select_set(True)
            context.view_layer.objects.active = bpy.data.objects[pivot]
            return True

    def apply_pivot(self, context, pivot):
        obj = bpy.data.objects[pivot.name[:-12]]
        piv_loc = pivot.location
        # I need to create piv as it seem like the pivot location is passed by reference? Still no idea why this happens
        cl = context.scene.cursor.location
        piv = (cl[0], cl[1], cl[2])
        context.scene.cursor.location = piv_loc
        bpy.context.view_layer.objects.active = obj
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        context.scene.cursor.location = (piv[0], piv[1], piv[2])

        # Select pivot, delete it and select obj again
        bpy.data.objects[obj.name].select_set(False)
        bpy.data.objects[pivot.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[obj.name].select_set(True)
        context.view_layer.objects.active = obj

    """
    @classmethod
    def poll(cls, context):
        mode = itools.get_mode()
        return mode not in ['VERT', 'EDGE', 'FACE']
    """

    def execute(self, context):
        version = bpy.app.version_string[:4]

        try:
            version = float(version)
        except ValueError:
            version = float(version[:-1])

        if version >= 2.82 and not get_enable_legacy_origin():
            mode = itools.get_mode()
            if mode in ['VERT', 'EDGE', 'FACE']:
                itools.set_mode('OBJECT')

            if bpy.context.scene.tool_settings.use_transform_data_origin:
                bpy.context.scene.tool_settings.use_transform_data_origin = False
            else:
                bpy.context.scene.tool_settings.use_transform_data_origin = True

        else:
            obj = bpy.context.active_object
            if obj.name.endswith(".PivotHelper"):
                self.apply_pivot(context, obj)
            elif self.get_pivot(context, obj):
                piv = bpy.context.active_object
            else:
                mode = itools.get_mode()
                if mode in ['VERT', 'EDGE', 'FACE']:
                    itools.set_mode('OBJECT')

                self.create_pivot(context, obj)
        return{'FINISHED'}
