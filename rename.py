import maya.cmds as cmds
import string

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