# Example for connecting nodes in Bifrost graph editor
# Resource: https://help.autodesk.com/cloudhelp/ENU/Bifrost-Tech-Docs/CommandsPython/vnnConnect.html
import maya.cmds as cmds

import maya.mel as mel
cmds.file(new=1, f=1)
mel.eval("createNewBifrostGraphCmd()")

cmds.vnnCompound("bifrostGraphShape1","/", addNode="BifrostGraph,Core::Math,add")
cmds.vnnCompound("bifrostGraphShape1","/", addNode="BifrostGraph,Core::Math,subtract")

cmds.vnnNode("bifrostGraphShape1", "/subtract", createInputPort=("input", "auto"))
cmds.vnnConnect("bifrostGraphShape1", "/add.output", "/subtract.input")