import bpy
from bpy.types import Menu
from .. utils.user_prefs import get_qblocker_active, get_ssc_qblocker_integration, get_ssc_bezierutilities_integration, get_bezierutilities_active


class VIEW3D_MT_PIE_SSC_Duplicate(Menu):
    # bl_idname = "mesh.ssc_duplicate_menu"
    bl_label = "Object Duplication"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("object.duplicate", text="Duplicate")
        # 6 - RIGHT
        pie.operator("object.duplicate", text="Duplicate Linked").linked = True
        # 2 - BOTTOM

        # 8 - TOP

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT


class VIEW3D_MT_PIE_SSC_New_Obj(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Object Creation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        qblocker = get_qblocker_active() and get_ssc_qblocker_integration()
        bezierutils = get_bezierutilities_active() and get_ssc_bezierutilities_integration()

        # 4 - LEFT
        if bezierutils:
            pie.operator("curve.flexitool_create", text="Add Curve", icon="IPO_EASE_IN")

        else:
            pie.operator("curve.primitive_bezier_curve_add", text="Add Curve", icon="IPO_EASE_IN")
        # 6 - RIGHT

        if qblocker:
            pie.operator("object.box_create", text="Add Cube", icon="MESH_CUBE")

        else:
            pie.operator("mesh.primitive_cube_add", text="Add Cube", icon="MESH_CUBE")

        # 2 - BOTTOM
        if qblocker:
            pie.operator("object.cylinder_create", text="Add Cylinder", icon="MESH_CYLINDER")

        else:
            pie.operator("mesh.primitive_cylinder_add", text="Add Cylinder", icon="MESH_CYLINDER")

        # 8 - TOP
        if qblocker:
            pie.operator("object.sphere_create", text="Add Sphere", icon="MESH_UVSPHERE")

        else:
            pie.operator("mesh.primitive_uv_sphere_add", text="Add Sphere", icon="MESH_UVSPHERE")
        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT


class VIEW3D_MT_PIE_SM_object(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_lattice", text="Quick Lattice")

        # 6 - RIGHT
        pie.operator("mesh.radial_symmetry", text="Radial Symmetry")

        # 2 - BOTTOM
        pie.operator("mesh.rebase_cylinder", text="Rebase Cylinder")

        # 8 - TOP
        pie.operator("object.convert", text="Visual Geo To Mesh").target = 'MESH'

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT

class VIEW3D_MT_PIE_SM_lattice(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.lattice_resolution_2x2x2", text="Resolution 2x2x2")

        # 6 - RIGHT
        pie.operator("mesh.lattice_resolution_4x4x4", text="Resolution 4x4x4")

        # 2 - BOTTOM
        pie.operator("mesh.lattice_resolution_3x3x3", text="Resolution 3x3x3")

        # 8 - TOP
        pie.operator("mesh.quick_lattice", text="Apply Lattice")

class VIEW3D_MT_PIE_SM_curve(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.lattice_resolution_2x2x2", text="Resolution 2x2x2")

        # 6 - RIGHT
        pie.operator("mesh.lattice_resolution_4x4x4", text="Resolution 4x4x4")

        # 2 - BOTTOM
        pie.operator("mesh.quick_lattice", text="Apply Lattice")

        # 8 - TOP
        pie.operator("mesh.lattice_resolution_3x3x3", text="Resolution 3x3x3")

class VIEW3D_MT_PIE_SM_mesh(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT

        # 6 - RIGHT


        # 2 - BOTTOM


        # 8 - TOP
        pie.operator("object.convert", text="Visual Geo To Mesh").target = 'MESH'

        # 7 - TOP - LEFT
        pie.operator("mesh.quick_lattice", text="Symmetrize")

        # 9 - TOP - RIGHT
        pie.operator("mesh.quick_lattice", text="Rebase Cylinder")


        # 1 - BOTTOM - LEFT
        pie.operator("mesh.quick_lattice", text="Quick Pipe(TODO)")

        # 3 - BOTTOM - RIGHT
        pie.operator("mesh.quick_lattice", text="Quick Lattice")



        # Align World Submenu
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align = True)
        row.operator("mesh.primitive_cube_add", text = "Align World")
        row = column.row(align = True)
        row.operator("mesh.primitive_cube_add", text = "X")
        row.operator("mesh.primitive_cube_add", text = "Y")
        row.operator("mesh.primitive_cube_add", text = "Z")

        # Flatten Submenu
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align = True)
        row.operator("mesh.primitive_cube_add", text = "Flatten")
        row = column.row(align = True)
        row.operator("transform.resize", text = "X")
        row.operator("transform.resize", text = "Y")
        row.operator("transform.resize", text = "Z")

        # Flow Submenu
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align = True)
        row.operator("mesh.looptools_circle", text="Make Circle")
        op = row.operator("mesh.set_edge_flow", text="Set Flow")
        op.tension = 180
        op.iterations = 1
        row.operator("mesh.looptools_space", text="Space")
        row = column.row(align = True)
        row.operator("wm.call_menu_pie", text = "Loop Tools...", icon = "RIGHTARROW_THIN").name="VIEW3D_MT_PIE_SM_looptools"

class VIEW3D_MT_PIE_SM_looptools(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Loop Tools"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.looptools_circle", text="Make Circle")
        # 6 - RIGHT
        pie.operator("mesh.looptools_flatten", text="Flatten")

        # 2 - BOTTOM
        pie.operator("mesh.looptools_curve", text="Make Curve")

        # 8 - TOP
        op4 = pie.operator("mesh.set_edge_flow", text="Set Flow")
        op4.tension = 180
        op4.iterations = 1

        # 7 - TOP - LEFT
        pie.operator("mesh.looptools_relax", text="Relax")

        # 9 - TOP - RIGHT
        pie.operator("mesh.looptools_space", text="Space")

class VIEW3D_MT_PIE_QTO(Menu):
    bl_label = "Transform Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Set Custom 2", icon = 'TRIA_DOWN').mode = 2

        # 6 - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Use Custom 2", icon = 'TRIA_UP').mode = 5

        # 2 - BOTTOM
        pie.operator("mesh.quick_transform_orientation", text="Reset Working Pivot", icon = 'FILE_REFRESH').mode = 7
        # 8 - TOP
        pie.operator("wm.call_menu_pie", text = "Default Orientations...", icon = "RIGHTARROW_THIN").name="VIEW3D_MT_PIE_DefaultOrientations"

        # 7 - TOP - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Set Custom 1", icon = 'TRIA_DOWN').mode = 1

        # 9 - TOP - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Use Custom 1", icon = 'TRIA_UP').mode = 4

        # 1 - BOTTOM - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Set Custom 3", icon = 'TRIA_DOWN').mode = 3

        # 3 - BOTTOM - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Use Custom 3", icon = 'TRIA_UP').mode = 6

class VIEW3D_MT_PIE_DefaultOrientations(Menu):
    bl_label = "Transform Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Global", icon = "ORIENTATION_GLOBAL").mode = 8

        # 6 - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Local", icon = "ORIENTATION_LOCAL").mode = 9

        # 2 - BOTTOM
        pie.operator("mesh.quick_transform_orientation", text="Cursor", icon = "ORIENTATION_CURSOR").mode = 13

        # 8 - TOP
        pie.operator("mesh.quick_transform_orientation", text="Normal", icon = "ORIENTATION_NORMAL").mode = 10

        # 7 - TOP - LEFT
        pie.operator("mesh.quick_transform_orientation", text="View", icon = "ORIENTATION_VIEW").mode = 12
   
        # 9 - TOP - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Gimbal", icon = "ORIENTATION_GIMBAL").mode = 11

class VIEW3D_MT_PIE_TransformOptions(Menu):
    bl_label = "Transform Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Orientations").mode = 2

        # 6 - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Pivot").mode = 5

        # 2 - BOTTOM
        pie.operator("mesh.quick_transform_orientation", text="Snap").mode = 7

        # 8 - TOP
        pie.operator("mesh.quick_transform_orientation", text="Proportional Editing").mode = 7

class VIEW3D_MT_PIE_SnapPresets(Menu):
    bl_label = "Snap Presets"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Surface").mode = 2

        # 6 - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Grid").mode = 5

        # 2 - BOTTOM
        pie.operator("mesh.quick_transform_orientation", text="Snap").mode = 7

        # 8 - TOP
        pie.operator("mesh.quick_transform_orientation", text="Proportional Editing").mode = 7