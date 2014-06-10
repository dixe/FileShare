#!usr/bin/python
import Client
import Tkinter as tk
import json
import os

class ClientGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # see if existing client data exits, else create new
        # default height and width
        self.height = 400
        self.width = 400
        self.onlineFH = 300
        self.onlineFW = 300
        self.buttonFH = 300
        self.buttonFW = 100

        if not self.loadClient():
            self.setupClient()

        # start client listen
        self.client.listen()

        # set client to use GUI
        gui = True
        # setup main gui swidgest
        self.setupWidgets()


    # try to load existing client data, true if success false if no existing was found
    def loadClient(self):
        # client is stores in a txt file, with name clientdata
        if os.path.isfile("clientdata"):
            with open("clientdata","r") as f:
                clientdata = f.read()
            # if json is malformed, return false
            try:
                clientJson = json.loads(clientdata)
            except:
                return False
            # create client
            self.client = Client.Client(clientJson['name'], clientJson['port'], (clientJson['tracker']['ip'],clientJson['tracker']['port']))

            return True
        return False


    def setupClient(self):
        # open widgets windows to initialize new client
        print "TODO"

    def setupWidgets(self):
        # create a main frame for widgets
        self.mainFrame = tk.Frame(self, width = self.width, height = self.height)
        # set to use width and height
        self.mainFrame.grid_propagate(False)
        self.mainFrame.grid()
##FRAMES##
        # the frame to hold online persons
        self.onlineFrame = tk.Frame(self.mainFrame, width = self.onlineFW, height = self.onlineFH, background='white')
        self.onlineFrame.grid_propagate(False)
        self.onlineFrame.grid(row = 0, column = 0) # set in upper left corner
        # button frame
        self.buttonFrame = tk.Frame(self.mainFrame, width = self.buttonFW, height = self.buttonFH, background='black')
        self.buttonFrame.grid_propagate(False)
        self.buttonFrame.grid(row = 0, column = 1)
##ONLINE##
        self.onlinelistBox = tk.Listbox(self.onlineFrame, selectmode = 'single',width = 30)
        self.onlinelistBox.grid(sticky = "E",)#pack(expand=1, fill='both')
        self.refreshOnlineList()

##BUTTONS##
        # create register button
        self.registerbutton = tk.Button(self.buttonFrame,text="Register", command=self.register)
        self.registerbutton.grid(row=0,sticky='W',pady=40)

        # cReate A Send Button
        self.sendbutton = tk.Button(self.buttonFrame,text="Send", command=self.send)
        self.sendbutton.grid(row=1, sticky='W',pady = 40)


    def refreshOnlineList(self):
        #clear list
        self.onlinelistBox.delete(0,'end')
        # for every json client in self.client
        for client in self.client.jsonReg:
            clientString = "Name: " + str(client['name']) + ", ip: " +  str(client['ip']) + ', port: ' + str(client['port'])
            self.onlinelistBox.insert('end',clientString)


    # send file to selected client
    def send(self):
        # get selected client
        selected = self.onlinelistBox.curselection()
        if len(selected) <1:
            return
        client = self.onlinelistBox.get(selected[0])

    def register(self):
        self.client.register()
        print "Jsonreg: " +str(self.client.jsonReg)
        self.refreshOnlineList()




# start the program
if __name__ == "__main__":

    clientGUI = ClientGUI()

    clientGUI.mainloop()
