import bpy

class AddBezierEmpty(bpy.types.Operator):
    bl_idname = "curve.add_bezier_empty"
    bl_label = "Add Bezier Empty"
    bl_description = "Adds Empty Bezier Curve and sets its as active"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        curve_data = bpy.data.curves.new('BezierCurve', 'CURVE')
        curve_data.dimensions = '3D'  
        curve_data.splines.new('BEZIER')

        curve_object = bpy.data.objects.new('BezierCurve', curve_data)

        # Link the object to the scene and set active
        bpy.context.collection.objects.link(curve_object)
        bpy.context.view_layer.objects.active = curve_object

        return{'FINISHED'}
