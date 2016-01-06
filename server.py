import socket
import sys
import subprocess
import os
import time

clientIP = ''
fileName="clientIP.txt"
if (os.path.isfile(fileName)):
    f = file(fileName,'r')
    clientIP = f.read()

    if clientIP and (not clientIP.isspace()):
        # Create a TCP/IP socket
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening

        print >>sys.stderr, 'connecting to %s' % clientIP
        client_address = (clientIP,10001)
        try:
            sock2.connect(client_address)
            print >>sys.stderr, 'connected'             
        except:
            print >>sys.stderr, 'no connection'                     
        sock2.close()
        
f = file(fileName,'w+')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
hostip = socket.gethostbyname(socket.gethostname())
server_address = (hostip, 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address

sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

try:
    print >>sys.stderr, 'connection from', client_address

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(16)
        print >>sys.stderr, 'received "%s"' % data
        f.write(client_address[0])
        f.flush()
        f.close()
        connection.sendall(client_address[0])
        time.sleep(1)
        allowed = subprocess.check_output(['CPU_Control.exe','/allowreboot'])
        subprocess.check_output(['shutdown','-r','-t', '0'])

finally:
    # Clean up the connection
    connection.close()
    if not f.closed:
        f.close()
