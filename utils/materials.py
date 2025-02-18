import bpy

def get_material(material_name):
    """Get material by material name, if it doesnt exist create it"""
    mat = bpy.data.materials.get(material_name)
    if not mat:
        mat = bpy.data.materials.new(name=material_name)
    return mat