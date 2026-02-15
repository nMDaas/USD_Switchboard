import os
import sys
import shutil
import maya.cmds as cmds

tool_root = cmds.fileDialog2(dialogStyle=2, fileMode=3, caption="Select Root Directory folder")[0]
script_folder = os.path.join(tool_root, "src")
icon_folder = os.path.join(tool_root, "icons")

# Add scripts to sys.path -------------------------------------------------------------------------
if script_folder not in sys.path:
    sys.path.append(script_folder)

# Copy icons --------------------------------------------------------------------------------------
maya_icon_folder = os.path.join(cmds.internalVar(userPrefDir=True), "icons")
os.makedirs(maya_icon_folder, exist_ok=True)
for icon in os.listdir(icon_folder):
    shutil.copy2(os.path.join(icon_folder, icon), maya_icon_folder)

# Create a shelf if it doesn't exist --------------------------------------------------------------
shelf_name = "NatashaUSDTools"
if not cmds.shelfLayout(shelf_name, exists=True):
    cmds.shelfLayout(shelf_name, parent="ShelfLayout")

# Add buttons -------------------------------------------------------------------------------------
import importlib

# Add button for UsdFileVariantAuthor_exec_tool.py ------------------------------------------------
import UsdFileVariantAuthor_exec_tool # your main script

# Remove button if it exists
buttons = cmds.shelfLayout(shelf_name, q=True, ca=True) or []
for btn in buttons:
    if cmds.shelfButton(btn, q=True, label=True) == "Usd_File_Variant_Author":
        cmds.deleteUI(btn)

cmds.shelfButton(
    parent=shelf_name,
    label="Usd_File_Variant_Author",
    imageOverlayLabel="",
    image="UsdFileVariant_AIcon.png",
    command=f'''
import sys
tool_root = r"{tool_root}"
if tool_root not in sys.path:
    sys.path.append(tool_root)

import src.UsdFileVariantAuthor_exec_tool as tool
importlib.reload(tool)
''',
    annotation="Runs Usd_File_Variant_Author",
    sourceType="Python"
)

# Add button TransformVariantAuthor_exec_tool.py ----------------------------------------------------
import TransformVariantAuthor_exec_tool # your main script

# Remove button if it exists
buttons = cmds.shelfLayout(shelf_name, q=True, ca=True) or []
for btn in buttons:
    if cmds.shelfButton(btn, q=True, label=True) == "Transform_Variant_Author":
        cmds.deleteUI(btn)

cmds.shelfButton(
    parent=shelf_name,
    label="Transform_Variant_Author",
    imageOverlayLabel="",
    image="TransformVariant_AIcon.png",
    command=f'''
import sys
tool_root = r"{tool_root}"
if tool_root not in sys.path:
    sys.path.append(tool_root)

import src.TransformVariantAuthor_exec_tool as tool
importlib.reload(tool)
''',
    annotation="Runs Transform_Variant_Author",
    sourceType="Python"
)

print("✅ NatashaUSDTools installed!")
