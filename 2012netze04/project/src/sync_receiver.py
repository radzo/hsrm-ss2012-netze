#!/usr/bin/python
 
from log import logActivity, debugLog
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Receives files from sync_sender
def sync_receiver(groupname, fileName, HOST, PORT):
  
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    
    try:
        conn, addr = s.accept()
        debugLog("CONNECTION OPENED")
        
        # file writer -> creates file with name <fileName> and sets it writable
        fw = file(fileName, "wb")
            
        # receiving blocksize
        blocksize = int (conn.recv(32))
        conn.send("1")  
        
        # file content puffer
        filecontent = ''
        # receiving data
        debugLog("receiving file content..")
        
        while 1:
            data = conn.recv(blocksize)
            conn.send("1")
            debugLog(data)
            filecontent += data
            if len(data) < blocksize:
                break
        
        debugLog("done")
       
        # writing data to file
        fw.write(filecontent)
        conn.close()
        fw.close()
    finally:
        s.close()
    
    logActivity(groupname, "addFile", fileName, "local")
