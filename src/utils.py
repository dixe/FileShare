"""THis contaions different util function that is useable
 both tracker and client """

import json
import socket

#List of know commands
commands = ["Register", "Refresh"]
errors = ["ERROR1", "ERROR2", "ERROR3"]
clientmessages = ["Send"]

# give a connection(socket)
# returns the message
def readRequest(conn):
    data = conn.recv(1024)
    return data.strip()

# message parse for tracker communication
# if valid return list with len = 2, first is the first line, second is rest of request
# if error, return [ERROR+errornum,message]
def parseMessageTracker(message):
    #split at first newline
    lines = message.split('\r\n',1)
    firstWord = lines[0].split(' ')[0]
    if not firstWord in commands:
        if not firstWord in errors:
            return ["ERROR1", message] # unknown command, send the command along with error
        else:
            return [firstWord, message]
    return lines


# message parse for clinet-client communication
# if valid return list with len = 2, first is the first line, second is rest of request
# if error, return [ERROR+errornum,message]
def parseMessageClient(message):
    #split at first newline
    lines = message.split('\r\n',1)
    firstWord = lines[0].split(' ')[0]
    if not firstWord in clientmessages:
        if not firstWord in errors:
            return ["ERROR1", message] # unknown command, send the command along with error
        else:
            return [firstWord, message]
    return lines




# given request and a host
# return tracker response, or
def sendRequest(request, tracker):
    if len(request) > 1024:
        return "ERROR2 Too big request size"
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect(tracker)
    except:
        conn.close()
        return "ERROR3 " + str(tracker)
    conn.send(request)
    data = ' '
    response = ""
    while len(data) >0:
        data = conn.recv(128)
        response += data
    conn.close()
    return response

# given file data and a host and port, try to send filedata
def sendFile(filename, filedata, host, port):
    print "connection"
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
    except:
        conn.close()
        return "ERROR3 " + str((host,port))
    sendRequest = "Send\r\n" + filename + " " + str(len(filedata))
    conn.send(sendRequest)
    response = conn.recv(128)
    send = False
    if response.strip() == "Send":

        send = True
        #send file
        sendData = filename + " " + str(len(filedata)) +"\r\n|"
        sendData += filedata
        print "send"
        conn.send(sendData)
    conn.close()
    return send


