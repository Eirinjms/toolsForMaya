def createTwist(*args):
    import maya.cmds as cmds

    # get number from UI
    twistJntsAmnt = cmds.intSliderGrp(twistInput, q=True, value=True)

    # get joint radius from UI
    jointRadius = cmds.floatSliderGrp(jointRadiusInput, q=True, value=True)

    axis = cmds.radioButtonGrp(axisInput, q=True, select=True)
    axis = ["X", "Y", "Z"][axis-1]

    #select joints in order, 1 jnt is start, 2nd is end
    Joints = cmds.ls(sl = True)

    if len(Joints) != 2:
        cmds.error('Please select exactly 2 joints, in order from start to end')
        return
    
    jointName = f"{Joints[0].replace('_JNT', '')}"
        
    jointsLoc = []
    for jnt in Joints:
        jntloc = cmds.xform(jnt, 
                            q = True, 
                            t = True, 
                            ws = True)
        jointsLoc.append(jntloc)

    curve = cmds.curve(d=1, 
                       ep = jointsLoc, 
                       n = "twistCrv")
    cmds.rebuildCurve(curve, d = 1, 
                      rpo = True , 
                      kep = True, 
                      s = twistJntsAmnt+1, 
                      n = "twistCrvRebuild", 
                      rt = 0)

    cvLocations = []
    cvs = cmds.ls(f"{curve}.cv[*]", fl=True)

    for cv in cvs:
        pos = cmds.xform(cv, q=True, ws=True, t=True)
        cvLocations.append(pos)

    twistJnts = []
    cmds.select(clear=True)

    for i in range(twistJntsAmnt):  
        jnt = cmds.joint(n = f"{jointName}_{i:02d}_TWIST_JNT", 
                         p = cvLocations[i+1], 
                         rad = jointRadius)
        twistJnts.append(jnt)

        if 'leg' in jointName: 
            cmds.matchTransform(jnt, Joints[1], 
                                rot = True, 
                                pos = False, 
                                scl = False)
        
        if 'arm' in jointName: 
            cmds.matchTransform(jnt, Joints[0], 
                                rot = True, 
                                pos = False, 
                                scl = False)
    

    cmds.parent(twistJnts[0], Joints[0])
    cmds.delete(curve)
    cmds.makeIdentity(twistJnts[0], 
                      apply = True, 
                      t = False, 
                      r = True, 
                      s = False)


    #mathematically apply percentages
    percentList = []
    percentStart = 1/(len(twistJnts)+1)

    count = 0

    for i in twistJnts: 
        count += 1
        
        percentList.append(percentStart*count)

    percent = percentList

    for twst, p in zip(twistJnts, percent): 
        md = cmds.createNode('multiplyDivide', n = f"{twst}_MD")
        cmds.setAttr(f"{md}.input2{axis}", p)
        cmds.connectAttr(f"{Joints[1]}.rotate{axis}", f"{md}.input1{axis}")
        cmds.connectAttr(f"{md}.output{axis}", f"{twst}.rotate{axis}")

    
def createUI(*args):
    import maya.cmds as cmds

    global twistInput, jointRadiusInput, axisInput
    if cmds.window("twistUI", exists=True):
        cmds.deleteUI("twistUI")

    window = cmds.window(
        "twistUI",
        title="Twist Joint Creator",
        widthHeight=(260, 150),
        resizeToFitChildren=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=15)

    cmds.text(label="Select 2 joints in order from start to end")
    cmds.separator(height=10)

    cmds.text(label="Number of Twist Joints")
    twistInput = cmds.intSliderGrp(field=True, 
                                        minValue=1, 
                                        maxValue=10, 
                                        value=3, 
                                        step=1)
   

    cmds.separator(height=10)

    cmds.text(label="Joint Radius")
    jointRadiusInput = cmds.floatSliderGrp(field=True, 
                                        minValue=0.1, 
                                        maxValue=20, 
                                        value=1, 
                                        step=0.1)
    
    cmds.separator(height=15)

    axisInput = cmds.radioButtonGrp(
    label="Twist Axis",
    labelArray3=["X", "Y", "Z"],
    numberOfRadioButtons=3,
    columnWidth4=(70, 30, 30, 30),
    columnAlign=(1, "left"),
    select=1)

    cmds.separator(height=15)

    cmds.button(
        label="Create Twist Joints",
        height=30,
        command=createTwist
    )

    cmds.showWindow(window)


# -----------------------------
# Run UI
# -----------------------------
createUI()
