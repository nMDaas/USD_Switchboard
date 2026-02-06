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

    # open dialog to allow user to choose texture folder
    def showDialog():
        initial_directory = "/Users/natashadaas"  # Replace this with the desired initial directory
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setDirectory(initial_directory)
        dialog.setWindowTitle("Select Folder")

        global folder_path

        # show which filename was selected if a folder was selected
        if dialog.exec_():
            folder_path = dialog.selectedFiles()[0]
            ui.filename_label.setText(folder_path)
        else:
            ui.filename_label.setText('')

    #apply button clicked
    @one_undo
    def apply():
        print("Apply clicked")
        variant_set_name = ui.vs_name_input.text()
        tool.createVariantSet(variant_set_name)

    #connect buttons to functions
    ui.apply_button.clicked.connect(partial(apply))
    ui.select_button.clicked.connect(partial(showDialog))
     
    # show the QT ui
    ui.show()
    return ui

def executeWrapper():
    tool = VariantAuthoringTool("Create Variants From USD Files")

    window=showWindow(tool)

if __name__ == "__main__":
    executeWrapper()

   