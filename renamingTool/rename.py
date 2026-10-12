import maya.cmds as cmds
import string
import QWidget


class renamingTool(QWidget):
    def __init__(self):
        self.selection = None
        ui_load = something. 

    def connections(self):
        self.nameTxt = findChild.smtsmth(QTextBox, "textBox")
        self.prefixTxt = findChild.smtsmth(QTextBox, "prefixBox")
        self.suffixTxt = findChild.smtsmth(QTextBox, "suffixBox")

        self.selectedRadio = findChild.smtsmth(QRadioButton, "selectedRadio")
        self.hierarchyRadio = findChild.smtsmth(QRadioButton, "hierarchyRadio")

        self.JendRadio = findChild.smtsmth(QRadioButton, "JendRadio")
        self.numberEndRadio = findChild.smtsmth(QRadioButton, "numberEndRadio")

    def renaming(self):
        name = self.nameTxt.value() 
        prefix = self.prefixTxt.value() 
        suffix = self.suffixTxt.value() 

        for obj in self.selection:
            cmds.rename(obj, prefix + name + suffix)
            
    def selectionRefresh(self):
        self.selection = cmds.ls(sl=True, long=True)

        return self.selection


joints = cmds.ls(sl=True, long=True)

name = "claw"
prefix = "L"

letters = string.ascii_uppercase
new_names = []
last_index = len(joints) - 1

for i, joint in enumerate(joints):
    if i == last_index:
        new_names.append(f"{prefix}_{name}_JEnd_GEO")
    else:
        letter = letters[i]
        new_names.append(f"{prefix}_{name}_J{letter}_GEO")

# rename child → parent
for joint, new_name in zip(reversed(joints), reversed(new_names)):
    cmds.rename(joint, new_name)