import bpy

class AddBezierSimple(bpy.types.Operator):
    bl_idname = "curve.add_bezier_simple"
    bl_label = "Add Bezier Simple"
    bl_description = "Adds Simple Bezier Curve and sets its as active"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.StringProperty(default="Simple")
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        curve_data = bpy.data.curves.new('BezierCurve', 'CURVE')
        curve_data.dimensions = '3D'  

        if self.mode == "Simple":
            spline = curve_data.splines.new('BEZIER')
            spline.bezier_points.add(1)
            spline.bezier_points[0].co = (0, 0, 0)  
            spline.bezier_points[1].co = (0, 0, 1)  

        curve_object = bpy.data.objects.new('BezierCurve', curve_data)
        curve_object.location = context.scene.cursor.location

        # Link the object to the scene and set active
        context.collection.objects.link(curve_object)
        context.view_layer.objects.active = curve_object
        curve_object.select_set(True)


        if self.mode == "Draw":
            if context.mode == "OBJECT":
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.wm.tool_set_by_id(name="builtin.draw")
                context.scene.tool_settings.curve_paint_settings.depth_mode = "SURFACE"

        return{'FINISHED'}
