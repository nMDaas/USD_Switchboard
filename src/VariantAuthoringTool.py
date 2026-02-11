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
import re

my_script_dir = "/Users/natashadaas/USD_Switchboard/src" 
if my_script_dir not in sys.path:
    sys.path.append(my_script_dir)

from usd_utils import get_selected_usd_xform_prim

# ------------------------------------------------------------------------------------------

class VariantAuthoringTool(ABC):
    @abstractmethod
    def __init__(self, _tool_name):
        self.tool_name = _tool_name
        self.targetPrim = get_selected_usd_xform_prim() # set targetPrim - the XForm that will have the variant
        
        self.creatingNewVariant = True # keeps track of whether we are creating a new variant or not

        # Set 
        self.settings = QSettings("USD_Switchboard", "VariantAuthoringTool")

    # GETTERS ------------------------------------------------------------------------------

    def getToolName(self):
        return self.tool_name
    
    def getTargetPrimPath(self):
        return self.targetPrim.GetPath()
    
    # UI SETUP -----------------------------------------------------------------------------

    @abstractmethod
    def setupUserInterface(self, ui):
        ui.setWindowTitle(self.getToolName())
        ui.setObjectName(self.getToolName())
        ui.targetPrim.setText(f"Target Prim: {self.getTargetPrimPath()}")
        pass
    
    def find_authoring_variant_set(self, targetValue):
        attr = self.targetPrim.GetAttribute("variant_set_pipeline_tag")
        # Get all places where this attribute is authored
        property_stack = attr.GetPropertyStack()

        for p in property_stack:
            path = str(p.path)
            value = p.default
            
            if (value == targetValue):
                match = re.search(r"\{([^=]+)=", path)
                if match:
                    print(match.group(1))
                    vset_name = match.group(1)
                    vsets = self.getVariantSetsOfTargetPrim()
                    variant_set = vsets.GetVariantSet(vset_name)
                    return True, variant_set
                
        return False, None
    
    # UI FUNCTIONS -------------------------------------------------------------------------

    def open_folder(self, ui, row_number):
        print(f"Opening folder for row: {row_number}")
        # Now you can find the specific LineEdit for this row:
        line_edit = ui.findChild(QLineEdit, f"variant_input_{row_number}")
        if line_edit:
            print(f"Current text is: {line_edit.text()}")

    @abstractmethod
    def add_variant_row(self, ui):
        pass

    def add_existing_variant_row(self, ui, v_name):
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

    def populateExistingVariantSetInUI(self, ui, vset):
        ui.vs_name_input.setText(vset.GetName())
        variants = vset.GetVariantNames()
        for v in variants:
            self.add_existing_variant_row(ui, v)

    def resetUI(self, ui):
        ui.vs_name_input.setText("")
        count = 1
        while (ui.gridLayout.rowCount() > 1):
            item = ui.gridLayout.itemAt(count)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # removes from UI
                widget.deleteLater()
    
    # USD VARIANT SPECIFIC FUNCTIONS -------------------------------------------------------

    # Get number variant sets for XForm
    # TODO: Warning if XForm not selected
    def getVariantSetsOfTargetPrim(self):
        vsets = self.targetPrim.GetVariantSets()
        return vsets
    
    # Creates a variant set of a given name for a given XForm
    def createVariantSet(self, in_vset_name):
        vset = self.targetPrim.GetVariantSets().AddVariantSet(in_vset_name)
        return vset
