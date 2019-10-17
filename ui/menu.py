import bpy


class SubMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_select_submenu"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.select_all", text="Super Smart Create")
        layout.operator("object.select_all", text="Smart Delete")
        layout.operator("object.select_random", text="Smart Modify")
        layout.operator("object.select_all", text="Super Smart Create")
        layout.operator("object.select_all", text="Smart Delete")
        layout.operator("object.select_random", text="Smart Modify")

        row.operator('mesh.quick_pivot', text="Quick Origin")
        row.operator('mesh.simple_edit_pivot', text="Edit Origin")
        row = layout.row()
        row.operator('mesh.quick_transform_orientation', text="Quick Transform Orientation")
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

        # access this operator as a submenu
        layout.operator_menu_enum("object.select_by_type", "type", text="Select All by Type...")

        layout.separator()

        # expand each operator option into this menu
        layout.operator_enum("object.light_add", "type")

        layout.separator()

        # use existing memu
        layout.menu("VIEW3D_MT_transform")


bpy.utils.register_class(SubMenu)

# test call to display immediately.
bpy.ops.wm.call_menu(name="OBJECT_MT_select_submenu")