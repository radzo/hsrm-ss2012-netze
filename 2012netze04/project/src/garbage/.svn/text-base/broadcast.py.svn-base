# usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
import select
import os, sys, time

port_b = 1717

def makeDir():
    try:
        os.mkdir(dir_name)
    except:
        pass

def sendName():
    sock_b = socket(AF_INET, SOCK_DGRAM)
    sock_b.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
    nachricht = "HELO " + dir_name
    sock_b.sendto(nachricht, ("<broadcast>", port_b))


def getUsers():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    port = 9876
    sock.bind(('', port))
    sock.listen(5)
    try:
        newSocket, address = sock.accept()
        data = ""
        while 1:
            d = newrecv(1024)
            data = data + d
            if (not d) or ("\n" in d): break
        newsend("Danke fuer " + data)
        newclose()
    finally:
        sock.close()


def sendUser(addr):
    sock = socket(AF_INET, SOCK_STREAM)
    port = 9876
    server = addr[1]
    sock.connect((server, port))
    sock.send("eine Anfrage\r\n")
    antwort = sock.recv(1024)
    print "Empfangen:", antwort
    sock.close()

    
def main():
    makeDir()
    sendName()


    getUsers()
    
    sock_b = socket(AF_INET, SOCK_DGRAM)
    sock_b.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock_b.bind(("<broadcast>", port_b))
    while 1:
        (data, addr) = sock_b.recvfrom(1000)
        

        print data[5:]
        if data[4:] == dir_name:
            sendUser(addr)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(-1)

    global dir_name
    dir_name = sys.argv[1]

    main()
