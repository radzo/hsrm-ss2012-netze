import settings, time
from log import logActivity, debugLog
from socket import socket, AF_INET, SOCK_STREAM

def sync_file(groupname, filename, HOST, PORT):
    blocksize = settings.BLOCKSIZE
  
    s = socket (AF_INET, SOCK_STREAM)
    tryCount = 0
    debugLog("TRYING TO CONNECT")
    while tryCount < settings.TRY_COUNT:
        try:
            s.connect((HOST, PORT))
            debugLog("OK")
            break
        except:
            debugLog("FAILED")
            tryCount += 1
        time.sleep(0.1)
            
    if tryCount > 9:
        return
        
    debugLog("CONNECTED")
     
    fr = open(filename, "rb")

    #sending bllocksize
    s.send (str(blocksize))
    s.recv(1)
    
    while 1:
        # read file
        filecontent = fr.read(blocksize)

        # sending data
        s.send(filecontent)
        s.recv(1)
        
        if len(filecontent) < blocksize:
            break
    
    fr.close()
    s.close()
    
    logActivity(groupname, "addFile", filename, "remote")
