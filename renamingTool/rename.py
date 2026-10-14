import maya.cmds as cmds
import string
from PySide6 import QtWidgets, QtGui, QtCore # pyright: ignore[reportMissingImports]
from PySide6.QtCore import QFile # pyright: ignore[reportMissingImports]
from PySide6.QtUiTools import QUiLoader # pyright: ignore[reportMissingImports]
from PySide6.QtWidgets import QFileDialog # pyright: ignore[reportMissingImports]
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance
import os

def getMayaWindow():
    mayaWindow = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    return mayaWindow

class renamingTool(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(getMayaWindow() or parent)

        self.selection = None

        self.folder = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.folder,
                            "renaming_UI.ui")

        self.setWindowTitle("Renaming Tool")

        self.newNames = []

        self._load_UI(self.file_path)
        self._addConnections()
        self._connectButtons()
        self.updatePreview()

        self.letters = string.ascii_uppercase
        self.name = self.nameTxt.text()
        self.prefix = self.prefixTxt.text() 
        self.suffix = self.suffixTxt.text()


    def _load_UI(self, path):
        if not os.path.exists(path):
            print("File not found")
            return

        file = QFile(path)
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(file, parentWidget = self)
        file.close()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.ui)

    def _addConnections(self):
        self.nameTxt = self.findChild(QtWidgets.QLineEdit, "textBox")
        self.prefixTxt = self.findChild(QtWidgets.QLineEdit, "prefixBox")
        self.suffixTxt = self.findChild(QtWidgets.QLineEdit, "suffixBox")

        self.selectedRadio = self.findChild(QtWidgets.QRadioButton, "selectedRadio")
        self.hierarchyRadio = self.findChild(QtWidgets.QRadioButton, "hierarchyRadio")

        self.JendRadio = self.findChild(QtWidgets.QRadioButton, "JendRadio")
        self.numberEndRadio = self.findChild(QtWidgets.QRadioButton, "numberEndRadio")

        self.comboBox = self.findChild(QtWidgets.QComboBox, "Count")

        #Suffixes
        self.leftPrefix = self.findChild(QtWidgets.QPushButton, "prefix_L")
        self.rightPrefix = self.findChild(QtWidgets.QPushButton, "prefix_R")
        self.centerPrefix = self.findChild(QtWidgets.QPushButton, "prefix_C")

        self.jointSuffix = self.findChild(QtWidgets.QPushButton, "suffix_jnt")
        self.geoSuffix = self.findChild(QtWidgets.QPushButton, "suffix_geo")
        self.controlSuffix = self.findChild(QtWidgets.QPushButton, "suffix_ctrl")

        self.renamingBtn = self.findChild(QtWidgets.QPushButton, "renaming_btn")

        self.preview = self.findChild(QtWidgets.QLineEdit, "preview")


    def _connectButtons(self):
        if self.renamingBtn:
            self.renamingBtn.clicked.connect(self.renaming)

        if self.rightPrefix:
            self.rightPrefix.clicked.connect(lambda: self.buttonText("R", self.prefixTxt))

        if self.leftPrefix:
            self.leftPrefix.clicked.connect(lambda: self.buttonText("L", self.prefixTxt))

        if self.centerPrefix:
            self.centerPrefix.clicked.connect(lambda: self.buttonText("C", self.prefixTxt))

        if self.jointSuffix:
            self.jointSuffix.clicked.connect(lambda: self.buttonText("JNT", self.suffixTxt))

        if self.geoSuffix:
            self.geoSuffix.clicked.connect(lambda: self.buttonText("GEO", self.suffixTxt))

        if self.controlSuffix:
            self.controlSuffix.clicked.connect(lambda: self.buttonText("CTRL", self.suffixTxt))

        if self.nameTxt:
            self.nameTxt.textChanged.connect(self.updatePreview)

        if self.prefixTxt:
            self.prefixTxt.textChanged.connect(self.updatePreview)

        if self.suffixTxt:
            self.suffixTxt.textChanged.connect(self.updatePreview)

        if self.comboBox:
            self.comboBox.activated.connect(self.updatePreview)

    def buttonText(self, text, button):
        button.setText(text)

    def updatePreview(self):
        self.updateText()
        
        letter = "A"

        if self.comboBox.currentIndex() == 1:
            self.preview.setText(f"{self.prefix}_{self.name}J{letter}_{self.suffix}")
        else: 
            self.preview.setText(f"{self.prefix}_{self.name}01_{self.suffix}")

    def selectionRefresh(self):
        self.selection = cmds.ls(sl=True)

        return self.selection

    def findHierarchy(self, root):
        hierarchy = []
        children = cmds.listRelatives(root, ad = True)
        hierarchy.extend(children)

        print(hierarchy)
        hierarchy.append(root)
        hierarchy.reverse()
        print(hierarchy)

        return hierarchy

    def renaming(self):
        self.selectionRefresh()
        self.updateText()
        self.newNames.clear()

        if not self.selection:
            return cmds.warning("No objects selected for renaming")

        if self.hierarchyRadio.isChecked():
            hierarchy = self.findHierarchy(self.selection[0])
            self.renameLoop(hierarchy)

        elif self.selectedRadio.isChecked(): 
            if len(self.selection) > 1:
                self.renameLoop(self.selection)

            else: 
                for obj in self.selection:
                    cmds.rename(obj, f"{self.prefix}_{self.name}_{self.suffix}")

    def updateText(self):
        self.name = self.nameTxt.text()
        self.prefix = self.prefixTxt.text() 
        self.suffix = self.suffixTxt.text()

    def renameLoop(self, sel):
        for i, obj in enumerate(sel):
            if self.comboBox.currentIndex() == 1:
                if obj == sel[-1]:
                    lastname = cmds.rename(obj, f"{self.prefix}_{self.name}JEnd_{self.suffix}")
                    self.newNames.append(lastname)
                else: 
                    letter = self.letters[i]
                    newName = cmds.rename(obj, f"{self.prefix}_{self.name}J{letter}_{self.suffix}")
                    self.newNames.append(newName)
            else: 
                newName = cmds.rename(obj, f"{self.prefix}_{self.name}{i+1:02d}_{self.suffix}")
                self.newNames.append(newName)


def runTool():
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if type(widget).__name__ == "renamingTool":
            widget.close()
            widget.deleteLater()

    window = renamingTool()
    window.show()