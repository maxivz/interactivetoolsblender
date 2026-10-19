import bpy
import random
from mathutils import Matrix
from .. utils.itools import get_collection_top_level_parent
from .. utils.custom_data import itools_data_get
from ..utils.constants import (COLLECTION_COLOR, COLLECTION_COLORS_USE_PARENT_COLOR,
							COLLECTION_COLORS_FORCE_RANDOM, ORIGIN, WORLD_ALIGNED,
							WORLD_ALIGNED_INSTANCE, DIRECT_CHILDREN, ASSAMBLY_INSTANCE,
							ASSAMBLY, ASSAMBLY_SCENE, COL_TYPE, COL_TAGS)
from ..utils.scenes import scene_get, ITOOLS_DATA
def collection_color_get(collection):
	"""Returns the color of a collection, if it has a tag it uses that one, if it doesnt it assigns one"""
	if collection is None:
		return (1, 1, 1, 1) 

	if not collection.get(COLLECTION_COLOR):
		collection[COLLECTION_COLOR] = (random.random(), random.random(), random.random(), 1)

	if itools_data_get(COLLECTION_COLORS_FORCE_RANDOM):
		return collection[COLLECTION_COLOR]
	
	if itools_data_get(COLLECTION_COLORS_USE_PARENT_COLOR):
		parent_collection = get_collection_top_level_parent(collection)
		if parent_collection: 
			return collection_color_get(parent_collection)
		

	if collection.color_tag != 'NONE':
		color_map = {
			'COLOR_01': (1.0, 0.0, 0.0, 1.0),
			'COLOR_02': (1.0, 0.7, 0.4, 1.0),
			'COLOR_03': (1.0, 0.95, 0.5, 1.0),
			'COLOR_04': (0.48, 0.8, 0.48, 1.0),
			'COLOR_05': (0.36, 0.71, 0.91, 1.0),
			'COLOR_06': (0.55, 0.35, 0.85, 1.0),
			'COLOR_07': (0.77, 0.45, 0.72, 1.0),
			'COLOR_08': (0.47, 0.33, 0.25, 1.0),
		}
		
		return color_map.get(collection.color_tag, 1)

	return collection[COLLECTION_COLOR]

def collection_colors_assign_to_objects():
	"""Assigns viewport display colors to objects based on their collections."""
	for obj in bpy.data.objects:
		if obj.type not in {'MESH', 'CURVE'}:
			continue  

		collection = next((col for col in bpy.data.collections if obj.name in col.objects), None)
		if collection:
			color = collection_color_get(collection)
			obj.color = color



def active_obj_collection_list_generate(self, context):
	"""Returns a list of collection that the active object belong to as an Enum Property"""
	items = []

	active_obj = bpy.context.view_layer.objects.active
	if active_obj is None:
		return items

	collections = [col for col in bpy.data.collections if active_obj.name in col.objects]

	if collections:
		for col in collections:
			items.append((col.name, col.name, f"{col.name}"))

	else:
		items.append(("NONE", "No Collections Found", "No Collections Found"))

	return items

def active_obj_collections_amountr(context):
	"""Returns the number of collections that the active object belong to"""
	active_obj = bpy.context.view_layer.objects.active
	if active_obj is None:
		return 0

	collections = [col for col in bpy.data.collections if active_obj.name in col.objects]

	if not collections:
		return 0
	
	return len(collections)


def layer_collection_get(col, _layer_collection=None):
	"""Returns layer collection for target col"""
	if _layer_collection is None:
		_layer_collection = bpy.context.view_layer.layer_collection
	if _layer_collection.name == col.name:
		return _layer_collection
	else:
		for l_col in _layer_collection.children:
			if rez := layer_collection_get(col, _layer_collection=l_col):
				return rez

def collection_active_get():
	"""Gets active viewlayer collection"""
	return bpy.context.view_layer.active_layer_collection 

def collection_active_set(col):
	"""Sets active viewlayer collection"""
	bpy.context.view_layer.active_layer_collection = layer_collection_get(col)

#Attributes
def collection_attr_set(target_col, attr_name, attr_value):
	"""Sets value on collection"""
	target_col[attr_name] = attr_value


def collection_attr_get(target_col, attr_name):
	"""Sets value on collection"""
	attr = target_col.get(attr_name)
	if not attr:
		return
	return attr

def collection_hide_viewport_get(target):
	"""Sets hide viewport value for object"""
	return target.hide_viewport


def collection_hide_viewport_set(target, value):
	"""Sets hide viewport value for object"""
	target.hide_viewport = value
	
def layer_collection_get(layer_col, target_col_name):
	"""Returns target collection if it exists in layer collection"""
	target_col = None
	if (layer_col.name == target_col_name):
		return layer_col
	for layer in layer_col.children:
		target_col = layer_collection_get(layer, target_col_name)
		if target_col:
			return target_col
	return None

def collection_new(col_name, col_parent):
	"""Creates new collection and parents it to col parent"""
	col_new = bpy.data.collections.new(col_name)
	col_parent.children.link(col_new)

	return col_new

def collection_direct_children_col_get(col): #TODO: Make update function
	"""Gets the direct children collection of target collection"""
	direct_children_col = col.get(DIRECT_CHILDREN)
	if not direct_children_col:
		name = f"{col.name}_{DIRECT_CHILDREN}"
		data_scene = scene_get(ITOOLS_DATA)
		direct_children_col = collection_new(name, data_scene.collection)
		col[DIRECT_CHILDREN] = direct_children_col
		

		for obj in col.objects: #TODO: Get children of objs that are not in other collections
			direct_children_col.objects.link(obj)

	return direct_children_col


def collection_origin_get(col):
	"""Gets the collection origin"""
	origin_col = col.get(ORIGIN)
	origin_name = f"_{ORIGIN.capitalize()}_" + col.name  

	if not origin_col:
		origin_col = bpy.data.objects.new(origin_name, None)
		origin_col.empty_display_type = 'ARROWS'
		
		col.objects.link(origin_col)
		origin_col.select_set(True)
		origin_col.location = col.instance_offset
		col[ORIGIN] = origin_col

	if origin_col.name != origin_name:
		origin_col.name = origin_name

	return origin_col

def collection_origin_inverse_matrix(col):
	"""Gets the origin inverse matrix for col"""
	origin = collection_origin_get(col)

	origin_matrix = origin.matrix_world.copy()

	# Keep position and rotation only.
	origin_position = origin_matrix.translation
	origin_rotation = origin_matrix.to_quaternion()

	origin_inverse = (
		Matrix.Translation(origin_position)
		@ origin_rotation.to_matrix().to_4x4()
	)

	return origin_inverse  

def collection_world_aligned_transform_update(col):
	"""Refreshes world aligned collection rotation and collection offset"""
	world_aligned_instance = col.get(WORLD_ALIGNED_INSTANCE)

	if not world_aligned_instance:
		return

	collection_origin = collection_origin_get(col)
	
	col.instance_offset = collection_origin.location 
	collection_direct_children_col_get(col).instance_offset = collection_origin.location

	#Calculate correction
	current_rotation = collection_origin.rotation_euler.copy()
	correction = current_rotation.to_matrix().transposed().to_euler(
		collection_origin.rotation_mode
	)
	world_aligned_instance.rotation_euler = correction
	world_aligned_instance.location = collection_origin.location


def collection_world_aligned_get(col):
	"""Gets the world aligned collection of the collection"""
	world_aligned_col = col.get(WORLD_ALIGNED)

	if not world_aligned_col:
		data_scene = scene_get(ITOOLS_DATA)
		data_scene_col = data_scene.collection

		world_aligned_col_name = f"{col.name}_WORLD_ALIGNED"
		world_aligned_col = collection_new(world_aligned_col_name, data_scene_col)
		collection_attr_set(world_aligned_col, COL_TYPE, WORLD_ALIGNED)


		#Instace col inside world aligned and rotate back to 0

		instance_name = f"{col.name}_{WORLD_ALIGNED_INSTANCE}"
		world_aligned_instance = bpy.data.objects.new(instance_name, None)
		direct_children_col = collection_direct_children_col_get(col)
		world_aligned_instance.instance_collection = direct_children_col
		world_aligned_instance.instance_type = 'COLLECTION'
		col[WORLD_ALIGNED_INSTANCE] = world_aligned_instance #TODO: Not sure i need this data


		world_aligned_col.objects.link(world_aligned_instance)
		#Apply world offset and rotation
		collection_world_aligned_transform_update(col) #TODO: Use drivers to set these


		col[WORLD_ALIGNED] = world_aligned_col #TODO: Maybe change name of this?

	return world_aligned_col

def collection_assambly_instance_get(col):
	assambly_instance = col.get(ASSAMBLY_INSTANCE)

	if not assambly_instance:
		assambly_scene = scene_get(ASSAMBLY_SCENE)
		instance_name = f"{col.name}_Inst"
		assambly_instance = bpy.data.objects.new(instance_name, None)
		assambly_instance.instance_collection = collection_world_aligned_get(col)
		assambly_instance.instance_type = 'COLLECTION'
		col[ASSAMBLY_INSTANCE] = assambly_instance
		assambly_scene.collection.objects.link(assambly_instance)



	return assambly_instance

def collection_tags_update(col):
	"""Updates tags for collection"""
	for tag in COL_TAGS:
		col_tag = col.get(tag)

		if not col_tag:
			continue

		collection_attr_set(col_tag, COL_TYPE, tag)
