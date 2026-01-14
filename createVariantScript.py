import ufe
import mayaUsd.ufe
from pxr import Usd, UsdGeom

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

# Get Xform selected
Xform_selected = get_selected_usd_prim()