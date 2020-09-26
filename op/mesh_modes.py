import bpy
from .. utils import itools as itools
from .. utils import dictionaries as dic
from ..utils.user_prefs import get_enable_sticky_selection  


def store_sel_data(mode):
    if mode == 'VERT':
        dic.write("selected_verts", itools.get_selected(mode, item=False))
    if mode == 'EDGE':
        dic.write("selected_edges", itools.get_selected(mode, item=False))
    if mode == 'FACE':
        dic.write("selected_faces", itools.get_selected(mode, item=False))


def quick_selection(target_mode, safe_mode=False):
    current_mode = itools.get_mode()
    current_object = bpy.context.object

    if current_object != None:

        #Convert types from Mesh to Gpencil space
        if current_object.type == 'GPENCIL':
            if target_mode == 'VERT':
                target_mode = 'POINT'
            elif target_mode == 'EDGE':
                target_mode = 'STROKE'
            elif target_mode == 'FACE':  
                target_mode = 'SEGMENT'

        other_modes = itools.list_difference(['VERT', 'EDGE', 'FACE', 'POINT', 'STROKE', 'SEGMENT', 'OBJECT'], [target_mode])
        sticky = get_enable_sticky_selection()

        if current_mode in other_modes and current_object.type == 'MESH':
            if current_mode != 'OBJECT' and sticky:
                itools.update_indexes()
                store_sel_data(current_mode)

            itools.set_mode(target_mode)

            if sticky:
                if target_mode == 'VERT':
                    stored_selection = dic.read("selected_verts")

                elif target_mode == 'EDGE':
                    stored_selection = dic.read("selected_edges")

                elif target_mode == 'FACE':
                    stored_selection = dic.read("selected_faces")

                if len(stored_selection) > 0 and "itools" in bpy.context.object:
                    itools.update_indexes()
                    indexes = [index for index in stored_selection]
                    if safe_mode:
                        itools.select(indexes, item=False, replace=True, safe_mode=safe_mode)
                    else:
                        itools.select(indexes, item=False, replace=True)

        elif current_mode == target_mode and current_object.type == 'MESH':
            if sticky:
                itools.update_indexes()
                store_sel_data(current_mode)
            itools.set_mode('OBJECT')

        if current_object.type == 'GPENCIL':
            bpy.ops.object.mode_set(mode="EDIT_GPENCIL")

            if current_mode in other_modes:
                if target_mode == 'POINT':
                    bpy.context.scene.tool_settings.gpencil_selectmode_edit = 'POINT'
                elif target_mode == 'STROKE':
                    bpy.context.scene.tool_settings.gpencil_selectmode_edit = 'STROKE'
                elif target_mode == 'SEGMENT':
                    bpy.context.scene.tool_settings.gpencil_selectmode_edit = 'SEGMENT'

            elif current_mode == target_mode:
                bpy.ops.object.mode_set(mode="OBJECT")



class SelectionModeCycle(bpy.types.Operator):
    bl_idname = "mesh.selection_mode_cycle"
    bl_label = "Selection Mode Cycle"
    bl_description = "Cycles trough selection modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        print(mode)
        if mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        elif mode == 'VERT':
            quick_selection('EDGE', safe_mode=True)

        elif mode == 'EDGE':
            quick_selection('FACE', safe_mode=True)

        elif mode == 'FACE':
            quick_selection('VERT', safe_mode=True)

        elif mode in ['EDIT_CURVE', 'EDIT_LATTICE']:
            bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class QuickSelectionVert(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_vert"
    bl_label = "Quick Selection Vert"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('VERT', safe_mode=True)
        return {'FINISHED'}


class QuickSelectionEdge(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_edge"
    bl_label = "Quick Selection Edge"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('EDGE', safe_mode=True)
        return {'FINISHED'}


class QuickSelectionFace(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_face"
    bl_label = "Quick Selection Face"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('FACE', safe_mode=True)
        return {'FINISHED'}
