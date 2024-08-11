import bpy
import addon_utils
from bpy.types import Operator, AddonPreferences, Menu
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from os.path import basename, dirname
import rna_keymap_ui


def addon_installed(addon_name):
    #Thanks machin3 for the help to make this work for 4.2!
    for mod in addon_utils.modules():
        name = mod.bl_info["name"]

        if name == addon_name:
            return True

    return False


def add_keymap(function_name, key, modifiers=[], kname='3D View Generic', context='VIEW_3D'):
    mod_alt = False
    mod_ctrl = False
    mod_shift = False

    if 'ALT' in modifiers:
        mod_alt = True

    if 'CTRL' in modifiers:
        mod_ctrl = True

    if 'SHIFT' in modifiers:
        mod_shift = True

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.user
    if kc:
        km = kc.keymaps.new(name=kname,
                            space_type=context,
                            region_type='WINDOW')
        kmi = km.keymap_items.new(function_name,
                                  type=key, value='PRESS',
                                  ctrl=mod_ctrl, shift=mod_shift,
                                  alt=mod_alt)

        addon_keymaps.append((km, kmi))


def add_hotkey_ui(name, km, kc, row):
    kmi = get_hotkey_entry_item(km, name)
    if kmi:
        row.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, row, 0)

    else:
        row.label(text="No hotkey entry found")
        add_keymap(name, 'NONE')


def activate_keymap(key):
    print("Get keymap")


def addon_active_prop(addon_active, addon, row, url='none'):
    if addon_active:
        row.operator('menu.placeholder', text=addon)

    else:
        if url != 'none':
            row.operator("wm.url_open", text='Get '+addon, icon="ERROR").url = url

        else:
            row.operator('menu.placeholder', text=addon, icon="ERROR")


def get_addon_name():
    name = __package__
    return name.split(".")[0]


def get_property(target):
    addon_name = get_addon_name()
    addon = bpy.context.preferences.addons.get(addon_name)
    if addon:
        prefs = addon.preferences
        try:
            value = prefs[target]
        except:
            print("Can't Find Value :", target)
        value = False
    else:
        value = False

    return value


def get_keymaps_by_key():
    wm = bpy.context.window_manager
    for km in wm.keyconfigs.user.keymaps:
        print("Keymap :", km)
        for kmi in km:
            print("Keymap Item :", kmi)


def get_keymap(name):
    print("Get keymap")


def get_addon_preferences():
    name = get_addon_name()
    addon_preferences = bpy.context.preferences.addons[name].preferences
    return addon_preferences


def get_hotkey_entry_item(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            return km_item
    return None


#
# Get addon preferences:
#
def get_set_flow_active():
    return set_flow_active


def get_f2_active():
    return f2_active


def get_loop_tools_active():
    return loop_tools_active


def get_qblocker_active():
    return qblocker_active


def get_bezierutilities_active():
    return bezierutilities_active


def get_textools_active():
    return textools_active


def get_ssc_switch_modes():
    prefs = get_addon_preferences()
    return prefs.ssc_switch_modes


def get_ssc_qblocker_integration():
    prefs = get_addon_preferences()
    return prefs.ssc_qblocker_integration


def get_ssc_bezierutilities_integration():
    prefs = get_addon_preferences()
    return prefs.ssc_bezierutilities_integration


def get_enable_sticky_selection():
    prefs = get_addon_preferences()
    return prefs.enable_sticky_selection


def get_enable_show_faces():
    prefs = get_addon_preferences()
    return prefs.enable_show_faces


def get_enable_dissolve_verts():
    prefs = get_addon_preferences()
    return prefs.enable_dissolve_verts


def get_enable_dissolve_faces():
    prefs = get_addon_preferences()
    return prefs.enable_dissolve_faces


def get_radsym_hide_pivot():
    prefs = get_addon_preferences()
    return prefs.radsym_hide_pivot


def get_quickhplp_lp_suffix():
    prefs = get_addon_preferences()
    return prefs.quickhplp_lp_suffix


def get_quickhplp_hp_suffix():
    prefs = get_addon_preferences()
    return prefs.quickhplp_hp_suffix


def get_enable_wireshaded_cs():
    prefs = get_addon_preferences()
    return prefs.enable_wireshaded_cs

def get_transform_mode_cycle_cyclic():
    prefs = get_addon_preferences()
    return prefs.transform_mode_cycle_cyclic

def get_enable_hotkey_editor():
    prefs = get_addon_preferences()
    return prefs.enable_hotkey_editor

def unregister_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.user

    print("Keymaps Disabled")
    print(len(addon_keymaps))
    for km, kmi in addon_keymaps:
        print(kmi)

    for km, kmi in addon_keymaps:
        print(kmi)
        kc.keymaps.keymap_items.remove(kmi)
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def get_enable_legacy_origin():
    prefs = get_addon_preferences()
    return prefs.enable_legacy_origin


def get_enable_legacy_tools():
    prefs = get_addon_preferences()
    return prefs.enable_legacy_tools

# Store keymaps to access after registration
addon_keymaps = []


# Check for integrations:
f2_active = addon_installed("F2")
loop_tools_active = addon_installed("LoopTools")
qblocker_active = addon_installed("QBlocker")
bezierutilities_active = addon_installed("blenderbezierutils")
textools_active = addon_installed("TexTools")
set_flow_active = addon_installed("EdgeFlow")


class MenuPlaceholder(bpy.types.Operator):
    bl_idname = "menu.placeholder"
    bl_label = ""
    bl_description = "Please enable this addon manually"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("addon keymaps : ", addon_keymaps)
        return {'FINISHED'}


class AddonPreferences(AddonPreferences):
    bl_idname = get_addon_name()
    print("NAME : %s", bl_idname)

    # Properties
    cateogries: EnumProperty(name="Categories",
                             items=[("GENERAL", "General Settings", ""),
                                    ("KEYMAPS", "Keymaps", ""), ],
                             default="GENERAL")

    ssc_switch_modes: BoolProperty(name="Super Smart Create Switch Modes",
                                   description="Enables Switching to optimal selection mode after certain operations in Super Smart Create",
                                   default=True)

    ssc_qblocker_integration: BoolProperty(name="Super Smart Create QBlocker Integration",
                                           description="Use QBlocker for primitive creation, needs QBlocker to be used",
                                           default=False)

    ssc_bezierutilities_integration: BoolProperty(name="Super Smart Create Bezier Utilities Integration",
                                                  description="Use Flexi Bezier Tool for spline creation, needs Beier Utilities to be used",
                                                  default=False)

    enable_sticky_selection: BoolProperty(name="Selection Sticky Mode",
                                          description="Enables Sticky Selection when using Quick Select Modes and Selection Cycle",
                                          default=False)

    enable_show_faces: BoolProperty(name="Selection Hilight Faces",
                                    description="Enables Face Hilighting when using Quick Select and Selection Cycle Modes",
                                    default=True)

    enable_dissolve_verts: BoolProperty(name="Smart Delete Dissolve Verts",
                                        description="Verts will be dissolved, if disabled they will be deleted",
                                        default=True)

    enable_dissolve_faces: BoolProperty(name="Smart Delete Dissolve Edges",
                                        description="Non-border edges will be dissolved, if disabled they will be deleted",
                                        default=True)

    radsym_hide_pivot: BoolProperty(name="Hide Radial Symmetry Pivot",
                                    description="Hide Radial Symmetry Pivot on symmetry creation",
                                    default=True)

    quickhplp_lp_suffix: StringProperty(name="Low Poly suffix",
                                      description="Suffix to use for Low Poly Meshes",
                                      default="_low")

    quickhplp_hp_suffix: StringProperty(name="High Poly suffix",
                                    description="Suffix to use for High Poly Meshes",
                                    default="_high")

    enable_wireshaded_cs: BoolProperty(name="Wireframe / Shaded Context Sensitive Mode",
                                       description="Enables context sensitive mode for the Wireframe / Shaded Tool",
                                       default=True)
                        
    transform_mode_cycle_cyclic: BoolProperty(name="Transform Mode Cycle Cyclic",
                                       description="Enables switching to the transform tool right after the Scale Tool",
                                       default=True)

    enable_legacy_origin:  BoolProperty(name="Legacy Origin Edit Mode",
                                        description="Enable Legacy Origin Edit Mode",
                                        default=False)

    enable_legacy_tools:  BoolProperty(name="Enable Legacy Tools",
                                       description="Enable Legacy Tools that are no longer in active development or supported. Use at own risk",
                                       default=False)

    enable_hotkey_editor: BoolProperty(name="Enable Experimental Hotkey Editor",
                                       description="Enables the hotkey editor in Itools Preference Pannel, this is a experimental feature, enable at own risk",
                                       default=False)

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()

        row.prop(self, "cateogries", expand=True)


        box = col.box()

        if self.cateogries == "GENERAL":
            self.draw_general(box)

        elif get_enable_hotkey_editor() and self.cateogries == "KEYMAPS":
            self.draw_keymaps(box)
        
        else:
            self.draw_keymaps_disabled(box)

    def draw_general(self, context):
        column = context.column()
        layout = column

        #Super Smart Create
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Super Smart Create:")
        row = box.row(align=True)

        row = box.row(align=True)
        row.prop(self, "ssc_switch_modes", toggle=False)

        if qblocker_active:
            row = box.row(align=True)
            row.prop(self, "ssc_qblocker_integration", toggle=True)
        else:
            row = box.row(align=True)
            row.label(text="Qblocker Integration unavailable, install the addon to enable")

        if bezierutilities_active:
            row = box.row(align=True)
            row.prop(self, "ssc_bezierutilities_integration", toggle=True)
        else:
            row = box.row(align=True)
            row.label(text="Bezier Utilities Integration unavailable, install the addon to enable")

        #Selection
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Selection:")
        row = box.row(align=True)

        row = box.row(align=True)
        row.prop(self, "enable_sticky_selection", toggle=False)

        row = box.row(align=True)
        row.prop(self, "enable_show_faces", toggle=False)

        #Smart Delete
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Smart Delete:")
        row = box.row(align=True)

        row = box.row(align=True)
        row.prop(self, "enable_dissolve_verts", toggle=False)

        row = box.row(align=True)
        row.prop(self, "enable_dissolve_faces", toggle=False)

        #Quick Lp Hp Name
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Quick Lp Hp Name:")
        row = box.row(align=True)

        row = box.row(align=True)
        row.prop(self, "quickhplp_lp_suffix", toggle=False)

        row = box.row(align=True)
        row.prop(self, "quickhplp_hp_suffix", toggle=False)

        #Other
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Other:")
        row = box.row(align=True)

        row = box.row(align=True)
        row.prop(self, "radsym_hide_pivot", toggle=False)

        row = box.row(align=True)
        row.prop(self, "enable_wireshaded_cs", toggle=False)

        row = box.row(align=True)
        row.prop(self, "transform_mode_cycle_cyclic", toggle=False)

        row = box.row(align=True)
        row.prop(self, "enable_legacy_tools", toggle=False)

        if bpy.app.version >= (2,82,0):
            row = box.row(align=True)
            row.prop(self, "enable_legacy_origin", toggle=False)

        row = box.row(align=True)
        row.prop(self, "enable_hotkey_editor", toggle=False)


        #
        # Recommended Addons::
        #
        box = layout.box()
        row = box.row(align=True)
        row = box.row(align=True)
        row.label(text="Recommended addons:")

        row = box.row(align=True)
        addon_active_prop(f2_active, "F2", row)
        addon_active_prop(loop_tools_active, "Loop Tools", row)
        addon_active_prop(set_flow_active, "Set Flow", row,
                          url='https://github.com/BenjaminSauder/EdgeFlow')
        row = box.row(align=True)
        addon_active_prop(qblocker_active, "QBlocker", row,
                          url='https://gumroad.com/l/gOEV')
        addon_active_prop(bezierutilities_active, "Bezier Utilities", row,
                          url='https://github.com/Shriinivas/blenderbezierutils')
        addon_active_prop(bezierutilities_active, "TexTools", row,
                          url='https://github.com/SavMartin/TexTools-Blender')

        row = box.row(align=True)
        row.label(text="To take full advantage of this addon make sure the following addons are enabled.")

    def draw_keymaps_disabled(self, context):
        column = context.column()
        layout = column

        # Hotkey setup:
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps['3D View Generic']

        row = layout.row(align=True)
        row.label(text="Feature currentlly disabled, to be released in future versions.")


    def draw_keymaps(self, context):
        column = context.column()
        layout = column

        # Hotkey setup:
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps['3D View Generic']

        row = layout.row(align=True)
        row.label(text="This pannel is a Beta feature, use at own risk.")
        row = layout.row(align=True)
        row.label(text="This pannel needs to be opened every time Blender is run for it to enable the set hotkeys")
        row = layout.row(align=True)
        row.label(text="Dont remove keymaps, disable or modify them instead.")


        #
        # Modes Cycling, double space:
        #
        row = layout.row(align=True)
        row = layout.row(align=True)
        row.label(text="Modes Cycling :")

        # Selection Mode Cycle:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.selection_mode_cycle', km, kc, row)

        # Transform Mode Cycle:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.transform_mode_cycle', km, kc, row)

        # Transform Orientation Cycle:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.transform_orientation_cycle', km, kc, row)

        #
        # Selection, double space:
        #
        row = layout.row(align=True)
        row = layout.row(align=True)
        row.label(text="Selection :")

        # Quick Vert:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.quick_selection_vert', km, kc, row)

        # Quick Edge:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.quick_selection_edge', km, kc, row)

        # Quick Face:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.quick_selection_face', km, kc, row)

        # Smart Select Loop:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.smart_select_loop', km, kc, row)

        # Smart Select Ring:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.smart_select_ring', km, kc, row)

        #
        # Smart Tools, double space:
        #
        row = layout.row(align=True)
        row = layout.row(align=True)
        row.label(text="Smart Tools :")

        # Super Smart Create Hotkey:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.super_smart_create', km, kc, row)

        # Smart Delete Hotkey:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.smart_delete', km, kc, row)

        # Smart Extrude:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.smart_extrude_modal', km, kc, row)

        # Smart Extrude:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.smart_modify', km, kc, row)

        # Smart Translate:
        row = layout.row(align=True)
        add_hotkey_ui('mesh.smart_translate_modal', km, kc, row)

        #
        # Utilities, double space:
        #
        row = layout.row(align=True)
        row = layout.row(align=True)
        row.label(text="Utilities :")

        # Quick Origin
        row = layout.row(align=True)
        add_hotkey_ui('mesh.quick_pivot', km, kc, row)

        # Edit Origin
        row = layout.row(align=True)
        add_hotkey_ui('mesh.simple_edit_pivot', km, kc, row)

        # Quick Transform Orientation
        row = layout.row(align=True)
        add_hotkey_ui('mesh.transform_options_pie', km, kc, row)

        # Quick Align
        row = layout.row(align=True)
        add_hotkey_ui('mesh.quick_align', km, kc, row)

        # Quick Lattice
        row = layout.row(align=True)
        add_hotkey_ui('mesh.quick_lattice', km, kc, row)

        # Rebase Cylinder
        row = layout.row(align=True)
        add_hotkey_ui('mesh.rebase_cylinder', km, kc, row)

        # Radial Symmetry
        row = layout.row(align=True)
        add_hotkey_ui('mesh.radial_symmetry', km, kc, row)

        # CS Slide
        row = layout.row(align=True)
        add_hotkey_ui('mesh.context_sensitive_slide', km, kc, row)

        # CS Bevel
        row = layout.row(align=True)
        add_hotkey_ui('mesh.context_sensitive_bevel', km, kc, row)

        #
        # Toggles, double space:
        #
        row = layout.row(align=True)
        row = layout.row(align=True)
        row.label(text="Toggles :")

        # Modifiers On/Off
        row = layout.row(align=True)
        add_hotkey_ui('mesh.modifier_toggle', km, kc, row)

        # Target Weld On/Off
        row = layout.row(align=True)
        add_hotkey_ui('mesh.target_weld_toggle', km, kc, row)

        # Wireframe On/Off
        row = layout.row(align=True)
        add_hotkey_ui('mesh.wire_toggle', km, kc, row)

        # Wireframe / Shaded Toggle
        row = layout.row(align=True)
        add_hotkey_ui('mesh.wire_shaded_toggle', km, kc, row)

        #
        # UV Utilities, double space:
        #
        row = layout.row(align=True)
        row = layout.row(align=True)
        row.label(text="UV Utilities :")

        # Rotate 90 +
        row = layout.row(align=True)
        add_hotkey_ui('uv.rotate_90_pos', km, kc, row)

        # Rotate 90 -
        row = layout.row(align=True)
        add_hotkey_ui('uv.rotate_90_neg', km, kc, row)

        # Seams From Sharps
        row = layout.row(align=True)
        add_hotkey_ui('uv.seams_from_sharps', km, kc, row)

        # UVs From Sharps
        row = layout.row(align=True)
        add_hotkey_ui('uv.uvs_from_sharps', km, kc, row)

    def draw_misc(self, context):
        layout = self.layout
        layout.label(text="This is still work in progress")
        layout.prop(self, "boolean")


class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}
