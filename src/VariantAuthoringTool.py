import sys
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
from PySide6.QtCore import QSettings

my_script_dir = "/Users/natashadaas/USD_Switchboard/src" 
if my_script_dir not in sys.path:
    sys.path.append(my_script_dir)

from usd_utils import get_selected_usd_xform_prim

# ------------------------------------------------------------------------------------------

class VariantAuthoringTool:
    def __init__(self, _tool_name):
        self.tool_name = _tool_name
        self.targetPrim = get_selected_usd_xform_prim() # set targetPrim - the XForm that will have the variant
        self.fileSelected = "" # only considering one
        self.usd_filepath_dict = {} # stores [row, filepath]

        # icon paths
        self.open_folder_icon = Path(__file__).parent / "icons" / "open-folder.png"
        self.folder_chosen_icon  = Path(__file__).parent / "icons" / "open-folder-confirmed.png"

        # Set 
        self.settings = QSettings("USD_Switchboard", "VariantAuthoringTool")

    # SETTERS ------------------------------------------------------------------------------

    def setFileSelected(self, _fileSelected):
        self.fileSelected = _fileSelected

    # GETTERS ------------------------------------------------------------------------------

    def getToolName(self):
        return self.tool_name
    
    def getTargetPrimPath(self):
        return self.targetPrim.GetPath()
    
    # UI SETUP -----------------------------------------------------------------------------

    def setupUserInterface(self, ui):
        ui.setWindowTitle(self.getToolName())
        ui.setObjectName(self.getToolName())
        ui.targetPrim.setText(f"Target Prim: {self.getTargetPrimPath()}")
    
    # UI FUNCTIONS -------------------------------------------------------------------------

    def open_folder(self, ui, row_number):
        print(f"Opening folder for row: {row_number}")
        # Now you can find the specific LineEdit for this row:
        line_edit = ui.findChild(QLineEdit, f"variant_input_{row_number}")
        if line_edit:
            print(f"Current text is: {line_edit.text()}")

    def add_variant_row(self, ui):
        # Create widgets
        label = QLabel(f"Variant: ")
        variant_name_line_edit = QLineEdit()
        folderButton = QPushButton()

        # Setting folderButton settings
        folderButton.setIcon(QIcon(str(self.open_folder_icon)))
        folderButton.setIconSize(QSize(22,22))
        folderButton.setFlat(True)

        # Get new row index
        rowIndex = ui.gridLayout.rowCount()

        if (rowIndex == 1):
            variant_name_line_edit.setText("Default")

        # Setting object names
        variant_name_line_edit.setObjectName(f"variant_input_{rowIndex}")
        folderButton.setObjectName(f"select_button_{rowIndex}")

        # Add to the grid layout in new row
        ui.gridLayout.addWidget(label, rowIndex, 0)
        ui.gridLayout.addWidget(variant_name_line_edit, rowIndex, 1)    
        ui.gridLayout.addWidget(folderButton, rowIndex, 2)   

        folderButton.clicked.connect(lambda checked=False, r=rowIndex: self.showDialogForUSDFileSelection(ui, r))

     # open dialog for user to select USD file - linked to row number
    def showDialogForUSDFileSelection(self, ui, row_number):
        if self.settings.value("defaultDirectory") is None:
            self.settings.setValue("defaultDirectory",  cmds.workspace(query=True, rootDirectory=True))

        initial_directory =  self.settings.value("defaultDirectory")
        select_button = ui.findChild(QPushButton, f"select_button_{row_number}")

        dialog = QFileDialog()
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setDirectory(initial_directory)
        dialog.setWindowTitle("Select USD File")

        # show which filename was selected if a folder was selected
        if dialog.exec_():
            file_selected = dialog.selectedFiles()[0]
            self.settings.setValue("defaultDirectory",  str(Path(file_selected).parent))
            self.usd_filepath_dict[row_number] = file_selected
            select_button.setIcon(QIcon(str(self.folder_chosen_icon)))
        else:
            select_button.setIcon(QIcon(str(self.open_folder_icon))) 
    
    # USD VARIANT SPECIFIC FUNCTIONS -------------------------------------------------------
    
    # Creates a variant set of a given name for a given XForm
    def createVariantSet(self, in_vset_name):
        vset = self.targetPrim.GetVariantSets().AddVariantSet(in_vset_name)
        return vset
    
    #TODO: There should be error checking for if the variant_name already exists for the vset
    #TODO: warning if file has not been selected
    def createVariant(self, vset, variant_name, file_selected):
        vset.AddVariant(variant_name)

        vset.SetVariantSelection(variant_name)

        # Go inside the variant and add the file reference
        with vset.GetVariantEditContext():
            self.targetPrim.GetReferences().AddReference(file_selected)
        
        print(f"Variant '{variant_name}' authored with reference to: {file_selected}")

    def createVariantsForSet(self, ui, vset):
        # Iterate through all num_variants
        # num_variants = ui.gridLayout.rowCount() - 1
        for i in range(1, ui.gridLayout.rowCount()):
            v_name_input_widget = ui.findChild(QLineEdit, f"variant_input_{i}")
            v_name_input = v_name_input_widget.text().strip() # strip white spaces just in case
            file_selected = self.usd_filepath_dict[i]
            self.createVariant(vset, v_name_input, file_selected)

        # set default variant as the first variant
        v_name_input_widget_1 = ui.findChild(QLineEdit, f"variant_input_1")
        v_name_input_1 = v_name_input_widget_1.text().strip() 
        vset.SetVariantSelection(v_name_input_1)
