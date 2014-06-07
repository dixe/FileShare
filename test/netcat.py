import socket
import time
import sys
import os

if len(sys.argv) <= 3:
    print "Usage: python netcat.py <filename> <host> <port>"
    exit(0)

path = os.path.abspath(sys.argv[1])
host = sys.argv[2]    
port = int(sys.argv[3])

if not os.path.exists(path) or not os.path.isfile(path):
    print "File not found: ", path
    exit(0)


# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# attempt to connect to host
sock.connect((host,port))
connected = True

# Send binary data into the connection
with open(path, 'rb') as f:
    data = f.read()
    sock.send(data)

data = ' '
while len(data) > 0:
    data = sock.recv(80)
    print data
    if data.strip() == '':
        break
sock.close()
