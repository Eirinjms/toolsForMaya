import maya.cmds as cmds# pyright: ignore[reportMissingImports] 
import os
from PySide6.QtCore import QTimer# pyright: ignore[reportMissingImports] 
import math

class AutoSaver:

    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.perform_autosave)

    def configWindow(self, *args):
        if cmds.window('config', exists = True):
            cmds.deleteUI('config')

        configWindow = cmds.window('config', iconName='Short Name', resizeToFitChildren=True, widthHeight=(400, 100))
        column = cmds.columnLayout(adj = True)
        cmds.separator(height = 10, style = 'none')
        rows = cmds.rowColumnLayout(numberOfColumns = 3, columnAttach =(1, 'right', 0))
        cmds.text('How many minutes between reminders?')
        self.iteration = cmds.textField()

        cmds.button('Accept', command = lambda *_: self.closeWindow(window = configWindow))
        cmds.showWindow('config')
    
    def closeWindow(self, window):
        self.start()
        cmds.deleteUI(window)

    def start(self):
        self.iterations = cmds.textField(self.iteration, q=True, text=True)
        minutes = float(self.iterations)
        minutes = int(math.ceil(minutes))
        milliseconds = minutes * 60 * 1000
        self.timer.start(milliseconds)
        print(f"Autosave started ({minutes} min interval)")

    def stop(self):
        self.timer.stop()
        print("Autosave stopped")
    

    def saving(self, *args, window):
        cmds.file(save = True)
        print("saving finished! :D")
        cmds.deleteUI(window, window=True)

    def saving_increment(self, *args, window):
        scene = cmds.file(q = True, sceneName = True)
        scene_name = os.path.basename(scene)
        scene_ma = scene_name.replace(".ma", "")

        integ = []

        for i in range(len(scene_ma)):
            letter = scene_ma[i]
            if letter.isdigit():
                integ.append(letter)
            else:
                continue

        integ = "".join(integ)
        if len(integ) > 0:
            integ_new = int(integ) + 1
            cmds.file(rename = f"{scene_ma.replace(str(integ),'')}{integ_new:02}")
        else: 
            cmds.file(rename = f"{scene.replace('.ma', '_' )}01")

        print('Saving your file babygirl...')
        cmds.file(save = True)
        cmds.deleteUI(window, window = True)
        
    def perform_autosave(self):
        if cmds.window("Friendly Reminder", exists=True):
            cmds.deleteUI("Friendly Reminder")

        window = cmds.window( title="Friendly Reminder", iconName='Short Name', resizeToFitChildren=True, widthHeight=(400, 100) )

        mainColumn = cmds.columnLayout(adjustableColumn = True)
        cmds.separator(height=10, style="none")
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
        
        cmds.text("It's been long since u saved pookie :(", font = 'boldLabelFont')
        cmds.image(image="C:/Users/Eirso/OneDrive/Bilder/owowown2.png")

        cmds.setParent(mainColumn)
        cmds.separator(height=10, style="none")

        cmds.button( label= "Save?" ,command =lambda *_: self.saving(window=window))
        cmds.button(label = 'increment?', command = lambda *_: self.saving_increment(window = window))
        cmds.button( label='Hurt owowon and ignore it :(', command=('cmds.deleteUI(\"' + window + '\", window=True)') )

        cmds.showWindow( window )

    def run_autosaver(self):
        self.start()
        self.perform_autosave()

        
