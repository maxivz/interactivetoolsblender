
import bpy
from bpy.types import Menu

class VIEW3D_MT_PIE_Collections(Menu):
    bl_label = "Collections"

    def active_col_panel(self, context, layout):
        col = context.view_layer.active_layer_collection.collection
        box = layout.box()
        row = box.row()
        row.label(text=f"Active Collection: {col.name}", icon='OUTLINER_COLLECTION')

        row = box.row()
        op = row.operator("collection.collection_boolean_create", text="Col Bool Add", icon="COLLECTION_COLOR_04")
        op.bool_type = 'UNION'

        row = box.row()
        op = row.operator("collection.collection_boolean_create", text="Col Bool Intersect", icon="COLLECTION_COLOR_03")
        op.bool_type = 'INTERSECT'

        row = box.row()
        op = row.operator("collection.collection_boolean_create", text="Col Bool Subtract", icon="COLLECTION_COLOR_01")
        op.bool_type = 'DIFFERENCE'

        row = box.row()
        row.operator('collection.move_to_active_collection', text="Move To Active Obj Col", icon = "DECORATE_DRIVER")

        

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("object.link_to_collection", text="Link To Collection", icon = "DECORATE_LINKED")

        # 6 - RIGHT
        pie.operator("mesh.looptools_curve", text="Remove from Collection")

        # 2 - BOTTOM
        pie.operator("object.move_to_collection", text="Move To Collection", icon = "DECORATE_DRIVER")

        # 8 - TOP
        row = pie.row()
        self.active_col_panel(context, row)

        # 7 - TOP - LEFT
        pie.operator("mesh.looptools_relax", text="Relax")

        # 9 - TOP - RIGHT
        pie.operator("mesh.looptools_space", text="Space")

#Register Classes
classes = [VIEW3D_MT_PIE_Collections]

def register():
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)