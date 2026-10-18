
import bpy
import math

class VIEW3D_OT_mouse_parameter(bpy.types.Operator):
	"""Base class for modifiying settings using mouse movement and modifier keys"""

	bl_idname = "view3d.mouse_parameter"
	bl_label = "Mouse Parameter Adjust"
	bl_options = {'REGISTER', 'UNDO',  "GRAB_CURSOR", "BLOCKING"}

	senitivity = 0.01
	_mouse_x = 0.0
	_mouse_x_start = 0.0
	_mouse_y = 0.0
	_mouse_y_start = 0.0
	_mod_ctrl = False
	_mod_alt = False
	_mod_shift = False
	modkey = 0
	using_settings = False
	ignore_initial_sym_count = False
	change_axis = False
	change_rotation = False
	change_iteration = False
	symmetry_center = ""
	first_run = False

	def draw_ui(self, context, event):
		pass

	def calculate_iterations(self, context, selection): #TODO: Generalize
		if self.change_iteration:
			if self.using_settings:
				self.sym_count = self.ui_count

			else:
				if self.ignore_initial_sym_count:
					self.sym_count = int(((self._mouse_x - self._mouse_x_start) * self.senitivity))
				else:
					self.sym_count = self.initial_sym_count + int(((self._mouse_x - self._mouse_x_start) * self.senitivity))

			if self.sym_count < 1:
				self.sym_count = 1
				self._mouse_x_start = self._mouse_x
				self.ignore_initial_sym_count = True

			bpy.context.view_layer.objects.active = selection

			selection.modifiers["Radial Symmetry"].count = self.sym_count
			self.change_iteration = False

	def calculate_axis(self, context): #TODO: Generalize
		if self.change_axis:
			self.sym_axis = int((self.initial_sym_axis + (self._mouse_x - self._mouse_x_start) * self.senitivity) % 3)
			self.change_axis = False


	@classmethod
	def poll(cls, context):
		return context.mode == 'OBJECT' and len(context.selected_objects) > 0

	def execute(self, context):
		#self.sync_ui_settings() #TODO: See if its needed
		self.calculate_iterations(context, bpy.data.objects[self.selection])
		self.calculate_axis(context)
		self.calculate_rotation(self.sym_axis)
		return{'FINISHED'}

	def modal(self, context, event):
		if event.type == 'MOUSEMOVE':  # Apply
			if event.ctrl:
				if self.modkey != 1:
					self.modkey = 1
					self._mouse_x_start = event.mouse_x
					self.initial_sym_count = self.sym_count
				self.change_axis = True

			else:
				if self.modkey != 0:
					self.modkey = 0
					self._mouse_x_start = event.mouse_x
					self.initial_sym_axis = self.sym_axis
				self.change_iteration = True

			self._mouse_x = event.mouse_x
			self.execute(context)
			self.change_rotation = True

		elif event.type in {'H', 'Z'}:  # Show Pivot
			if event.value == 'RELEASE':
				if bpy.data.objects[self.offset_obj].hide_viewport:
					bpy.data.objects[self.offset_obj].hide_viewport = False
				else:
					bpy.data.objects[self.offset_obj].hide_viewport = True

		elif event.type == 'LEFTMOUSE':  # Confirm
			if event.value == 'RELEASE':
				self.using_settings = True
				context.area.header_text_set(text=None)
				bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')

				#Switch between modes to force update UI
				bpy.ops.object.mode_set(mode='EDIT')
				bpy.ops.object.mode_set(mode='OBJECT')
				return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
			if not self.first_run:
				self.restore_settings(context, bpy.data.objects[self.selection])
			bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
			context.area.header_text_set(text=None)

			#Switch between modes to force update UI
			bpy.ops.object.mode_set(mode='EDIT')
			bpy.ops.object.mode_set(mode='OBJECT')

			if self.first_run:
				bpy.ops.object.modifier_remove(modifier="Radial Symmetry")

			return {'CANCELLED'}

		#Tooltip
		context.area.header_text_set("LMB: confirm, RMB:Cancel, Mouse Left/Right for number of instances, CTRL + Mouse Left/ Right to change Symmetry Axis H: Show / Hide Origin")
		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		self._mouse_x_start = event.mouse_x
		self.selection = bpy.context.active_object.name

		if bpy.data.objects[self.selection].modifiers.find("Radial Symmetry") < 0:
			self.setup_symmetry(context, bpy.data.objects[self.selection])
			self.first_run = True

		self.recover_settings(context, bpy.data.objects[self.selection])

		self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_ui, (self, context), 'WINDOW','POST_PIXEL')

		self.execute(context)
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}
