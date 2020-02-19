import bpy
from bpy.types import Menu
from .. utils.user_prefs import get_qblocker_active, get_ssc_qblocker_integration, get_ssc_bezierutilities_integration, get_set_flow_active, get_bezierutilities_active, get_loop_tools_active, get_textools_active


class VIEW3D_MT_PIE_SSC_Duplicate(Menu):
    # bl_idname = "mesh.ssc_duplicate_menu"
    bl_label = "Object Duplication"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("object.duplicate", text="Duplicate")
        # 6 - RIGHT
        pie.operator("object.duplicate", text="Duplicate Linked").linked = True
        # 2 - BOTTOM

        # 8 - TOP

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT


class VIEW3D_MT_PIE_SSC_New_Obj(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Object Creation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        qblocker = get_qblocker_active() and get_ssc_qblocker_integration()
        bezierutils = get_bezierutilities_active() and get_ssc_bezierutilities_integration()

        # 4 - LEFT
        if bezierutils:
            submenu = pie.column()
            container = submenu.box()
            column = container.column()
            row = column.row(align = True)
            row.operator("curve.primitive_bezier_curve_add", text="Curve", icon="IPO_EASE_IN")
            row.operator("curve.flexitool_create", text="Curve Flexitools", icon="IPO_EASE_IN")

        else:
            pie.operator("curve.primitive_bezier_curve_add", text="Add Curve", icon="IPO_EASE_IN")
        # 6 - RIGHT

        if qblocker:
            submenu = pie.column()
            container = submenu.box()
            column = container.column()
            row = column.row(align=True)
            row.operator("mesh.primitive_cube_add", text="Cube", icon="MESH_CUBE")
            row.operator("object.box_create", text="Cube QBlocker", icon="MESH_CUBE")

        else:
            pie.operator("mesh.primitive_cube_add", text="Cube", icon="MESH_CUBE")

        # 2 - BOTTOM
        if qblocker:
            submenu = pie.column()
            container = submenu.box()
            column = container.column()
            row = column.row(align=True)
            row.operator("mesh.primitive_cylinder_add", text="Cylinder", icon="MESH_CYLINDER")
            row.operator("object.cylinder_create", text="Cylinder QBlocker", icon="MESH_CYLINDER")

        else:
            pie.operator("mesh.primitive_cylinder_add", text="Cylinder", icon="MESH_CYLINDER")

        # 8 - TOP
        if qblocker:
            submenu = pie.column()
            container = submenu.box()
            column = container.column()
            row = column.row(align=True)
            row.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon="MESH_UVSPHERE")
            row.operator("object.sphere_create", text="Sphere QBlocker", icon="MESH_UVSPHERE")

        else:
            pie.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon="MESH_UVSPHERE")

        # 7 - TOP - LEFT
        pie.operator("object.light_add", text="Light", icon="OUTLINER_OB_LIGHT").type = 'POINT'

        # 9 - TOP - RIGHT
        pie.operator("object.camera_add", text="Camera", icon="OUTLINER_OB_CAMERA")
        # 1 - BOTTOM - LEFT
        pie.operator("object.gpencil_add", text="Gpencil", icon="OUTLINER_OB_GREASEPENCIL").type = 'EMPTY'

        # 3 - BOTTOM - RIGHT
        pie.operator("object.empty_add", text="Empty", icon="OUTLINER_OB_EMPTY").type = 'PLAIN_AXES'


class VIEW3D_MT_PIE_SM_object(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.quick_lattice", text="Quick Lattice")

        # 6 - RIGHT
        pie.operator("mesh.radial_symmetry", text="Radial Symmetry")

        # 2 - BOTTOM
        pie.operator("mesh.rebase_cylinder", text="Rebase Cylinder")

        # 8 - TOP
        pie.operator("object.convert", text="Visual Geo To Mesh").target='MESH'

        # 7 - TOP - LEFT
        # Align World Submenu
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align=True)
        op = row.operator("mesh.quick_align", text="Align World")
        op.relative_to = 'OPT_1'
        op.align_axis = {'X', 'Y', 'Z'}

        row = column.row(align=True)
        op = row.operator("mesh.quick_align", text="X")
        op.relative_to = 'OPT_1'
        op.align_axis = {'X'}

        op = row.operator("mesh.quick_align", text="Y")
        op.relative_to = 'OPT_1'
        op.align_axis = {'Y'}

        op = row.operator("mesh.quick_align", text="Z")
        op.relative_to = 'OPT_1'
        op.align_axis = {'Z'}

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT


class VIEW3D_MT_PIE_SM_lattice(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.lattice_resolution_2x2x2", text="Resolution 2x2x2")

        # 6 - RIGHT
        pie.operator("mesh.lattice_resolution_4x4x4", text="Resolution 4x4x4")

        # 2 - BOTTOM
        pie.operator("mesh.lattice_resolution_3x3x3", text="Resolution 3x3x3")

        # 8 - TOP
        pie.operator("mesh.quick_lattice", text="Apply Lattice")


class VIEW3D_MT_PIE_SM_curve(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("curve.normals_make_consistent", text="Recalc Normal")

        # 6 - RIGHT
        pie.operator("curve.subdivide", text="Subdivide")

        # 2 - BOTTOM
        submenu = pie.column()
        container = submenu.box()
        column = container.column()

        row = column.row(align=True)
        row.label(text="Set Spline Type...")
        row = column.row(align=True)

        row.operator("curve.handle_type_set", text="Automatic").type = 'AUTOMATIC'
        row.operator("curve.handle_type_set", text="Vector").type = 'VECTOR'

        row = column.row(align=True)
        row.operator("curve.handle_type_set", text="Aligned").type = 'ALIGNED'
        row.operator("curve.handle_type_set", text="Free Align").type = 'FREE_ALIGN'

        row = column.row(align=True)
        row.operator("curve.handle_type_set", text="Toggle Free/Align").type = 'TOGGLE_FREE_ALIGN'

        # 8 - TOP
        submenu = pie.column()
        container = submenu.box()
        column = container.column()

        row = column.row(align=True)
        row.label(text="Set Spline Type...")
        row = column.row(align=True)

        row.operator("curve.spline_type_set", text="Poly").type = 'POLY'
        row.operator("curve.spline_type_set", text="Bezier").type = 'BEZIER'
        row.operator("curve.spline_type_set", text="Nurbs").type = 'NURBS'


class VIEW3D_MT_PIE_SM_uv(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        submenu = pie.column()
        container = submenu.box()

        column = container.column()
        row = column.row(align=True)
        row.operator("uv.textools_island_align_edge", text="Align Edge", icon="MOD_EDGESPLIT")
        row = column.row(align=True)
        row.operator("uv.textools_island_align_world", text="Align World", icon="WORLD_DATA")


        # 6 - RIGHT
        pie.operator("uv.textools_rectify", text="Rectify", icon="UV_FACESEL")

        # 2 - BOTTOM
        submenu = pie.column()
        container = submenu.box()
        column = container.column()

        row = column.row(align=True)
        row.label(text="Seams From...")

        row = column.row(align=True)
        row.operator("uv.seams_from_islands", text="Islands")

        row.operator("uv.seams_from_sharps", text="Sharps")

        # 8 - TOP
        submenu = pie.column()
        container = submenu.box()
        column = container.column()

        row = column.row(align=True)
        row.operator("uv.textools_island_rotate_90", text="Rotate -90", icon="LOOP_BACK").angle = -1.5708
        row.operator("uv.textools_align", text="Align Top", icon="TRIA_UP").direction = "top"
        row.operator("uv.textools_island_rotate_90", text="Rotate +90", icon="LOOP_FORWARDS").angle = 1.5708

        row = column.row(align=True)
        row.operator("uv.textools_align", text="Align Left", icon="TRIA_LEFT").direction = "left"
        row.operator("uv.textools_align", text="Align Bottom", icon="TRIA_DOWN").direction = "bottom"
        row.operator("uv.textools_align", text="Align Right", icon="TRIA_RIGHT").direction = "right"

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT


class VIEW3D_MT_PIE_SM_mesh(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Smart Modify"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT

        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align=True)
        row.operator("mesh.quick_flatten", text="Flatten Avg Normal").mode = 1

        row = column.row(align=True)
        # row.label(text="Global")
        row.operator("mesh.quick_flatten", text="X").mode = 2
        row.operator("mesh.quick_flatten", text="Y").mode = 3
        row.operator("mesh.quick_flatten", text="Z").mode = 4

        # 6 - RIGHT
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align=True)
        row.operator("mesh.quick_lattice", text="Quick Lattice")

        row = column.row(align=True)
        row.operator("mesh.quick_pipe", text="Quick Pipe")


        # 2 - BOTTOM
        # Flow Submenu
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        if get_loop_tools_active():
            row = column.row(align=True)
            row.operator("mesh.looptools_circle", text="Make Circle")

        if get_set_flow_active():
            op = row.operator("mesh.set_edge_flow", text="Set Flow")
            op.tension = 180
            op.iterations = 1

        if get_loop_tools_active():
            row.operator("mesh.looptools_space", text="Space")
            row = column.row(align=True)

            row.operator("mesh.looptools_curve", text="Make Curve")
            row.operator("mesh.looptools_relax", text="Relax")

        # 8 - TOP
        pie.operator("mesh.quick_visual_geo_to_mesh", text="Visual Geo To Mesh")

        # 7 - TOP - LEFT
        pie.operator("mesh.flip_normals", text="Flip Normal")

        # 9 - TOP - RIGHT
        pie.operator("mesh.rebase_cylinder", text="Rebase Cylinder")
        # 1 - BOTTOM - LEFT

        # 3 - BOTTOM - RIGHT

        # Align World Submenu
        """
        submenu = pie.column()
        container = submenu.box()
        column = container.column()
        row = column.row(align = True)
        op = row.operator("mesh.quick_align", text="Align World")
        op.relative_to = 'OPT_1'
        op.align_axis = {'X', 'Y', 'Z'}

        row = column.row(align = True)
        op = row.operator("mesh.quick_align", text="X")
        op.relative_to = 'OPT_1'
        op.align_axis = {'X'}

        op = row.operator("mesh.quick_align", text="Y")
        op.relative_to = 'OPT_1'
        op.align_axis = {'Y'}

        op = row.operator("mesh.quick_align", text="Z")
        op.relative_to = 'OPT_1'
        op.align_axis = {'Z'}
        """
        # Flatten Submenu


        '''
        TO Do: Local Alignment

        row = column.row(align = True)
        row.label(text="Local  ")
        row.operator("mesh.quick_flatten", text = "X").mode = 2
        row.operator("mesh.quick_flatten", text = "Y").mode = 3
        row.operator("mesh.quick_flatten", text = "Z").mode = 4
        '''


class VIEW3D_MT_PIE_SM_looptools(Menu):
    # bl_idname = "mesh.ssc_new_obj_menu"
    bl_label = "Loop Tools"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.looptools_circle", text="Make Circle")
        # 6 - RIGHT
        pie.operator("mesh.looptools_flatten", text="Flatten")

        # 2 - BOTTOM
        pie.operator("mesh.looptools_curve", text="Make Curve")

        # 8 - TOP
        if get_set_flow_active():
            op4 = pie.operator("mesh.set_edge_flow", text="Set Flow")
            op4.tension = 180
            op4.iterations = 1

        # 7 - TOP - LEFT
        pie.operator("mesh.looptools_relax", text="Relax")

        # 9 - TOP - RIGHT
        pie.operator("mesh.looptools_space", text="Space")


class VIEW3D_MT_PIE_QTO(Menu):
    bl_label = "Transform Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("mesh.transform_orientation_op", text="Set Custom 2", icon='TRIA_DOWN').mode = 2

        # 6 - RIGHT
        pie.operator("mesh.transform_orientation_op", text="Use Custom 2", icon='TRIA_UP').mode = 5

        # 2 - BOTTOM
        pie.operator("mesh.transform_orientation_op", text="Reset Working Pivot", icon='FILE_REFRESH').mode = 7
        # 8 - TOP
        menu = pie.row()
        draw_orientations_submenu(menu)

        # 7 - TOP - LEFT
        pie.operator("mesh.transform_orientation_op", text="Set Custom 1", icon='TRIA_DOWN').mode = 1

        # 9 - TOP - RIGHT
        pie.operator("mesh.transform_orientation_op", text="Use Custom 1", icon='TRIA_UP').mode = 4

        # 1 - BOTTOM - LEFT
        pie.operator("mesh.transform_orientation_op", text="Set Custom 3", icon='TRIA_DOWN').mode = 3

        # 3 - BOTTOM - RIGHT
        pie.operator("mesh.transform_orientation_op", text="Use Custom 3", icon='TRIA_UP').mode = 6


def draw_orientations_submenu(ui_space):
    submenu = ui_space.column()
    container = submenu.box()
    column = container.column()

    row = column.row(align=True)
    row.label(text="Default Orientations")
    row = column.row(align=True)
    row.operator("mesh.transform_orientation_op", text="Global", icon="ORIENTATION_GLOBAL").mode = 8
    row.operator("mesh.transform_orientation_op", text="Local", icon="ORIENTATION_LOCAL").mode = 9
    row.operator("mesh.transform_orientation_op", text="Cursor", icon="ORIENTATION_CURSOR").mode = 13

    row = column.row(align=True)
    row.operator("mesh.transform_orientation_op", text="Normal", icon="ORIENTATION_NORMAL").mode = 10
    row.operator("mesh.transform_orientation_op", text="View", icon="ORIENTATION_VIEW").mode = 12
    row.operator("mesh.transform_orientation_op", text="Gimbal", icon="ORIENTATION_GIMBAL").mode = 11


def draw_snap_submenu(ui_space):
    submenu = ui_space.column()
    container = submenu.box()
    column = container.column()

    row = column.row(align=True)
    row.label(text="Default Orientations")
    row = column.row(align=True)
    row.operator("mesh.transform_orientation_pie", text="Global", icon="ORIENTATION_GLOBAL").mode = 8
    row.operator("mesh.transform_orientation_pie", text="Local", icon="ORIENTATION_LOCAL").mode = 9

    row = column.row(align=True)
    row.operator("mesh.transform_orientation_pie", text="Global", icon="ORIENTATION_GLOBAL").mode = 8
    row.operator("mesh.transform_orientation_pie", text="Local", icon="ORIENTATION_LOCAL").mode = 9


class VIEW3D_MT_PIE_TransformOptions(Menu):
    bl_label = "Transform Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        draw_orientations_submenu(pie)

        # 6 - RIGHT
        pie.operator("mesh.transform_orientation_pie", text="Pivot").mode = 5

        # 2 - BOTTOM
        pie.operator("mesh.transform_orientation_pie", text="Snap").mode = 7

        # 8 - TOP
        pie.operator("mesh.transform_orientation_pie", text="Proportional Editing").mode = 7


class VIEW3D_MT_PIE_QSP(Menu):
    bl_label = "Snap Presets"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        op = pie.operator("mesh.snap_presets_op", text="Vert Closest", icon="SNAP_VERTEX").mode = 3

        # 6 - RIGHT
        pie.operator("mesh.snap_presets_op", text="Vert Center", icon="SNAP_VERTEX").mode = 2

        # 2 - BOTTOM
        pie.operator("mesh.snap_presets_op", text="Face Normal", icon="SNAP_FACE").mode = 4

        # 8 - TOP
        pie.operator("mesh.snap_presets_op", text="Grid Absolute", icon="SNAP_INCREMENT").mode = 1


class VIEW_MT_PIE_PropEdit(Menu):
    bl_label = "Prop Edit"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()


        if bpy.context.scene.tool_settings.use_proportional_connected:
            pie.operator("mesh.prop_edit_op", text="Connected Only", icon = "PROP_ON", depress=True).mode = 10
        else:
            pie.operator("mesh.prop_edit_op", text="Connected Only", icon = "PROP_OFF").mode = 10

        if bpy.context.scene.tool_settings.use_proportional_projected:
            pie.operator("mesh.prop_edit_op", text="Projected", icon = "PROP_ON", depress=True).mode = 11
        else:
            pie.operator("mesh.prop_edit_op", text="Projected", icon = "PROP_OFF").mode = 11

        if bpy.context.scene.tool_settings.use_proportional_edit:
            pie.operator("mesh.prop_edit_op", text="Proportional Edit", icon = "PROP_ON", depress=True).mode = 9
        else:
            pie.operator("mesh.prop_edit_op", text="Proportional Edit", icon = "PROP_OFF").mode = 9

        submenu = pie.column()
        container = submenu.box()
        column = container.column()

        row = column.row(align=False)
        row.label(text="Falloffs")
        row = column.row(align=True)
        row.operator("mesh.prop_edit_op", text="Smooth", icon = "SMOOTHCURVE").mode = 1
        row.operator("mesh.prop_edit_op", text="Sphere", icon = "SPHERECURVE").mode = 2
        row.operator("mesh.prop_edit_op", text="Root", icon = "ROOTCURVE").mode = 3

        row = column.row(align=True)
        row.operator("mesh.prop_edit_op", text="Inverse Square", icon = "INVERSESQUARECURVE").mode = 4
        row.operator("mesh.prop_edit_op", text="Sharp", icon = "SHARPCURVE").mode = 5
        row.operator("mesh.prop_edit_op", text="Linear", icon = "LINCURVE").mode = 6

        row = column.row(align=True)
        row.operator("mesh.prop_edit_op", text="Constant", icon = "NOCURVE").mode = 7
        row.operator("mesh.prop_edit_op", text="Random", icon = "RNDCURVE").mode = 8
