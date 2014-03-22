# usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, settings
from log import removeLogfile, createLogfile
from help import showHelp
from selectManager import start

HOST = "172.26.36.117"
PORT = 21567

if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        groupname = sys.argv[1]
    
        ## Existiert der übergebene Ordner?
        if os.path.isdir("../data/" + groupname): 
    
            if(settings.DEBUG == 1 and os.path.isfile(groupname + ".log")):
                removeLogfile(groupname)
        
            ## Wenn das Log-File noch nicht existiert
            if not os.path.isfile(groupname + ".log"):
                createLogfile(groupname)
            
          
            #### HIER START DER ANWENDUNG ####
            """if (sys.argv[3] == 'host'):
                sync_sender(groupname, '../hier.zip', HOST, PORT)
            else:
                sync_receiver(groupname, '../da.zip', HOST, PORT)"""
            start(groupname, "../data/" + groupname + "/")
                
        else:
            print "Der Ordner >>" + groupname + "<< existiert nicht. Synchronisierung abgebrochen!"
        
    else:
        showHelp()
