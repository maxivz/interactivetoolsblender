import bpy
from . ui.pannels import MaxivzTools_PT_Panel
from . utils.debug import MaxivzToolsDebug_PT_Panel, DebugOp
from . op.super_smart_create import SuperSmartCreate
from . op.radial_symmetry import QuickRadialSymmetry
from . op.quick_align import QuickAlign


bl_info = {
    "name": "MaxivzsTools",
    "author": "Maxi Vazquez",
    "description": "Collection of context sensitive and time saving tools",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}


classes = (MaxivzTools_PT_Panel, MaxivzToolsDebug_PT_Panel, DebugOp, SuperSmartCreate, QuickAlign, QuickRadialSymmetry)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()

