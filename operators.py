######################################################################################################
#                                  Bone Breaker Rigging for UE4                                      #
######################################################################################################
#                                                                   #                                #
#    Adjust your rig to export native unreal skeleton animation.    #                                #
#                                                                   #          Created By            #
#  This software is provided as is, with the following restriction. #        Andy @ MostHostLA       #
#   You may NOT include this software into a PAID application or    #                                #
#     make a profit by directly selling portions of this code.      #       www.mosthostla.com       #
#                                                                   #                                #
#                                                                   #                                #
#*******************************************************************#********************************#
# A bunch of "hidden" functions that the script won't just run for you. They are included so as to   #
# help users who are creating or modifying their own custom Rig. this process works with any type of #
# skeleton, you just need to work some magic to get the bones to match up in 3d space...             #
#                                                                                                    #
# This version for blender 2.82 support animation importing/authoring -- the best possible with the  #
# current rigify stretch/rotate issues                                                               #
#                                                                                 (2K screens rulke) #
######################################################################################################
if "bpy" in locals():
	import importlib
	importlib.reload(BoneBreaker)
else:
	from . import BoneBreaker
import bpy
import bpy.ops
import bmesh
import bgl
import gpu
import mathutils
import math
import numpy as np
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from bpy.types import Operator
from bpy.props import IntProperty

#***************************************************************************************************#
#                                    - - - OPERATORS - - -                     	                    #
#***************************************************************************************************#
class BONEBREAKER_OT_AddFeature(bpy.types.Operator):
	"""Import an FBX file using suggested settings for Unreal"""
	bl_idname = "bonebreaker.addfeature"
	bl_label = "Get information on adding this feature."
	fileimport = False
	# this values are manipulated to decide if to close the modal operator.
	sceneobjects = 0
	currentobjects = 0
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is None
	def execute(self, context):
		def infomenu(self, context):
			scene = context.scene
			layout = self.layout
			row = layout.column()
			row.label(text="Find updated features on our website")
			row.label(text="Where you can get our Ue4FBX addon to enable this feature")
			row.label(text="http://MostHostLa.com/gamedev/")
			row.operator("wm.url_open", text="Open Link").url = "http://mosthostla.com/gamedev/"
		bpy.context.window_manager.popup_menu(infomenu, title="Addon Information", icon='QUESTION')

		#self.report({'INFO'}, 'Info message download the additional addon to enable this feature!')
		return {'FINISHED'}
	
		
class BONEBREAKER_OT_FBXimportUE4(bpy.types.Operator):
	"""Import an FBX file using suggested settings for Unreal"""
	bl_idname = "bonebreaker.fbximportue4"
	bl_label = "Import an FBX file using suggested settings for Unreal."
	fileimport = False
	# this values are manipulated to decide if to close the modal operator.
	sceneobjects = 0
	currentobjects = 0
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is None
		
	#Modal wokaround.
	def modal(self, context, event):
		#check if the objects on screen have changed.
		if self.currentobjects > self.sceneobjects:
			#Blender versions will probably change this in the future - last update 2/23/2020
			imported = bpy.data.objects.items()[0][1]#bpy.context.selected_objects[0]
			if imported.animation_data is not None:
				if imported.animation_data.action is not None:
					print("Imported an animated skeletal mesh.")
					context.scene.frame_end = imported.animation_data.action.frame_range[1]
				else:
					print("Imported static skeletal mesh.")
					context.scene.frame_end = 1
			else:
				print("Imported static skeletal mesh.")
				context.scene.frame_end = 1
			context.scene.frame_start=0
			bpy.context.scene.frame_set(1)
			bpy.ops.object.select_all(action='DESELECT')
			return {'FINISHED'}
		else:
			#objects haven't changed, import can't be done.
			self.currentobjects = len(bpy.data.objects)
			return {'PASS_THROUGH'}	
	def invoke(self, context, event):
		#override system unit scale
		context.scene.unit_settings.scale_length=.01
		context.scene.unit_settings.system='METRIC'
		context.space_data.clip_end = 50000
		#save current number of objects on scene
		self.sceneobjects = len(bpy.data.objects)
		#start the import
		bpy.ops.ue4fbx.importfbx("INVOKE_REGION_WIN")
		#bpy.ops.bonebreaker.bbimportfbx("INVOKE_REGION_WIN")
		#set up the modal
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class BONEBREAKER_OT_FBXimport(bpy.types.Operator):
	"""Import an FBX file using suggested settings for Unreal"""
	bl_idname = "bonebreaker.fbximport"
	bl_label = "Import an FBX file using suggested settings for Unreal."
	fileimport = False
	# this values are manipulated to decide if to close the modal operator.
	sceneobjects = 0
	currentobjects = 0
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is None
		
	#Modal wokaround.
	def modal(self, context, event):
		#check if the objects on screen have changed.
		if self.currentobjects > self.sceneobjects:
			#Blender versions will probably change this in the future - last update 2/23/2020
			imported = bpy.data.objects.items()[0][1]#bpy.context.selected_objects[0]
			if imported.animation_data is not None:
				if imported.animation_data.action is not None:
					print("Imported an animated skeletal mesh.")
					context.scene.frame_end = imported.animation_data.action.frame_range[1]
				else:
					print("Imported static skeletal mesh.")
					context.scene.frame_end = 1
			else:
				print("Imported static skeletal mesh.")
				context.scene.frame_end = 1
			context.scene.frame_start=0
			bpy.context.scene.frame_set(1)
			bpy.ops.object.select_all(action='DESELECT')
			return {'FINISHED'}
		else:
			#objects haven't changed, import can't be done.
			self.currentobjects = len(bpy.data.objects)
			return {'PASS_THROUGH'}	
	def invoke(self, context, event):
		#override system unit scale
		context.scene.unit_settings.scale_length=.01
		context.scene.unit_settings.system='METRIC'
		context.space_data.clip_end = 50000
		#save current number of objects on scene
		self.sceneobjects = len(bpy.data.objects)
		#start the import
		bpy.ops.import_scene.fbx("INVOKE_REGION_WIN")
		#set up the modal
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}
		
class BONEBREAKER_OT_exportmannequin(bpy.types.Operator):
	"""Export the final animation in an automated process"""
	bl_idname = "bonebreaker.exportmannequin"
	bl_label = "Export the final animation in an automated process."
		
	@classmethod
	def poll(cls, context):
		return bpy.context.window.view_layer.layer_collection.children.get('UE4') is not None and bpy.context.window.view_layer.layer_collection.children.get('Collection') is not None
		
	def execute(self, context):
		bpy.ops.bonebreaker.follownone()
		#select none at all.
		for ob in bpy.context.scene.collection.children['Collection'].objects: ob.select_set(False)
		#disable collection and jump to UE4.
		bpy.context.window.view_layer.layer_collection.children['Collection'].exclude = True
		bpy.context.window.view_layer.layer_collection.children['UE4'].exclude = False
		#select the root rig.
		UE4 = bpy.context.scene.collection.children['UE4'].objects.get("root")
		context.view_layer.objects.active = UE4
		#with the object select go to pose mode.
		UE4.select_set(True)
		bpy.ops.object.mode_set(mode='OBJECT')
		print("ready")
		#Run the export.
		if hasattr(bpy.types, "UE4FBX_OT_exportfbx") is not False:
			bpy.ops.ue4fbx.exportfbx("INVOKE_REGION_WIN",
				use_selection=True,
				bake_space_transform=True,
				axis_forward='Y', axis_up='Z',
				object_types={'ARMATURE', 'MESH', 'OTHER'},
				use_custom_props=True,
				add_leaf_bones=False,
				primary_bone_axis='Y', secondary_bone_axis='X')
		else:
			bpy.ops.export_scene.fbx("INVOKE_REGION_WIN",
				use_selection=True,
				bake_space_transform=True,
				axis_forward='Y', axis_up='Z',
				object_types={'ARMATURE', 'MESH', 'OTHER'},
				use_custom_props=True,
				add_leaf_bones=False,
				primary_bone_axis='Y', secondary_bone_axis='X')
		#deselect all.
		#BoneBreaker.setObj()
		#return to home layer.
		#bpy.data.scenes[0].layers = BoneBreaker.LayerSet(0)
		#Switch pole rotation to key frames.
		return {'FINISHED'}

class BONEBREAKER_OT_FBXexport(bpy.types.Operator):
	"""Export the an FBX file with the unreal settings"""
	bl_idname = "bonebreaker.fbxexport"
	bl_label = "Export selected object to FBX."
	
	type: bpy.props.StringProperty(default = "Null")
	@classmethod
	def poll(cls, context):
		if len(bpy.data.objects) >= 1:
			return True
		
	def execute(self, context):
		#Run the export.
		if hasattr(bpy.types, "UE4FBX_OT_exportfbx") is not False:
			if self.type=="MIXER":
				bpy.ops.ue4fbx.exportfbx("INVOKE_REGION_WIN",
				use_selection=False,
				mesh_smooth_type='FACE',
				axis_forward='-Z', axis_up='Y',
				bake_space_transform=True,
				object_types={'EMPTY','ARMATURE', 'MESH', 'OTHER'},
				add_leaf_bones=False,
				primary_bone_axis='Y', secondary_bone_axis='X')
			else:
				bpy.ops.ue4fbx.exportfbx("INVOKE_REGION_WIN",
				use_selection=False,
				mesh_smooth_type=self.type,
				axis_forward='Y', axis_up='Z',
				bake_space_transform=True,
				object_types={'EMPTY','ARMATURE', 'MESH', 'OTHER'},
				add_leaf_bones=False,
				primary_bone_axis='Y', secondary_bone_axis='X')
		else:
			if self.type=="MIXER":
				bpy.ops.export_scene.fbx("INVOKE_REGION_WIN",
				use_selection=False,
				mesh_smooth_type='FACE',
				axis_forward='-Z', axis_up='Y',
				bake_space_transform=True,
				object_types={'EMPTY','ARMATURE', 'MESH', 'OTHER'},
				add_leaf_bones=False,
				primary_bone_axis='Y', secondary_bone_axis='X')
			else:
				bpy.ops.export_scene.fbx("INVOKE_REGION_WIN",
				use_selection=False,
				mesh_smooth_type=self.type,
				bake_space_transform=True,
				axis_forward='Y', axis_up='Z',
				object_types={'EMPTY','ARMATURE', 'MESH', 'OTHER'},
				add_leaf_bones=False,
				primary_bone_axis='Y', secondary_bone_axis='X')
		return {'FINISHED'}
		
class BONEBREAKER_OT_all(bpy.types.Operator):
	"""Create a metarig if one does not exist.
form the rigify rig based on the metarig"""
	bl_idname = "bonebreaker.all"
	bl_label = "Create a metarig if one does not exist, and form the rigify rig based on the rig."
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is not None

	def execute(self, context):
		bpy.ops.bonebreaker.metarig()
		bpy.ops.bonebreaker.rigify()
		rig = bpy.data.objects.get("rig")
		rig.select_set(True)
		context.view_layer.objects.active = rig
		BoneBreaker.IK_bones_follow(rig)
		rig_id = rig.data['rig_id']
		#Toggle Pole Rotation isntead of default setting.
		rigify_function = "rigify_limb_toggle_pole_"
		rigify_function = rigify_function+bpy.data.objects['rig'].data['rig_id']
		eval("bpy.ops.pose."+rigify_function+'(prop_bone="upper_arm_parent.L", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["upper_arm_ik.L", "MCH-forearm_ik.L", "MCH-upper_arm_ik_target.L"]\', ctrl_bones=\'["upper_arm_ik.L", "hand_ik.L", "upper_arm_ik_target.L"]\', extra_ctrls=\'[""]\', use_pole=True)')
		eval("bpy.ops.pose."+rigify_function+'(prop_bone="upper_arm_parent.R", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["upper_arm_ik.R", "MCH-forearm_ik.R", "MCH-upper_arm_ik_target.R"]\', ctrl_bones=\'["upper_arm_ik.R", "hand_ik.R", "upper_arm_ik_target.R"]\', extra_ctrls=\'[""]\', use_pole=True)')
		eval("bpy.ops.pose."+rigify_function+'(prop_bone="thigh_parent.R", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["thigh_ik.R", "MCH-shin_ik.R", "MCH-thigh_ik_target.R"]\', ctrl_bones=\'["thigh_ik.R", "foot_ik.R", "thigh_ik_target.R"]\', extra_ctrls=\'[""]\', use_pole=True)')
		eval("bpy.ops.pose."+rigify_function+'(prop_bone="thigh_parent.L", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["thigh_ik.L", "MCH-shin_ik.L", "MCH-thigh_ik_target.L"]\', ctrl_bones=\'["thigh_ik.L", "foot_ik.L", "thigh_ik_target.L"]\', extra_ctrls=\'[""]\', use_pole=True)')
		print('Rigify Function Name', rigify_function)
        #Hide rig's needless FK/Tweak.
		bpy.context.object.data.layers[8] = False
		bpy.context.object.data.layers[9] = False
		bpy.context.object.data.layers[11] = False
		bpy.context.object.data.layers[12] = False
		bpy.context.object.data.layers[14] = False
		bpy.context.object.data.layers[15] = False
		bpy.context.object.data.layers[17] = False
		bpy.context.object.data.layers[18] = False
		return {'FINISHED'}

class BONEBREAKER_OT_metarig(bpy.types.Operator):
	"""create a metarig following the structure of the unreal engine mannequin"""
	bl_idname = "bonebreaker.metarig"
	bl_label = "create a metarig following the structure of the unreal engine mannequin"
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is not None
			 
	def execute(self, context):
		if bpy.data.objects.get("metarig") is not None:
			#Deselect all
			bpy.ops.object.select_all(action='DESELECT')
			#object Select
			bpy.data.objects['metarig'].select_set(True)
			#remove object
			bpy.ops.object.delete()
			#Deselect all agian.
			bpy.ops.object.select_all(action='DESELECT')
		
		if bpy.data.objects.get("root") is not None and bpy.data.objects.get("metarig") is None:
			#create our metarig and make our rigify rig! booya.
			BoneBreaker.metaBlending2(bpy.data.objects["root"])
		else:
			bpy.context.window_manager.popup_menu(BoneBreaker.popup, title="NO BASE FILE! Please import the mannequin FBX!", icon='ERROR')

		return {'FINISHED'}

class BONEBREAKER_OT_rigify(bpy.types.Operator):
	"""generate the rigify rig"""
	bl_idname = "bonebreaker.rigify"
	bl_label = "generate the rigify rig"

	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is not None and bpy.data.objects.get("metarig") is not None

	def execute(self, context):
		if bpy.data.objects.get("rig") is not None:
			#try obj mode
			BoneBreaker.setObj()
			#object Select
			bpy.data.objects['rig'].select_set(True)
			#remove object
			bpy.ops.object.delete()
			#Deselect all agian.
			BoneBreaker.setObj()

		#select Metarig.
		if bpy.data.objects.get("metarig") is not None and bpy.data.objects.get("rig") is None:
			metarig = bpy.data.objects.get("metarig")
			metarig.select_set(True)
			# Create a new collection and link it to the scene.
			MetarigC = bpy.data.collections.new("Metarig")
			bpy.context.scene.collection.children.link(MetarigC)
			# Link active object to the new collection
			MetarigC.objects.link(metarig)
			bpy.context.window.view_layer.layer_collection.children["Metarig"].exclude = True
			bpy.ops.pose.rigify_generate()
			#hide not needed bone layers.
			bpy.context.object.data.layers[0] = False
			bpy.context.object.data.layers[1] = False
			bpy.context.object.data.layers[2] = False
			#deselect the metarig.
			metarig.select_set(False)
			#remove layer
			bpy.context.scene.collection.children['Collection'].objects.unlink(metarig)
			if bpy.data.objects.get("rig") is not None:
				BoneBreaker.AdjustRig4UE4(bpy.data.objects.get("rig"))
				BoneBreaker.AdjustRigSuperFingers(bpy.data.objects.get("rig"))
				BoneBreaker.setObj()
				if bpy.data.objects.get("root") is not None:
					ue4 = bpy.data.objects.get("root")
					ue4.select_set(True)
					print(ue4.name)
					BoneBreaker.adjustConstraint(ue4)
					
					#Create a new collection and link it to the scene.
					UE4C = bpy.data.collections.new("UE4")
					bpy.context.scene.collection.children.link(UE4C)
					#Link active object to the new collection
					UE4C.objects.link(ue4)
					bpy.context.window.view_layer.layer_collection.children["UE4"].exclude = True
					#deselect
					ue4.select_set(False)
					#remove layer
					bpy.context.scene.collection.children['Collection'].objects.unlink(ue4)
					#Make Mannequin mesh not selectable.
					if bpy.data.objects.get("SK_Mannequin") is not None:
						mannequin = bpy.data.objects.get("SK_Mannequin")
						mannequin.hide_select = True
					#select the rig. go into pose mode. 
					rig = bpy.data.objects.get("rig")
					rig.select_set(True)
					bpy.context.view_layer.objects.active = rig
					#Adjust Should Socket Display
					if bpy.data.objects.get("WGT-rig_foot_heel_ik.L") is not None:
						rig.pose.bones.get("upperarm_twist_ctrl_l").custom_shape = bpy.data.objects["WGT-rig_foot_heel_ik.L"]
						rig.pose.bones.get("upperarm_twist_ctrl_l").custom_shape_scale_xyz = mathutils.Vector((1.5,1.5,1.5))
					if bpy.data.objects.get("WGT-rig_foot_heel_ik.R") is not None:
						rig.pose.bones.get("upperarm_twist_ctrl_r").custom_shape = bpy.data.objects["WGT-rig_foot_heel_ik.R"]
						rig.pose.bones.get("upperarm_twist_ctrl_r").custom_shape_scale_xyz = mathutils.Vector((1.5,1.5,1.5))
					rig.pose.bones.get("thigh_parent.L")["IK_Stretch"] = 0
					rig.pose.bones.get("thigh_parent.R")["IK_Stretch"] = 0
					rig.pose.bones.get("upper_arm_parent.L")["IK_Stretch"] = 0
					rig.pose.bones.get("upper_arm_parent.R")["IK_Stretch"] = 0
					fixconstraint = rig.pose.bones.get("ORG-spine.003").constraints.get("Stretch To")
					if fixconstraint is not None:
						rig.pose.bones.get("ORG-spine.003").constraints.remove( fixconstraint )
					#pose
					bpy.ops.object.posemode_toggle()
					BoneBreaker.addrigconstraint(rig)
				else:
					bpy.context.window_manager.popup_menu(BoneBreaker.popup, title="NO BASE FILE! Please import the mannequin FBX!", icon='ERROR')
		else:
			bpy.context.window_manager.popup_menu(BoneBreaker.popup, title="NO Metarig something's not right, generate one.", icon='ERROR')

		return {'FINISHED'}

class BONEBREAKER_OT_animall(bpy.types.Operator):
	"""Perform all the standard animations when importing a UE4 animation"""
	bl_idname = "bonebreaker.animall"
	bl_label = "Perform all the standard animations when importing a UE4 animation."
	
	@classmethod
	def poll(cls, context):
		if bpy.data.objects.get("root") is not None:
			armature = bpy.data.objects.get("root")
			if armature.animation_data is not None:
				if armature.animation_data.action is None:
					return False
			else:
				return False
		else:
			return False
		return context.scene.frame_end > 1 and bpy.data.objects.get("root") is not None and bpy.data.objects.get("rig") is not None

	def execute(self, context):
		#Follow nothing (removes links/such)
		bpy.ops.bonebreaker.follownone()
		#Switch pole rotation to key frames.
		bpy.context.view_layer.objects.active = bpy.data.objects.get("rig")
		bpy.ops.object.mode_set(mode='POSE')
		#Show rig's needless FK/Tweak.
		bpy.context.object.data.layers[8] = True
		bpy.context.object.data.layers[9] = True
		bpy.context.object.data.layers[11] = True
		bpy.context.object.data.layers[12] = True
		bpy.context.object.data.layers[14] = True
		bpy.context.object.data.layers[15] = True
		bpy.context.object.data.layers[17] = True
		bpy.context.object.data.layers[18] = True
		#Toggle Pole Rotation isntead of default setting.
		#rigify_function = "rigify_limb_toggle_pole_"
		#rigify_function = rigify_function+bpy.data.objects['rig'].data['rig_id']
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="upper_arm_parent.L", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["upper_arm_ik.L", "MCH-forearm_ik.L", "MCH-upper_arm_ik_target.L"]\', ctrl_bones=\'["upper_arm_ik.L", "hand_ik.L", "upper_arm_ik_target.L"]\', extra_ctrls=\'[""]\', use_pole=False)')
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="upper_arm_parent.R", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["upper_arm_ik.R", "MCH-forearm_ik.R", "MCH-upper_arm_ik_target.R"]\', ctrl_bones=\'["upper_arm_ik.R", "hand_ik.R", "upper_arm_ik_target.R"]\', extra_ctrls=\'[""]\', use_pole=False)')
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="thigh_parent.R", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["thigh_ik.R", "MCH-shin_ik.R", "MCH-thigh_ik_target.R"]\', ctrl_bones=\'["thigh_ik.R", "foot_ik.R", "thigh_ik_target.R"]\', extra_ctrls=\'[""]\', use_pole=False)')
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="thigh_parent.L", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["thigh_ik.L", "MCH-shin_ik.L", "MCH-thigh_ik_target.L"]\', ctrl_bones=\'["thigh_ik.L", "foot_ik.L", "thigh_ik_target.L"]\', extra_ctrls=\'[""]\', use_pole=False)')
		#Hide rig's needless FK/Tweak.
		bpy.context.object.data.layers[8] = False
		bpy.context.object.data.layers[9] = False
		bpy.context.object.data.layers[11] = False
		bpy.context.object.data.layers[12] = False
		bpy.context.object.data.layers[14] = False
		bpy.context.object.data.layers[15] = False
		bpy.context.object.data.layers[17] = False
		bpy.context.object.data.layers[18] = False
		#follow the FBX file animation.
		bpy.ops.bonebreaker.followfbx()
		#generate all animation frames.
		scene = context.scene
		ue4 = bpy.data.objects.get("root")
		if bpy.context.scene.collection.children['Collection'].objects.get(ue4.name) is None:
			bpy.context.scene.collection.children['Collection'].objects.link(ue4)
		ue4.select_set(True)
		bpy.context.view_layer.objects.active = ue4
		bpy.ops.object.mode_set(mode='POSE')
		BoneBreaker.selectAllBones(bpy.context.view_layer.objects.active, True)
		bpy.context.view_layer.objects.active = bpy.data.objects.get("rig")
		bpy.ops.object.mode_set(mode='POSE')
		bpy.data.objects.get("rig").select_set(True)
		scene = context.scene
		bpy.ops.nla.bake(
			frame_start=scene.frame_start,
			frame_end=scene.frame_end,
			step=1,
			only_selected=True,
			visual_keying=True,
			clear_constraints=False,
			clear_parents=False,
			use_current_action=True,
			bake_types={'POSE'})
		#remove UE4 Armor.
		ue4.select_set(False)
		bpy.context.scene.collection.children['Collection'].objects.unlink(ue4)

		#de-select all.
		#bpy.ops.pose.select_all(action='DESELECT')
		#remove the follow settings
		bpy.ops.bonebreaker.follownone()
		#return to the rig since we keyed everything we can.
		bpy.ops.bonebreaker.followrig()
		
		#return to object mode.
		BoneBreaker.setObj()
		#Go pose mode - should be layer 1 rig.
		bpy.ops.object.select_all(action='DESELECT')
		#select rig.
		context.view_layer.objects.active = bpy.data.objects["rig"]
		bpy.ops.object.mode_set(mode='POSE')
		#deselect all.
		bpy.ops.pose.select_all(action='DESELECT')
		#reset poles. Disabled bacause poles aren't keyed in the UE4 anim. causes issues.
		#rigify_function = "rigify_limb_toggle_pole_"
		#rigify_function = rigify_function+bpy.data.objects['rig'].data['rig_id']
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="upper_arm_parent.L", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["upper_arm_ik.L", "MCH-forearm_ik.L", "MCH-upper_arm_ik_target.L"]\', ctrl_bones=\'["upper_arm_ik.L", "hand_ik.L", "upper_arm_ik_target.L"]\', extra_ctrls=\'[""]\', use_pole=True)')
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="upper_arm_parent.R", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["upper_arm_ik.R", "MCH-forearm_ik.R", "MCH-upper_arm_ik_target.R"]\', ctrl_bones=\'["upper_arm_ik.R", "hand_ik.R", "upper_arm_ik_target.R"]\', extra_ctrls=\'[""]\', use_pole=True)')
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="thigh_parent.R", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["thigh_ik.R", "MCH-shin_ik.R", "MCH-thigh_ik_target.R"]\', ctrl_bones=\'["thigh_ik.R", "foot_ik.R", "thigh_ik_target.R"]\', extra_ctrls=\'[""]\', use_pole=True)')
		#eval("bpy.ops.pose."+rigify_function+'(prop_bone="thigh_parent.L", pole_prop="pole_vector", fk_bones=\'[""]\', ik_bones=\'["thigh_ik.L", "MCH-shin_ik.L", "MCH-thigh_ik_target.L"]\', ctrl_bones=\'["thigh_ik.L", "foot_ik.L", "thigh_ik_target.L"]\', extra_ctrls=\'[""]\', use_pole=True)')
		#done.
		print("All set, the anim was keyed, the UE4 skeleton changes were reversed, you can anim and export as normal")
		
		return {'FINISHED'}

class BONEBREAKER_OT_followfbx(bpy.types.Operator):
	"""Follow the imported FBX animation with the rig.
does not isolate the animations"""
	bl_idname = "bonebreaker.followfbx"
	bl_label = "Follow the imported FBX animation with the rig. (does not isolate the animations)"
	@classmethod
	def poll(cls, context):
		if bpy.data.objects.get("root") is not None:
			armature = bpy.data.objects.get("root")
			if armature.animation_data is not None:
				if armature.animation_data.action is None:
					return False
			else:
				return False
		else:
			return False
		return context.scene.frame_end > 1 and bpy.data.objects.get("root") is not None and bpy.data.objects.get("rig") is not None

	def execute(self, context):
		print("followfbx")
		BoneBreaker.setObj()
		if bpy.data.objects.get("rig") is not None and bpy.data.objects.get("root") is not None:
			ue4 = bpy.data.objects.get("root")
			rig = bpy.data.objects.get("rig")
			rig.select_set(True)
			context.view_layer.objects.active = rig
			BoneBreaker.IK_bones_follow(rig)
			#move to layer 0 to perform operations
			#bpy.context.scene.collection.children['Collection'].objects.link(ue4)
			bpy.context.view_layer.layer_collection.children['UE4'].exclude=False
			armature = bpy.data.objects.get("root")
			armature.select_set(True)
			context.view_layer.objects.active = armature
			bpy.ops.object.mode_set(mode='EDIT')
			BoneBreaker.rigRootAdd(armature, rig)
			#bpy.ops.object.mode_set(mode='EDIT')
			#bpy.ops.edit.select_all(action='SELECT')
			#BoneBreaker.adjustConstraintReverse(armature)
			#armature.select_set(False)
			#bpy.context.scene.collection.children['Collection'].objects.unlink(ue4)
		else:
			bpy.context.window_manager.popup_menu(BoneBreaker.popup, title="NO Metarig something's not right, generate one.", icon='ERROR')
		return {'FINISHED'}
class BONEBREAKER_OT_follownone(bpy.types.Operator):
	"""Remove all constraints from both the rig, and the FBX"""
	bl_idname = "bonebreaker.follownone"
	bl_label = "Remove all constraints from both the rig, and the FBX"
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is not None and bpy.data.objects.get("rig") is not None

	def execute(self, context):
		BoneBreaker.setObj()
		if bpy.data.objects.get("root") is not None:
			ue4 = bpy.data.objects.get("root")
			#move to layer 0 to perform operations
			if bpy.context.scene.collection.children['Collection'].objects.get(ue4.name) is None:
				bpy.context.scene.collection.children['Collection'].objects.link(ue4)
			ue4.select_set(True)
			context.view_layer.objects.active = ue4
			BoneBreaker.clearConstraint(ue4)
			#Make invisible on layer again.
			bpy.context.scene.collection.children['Collection'].objects.unlink(ue4)
			print("removed constraints from UE4")
			BoneBreaker.rigRootRem(ue4)
            #Remove constraints from Rig
			#rig = bpy.data.objects.get("rig")
			#rig.select_set(True)
			#context.view_layer.objects.active = rig
			#BoneBreaker.removeRigConstraint(rig)
			#print("removed constraints from Rig")
		return {'FINISHED'}
class BONEBREAKER_OT_followrig(bpy.types.Operator):
	"""Go back to having the mannequin follow the rig.
Also removed unneeded bones from UE4"""
	bl_idname = "bonebreaker.followrig"
	bl_label = "Go back to having the mannequin follow the rig - also removed unneeded bones from UE4."
	@classmethod
	def poll(cls, context):
		return bpy.data.objects.get("root") is not None and bpy.data.objects.get("rig") is not None

	def execute(self, context):
		print("following the rig")
		#Remove constraints from Rig
		rig = bpy.data.objects.get("rig")
		rig.select_set(True)
		context.view_layer.objects.active = rig
		print("removed constraints from Rig")
		BoneBreaker.setObj()
		rig.select_set(False)
		if bpy.data.objects.get("root") is not None:
			ue4 = bpy.data.objects.get("root")
			#move to layer 0 to perform operations
			if bpy.context.scene.collection.children['Collection'].objects.get(ue4.name) is None:
				bpy.context.scene.collection.children['Collection'].objects.link(ue4)
			ue4.select_set(True)
			context.view_layer.objects.active = ue4
			bpy.ops.object.mode_set(mode='POSE')
			BoneBreaker.adjustConstraint(ue4)
			BoneBreaker.deleteUE4rigBones(ue4)
			ue4.select_set(False)
			bpy.context.scene.collection.children['Collection'].objects.unlink(ue4)
			BoneBreaker.IK_bones_follow(rig)
			#BoneBreaker.copy_loc(rig)
		else:
			bpy.context.window_manager.popup_menu(BoneBreaker.popup, title="NO Metarig something's not right, generate one.", icon='ERROR')
		return {'FINISHED'}
class BONEBREAKER_OT_animkeyall(bpy.types.Operator):
	"""Key all the animations for export!
Selects and bakes appropriate bones."""
	bl_idname = "bonebreaker.animkeyall"
	bl_label = "Key all the animations for export!"
	@classmethod
	def poll(cls, context):
		if bpy.data.objects.get("rig") is not None:
			armature = bpy.data.objects.get("rig")
			if armature.animation_data is not None:
				if armature.animation_data.action is None:
					return False
			else:
				return False
		else:
			return False
		return bpy.data.objects.get("root") is not None and bpy.data.objects.get("rig") is not None

	def execute(self, context):
		BoneBreaker.setObj()
		#select none at all.
		for ob in bpy.context.scene.collection.children['Collection'].objects: ob.select_set(False)
		#disable collection and jump to UE4.
		bpy.context.window.view_layer.layer_collection.children['Collection'].exclude = True
		bpy.context.window.view_layer.layer_collection.children['UE4'].exclude = False
		#select the root rig.
		UE4 = bpy.context.scene.collection.children['UE4'].objects.get("root")
		context.view_layer.objects.active = UE4
		#with the object select go to pose mode.
		UE4.select_set(True)
		bpy.ops.object.mode_set(mode='POSE')
		#select all bones.
		BoneBreaker.selectAllBones(context.view_layer.objects.active, True)
        #Run the bake
		print("baking...")
		scene = context.scene
		bpy.ops.nla.bake(
			frame_start=scene.frame_start,
			frame_end=scene.frame_end,
			step=1,
			only_selected=True,
			visual_keying=True,
			clear_constraints=True,
			clear_parents=False,
			use_current_action=True,
			bake_types={'POSE'})
		print("Baked.")
		#deselect absolutely all.
		for ob in bpy.context.scene.collection.children['UE4'].objects: ob.select_set(False)
		#in case
		UE4.select_set(False)
		#disable UE4 and jump to Collection
		bpy.context.window.view_layer.layer_collection.children['Collection'].exclude = False
		bpy.context.window.view_layer.layer_collection.children['UE4'].exclude = True
		#select the rig as active
		rig = context.view_layer.objects.active = bpy.context.scene.collection.children['Collection'].objects.get('rig')
		#all done.
		bpy.ops.object.mode_set(mode='POSE')
		bpy.ops.bonebreaker.follownone()
		bpy.ops.bonebreaker.followrig()
		print("done, ready for export")
		return {'FINISHED'}
		
class BONEBREAKER_OT_animkey(bpy.types.Operator):
	"""Key all the selected bones - useful directly on rig or ue4 bones if doing manual keying"""
	bl_idname = "bonebreaker.animkey"
	bl_label = "Key all the selected bones - useful directly on rig if doing manual keying"
	@classmethod
	def poll(cls, context):
		if context.view_layer.objects.active:
			if bpy.data.objects.get('root') is not None:
				if context.view_layer.objects.active == bpy.data.objects['root']:
					return False
			else:
				return True
			if bpy.data.objects.get('rig') is not None:
				if context.view_layer.objects.active == bpy.data.objects['rig']:
					return False
			else:
				return True
		else:
			return False
		return bpy.context.selected_pose_bones is not None and bpy.context.object.mode == 'POSE'
		
		
	def execute(self, context):
		scene = context.scene
		bpy.ops.nla.bake(
			frame_start=scene.frame_start,
			frame_end=scene.frame_end,
			step=1,
			only_selected=True,
			visual_keying=True,
			clear_constraints=False,
			clear_parents=False,
			use_current_action=True,
			bake_types={'POSE'})
		return {'FINISHED'}
		
class BONEBREAKER_OT_addkeyframe(bpy.types.Operator):
	"""Add an animation keyframe"""
	bl_idname = "bonebreaker.addkeyframe"
	bl_label = "Add an animation keyframe"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.selected_pose_bones is not None and bpy.context.object.mode == 'POSE'
	def execute(self, context):
		bpy.ops.pose.visual_transform_apply()
		bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
		return {'FINISHED'}

class BONEBREAKER_OT_clearkeyframe(bpy.types.Operator):
	"""Delete an animation keyframe"""
	bl_idname = "bonebreaker.clearkeyframe"
	bl_label = "Delete an animation keyframe"
	@classmethod
	def poll(cls, context):
		return bpy.context.selected_pose_bones is not None and bpy.context.object.mode == 'POSE'
	def execute(self, context):
		bpy.ops.anim.keyframe_delete_v3d()
		return {'FINISHED'}

class BONEBREAKER_OT_clearallselected(bpy.types.Operator):
	"""Remove ALL keyframe entries for selected item"""
	bl_idname = "bonebreaker.clearallselected"
	bl_label = "Remove ALL keyframe entries for selected item"
	
	@classmethod
	def poll(cls, context):
		return bpy.context.selected_pose_bones is not None and bpy.context.object.mode == 'POSE'

	def execute(self, context):
		if context.view_layer.objects.active is not None:
			bpy.ops.anim.keyframe_clear_v3d()
		return {'FINISHED'}

class BONEBREAKER_OT_clearvertcolor(bpy.types.Operator):
	"""Set vertex paint values to 0 on all channels"""
	bl_idname = "bonebreaker.clearvertcolor"
	bl_label = "Set vertex paint values to 0 on all channels"
	@classmethod
	def poll(cls, context):
		return bpy.context.view_layer.objects.active

	def execute(self, context):
		mode = context.active_object.mode
		bpy.ops.object.mode_set(mode = 'OBJECT')
		ob = bpy.context.active_object
		my_object = ob.data
		vert_list = my_object.vertices
		color_map_collection = my_object.vertex_colors
		if len(color_map_collection) == 0:
			color_map_collection.new()
		color_map = color_map_collection['Col']
		i=0
		for poly in my_object.polygons:
			for idx in poly.loop_indices:
				loop = my_object.loops[idx]
				v = loop.vertex_index
				x = 0
				y = 0
				z = 0
				t = 0
				final = (x,y,z,t)
				color_map.data[i].color = final
				i += 1
		# set to vertex paint mode to see the result
		bpy.ops.object.mode_set(mode='VERTEX_PAINT')
		return {'FINISHED'}

class BONEBREAKER_OT_enablenvphysview(bpy.types.Operator):
	"""Enable the PhisX distance view"""
	bl_idname = "bonebreaker.enablenvphysview"
	bl_label = "Enable displaying of vector distance based on vertex paint color"
	bl_description = "Start line drawing operator"
	bl_options = {'REGISTER'}
	
	def __init__(self):
		self.draw_handle = None
		self.draw_event = None
		self.vertices = []
		self.vertex_colors = []
		self.visited = []
		self.buffer = [[None,None,None]]

	def invoke(self, context, event):
		if (bpy.types.Object.BoneBreaker_modal_status==0):
			bpy.types.Object.BoneBreaker_modal_status=1
			if context.active_object.mode!="VERTEX_PAINT":
				bpy.ops.paint.vertex_paint_toggle()
			self.create_batch()
			args = (self, context)
			self.register_handlers(args, context)
			context.window_manager.modal_handler_add(self)
			return {"RUNNING_MODAL"}
		else:
			bpy.types.Object.BoneBreaker_modal_status=0
			self.finish(context)
			return {'FINISHED'}

	def register_handlers(self, args, context):
		self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, args, "WINDOW", "POST_VIEW")
		self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

	def unregister_handlers(self, context):
		if self.draw_event:
			context.window_manager.event_timer_remove(self.draw_event)
			self.draw_event = None
		if self.draw_handle:
			bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
			self.draw_handle = None

	def modal(self, context, event):
		if context.area:
			context.area.tag_redraw()
		if context.active_object.mode!="VERTEX_PAINT":
			bpy.types.Object.BoneBreaker_modal_status=0
			self.unregister_handlers(context)
			return {'CANCELLED'}
		if event.type in {"ESC"}:
			bpy.types.Object.BoneBreaker_modal_status=0
			self.unregister_handlers(context)
			return {'CANCELLED'}
		if (bpy.types.Object.BoneBreaker_modal_status==0):
			self.unregister_handlers(context)
			return {'CANCELLED'}
		if event.type in {"RIGHTMOUSE"}:
			self.update_batch()
			#self.update_batch(self.find_nearest_vert(context, event))
			return {'RUNNING_MODAL'}
		return {'PASS_THROUGH'}

	def finish(self,context):
		self.unregister_handlers(context)
		return {'FINISHED'}

	def create_batch(self):
		ob = bpy.context.object
		index = 0
		if ob.type == 'MESH':
			loops = len(ob.data.loops)
			verts = len(ob.data.vertices)
			#go through each vert
			if len(self.visited)==0:
				for vcol in ob.data.vertex_colors:
					self.visited = verts * [False]
					colors = {}
			l=0
			for l in range(loops):
				v = ob.data.loops[l].vertex_index
				#vd=ob.data.loops[l]
				c = vcol.data[l].color
				if not self.visited[v]:
					colors[v] = c
					self.visited[v] = True
                #Set the lenght of line based on vertex color value
				scale=0
				div=0
				length = (bpy.context.object.BoneBreaker_vertexlen)#*(bpy.context.scene.unit_settings.scale_length)
				if c[0] > 0:
					scale =(length*c[0])
					div = div+1
				if c[1] > 0:
					scale =scale+(length*c[1])
					div = div+1
				if c[2] > 0:
					scale =scale+(length*c[2])
					div = div+1
				if c[3] > 0:
					if "VCM" in bpy.context.object.data.vertex_colors.active.name is False:
						scale =scale+(length*c[3])
						div = div+1
				if div == 0:
					div=1
				scale = (scale/div)
				#Define the vertex positions for lines.
				VertLOC=(bpy.context.view_layer.objects.active.matrix_world @ bpy.context.view_layer.objects.active.data.vertices[v].co)
				self.vertices.append(VertLOC)
				#Double vertex colors because a line is 2 points.
				color = (c[0],c[1],c[2],c[3])
				self.vertex_colors.append(color)
				buffer_item = [VertLOC,color,bpy.context.view_layer.objects.active.data.vertices[v].normal]
				self.buffer.append(buffer_item)
				self.vertices.append(VertLOC+(bpy.context.view_layer.objects.active.data.vertices[v].normal* scale))
				self.vertex_colors.append(color)
				buffer_item = [VertLOC+(bpy.context.view_layer.objects.active.data.vertices[v].normal* scale),color,bpy.context.view_layer.objects.active.data.vertices[v].normal]
				self.buffer.append(buffer_item)
        #Setup the batch for drawing.
		self.shader = gpu.shader.from_builtin('3D_FLAT_COLOR')
		self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.vertices, "color": self.vertex_colors})

	def draw_callback(self, op, context):
		self.shader.bind()
		#self.shader.uniform_float("color", self.vertex_colors)
		self.batch.draw(self.shader)
	def update_batch(self): #add ,VertID for alternate
		obj=bpy.context.view_layer.objects.active
		for id, v in enumerate(self.buffer):
			#Change only tils:
			if id > 0 and id%2==0:
				#print(id, ":", v[0],v[1],v[2])
				if v[2] != None:
					c=bpy.context.active_object.data.vertex_colors.active.data[math.ceil(id/2)-1].color
					length = (bpy.context.object.BoneBreaker_vertexlen)#*(bpy.context.scene.unit_settings.scale_length)
					div=0
					scale=0
					if c[0] > 0:
						scale =(length*c[0])
						div = div+1
					if c[1] > 0:
						scale =scale+(length*c[1])
						div = div+1
					if c[2] > 0:
						scale =scale+(length*c[2])
						div = div+1
					if c[3] > 0:
						if "VCM" in bpy.context.object.data.vertex_colors.active.name is False:
							scale =scale+(length*c[3])
							div = div+1
					if div == 0:
						div=1
					scale = (scale/div)
					v[0] = self.buffer[id-1][0]+v[2]*scale
					v[1] = bpy.context.active_object.data.vertex_colors.active.data[math.ceil(id/2)-1].color
					if id <= len(self.vertices):
						self.vertices[id-1] = v[0]
					if id <= len(self.vertex_colors):
						self.vertex_colors[id-1] = v[1]
		self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.vertices, "color": self.vertex_colors})
            
	def find_nearest_vert(self, context, event):
		""" Technically a good idea, but vert paint changes many more verts then this can detect"""
		#Base args.
		scene = context.scene
		region = context.region
		rv3d = context.region_data
		coord = event.mouse_region_x, event.mouse_region_y
        # standard info for ray
		view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
		ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        #Base self contained functions used in the script below.
		def getObj():
			yield (bpy.context.view_layer.objects.active, bpy.context.view_layer.objects.active.matrix_world)

		def obj_ray_cast(obj, matrix):
			matrix_inv = matrix.inverted()
			bv = mathutils.bvhtree.BVHTree.FromObject(obj, bpy.context.evaluated_depsgraph_get())
			location, normal, face_index, success = bv.ray_cast(matrix_inv @ ray_origin, view_vector @ matrix)
			if success:
				return location, normal, face_index
			else:
				return None, None, None    
        # cast rays and find the closest object
		best_length_squared = -1.0
		for obj, matrix in getObj():
			hit, normal, face_index = obj_ray_cast(obj, matrix)
			if hit is not None:
				hit_world = matrix.inverted() @ hit
				vidx = [v for v in obj.data.polygons[face_index].vertices]
				verts = np.array([matrix @ obj.data.vertices[v].co for v in obj.data.polygons[face_index].vertices])
				vecs = verts - np.array(hit_world)
				closest = vidx[np.argmin(np.einsum('ij,ij->i', vecs, vecs))]
				length_squared = (hit_world - ray_origin).length_squared
				if obj is None or length_squared < best_length_squared:
					best_length_squared = length_squared
				return closest 

def register():
	bpy.utils.register_class(BONEBREAKER_OT_AddFeature)
	bpy.utils.register_class(BONEBREAKER_OT_FBXimportUE4)
	bpy.utils.register_class(BONEBREAKER_OT_FBXimport)
	bpy.utils.register_class(BONEBREAKER_OT_exportmannequin)
	bpy.utils.register_class(BONEBREAKER_OT_FBXexport)
	bpy.utils.register_class(BONEBREAKER_OT_all)
	bpy.utils.register_class(BONEBREAKER_OT_metarig)
	bpy.utils.register_class(BONEBREAKER_OT_rigify)
	bpy.utils.register_class(BONEBREAKER_OT_followfbx)
	bpy.utils.register_class(BONEBREAKER_OT_followrig)
	bpy.utils.register_class(BONEBREAKER_OT_follownone)
	bpy.utils.register_class(BONEBREAKER_OT_animall)
	bpy.utils.register_class(BONEBREAKER_OT_animkeyall)
	bpy.utils.register_class(BONEBREAKER_OT_animkey)
	bpy.utils.register_class(BONEBREAKER_OT_addkeyframe)
	bpy.utils.register_class(BONEBREAKER_OT_clearkeyframe)
	bpy.utils.register_class(BONEBREAKER_OT_clearallselected)
	bpy.utils.register_class(BONEBREAKER_OT_clearvertcolor)
	bpy.utils.register_class(BONEBREAKER_OT_enablenvphysview)
def unregister():
	bpy.utils.unregister_class(BONEBREAKER_OT_enablenvphysview)
	bpy.utils.unregister_class(BONEBREAKER_OT_clearvertcolor)
	bpy.utils.unregister_class(BONEBREAKER_OT_clearallselected)
	bpy.utils.unregister_class(BONEBREAKER_OT_clearkeyframe)
	bpy.utils.unregister_class(BONEBREAKER_OT_addkeyframe)
	bpy.utils.unregister_class(BONEBREAKER_OT_animkey)
	bpy.utils.unregister_class(BONEBREAKER_OT_animkeyall)
	bpy.utils.unregister_class(BONEBREAKER_OT_animall)
	bpy.utils.unregister_class(BONEBREAKER_OT_follownone)
	bpy.utils.unregister_class(BONEBREAKER_OT_followrig)
	bpy.utils.unregister_class(BONEBREAKER_OT_followfbx)
	bpy.utils.unregister_class(BONEBREAKER_OT_rigify)
	bpy.utils.unregister_class(BONEBREAKER_OT_metarig)
	bpy.utils.unregister_class(BONEBREAKER_OT_all)
	bpy.utils.unregister_class(BONEBREAKER_OT_FBXexport)
	bpy.utils.unregister_class(BONEBREAKER_OT_exportmannequin)
	bpy.utils.unregister_class(BONEBREAKER_OT_FBXimport)
	bpy.utils.unregister_class(BONEBREAKER_OT_FBXimportUE4)
	bpy.utils.unregister_class(BONEBREAKER_OT_AddFeature)