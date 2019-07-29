import bpy
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d
from bpy.props import BoolProperty, EnumProperty
from mathutils import Vector
from .. utils import itools as itools


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
                mode = itools.get_mode()
                selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))

                if mode == 'VERT':
                    verts = itools.get_selected()

                elif mode == 'EDGE':
                    edges = itools.get_selected()
                    verts = [edge.verts for edge in edges]
                    verts = [vert for vert_pair in verts for vert in vert_pair]
                    verts = list(set(verts))

                elif mode == 'FACE':
                    faces = itools.get_selected()
                    verts = [face.verts for face in faces]
                    verts = [vert for vert_pair in verts for vert in vert_pair]
                    verts = list(set(verts))

                vert_indexes = [vert.index for vert in verts]
                vert_positions = [(selection.matrix_world @ vert.co) for vert in verts]

                # Make vertex group, assign verts and update viewlayer
                itools.set_mode('OBJECT')
                vg = selection.vertex_groups.new(name="lattice_group")
                vg.add(vert_indexes, 1.0, 'ADD')
                bpy.context.view_layer.update()
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

            # Make sure no axis is 0 as this caused the bug where you couldnt move the lattice.
            for axis in range(3):
                print(axis)
                if dimensions[axis] == 0:
                    dimensions[axis] = 0.001

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

    @classmethod
    def poll(cls, context):
        mode = itools.get_mode()
        cond_a = mode in ['VERT', 'EDGE', 'FACE'] and len(itools.get_selected()) > 0
        cond_b = mode == 'OBJECT' and len(context.selected_objects) == 1

        if len(context.selected_objects) > 0:
            cond_c = context.selected_objects[0].type == 'LATTICE'

        else:
            cond_c = False

        return cond_a or cond_b or cond_c

    def execute(self, context):
        selection = bpy.context.active_object
        if selection.name.endswith(".Lattice"):
            self.apply_lattice(context, selection)
        elif self.get_lattice(context, selection):
            lattice = bpy.context.active_object
        else:
            self.setup_lattice(context, selection)
        return{'FINISHED'}
