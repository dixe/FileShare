#!usr/bin/python
import Client
import Tkinter as tk
import tkFileDialog as tkfile
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
        self.client = None
        self.option = ["Update Tracker", "Update Client"]


        if self.loadClient():
            # client loaded and ready to listen
            self.client.listen()
        else:
            self.setupClient()

        # set client to use GUI
        gui = True
        # setup main gui swidgest
        self.setupWidgets()


    # try to load existing client data, true if success false if no existing was found
    def loadClient(self):
        # client is stores in a txt file, with name clientdata
        if os.path.isfile(".client"):
            with open(".client","r") as f:
                clientdata = f.read()
            # if json is malformed, return false
            try:
                clientJson = json.loads(clientdata)
            except:
                return False
            # create client
            self.client = Client.Client(clientJson['name'], clientJson['port'], (clientJson['tracker']['ip'],clientJson['tracker']['port']), True)

            return True
        return False


    def setupGUI(self):
        # open widgets windows to initialize new client
        # client setup Frame
        self.clientWindow = tk.Toplevel()
        self.clientWindow.grid()

        # name field
        if self.client != None:
            name = self.client.name
            port = str(self.client.port)
            trackport = self.client.tracker[1]
            trackip = self.client.tracker[0]

        else:
            name = 'Your machine name'
            port = 'Your machine port'
            trackip = 'Your tracker ip'
            trackport ='Your tracker port'

        #own machine name
        self.nameLabel= tk.Label(self.clientWindow, text = "Machine name")
        self.nameLabel.grid(row=0,column =0)

        self.namefield = tk.Entry(self.clientWindow)
        self.namefield.delete(0,'end')
        self.namefield.insert(0,name)
        self.namefield.grid(row=0,column =1)

        #own port
        self.portLabel= tk.Label(self.clientWindow, text = "Machine port")
        self.portLabel.grid(row=0,column =2)

        self.portfield = tk.Entry(self.clientWindow)
        self.portfield.delete(0,'end')
        self.portfield.insert(0,port)
        self.portfield.grid(row=0,column =3)

        # tracker ip
        self.tracknameLabel= tk.Label(self.clientWindow, text = "Tracker ip")
        self.tracknameLabel.grid(row=1,column =0)

        self.trackerfield = tk.Entry(self.clientWindow)
        self.trackerfield.delete(0,'end')
        self.trackerfield.insert(0,trackip)
        self.trackerfield.grid(row=1,column =1)

        # tracker port
        self.trackportLabel= tk.Label(self.clientWindow, text = "Tracker port")
        self.trackportLabel.grid(row=1,column =2)

        self.trackerportfield = tk.Entry(self.clientWindow)
        self.trackerportfield.delete(0,'end')
        self.trackerportfield.insert(0,trackport)
        self.trackerportfield.grid(row=1,column =3)

        # create button
        self.createButton = tk.Button(self.clientWindow, text = "Update client", command=self.createClient)
        self.createButton.grid()
        # tmp


    def createClient(self):
        trackip = self.trackerfield.get()
        trackport = self.trackerportfield.get()
        name = self.namefield.get()
        myport = self.portfield.get()

        # test to see if they are valid
        try:
            trackport = int(trackport)
            port = int(myport)
        except:
            print "port has to be int"
            return

        self.client = Client.Client(name, port ,(trackip, trackport), True)

        self.startClient()
        self.saveClient()
        # destroy setup window
        self.clientWindow.destroy()

    def saveClient(self):
        self.client.ip
        saveString = """{\"ip\": \"%s\", \"name\": \"%s\", \"port\": %d,
                    \"tracker\": {\"ip\": \"%s\", \"port\": %d}}""" % (self.client.ip, self.client.name,
                                                                       self.client.port, self.client.tracker[0],
                                                                       self.client.tracker[1])
        with open(".client",'w+') as f:
            f.write(saveString)

    def startClient(self):
        if not self.client is None:
            self.client.listen()


    def updateClient(self):
        # stop client listener
        listener = self.client.threads['listener']
        print listener
        if listener == None:
            self.setupGUI()
            return
        listener.stop()
        listener.join()

        self.setupGUI()

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


    ##ONLINE LIST##
        self.onlinelistBox = tk.Listbox(self.onlineFrame, selectmode = 'single',width = 30)
        self.onlinelistBox.grid(sticky = "E",)#pack(expand=1, fill='both')
        if not self.client is None:
            self.refreshOnlineList()

    ##OPTIONMENU##
        self.menuBar = tk.Menu(self.mainFrame)
        self.menuBar.add_command(label = "Update info", command = self.updateClient)
        self.config(menu = self.menuBar)
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
            print "Select client to send file to"
            return
        sendClient = self.client.jsonReg[int(selected[0])]
        # select file
        filepath = tkfile.askopenfilename()
        self.client.send(filepath, sendClient['ip'],sendClient['port'])


    def register(self):
        print "Register"
        self.client.register()
        print "Jsonreg: " +str(self.client.jsonReg)
        self.refreshOnlineList()




# start the program
if __name__ == "__main__":

    clientGUI = ClientGUI()

    clientGUI.mainloop()
