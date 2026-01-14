import ufe
import mayaUsd.ufe
from pxr import Usd, UsdGeom

# Gets the selected USD prim in the outliner
def get_selected_usd_prim():
    # Get the current UFE (Universal Front End) selection made by user in outliner
    selection = ufe.GlobalSelection.get()

    # TODO: Error should be generated if nothing was selected
    if selection.empty():
        print("Nothing selected.")
        return None
    
    # Get last item in the selection
    selected_item = list(selection)[-1]

    # Convert UFE path object to a string path
    ufe_path_obj = selected_item.path()
    ufe_path_string = ufe.PathString.string(ufe_path_obj)

    # Access prim via string path
    prim = mayaUsd.ufe.ufePathToPrim(ufe_path_string)
    
    # Ensure prim is an Xform
    if (not prim.IsA(UsdGeom.Xform)):
        #TODO: Error should be generated if XForm was not selected
        print("XForm prim must be selected for variant set creation.")

    return prim

# Creates a variant set of a given name for a given XForm
def createVariantSet(Xf_selected, in_vset_name):
    vset = Xf_selected.GetVariantSets().AddVariantSet(in_vset_name)
    return vset

# Currently kind of a "dummy" implementation - num is to create spheres of different radii
#TODO: There should be error checking for if the variant_name already exists for the vset
def createVariantForSet(stage, Xf_path, vset, variant_name, num):
    vset.AddVariant(variant_name)

    vset.SetVariantSelection(variant_name)

    # Dummy for demonstration purposes
    with vset.GetVariantEditContext():
        sphere = UsdGeom.Sphere.Define(stage, f"{Xf_path}/geometry")
        sphere.GetRadiusAttr().Set(num)

# TODO: This is assumed, which it should not be (?)
proxy_shape_path = "|stage1|stageShape1"
stage = mayaUsd.ufe.getStage(proxy_shape_path)

# Get Xform selected
Xf_selected = get_selected_usd_prim()
Xf_path = Xf_selected.GetPath() # this is the path that is preceded by '/', so not the ufe path

# Create a variant set for the XForm prim selected
# TODO: The variant set name should come from the user 
vset = createVariantSet(Xf_selected, "MyVariantSet")

# TODO: variant names should come from the user
# TODO: variant content should also come from the user
createVariantForSet(stage, Xf_path, vset, "vs_1", 3.0)
createVariantForSet(stage, Xf_path, vset, "vs_2", 1.0)