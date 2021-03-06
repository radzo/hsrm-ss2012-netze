import settings, time, sha
from logging import logActivity
from socket import socket, AF_INET, SOCK_STREAM
from sync_server import sync_server

data = []


def sync(groupname, filename):
    logActivity(groupname, comment="Die Synchronisierung des Ordners >>" + groupname + "<< wird gestartet!")

    if settings.DEBUG == 1:
        logActivity(groupname, comment="Ein Kommentar")
        logActivity(groupname, "addFile", "Dateiname")
        logActivity(groupname, "removeFile", "Dateiname")
        logActivity(groupname, "update", "Dateiname", modifiedDate=time.strftime("%d.%m.%Y um %H:%M:%S Uhr"))
    
    sync_file(groupname, filename);
 

def sync_file(groupname, filename):
    HOST = ''
    PORT = 50007
  
    fw = file(filename, "wb")


    s = socket (AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()


    # receiving blocksize
    blocksize = int(conn.recv(32))
    conn.send("1")

    while 1:
        # receiving data
        filecontent = ''
        while len(filecontent) < blocksize:
            filecontent += conn.recv(blocksize - len(filecontent))
        conn.send("1")
        checksum = conn.recv(160)
        conn.send("1")
        print "CHECKSUM:", checksum

        # checking file integrity
        sha_check = sha.new(filecontent)
        if not checksum == sha_check.hexdigest():
            print "Fehler in der Uebertragung! -> Abbruch"

        # writing data to file
        fw.write(filecontent)
        if len(filecontent) != blocksize:
            break
    fw.close()
    s.close()
    
    logActivity(groupname, "addFile", filename, "local")
    
    while 1:
        try:
            txt = input("Enter -> Ende")
            break
        except:
            break
        

