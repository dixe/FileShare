import socket
import utils as util
import json
import threading
import clientInput as ci
import os
gui = False


class ListenerRequestHandler(threading.Thread):
    """Handle request to the client"""

    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address


    def run(self):
        #read request
        request = util.readRequest(self.conn)

        # parse request
        message = util.parseMessageClient(request)
        # get message type
        if message[0] == "Send":
            filename = message[1].split(' ')[0]
            filesize = int(message[1].split(' ')[1])
            # ask user whether to recive or not
            if not gui:
                recive = ci.reciveFileCli(filename, filesize)
            else:
                recive = ci.reciveFileGui(filename, filesize)

            if recive:
                # send that we want to recive
                self.conn.send("Send\r\n")
                # listen for file data
                d = ' '
                data = ''
                while len(d) >0:
                    d = self.conn.recv(128)
                    data += d

                # write file data to new file
                with open(filename+"OUT",'w') as f:
                    print "writing data: " + data
                    f.write(data)
                print "Saved " + filename+"OUT"
        else:
            print ""


        self.conn.close()

class Listener(threading.Thread):
    """Class that listen on a port for requests from other clients"""
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port


    def run(self):
        print "Listener run ip: " + self.host + " port: " + str(self.port)
        listenersocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listenersocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to anyone

        listenersocket.bind((self.host,self.port))

        listenersocket.listen(5)
        run = True
        while run:
            # accept socket from world
            (conn,address) = listenersocket.accept()
            # create and start request handler
            reqhandler = ListenerRequestHandler(conn,address)
            reqhandler.setDaemon(True)
            reqhandler.start()


class Client():
    def __init__(self, name, port, tracker):
        self.name = name
        self.port = port
        self.tracker = tracker
        self.threadlist = []
        self.jsonReg = [] # emty jsonReg
        self.ip = ([(s.connect(('8.8.8.8', port)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

    def register(self):
        # create the request message
        registerRequest = "Register\r\n"
        registerRequest += "{\"ip\": \"%s\", \"name\": \"%s\", \"port\": %d}" % (self.ip, self.name, self.port)

        # send request to tracker
        response = util.sendRequest(registerRequest,self.tracker)
        # parse response

        parsed = util.parseMessageTracker(response)
        #
        if parsed[0] == 'Register':
            self.jsonReg = json.loads(parsed[1])
        else:
            #error
            print "ERROR" + str(parsed)

    # start to listen for other clienets that want to send communicate
    def listen(self):
        listener = Listener(self.ip, self.port)
        listener.setDaemon(True)
        listener.start()
        self.threadlist.append(listener)

    # send file
    def send(self, filepath, host, port):
        # assume file can be in memory
        with open(filepath,'r') as f:
            filedata =f.read()
        print "sending"
        filepath_name = filepath.rsplit(os.sep,1)
        # select the filename, if len = 0, then filepath_name = filename
        filename = filepath_name[len(filepath_name)-1]
        util.sendFile(filename, filedata, host, port)


    def changeName(self, name):
        self.name = name

    def changePort(self, port):
        self.port = port

    def changeTracker(self, tracker):
        self.tracker = tracker

    def updateIp(self):
        self.ip = ([(s.connect(('8.8.8.8', self.port)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

#start the program
if __name__ =="__main__":
    client = Client("name", 3001, ("192.168.1.6", 3000))
#    client.register()
    client.listen()
    client2 = Client("name", 3002, ("192.168.1.6", 3000))
    client2.send('myfile',"192.168.1.129", 3001)
    while True:
        # makes test clients run
        a=1


