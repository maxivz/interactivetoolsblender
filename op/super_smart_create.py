import bpy
import bmesh
import mesh_f2
from ..utils import itools as itools
from ..utils import mesh as mesh


class SuperSmartCreate(bpy.types.Operator):
    bl_idname = "mesh.super_smart_create"
    bl_label = "Super Smart Create"
    bl_description = "Context sensitive creation"
    bl_options = {'REGISTER', 'UNDO'}

    def split_edge_select_vert(self):

        bpy.ops.mesh.subdivide()
        itools.update_indexes('ALL')

        selection = itools.get_selected()
        new_selection = [vert for edge in selection for vert in edge.verts
                         if all(edge in selection for edge in vert.link_edges)]
        new_selection = itools.remove_duplicates(new_selection)

        itools.set_mode('VERT')
        itools.select(new_selection, replace=True)

    def split_edges_make_loop(self, selection):

        new_verts = []

        for edge in selection:
            itools.set_mode('EDGE')
            itools.select(edge, replace=True)
            self.split_edge_select_vert()
            new_verts.append(itools.get_selected('VERT', item=False)[0])

        itools.set_mode('VERT')
        itools.select(new_verts, replace=True, item=False)
        bpy.ops.mesh.vert_connect()
        itools.set_mode('EDGE')

    def connect_verts_to_last(self, selection):
        bm = itools.get_bmesh()
        ordered_selection = []

        for vert in selection:
            if vert not in bm.select_history:
                ordered_selection.append(vert)

        for item in bm.select_history:
            ordered_selection.append(item)

        for vert in ordered_selection:
            itools.select([vert, ordered_selection[-1]], replace=True)
            bpy.ops.mesh.vert_connect()

        itools.select(selection, replace=True)

    def quad_fill(self):
        selection = itools.get_selected('EDGE')
        bpy.ops.mesh.delete(type='FACE')
        itools.select(selection, 'EDGE', replace=True)
        bpy.ops.mesh.fill_grid()

    def super_smart_create(self):

        mode = itools.get_mode()

        if mode == 'OBJECT':
            if len(itools.get_selected()) > 0:
                bpy.ops.object.duplicate()

            else:
                # if nothing is selected then run creation pie
                print("Nothing Selected")

        # if Vertex is selected
        elif mode == 'VERT':
            bm = itools.get_bmesh()
            selection = itools.get_selected()

            if len(selection) == 0:
                bpy.ops.mesh.knife_tool('INVOKE_DEFAULT')

            elif len(selection) == 1 or (mesh.verts_share_edge(selection) and mesh.are_border_verts(selection)):
                mesh_f2.bpy.ops.mesh.f2('INVOKE_DEFAULT')

            elif mesh.verts_share_face(selection):
                self.connect_verts_to_last(selection)

            else:
                bpy.ops.mesh.vert_connect()

        # if Edge is selected
        elif mode == 'EDGE':
            bm = itools.get_bmesh()
            selection = itools.get_selected()

            if len(selection) == 0:
                bpy.ops.mesh.loopcut_slide('INVOKE_DEFAULT')

            elif len(selection) == 1:
                self.split_edge_select_vert()

            elif mesh.is_border(selection):
                bpy.ops.mesh.edge_face_add()
                itools.set_mode('FACE')

            elif mesh.is_ring(selection):
                self.split_edges_make_loop(selection)

            elif mesh.is_adjacent(selection):
                bpy.ops.mesh.edge_face_add()
                itools.set_mode('EDGE')

            else:
                bpy.ops.mesh.bridge_edge_loops()
                itools.set_mode('EDGE')

        # if Face is selected
        elif mode == 'FACE':
            bm = itools.get_bmesh()
            selection = itools.get_selected()

            if len(selection) == 0:
                print("Reserved for the future")

            if len(selection) == 1:
                self.quad_fill()

            if len(selection) > 1:
                bpy.ops.mesh.bridge_edge_loops()

        # if curve selected
        elif mode == 'EDIT_CURVE':
            selection = itools.get_selected()

            if len(selection) == 0:
                print("Reserved for the future")

            if len(selection) == 2:
                print("")
                bpy.ops.curve.subdivide()

            if len(selection) > 1:
                bpy.ops.mesh.bridge_edge_loops()

    def execute(self, context):
        self.super_smart_create()
        return{'FINISHED'}
