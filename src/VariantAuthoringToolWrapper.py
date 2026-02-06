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

import sys
my_script_dir = "/Users/natashadaas/USD_Switchboard/src" 
if my_script_dir not in sys.path:
    sys.path.append(my_script_dir)

from VariantAuthoringTool import VariantAuthoringTool

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
        
#show gui window
def showWindow(tool):
    # get this files location so we can find the .ui file in the /ui/ folder alongside it
    UI_FILE = str(Path(__file__).parent.resolve() / "starter_gui.ui")
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
    
    ui.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    global folder_path
    folder_path = ''

    # tool specific set up
    ui.setWindowTitle(tool.getToolName())
    ui.setObjectName(tool.getToolName())
    ui.targetPrim.setText(f"Target Prim: {tool.getTargetPrimPath()}")
    global icon_path
    icon_path = Path(__file__).parent / "icons" / "open-folder.png"
    icon_path2 = Path(__file__).parent / "icons" / "open-folder-confirmed.png"
    ui.select_button.setIcon(QIcon(str(icon_path)))
    ui.select_button.setIconSize(QSize(22,22))
    ui.select_button.setFlat(True)

    # open dialog to allow user to choose texture folder
    def showDialogForUSDFileSelection():
        initial_directory = "/Users/natashadaas"  # TODO: Replace this with the desired initial directory
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setDirectory(initial_directory)
        dialog.setWindowTitle("Select USD File")

        global folder_path

        # show which filename was selected if a folder was selected
        if dialog.exec_():
            tool.setFileSelected(dialog.selectedFiles()[0])
            ui.select_button.setIcon(QIcon(str(icon_path2)))
        else:
            ui.select_button.setIcon(QIcon(str(icon_path)))

    def add_variant_row():
        global icon_path

        label = QLabel(f"Variant: ")
        variant_name_line_edit = QLineEdit()
        folderButton = QPushButton()
        folderButton.setIcon(QIcon(str(icon_path)))
        folderButton.setIconSize(QSize(22,22))
        folderButton.setFlat(True)

        # Add to the grid layout in new row
        rowIndex = ui.gridLayout.rowCount()
        ui.gridLayout.addWidget(label, rowIndex, 0)
        ui.gridLayout.addWidget(variant_name_line_edit, rowIndex, 1)    
        ui.gridLayout.addWidget(folderButton, rowIndex, 2)    

    #apply button clicked
    @one_undo
    def apply():
        variant_set_name = ui.vs_name_input.text()
        vset = tool.createVariantSet(variant_set_name)
        v_name_input = ui.vs_name_input.text()
        tool.createVariantForSet(vset, v_name_input)

    #connect buttons to functions
    ui.apply_button.clicked.connect(partial(apply))
    ui.select_button.clicked.connect(partial(showDialogForUSDFileSelection))
    ui.addVariantButton.clicked.connect(add_variant_row)
     
    # show the QT ui
    ui.show()
    return ui

def executeWrapper():
    tool = VariantAuthoringTool("Create Variants From USD Files")

    window=showWindow(tool)

if __name__ == "__main__":
    executeWrapper()

   