# usr/bin/python
# -*- coding: utf-8 -*-

import time, os, settings
from string import Template

## Templates
update = Template("Die Datei $name wurde auf $where auf den Stand vom $date aktualisiert.")
addFile = Template("Die Datei $name wurde auf $where hinzugefügt.")
removeFile = Template("Die Datei $name wurde auf $where entfernt.")
addFolder = Template("Der Ordner $name wurde auf $where hinzugefügt.")
removeFolder = Template("Der Ordner $name wurde auf $where entfernt.")
    
def logActivity(groupname, command="", filename=None, dest="", modifiedDate=None, comment=""):
    outfile = open(groupname + ".log", "a")
   
    outfile.write("(" + time.strftime("%d.%m.%Y um %H:%M:%S Uhr") + "): ")
    
    destination = ""
    if(dest == "local"):
        destination = "dem lokalen Rechner"
    if(dest == "remote"):
        destination = "dem entfernten Rechner"
                          
    if(command == ""):
        outfile.write(comment)
    if(command == "update"):
        outfile.write(update.substitute(name=filename, where=destination, date=modifiedDate))
    if(command == "removeFile"):
        outfile.write(removeFile.substitute(name=filename, where=destination))
    if(command == "addFile"):
        outfile.write(addFile.substitute(name=filename, where=destination))
    if(command == "removeFolder"):
        outfile.write(removeFolder.substitute(name=filename, where=destination))
    if(command == "addFolder"):
        outfile.write(addFolder.substitute(name=filename, where=destination))
    outfile.write("\n")
    
    if(settings.DEBUG == 1): 
        print("Ein Eintrag wurde geloggt!")
    
    outfile.close()

def createLogfile(groupname):
    if(settings.DEBUG == 1): 
        print("Es existiert noch keine Log-Datei. Eine Log-Datei wird erstellt..")
 
    outfile = open(groupname + ".log", "a")
    outfile.write("\n\n")
    outfile.write("$$\                           $$$$$$\  $$\ $$\           \n")
    outfile.write("$$ |                         $$  __$$\ \__|$$ |          \n")
    outfile.write("$$ |      $$$$$$\   $$$$$$\  $$ /  \__|$$\ $$ | $$$$$$\  \n")
    outfile.write("$$ |     $$  __$$\ $$  __$$\ $$$$\     $$ |$$ |$$  __$$\ \n")
    outfile.write("$$ |     $$ /  $$ |$$ /  $$ |$$  _|    $$ |$$ |$$$$$$$$ |\n")
    outfile.write("$$ |     $$ |  $$ |$$ |  $$ |$$ |      $$ |$$ |$$   ____|\n")
    outfile.write("$$$$$$$$\\$$$$$$  |\$$$$$$$ |$$ |      $$ |$$ |\$$$$$$$\ \n")
    outfile.write("\________|\______/  \____$$ |\__|      \__|\__| \_______|\n")
    outfile.write("                   $$\   $$ |                            \n")
    outfile.write("                   \$$$$$$  |                            \n")
    outfile.write("                    \______/                             \n")
    outfile.write("                               Gruppenname: " + groupname + "\n\n")
    outfile.close()
    if(settings.DEBUG == 1): 
        print(".. die Log-Datei wurde erstellt!")

def debugLog(message):
    if(settings.DEBUG == 1): 
        print "--", message, "--"

def removeLogfile(groupname):
    os.remove(groupname + ".log")
    if(settings.DEBUG == 1): 
        print("..die Log-Datei wurde gelöscht!")
    
