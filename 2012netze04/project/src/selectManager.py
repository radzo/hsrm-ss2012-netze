# usr/bin/python
# -*- coding: utf-8 -*-

import select, socket, time, pickle, reader
from log import debugLog
from sync_receiver import sync_receiver
from sync_sender import sync_file

client_search_duration = 2
client_send_duration = 10

port_tcp = 21567

host_bc = ''
port_bc = 11717
sock_bc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_bc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
sock_bc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock_bc.bind(("<broadcast>", port_bc))

host_udp = ''
port_udp = 19876
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_udp.bind(('', port_udp))

running = True

def rekPathing(gruppe, cLis, cPath):
    for e in cLis:
        cType = type(cLis[e])
        if cType is list:
            host = cLis[e][0][1]
            if host != "LOCAL":
                filepath = cPath + e
                debugLog("GETTING '" + filepath + "' FROM " + host)
                sock_udp.sendto("GETF" + filepath, (host, port_udp))
                sync_receiver(gruppe, filepath + "_N", "172.26.36.113", port_tcp)
        elif cType is dict:
            rekPathing(gruppe, cLis[e], cPath + e + "/")
            
def start(gruppe, GRUPPE_LOC):
    # States:
    # send_bc
    # get_clients
    # require_clients_list
    # get_clients_list
    # update
    # distribute
    # wait
    # send_list
    # passive
    state = "send_bc"
    
    start_time_GC = 0 # get clients timer
    start_time_GL = 0 # get lists timer
    start_time_SEND = 0 # send timer
    
    lis_clients = []
    lis_clients_lists = {}
    
    while running:
      
        if state == "send_bc":
            debugLog("START GETTING CLIENTS")
            nachricht = "HELO" + gruppe
            sock_bc.sendto(nachricht, ("<broadcast>", port_bc))
            state = "get_clients"
            start_time_GC = time.time()
        
        if (time.time() - start_time_GC) > client_search_duration and state == "get_clients":
            debugLog("END GETTING CLIENTS")
            #gibt es einen einen teilnehmer? wenn nicht -> warte
            if lis_clients == []:
                state = "wait"
                debugLog("NOONE TO UPDATE WITH")
            else:
                state = "require_clients_list"
                debugLog("WILL START GETTING CLIENTS DATA")
                print lis_clients
        
        if state == "require_clients_list":
            debugLog("GETTING CLIENT LIST DATA")
            for e in lis_clients:
                sock_udp.sendto("LISTS", (e[0], port_udp))
            start_time_GL = time.time()
            state = "get_clients_list"
            
        if (time.time() - start_time_GL) > client_search_duration and state == "get_clients_list":
            debugLog("LISTS COMPLETE! UPDATING NOW")
            lis_clients_lists['LOCAL'] = reader.readPath(GRUPPE_LOC)
            cLists = []
            cHosts = []
            for e in lis_clients_lists.keys():
                cLists.append(lis_clients_lists[e])
                cHosts.append(e)
            mergedList = reader.mergeDicts(cLists, cHosts)
            print mergedList
            state = "update"
            
        if (time.time() - start_time_SEND) > client_send_duration and state == "send_list":
            debugLog("SENT TOO LONG, WAITING NOW")
            state = "wait"
                
        if state == "update":
            debugLog("UPDATING")
            rekPathing(gruppe, mergedList, GRUPPE_LOC)
            state = "distribute"
        
        if state == "distribute":
            debugLog("DISTRIBUTING")
            
        inputready, outputready, exceptready = select.select([sock_bc, sock_udp], [], [], 5)
        
        for s in inputready:
            
            # empfange antworten per udp und fuege clienten an liste an
            if s == sock_udp and state == "get_clients":
                debugLog("GETTING CLIENT")
                (data, addr) = sock_udp.recvfrom(1024)
                lis_clients.append(addr)
            
            # empfange Dateirequest und sende die Datei    
            elif s == sock_udp and state == "wait":
                (data, addr) = sock_udp.recvfrom(1024)
                if data[:4] == "GETF":
                    fp = data[4:]
                    debugLog("SENDING FILE: " + fp)
                    sync_file(gruppe, GRUPPE_LOC + fp, addr[0], port_tcp)
                
            
            # empfange ordnernamen als Broadcast
            elif s == sock_bc and state == "wait":
                (data, host) = sock_bc.recvfrom(1024)
                if data[4:] == gruppe:
                    debugLog("GETTING BC AND RESPONDING")
                    
                    # sende antwort an broadcast-sender
                    sock_udp.sendto("dabei", (host[0], port_udp))
                    state = "send_list"
                    start_time_SEND = time.time()
                else:
                    debugLog("GOT WRONG GROUP REQUEST")
            
            # empfange listerequest und sende liste
            elif s == sock_udp and state == "send_list":
                debugLog("GETTING LIST REQUEST AND RESPONDING")
                (data, host) = sock_udp.recvfrom(1024)
                
                # sende antwort an broadcast-sender
                d = pickle.dumps(reader.readPath(GRUPPE_LOC))
                sock_udp.sendto(d, (host[0], port_udp))
                state = "wait"
            
            # empfange listen
            elif s == sock_udp and state == "get_clients_list":
                debugLog("GETTING LIST DATA")
                (data, host) = sock_udp.recvfrom(1024)
                
                lis_clients_lists[host[0]] = pickle.loads(data)
                print lis_clients_lists[host[0]]
            
            else:
                data = s.recv(1024)
            
