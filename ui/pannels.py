import bpy
from ..utils.user_prefs import get_enable_legacy_tools
from ..utils.constants import COLLISION_COLORS_UPDATE, COLLECTION_COLORS_USE_PARENT_COLOR, DESCRIPTION_DIC
from ..utils.custom_data import itools_data_get

def icon_toggle(row, operator_name, icon_name, constant):
    depress = False     
    if itools_data_get(constant):
        depress = True
    op = row.operator(operator_name, text="", icon = icon_name, depress = depress)
    op.prop_name = constant
    
    if constant in DESCRIPTION_DIC:
        op.description = f"{DESCRIPTION_DIC[constant]} \nCLICK: ON/OFF"
    
    return op

class VIEW3D_PT_Itools(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Itools"
    bl_label = "Interactive Tools"
    bl_category = "Interactive Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Modes Cycling")
        row = layout.row()
        row.operator('mesh.selection_mode_cycle', text="Selection Mode Cycle", icon="RESTRICT_SELECT_OFF")
        row = layout.row()
        row.operator('mesh.transform_mode_cycle', text="Transform Mode Cycle", icon="OUTLINER_OB_EMPTY")
        row = layout.row()
        row.operator('mesh.transform_orientation_cycle', text="Transform Orientation Cycle", icon="OBJECT_ORIGIN")

        layout.label(text="Selection")
        row = layout.row(align=True)
        row.operator('mesh.quick_selection_vert', text="QS Vert", icon="VERTEXSEL")
        row.operator('mesh.quick_selection_edge', text="QS Edge", icon="EDGESEL")
        row.operator('mesh.quick_selection_face', text="QS Face", icon="FACESEL")

        row = layout.row(align=True)
        row.operator('mesh.smart_select_loop', text="Smart Loop")
        row.operator('mesh.smart_select_ring', text="Smart Ring")

        layout.label(text="Transform")
        row = layout.row(align=True)
        row.operator('mesh.cs_move', text="CS Move", icon="ORIENTATION_VIEW")
        row.operator('mesh.cs_rotate', text="CS Rotate", icon="ORIENTATION_GIMBAL")
        row.operator('mesh.cs_scale', text="CS Scale", icon="OBJECT_DATAMODE")

        layout.label(text="Tools")
        row = layout.row()
        row.operator('mesh.super_smart_create', text="Super Smart Create", icon="PLUS")
        row = layout.row()
        row.operator('mesh.smart_delete', text="Smart Delete", icon="TRASH")
        row = layout.row()
        row.operator('mesh.smart_extrude', text="Smart Extrude", icon="EMPTY_SINGLE_ARROW")
        row = layout.row(align=True)
        row.operator('mesh.quick_pivot', text="Quick Origin")
        row.operator('mesh.simple_edit_pivot', text="Edit Origin")
        row = layout.row()
        row.operator('mesh.quick_align', text="Quick Align")
        row = layout.row(align=True)
        row.operator('mesh.quick_pipe', text="Quick Pipe")
        row.operator('mesh.quick_lattice', text="Quick Lattice")
        row = layout.row(align=True)
        row.operator('mesh.rebase_cylinder', text="Rebase Cylinder")
        row.operator('mesh.radial_symmetry', text="Radial Symmetry")
        row = layout.row(align=True)
        row.operator('mesh.context_sensitive_slide', text="CS Slide")
        row.operator('mesh.context_sensitive_bevel', text="CS Bevel")
        row = layout.row(align=True)
        row.operator('mesh.quick_hplp_namer', text="Quick Hp Lp Namer")



        layout.label(text="Collections")
        row = layout.row()
        row.operator('collection.edit_collection_offset_toggle', text="Edit Collection Offset")
        row = layout.row()
        row.operator('collection.rename_objs_by_collection', text="Rename Objects By Collection")

        #Color Object By Collection row
        row = layout.row(align = True)
        row.operator('collection.color_objs_by_collection', text="Color Objects By Collection")
        icon_toggle(row, "itools.toggle_property", "FILE_REFRESH", COLLISION_COLORS_UPDATE)
        icon_toggle(row, "itools.toggle_property", "ORIENTATION_PARENT", COLLECTION_COLORS_USE_PARENT_COLOR)



        layout.label(text="Collisions")
        row = layout.row(align=True)
        row.operator('mesh.quick_convex_hull', text="Quick Convex Hull")

        layout.label(text="Pie Menus")
        row = layout.row()
        row.operator('mesh.smart_modify', text="Smart Modify Pie")
        row = layout.row()
        row.operator('mesh.transform_options_pie', text="Transform Options Pie")

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
        row.operator('uv.seams_from_islands', text="Seams From Islands")
        row = layout.row()
        row.operator('uv.seams_from_sharps', text="Seams From Sharps")
        row = layout.row()
        row.operator('uv.uvs_from_sharps', text="Uvs From Sharps")

        if get_enable_legacy_tools():
            layout.label(text="Legacy Tools")
            row = layout.row()
            row.operator('mesh.smart_extrude_modal', text="Smart Extrude Legacy")
            row = layout.row()
            row.operator('mesh.smart_translate_modal', text="Smart Translate Legacy")
