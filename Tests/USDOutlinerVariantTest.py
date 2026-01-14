import mayaUsd.ufe
from pxr import Usd, UsdGeom, Sdf

# 1. Access the existing stage
proxy_shape_path = "|stage1|stageShape1"
stage = mayaUsd.ufe.getStage(proxy_shape_path)

# 2. Get the specific prim for your existing Xform
# (Assuming the path you used previously was /my_new_xform)
xform_path = "/my_new_xform"
xform_prim = stage.GetPrimAtPath(xform_path)

if xform_prim.IsValid():
    # 3. Create (or get) the VariantSet named "ModelConfig"
    vset = xform_prim.GetVariantSets().AddVariantSet("ModelConfig")
    
    # 4. Add variant names
    vset.AddVariant("HighDetail")
    vset.AddVariant("LowDetail")
    
    # 5. Author content for 'HighDetail'
    vset.SetVariantSelection("HighDetail")
    with vset.GetVariantEditContext():
        # We create a Sphere inside the HighDetail variant
        sphere = UsdGeom.Sphere.Define(stage, f"{xform_path}/geometry")
        sphere.GetRadiusAttr().Set(2.0)
        
    # 6. Author content for 'LowDetail'
    vset.SetVariantSelection("LowDetail")
    with vset.GetVariantEditContext():
        # We create a Cube at the SAME path inside the LowDetail variant
        cube = UsdGeom.Cube.Define(stage, f"{xform_path}/geometry")
        cube.GetSizeAttr().Set(1.0)
        
    # 7. Set the default state
    vset.SetVariantSelection("HighDetail")
    
    print(f"VariantSet 'ModelConfig' added to {xform_path}")
else:
    print(f"Error: Prim at {xform_path} not found!")