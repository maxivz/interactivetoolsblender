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


class SM_Menu(Menu):
    bl_idname = "mesh.sm_main_menu"
    bl_label = "Context Sensitive Modify Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("curve.primitive_bezier_curve_add", text="Add Curve", icon="IPO_EASE_IN")
        # 6 - RIGHT
        pie.operator("mesh.primitive_cube_add", text="Add Cube", icon="MESH_CUBE")

        # 2 - BOTTOM
        pie.operator("mesh.primitive_cylinder_add", text="Add Cylinder", icon="MESH_CYLINDER")

        # 8 - TOP
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
        pie.operator("object.sphere_create", text="Add Sphere")

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT

class VIEW3D_MT_PIE_SM_mesh(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

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

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT

class VIEW3D_MT_PIE_QTO(Menu):
    # bl_idname = "mesh.quick_transform_orientation_pie"
    bl_label = "Transform Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_transform_orientation", text="Set Working Pivot").mode = 0

        # 6 - RIGHT
        pie.operator("mesh.quick_transform_orientation", text="Reset Working Pivot").mode = 1

        # 2 - BOTTOM

        # 8 - TOP

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT