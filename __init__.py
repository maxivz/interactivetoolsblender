import bpy
from . ui.pannels import MaxivzTools_PT_Panel
from . utils.debug import MaxivzToolsDebug_PT_Panel, DebugOp
from . op.super_smart_create import SuperSmartCreate
from . op.radial_symmetry import QuickRadialSymmetry
from . op.quick_align import QuickAlign
from . op.pivot import QuickPivot, QuickEditPivot
from . op.mesh_modes import SelectionModeCycle, QuickSelectionVert, QuickSelectionEdge, QuickSelectionFace
from . op.misc import TransformModeCycle, CSBevel, ContextSensitiveSlide, TargetWeldToggle, QuickModifierToggle, QuickWireToggle, WireShadedToggle
from . op.smart_delete import SmartDelete
from . op.selection import SmartSelectLoop, SmartSelectRing
from . utils.pref_settings import ExampleAddonPreferences, OBJECT_OT_addon_prefs_example, register_keymaps, unregister_keymaps


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
           SuperSmartCreate, TransformModeCycle, QuickAlign, QuickRadialSymmetry,
           QuickPivot, QuickEditPivot, SelectionModeCycle,
           QuickSelectionEdge, QuickSelectionVert, QuickSelectionFace,
           ContextSensitiveSlide, TargetWeldToggle, QuickModifierToggle,
           QuickWireToggle, WireShadedToggle, CSBevel, SmartDelete,
           ExampleAddonPreferences, OBJECT_OT_addon_prefs_example,
           SmartSelectLoop, SmartSelectRing)

# register, unregister = bpy.utils.register_classes_factory(classes)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Keymapping
    register_keymaps()


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)   

    # Keymap removal
    unregister_keymaps()

if __name__ == "__main__":
    register()
