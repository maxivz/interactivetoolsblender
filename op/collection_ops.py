import bpy
from .. utils.itools import get_selected, parent_set, show_enum_values
from .. utils.collections import (collection_colors_assign_to_objects,
								collection_active_set,
								collection_attr_set,
								collection_hide_viewport_get,
								collection_hide_viewport_set,
								layer_collection_get,
								active_obj_collection_list_generate,
								active_obj_collections_amountr )
DIFFERENCE = 'DIFFERENCE'
UNION = 'UNION'
INTERSECT = 'INTERSECT'


class ColorObjsByCollection(bpy.types.Operator):
	bl_idname = "collection.color_objs_by_collection"
	bl_label = "Color Objects By Collection"
	bl_description = """Sets the color of the objects to the color of its collection.
	If the collection has a color tag it will use it, if it doesnt it will generate a random one
	The color is visible in Solid shading mode, with color mode set to attribute"""
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		collection_colors_assign_to_objects()
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
	bl_description = """Spawns a locator to edit the offset of the collection 
	ALT: Set the collection offset to the 3D cursor location"""
	bl_options = {'REGISTER', 'UNDO'}

	set_from_3dcursor: bpy.props.BoolProperty( 
		name="Set from 3D Cursor",
		description="Set the collection offset from the 3D cursor position",
		default = False # type: ignore
	)

	def invoke(self, context, event):
		# Show popup dialog with properties
		self.set_from_3dcursor = False
		if event.alt:
			self.set_from_3dcursor = True
		return self.execute(context)

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
		if self.set_from_3dcursor:
			active_col.instance_offset = context.scene.cursor.location
		else:
			self.edit_collection_offset_toggle(active_col, context)
		return {'FINISHED'}

class CollectionActiveObjectCollectionsTemplate(bpy.types.Operator):
	bl_idname = "Template"
	bl_label = "Template"
	bl_description = """Template"""
	bl_options = {'REGISTER', 'UNDO'}
	
	active_obj_collections: bpy.props.EnumProperty( 
		name="Colllection Target",
		description="Target Collection to move selected objects to.",
		items=active_obj_collection_list_generate, # type: ignore
	)

	def invoke(self, context, event):
		# Show popup dialog with properties
		if active_obj_collections_amountr(context) > 1:
			return context.window_manager.invoke_props_dialog(self)

		return self.execute(context)
		

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "active_obj_collections", expand=True) 

	def execute(self, context):
		return {'FINISHED'}

class CollectionActiveObjectMoveTo(CollectionActiveObjectCollectionsTemplate):
	bl_idname = "collection.move_to_active_collection"
	bl_label = "Move Objects To Active Collection"
	bl_description = """Moves selected objects to the selected collection the active object belong to.
	ALT: Add selected objects to the selected collection instead of moving them"""
	bl_options = {'REGISTER', 'UNDO'}
	
	unlink_other_collections: bpy.props.BoolProperty( 
		name="Unlink other collections",
		description="Unlink other collections from Objects when performing the move",
		default = False # type: ignore
	)

	def invoke(self, context, event):
		# Show popup dialog with properties
		self.unlink_other_collections = True
		if event.alt:
			self.unlink_other_collections = False
		
		return super().invoke(context, event)

	def execute(self, context):
		target_objs = context.selected_objects

		target_col = bpy.data.collections.get(self.active_obj_collections)

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

class CollectionActiveObjectSelect(CollectionActiveObjectCollectionsTemplate):
	bl_idname = "collection.collection_active_object_select"
	bl_label = "Select collection of active object"
	bl_description = """Select objects in the active objects collection.
	ALT: Selects the collection instead, focuses on it in the outliner"""
	bl_options = {'REGISTER', 'UNDO'}

	select_collection: bpy.props.BoolProperty( 
		name="Select Collection",
		description="Selects Collection instead of selecting the objects",
		default = False # type: ignore
	)


	def invoke(self, context, event):
		self.select_collection = False
		if event.alt:
			self.select_collection = True

		return super().invoke(context, event)

	def execute(self, context):
		target_col = bpy.data.collections.get(self.active_obj_collections)

		if not target_col:
			return {'CANCELLED'}
		

		if self.select_collection:
			collection_active_set(target_col)

		else:
			target_objs = target_col.objects
			bpy.ops.object.select_all(action='DESELECT')
			for obj in target_objs:
				obj.select_set(True)

		return {'FINISHED'}

class CollectionBooleanCreate(CollectionActiveObjectCollectionsTemplate):
	bl_idname = "collection.collection_boolean_create"
	bl_label = "Creates a boolean collection for active collection"
	bl_description = """Creates a boolean collection for active collection"""
	bl_options = {'REGISTER', 'UNDO'}

	bool_type: bpy.props.EnumProperty(
		name="Boolean Type",
		description="Type of boolean operation to perform",
		items=[
			('DIFFERENCE', 'Difference', 'Subtracts the boolean collection from the active object'),
			('UNION', 'Union', 'Adds the boolean collection to the active object'),
			('INTERSECT', 'Intersect', 'Intersects the boolean collection from the active object'),
		],
		default='DIFFERENCE'
		) # type: ignore

	def invoke(self, context, event):
		# Show popup dialog with properties
		return super().invoke(context,event)

	def execute(self, context):
		obj_active = bpy.context.active_object
		objs_selected = context.selected_objects

		if obj_active is None:
			print("Error: No active object.")
			return {'CANCELLED'}


		#Remap bool type name, color for col
		bool_tag = "Sub"
		color_tag = "COLOR_01"
		if self.bool_type == 'UNION':
			bool_tag = "Add"
			color_tag = "COLOR_04" 

		elif self.bool_type == 'INTERSECT':
			bool_tag = "Int"
			color_tag = "COLOR_03"


		#Check if bool col exists before creating it
		target_col = bpy.data.collections.get(self.active_obj_collections)

		if not target_col:
			return { "CANCELLED" }
		
		bool_col_name = f"{target_col.name}_{bool_tag}"
		bool_col = bpy.data.collections.get(bool_col_name)

		if bool_col is None:
			bool_col = bpy.data.collections.new(bool_col_name)
			target_col.children.link(bool_col)
			collection_attr_set(target_col, self.bool_type, bool_col)
			bool_col.color_tag = color_tag


		bpy.context.view_layer.update() #Update viewlayer to update hirarchies before parenting

		#Link objs to bool col 
		for obj in objs_selected:
			#Set new Col
			if obj.name in bool_col.objects:
				continue

			if obj == obj_active:
				continue

			for col in obj.users_collection:
				col.objects.unlink(obj)

			bool_col.objects.link(obj)

			#Set new parent
			parent_set(obj, obj_active)

			obj.display_type = "WIRE"


		# Create the Boolean modifier
		bool_mod_name = f"Bool Col {bool_tag}"

		bool_mod = obj_active.modifiers.get(bool_mod_name)

		if not bool_mod:
			bool_mod = obj_active.modifiers.new(
				name=bool_mod_name,
				type='BOOLEAN'
			)

		# Configure the Boolean modifier
		bool_mod.operation = self.bool_type
		bool_mod.operand_type = 'COLLECTION'
		bool_mod.collection = bool_col
	

		return {'FINISHED'}



class CollectionHiddenSet(bpy.types.Operator):
	bl_idname = "collection.hidden_set"
	bl_label = "Collection Hidden Set"
	bl_description = """Sets Hidden Set for Collection and all children"""
	bl_options = {'REGISTER', 'UNDO'}

	col_target: bpy.props.StringProperty( 
		name="Collection Target",
		description="Target Collection", # type: ignore
	)

	def execute(self, context):
		target_col = bpy.data.collections.get(self.col_target)
		if not target_col:
			return { "CANCELLED" }

		hide_set = collection_hide_viewport_get(target_col)

		print(f"Hide ser {hide_set}")

		collection_hide_viewport_set(target_col, not hide_set)

		return {'FINISHED'}

class CollectionActiveBySelection(CollectionActiveObjectCollectionsTemplate):
	bl_idname = "collection.active_by_selection"
	bl_label = "Collection Active by selection"
	bl_description = """Sets active collection from the selection the active object is part of"""
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		target_col = self.active_obj_collections
		layer_collection = context.view_layer.layer_collection
		layer_col_target = layer_collection_get(layer_collection, target_col)

		if layer_col_target:
			context.view_layer.active_layer_collection = layer_col_target
			return {'FINISHED'}

		return {'FINISHED'}

class CollectionsOptionsPie(bpy.types.Operator):
	bl_idname = "collection.itools_collections_pie"
	bl_label = "Collections Options Pie"
	bl_description = "Display collections options"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_Collections")
		return{'FINISHED'}

#Register Classes
classes = [RenameObjsByCollection, EditCollectionOffset, ColorObjsByCollection, 
		   CollectionActiveObjectMoveTo, CollectionActiveObjectSelect, CollectionsOptionsPie,
		   CollectionBooleanCreate, CollectionHiddenSet, CollectionActiveBySelection]

def register():
	from bpy.utils import register_class
	
	for cls in classes:
		register_class(cls)


def unregister():
	from bpy.utils import unregister_class

	for cls in reversed(classes):
		unregister_class(cls)