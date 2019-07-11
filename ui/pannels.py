import bpy


class MaxivzTools_PT_Panel(bpy.types.Panel):
    bl_idname = "MaxivzTools_PT_Panel"
    bl_label = "Maxivz Interactive Tools"
    bl_category = "Maxivz Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        rowa = layout.row()
        rowa.operator('mesh.selection_mode_cycle', text="Selection Mode Cycle")
        rowa.operator('mesh.transform_mode_cycle', text="Transform Mode Cycle")

        row0 = layout.row()
        row0.operator('mesh.quick_selection_vert', text="Quick Sel Vert")
        row0.operator('mesh.quick_selection_edge', text="Quick Sel Edge")
        row0.operator('mesh.quick_selection_face', text="Quick Sel Face")

        row1 = layout.row()
        row1.operator('mesh.super_smart_create', text="Super Smart Create")
        row1.operator('mesh.smart_delete', text="Smart Delete")

        row2 = layout.row()
        row2.operator('mesh.smart_select_loop', text="Smart Loop")
        row2.operator('mesh.smart_select_ring', text="Smart Ring")

        row3 = layout.row()
        # row3.operator('itools.set_cylindrical_sides', text="Set Cylindrical Obj Sides")
        row3.operator('mesh.radial_symmetry', text="Radial Symmetry")

        row4 = layout.row()
        row4.operator('mesh.quick_lattice', text="Quick Lattice")
        row4.operator('mesh.quick_pivot', text="Quick Origin")
        row4.operator('mesh.simple_edit_pivot', text="Edit Origin")

        row5 = layout.row()
        row5.operator('mesh.modifier_toggle', text="Modifier Toggle")
        row5.operator('mesh.wire_toggle', text="Wireframe Toggle")
        row5.operator('mesh.wire_shaded_toggle', text="Wireframe Shaded Toggle")

        row6 = layout.row()
        row6.operator('mesh.target_weld_toggle', text="Target Weld Toggle")

        row7 = layout.row()
        # row6.operator('mesh.smart_extrude_modal', text="Smart Extrude")
        row7.operator('mesh.smart_translate_modal', text="Smart Translate")
        row7.operator('mesh.smart_rotate_modal', text="Smart Rotate")
        row7.operator('mesh.smart_scale_modal', text="Smart Scale")

        row8 = layout.row()
        row8.operator('mesh.context_sensitive_slide', text="CS Slide")
        row8.operator('mesh.context_sensitive_bevel', text="CS Bevel")

        row9 = layout.row()
        # row9.operator('uv.rotate_90_pos', text="Rotate UV 90 Pos")
        # row9.operator('uv.rotate_90_neg', text="Rotate UV 90 Neg")

        row10 = layout.row()
        row10.operator('itools.quick_align', text="Quick Align")
