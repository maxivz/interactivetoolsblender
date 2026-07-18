import bpy

def get_itools_data_obj():
    obj_name = "Itools_data_obj"
    # Check if the data object exists, make it if it doesnt
    if obj_name not in bpy.data.objects:
        obj = bpy.data.objects.new(obj_name, None)
        obj.use_fake_user = True
        
    return bpy.data.objects[obj_name]

def itools_data_get(data_key):
    """Looks for itools data on data obj, if it doesnt find it returns nothing"""
    itools_data_obj = get_itools_data_obj()

    return itools_data_obj.get(data_key, None)

def itools_data_set(data_key, value):
    """Sets data in itools data obj"""
    itools_data_obj = get_itools_data_obj()
    itools_data_obj[data_key] = value
    itools_data_obj.update_tag()

class ToggleItoolsProperty(bpy.types.Operator):
    """Toggles target property"""
    bl_idname = "itools.toggle_property"
    bl_label = ""

    prop_name: bpy.props.StringProperty()
    description: bpy.props.StringProperty(default="Toggles Property")

    @classmethod
    def description(cls, context, properties):
        return properties.description
    
    def execute(self, context):
        prop_value = itools_data_get(self.prop_name)
        print(prop_value)
        if prop_value:
            itools_data_set(self.prop_name, not prop_value)

        else:
            itools_data_set(self.prop_name, True)
            
        return {'FINISHED'}