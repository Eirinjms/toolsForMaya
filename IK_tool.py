def ikTool():
    import maya.cmds as cmds
    from autoRigTool import shapes as shapes

    # --- GET SELECTION ---
    ikJoints = cmds.ls(sl=True)

    if not ikJoints or len(ikJoints) < 2:
        cmds.warning("Select joint chain from top to bottom")
        return

    # --- CLEAN PREVIOUS RIG ---
    for grp in ["IKGRP", "JNTGRP"]:
        if cmds.objExists(grp):
            cmds.delete(grp)

    # --- BASE NAME ---
    baseName = ikJoints[0].replace('_JNT', '').replace('JA', '')

    # --- BUILD CURVE FROM JOINTS ---
    curvePoints = [cmds.xform(j, q=True, ws=True, t=True) for j in ikJoints]

    curve = cmds.curve(
        d=3,
        ep=curvePoints,
        n=f"{baseName}_IKH_Curve"
    )

    cmds.setAttr(f"{curve}.inheritsTransform", 0)

    # --- IK SPLINE ---
    ikh, eff = cmds.ikHandle(
        sol="ikSplineSolver",
        sj=ikJoints[0],
        ee=ikJoints[-1],
        c=curve,
        ccv=False,
        rtm=False,
        n=f"{baseName}_IKH"
    )

    # --- CREATE CONTROL JOINTS ---
    curveJoints = ikJoints[0::1]
    names = ['top', 'midA', 'midB', 'midC', 'midD', 'midE', 'end']

    ctrlJoints = []

    for i, jnt in enumerate(curveJoints):
        if i >= len(names):
            break

        name = names[i]

        ctrlJnt = cmds.joint(n=f"{baseName}_{name}_CTRL_JNT#")
        cmds.delete(cmds.parentConstraint(jnt, ctrlJnt))
        cmds.parent(ctrlJnt, w=True)

        ctrlJoints.append(ctrlJnt)

    # --- LOCATORS + CONTROLS ---
    ikCtrls = []
    grp = cmds.group(em=True, n="IKGRP")

    for i, jnt in enumerate(ctrlJoints):
        name = names[i]

        loc = cmds.spaceLocator(n=f"{baseName}_{name}_LOC")[0]

        ctrl = shapes.cubeCtrl(
            name=f"{baseName}_{name}_CTRL",
            X=0, Y=30, Z=30
        )

        ikCtrls.append(ctrl)

        cmds.parent(ctrl, loc)
        cmds.delete(cmds.parentConstraint(jnt, loc))

        cmds.parent(loc, grp)

        cmds.parentConstraint(ctrl, jnt, mo=False)

    # --- SKIN CURVE ---
    cmds.skinCluster(ctrlJoints, curve, tsb=True, n=f"{baseName}_curveSKN")

    # --- TWIST SETUP ---
    md = cmds.shadingNode('multiplyDivide', au=True)
    cmds.setAttr(f"{md}.input2X", -1)

    pma = cmds.shadingNode('plusMinusAverage', au=True)
    cmds.setAttr(f"{pma}.operation", 1)

    cmds.connectAttr(f"{ikCtrls[0]}.rotateX", f"{ikh}.roll")
    cmds.connectAttr(f"{ikCtrls[0]}.rotateX", f"{md}.input1X")
    cmds.connectAttr(f"{md}.outputX", f"{pma}.input1D[0]")
    cmds.connectAttr(f"{ikCtrls[-1]}.rotateX", f"{pma}.input1D[1]")
    cmds.connectAttr(f"{pma}.output1D", f"{ikh}.twist")

    # --- COLOR CONTROLS ---
    for ctrl in ikCtrls:
        shapesList = cmds.listRelatives(ctrl, s=True, f=True)

        if not shapesList:
            continue

        for shape in shapesList:
            cmds.setAttr(shape + ".overrideEnabled", 1)

            if ctrl.startswith("C_"):
                cmds.setAttr(shape + ".overrideColor", 17)
            elif ctrl.startswith("L_"):
                cmds.setAttr(shape + ".overrideColor", 6)
            elif ctrl.startswith("R_"):
                cmds.setAttr(shape + ".overrideColor", 13)

    # --- FINAL GROUP ---
    jntGrp = cmds.group(ctrlJoints, n="JNTGRP")

    cmds.group(ikh, grp, jntGrp, n=f"{baseName}_GRP")