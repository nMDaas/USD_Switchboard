import maya.cmds as cmds
import mayaUsd.ufe
from pxr import UsdGeom

# 1. Get the USD Stage from the Maya node name
# Use the full DAG path to the shape node
proxy_shape_path = "|stage1|stageShape1" 
stage = mayaUsd.ufe.getStage(proxy_shape_path)

if stage:
    # 2. Define a new Xform prim
    # This authors the prim in the current "Edit Target" layer
    xform_path = "/my_new_xform"
    new_xform = UsdGeom.Xform.Define(stage, xform_path)
    
    print(f"Successfully created {xform_path} in stage: {stage}")
else:
    cmds.error("Could not find the USD Stage. Check your proxy shape path.")

# Define a Sphere under the Xform we created earlier
sphere_path = "/my_new_xform/my_sphere"
sphere_prim = UsdGeom.Sphere.Define(stage, sphere_path)

# You can now set attributes on the sphere
sphere_prim.GetRadiusAttr().Set(2.0)