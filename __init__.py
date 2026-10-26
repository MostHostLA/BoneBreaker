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
bl_info = {
	"name": "BoneBreaker",
	"description": "Automagical rigify for Unreal Engine 4 Mannequin",
	"author": "Andy Fattoracci @ MostHostLA.com",
	"version": (3, 5, 0),
	"blender": (2, 80, 0),
	"location": "Armature properties, Bone properties, View3d tools panel, Armature Add menu",
	"warning": "", # used for warning icon and text in addons panel
	"tracker_url": "http://mosthostla.com/gamedev/contact/",
	"wiki_url": "http://mosthostla.com/gamedev/bonebreaker",
	"category": "Rigging"}

# ---------------------#
#   Reload Process?    #
# ---------------------#
if "bpy" in locals():
	import importlib
	# ---------------------#
	#    User Interface    #
	# ---------------------#
	importlib.reload(ui)
	importlib.reload(operators)
else:
	# ---------------------#
	#    User Interface    #
	# ---------------------#
	from . import ui, operators#, bbimport_fbx

import bpy
from bpy.props import (
	StringProperty,
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
# ------------------------------------------------------------------------
#    Needed everywhere.
# ------------------------------------------------------------------------
def selectLayer(layernum):
    bools = []
    for i in range(20):
        if layernum == i:
            bools.append(True)
        else:
            bools.append(False)
    return tuple(bools)

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------
def register():
	ui.register()
	operators.register()
def unregister():
	operators.unregister()
	ui.unregister()
if __name__ == "__main__":
    register()