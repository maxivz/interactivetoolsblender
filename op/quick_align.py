import bpy
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from bpy.props import BoolProperty, EnumProperty
from mathutils import Vector
from .. utils import itools as itools


class QuickAlign(bpy.types.Operator):
    bl_idname = "mesh.quick_align"
    bl_label = "Quick Align"
    bl_description = "Quickly Align Objects"
    bl_options = {'REGISTER', 'UNDO'}

    bb_quality: BoolProperty(
        name="High Quality",
        description=(
            "Enables high quality calculation of the "
            "bounding box for perfect results on complex "
            "shape meshes with rotation/scale (Slow)"
        ),
        default=True,
    )
    align_mode: EnumProperty(
        name="Align Mode:",
        description="Side of object to use for alignment",
        items=(
            ('OPT_1', "Negative Sides", ""),
            ('OPT_2', "Centers", ""),
            ('OPT_3', "Positive Sides", ""),
        ),
        default='OPT_2',
    )
    relative_to: EnumProperty(
        name="Relative To:",
        description="Reference location to align to",
        items=(
            ('OPT_1', "Scene Origin", "Use the Scene Origin as the position for the selected objects to align to"),
            ('OPT_2', "3D Cursor", "Use the 3D cursor as the position for the selected objects to align to"),
            ('OPT_3', "Selection", "Use the selected objects as the position for the selected objects to align to"),
            ('OPT_4', "Active", "Use the active object as the position for the selected objects to align to"),
        ),
        default='OPT_4',
    )
    align_axis: EnumProperty(
        name="Align",
        description="Align on axis",
        items=(
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ),
        options={'ENUM_FLAG'},
        default= {'X', 'Y', 'Z'},
    )
    rotation_axis: EnumProperty(
        name="Rotation",
        description="Align rotation on axis",
        items=(
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ),
        options={'ENUM_FLAG'},
    )
    scale_axis: EnumProperty(
        name="Scale",
        description="Align scale on axis",
        items=(
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ),
        options={'ENUM_FLAG'},
    )

    raycast = False
    target = ""
    

    # Get name of the object under the mouse, if nothing is under it will return 'World'
    def mouse_raycast(self, context, event):
        region = context.region
        rv3d = context.region_data
        coord = event.mouse_region_x, event.mouse_region_y

        if not all((region, coord, rv3d)):
            return 'World'

        view_vector = region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin = region_2d_to_origin_3d(region, rv3d, coord, clamp=20)
        ray_target = None
        ray_target = ray_origin + (view_vector * 1000)
        ray_target.normalized()

        result, location, normal, index, object, matrix = context.scene.ray_cast(context.view_layer.depsgraph,
                                                                                 ray_origin,
                                                                                 ray_target)
        
        
        if bpy.context.mode == 'OBJECT':
            if result and not object.select_get():
                return object.name
    
        return 'World'

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 0

    def execute(self, context):

        target_rotation = Vector((0.0, 0.0, 0.0))
        target_scale = Vector((1.0, 1.0, 1.0))

        # Change mode if target is World
        if self.target == 'World':
            self.relative_to = 'OPT_1'

            target_rotation.x = 0.0
            target_rotation.y = 0.0
            target_rotation.z = 0.0

            target_scale.x = 1.0
            target_scale.y = 1.0
            target_scale.z = 1.0

        else:
            self.relative_to = 'OPT_4'

            target_rotation = bpy.data.objects[self.target].rotation_euler
            target_scale = bpy.data.objects[self.target].scale

            itools.select(self.target, item=False)
            itools.active_set(self.target, item=False)

        # Use default align operator to handle alignment
        bpy.ops.object.align(bb_quality=self.bb_quality, align_mode=self.align_mode,
                             relative_to=self.relative_to, align_axis=self.align_axis)

        # Extend align operator
        for obj in self.selected:
            if 'X' in self.rotation_axis:
                bpy.data.objects[obj].rotation_euler.x = target_rotation.x

            if 'Y' in self.rotation_axis:
                bpy.data.objects[obj].rotation_euler.y = target_rotation.y

            if 'Z' in self.rotation_axis:
                bpy.data.objects[obj].rotation_euler.z = target_rotation.z

            if 'X' in self.scale_axis:
                bpy.data.objects[obj].scale.x = target_scale.x

            if 'Y' in self.scale_axis:
                bpy.data.objects[obj].scale.y = target_scale.y

            if 'Z' in self.scale_axis:
                bpy.data.objects[obj].scale.z = target_scale.z

        # Deselect Target
        if self.target != 'World':
            itools.select(self.target, item=False, deselect=True)

            # Make first selected object active again
            for obj in self.selected:
                itools.active_set(obj, item=False)

        return {'FINISHED'}

    def invoke(self, context, event):
        # self.align_axis = {'X', 'Y', 'Z'}
        self.selected = itools.get_selected('OBJECT', item=False)
        self.target = self.mouse_raycast(context, event)

        return self.execute(context)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row1 = col.row()
        row1.label(text="High Quality")
        row1.prop(self, "bb_quality", text="")

        row2 = col.row()
        row2.label(text="Align Mode")
        row2.prop(self, "align_mode", text="")

        row3 = col.row()
        row3.label(text="Relative To")
        row3.prop(self, "relative_to", text="")

        row4 = col.row()
        row4.label(text="Location")
        row4.prop(self, "align_axis")

        row5 = col.row()
        row5.label(text="Rotation")
        row5.prop(self, "rotation_axis")

        row6 = col.row()
        row6.label(text="Scale")
        row6.prop(self, "scale_axis")
