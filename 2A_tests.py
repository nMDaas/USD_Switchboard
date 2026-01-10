import maya.cmds as cmds
import maya.mel as mel

graph_shape = cmds.createNode("bifrostGraphShape", name="myBifrostGraph")

# Add a create_usd_stage node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::Stage,create_usd_stage")

# Add an add_to_stage node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::Stage,add_to_stage")

#Connect create_usd_stage to add_to_stage node
cmds.vnnConnect(f"{graph_shape}", "/create_usd_stage.stage", "/add_to_stage.stage")