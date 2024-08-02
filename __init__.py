import bpy
from . ui.menus import load_menus_itools, unload_menus_itools, VIEW3D_MT_object_mode_itools, VIEW3D_MT_edit_mesh_itools, VIEW3D_MT_edit_lattice_itools, VIEW3D_MT_edit_uvs_itools
from . ui.pies import VIEW3D_MT_PIE_SSC_Duplicate,VIEW3D_MT_PIE_SM_uv ,VIEW3D_MT_PIE_SM_looptools, VIEW3D_MT_PIE_SM_lattice, VIEW3D_MT_PIE_SSC_New_Obj,VIEW3D_MT_PIE_TransformOptions, VIEW3D_MT_PIE_SM_object, VIEW3D_MT_PIE_SM_mesh, VIEW3D_MT_PIE_SM_curve
from . ui.pannels import VIEW3D_PT_Itools
#from . utils.debug import MaxivzToolsDebug_PT_Panel, DebugOp
from . op.super_smart_create import SuperSmartCreate
from . op.radial_symmetry import QuickRadialSymmetry
from . op.quick_align import QuickAlign
from . op.pivot import QuickPivot, QuickEditPivot
from . op.smart_extrude import SmartExtrude, SmartExtrudeModal
from . op.mesh_modes import SelectionModeCycle, QuickSelectionVert, QuickSelectionEdge, QuickSelectionFace
from . op.misc import TransformModeCycle, CSBevel, QuickFlattenAxis, ContextSensitiveSlide, TargetWeldToggle, QuickModifierToggle, QuickWireToggle, WireShadedToggle, FlexiBezierToolsCreate, TransformOrientationCycle, TransformOrientationOp, QuickHpLpNamer, TransformOptionsPie, QuickVisualGeoToMesh, SnapPresetsOp, PropEditOp, ChildrenVisibility, TransformPivotPointOp
from . op.smart_delete import SmartDelete
from . op.smart_modify import SmartModify
from . op.selection import SmartSelectLoop, SmartSelectRing
from . op.smart_transform import SmartTranslate, CSMove, CSRotate, CSScale
from . op.quick_lattice import QuickLattice, LatticeResolution2x2x2, LatticeResolution3x3x3, LatticeResolution4x4x4
from . op.quick_pipe import QuickPipe
from . op.rebase_cylinder import RebaseCylinder
from . op.uv_functions import QuickRotateUv90Pos, QuickRotateUv90Neg, SeamsFromSharps, UvsFromSharps
from . utils.user_prefs import AddonPreferences, OBJECT_OT_addon_prefs_example, MenuPlaceholder, unregister_keymaps, get_enable_legacy_tools

bl_info = {
    "name": "Interactive Tools",
    "author": "Maxi Vazquez, Ajfurey",
    "description": "Collection of context sensitive tools",
    "blender": (4, 2, 0),
    "location": "View3D",
    "version": (1, 4, 1),
    "tracker_url": "https://github.com/maxivz/interactivetoolsblender/issues",
    "wiki_url": "https://maxivz.github.io/interactivetoolsblenderdocs.github.io/",
    "warning": "",
    "category": "Generic"
}


classes = (VIEW3D_PT_Itools, VIEW3D_MT_PIE_SSC_Duplicate, VIEW3D_MT_PIE_SSC_New_Obj, RebaseCylinder,
           VIEW3D_MT_object_mode_itools, VIEW3D_MT_edit_mesh_itools, VIEW3D_MT_edit_lattice_itools,
            VIEW3D_MT_PIE_SM_object, VIEW3D_MT_PIE_SM_mesh, TransformOptionsPie,
           VIEW3D_MT_edit_uvs_itools, VIEW3D_MT_PIE_TransformOptions, SuperSmartCreate, TransformModeCycle, QuickAlign,
           QuickRadialSymmetry,QuickPivot, QuickEditPivot, SelectionModeCycle,
           QuickSelectionEdge, QuickSelectionVert, QuickSelectionFace, VIEW3D_MT_PIE_SM_lattice,
           FlexiBezierToolsCreate, ContextSensitiveSlide, TargetWeldToggle, QuickModifierToggle,
           QuickWireToggle, WireShadedToggle, CSBevel, SmartDelete, TransformOrientationCycle,
           AddonPreferences, OBJECT_OT_addon_prefs_example, TransformOrientationOp, QuickFlattenAxis,
           SmartSelectLoop, SmartSelectRing, CSMove, CSRotate, CSScale,
           VIEW3D_MT_PIE_SM_looptools, VIEW3D_MT_PIE_SM_uv, VIEW3D_MT_PIE_SM_curve,
           QuickLattice,SmartExtrude , SeamsFromSharps, QuickVisualGeoToMesh,
           QuickRotateUv90Pos, QuickRotateUv90Neg, UvsFromSharps,QuickPipe,
           MenuPlaceholder, SmartModify, LatticeResolution2x2x2,
           SnapPresetsOp, PropEditOp, TransformPivotPointOp,
           LatticeResolution3x3x3, LatticeResolution4x4x4, QuickHpLpNamer, ChildrenVisibility)

legacy_classes = (SmartExtrudeModal, SmartTranslate)

classes += legacy_classes

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Load Custom Menus
    load_menus_itools()

    # Keymapping

    # register_keymaps()


def unregister():
    from bpy.utils import unregister_class
    # Keymap removal
    unregister_keymaps()

    # Unload Custom Menus
    unload_menus_itools()

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
