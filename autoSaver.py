import maya.cmds as cmds# pyright: ignore[reportMissingImports] 
import os
import time
from PySide6.QtCore import QTimer# pyright: ignore[reportMissingImports] 

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
        minutes = int(round(minutes))
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
        scene = cmds.file(q=True, sceneName=True)

        folder = os.path.dirname(scene)
        filename = os.path.basename(scene)

        name, ext = os.path.splitext(filename)

        integ = []

        for letter in name:
            if letter.isdigit():
                integ.append(letter)

        integ = "".join(integ)

        if integ:
            integ_new = int(integ) + 1
            new_name = f"{name.replace(integ, '')}{integ_new:02}{ext}"
        else:
            new_name = f"{name}_01{ext}"

        new_path = os.path.join(folder, new_name)

        cmds.file(rename=new_path)

        print("Saving your file...")

        cmds.file(save=True)

        cmds.deleteUI(window, window = True)

    
    def findElapsedTime(self) -> float:
        scene = cmds.file(q = True, sceneName = True)

        if not scene:
            return 0
        todaysDate = time.time() 

        timestamp = os.path.getmtime(scene)

        elapsedTime = todaysDate - timestamp

        return elapsedTime

        
    def perform_autosave(self):
        if cmds.window("Friendly_Reminder", exists=True):
            cmds.deleteUI("Friendly_Reminder")

        window = cmds.window("Friendly_Reminder", title="Friendly Reminder", iconName='Short Name', resizeToFitChildren=True, widthHeight=(400, 100) )

        mainColumn = cmds.columnLayout(adjustableColumn = True)
        cmds.separator(height=10, style="none")
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)

        seconds = int(self.findElapsedTime())

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        cmds.text(f"It's been {hours}h {minutes}m since last save", font = 'boldLabelFont')
        #cmds.image(image="C:/Users/Eirso/OneDrive/Bilder/owowown2.png")

        cmds.setParent(mainColumn)
        cmds.separator(height=10, style="none")

        cmds.button( label= "Save current file?" ,command =lambda *_: self.saving(window=window))
        cmds.button(label = 'increment new file?', command = lambda *_: self.saving_increment(window = window))
        cmds.button(label='Ignore', command=(lambda *_: cmds.deleteUI(window, window=True)))

        cmds.showWindow( window )

    def run_autosaver(self):
        self.start()
        self.perform_autosave()

        
