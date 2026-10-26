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
import bpy
from . import operators

from bpy.props import (StringProperty,
						BoolProperty,
						IntProperty,
						FloatProperty,
						EnumProperty,
						PointerProperty,
						)
from bpy.types import (Panel,
						Operator,
						PropertyGroup,
						)

if bpy.app.version < (2,80,0):
	Region = "TOOLS"
else:
	Region = "UI"
    
def create_properties():
    bpy.types.Object.BoneBreaker_vertexlen = bpy.props.IntProperty(name="lenght", description="Multiplier of the cloth distance in cm.", default=100, min=0, max=1000, soft_min=0, soft_max=1000)
    #bpy.types.Object.vertexlen=100
    #bpy.types.Object.modal_status = bpy.props.IntProperty(name="Modal Status", description="Status of draw operator", default=0)
    bpy.types.Object.BoneBreaker_modal_status=0
def remove_properties():
    del(bpy.types.Object.BoneBreaker_vertexlen)
    del(bpy.types.Object.BoneBreaker_modal_status)
    
class BoneBreaker_Import(bpy.types.Panel):
	"""Creates the addon's Import panel """
	bl_idname = "BONEBREAKER_PT_import"
	bl_label = "Import"
	bl_space_type = "VIEW_3D"
	bl_region_type = Region
	bl_category = "BoneBreaker"
	def draw(self, context):
		obj = context.object
		scene = context.scene
		#layout info.
		layout = self.layout
		row = layout.row()
		#Buttons
		row = layout.row(align=True)
		row.operator("bonebreaker.fbximport", text="FBX", icon='IMPORT')
		if hasattr(bpy.types, "UE4FBX_OT_importfbx") is not False:
			row.operator("bonebreaker.fbximportue4", text="UE4", icon='KEYTYPE_JITTER_VEC')
		else:
			row.operator("bonebreaker.addfeature", text="UE4", icon='KEYTYPE_JITTER_VEC')
		
class BoneBreaker_Metarig(bpy.types.Panel):
	"""Creates the addon's Metarig Control panel """
	bl_idname = "BONEBREAKER_PT_metarig"
	bl_label = "Char Rigging"
	bl_space_type = "VIEW_3D"
	bl_region_type = Region
	bl_category = "BoneBreaker"
	def draw(self, context):
		obj = context.object
		scene = context.scene
		#layout info.
		layout = self.layout
		row = layout.column()
		#Buttons
		row.operator("bonebreaker.all", text="DO IT ALL", icon='PLUGIN')
		row.label(text="Separate Parts:")
		row = layout.row(align=True)
		row.operator("bonebreaker.metarig", text="Metarig", icon='OUTLINER_OB_ARMATURE')
		row.operator("bonebreaker.rigify", text="Rigify", icon='POSE_HLT')

class BoneBreaker_Actions(bpy.types.Panel):
	"""Creates the addon's Actions panel """
	bl_idname = "BONEBREAKER_PT_actions"
	bl_label = "Rig Actions"
	bl_space_type = "VIEW_3D"
	bl_region_type = Region
	bl_category = "BoneBreaker"
	def draw(self, context):
		obj = context.object
		scene = context.scene
		#layout info.
		layout = self.layout
		row = layout.column()
		#Buttons
		row.operator("bonebreaker.animall", text="Do it All", icon='MOD_PARTICLES')
		row.label(text="Follow what?")
		row = layout.row(align=True)
		row.operator("bonebreaker.followfbx", text="UE4", icon='POSE_HLT')
		row.operator("bonebreaker.follownone", text="No", icon='SNAP_OFF')
		row.operator("bonebreaker.followrig", text="My", icon='OUTLINER_DATA_ARMATURE')
		
class BoneBreaker_Animations(bpy.types.Panel):
	"""Creates the addon's Animation panel """
	bl_idname = "BONEBREAKER_PT_animations"
	bl_label = "Animation"
	bl_space_type = "VIEW_3D"
	bl_region_type = Region
	bl_category = "BoneBreaker"
	def draw(self, context):
		obj = context.object
		scene = context.scene
		#layout info.
		layout = self.layout
		row = layout.column()
		row.operator("bonebreaker.animkeyall", text="Key All Frames", icon='PARTICLE_DATA')
		row.label(text="Anim what?")
		row.operator("bonebreaker.animkey", text="Key Active", icon='OUTLINER_DATA_CAMERA')
		split = layout.split()
		#Frame column
		col = split.column(align=True)
		col.label(text="FrameRange")
		col.prop(scene, "frame_start")
		col.prop(scene, "frame_end")
		col = split.column(align=True)
		col.label(text="Keyframe")
		col.operator("bonebreaker.addkeyframe", text="Add", icon='ZOOM_IN')
		col.operator("bonebreaker.clearkeyframe", text="Remove", icon='ZOOM_OUT')
		
		#split = layout.split()
		#col = split.column()
		#col.operator("bonebreaker.addallselected", text="Add All", icon='REC')
		#col = split.column(align=True)
		row = layout.column()
		row.operator("bonebreaker.clearallselected", text="Remove All Selected", icon='LIBRARY_DATA_BROKEN')
		
class BoneBreaker_NVCloth(bpy.types.Panel):
	"""Creates the addon's NvCloth panel """
	bl_idname = "BONEBREAKER_PT_nvcloth"
	bl_label = "Nv Cloth"
	bl_space_type = "VIEW_3D"
	bl_region_type = Region
	bl_category = "BoneBreaker"
	def draw(self, context):
		obj = context.object
		scene = context.scene
		#layout info.
		layout = self.layout
		row = layout.column()
		if obj:
			row.operator("bonebreaker.clearvertcolor", text="Remove Color", icon='CANCEL')
			row.prop(obj, "BoneBreaker_vertexlen", text="Distance", icon="PHYSICS")
        
		if (bpy.types.Object.BoneBreaker_modal_status==0):
			custom_text = "Enable View"
		else :
			custom_text = "Disable View"
		row.operator("bonebreaker.enablenvphysview", text=custom_text, icon='OUTLINER_DATA_CAMERA')
		split = layout.split()
		#Frame column

class BoneBreaker_Export(bpy.types.Panel):
	"""Creates the addon's Export panel """
	bl_idname = "BONEBREAKER_PT_export"
	bl_label = "Export"
	bl_space_type = "VIEW_3D"
	bl_region_type = Region
	bl_category = "BoneBreaker"
	def draw(self, context):
		obj = context.object
		scene = context.scene
		#layout info.
		layout = self.layout
		row = layout.column()
		#Buttons
				
		row.label(text="FPS Rate:")
		row = layout.split()
		row.prop(scene.render, "fps")
		row.prop(scene.render, "fps_base", text="Base")
		row = layout.column()
		row.label(text="Export File:")
		row = layout.row(align=True)
		row.operator('bonebreaker.exportmannequin', text="Rig", icon='MOD_ARMATURE')
		row.operator('bonebreaker.fbxexport', text="FBX", icon='FILE_3D').type="OFF" 
		row = layout.row(align=True)
		row.operator('bonebreaker.fbxexport', text="Edges", icon='MOD_EDGESPLIT').type="EDGE"
		row.operator('bonebreaker.fbxexport', text="Faces", icon='MOD_OPACITY').type="FACE"
		row.operator('bonebreaker.fbxexport', text="Mixer", icon='GREASEPENCIL').type="MIXER"

def register():
	create_properties()
	bpy.utils.register_class(BoneBreaker_Import)
	bpy.utils.register_class(BoneBreaker_Metarig)
	bpy.utils.register_class(BoneBreaker_Actions)
	bpy.utils.register_class(BoneBreaker_Animations)
	bpy.utils.register_class(BoneBreaker_NVCloth)
	bpy.utils.register_class(BoneBreaker_Export)

def unregister():
	remove_properties()
	bpy.utils.unregister_class(BoneBreaker_Export)
	bpy.utils.unregister_class(BoneBreaker_NVCloth)
	bpy.utils.unregister_class(BoneBreaker_Animations)
	bpy.utils.unregister_class(BoneBreaker_Actions)
	bpy.utils.unregister_class(BoneBreaker_Metarig)
	bpy.utils.unregister_class(BoneBreaker_Import)