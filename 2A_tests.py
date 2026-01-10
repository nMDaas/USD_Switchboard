import maya.cmds as cmds

graph_shape = cmds.createNode("bifrostGraphShape", name="myBifrostGraph")

# Add a create_usd_stage node
mel.eval(
    f'vnnCompound "{graph_shape}" "/" '
    f'-addNode "BifrostGraph,USD::Stage,create_usd_stage";'
)
