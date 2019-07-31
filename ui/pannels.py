import bpy
from bpy.utils import register_class, unregister_class


class MaxivzTools_PT_Panel(bpy.types.Panel):
    bl_idname = "MaxivzTools_PT_Panel"
    bl_label = "Maxivz Interactive Tools"
    bl_category = "Maxivz Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Modes Cycling")
        row = layout.row()
        row.operator('mesh.selection_mode_cycle', text="Selection Mode Cycle", icon="RESTRICT_SELECT_OFF")
        row = layout.row()
        row.operator('mesh.transform_mode_cycle', text="Transform Mode Cycle", icon="OUTLINER_OB_EMPTY")

        layout.label(text="Selection")
        row = layout.row(align=True)
        row.operator('mesh.quick_selection_vert', text="QS Vert", icon="VERTEXSEL")
        row.operator('mesh.quick_selection_edge', text="QS Edge", icon="EDGESEL")
        row.operator('mesh.quick_selection_face', text="QS Face", icon="FACESEL")

        row = layout.row(align=True)
        row.operator('mesh.smart_select_loop', text="Smart Loop")
        row.operator('mesh.smart_select_ring', text="Smart Ring")

        layout.label(text="Smart Tools")
        row = layout.row()
        row.operator('mesh.super_smart_create', text="Super Smart Create", icon="PLUS")
        row = layout.row()
        row.operator('mesh.smart_delete', text="Smart Delete", icon="TRASH")
        row = layout.row()
        row.operator('mesh.smart_modify', text="Smart Modify")
        row = layout.row(align=True)
        row.operator('mesh.smart_extrude_modal', text="Smart Extrude")
        row.operator('mesh.smart_translate_modal', text="Smart Translate")

        layout.label(text="Utilities")
        row = layout.row(align=True)
        row.operator('mesh.quick_pivot', text="Quick Origin")
        row.operator('mesh.simple_edit_pivot', text="Edit Origin")
        row = layout.row()
        row.operator('mesh.quick_align', text="Quick Align")
        row = layout.row()
        row.operator('mesh.quick_lattice', text="Quick Lattice")
        row = layout.row(align=True)
        row.operator('mesh.rebase_cylinder', text="Rebase Cylinder")
        row.operator('mesh.radial_symmetry', text="Radial Symmetry")
        row = layout.row(align=True)
        row.operator('mesh.context_sensitive_slide', text="CS Slide")
        row.operator('mesh.context_sensitive_bevel', text="CS Bevel")

        layout.label(text="Toggles")
        row = layout.row()
        row.operator('mesh.modifier_toggle', text="Modifiers On / Off", icon="MODIFIER_ON")
        row = layout.row()
        row.operator('mesh.target_weld_toggle', text="Target Weld On / Off")
        row = layout.row(align=True)
        row.operator('mesh.wire_toggle', text="Wireframe On/Off")
        row.operator('mesh.wire_shaded_toggle', text="Wire / Shaded")

        layout.label(text="UV Utilities")
        row = layout.row()
        row.operator('uv.rotate_90_pos', text="Rotate 90 +", icon="LOOP_FORWARDS")
        row.operator('uv.rotate_90_neg', text="Rotate 90 -", icon="LOOP_BACK")
        row = layout.row()
        row.operator('uv.seams_from_sharps', text="Seams From Sharps")
        row = layout.row()
        row.operator('uv.uvs_from_sharps', text="Uvs From Sharps")
