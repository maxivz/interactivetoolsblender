import bpy
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from bpy.props import BoolProperty, EnumProperty
from mathutils import Vector
from .. utils import itools as itools


class QuickAlign(bpy.types.Operator):
    bl_idname = "itools.quick_align"
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


class QuickLattice(bpy.types.Operator):
    bl_idname = "mesh.quick_lattice"
    bl_label = "Quick Lattice"
    bl_description = "Setup a Quick Lattice"
    bl_options = {'REGISTER', 'UNDO'}

    mouseX = 0.0
    initial_pos_x = 0.0
    sym_count = 0.0
    sym_axis = 0
    initial_sym_axis = 0
    initial_sym_count = 0
    offset_obj = "Empty"
    selection = "Empty"
    senitivity = 0.01
    modkey = 0

    def setup_lattice(self, context, selection):
        if selection is not []:
            if context.mode == 'OBJECT':
                verts = selection.data.vertices
                vert_positions = [vert.co @ selection.matrix_world for vert in verts] 
                rotation = bpy.data.objects[selection.name].rotation_euler

            elif context.mode == 'EDIT_MESH':
                bmesh = itools.get_bmesh()
                minimum = Vector()
                maximum = Vector()
                selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))

                if selectionMode[0]:
                    verts = itools.get_selected('VERT')

                elif selectionMode[1]:
                    edges = itools.get_selected('EDGE')
                    verts = [edge.verts for edge in edges]
                    verts = [vert for vert_pair in verts for vert in vert_pair]
                    verts = list(set(verts))

                elif selectionMode[2]:
                    faces = itools.get_selected('FACE')
                    verts = [face.verts for face in faces]
                    verts = [vert for vert_pair in verts for vert in vert_pair]
                    verts = list(set(verts))

                vert_positions = [(selection.matrix_world @ vert.co) for vert in verts]

                # Make vertex group, assign verts and update viewlayer
                vg = selection.vertex_groups.new(name="lattice_group")
                vert_indexes = [vert.index for vert in verts]
                bpy.ops.object.editmode_toggle()
                vg.add(vert_indexes, 1.0, 'ADD')
                bpy.context.view_layer.update()
                bpy.ops.object.editmode_toggle()
                rotation = Vector()

            # Calculate positions
            minimum = Vector()
            maximum = Vector()

            for axis in range(3):
                poslist = [pos[axis] for pos in vert_positions]
                maximum[axis] = max(poslist)
                minimum[axis] = min(poslist)

            location = (maximum + minimum) / 2
            dimensions = maximum - minimum

            # Add Lattice
            bpy.ops.object.add(type='LATTICE', enter_editmode=False, location=(0, 0, 0))
            lattice = bpy.context.active_object
            lattice.data.use_outside = True
            lattice.name = selection.name + ".Lattice"
            lattice.data.interpolation_type_u = 'KEY_LINEAR'
            lattice.data.interpolation_type_v = 'KEY_LINEAR'
            lattice.data.interpolation_type_w = 'KEY_LINEAR'
            lattice.location = location
            lattice.scale = dimensions
            lattice.rotation_euler = rotation

            bpy.context.view_layer.objects.active = selection
            mod = selection.modifiers.new(name="Lattice", type='LATTICE')
            mod.object = lattice
            mod.vertex_group = "lattice_group"
            bpy.context.view_layer.objects.active = lattice

            # Deselect obj, select lattice and make it active, switch to edit mode
            bpy.data.objects[selection.name].select_set(False)
            bpy.data.objects[lattice.name].select_set(True)
            bpy.ops.object.editmode_toggle()

    def apply_lattice(self, context, lattice):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        obj = bpy.data.objects[lattice.name[:-8]]
        bpy.data.objects[lattice.name].select_set(False)
        bpy.data.objects[obj.name].select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Lattice")

        # Delete vertex group
        vg = obj.vertex_groups.get("lattice")
        if vg is not None:
            obj.vertex_groups.remove(vg)

        # Delete lattice
        bpy.data.objects[obj.name].select_set(False)
        bpy.data.objects[lattice.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.editmode_toggle()

    def get_lattice(self, context, obj):
        lattice = obj.name + ".Lattice"
        if bpy.data.objects.get(lattice) is None:
            return False
        else:
            bpy.data.objects[obj.name].select_set(False)
            bpy.data.objects[lattice].select_set(True)
            context.view_layer.objects.active = bpy.data.objects[lattice]
            bpy.ops.object.editmode_toggle()
            return True
    """
    @classmethod
    def poll(cls, context):
        len(context.selected_objects) == 1
     """   

    def execute(self, context):
        selection = bpy.context.active_object
        if selection.name.endswith(".Lattice"):
            self.apply_lattice(context, selection)
        elif self.get_lattice(context, selection):
            lattice = bpy.context.active_object
        else:
            self.setup_lattice(context, selection)
        return{'FINISHED'}

    """
    def invoke(self, context, event):
        self.align_axis = {'X', 'Y', 'Z'}
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

    """