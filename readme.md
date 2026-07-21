--------------------------------------------------------------
#IMPORT GUIDE
--------------------------------------------------------------

MESH CHECKER 
Importing the scripts and making a shelf tool: 
Download toolsForMaya folder (ill upload..soon) 
Put folder into documents -> maya -> scripts
Inside of maya: 
Open script editor
From readme copy run code
Paste into script editor, python folder
Put code on ur shelf and voila, uve stolen my script <3

How to use mesh Checker: 
 - Select a mesh, then press the shelf button, this opens UI (at a later time ill fix so it opens without selecting)
 - From here you can safely analyze new meshes without cluttering the hierarchy as only ONE checkmesh can be active at a time
 - Using the select buttons you can select the offending bad topology on the ORIGINAL mesh, the check mesh is ONLY for templating. Script does allat on its own.
 - IF errors, pls tell me <3

   
--------------------------------------------------------------
#MeshChecker RUN 1.0 script: 
--------------------------------------------------------------

from toolsForMaya import meshCheck
meshCheck.TopologyChecker().runTool()


--------------------------------------------------------------
#save reminder RUN 1.0 script: 
--------------------------------------------------------------

from toolsForMaya import autoSaver #or whatever folder youve put it in

#start timer: 
autosaver = autoSaver.AutoSaver()
autosaver.configWindow()

#stop timer: 
autosaver = autoSaver.AutoSaver()
autosaver.stop()

