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

    global folder_path
    folder_path = ''

    targetPrim = get_selected_usd_xform_prim()
    targetPrimPath = targetPrim.GetPath()
    ui.targetPrim.setText(f"Target Prim: {targetPrimPath}")
    global icon_path
    icon_path = Path(__file__).parent / "icons" / "open-folder.png"
    icon_path2 = Path(__file__).parent / "icons" / "open-folder-confirmed.png"

    file_selected = ""

    # open dialog to allow user to choose texture folder
    def showDialogForUSDFileSelection():
        global file_selected
        initial_directory = "/Users/natashadaas"  # TODO: Replace this with the desired initial directory
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setDirectory(initial_directory)
        dialog.setWindowTitle("Select USD File")

        global folder_path

        # show which filename was selected if a folder was selected
        if dialog.exec_():
            file_selected = dialog.selectedFiles()[0]
            ui.select_button.setIcon(QIcon(str(icon_path2)))
        else:
            ui.select_button.setIcon(QIcon(str(icon_path)))

    def open_folder(row_number):
        print(f"Opening folder for row: {row_number}")
        # Now you can find the specific LineEdit for this row:
        line_edit = ui.findChild(QLineEdit, f"variant_input_{row_number}")
        if line_edit:
            print(f"Current text is: {line_edit.text()}")

    def add_variant_row():
        global icon_path

        # Create widgets
        label = QLabel(f"Variant: ")
        variant_name_line_edit = QLineEdit()
        folderButton = QPushButton()

        # Setting folderButton settings
        folderButton.setIcon(QIcon(str(icon_path)))
        folderButton.setIconSize(QSize(22,22))
        folderButton.setFlat(True)

        # Get new row index
        rowIndex = ui.gridLayout.rowCount()

        # Setting object names
        variant_name_line_edit.setObjectName(f"variant_input_{rowIndex}")
        folderButton.setObjectName(f"select_button_{rowIndex}")

        # Add to the grid layout in new row
        ui.gridLayout.addWidget(label, rowIndex, 0)
        ui.gridLayout.addWidget(variant_name_line_edit, rowIndex, 1)    
        ui.gridLayout.addWidget(folderButton, rowIndex, 2)    

        folderButton.clicked.connect(lambda checked=False, r=rowIndex: open_folder(r))

    #apply button clicked
    @one_undo
    def apply():
        global file_selected
        variant_set_name = ui.vs_name_input.text()
        vset = createVariantSet(targetPrim, variant_set_name)
        v_name_input = ui.vs_name_input.text()
        createVariantForSet(targetPrim, vset, v_name_input, file_selected)

    #connect buttons to functions
    ui.apply_button.clicked.connect(partial(apply))
    ui.addVariantButton.clicked.connect(add_variant_row)
     
    # show the QT ui
    ui.show()
    return ui

if __name__ == "__main__":
    window=showWindow()