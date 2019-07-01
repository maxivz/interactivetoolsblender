import bpy
from . ui.pannels import MaxivzTools_PT_Panel
from . utils.debug import MaxivzToolsDebug_PT_Panel, DebugOp
from . op.super_smart_create import SuperSmartCreate
from . op.radial_symmetry import QuickRadialSymmetry
from . op.quick_align import QuickAlign
from . op.pivot import QuickPivot, QuickEditPivot
from . op.mesh_modes import QuickSelectionVert, QuickSelectionEdge, QuickSelectionFace
from . op.misc import CSBevel, ContextSensitiveSlide, TargetWeldToggle, QuickModifierToggle, QuickWireToggle, WireShadedToggle
from . op.smart_delete import SmartDelete


bl_info = {
    "name": "MaxivzsTools",
    "author": "Maxi Vazquez",
    "description": "Collection of context sensitive and time saving tools",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}


classes = (MaxivzTools_PT_Panel, MaxivzToolsDebug_PT_Panel, DebugOp,
           SuperSmartCreate, QuickAlign, QuickRadialSymmetry,
           QuickPivot, QuickEditPivot,
           QuickSelectionEdge, QuickSelectionVert, QuickSelectionFace,
           ContextSensitiveSlide, TargetWeldToggle, QuickModifierToggle,
           QuickWireToggle, WireShadedToggle, CSBevel, SmartDelete)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
