import maya.cmds as cmds
import maya.mel as mel

graph_shape = cmds.createNode("bifrostGraphShape", name="myBifrostGraph")

# Add a create_usd_stage node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::Stage,create_usd_stage")

# Add an add_to_stage node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::Stage,add_to_stage")

# Connect add_to_stage node to output node
cmds.vnnNode(f"{graph_shape}", "/output", createInputPort=("out_stage", "BifrostUsd::Stage"))
cmds.vnnConnect(f"{graph_shape}", "/add_to_stage.out_stage", "/output.out_stage")

# Connect create_usd_stage to add_to_stage node
cmds.vnnConnect(f"{graph_shape}", "/create_usd_stage.stage", "/add_to_stage.stage")

# Add a define_usd_prim / Xform node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::Prim,define_usd_prim")
# Connect it to add_to_stage prim_definitions port
cmds.vnnNode(f"{graph_shape}", "/add_to_stage", createInputPort=("prim_definitions.prim_definition", "Object"))
cmds.vnnConnect(f"{graph_shape}", "/define_usd_prim.prim_definition", "/add_to_stage.prim_definitions.prim_definition")

# Add a define_usd_variant_set node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::VariantSet,define_usd_variant_set")
# Connect it to define_usd_prim variant_set_definitions port
cmds.vnnNode(f"{graph_shape}", "/define_usd_prim", createInputPort=("variant_set_definitions.variant_set_definition", "Object"))
cmds.vnnConnect(f"{graph_shape}", "/define_usd_variant_set.variant_set_definition", "/define_usd_prim.variant_set_definitions.variant_set_definition")

# Add a define_usd_mesh node
cmds.vnnCompound(f"{graph_shape}","/", addNode="BifrostGraph,USD::Prim,define_usd_mesh")
# Connect it to define_usd_prim children port
cmds.vnnNode(f"{graph_shape}", "/define_usd_prim", createInputPort=("children.mesh_definition", "Object"))
cmds.vnnConnect(f"{graph_shape}", "/define_usd_mesh.mesh_definition", "/define_usd_prim.children.mesh_definition")