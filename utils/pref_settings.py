import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

# this is an internal API at the moment
import rna_keymap_ui

# bl_info = {"name": "KeyMap Test", "category": "Object"}


class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")

        """
        col = layout.column()
        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in addon_keymaps:
            km = km.active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        """


class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "itools.addon_prefs_example"
    bl_label = "Addon Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # user_preferences = context.user_preferences
        #  addon_prefs = user_preferences.addons[__name__].preferences
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}


addon_keymaps = []


# Registration
def register_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("object.editmode_toggle", 'NUMPAD_SLASH', 'PRESS', shift=True)
    kmi.active = True
    addon_keymaps.append((km, kmi))
    kmi = km.keymap_items.new("object.transform_apply", 'NUMPAD_SLASH', 'PRESS', shift=True)
    kmi.active = True
    addon_keymaps.append((km, kmi))


def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

"""
# Remove keymap

wm = bpy.context.window_manager
kc = wm.keyconfigs.user

for k in kc.keymaps["Frames"].keymap_items:
    if k.idname == "screen.animation_play" and k.active:
        k.active = True
        k.type = 'Q'
        k.value = 'PRESS'
        k.shift = True
        k.ctrl = True
        k.alt = True    
"""