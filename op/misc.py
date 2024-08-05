import bpy
from ..utils import itools as itools
from .. utils import dictionaries as dic
from .. utils.user_prefs import get_quickhplp_hp_suffix, get_quickhplp_lp_suffix, get_enable_wireshaded_cs, get_transform_mode_cycle_cyclic


class TransformModeCycle(bpy.types.Operator):
    bl_idname = "mesh.transform_mode_cycle"
    bl_label = "Transform Mode Cycle"
    bl_description = "Cycle between Move/Rotate/Scale modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        areas = bpy.context.workspace.screens[0].areas

        for area in areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Make active tool is set to select
                    context_override = bpy.context.copy()
                    context_override["space_data"] = area.spaces[0]
                    context_override["area"] = area

                    with context.temp_override(**context_override):
                        bpy.ops.wm.tool_set_by_id( name="builtin.select_box")

                    if space.show_gizmo_object_translate:
                        space.show_gizmo_object_translate = False
                        space.show_gizmo_object_rotate = True

                    elif space.show_gizmo_object_rotate:
                        space.show_gizmo_object_rotate = False
                        space.show_gizmo_object_scale = True

                    elif space.show_gizmo_object_scale:
                        space.show_gizmo_object_scale = False

                        if get_transform_mode_cycle_cyclic():
                            space.show_gizmo_object_translate = True

                    else:
                        space.show_gizmo_object_translate = True

        return{'FINISHED'}


class TransformOrientationCycle(bpy.types.Operator):
    bl_idname = "mesh.transform_orientation_cycle"
    bl_label = "Transform Orientation Cycle"
    bl_description = "Cycles trough transform orientation modes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        space = bpy.context.scene.transform_orientation_slots[0].type

        if space == 'GLOBAL':
            new_space = 'LOCAL'

        elif space == 'LOCAL':
            new_space = 'NORMAL'

        elif space == 'NORMAL':
            new_space = 'GIMBAL'

        elif space == 'GIMBAL':
            new_space = 'VIEW'

        elif space == 'VIEW':
            new_space = 'CURSOR'

        elif space == 'CURSOR':
            new_space = 'GLOBAL'

        bpy.context.scene.transform_orientation_slots[0].type = new_space

        return {'FINISHED'}


class CSBevel(bpy.types.Operator):
    bl_idname = "mesh.context_sensitive_bevel"
    bl_label = "Context Sensistive Bevel"
    bl_description = "Context Sensitive Bevels and Inset"
    bl_options = {'REGISTER', 'UNDO'}

    def cs_bevel(self):

        mode = itools.get_mode()

        version = bpy.app.version_string[:4]

        try:
            version = float(version)
        except ValueError:
            version = float(version[:-1])

        if mode == 'VERT':
            if version >= 2.90:
                bpy.ops.mesh.bevel('INVOKE_DEFAULT', affect='VERTICES')
            else:
                bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=True)

        if mode == 'EDGE':
            if version >= 2.90:
                bpy.ops.mesh.bevel('INVOKE_DEFAULT', affect='EDGES')
            else:
                bpy.ops.mesh.bevel('INVOKE_DEFAULT', vertex_only=False)

        if mode == 'FACE':
            bpy.ops.mesh.inset('INVOKE_DEFAULT')

    def execute(self, context):
        self.cs_bevel()
        return{'FINISHED'}


class ChildrenVisibility(bpy.types.Operator):
    bl_idname = "object.children_visibility"
    bl_label = "Children Visibility"
    bl_description = "Hide or show children for the selected object"
    bl_options = {'REGISTER', 'UNDO'}

    hide: bpy.props.BoolProperty(default=True)

    def change_children_visibility(self):
        children = itools.get_children(itools.get_selected(item=False)[0])
        for obj in children:
            bpy.data.objects[obj.name].hide_viewport = self.hide

    def execute(self, context):
        self.change_children_visibility()
        return{'FINISHED'}


class ContextSensitiveSlide(bpy.types.Operator):
    bl_idname = "mesh.context_sensitive_slide"
    bl_label = "Context Sensitive Slide"
    bl_description = "Slide vert or edge based on selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bm = itools.get_bmesh()
        mode = itools.get_mode()

        if mode == 'VERT':
            bpy.ops.transform.vert_slide('INVOKE_DEFAULT')

        elif mode == 'EDGE':
            bpy.ops.transform.edge_slide('INVOKE_DEFAULT')

        return{'FINISHED'}


class TargetWeldToggle(bpy.types.Operator):
    bl_idname = "mesh.target_weld_toggle"
    bl_label = "Target Weld On / Off"
    bl_description = "Toggles snap to vertex and automerge editing on and off"
    bl_options = {'REGISTER', 'UNDO'}

    def toggle_target_weld(self, context):
        if context.scene.tool_settings.use_mesh_automerge and bpy.context.scene.tool_settings.use_snap:
            context.scene.tool_settings.use_mesh_automerge = False
            bpy.context.scene.tool_settings.use_snap = False
        else:
            context.scene.tool_settings.snap_elements |= {'VERTEX'}
            context.scene.tool_settings.use_mesh_automerge = True
            bpy.context.scene.tool_settings.use_snap = True

    def execute(self, context):
        self.toggle_target_weld(context)
        return{'FINISHED'}


class QuickModifierToggle(bpy.types.Operator):
    bl_idname = "mesh.modifier_toggle"
    bl_label = "Modifiers On / Off"
    bl_description = "Toggles the modifiers on and off for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def modifier_toggle(self, context):
        mode = itools.get_mode()

        if mode in ['VERT', 'EDGE', 'FACE']:
            itools.set_mode('OBJECT')

        selected = itools.get_selected()

        for obj in selected:
            if all(modifier.show_in_editmode and modifier.show_viewport for modifier in obj.modifiers):
                for modifier in obj.modifiers:
                    modifier.show_in_editmode = False
                    modifier.show_viewport = False

            else:
                for modifier in obj.modifiers:
                    modifier.show_in_editmode = True
                    modifier.show_viewport = True

        if mode in ['VERT', 'EDGE', 'FACE']:
            itools.set_mode(mode)

    def execute(self, context):
        self.modifier_toggle(context)
        return {'FINISHED'}


class QuickWireToggle(bpy.types.Operator):
    bl_idname = "mesh.wire_toggle"
    bl_label = "Wireframe On / Off"
    bl_description = "Toggles wire mode on and off on all objects"
    bl_options = {'REGISTER', 'UNDO'}

    def wire_toggle(self, context):
        if context.space_data.overlay.show_wireframes:
            context.space_data.overlay.show_wireframes = False
        else:
            context.space_data.overlay.show_wireframes = True

    def execute(self, context):
        self.wire_toggle(context)
        return{'FINISHED'}


class TransformOrientationOp(bpy.types.Operator):
    bl_idname = "mesh.transform_orientation_op"
    bl_label = "Transform Orientation Operator"
    bl_description = "Sets up a transform orientation from selected"
    bl_options = {'REGISTER', 'UNDO'}

    # Mode 1 - Set Orientation 1
    # Mode 2 - Set Orientation 2
    # Mode 3 - Set Orientation 3
    # Mode 4 - Use Orientation 1
    # Mode 5 - Use Orientation 2
    # Mode 6 - Use Orientation 3
    # Mode 7 - Reset Orientation

    mode: bpy.props.IntProperty(default=0)
    target_space = 'NONE'

    def set_target_space(self, context):
        if self.mode in [1, 4]:
            self.target_space = 'Custom 1'

        elif self.mode in [2, 5]:
            self.target_space = 'Custom 2'

        elif self.mode in [3, 6]:
            self.target_space = 'Custom 3'

    def make_orientation(self, context):
        space = bpy.context.scene.transform_orientation_slots[0].type
        selection = itools.get_selected()

        if space in ['GLOBAL', 'LOCAL', 'NORMAL', 'GIMBAL', 'VIEW', 'CURSOR']:
            dic.write("stored_transform_orientation", space)

        bpy.ops.transform.create_orientation(
            name=self.target_space, use=True, overwrite=True)

    def set_orientation(self, context):
        if self.mode in [4, 5, 6]:
            try:
                bpy.context.scene.transform_orientation_slots[0].type = self.target_space

            except:
                self.make_orientation(context)

        else:
            if self.mode == 8:
                bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
            elif self.mode == 9:
                bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
            elif self.mode == 10:
                bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
            elif self.mode == 11:
                bpy.context.scene.transform_orientation_slots[0].type = 'GIMBAL'
            elif self.mode == 12:
                bpy.context.scene.transform_orientation_slots[0].type = 'VIEW'
            elif self.mode == 13:
                bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'

    def reset_orientation(self, context):
        space = bpy.context.scene.transform_orientation_slots[0].type
        new_space = dic.read("stored_transform_orientation")

        if new_space != '':
            bpy.context.scene.transform_orientation_slots[0].type = new_space
        else:
            bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'

    def execute(self, context):
        self.set_target_space(context)

        if self.mode in [1, 2, 3]:
            self.make_orientation(context)

        elif self.mode in [4, 5, 6, 8, 9, 10, 11, 12, 13]:
            self.set_orientation(context)

        elif self.mode == 7:
            self.reset_orientation(context)

        return{'FINISHED'}


class TransformPivotPointOp(bpy.types.Operator):
    bl_idname = "mesh.transform_pivot_point_op"
    bl_label = "Transform Pivot Point Operator"
    bl_description = "Sets up transform Pivot Point"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.IntProperty(default=0)

    def set_transform_pivot_point(self, context):
        if self.mode == 1:
            bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
        elif self.mode == 2:
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
        elif self.mode == 3:
            bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        elif self.mode == 4:
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        elif self.mode == 5:
            bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

    def execute(self, context):
        self.set_transform_pivot_point(context)

        return{'FINISHED'}


class TransformOptionsPie(bpy.types.Operator):
    bl_idname = "mesh.transform_options_pie"
    bl_label = "Transform Orientation Pie"
    bl_description = "Sets up a transform orientation from selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_TransformOptions")
        return{'FINISHED'}


class SnapPresetsOp(bpy.types.Operator):
    bl_idname = "mesh.snap_presets_op"
    bl_label = "Quick Snap Presets"
    bl_description = "Sets up snapping settings based on presets"
    bl_options = {'REGISTER', 'UNDO'}

    # Mode 1 - Grid Absolute
    # Mode 2 - Vert Center
    # Mode 3 - Vert Closest
    # Mode 4 - Face Normal

    mode: bpy.props.IntProperty(default=0)

    def set_preset(self, context):
        bpy.context.scene.tool_settings.use_snap_translate = True
        bpy.context.scene.tool_settings.use_snap_rotate = True
        bpy.context.scene.tool_settings.use_snap_scale = True

        if self.mode == 1:
            bpy.context.scene.tool_settings.snap_elements = {'INCREMENT'}
            bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
            bpy.context.scene.tool_settings.use_snap_grid_absolute = True
            bpy.context.scene.tool_settings.use_snap_align_rotation = False

        elif self.mode == 2:
            bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
            bpy.context.scene.tool_settings.snap_target = 'CENTER'
            bpy.context.scene.tool_settings.use_snap_align_rotation = False

        elif self.mode == 3:
            bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
            bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
            bpy.context.scene.tool_settings.use_snap_align_rotation = False

        elif self.mode == 4:
            bpy.context.scene.tool_settings.snap_elements = {'FACE'}
            bpy.context.scene.tool_settings.snap_target = 'CENTER'
            bpy.context.scene.tool_settings.use_snap_align_rotation = True
            bpy.context.scene.tool_settings.use_snap_project = True

        elif self.mode == 5:
            bpy.context.scene.tool_settings.snap_elements = {'EDGE_MIDPOINT'}
            bpy.context.scene.tool_settings.snap_target = 'MEDIAN'
            bpy.context.scene.tool_settings.use_snap_align_rotation = False
            bpy.context.scene.tool_settings.use_snap_project = False

    def execute(self, context):
        self.set_preset(context)
        return{'FINISHED'}


class PropEditOp(bpy.types.Operator):
    bl_idname = "mesh.prop_edit_op"
    bl_label = "Proportional Editing Op"
    bl_description = "Sets up Proportional Editing Falloffs"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.IntProperty(default=0)

    def set_preset(self, context):

        if self.mode == 1:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'SMOOTH'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 2:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'SPHERE'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 3:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'ROOT'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 4:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'INVERSE_SQUARE'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 5:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'SHARP'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 6:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'LINEAR'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 7:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'CONSTANT'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 8:
            bpy.context.scene.tool_settings.proportional_edit_falloff = 'RANDOM'
            bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 9:
            if bpy.context.scene.tool_settings.use_proportional_edit_objects:
                bpy.context.scene.tool_settings.use_proportional_edit_objects = False
            else:
                bpy.context.scene.tool_settings.use_proportional_edit_objects = True

        elif self.mode == 10:
            if bpy.context.scene.tool_settings.use_proportional_connected:
                bpy.context.scene.tool_settings.use_proportional_connected = False
            else:
                bpy.context.scene.tool_settings.use_proportional_connected = True

        elif self.mode == 11:
            if bpy.context.scene.tool_settings.use_proportional_projected:
                bpy.context.scene.tool_settings.use_proportional_projected = False
            else:
                bpy.context.scene.tool_settings.use_proportional_projected = True

    def execute(self, context):
        self.set_preset(context)
        return{'FINISHED'}


class ObjectPropertiesPie(bpy.types.Operator):
    bl_idname = "mesh.obj_properties_pie"
    bl_label = "Object Properties Pie"
    bl_description = "Sets up Object Properties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_ObjectProperties")
        return{'FINISHED'}


class WireShadedToggle(bpy.types.Operator):
    bl_idname = "mesh.wire_shaded_toggle"
    bl_label = "Wireframe / Shaded Toggle"
    bl_description = "Toggles between wireframe and shaded mode"
    bl_options = {'REGISTER', 'UNDO'}

    def wire_shaded_toggle(self, context):
        selection = itools.get_selected('OBJECT')

        if len(selection) > 0 and get_enable_wireshaded_cs():
            if all(obj.display_type == 'WIRE' for obj in selection):
                for obj in selection:
                    obj.display_type = 'TEXTURED'

            else:
                for obj in selection:
                    obj.display_type = 'WIRE'

        else:
            areas = context.workspace.screens[0].areas
            for area in areas:
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.shading.type == 'WIREFRAME':
                            stored_mode = dic.read("shading_mode")

                            if len(stored_mode) < 1:
                                stored_mode = 'SOLID'

                            space.shading.type = stored_mode
                        else:
                            dic.write("shading_mode", space.shading.type)
                            space.shading.type = 'WIREFRAME'

    def execute(self, context):
        self.wire_shaded_toggle(context)
        return{'FINISHED'}


class FlexiBezierToolsCreate(bpy.types.Operator):
    bl_idname = "curve.flexitool_create"
    bl_label = "Flexi Bezier Tools Create"
    bl_description = "Executes Flexi Bezier Tools Create"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                bpy.ops.wm.tool_set_by_id(name='flexi_bezier.draw_tool')
        return{'FINISHED'}


class QuickHpLpNamer(bpy.types.Operator):
    bl_idname = "mesh.quick_hplp_namer"
    bl_label = "Quick HP Lp Namer"
    bl_description = "Helps with naming the hp and lp for name matching baking"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = []
        selection = itools.get_selected()
        lp_suffix = get_quickhplp_lp_suffix()
        hp_suffix = get_quickhplp_hp_suffix()

        lp = [obj for obj in selection if obj.name.endswith(lp_suffix)]
        if len(lp) != 1:
            polycount_list = [len(obj.data.polygons) for obj in selection]
            lowest_index = polycount_list.index(min(polycount_list))
            lp = selection[lowest_index]
            lp.name = lp.name + lp_suffix

        elif lp[0].name.endswith(lp_suffix):
            lp = lp[0]

        for obj in selection:
            if obj != lp:
                obj.name = lp.name[:-len(lp_suffix)] + hp_suffix

        return{'FINISHED'}


class QuickVisualGeoToMesh(bpy.types.Operator):
    bl_idname = "mesh.quick_visual_geo_to_mesh"
    bl_label = "Quick Visual Geo To Mesh"
    bl_description = "Visual Geo To Mesh that also workds from edit mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mode = itools.get_mode()
        if mode in ['VERT', 'EDGE', 'FACE']:
            itools.set_mode('OBJECT')
            bpy.ops.object.convert(target='MESH')
            itools.set_mode(mode)

        else:
            bpy.ops.object.convert(target='MESH')

        return{'FINISHED'}


class QuickFlattenAxis(bpy.types.Operator):
    # Add support for local aligns

    bl_idname = "mesh.quick_flatten"
    bl_label = "Quick Flatten"
    bl_description = "Quick Flatten with axis options"
    bl_options = {'REGISTER', 'UNDO'}

    # Mode 1 - Global
    # Mode 2 - Flatten X
    # Mode 3 - Flatten Y
    # Mode 4 - Flatten Z

    mode: bpy.props.IntProperty(default=0)

    def execute(self, context):
        if self.mode == 1:
            bpy.ops.mesh.looptools_flatten()

        else:
            if self.mode == 2:
                axis_transform = (0, 1, 1)
            elif self.mode == 3:
                axis_transform = (1, 0, 1)
            elif self.mode == 4:
                axis_transform = (1, 1, 0)

            bpy.ops.transform.resize(value=axis_transform, orient_type='GLOBAL',
                                     mirror=True, use_proportional_edit=False, release_confirm=True)

        return{'FINISHED'}
