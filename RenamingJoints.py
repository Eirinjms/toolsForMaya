import maya.cmds as cmds
import string

# get selected joints as full paths (safe for renaming)
joints = cmds.ls(sl=True, long=True)

letters = string.ascii_uppercase
name = "hairSideBang01"
prefix = "L"
suffix = "_JNT"

new_names = []
last_index = len(joints) - 1

# build new names first
for i, joint in enumerate(joints):
    if i == last_index:
        new_names.append(f"{prefix}_{name}JEnd_{suffix}")
    else:
        new_names.append(f"{prefix}_{name}J{letters[i]}_{suffix}")

# rename from child to parent
for joint, new_name in zip(reversed(joints), reversed(new_names)):
    cmds.rename(joint, new_name)
