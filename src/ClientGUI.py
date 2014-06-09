#!usr/bin/python
import Client
import Tkinter as tk
import json
import os

class ClientGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # see if existing client data exits, else create new

        if not self.loadClient():
            self.setupClient()

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
            print clientJson
            self.client = Client.Client(clientJson['name'], clientJson['port'], clientJson['tracker'])



            return True
        return False


    def setupClient(self):
        # open widgets windows to initialize new client
        print "TODO"

    def setupWidgets(self):
        # Code to add widgets will go here...

        button = tk.Button(self,text="Send", command=self.Client.send())linx



# start the program
if __name__ == "__main__":

    clientGUI = ClientGUI()

    clientGUI.mainloop()
