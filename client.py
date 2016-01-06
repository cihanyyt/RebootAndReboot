import socket
import sys
import os
import time

target_IP = sys.argv[1]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (target_IP, 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address

# hostip = socket.gethostbyname(socket.gethostname())

try:
    sock.connect(server_address)
    hostip = socket.gethostbyname(socket.gethostname())
    # Send data
    sock.sendall(hostip)

    data = ''
        
    while (data == ''):
        data = sock.recv(16)
        print >>sys.stderr, 'received "%s"' % data
        ip_to_server = data
        
    sock.close()
    try:
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port

        server_address = (ip_to_server, 10001)
        print >>sys.stderr, 'listen %s port %s' % server_address

        serverSock.bind(server_address)
        
        # Listen for incoming connections
        serverSock.listen(1)

        connection, client_address = serverSock.accept()
        serverSock.close()
        print >>sys.stderr, 'reboot successs:', target_IP
        ss = 'mstsc /v:' + target_IP

        time.sleep(20)
        print 'Starting Remote Desktop Connetion'
        os.system(ss)
        time.sleep(5)
    except:
        print >>sys.stderr, 'closing serverSock'
        serverSock.close()
        time.sleep(5)
    
except:
    print >>sys.stderr, 'closing socket'
    sock.close()
    time.sleep(5)
