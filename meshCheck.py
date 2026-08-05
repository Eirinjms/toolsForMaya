import maya.cmds as cmds 

class TopologyChecker:
    def __init__(self):
        self.new_run = False
        self.mesh = cmds.ls(sl=True)

        self.tris = []
        self.ngonsList = []
        self.poles = []
        self.nonManFaces = []
        self.sixStars = []

    def meshSetup(self):
        if len(self.mesh) == 0:
            cmds.warning('No meshes selected. Please select one mesh and try again')
            return

        if len(self.mesh) > 1:
            cmds.warning('Multiple meshes selected. Please select one mesh and try again')
            return

        if self.new_run:
            if self.mesh == []:
                cmds.warning('Template mesh selected, please choose a new mesh and try again')
                return
            if self.mesh and self.mesh[0].endswith("_topoCheckMesh"):
                cmds.warning('Template mesh selected, please select a new mesh and try again')
                cmds.select(cl=True)
                return

        self.verts = cmds.ls(self.mesh[0] + '.vtx[*]', fl=True)
        self.faces = cmds.ls(self.mesh[0] + '.f[*]', fl=True)
        self.max = len(self.verts)
        self.counter = 0

    def duplicateMesh(self):
        if cmds.objExists("*_topoCheckMesh"):
            cmds.delete("*_topoCheckMesh")

        self.checkMesh = cmds.duplicate(self.mesh[0], n=f"{self.mesh[0]}_topoCheckMesh")[0]
        self.checkMeshShape = cmds.listRelatives(self.checkMesh, s=True)[0]

        self.template = True
        cmds.setAttr(self.checkMesh + ".template", self.template)

        cmds.polySoftEdge(self.checkMesh, a=180, ch=True)
        cmds.setAttr(f"{self.checkMeshShape}.displayEdges", 2)
        cmds.setAttr(f"{self.checkMeshShape}.displayColors", 1)
        cmds.displayRGBColor('hardedgeHilite', 0, 1, 0)

    def vertConfirm(self):
        result = "Analyse it"
        if self.max > 100_000:
            result = cmds.confirmDialog(
                message= f"Are you really sure you wanna do this buddy? selected mesh has {len(self.verts):,} vertices and could take a while or crash maya :(",
                button = ["Analyse it", "Cancel"],
                defaultButton = "Analyse it",
                cancelButton = "Cancel")
        
        return result

    def progressBar(self):
        cmds.progressWindow(
            title='Topology Checker',
            progress=0,
            maxValue=self.max,
            status='Checking topology...',
            isInterruptable=True)

    def locateTriangles(self):
        cmds.select(self.checkMesh)
        cmds.polySelectConstraint(mode=3, type=0x0008, size=1)
        self.tris = cmds.ls(sl=True, fl=True)
        cmds.polySelectConstraint(disable=True)

        if self.tris:
            cmds.polySoftEdge(self.tris, a=0, ch=True)
            
        cmds.select(clear=True)

    def locateNGons(self):

        for face in self.faces:

            info = cmds.polyInfo(face, faceToEdge=True)

            if info:
                edges = info[0].split()[2:]

                if len(edges) > 4:
                    self.ngonsList.append(face)

        if self.ngonsList:
            cmds.select(self.ngonsList)
            cmds.polySoftEdge(self.ngonsList, a=0, ch=True)

        cmds.select(clear=True)

    def locateNonManifold(self):

        results = cmds.polyInfo(self.checkMesh, nme=True) or []

        for line in results:
            face = line.split()[-1]
            self.nonManFaces.append(face)
        
        cmds.select(clear=True)


    def locatePoles(self):
        for vtx in self.verts:

            info = cmds.polyInfo(vtx, vertexToEdge=True)

            if info:
                edges = info[0].split()[2:]

                if len(edges) == 5:
                    self.poles.append(vtx)

                elif len(edges) >= 6:
                    self.sixStars.append(vtx)
        

            self.counter += 1
            cmds.progressWindow(
                edit=True,
                progress=self.counter,
                status='Analyzing Topology..')

        if len(self.poles) >= 1:      
            cmds.select(self.poles)
            edges = cmds.polyListComponentConversion(self.poles, toEdge=True)
            edges = cmds.ls(edges, fl=True)
            cmds.polySoftEdge(edges, a=0, ch=True)
        
        if len(self.sixStars) >= 1:
            cmds.select(self.sixStars)
            edges = cmds.polyListComponentConversion(self.sixStars, toEdge=True)
            edges = cmds.ls(edges, fl=True)
            cmds.polySoftEdge(edges, a=0, ch=True)

        cmds.progressWindow(endProgress=True)
        cmds.select(clear=True)


    def deleteCheckMesh(self, *args):
        if not self.new_run:
            if cmds.objExists(f"{self.checkMesh}"):
                cmds.delete(f"{self.checkMesh}")
                cmds.select(cl = True)
            else:
                cmds.warning("No check mesh found.")


#UI
    def analysisWindow(self):
        if cmds.window('topoResults', exists=True):
            cmds.deleteUI('topoResults')
        
        cmds.window('topoResults', 
                    title='Topology Analysis Results', 
                    widthHeight=(300, 200), 
                    resizeToFitChildren=True,
                    cc = self.deleteCheckMesh)

        cmds.columnLayout(adj = True, mar = 5)

        check = "Topology check complete!"
        if len(self.ngonsList) == 0: 
            cmds.text(label= f"{check} You're awesome! :D ", align='center', height=30, font='boldLabelFont')
        else: 
            cmds.text(label= f"{check} You suck! D: ", align='center', height=30, font='boldLabelFont')
        cmds.separator(height=15, st = "shelf")

        cmds.rowColumnLayout(adj = 1, nc = 2)

        #Poles!
        cmds.text(label=f"Poles found: {len(self.poles)}", align='left', height=30)

        btnColour = (1, 0.6, 0.8)

        cmds.button(label="Select Poles",
            command=lambda x: cmds.select([f.replace(self.checkMesh, self.mesh[0]) for f in self.poles]),
            align = "center",
            bgc = btnColour)
        
        cmds.separator(height=15, st = "in")
        cmds.separator(height=15, st = "in")

        #SixSidedStars
        cmds.text(label=f"6+ Star Poles: {len(self.sixStars)}", align='left', height=30)

        btnColour = (1, 0.6, 0.8)

        cmds.button(label="6+ Star Poles",
            command=lambda x: cmds.select([f.replace(self.checkMesh, self.mesh[0]) for f in self.sixStars]),
            align = "center",
            bgc = btnColour)
        
        cmds.separator(height=15, st = "in")
        cmds.separator(height=15, st = "in")
        
        #Ngon ui items
        cmds.text(label=f"N-gons found: {len(self.ngonsList)}", align='left', height=30)

        cmds.button(label="Select N-gons",
                    command=lambda x: cmds.select([f.replace(self.checkMesh, self.mesh[0]) for f in self.ngonsList]),
                    align = "center",
                    bgc = btnColour)
        
        cmds.separator(height=15, st = "in")
        cmds.separator(height=15, st = "in")
        
        #Triangle UI items
        cmds.text(label=f"Triangles found: {len(self.tris)}", align='left', height=30)

        cmds.button(label="Select Triangles",
                    command=lambda x: cmds.select([f.replace(self.checkMesh, self.mesh[0]) for f in self.tris]),
                    align = "center",
                    bgc = btnColour)
        
        cmds.separator(height=15, st = "in")
        cmds.separator(height=15, st = "in")
        
        #non manifold geometry UI 
        cmds.text(label=f"Non-manifold Geometry found: {len(self.nonManFaces)}", align='left', height=30)

        cmds.button(label="Select Non-Manifold Edges",
                    command=lambda x: cmds.select([f.replace(self.checkMesh, self.mesh[0]) for f in self.nonManFaces]),
                    align = "right",
                    bgc = btnColour)
        
        cmds.separator(height=15, st = "in")
        cmds.separator(height=15, st = "in")

        cmds.button(label="Analyse New Mesh",
            command=lambda x: self.runTool(new_run_state = True),
            align = "center",
            bgc = btnColour)
        
        cmds.button(label="Select Template Mesh",
            command=lambda x: cmds.select(self.checkMesh),
            bgc = btnColour)
        
        cmds.separator(height=15, st = "in")
        cmds.separator(height=15, st = "in")
        
        cmds.setParent('..') #exits
        
        cmds.button(label="Delete Check Mesh",
            command=self.deleteCheckMesh,
            bgc = btnColour)
        
        cmds.separator(height=15, st = "in")

        cmds.showWindow()
    
    def showUI(self):
        if cmds.window('topoResults', exists=True):
            cmds.deleteUI('topoResults')

        cmds.window('topoResults', title='Topology Checker')

        cmds.columnLayout(adj=True)

        cmds.separator(height=15, st = "in")        

        cmds.text(label = 'Select a mesh to Analyse and hit the button below')

        cmds.separator(height=15, st = "in")        

        cmds.button(label="Analyse Mesh",
            command=lambda x: self.runTool(),
            height = 60
            )

        cmds.showWindow()

# ---------------- RUN TOOL ---------------- #

    def runTool(self,new_run_state=False):
        if new_run_state:
            self.new_run=new_run_state

        self.meshSetup()
        if self.vertConfirm() == "Cancel":
            return
        self.duplicateMesh()
        self.progressBar()
        self.locateTriangles()
        self.locateNGons()
        self.locateNonManifold()
        self.locatePoles()
        self.analysisWindow()

        self.new_run=False