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
from abc import ABC, abstractmethod

my_script_dir = "/Users/natashadaas/USD_Switchboard/src" 
if my_script_dir not in sys.path:
    sys.path.append(my_script_dir)

from VariantAuthoringTool import VariantAuthoringTool

# ------------------------------------------------------------------------------------------

class TransformVariantAuthor(VariantAuthoringTool):

    def __init__(self, _tool_name):
        super().__init__(_tool_name)

        # icon paths
        self.pin_icon = Path(__file__).parent / "icons" / "pin.png"
        self.pinned_icon  = Path(__file__).parent / "icons" / "pin-confirmed.png"

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
        setButton = QPushButton()

        # Setting folderButton settings
        setButton.setIcon(QIcon(str(self.pin_icon)))
        setButton.setIconSize(QSize(22,22))
        setButton.setFlat(True)

        # Get new row index
        rowIndex = ui.gridLayout.rowCount()

        if (rowIndex == 1):
            variant_name_line_edit.setText("Default")

        # Setting object names
        variant_name_line_edit.setObjectName(f"variant_input_{rowIndex}")
        setButton.setObjectName(f"set_button_{rowIndex}")

        # Add to the grid layout in new row
        ui.gridLayout.addWidget(label, rowIndex, 0)
        ui.gridLayout.addWidget(variant_name_line_edit, rowIndex, 1)    
        ui.gridLayout.addWidget(setButton, rowIndex, 2)   

        setButton.clicked.connect(lambda checked=False, r=rowIndex: self.showDialogForUSDFileSelection(ui, r))

    # open dialog for user to select USD file - linked to row number
    def showDialogForUSDFileSelection(self, ui, row_number):
        # doing something...

        # if successful: 
            #change pin icon
        # otherwise
            # keep pin icon as before
        pass

    def createVariantsForSet(self, ui, vset):
        # Iterate through all num_variants
        # num_variants = ui.gridLayout.rowCount() - 1
        for i in range(1, ui.gridLayout.rowCount()):
            v_name_input_widget = ui.findChild(QLineEdit, f"variant_input_{i}")

            # Only make variants for NEW variants (ones that do not have object name pattern of variant_input_x)
            # This works because when populating existing variants, I didn't give it object names
            if v_name_input_widget:
                v_name_input = v_name_input_widget.text().strip() # strip white spaces just in case
                file_selected = self.usd_filepath_dict[i]
                self.createVariant(vset, v_name_input, file_selected)

        # set default variant as the first variant, only if the variant set is new
        if self.creatingNewVariant:
            v_name_input_widget_1 = ui.findChild(QLineEdit, f"variant_input_1")
            v_name_input_1 = v_name_input_widget_1.text().strip() 
            vset.SetVariantSelection(v_name_input_1)

    #TODO: warning if file has not been selected
    def createVariant(self, vset, variant_name, file_selected):
        vset.AddVariant(variant_name)

        vset.SetVariantSelection(variant_name)

        # Go inside the variant and add the file reference
        with vset.GetVariantEditContext():
            self.targetPrim.GetReferences().AddReference(file_selected)
        
        print(f"Variant '{variant_name}' authored with reference to: {file_selected}")

