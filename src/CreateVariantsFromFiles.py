# Details

# Instructions: to run, navigate to execute_tool.py and run the file

from PySide6.QtCore import * 
from PySide6.QtGui import *
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
from functools import partial
import maya.cmds as cmds
from maya import OpenMayaUI
from pathlib import Path
from shiboken6 import wrapInstance
from functools import wraps
import math
import os
import ufe
import mayaUsd.ufe
from pxr import Usd, UsdGeom

def one_undo(func):
    """
    Decorator - guarantee close chunk.
    type: (function) -> function
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrap

# Gets the selected USD XForm in the outliner
#TODO: possibly can be moved into a utils file
def get_selected_usd_xform_prim():
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
#TODO: move into a special utils file because this will be used everywhere
def createVariantSet(Xf_selected, in_vset_name):
    vset = Xf_selected.GetVariantSets().AddVariantSet(in_vset_name)
    return vset

# Get number variant sets for XForm
# TODO: Warning if XForm not selected
def getVariantSets(Xf_selected):
    vsets = Xf_selected.GetVariantSets()
    return vsets

#TODO: There should be error checking for if the variant_name already exists for the vset
def createVariantForSet(Xf_prim, vset, variant_name, file_path):
    vset.AddVariant(variant_name)

    vset.SetVariantSelection(variant_name)

    # Go inside the variant and add the file reference
    with vset.GetVariantEditContext():
        Xf_prim.GetReferences().AddReference(file_path)
    
    print(f"Variant '{variant_name}' authored with reference to: {file_path}")
        
#show gui window
def showWindow():
    # get this files location so we can find the .ui file in the /ui/ folder alongside it
    UI_FILE = str(Path(__file__).parent.resolve() / "gui.ui")
    loader = QUiLoader()
    file = QFile(UI_FILE)
    file.open(QFile.ReadOnly)
     
    #Get Maya main window to parent gui window to it
    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    ui = loader.load(file, parentWidget=mayaMainWindow)
    file.close()
    
    ui.setParent(mayaMainWindow)
    ui.setWindowFlags(Qt.Window)
    ui.setWindowTitle('Create Variants From USD Files')
    ui.setObjectName('Create Variants From USD Files')
    ui.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    global default_initial_directory
    # TODO: should check if this works in Windows
    default_initial_directory = cmds.workspace(query=True, rootDirectory=True) 

    # stores [row, filepath]
    global usd_filepath_dict
    usd_filepath_dict = {}

    # set targetPrim - the XForm that will have the variant
    targetPrim = get_selected_usd_xform_prim()
    targetPrimPath = targetPrim.GetPath()
    ui.targetPrim.setText(f"Target Prim: {targetPrimPath}")

    def add_existing_variant_row(v_name):
        label = QLabel(f"Variant: ")
        variant_name_label = QLineEdit()

        # Set name of variant name and as read only
        variant_name_label.setText(v_name)
        variant_name_label.setReadOnly(True)
        
        # Get new row index
        rowIndex = ui.gridLayout.rowCount()

        # Add to the grid layout in new row
        ui.gridLayout.addWidget(label, rowIndex, 0)
        ui.gridLayout.addWidget(variant_name_label, rowIndex, 1)  

    def populateVariantSet(vset_name):
        variants = vset_name.GetVariantNames()
        for v in variants:
            add_existing_variant_row(v)

    # Check if the targetPrim already has a variant or not
    # Either: 
    # (A) It has a variant set, and we can edit the variant set
    # or (B) It does not have a variant set and we can create a new one
    # TODO: Should account for other kinds of variant sets so this might look different later
    vsets = getVariantSets(targetPrim)
    vset_names = vsets.GetNames()
    global creatingNewVariant
    creatingNewVariant = True
    if (len(vset_names) > 0):
        creatingNewVariant = False
        # Variant set already exists on targetPrim 
        existing_vs_name = vset_names[0]

        # Set in the UI so the user knows there is already a variant on the targetPrim
        ui.vs_name_input.setText(existing_vs_name)

        # TODO: this is currently only populating the first one
        vset = vsets.GetVariantSet(existing_vs_name)
        populateVariantSet(vset)

    # icon paths
    global open_folder_icon
    open_folder_icon = Path(__file__).parent / "icons" / "open-folder.png"
    folder_chosen_icon = Path(__file__).parent / "icons" / "open-folder-confirmed.png"

    # open dialog for user to select USD file - linked to row number
    def openDialogForUSDFileSelection(row_number):
        select_button = ui.findChild(QPushButton, f"select_button_{row_number}")

        global default_initial_directory

        dialog = QFileDialog()
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setDirectory(default_initial_directory)
        dialog.setWindowTitle("Select USD File")

        # show which filename was selected if a folder was selected
        if dialog.exec_():
            file_selected = dialog.selectedFiles()[0]
            global usd_filepath_dict
            usd_filepath_dict[row_number] = file_selected

            # set default_initial_directory so it's easier for the user
            default_initial_directory = str(Path(file_selected).parent)
            select_button.setIcon(QIcon(str(folder_chosen_icon)))
        else:
            select_button.setIcon(QIcon(str(open_folder_icon)))  

    def add_variant_row():
        global open_folder_icon

        # Create widgets
        label = QLabel(f"Variant: ")
        variant_name_line_edit = QLineEdit()
        folderButton = QPushButton()

        # Setting folderButton settings
        folderButton.setIcon(QIcon(str(open_folder_icon)))
        folderButton.setIconSize(QSize(22,22))
        folderButton.setFlat(True)

        # Get new row index
        rowIndex = ui.gridLayout.rowCount()

        # if this is the first variant, set name automatically to "Default"
        if (rowIndex == 1):
            variant_name_line_edit.setText("Default")

        # Setting object names
        variant_name_line_edit.setObjectName(f"variant_input_{rowIndex}")
        folderButton.setObjectName(f"select_button_{rowIndex}")

        # Add to the grid layout in new row
        ui.gridLayout.addWidget(label, rowIndex, 0)
        ui.gridLayout.addWidget(variant_name_line_edit, rowIndex, 1)    
        ui.gridLayout.addWidget(folderButton, rowIndex, 2)    

        folderButton.clicked.connect(lambda checked=False, r=rowIndex: openDialogForUSDFileSelection(r))

    #apply button clicked
    @one_undo
    def apply():
        global usd_filepath_dict
        global creatingNewVariant
        variant_set_name = ui.vs_name_input.text()

        vset = createVariantSet(targetPrim, variant_set_name)

        # Iterate through all num_variants
        # num_variants = ui.gridLayout.rowCount() - 1
        for i in range(1, ui.gridLayout.rowCount()):
            v_name_input_widget = ui.findChild(QLineEdit, f"variant_input_{i}")

            # Only make variants for NEW variants (ones that do not have object name pattern of variant_input_x)
            if v_name_input_widget:
                v_name_input = v_name_input_widget.text().strip() # strip white spaces just in case
                file_selected = usd_filepath_dict[i]
                createVariantForSet(targetPrim, vset, v_name_input, file_selected)

            if (creatingNewVariant):
                # set default variant as the first variant
                v_name_input_widget_1 = ui.findChild(QLineEdit, f"variant_input_1")
                v_name_input_1 = v_name_input_widget_1.text().strip() 
                vset.SetVariantSelection(v_name_input_1)

    #connect buttons to functions
    ui.apply_button.clicked.connect(partial(apply))
    ui.addVariantButton.clicked.connect(add_variant_row)
     
    # show the QT ui
    ui.show()
    return ui

if __name__ == "__main__":
    window=showWindow()