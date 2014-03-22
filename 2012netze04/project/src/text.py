import select
import socket

host_bc = ''
port_bc = 1717
sock_bc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_bc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

nachricht = "HELO gruppe"
sock_bc.sendto(nachricht, ("<broadcast>", port_bc))

running = 1
while running:
    (inputready, outputready, exceptready) = select.select([sock_bc], [], [])
    
    for s in inputready:
        
        if s == sock_bc:
            (data, addr) = sock_bc.recvfrom(1000)
            print data
