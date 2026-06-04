import maya.cmds as cmds 

 

#menu stuffs 

def run_tool(*args): 

    radius = cmds.floatSliderGrp("radiusField", 
    q=True, 
    value=True)  
    
    locator_only = cmds.checkBox("LocatorOnly", 
    q = True, 
    value = True)
    
    Constraint = cmds.radioButtonGrp("ConstraintChoice", 
    q = True, 
    sl = True)  

 
# selects joints (lists joints) -> select in the order of the hierarchy

    joints = cmds.ls(sl=True, long=True) 

    if not joints: 

        cmds.error("Select at least one joint")
        
        
    if locator_only: 

        for joint in joints: 

            joint_name = joint.split('|')[-1] 



            loc = cmds.spaceLocator(name=joint_name.replace("_JNT", "FK_LOC"))[0] 
            

            cmds.delete(cmds.parentConstraint(joint, loc))  
            cmds.select(loc) 

 
    if not locator_only:
        
# defines the grpthingy 

        previousCtrl = None 
    
     
    # for every joint it creates locator 
    
        for joint in joints: 
    
            joint_name = joint.split('|')[-1] 
    
     
    
            loc = cmds.spaceLocator(name=joint_name.replace("_JNT", "_FK_LOC"), )[0]
            
            shape = cmds.listRelatives(loc, shapes=True)[0]
            cmds.setAttr(shape + ".visibility", 0) 
              
    
            cmds.delete(cmds.parentConstraint(joint, loc)) 
    
             
    
    # for every locator it creates a circle
    
            if "_leg_JC_" in joint_name: 
    
                normal=(0, 1, 0 )
                
            else: 
                normal=(1, 0, 0 )
                    
            
            ctrl = cmds.circle( 
                name=joint_name.replace("_JNT", "_FK_CTRL"),
                r=radius, normal = normal)[0]
                
            cmds.nodeType(ctrl) == "transform"
               
    
            cmds.delete(cmds.parentConstraint(joint, ctrl)) 
    
     
    
    # Parent CTRL under LOC 
    
            cmds.parent(ctrl, loc) 
    
            cmds.makeIdentity(ctrl, t=True, r=True, s=True) 
    
             
    
    # colour SHAPE of ctrl 
    
            shapes = cmds.listRelatives(ctrl, s=True) 
    
            for shape in shapes:
                
                cmds.setAttr(shape + ".overrideEnabled", 1) 
                  
                
                if shape.startswith("C_"):
                    cmds.setAttr(shape + ".overrideColor", 17)
                
                elif shape.startswith("R_"):
                    cmds.setAttr(shape + ".overrideColor", 13)
                                
    
                elif shape.startswith("L_"):
                    cmds.setAttr(shape + ".overrideColor", 6)
                             
     
    
    # makes the parent chain 
    
            if previousCtrl is not None: 
    
                cmds.parent(loc, previousCtrl) 
    
     
    
            previousCtrl = ctrl 
            

#constraint radio options  

            #Constraint = 1: None 

            if Constraint == 2: 
                cmds.parentConstraint(ctrl,joint,
                name = joint_name.replace("_JNT", "_paCON"), 
                mo = False)
                
            elif Constraint == 3: 
                cmds.orientConstraint(ctrl, joint,
                name = joint_name.replace("_JNT", "_oCON"), 
                mo = False)
                
            elif Constraint == 4: 
                cmds.pointConstraint(ctrl, joint,
                name = joint_name.replace("_JNT", "_poCON"), 
                mo = False) 
                            


#the ui window setup 

def make_ui(): 

    if cmds.window("fkUI", exists=True): 

        cmds.deleteUI("fkUI") 

 

    cmds.window("fkUI", title="FK Tool") 

    cmds.columnLayout(adjustableColumn=True, 
    rowSpacing=10, 
    mar = 10)
    
    cmds.text("Fancy ol' FK tool", 
    bgc = (1,0.71,0.80))
    
    cmds.checkBox("LocatorOnly", 
    label = "Only Locator", )

    cmds.floatSliderGrp("radiusField", 
    label="Control Shape Radius   ", 
    field=True, 
    minValue=1, 
    maxValue=15.0, 
    value=7.0) 
    
    cmds.radioButtonGrp("ConstraintChoice", l = "Select Constraint Type : ", la4 = (
    "No Constraint", 
    "Parent Constraint", 
    "Orient Constraint",
    "Point Constraint"),
    nrb = 4, sl = 1) 


    cmds.button( 

        label="Build FK Controls", 

        command=run_tool) 

     

    cmds.showWindow("fkUI") 

 

#Run 

make_ui() 
