import bpy
from bpy.types import Menu


class SSC_Duplicate_Menu(Menu):
    bl_idname = "mesh.ssc_duplicate_menu"
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


class SSC_New_Obj_Menu(Menu):
    bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Object Creation"

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