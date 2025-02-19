import bpy
from bpy.types import Menu

class VIEW3D_MT_PIE_Make_New(Menu):
    bl_label = "New"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 1 - LEFT
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align=True)

        row.operator("object.empty_add", text="Empty", icon="OUTLINER_OB_EMPTY").type = 'ARROWS'
        row = column.row(align=True)
        row.operator("object.gpencil_add", text="Gpencil", icon="OUTLINER_OB_GREASEPENCIL").type = 'EMPTY'

        row = column.row(align=True)
        row.operator("object.camera_add", text="Camera", icon="OUTLINER_OB_CAMERA")

        row = column.row(align=True)
        row.operator("object.light_add", text="Light", icon="OUTLINER_OB_LIGHT").type = 'POINT'



        # 2 - RIGHT
        submenu = pie.column()
        container = submenu.box()
        column = container.column()

        row = column.row(align=True)
        row.operator("mesh.primitive_cube_add", text="Cube", icon="MESH_CUBE")

        row = column.row(align=True)
        row.operator("mesh.primitive_cylinder_add", text="Cylinder", icon="MESH_CYLINDER")

        row = column.row(align=True)
        row.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon="MESH_UVSPHERE")

        row = column.row(align=True)
        row.operator("curve.add_bezier_empty", text="Curve", icon="IPO_EASE_IN")

        # 3 - BOTTOM

        submenu = pie.column()
        column = submenu.column()

        has_collections = bool(bpy.data.collections)
        column.enabled = has_collections


        column.operator_context = 'INVOKE_REGION_WIN'
        column.operator(
            "object.collection_instance_add",
            text="Collection Instance..." if has_collections else "No Collections to Instance",
            icon='OUTLINER_OB_GROUP_INSTANCE',
        )
