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
    
    def getTargetPrim(self):
        return self.targetPrim
