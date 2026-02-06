import sys
my_script_dir = "/Users/natashadaas/USD_Switchboard/src" 
if my_script_dir not in sys.path:
    sys.path.append(my_script_dir)

from usd_utils import get_selected_usd_xform_prim

class VariantAuthoringTool:
    def __init__(self, _tool_name):
        self.tool_name = _tool_name
        self.targetPrim = get_selected_usd_xform_prim()

    def getToolName(self):
        return self.tool_name
    
    def getTargetPrimPath(self):
        return self.targetPrim.GetPath()
    
    # Creates a variant set of a given name for a given XForm
    def createVariantSet(self, in_vset_name):
        vset = self.targetPrim.GetVariantSets().AddVariantSet(in_vset_name)
        return vset
    
    #TODO: There should be error checking for if the variant_name already exists for the vset
    def createVariantForSet(self, vset, variant_name, file_path):
        vset.AddVariant(variant_name)

        vset.SetVariantSelection(variant_name)

        # Go inside the variant and add the file reference
        with vset.GetVariantEditContext():
            self.targetPrim.GetReferences().AddReference(file_path)
        
        print(f"Variant '{variant_name}' authored with reference to: {file_path}")
