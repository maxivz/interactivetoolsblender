import bpy
from .. utils import itools as itools
from .. utils import dictionaries as dic

# Change vertex group implementation for data blocks


def store_sel_data(mode):
    if mode == 'VERT':
        dic.write("selected_verts", itools.get_selected(mode, item=False))
    if mode == 'EDGE':
        dic.write("selected_edges", itools.get_selected(mode, item=False))
    if mode == 'FACE':
        dic.write("selected_faces", itools.get_selected(mode, item=False))


def quick_selection(target_mode, sticky=False, safe_mode=False):
    current_mode = itools.get_mode()
    current_object = bpy.context.object
    other_modes = itools.list_difference(['VERT', 'EDGE', 'FACE', 'OBJECT'], [target_mode])

    if current_mode in other_modes and current_object.type != 'CURVE':
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

    elif current_mode == target_mode and current_object.type != 'CURVE':
        if sticky:
            itools.update_indexes()
            store_sel_data(current_mode)
        itools.set_mode('OBJECT')

    elif current_object.type == 'CURVE':
        bpy.ops.object.editmode_toggle()

    elif current_object.type == 'LATTICE':
        bpy.ops.object.editmode_toggle()


class SelectionModeCycle(bpy.types.Operator):
    bl_idname = "mesh.selection_mode_cycle"
    bl_label = "Mesh Mode Cycle"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        print(mode)
        if mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        elif mode == 'VERT':
            itools.set_mode('EDGE')

        elif mode == 'EDGE':
            itools.set_mode('FACE')

        elif mode == 'FACE':
            itools.set_mode('VERT')

        elif mode in ['EDIT_CURVE', 'EDIT_LATTICE']:
            bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class SelectionModeCycleSticky(bpy.types.Operator):
    bl_idname = "mesh.selection_mode_cycle_sticky"
    bl_label = "Mesh Mode Cycle"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        if mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        elif mode == 'VERT':
            quick_selection('EDGE', sticky=True, safe_mode=True)

        elif mode == 'EDGE':
            quick_selection('FACE', sticky=True, safe_mode=True)

        elif mode == 'FACE':
            quick_selection('VERT', sticky=True, safe_mode=True)

        elif mode in ['EDIT_CURVE', 'EDIT_LATTICE']:
            bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class QuickSelectionVert(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_vert"
    bl_label = "Quick Selection Vert"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('VERT')
        return {'FINISHED'}


class QuickSelectionVertSticky(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_vert_sticky"
    bl_label = "Quick Selection Vert Sticky"
    bl_description = "Set selection mode quickly, restores last selection in this mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('VERT', sticky=True, safe_mode=True)
        return {'FINISHED'}


class QuickSelectionEdge(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_edge"
    bl_label = "Quick Selection Edge"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('EDGE')
        return {'FINISHED'}


class QuickSelectionEdgeSticky(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_edge_sticky"
    bl_label = "Quick Selection Edge Sticky"
    bl_description = "Set selection mode quickly, restores last selection in this mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('EDGE', sticky=True, safe_mode=True)
        return {'FINISHED'}


class QuickSelectionFace(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_face"
    bl_label = "Quick Selection Face"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('FACE')
        return {'FINISHED'}


class QuickSelectionFaceSticky(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_face_sticky"
    bl_label = "Quick Selection Face Sticky"
    bl_description = "Set selection mode quickly, restores last selection in this mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        quick_selection('FACE', sticky=True, safe_mode=True)
        return {'FINISHED'}
