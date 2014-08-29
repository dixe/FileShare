""" This is ment to be used to handle gui and cli input, by switching functions around."""
import Tkinter as tk

# return true if we want file, false if not
def reciveFileCli(filename, filesize):
    # as if user want toa get file
    while 1:
        answer = raw_input("Getting file %s, with size %d, y to get n to discard " % (filename, filesize))
        if answer is 'y':
            return True
        if answer is 'n':
            return False

def nofun(reciver):
    reciver.recive = False
    reciver.ispressed = True

def yesfun(reciver):
    reciver.recive = True
    reciver.ispressed = True

class Reciver():
    def __init__(self):
        self.recive = False
        self.ispressed = False

# return true if we want file, false if not
def reciveFileGui(filename, filesize):
    # ask if user want to get the file
    reciver = Reciver()
    # open new window
    window = tk.Toplevel()
    window.grid()
    labelText = 'Getting file %s with size %d wonna keep it?' % (filename, filesize)
    name = tk.Label(window,text = labelText)
    name.grid(row=0,column =0)

    yes = tk.Button(window, text = "Yes", command =lambda : yesfun(reciver))

    yes.grid(row= 1, column =0)
    no =tk.Button(window, text = "No", command = lambda : nofun(reciver))
    no.grid(row= 1, column =1)

    # run until a button is pressed
    while True:
        if reciver.ispressed:
            window.destroy()
            return reciver.recive


