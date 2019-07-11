import bpy
from .. utils import itools as itools

# Change vertex group implementation for data blocks


class SelectionModeCycle(bpy.types.Operator):
    bl_idname = "mesh.selection_mode_cycle"
    bl_label = "Mesh Mode Cycle"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        if mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        elif mode == 'VERT':
            itools.set_mode('EDGE')
        elif mode == 'EDGE':
            itools.set_mode('FACE')
        elif mode == 'FACE':
            itools.set_mode('VERT')

        return {'FINISHED'}


class QuickSelectionVert(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_vert"
    bl_label = "Quick Selection Vert"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        if mode in ['OBJECT', 'EDGE', 'FACE']:
            itools.set_mode('VERT')

        elif mode == 'VERT':
            itools.set_mode('OBJECT')

        elif mode == 'EDIT_CURVE':
            bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class QuickSelectionVertSticky(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_vert"
    bl_label = "Quick Selection Vert"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.active_object
        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            if context.mode == 'EDIT_MESH':
                itools.set_mode('VERT')

        elif context.mode == 'EDIT_MESH':
            selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
            if selectionMode[0]:
                bpy.ops.object.editmode_toggle()
            else:
                if selectionMode[1]:
                    # Create vertex group to store edge selection
                    selection.vertex_groups.new(name="quicksel_edges")
                    bpy.ops.object.vertex_group_assign()
                elif selectionMode[2]:
                    selection.vertex_groups.new(name="quicksel_faces")
                    bpy.ops.object.vertex_group_assign()
                # Clear Selection
                bpy.ops.mesh.select_all(action='DESELECT')
                # Switch Mode
                bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='VERT')
                # Load Stored Selection if it exists
                vg = selection.vertex_groups.get("quicksel_verts")
                if vg is not None:
                    bpy.ops.object.vertex_group_set_active(group='quicksel_verts')
                    bpy.ops.object.vertex_group_select()
                    # Delete Stored Vertex Group Data
                    selection.vertex_groups.remove(vg)
        elif context.mode == 'EDIT_CURVE':
            bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}


class QuickSelectionEdge(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_edge"
    bl_label = "Quick Selection Edge"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        if mode in ['OBJECT', 'VERT', 'FACE']:
            itools.set_mode('EDGE')

        elif mode == 'EDGE':
            itools.set_mode('OBJECT')

        elif mode == 'EDIT_CURVE':
            bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class QuickSelectionEdgeSticky(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_edge_sticky"
    bl_label = "Quick Selection Edge, stores previous selection"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.active_object
        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            if context.mode == 'EDIT_MESH':
                bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='EDGE')
        elif context.mode == 'EDIT_MESH':
            selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
            if selectionMode[1]:
                bpy.ops.object.editmode_toggle()
            else:
                if selectionMode[0]:
                    # Create vertex group to store edge selection
                    selection.vertex_groups.new(name="quicksel_verts")
                    bpy.ops.object.vertex_group_assign()
                elif selectionMode[2]:
                    selection.vertex_groups.new(name="quicksel_faces")
                    bpy.ops.object.vertex_group_assign()
                # Clear Selection
                bpy.ops.mesh.select_all(action='DESELECT')
                # Switch Mode
                bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='EDGE')
                # Load Stored Selection if it exists
                vg = selection.vertex_groups.get("quicksel_edges")
                if vg is not None:
                    bpy.ops.object.vertex_group_set_active(group='quicksel_edges')
                    bpy.ops.object.vertex_group_select()
                    # Delete Stored Vertex Group Data
                    selection.vertex_groups.remove(vg)
        elif context.mode == 'EDIT_CURVE':
            bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}


class QuickSelectionFace(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_face"
    bl_label = "Quick Selection Face"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        if mode in ['OBJECT', 'VERT', 'EDGE']:
            itools.set_mode('FACE')

        elif mode == 'FACE':
            itools.set_mode('OBJECT')

        elif mode == 'EDIT_CURVE':
            bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class QuickSelectionFaceSticky(bpy.types.Operator):
    bl_idname = "mesh.quick_selection_face_sticky"
    bl_label = "Quick Selection Face Sticky"
    bl_description = "Set selection modes quickly"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selection = bpy.context.active_object
        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            if context.mode == 'EDIT_MESH':
                bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='FACE')
        elif context.mode == 'EDIT_MESH':
            selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
            if selectionMode[2]:
                bpy.ops.object.editmode_toggle()
            else:
                if selectionMode[0]:
                    # Create vertex group to store edge selection
                    selection.vertex_groups.new(name="quicksel_verts")
                    bpy.ops.object.vertex_group_assign()
                elif selectionMode[1]:
                    selection.vertex_groups.new(name="quicksel_edges")
                    bpy.ops.object.vertex_group_assign()
                # Clear Selection
                bpy.ops.mesh.select_all(action='DESELECT')
                # Switch Mode
                bpy.ops.mesh.select_mode('EXEC_DEFAULT', type='FACE')
                # Load Stored Selection if it exists
                vg = selection.vertex_groups.get("quicksel_faces")
                if vg is not None:
                    bpy.ops.object.vertex_group_set_active(group='quicksel_faces')
                    bpy.ops.object.vertex_group_select()
                    # Delete Stored Vertex Group Data
                    selection.vertex_groups.remove(vg)
        elif context.mode == 'EDIT_CURVE':
            bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}
