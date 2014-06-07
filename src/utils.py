"""THis contaions different util function that is useable
 both tracker and client """

import json


#List of know commands
commands = ["Register", "Refresh"]

# give a connection(socket)
# returns the message
def readRequest(conn):
    data = conn.recv(1024)
    return data.strip()

# if valid return list with len = 2, first is the first line, second is rest of request
def parseRequest(request):
    #split at first newline
    lines = request.split('\r\n',1)
    firstWord = lines[0].split(' ')[0]
    if not firstWord in commands:
        return ["ERROR","1 " + firstWord] # unknown command, send the command along with error
    return lines

