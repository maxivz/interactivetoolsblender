import bpy

ITOOLS_DATA = "Itools_data"

def scene_get(scene_name):
	"""Creates target scene"""
	target_scene = bpy.data.scenes.get(scene_name)

	if not target_scene:
		target_scene = bpy.data.scenes.new(scene_name)
		
	return target_scene

