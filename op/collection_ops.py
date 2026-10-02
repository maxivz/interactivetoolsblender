import bpy
import random

from .. utils.itools import get_collection_top_level_parent, get_selected
from .. utils.custom_data import itools_data_get
from ..utils.constants import COLLECTION_COLOR, COLLECTION_COLORS_USE_PARENT_COLOR, COLLECTION_COLORS_FORCE_RANDOM

def get_collection_color(collection):
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
			return get_collection_color(parent_collection)
		

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

def assign_object_collection_colors():
	"""Assigns viewport display colors to objects based on their collections."""
	for obj in bpy.data.objects:
		if obj.type not in {'MESH', 'CURVE'}:
			continue  

		collection = next((col for col in bpy.data.collections if obj.name in col.objects), None)
		if collection:
			color = get_collection_color(collection)
			obj.color = color
	
class ColorObjsByCollection(bpy.types.Operator):
	bl_idname = "collection.color_objs_by_collection"
	bl_label = "Color Objects By Collection"
	bl_description = """Sets the color of the objects to the color of its collection.
	If the collection has a color tag it will use it, if it doesnt it will generate a random one
	The color is visible in Solid shading mode, with color mode set to attribute"""
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		assign_object_collection_colors()
		return {'FINISHED'}


class RenameObjsByCollection(bpy.types.Operator):
	bl_idname = "collection.rename_objs_by_collection"
	bl_label = "Rename Objects By Collection"
	bl_description = "Renames all objects in collection to reflect the collection name"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		active_col = bpy.context.collection
		for obj_num, obj in enumerate(active_col.objects):
			obj.name = f"{active_col.name}_{obj_num}"
		return {'FINISHED'}
	

class EditCollectionOffset(bpy.types.Operator):
	bl_idname = "collection.edit_collection_offset_toggle"
	bl_label = "Edit Collection Offset"
	bl_description = "Spawns a locator to edit the offset of the collection"
	bl_options = {'REGISTER', 'UNDO'}

	def edit_collection_offset_toggle(self, collection, context):
		locator_name = collection.name + "_origin"
		locator = bpy.data.objects.get(locator_name)

		selection = get_selected()

		if selection:
			bpy.ops.object.select_all(action='DESELECT')
		
		if not locator:
			if collection.objects:
				locator = bpy.data.objects.new(locator_name, None)
				locator.empty_display_type = 'ARROWS'
				
				collection.objects.link(locator)
				locator.select_set(True)
				locator.location = collection.instance_offset
				context.view_layer.objects.active = locator

		else:
			# Set the collection offset to the locator location and delete it
			collection.instance_offset = locator.location
			bpy.data.objects.remove(locator)
			

	def execute(self, context):
		active_col = bpy.context.collection
		self.edit_collection_offset_toggle(active_col, context)
		return {'FINISHED'}

class ObjectMoveToActiveCollection(bpy.types.Operator):
	bl_idname = "collection.move_to_active_collection"
	bl_label = "Move Objects To Active Collection"
	bl_description = "Moves selected objects to the active collection"
	bl_options = {'REGISTER', 'UNDO'}

	def collection_list_generate(self, context):
		"""Return a list of tuples for EnumProperty."""
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
	
	collection_target: bpy.props.EnumProperty( 
		name="Colllection Target",
		description="Target Collection to move selected objects to.",
		items=collection_list_generate, # type: ignore
	)

	unlink_other_collections: bpy.props.BoolProperty( 
		name="Unlink other collections",
		description="Unlink other collections from Objects when performing the move",
		default = False # type: ignore
	)


	def invoke(self, context, event):
		# Show popup dialog with properties
		return context.window_manager.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "collection_target", expand=True) 

	def execute(self, context):
		target_objs = context.selected_objects

		target_col = bpy.data.collections.get(self.collection_target)

		if not target_col:
			return {'CANCELLED'}

		for obj in target_objs:
			# Unlink from all collections
			if self.unlink_other_collections:
				for col in obj.users_collection:
					col.objects.unlink(obj)
			# Link to the active collection
			target_col.objects.link(obj)

		return {'FINISHED'}
