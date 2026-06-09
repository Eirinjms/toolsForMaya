from autoRigger import shapes as shapes
import maya.cmds as cmds# pyright: ignore[reportMissingImports] 
import importlib

importlib.reload(shapes)
# ------------------------------
# UIII
# ------------------------------
def run_tool(*args):
    choice = cmds.optionMenu("CtrlChoice", q=True, v=True)
    scale = cmds.floatSliderGrp("CtrlScale", q=True, value=True)
    
    name = "_CTRL"
    size = scale
    
    if choice == "Pyramid CTRL":
        ctrl = shapes.pyramidCtrl(name = name, size = size)

    elif choice == "Cube CTRL":
        ctrl = shapes.cubeCtrl(name = name, X = size, Y = size, Z = size)

    elif choice == "Fourway Arrow CTRL":
        ctrl = shapes.fourWayArrowCtrl(name = name, size = size)

    elif choice == "Twoway Arrow CTRL":
        ctrl = shapes.twoWayArrowCtrl(name = name, size = size)

    elif choice == "Oneway Arrow CTRL":
        ctrl = shapes.oneWayArrowCtrl(name = name, size = size)

    elif choice == "Diamond CTRL":
        ctrl = shapes.pvCtrl(name = name, size = size)

    elif choice == "Gear CTRL":
        ctrl = shapes.gearCtrl(name = name, size = size, side = None, limb = None)
    
    elif choice == "Square CTRL":
        ctrl = shapes.squareCtrl(name = name, size = size)

    # Apply scale to whatever was create

# ------------------------------
# UI
# ------------------------------
def make_ui():

    if cmds.window("fkUI", exists=True):
        cmds.deleteUI("fkUI")

    cmds.window("fkUI", title="FK Tool")

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, mar=10)

    cmds.text("Fancy ol' CTRL tool", bgc=(1, 0.71, 0.80))
    cmds.text("Select CTRL Type")

    cmds.optionMenu("CtrlChoice")
    cmds.menuItem(label="Pyramid CTRL")
    cmds.menuItem(label="Cube CTRL")
    cmds.menuItem(label="Fourway Arrow CTRL")
    cmds.menuItem(label="Twoway Arrow CTRL")
    cmds.menuItem(label="Oneway Arrow CTRL")
    cmds.menuItem(label="Diamond CTRL")
    cmds.menuItem(label="Gear CTRL")
    cmds.menuItem(label="Square CTRL")

    
    cmds.text("CTRL Size")
    cmds.floatSliderGrp(
        "CtrlScale",
        field=True,
        minValue=0.1,
        maxValue=20,
        value=1,
        step=0.1
        )

    cmds.button(label="Build CTRL", command=run_tool)
        
    cmds.showWindow("fkUI")
    


# ------------------------------
# RUN
# ------------------------------
make_ui()