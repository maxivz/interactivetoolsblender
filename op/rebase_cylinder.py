import bpy
from .. utils import itools as itools


class RebaseCylinder(bpy.types.Operator):
    bl_idname = "mesh.rebase_cylinder"
    bl_label = "Rebase Cylinder"
    bl_description = "Reconstruct cylinder with a different number of sides"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.active_object

        if bpy.context.object.modifiers.find("Cylindrical Sides") > -1:
            bpy.ops.wm.context_modal_mouse('INVOKE_DEFAULT',
                                           data_path_iter='selected_editable_objects',
                                           data_path_item='modifiers["Cylindrical Sides"].steps',
                                           input_scale=0.10000000149011612,
                                           header_text='Number of Sides %.f')

        elif bpy.context.mode == 'EDIT_MESH':
            bpy.ops.mesh.separate(type='SELECTED')
            new_selection = bpy.context.selected_objects
            mesh_to_select = list(filter(lambda x: x.name != selection.name, new_selection))
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[mesh_to_select[0].name].select_set(state=True)
            bpy.context.view_layer.objects.active = mesh_to_select[0]

            bpy.ops.object.modifier_add(type='SCREW')
            bpy.context.object.modifiers["Screw"].name = "Cylindrical Sides"
            bpy.context.object.modifiers["Cylindrical Sides"].use_merge_vertices = True
            bpy.context.object.modifiers["Cylindrical Sides"].use_normal_calculate = True
            bpy.ops.wm.context_modal_mouse('INVOKE_DEFAULT', data_path_iter='selected_editable_objects',
                                           data_path_item='modifiers["Cylindrical Sides"].steps',
                                           input_scale=0.10000000149011612, header_text='Number of Sides %.f')
        return {'FINISHED'}
