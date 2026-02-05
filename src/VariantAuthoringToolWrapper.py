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
def showWindow():
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
    ui.setWindowTitle('Shader Plugin')
    ui.setObjectName('Shader plugin')
    ui.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    global folder_path
    folder_path = ''

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

    #connect buttons to functions
    ui.apply_button.clicked.connect(partial(apply))
    ui.select_button.clicked.connect(partial(showDialog))
     
    # show the QT ui
    ui.show()
    return ui

def executeWrapper():
    # Create two instances (objects) of the Dog class
    dog1 = VariantAuthoringTool("Buddy", 3)
    dog2 = VariantAuthoringTool("Lucy", 5)

    # Access attributes of the objects
    print(f"{dog1.name} is {dog1.age} years old.")
    print(f"{dog2.name} is {dog2.age} years old.")

    # Call a method on an object
    print(dog1.bark())
    print(dog2.bark())

    #window=showWindow()

if __name__ == "__main__":
    executeWrapper()

   