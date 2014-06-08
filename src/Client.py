import socket
import utils as util

class Client():

    def __init__(self, name, port, tracker):
        self.ip = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        self.name = name
        self.port = port
        self.tracker = tracker
        
        
    def register(self):
        # create the request message
        registerRequest = "Register\r\n"
        registerRequest += "{ip: %s, name: %s, port: %d}" % (self.ip, self.name, self.port)
        
        # send request to tracker
        print registerRequest
        print self.tracker


    def changeName(self, name):
        self.name = name

    def changePort(self, port):
        self.port = port
  
    def changeTracker(self, tracker):
        self.tracker = tracker

    def updateIp(self):
        self.ip = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
#start the program
if __name__ =="__main__":
    client = Client("name", 80, ("192.168.6",80))
    client.register()
