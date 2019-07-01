import bpy

class QuickFFD(bpy.types.Operator):
    bl_idname = "mesh.quick_ffd"
    bl_label = "Quick FFD"
    bl_description = "Setup a Quick FFD"
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

    def setup_ffd(self, context, selection):
        if selection is not []:
            if context.mode == 'OBJECT':
                verts = selection.data.vertices
                vert_positions = [vert.co @ selection.matrix_world for vert in verts] 
                rotation = bpy.data.objects[selection.name].rotation_euler
            elif context.mode == 'EDIT_MESH':
                bmesh = get_bmesh()
                minimum = Vector()
                maximum = Vector()
                selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
                if selectionMode[0]:
                    verts = get_selected(verts=True, get_item = True)
                elif selectionMode[1]:
                    edges = get_selected(edges=True, get_item = True)
                    verts = [edge.verts for edge in edges]
                    verts = [vert for vert_pair in verts for vert in vert_pair]
                    verts = list(set(verts))
                elif selectionMode[2]:
                    faces = get_selected(faces=True, get_item = True)
                    verts = [face.verts for face in faces]
                    verts = [vert for vert_pair in verts for vert in vert_pair]
                    verts = list(set(verts))
                vert_positions = [(selection.matrix_world @ vert.co) for vert in verts]
                #Make vertex group
                selection.vertex_groups.new(name = "ffd_group")
                bpy.ops.object.vertex_group_assign()
                rotation = Vector()
                bpy.ops.object.editmode_toggle()
            #calculate positions
            minimum = Vector()
            maximum = Vector()
            for axis in range(3):
                poslist = [pos[axis] for pos in vert_positions]
                maximum[axis] = max(poslist)
                minimum[axis] = min(poslist)
            location = (maximum + minimum) / 2 
            dimensions = maximum - minimum
            #add lattice			
            bpy.ops.object.add(type='LATTICE', enter_editmode=False, location=(0, 0, 0))
            ffd = bpy.context.active_object
            ffd.data.use_outside = True
            ffd.name = selection.name + ".Lattice"
            ffd.data.interpolation_type_u = 'KEY_LINEAR'
            ffd.data.interpolation_type_v = 'KEY_LINEAR'
            ffd.data.interpolation_type_w = 'KEY_LINEAR'
            ffd.location = location
            ffd.scale = dimensions
            ffd.rotation_euler = rotation
            bpy.context.view_layer.objects.active = selection
            bpy.ops.object.modifier_add(type='LATTICE')
            selection.modifiers["Lattice"].object = ffd
            selection.modifiers["Lattice"].vertex_group = "ffd_group"
            bpy.context.view_layer.objects.active = ffd
            #Deselect obj, select FFD and make it active, switch to edit mode
            bpy.data.objects[selection.name].select_set(False)
            bpy.data.objects[ffd.name].select_set(True)
            bpy.ops.object.editmode_toggle()

    def apply_ffd(self, context, ffd):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        obj = bpy.data.objects[ffd.name[:-8]]
        bpy.data.objects[ffd.name].select_set(False)
        bpy.data.objects[obj.name].select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Lattice")
        #Delete vertex group
        vg = obj.vertex_groups.get("ffd_group")
        if vg is not None:
            obj.vertex_groups.remove(vg)
        #Delete lattice
        bpy.data.objects[obj.name].select_set(False)
        bpy.data.objects[ffd.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.editmode_toggle()

    def get_ffd(self,context, obj):
        ffd = obj.name + ".Lattice"
        if bpy.data.objects.get(ffd) is None:
            return False
        else:
            bpy.data.objects[obj.name].select_set(False)
            bpy.data.objects[ffd].select_set(True)
            context.view_layer.objects.active = bpy.data.objects[ffd]
            bpy.ops.object.editmode_toggle()
            return True

    def execute(self, context):
        selection = bpy.context.active_object
        if selection.name.endswith(".Lattice"):
            self.apply_ffd(context, selection)
        elif self.get_ffd(context, selection):
            ffd = bpy.context.active_object
        else:
            self.setup_ffd(context, selection)
        return{'FINISHED'}