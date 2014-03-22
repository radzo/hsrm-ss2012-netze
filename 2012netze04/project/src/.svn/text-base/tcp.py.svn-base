from socket import AF_INET, SOCK_DGRAM, socket
from array import array
import pickle

# Set the socket parameters
host = "localhost"
port = 21567
buf = 4096
addr = (host, port)

# Create socket
UDPSock = socket(AF_INET, SOCK_DGRAM)

def_msg = "===Enter message to send to server===";
print "\n", def_msg
a = array('i', [1, 3, 2])
# Send messages
while (1):
    data = raw_input('yes or now')
    if data != "yes":
        break
    else:
        if (UDPSock.sendto(pickle.dumps(a), addr)):
            print "Sending message"

# Close socket
UDPSock.close()

