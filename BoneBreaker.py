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
# HouseKeeping
import bpy
import mathutils
from mathutils import Vector,Quaternion
import math
armatureSet = []
int = 0
#Functions:
def setObj():
	try:
		bpy.ops.armature.select_all(action='DESELECT')
		print("Succeeded deselect")
	except Exception: 
		pass
	try:
		bpy.ops.object.mode_set(mode='OBJECT')
		print("Succeeded obj mode")
	except Exception: 
		pass

def LayerSet(layer):
    booleans = []
    for i in range(20):
        if layer == i:
            booleans.append(True)
        else:
            booleans.append(False)
    return tuple(booleans)
	
def parentUE4(armature):
	"Set the parenting of the metarig to the standard UE4 bones"
	bpy.ops.object.mode_set(mode='EDIT')
	#define the bones for matching.
	MetarigUE4Bone=["spine_02","neck_01","head","spine_03","lowerarm_l","lowerarm_twist_01_l","index_01_l","index_03_l","index_02_l","thumb_03_l","thumb_02_l","thumb_01_l","hand_l","middle_01_l","middle_03_l","middle_02_l","ring_01_l","ring_03_l","ring_02_l","pinky_03_l","pinky_02_l","pinky_01_l","upperarm_l","upperarm_twist_01_l","lowerarm_r","lowerarm_twist_01_r","index_01_r","index_03_r","index_02_r","thumb_03_r","thumb_02_r","thumb_01_r","hand_r","middle_03_r","middle_02_r","middle_01_r","ring_03_r","ring_02_r","ring_01_r","pinky_03_r","pinky_02_r","pinky_01_r","upperarm_r","upperarm_twist_01_r","clavicle_l","clavicle_r","pelvis","thigh_l","thigh_twist_01_l","calf_l","calf_twist_01_l","foot_l","ball_l","thigh_r","thigh_twist_01_r","calf_r","calf_twist_01_r","foot_r","ball_r","spine_01","ik_hand_l","ik_hand_r","ik_hand_gun","ik_foot_l","ik_foot_r","ik_foot_root","ik_hand_root"]
	MetarigBoneParent=["spine.002","spine.005","face","spine.004","forearm.L","lowerarm_l","f_index.01.L","f_index.03.L","f_index.02.L","thumb.03.L","thumb.02.L","thumb.01.L","palm.02.L","f_middle.01.L","f_middle.03.L","f_middle.02.L","f_ring.01.L","f_ring.03.L","f_ring.02.L","f_pinky.03.L","f_pinky.02.L","f_pinky.01.L","upper_arm.L","upperarm_l","forearm.R","lowerarm_r","f_index.01.R","f_index.03.R","f_index.02.R","thumb.03.R","thumb.02.R","thumb.01.R","palm.02.R","f_middle.03.R","f_middle.02.R","f_middle.01.R","f_ring.03.R","f_ring.02.R","f_ring.01.R","f_pinky.03.R","f_pinky.02.R","f_pinky.01.R","upper_arm.R","upperarm_r","shoulder.L","shoulder.R","spine","thigh.L","thigh_l","shin.L","calf_l","foot.L","toe.L","thigh.R","thigh_r","shin.R","calf_r","foot.R","toe.R","spine.001","hand_l","hand_r","hand_r","foot_l","foot_r","pelvis","pelvis"]
	bpy.ops.object.mode_set(mode='EDIT')
	#loop though armature edit bones.
	for bone in armature.data.edit_bones:
		if bone.name in MetarigUE4Bone is not False:
			if MetarigBoneParent[MetarigUE4Bone.index(bone.name)] is not False:
				if armatureSet[0].data.edit_bones[MetarigBoneParent[MetarigUE4Bone.index(bone.name)]] is not False:
					#set the bone parent.
					bone.parent = armatureSet[0].data.edit_bones[MetarigBoneParent[MetarigUE4Bone.index(bone.name)]]

def AdjustRigSuperFingers(armature):
	"Superfingers and hands require a parenting adjustment to function. this is how we get it to comply with the rig."
	bpy.ops.object.mode_set(mode='EDIT')
	MetarigUE4Bone=["ORG-index_01_l","ORG-index_03_l","ORG-index_02_l","ORG-thumb_03_l","ORG-thumb_02_l","ORG-thumb_01_l","ORG-hand_l","ORG-middle_01_l","ORG-middle_03_l","ORG-middle_02_l","ORG-ring_01_l","ORG-ring_03_l","ORG-ring_02_l","ORG-pinky_03_l","ORG-pinky_02_l","ORG-pinky_01_l","ORG-index_01_r","ORG-index_03_r","ORG-index_02_r","ORG-thumb_03_r","ORG-thumb_02_r","ORG-thumb_01_r","ORG-hand_r","ORG-middle_03_r","ORG-middle_02_r","ORG-middle_01_r","ORG-ring_03_r","ORG-ring_02_r","ORG-ring_01_r","ORG-pinky_03_r","ORG-pinky_02_r","ORG-pinky_01_r","ORG-foot_l","ORG-foot_r"]
	MetarigBoneParent=["DEF-f_index.01.L","DEF-f_index.03.L","DEF-f_index.02.L","DEF-thumb.03.L","DEF-thumb.02.L","DEF-thumb.01.L","DEF-palm.02.L","DEF-f_middle.01.L","DEF-f_middle.03.L","DEF-f_middle.02.L","DEF-f_ring.01.L","DEF-f_ring.03.L","DEF-f_ring.02.L","DEF-f_pinky.03.L","DEF-f_pinky.02.L","DEF-f_pinky.01.L","DEF-f_index.01.R","DEF-f_index.03.R","DEF-f_index.02.R","DEF-thumb.03.R","DEF-thumb.02.R","DEF-thumb.01.R","DEF-palm.02.R","DEF-f_middle.03.R","DEF-f_middle.02.R","DEF-f_middle.01.R","DEF-f_ring.03.R","DEF-f_ring.02.R","DEF-f_ring.01.R","DEF-f_pinky.03.R","DEF-f_pinky.02.R","DEF-f_pinky.01.R","ORG-foot.L","ORG-foot.R"]
	#loop though armature edit bones.
	for bone in armature.data.edit_bones:
		if bone.name in MetarigUE4Bone is not None:
			if MetarigBoneParent[MetarigUE4Bone.index(bone.name)] is not None:
				if armature.data.edit_bones.get(MetarigBoneParent[MetarigUE4Bone.index(bone.name)]) is not None:
					#set the bone parent.
					bone.parent = armature.data.edit_bones[MetarigBoneParent[MetarigUE4Bone.index(bone.name)]]

def selectAllBones(armature, state=True):
	for bone in armature.data.bones:
		bone.select = state

def selectUE4Bones(armature):
	"Select all of the UE4 Bones"
	bpy.ops.object.mode_set(mode='EDIT')
	MetarigUE4Bone=["spine_02","neck_01","head","spine_03","lowerarm_l","lowerarm_twist_01_l","index_01_l","index_03_l","index_02_l","thumb_03_l","thumb_02_l","thumb_01_l","hand_l","middle_01_l","middle_03_l","middle_02_l","ring_01_l","ring_03_l","ring_02_l","pinky_03_l","pinky_02_l","pinky_01_l","upperarm_l","upperarm_twist_01_l","lowerarm_r","lowerarm_twist_01_r","index_01_r","index_03_r","index_02_r","thumb_03_r","thumb_02_r","thumb_01_r","hand_r","middle_03_r","middle_02_r","middle_01_r","ring_03_r","ring_02_r","ring_01_r","pinky_03_r","pinky_02_r","pinky_01_r","upperarm_r","upperarm_twist_01_r","clavicle_l","clavicle_r","pelvis","thigh_l","thigh_twist_01_l","calf_l","calf_twist_01_l","foot_l","ball_l","thigh_r","thigh_twist_01_r","calf_r","calf_twist_01_r","foot_r","ball_r","spine_01","ik_hand_l","ik_hand_r","ik_hand_gun","ik_foot_l","ik_foot_r","ik_foot_root","ik_hand_root"]
	RigModifiedUE4Bones=["ORG-spine_02","ORG-neck_01","ORG-head","ORG-spine_03","ORG-lowerarm_l","ORG-lowerarm_twist_01_l","ORG-index_01_l","ORG-index_03_l","ORG-index_02_l","ORG-thumb_03_l","ORG-thumb_02_l","ORG-thumb_01_l","ORG-hand_l","ORG-middle_01_l","ORG-middle_03_l","ORG-middle_02_l","ORG-ring_01_l","ORG-ring_03_l","ORG-ring_02_l","ORG-pinky_03_l","ORG-pinky_02_l","ORG-pinky_01_l","ORG-upperarm_l","ORG-upperarm_twist_01_l","ORG-lowerarm_r","ORG-lowerarm_twist_01_r","ORG-index_01_r","ORG-index_03_r","ORG-index_02_r","ORG-thumb_03_r","ORG-thumb_02_r","ORG-thumb_01_r","ORG-hand_r","ORG-middle_03_r","ORG-middle_02_r","ORG-middle_01_r","ORG-ring_03_r","ORG-ring_02_r","ORG-ring_01_r","ORG-pinky_03_r","ORG-pinky_02_r","ORG-pinky_01_r","ORG-upperarm_r","ORG-upperarm_twist_01_r","ORG-clavicle_l","ORG-clavicle_r","ORG-pelvis","ORG-thigh_l","ORG-thigh_twist_01_l","ORG-calf_l","ORG-calf_twist_01_l","ORG-foot_l","ORG-ball_l","ORG-thigh_r","ORG-thigh_twist_01_r","ORG-calf_r","ORG-calf_twist_01_r","ORG-foot_r","ORG-ball_r","ORG-spine_01","ORG-ik_hand_l","ORG-ik_hand_r","ORG-ik_hand_gun","ORG-ik_foot_l","ORG-ik_foot_r","ORG-ik_foot_root","ORG-ik_hand_root"]
	for bone in armature.data.edit_bones:
		if bone.name in RigModifiedUE4Bones is not False:
			bone.select=True

def AdjustRig4UE4(armature):
	"loop though the rig and move the UE4 bones to the appropriate layer so they can easily be found."
	bpy.ops.object.mode_set(mode='EDIT')
	RigModifiedUE4Bones=["ORG-spine_02","ORG-neck_01","ORG-head","ORG-spine_03","ORG-lowerarm_l","ORG-lowerarm_twist_01_l","ORG-index_01_l","ORG-index_03_l","ORG-index_02_l","ORG-thumb_03_l","ORG-thumb_02_l","ORG-thumb_01_l","ORG-hand_l","ORG-middle_01_l","ORG-middle_03_l","ORG-middle_02_l","ORG-ring_01_l","ORG-ring_03_l","ORG-ring_02_l","ORG-pinky_03_l","ORG-pinky_02_l","ORG-pinky_01_l","ORG-upperarm_l","ORG-upperarm_twist_01_l","ORG-lowerarm_r","ORG-lowerarm_twist_01_r","ORG-index_01_r","ORG-index_03_r","ORG-index_02_r","ORG-thumb_03_r","ORG-thumb_02_r","ORG-thumb_01_r","ORG-hand_r","ORG-middle_03_r","ORG-middle_02_r","ORG-middle_01_r","ORG-ring_03_r","ORG-ring_02_r","ORG-ring_01_r","ORG-pinky_03_r","ORG-pinky_02_r","ORG-pinky_01_r","ORG-upperarm_r","ORG-upperarm_twist_01_r","ORG-clavicle_l","ORG-clavicle_r","ORG-pelvis","ORG-thigh_l","ORG-thigh_twist_01_l","ORG-calf_l","ORG-calf_twist_01_l","ORG-foot_l","ORG-ball_l","ORG-thigh_r","ORG-thigh_twist_01_r","ORG-calf_r","ORG-calf_twist_01_r","ORG-foot_r","ORG-ball_r","ORG-spine_01","ORG-ik_hand_l","ORG-ik_hand_r","ORG-ik_hand_gun","ORG-ik_foot_l","ORG-ik_foot_r","ORG-ik_foot_root","ORG-ik_hand_root"]
	for bone in armature.data.edit_bones:
		if bone.name in RigModifiedUE4Bones is not False:
			bone.layers[31] = False
			bone.layers[24] = True

def clearConstraint(armature): 
	"""Adjust the bones of the armature by remove all constraints and adding in the copy transform"""
	if armature is not None:
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='POSE')
		print("Clear constraints for: ",armature.name)
		if armature.name=="root":
			bpy.ops.pose.select_all(action='SELECT')
			for bone in bpy.context.selected_pose_bones:
				for c in bone.constraints:
					bone.constraints.remove( c )
		else:
			RigIKBones=["foot_ik.L","foot_heel_ik.L","thigh_ik_target.L","thigh_ik.L","foot_ik.R","foot_heel_ik.R","thigh_ik_target.R","thigh_ik.R","hand_ik.L","upper_arm_ik_target.L","upper_arm_ik.L","hand_ik.R","upper_arm_ik_target.R","upper_arm_ik.R","torso","hips","chest","shoulder.L","shoulder.R","neck","head"]
			#start selecting the correct bones in pose mode.
			for index, bone in enumerate(RigIKBones):
				if armature.data.bones.get(bone) is not None:
					armature.data.bones.get(bone).select = True
			#loop the selected bones and remove / add constraint.
			for bone in bpy.context.selected_pose_bones:
				#delete previous constraint
				for c in bone.constraints:
					bone.constraints.remove( c )
		bpy.ops.object.mode_set(mode='OBJECT')

def IK_bones_follow(armature):
	""" Reset the IK bones within the rig so they follow the correct parents with copy transforms"""
	IKBones=["ORG-ik_hand_l","ORG-ik_hand_r","ORG-ik_hand_gun","ORG-ik_foot_l","ORG-ik_foot_r","ORG-ik_foot_root","ORG-ik_hand_root"]
	RigBoneParent=["ORG-hand_l","ORG-hand_r","ORG-hand_r","ORG-foot_l","ORG-foot_r","root","root"]
	if armature.name=="rig":
		#select armor.
		bpy.context.view_layer.objects.active = armature
		#enter pose mode.
		bpy.ops.object.mode_set(mode='POSE')
		#Set regular IK to follow as defined.
		for id, IKBone in enumerate(IKBones):
			if armature.pose.bones[IKBone] is not None:
				bone = armature.pose.bones[IKBone]
				if armature.pose.bones[RigBoneParent[id]] is not None:
					for c in bone.constraints:
						bone.constraints.remove( c )
					constraint = bone.constraints.new('COPY_TRANSFORMS')
					constraint.target = bpy.context.scene.collection.children['Collection'].objects["rig"]
					constraint.subtarget = RigBoneParent[id]
	#All done.
def addrigconstraint(armature):
    """Setup inverse rig follow copy constraints."""
    DoubleHelixReverseP=["spine","spine.001","spine.002","spine.003","spine.005","spine.006","thigh.L","shin.L","foot.L","thigh.R","shin.R","foot.R","shoulder.L","upper_arm.L","forearm.L","shoulder.R","upper_arm.R","forearm.R","hand.L","hand.R","toe.L","toe.R"]
    #ensure correct armor selection + pose mode.
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    for bone in DoubleHelixReverseP:
        if armature.pose.bones.get("ORG-" + bone + "_Follow") is not None:
            boneA = armature.pose.bones.get("ORG-" + bone + "_Follow")
            #print(boneA.name)
            for c in boneA.constraints:
                boneA.constraints.remove( c )
            constraint = boneA.constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.context.scene.collection.children['Collection'].objects["rig"]
            constraint.subtarget = "ORG-" + bone
def remrigconstraint(armature):
    """Remove the constraints on the base rig."""
    DoubleHelixReverseP=["spine","spine.001","spine.002","spine.003","spine.005","spine.006","thigh.L","shin.L","foot.L","thigh.R","shin.R","foot.R","shoulder.L","upper_arm.L","forearm.L","shoulder.R","upper_arm.R","forearm.R","hand.L","hand.R","toe.L","toe.R"]
    #ensure correct armor selection + pose mode.
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    for bone in DoubleHelixReverseP:
        if armature.pose.bones.get("ORG-" + bone + "_Follow") is not None:
            boneA = armature.pose.bones.get("ORG-" + bone + "_Follow")
            #print(boneA.name)
            for c in boneA.constraints:
                boneA.constraints.remove( c )
def adjustConstraint(armature):
	"""Adjust the bones of the armature by remove all constraints and add in the copy transform"""
	if armature.name=="root":
		#deselect all.
		for ob in bpy.context.scene.collection.children['Collection'].objects: ob.select_set(False)
		#select active armature.
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='POSE')
		#select all bones.
		bpy.ops.pose.select_all(action='SELECT')
		for bone in bpy.context.selected_pose_bones:
			for c in bone.constraints:
				bone.constraints.remove( c )
			if bpy.context.scene.collection.children['Collection'].objects["rig"].data.bones.get("ORG-"+bone.name) is not None:
				constraint = bone.constraints.new('COPY_ROTATION')
				constraint.target = bpy.context.scene.collection.children['Collection'].objects["rig"]
				constraint.subtarget = "ORG-"+bone.name
				constraint = bone.constraints.new('COPY_LOCATION')
				constraint.target = bpy.context.scene.collection.children['Collection'].objects["rig"]
				constraint.subtarget = "ORG-"+bone.name
		bpy.ops.object.mode_set(mode='OBJECT')
		#not sure what this was...
		#armature.layers[0] = False
	else:
		print("Could not find UE4 Mannequin to associate")
	#Remove extra UE4 Bones if they exist. the anim was cut and made to follow they need to be removed for export.
	
def removeRigConstraint(armature):
    bonesFollow=["ORG-spine_Follow","ORG-spine.001_Follow","ORG-spine.002_Follow","ORG-spine.003_Follow","ORG-spine.005_Follow","ORG-spine.006_Follow","ORG-thigh.L_Follow","ORG-shin.L_Follow","ORG-foot.L_Follow","ORG-thigh.R_Follow","ORG-shin.R_Follow","ORG-foot.R_Follow","ORG-shoulder.L_Follow","ORG-upper_arm.L_Follow","ORG-forearm.L_Follow","ORG-shoulder.R_Follow","ORG-upper_arm.R_Follow","ORG-forearm.R_Follow","ORG-hand.L_Follow","ORG-hand.R_Follow","ORG-toe.L_Follow","ORG-toe.R_Follow"]
    for index, bonename in enumerate(bonesFollow):
        if armature.pose.bones.get(bonename) is not None:
            bone = armature.pose.bones.get(bonename)
            for c in bone.constraints:
                bone.constraints.remove( c )
def adjustConstraintReverse(armature):
    """Adjust the rig to follow the root"""
    bonesFollow=["ORG-spine_Follow","ORG-spine.001_Follow","ORG-spine.002_Follow","ORG-spine.003_Follow","ORG-spine.005_Follow","ORG-spine.006_Follow","ORG-thigh.L_Follow","ORG-shin.L_Follow","ORG-foot.L_Follow","ORG-thigh.R_Follow","ORG-shin.R_Follow","ORG-foot.R_Follow","ORG-shoulder.L_Follow","ORG-upper_arm.L_Follow","ORG-forearm.L_Follow","ORG-hand.L_Follow","ORG-shoulder.R_Follow","ORG-upper_arm.R_Follow","ORG-forearm.R_Follow","ORG-hand.R_Follow","ORG-toe.L_Follow","ORG-toe.R_Follow"]
    bonesMetarig=["ORG-pelvis","ORG-spine_01","ORG-spine_02","ORG-spine_03","ORG-neck_01","ORG-head","ORG-thigh_l","ORG-calf_l","ORG-foot_l","ORG-thigh_r","ORG-calf_r","ORG-foot_r","ORG-clavicle_l","ORG-upperarm_l","ORG-lowerarm_l","ORG-hand_l","ORG-clavicle_r","ORG-upperarm_r","ORG-lowerarm_r","ORG-hand_r","ORG-ball_l","ORG-ball_r"]
    bonesRig=["pelvis","spine_01","spine_02","spine_03","neck_01","head","thigh_l","calf_l","foot_l","thigh_r","calf_r","foot_r","clavicle_l","upperarm_l","lowerarm_l","hand_l","clavicle_r","upperarm_r","lowerarm_r","hand_r","ball_l","ball_r"]
    bonesOrg=["ORG-spine","ORG-spine.001","ORG-spine.002","ORG-spine.003","ORG-spine.005","ORG-spine.006","ORG-thigh.L","ORG-shin.L","ORG-foot.L","ORG-thigh.R","ORG-shin.R","ORG-foot.R","ORG-shoulder.L","ORG-upper_arm.L","ORG-forearm.L","ORG-hand.L","ORG-shoulder.R","ORG-upper_arm.R","ORG-forearm.R","ORG-hand.R","ORG-toe.L","ORG-toe.R"]
    remrigconstraint(armature)
    bpy.ops.object.mode_set(mode='EDIT')
    for index, bonename in enumerate(bonesMetarig):
        if armature.data.edit_bones.get(bonename) is not None:
            bone = armature.data.edit_bones.get(bonename)
            bone.parent = None
    for index, bonename in enumerate(bonesFollow):
        if armature.data.edit_bones.get(bonename) is not None:
            bone = armature.data.edit_bones.get(bonename)
            bone.parent = armature.data.edit_bones.get(bonesMetarig[index])
            #print(bone.name, ' ', bonesMetarig[index])
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')
    for index, bonename in enumerate(bonesMetarig):
        if armature.pose.bones.get(bonename) is not None:
            bone = armature.pose.bones.get(bonename)
            for c in bone.constraints:
                bone.constraints.remove( c )
            constraint = bone.constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.context.scene.collection.children['Collection'].objects["root"]
            constraint.subtarget = bonesRig[index]
    for index, bonename in enumerate(bonesOrg):
        if armature.pose.bones.get(bonename) is not None:
            bone = armature.pose.bones.get(bonename)
            constraint = bone.constraints.new('COPY_TRANSFORMS')
            constraint.target = bpy.context.scene.collection.children['Collection'].objects["rig"]
            constraint.subtarget = bonesFollow[index]
    print("the armor was reverse rigged")
    
def getConstraintInfo(armature):
	RigIKBones=["foot_ik.L","foot_heel_ik.L","thigh_ik_target.L","thigh_ik.L","foot_ik.R","foot_heel_ik.R","thigh_ik_target.R","thigh_ik.R","hand_ik.L","upper_arm_ik_target.L","upper_arm_ik.L","hand_ik.R","upper_arm_ik_target.R","upper_arm_ik.R","torso","hips","chest","shoulder.L","shoulder.R","neck","head"]
	bpy.ops.object.mode_set(mode='POSE')
	for bone in RigIKBones:
		if armature.data.bones.get(bone) is not None:
			armature.data.bones.get(bone).select = True
	for bone in bpy.context.selected_pose_bones:
		for c in bone.constraints:
			print(bone.name, c.target,c.subtarget)
def rigRootAdd(armature,rig):
    """ Create required bone structure inside of the UE4 armor - a bit dangerous for hierarchy. Needs to use Constraints to parent for immidiate removal. """
    RigIKBones=["foot_ik.L","foot_heel_ik.L","thigh_ik.L","foot_ik.R","foot_heel_ik.R","thigh_ik.R","hand_ik.L","upper_arm_ik_target.L","upper_arm_ik.L","hand_ik.R","upper_arm_ik_target.R","upper_arm_ik.R","torso","hips","chest","shoulder.L","shoulder.R","neck","head","spine_fk.001","spine_fk.002","spine_fk.003","tweak_spine.001","f_index.01.L","f_index.02.L","f_index.03.L","thumb.01.L","thumb.02.L","thumb.03.L","f_middle.01.L","f_middle.02.L","f_middle.03.L","f_ring.01.L","f_ring.02.L","f_ring.03.L","f_pinky.01.L","f_pinky.02.L","f_pinky.03.L","f_index.01.R","f_index.02.R","f_index.03.R","thumb.01.R","thumb.02.R","thumb.03.R","f_middle.01.R","f_middle.02.R","f_middle.03.R","f_ring.01.R","f_ring.02.R","f_ring.03.R","f_pinky.01.R","f_pinky.02.R","f_pinky.03.R","thigh_ik_target.L","thigh_ik_target.R"]
    RigParents=["foot_l","foot_l","thigh_l","foot_r","foot_r","thigh_r","hand_l","lowerarm_l","upperarm_l","hand_r","lowerarm_r","upperarm_r","spine_02","pelvis","spine_02","clavicle_l","clavicle_r","neck_01","head","spine_02","spine_02","spine_03","spine_01","index_01_l","index_02_l","index_03_l","thumb_01_l","thumb_02_l","thumb_03_l","middle_01_l","middle_02_l","middle_03_l","ring_01_l","ring_02_l","ring_03_l","pinky_01_l","pinky_02_l","pinky_03_l","index_01_r","index_02_r","index_03_r","thumb_01_r","thumb_02_r","thumb_03_r","middle_01_r","middle_02_r","middle_03_r","ring_01_r","ring_02_r","ring_03_r","pinky_01_r","pinky_02_r","pinky_03_r","calf_l","calf_r"]
    FixLOCA=["thigh_ik_target.L","thigh_ik_target.R","upper_arm_ik_target.L","upper_arm_ik_target.R"]
    FixLOCB=["calf_l","calf_r","lowerarm_l","lowerarm_r"]
    Adjust=[]
    for index, bone in enumerate(RigIKBones):
        if armature.data.edit_bones.get(bone) is not None:
            #This bone exists. we need to create an alias.
            if rig.data.edit_bones.get(bone) is not None:
                oldbone = rig.data.edit_bones.get(bone)
                newbone = armature.data.edit_bones.new(oldbone.name + "_Follow")
                newbone.roll = oldbone.roll
                newbone.tail = oldbone.tail
                newbone.head = oldbone.head
                newbone.use_connect = False
                Adjust.append(oldbone.name)
        else:
            #print(bone, "needs creation");
            if rig.data.edit_bones.get(bone) is not None:
                oldbone = rig.data.edit_bones.get(bone)
                newbone = armature.data.edit_bones.new(oldbone.name)
                newbone.roll = oldbone.roll
                newbone.tail = oldbone.tail
                newbone.head = oldbone.head
                newbone.use_connect = False
                if armature.data.edit_bones.get(RigParents[index]) is not None:
                    parent = armature.data.edit_bones.get(RigParents[index])
                    newbone.parent = parent
    #Fixing extra locations (baiscally the position of the pole affectors).
    for index, bone in enumerate(FixLOCA):
        if armature.data.edit_bones.get(bone) is not None:
            bone = armature.data.edit_bones.get(bone)
            if armature.data.edit_bones.get(FixLOCB[index]) is not None:
                parent = armature.data.edit_bones.get(FixLOCB[index])
                print(parent.name, parent.tail, parent.head)
                loc = parent.tail - parent.head
                bone.tail = armature.matrix_world @ mathutils.Vector( ( (parent.head.x + loc.x), bone.tail.y, bone.tail.z) )
                bone.head = armature.matrix_world @ mathutils.Vector( ( (parent.head.x +  + loc.x), bone.head.y, bone.head.z) )
    for boneName in Adjust:
        #print("adjusting ", bone)
        if armature.data.edit_bones.get(boneName + "_Follow") is not None:
            bone = armature.data.edit_bones.get(boneName + "_Follow")
            if armature.data.edit_bones.get(boneName) is not None:
                boneParent = armature.data.edit_bones.get(boneName)
                bone.parent = boneParent
                #print(bone, " ", boneParent)
    #All bones are added and parent - they now follow the rig. Time to create constraints.
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')
    for index, bone in enumerate(RigIKBones):
        if armature.pose.bones.get(bone + "_Follow") is not None:
            bone = rig.pose.bones.get(bone)
            constraint = bone.constraints.new('COPY_TRANSFORMS')
            constraint.target = armature
            constraint.subtarget = RigIKBones[index] + "_Follow"
        else:
            if rig.pose.bones.get(bone) is not None:
                bone = rig.pose.bones.get(bone)
                constraint = bone.constraints.new('COPY_TRANSFORMS')
                constraint.target = armature
                constraint.subtarget = RigIKBones[index]
    #Extra Adjust (mostly for pelvis)
    SpecialsA=["hips"]
    SpecialsB=["spine_02"]
    for index, bone in enumerate(SpecialsA):
        if armature.pose.bones.get(bone) is not None:
            bone = armature.pose.bones.get(bone)
            constraint = bone.constraints.new('COPY_LOCATION')
            constraint.target = armature
            constraint.subtarget = SpecialsB[index]
    #Fingers have to follow...
    #FingerMetarig=["f_index.01.L","f_index.02.L","f_index.03.L","thumb.01.L","thumb.02.L","thumb.03.L","f_middle.01.L","f_middle.02.L","f_middle.03.L","f_ring.01.L","f_ring.02.L","f_ring.03.L","f_pinky.01.L","f_pinky.02.L","f_pinky.03.L","f_index.01.R","f_index.02.R","f_index.03.R","thumb.01.R","thumb.02.R","thumb.03.R","f_middle.01.R","f_middle.02.R","f_middle.03.R","f_ring.01.R","f_ring.02.R","f_ring.03.R","f_pinky.01.R","f_pinky.02.R","f_pinky.03.R"]
    #FingerRoot=["index_01_l","index_02_l","index_03_l","thumb_01_l","thumb_02_l","thumb_03_l","middle_01_l","middle_02_l","middle_03_l","ring_01_l","ring_02_l","ring_03_l","pinky_01_l","pinky_02_l","pinky_03_l","index_01_r","index_02_r","index_03_r","thumb_01_r","thumb_02_r","thumb_03_r","middle_01_r","middle_02_r","middle_03_r","ring_01_r","ring_02_r","ring_03_r","pinky_01_r","pinky_02_r","pinky_03_r"]
    #for index, bone in enumerate(FingerMetarig):
    #    if rig.pose.bones.get(bone) is not None:
    #        bone = rig.pose.bones.get(bone)
    #        constraint = bone.constraints.new('COPY_TRANSFORMS')
    #        constraint.target = armature
    #        constraint.subtarget = FingerRoot[index]
def rigRootRem(armature):
    """ Remove all created bones. """
    RigIKBones=["foot_ik.L","foot_heel_ik.L","thigh_ik_target.L","thigh_ik.L","foot_ik.R","foot_heel_ik.R","thigh_ik_target.R","thigh_ik.R","hand_ik.L","upper_arm_ik_target.L","upper_arm_ik.L","hand_ik.R","upper_arm_ik_target.R","upper_arm_ik.R","torso","hips","chest","shoulder.L","shoulder.R","neck","spine_fk.001","spine_fk.002","spine_fk.003","tweak_spine.001","f_index.01.L","f_index.02.L","f_index.03.L","thumb.01.L","thumb.02.L","thumb.03.L","f_middle.01.L","f_middle.02.L","f_middle.03.L","f_ring.01.L","f_ring.02.L","f_ring.03.L","f_pinky.01.L","f_pinky.02.L","f_pinky.03.L","f_index.01.R","f_index.02.R","f_index.03.R","thumb.01.R","thumb.02.R","thumb.03.R","f_middle.01.R","f_middle.02.R","f_middle.03.R","f_ring.01.R","f_ring.02.R","f_ring.03.R","f_pinky.01.R","f_pinky.02.R","f_pinky.03.R","thigh_ik_target.L","thigh_ik_target.R"]
    #Remove all follow bones first, so the list above doesn't need to contain them
    # * * * You need to adjst that list still, or you can remove bones that should not be removed * * * #
    bpy.context.view_layer.layer_collection.children['UE4'].exclude=False
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature.data.edit_bones:
        if "_Follow" in bone.name:
            armature.data.edit_bones.remove(bone)
    for index, bone in enumerate(RigIKBones):
        if armature.data.edit_bones.get(bone) is not None:
            bone = armature.data.edit_bones.get(bone)
            armature.data.edit_bones.remove(bone)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.layer_collection.children['UE4'].exclude=True
def deleteUE4rigBones(armature):
	RigIKBones=["foot_ik.L","foot_heel_ik.L","thigh_ik_target.L","thigh_ik.L","foot_ik.R","foot_heel_ik.R","thigh_ik_target.R","thigh_ik.R","hand_ik.L","upper_arm_ik_target.L","upper_arm_ik.L","hand_ik.R","upper_arm_ik_target.R","upper_arm_ik.R","torso","hips","chest","shoulder.L","shoulder.R","neck","head","thumb.01.L","f_index.01.L","f_middle.01.L","f_ring.01.L","f_pinky.01.L","thumb.02.L","f_index.02.L","f_middle.02.L","f_ring.02.L","f_pinky.02.L","thumb.03.L","f_index.03.L","f_middle.03.L","f_ring.03.L","f_pinky.03.L","thumb.01.R","f_index.01.R","f_middle.01.R","f_ring.01.R","f_pinky.01.R","thumb.02.R","f_index.02.R","f_middle.02.R","f_ring.02.R","f_pinky.02.R","thumb.03.R","f_index.03.R","f_middle.03.R","f_ring.03.R","f_pinky.03.R"]
	#check it's the right armor.
	if armature.name.startswith("root") is True:
		#make sure mode is edit.
		bpy.ops.object.mode_set(mode='OBJECT')
		#select armature.
		bpy.context.view_layer.objects.active = armature
		#put armature on layer 0 to work.
		#armature.layers[0] = True
		#Edit Mode!
		bpy.ops.object.mode_set(mode='EDIT') #select all is unnecesary.
		#loop and remove all bones.
		for bone in RigIKBones:
			if armature.data.bones.get(bone) is not None:
				if bone=="head":
					bone=armature.data.edit_bones.get(bone+"_rig")
				else:
					bone=armature.data.edit_bones.get(bone)
				if bone is not None:
					armature.data.edit_bones.remove(bone)
		#back to object mode via function.
		setObj()
		# remove armature from layer again.
		#armature.layers[0] = False
	else:
		print("Surely you did not wish to call the removal script on an armature that isn't the UE4 one...")
def copy_loc(armature):
	""" Force the tight twist to follow the IK / Not use Poles """
	IKBones=["thigh_ik.R","thigh_ik.L"]
	RigBoneParent=["MCH-thigh_ik_stretch.R","MCH-thigh_ik_stretch.L"]
	if armature.name=="rig":
		#select armor.
		bpy.context.view_layer.objects.active = armature
		#enter pose mode.
		bpy.ops.object.mode_set(mode='POSE')
		#Set regular IK to follow as defined.
		for id, IKBone in enumerate(IKBones):
			if armature.pose.bones[IKBone] is not None:
				bone = armature.pose.bones[IKBone]
				if armature.pose.bones[RigBoneParent[id]] is not None:
					for c in bone.constraints:
						bone.constraints.remove( c )
					constraint = bone.constraints.new('COPY_LOCATION')
					constraint.target = bpy.context.scene.collection.children['Collection'].objects["rig"]
					constraint.subtarget = RigBoneParent[id]
	#All done.
def metaBlending2(armature,metarig = None):
	MetarigBone_tail=["palm.01.L","palm.01.R","palm.02.L","palm.02.R","palm.03.L","palm.03.R","palm.04.L","palm.04.R", "hand.L", "hand.R"]
	UnrealBones_tail=["index_01_l","index_01_r","middle_01_l","middle_01_r","ring_01_l","ring_01_r","pinky_01_l","pinky_01_r","middle_01_l","middle_01_r"]
	metarigBones=["pelvis.R","pelvis.L","spine","spine.001","spine.002","spine.003","spine.005","spine.006","thigh.L","shin.L","foot.L","toe.L","thigh.R","shin.R","foot.R","toe.R","shoulder.L","upper_arm.L","forearm.L","shoulder.R","upper_arm.R","forearm.R","thumb.01.L","thumb.02.L","thumb.03.L","f_index.01.L","f_index.02.L","f_index.03.L","f_middle.01.L","f_middle.02.L","f_middle.03.L","f_ring.01.L","f_ring.02.L","f_ring.03.L","f_pinky.01.L","f_pinky.02.L","f_pinky.03.L","thumb.01.R","thumb.02.R","thumb.03.R","f_index.01.R","f_index.02.R","f_index.03.R","f_middle.01.R","f_middle.02.R","f_middle.03.R","f_ring.01.R","f_ring.02.R","f_ring.03.R","f_pinky.01.R","f_pinky.02.R","f_pinky.03.R","hand.L","hand.R"]
	armatureBones=["pelvis","pelvis","pelvis","spine_01","spine_02","spine_03","neck_01","head","thigh_l","calf_l","foot_l","ball_l","thigh_r","calf_r","foot_r","ball_r","clavicle_l","upperarm_l","lowerarm_l","clavicle_r","upperarm_r","lowerarm_r","thumb_01_l","thumb_02_l","thumb_03_l","index_01_l","index_02_l","index_03_l","middle_01_l","middle_02_l","middle_03_l","ring_01_l","ring_02_l","ring_03_l","pinky_01_l","pinky_02_l","pinky_03_l","thumb_01_r","thumb_02_r","thumb_03_r","index_01_r","index_02_r","index_03_r","middle_01_r","middle_02_r","middle_03_r","ring_01_r","ring_02_r","ring_03_r","pinky_01_r","pinky_02_r","pinky_03_r","hand_l","hand_r"]
	tip_tweaks=["f_index.03.L","f_index.03.R","f_middle.03.L","f_middle.03.R","f_ring.03.L","f_ring.03.R","f_pinky.03.L","f_pinky.03.R","thumb.03.L","thumb.03.R"]
	MetarigKnuckleBones=["f_index.01.L","thumb.01.L","f_middle.01.L","f_ring.01.L","f_pinky.01.L","f_index.01.R","thumb.01.R","f_middle.01.R","f_ring.01.R","f_pinky.01.R"]
	follow_parent =["heel.02.R","heel.02.L"]
	toes=["toe.L","toe.R"]
	DoubleHelix=["spine","spine.001","spine.002","spine.003","spine.005","spine.006","thigh.L","shin.L","foot.L","toe.L","thigh.R","shin.R","foot.R","toe.R","shoulder.L","upper_arm.L","forearm.L","shoulder.R","upper_arm.R","forearm.R","thumb.01.L","thumb.02.L","thumb.03.L","f_index.01.L","f_index.02.L","f_index.03.L","f_middle.01.L","f_middle.02.L","f_middle.03.L","f_ring.01.L","f_ring.02.L","f_ring.03.L","f_pinky.01.L","f_pinky.02.L","f_pinky.03.L","thumb.01.R","thumb.02.R","thumb.03.R","f_index.01.R","f_index.02.R","f_index.03.R","f_middle.01.R","f_middle.02.R","f_middle.03.R","f_ring.01.R","f_ring.02.R","f_ring.03.R","f_pinky.01.R","f_pinky.02.R","f_pinky.03.R","hand.L","hand.R"]
	DoubleHelixParent=["","","","","","","","","","","","","","","","","","","","","thumb_01_l","thumb_02_l","thumb_03_l","index_01_l","index_02_l","index_03_l","middle_01_l","middle_02_l","middle_03_l","ring_01_l","ring_02_l","ring_03_l","pinky_01_l","pinky_02_l","pinky_03_l","thumb_01_r","thumb_02_r","thumb_03_r","index_01_r","index_02_r","index_03_r","middle_01_r","middle_02_r","middle_03_r","ring_01_r","ring_02_r","ring_03_r","pinky_01_r","pinky_02_r","pinky_03_r","",""]
	#If no metarig was fed into the function, let's create the thing.
	DoubleHelixReverseA=["pelvis","spine_01","spine_02","spine_03","neck_01","head","thigh_l","calf_l","foot_l","thigh_r","calf_r","foot_r","clavicle_l","upperarm_l","lowerarm_l","clavicle_r","upperarm_r","lowerarm_r","hand_l","hand_r","ball_l","ball_r"]
	DoubleHelixReverseP=["spine_Follow","spine.001_Follow","spine.002_Follow","spine.003_Follow","spine.005_Follow","spine.006_Follow","thigh.L_Follow","shin.L_Follow","foot.L_Follow","thigh.R_Follow","shin.R_Follow","foot.R_Follow","shoulder.L_Follow","upper_arm.L_Follow","forearm.L_Follow","shoulder.R_Follow","upper_arm.R_Follow","forearm.R_Follow","hand.L_Follow","hand.R_Follow","toe.L_Follow","toe.R_Follow"]
	if metarig is None:
		setObj()
		bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
		bpy.ops.object.armature_human_metarig_add()
		bpy.ops.transform.resize(value=(91, 91, 91))
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		metarig = bpy.context.view_layer.objects.active
	#re-check metarig/armature existence
	if armature is not None and armature.name.startswith("root") is not True:
		print("There is no second armor. what are we doing here?")
		#return
	if metarig is not None and metarig.name.startswith("meta") is not True:
		print("no metarig found, must be an error")
		#return
	#tails first, so the heads get fixed.
	for index, UE4Bone in enumerate(UnrealBones_tail):
		#select armature
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='EDIT')
		if armature.data.edit_bones.get(UE4Bone) is not None:
			tmp = armature.matrix_world @ armature.data.edit_bones.get(UE4Bone).head
			#select metarig
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.select_all(action='DESELECT')
			bpy.context.view_layer.objects.active = metarig
			bpy.ops.object.mode_set(mode='EDIT')
			if metarig.data.edit_bones.get(MetarigBone_tail[index]) is not None:
				MetaBone = metarig.data.edit_bones.get(MetarigBone_tail[index])
				MetaBone.head = tmp + -MetaBone.vector
				MetaBone.tail = tmp
	#Object Mode
	bpy.ops.object.mode_set(mode='OBJECT')
	#select both armatures
	armature.select_set(True)
	metarig.select_set(True)
	#EditMode
	bpy.ops.object.mode_set(mode='EDIT')
	#deselect bones (may not matter).
	bpy.ops.armature.select_all(action='DESELECT')
	
	for bone in armature.data.edit_bones:
		#print(bone.name)
		if armature.data.edit_bones.get(bone.name) is not None:
			Editbone = armature.data.edit_bones.get(bone.name)
			boneTail = armature.matrix_world @ Editbone.tail
			boneHead = armature.matrix_world @ Editbone.head
			boneRoll = Editbone.roll
			boneParent = Editbone.parent
			boneParentName = None
			if boneParent is not None:
				boneParentName = boneParent.name
			if metarig.data.edit_bones.get(bone.name) is None:
				#Debug Line - useful to check what's going on.
				#print(armature.name, "\t",bone.name, " ",Editbone.name, "\t\t",boneParentName, boneTail, boneHead, boneRoll)
                #create it.
				newbone = metarig.data.edit_bones.new(bone.name)
				if boneParentName is not None:
					newbone.parent = metarig.data.edit_bones.get(boneParentName)
				newbone.use_connect = False
				newbone.tail = metarig.matrix_world @ boneTail
				newbone.head = metarig.matrix_world @ boneHead
				newbone.roll = boneRoll
	#Adjust position of the relative parent bone. need to work out a list...
	for index, armatureBone in enumerate(armatureBones):
		if armature.data.edit_bones.get(armatureBone) is not None:
			armatureBone = armature.data.edit_bones.get(armatureBone)
			#print(armatureBone.name)
			if metarig.data.edit_bones.get(metarigBones[index]) is not None:
				metarigBone = metarig.data.edit_bones.get(metarigBones[index])
				#print(metarigBone.name)
				metarigBone.head = armatureBone.head
	#Correct finger tips.
	for tipbone in tip_tweaks:
		if metarig.data.edit_bones.get(tipbone) is not None:
			tipbone = metarig.data.edit_bones.get(tipbone)
			parent = tipbone.parent
			#print(tipbone.name, "\t", parent,"\t",parent.vector)
			tipbone.tail = tipbone.head + ( (parent.vector / 8) * 6.18)
	for toebone in toes:
		if metarig.data.edit_bones.get(toebone) is not None:
			toebone = metarig.data.edit_bones.get(toebone)
			tmp = toebone.head.y + -toebone.vector.length
			tmp = mathutils.Vector( (toebone.head.x, tmp, toebone.head.z) )
			toebone.tail = tmp
			#print(toebone.name, toebone.head, toebone.tail)
    #correct heel controls
	for index, MetaBone in enumerate(follow_parent):    
		#select armature
		if metarig.data.edit_bones.get(MetaBone) is not None:
			MetaBone = metarig.data.edit_bones.get(MetaBone)
			if MetaBone.parent is not None:
				tmp = metarig.matrix_world @ MetaBone.parent.head
				length = MetaBone.length / 2
				if tmp.x > 0:
					tail = mathutils.Vector( (tmp.x + length, tmp.y, 0) )
					head = mathutils.Vector( (tmp.x - length, tmp.y, 0) )
				else:
					tail = mathutils.Vector( (tmp.x - length, tmp.y, 0) )
					head = mathutils.Vector( (tmp.x + length, tmp.y, 0) )
				MetaBone.tail = tail
				MetaBone.head = head
			else:
				print("impossible")
			#select metarig
    #correct feet tips.
    #Arbitrary? correct the spine node.
	BoneA = metarig.data.edit_bones.get("spine_03").head
	BoneB = metarig.data.edit_bones.get("neck_01").head
	Spot = BoneB + BoneA
	Spot = Spot / 2
	metarig.data.edit_bones.get("spine.004").head = metarig.matrix_world @ Spot
	metarig.data.edit_bones.get("spine.003").tail = metarig.matrix_world @ Spot
	bpy.ops.object.mode_set(mode='OBJECT')
	#Everything else should be ready. Adjust the face.
	bpy.context.view_layer.objects.active = metarig
	bpy.ops.object.mode_set(mode='EDIT')
	#deselct all.
	bpy.ops.armature.select_all(action='DESELECT')
	#get the face.
	face = metarig.data.edit_bones.get("face")
	face.select = True
	face.parent.select_tail = True
	metarig.data.edit_bones.active = face
	#select all the face children
	bpy.ops.armature.select_similar(type="CHILDREN")
	#find where to go (in line with head bone), we only need Y
	destination = metarig.data.edit_bones.get("head").head.y - face.parent.tail.y
	if face.parent.tail.y <= destination:
		bpy.ops.transform.transform(mode='TRANSLATION', value=(0, destination, 0, 0))
    # ***************************************#
	#     Create DoubleHelix System bones    #
	# ************************************** #
	for index, MetaBone in enumerate(DoubleHelix):
		if metarig.data.edit_bones.get(MetaBone) is not None:
			NewBoneName = MetaBone + "_Follow"
			MetaBone = metarig.data.edit_bones.get(MetaBone)
			NewBone = metarig.data.edit_bones.new(NewBoneName)
			newbone.use_connect = False
			NewBone.head = MetaBone.head
			NewBone.tail = MetaBone.tail
			NewBone.roll = MetaBone.roll
			if DoubleHelixParent[index]!="" :
				NewBone.parent = metarig.data.edit_bones.get(DoubleHelixParent[index])
				newbone.use_connect = True
	for index, MetaBone in enumerate(DoubleHelixReverseA):
		if metarig.data.edit_bones.get(MetaBone) is not None:
			MetaParent = metarig.data.edit_bones.get(DoubleHelixReverseP[index])
			MetaBone = metarig.data.edit_bones.get(MetaBone)
			MetaBone.parent = MetaParent
			print(MetaBone.name, " follows ", MetaParent.name)
    # ************************************** #
    # ***************************************#
	#   Create the new Shoulder Twist bones  #
	# ************************************** #
	newbone = metarig.data.edit_bones.new("upperarm_twist_ctrl_l")
	newbone.parent = metarig.data.edit_bones["upper_arm.L"]
	newbone.use_connect = False
	#Places the bone's head in the correct spot.
	newbone.head = metarig.data.edit_bones['upperarm_twist_01_l'].head
	#sets the tail multiplied out into the far distance
	newbone.tail = mathutils.Vector((newbone.head[0],  newbone.head[1] * 10, newbone.head[2]))
	#cuts the bone lenght back to a decent value.
	newbone.length = 20
	#Make this new bone the parent of the actual twist bone.
	metarig.data.edit_bones['upperarm_twist_01_l'].parent = newbone;
	newbone = metarig.data.edit_bones.new("upperarm_twist_ctrl_r")
	newbone.parent = metarig.data.edit_bones["upper_arm.R"]
	newbone.use_connect = False
	#Places the bone's head in the correct spot.
	newbone.head = metarig.data.edit_bones['upperarm_twist_01_r'].head
	#sets the tail multiplied out into the far distance
	newbone.tail = mathutils.Vector((newbone.head[0],  newbone.head[1] * 10, newbone.head[2]))
	#cuts the bone lenght back to a decent value.
	newbone.length = 20
	#Make this new bone the parent of the actual twist bone.
	metarig.data.edit_bones['upperarm_twist_01_r'].parent = newbone;
    #change out to Pose Mode for super fingers!
	bpy.ops.object.mode_set(mode='POSE')
	metarig.pose.bones
	#bpy.context.selected_pose_bones[0]['rigify_type'] = 'limbs.super_finger'
	for MetaBoneName in MetarigKnuckleBones:
		if metarig.pose.bones.get(MetaBoneName) is not None:
			metarig.pose.bones.get(MetaBoneName)['rigify_type'] = 'limbs.super_finger'
	#Adjust the legs! foot rotation to non auto.        
	metarig.pose.bones.get("thigh.L")['rigify_parameters']['rotation_axis'] = 0
	metarig.pose.bones.get("thigh.L")['rigify_parameters']['auto_align_extremity'] = 0
	metarig.pose.bones.get("thigh.R")['rigify_parameters']['rotation_axis'] = 0
	metarig.pose.bones.get("thigh.R")['rigify_parameters']['auto_align_extremity'] = 0
	# ***************************************#
	#   Adjust the new Shoulder Twist bones  #
	# ************************************** #
	metarig.pose.bones.get("upperarm_twist_ctrl_l")['rigify_type'] = 'basic.super_copy'
	metarig.pose.bones.get("upperarm_twist_ctrl_r")['rigify_type'] = 'basic.super_copy'
	for layer in metarig.data.bones['upperarm_twist_ctrl_l'].layers:
		layer = False
	for layer in metarig.data.bones.get("upperarm_twist_ctrl_r").layers:
		layer = False
	metarig.data.bones.get("upperarm_twist_ctrl_l").layers[7] = True
	metarig.data.bones.get("upperarm_twist_ctrl_r").layers[10] = True
	#finish out.
	for ob in bpy.context.scene.collection.children['Collection'].objects: ob.select_set(False)
	bpy.ops.object.mode_set(mode='OBJECT')

def popup(self, context, txt_Text=""):
	 self.layout.label(text=txt_Text)
