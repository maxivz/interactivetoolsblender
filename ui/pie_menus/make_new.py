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
        row.operator("wm.tool_set_by_id", text="", icon="GREASEPENCIL").name = "builtin.primitive_cube_add"


        row = column.row(align=True)
        row.operator("mesh.primitive_cylinder_add", text="Cylinder", icon="MESH_CYLINDER")
        row.operator("wm.tool_set_by_id", text="", icon="GREASEPENCIL").name = "builtin.primitive_cylinder_add"


        row = column.row(align=True)
        row.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon="MESH_UVSPHERE")
        row.operator("wm.tool_set_by_id", text="", icon="GREASEPENCIL").name = "builtin.primitive_uv_sphere_add"


        row = column.row(align=True)
        row.operator("curve.add_bezier_simple", text="Curve", icon="IPO_EASE_IN").mode = "Simple"
        row.emboss = "PULLDOWN_MENU"
        row.operator("curve.add_bezier_simple", text="", icon="GREASEPENCIL").mode = "Draw"

        

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

