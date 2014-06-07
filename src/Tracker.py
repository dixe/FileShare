import socket
import sys
import threading
import utils as util
import json

class JsonRegister():
    """This is a class to hold the json register string, classes is mutable"""
    def __init__(self, jsonString ="{}"):
        # default initialize is empty json string
        self.jsonObject = json.loads(jsonString)
        self.regSem = threading.Semaphore()

    # Given a register string, insert it if it is not present in the json string
    # return json string of registered machines
    def register(self, registerString):
        # start with aquireing the reg semaphore
        registered = ""
        with self.regSem:
            # register
            jsonReg = json.loads(registerString)
            if not self.jsonObject:
                # empty json, just add jsonRegObj
                self.jsonObject = [jsonReg]

            else:
                #json is not empty
                exist = False
                for i in self.jsonObject:
                    if i['ip'] == jsonReg['ip']:
                        exist = True
                if not exist:
                    self.jsonObject.append(jsonReg)
            registered = self.jsonObject
        return json.dumps(registered)
            
    def refresh(self):
        # start with aquireing the reg semaphore
        with self.regSem:
           print "to be implemented"
        

class RequestHandler(threading.Thread):
    """Handle request to the tracker
    should respond with a json list of online machine
    in the network"""
    def __init__(self, conn, address, jsonRegister):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.jsonRegister = jsonRegister

    def run(self):
        #read request
        request = util.readRequest(self.conn)
        # parse request 
        message = util.parseRequest(request)

        # if register, add to registation file

        if message[0] == "Register":
            # update register object
            registered =self.jsonRegister.register(message[1])
            
            # respond with the register list
            response = "Register OK\r\n"
            response += registered
            print "sending"
            self.conn.send(response)
        elif message[0] == "Refresh":
            print "Refresh"
            #self.refresh()
        else: #Must be error at this point
            print ""
        # if refresh, conntact everyone in list, but the connected
        # and see if online
        

        self.conn.close()

    

class Tracker(threading.Thread):
    """The main tracker class"""
    def __init__(self, port, host):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        # json array of registered machines online
        self.jsonRegister = JsonRegister()

    # start
    def run(self):
        print "Running"
        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to anyone
        serversocket.bind((self.host,self.port))
        serversocket.listen(5)
        run = 3
        while run:
            # accept socket from world
            (conn,address) = serversocket.accept()
            # create and start request handler 
            reqhandler = RequestHandler(conn,address,self.jsonRegister)
            reqhandler.start()
            run -= 1

#Start the program
if __name__ == "__main__":
    # tracker on port 80, any host
    tracker = Tracker(80,'')
    tracker.start()
