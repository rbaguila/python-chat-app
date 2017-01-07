'''
Roinand Aguila
IT 238 Exercise 2
'''

import thread
from Tkinter import *
from socket import *
import re
import sys
import select


# Connection Variables
WindowTitle = 'IT238 Chat v0.1 - Client'
HOST = ""
PORT = 9009
s = socket(AF_INET, SOCK_STREAM)



def ConnectAction():
    thread.start_new_thread(ReceiveData,())

def LeaveAction():
    s.close()
    exit()

# Keyboard Events
def PressAction(event):
    EntryBox.config(state=NORMAL)
    ClickAction()
def DisableEntry(event):
    EntryBox.config(state=DISABLED)

# Chat Functions
def FilteredMessage(EntryText):
    """
    Filter out all useless white lines at the end of a string,
    returns a new, beautifully filtered string.
    """
    EndFiltered = ''
    for i in range(len(EntryText)-1,-1,-1):
        if EntryText[i]!='\n':
            EndFiltered = EntryText[0:i+1]
            break
    for i in range(0,len(EndFiltered), 1):
            if EndFiltered[i] != "\n":
                    return EndFiltered[i:]+'\n'
    return ''
    
def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ChatLog.insert(END, EntryText+'\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

def LoadMyEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            LineNumber = float(ChatLog.index('end'))-1.0
            Username = UserNameBox.get("1.0", "end-1c")
            ChatLog.insert(END, Username +": "+ EntryText)
            ChatLog.tag_add(Username, LineNumber, LineNumber+0.4)
            ChatLog.tag_config(Username, foreground="#3b5998", font=("Arial", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


def LoadOtherEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            try:
                LineNumber = float(ChatLog.index('end'))-1.0
            except:
                pass
            ChatLog.insert(END, EntryText)
            ChatLog.tag_add(":", LineNumber, LineNumber+0.6)
            ChatLog.tag_config(":", foreground="#04B404", font=("Arial", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

# Connection

def ReceiveData():
    s.settimeout(2)
    try:
        
        HOST = IPBox.get("1.0", "end-1c")
        PORT = int(PortBox.get("1.0", "end-1c"))

        print HOST
        print PORT
        s.connect((HOST, PORT))
        LoadConnectionInfo(ChatLog, '[ Succesfully connected ]\n---------------------------------------------------------------')
    except:
        LoadConnectionInfo(ChatLog, '[ Unable to connect ]')
        return
    
    while 1:

        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(1024)
                if not data :
                    LoadConnectionInfo(ChatLog, '\n [ Disconnected from chat server ]\n')
                    # print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data   
                    LoadOtherEntry(ChatLog, data) 
    s.close()


# Mouse Events
def ClickAction():

    #Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))
    LoadMyEntry(ChatLog, EntryText)

    #Scroll to the bottom of chat windows
    ChatLog.yview(END)

    #Erace previous message in Entry Box
    EntryBox.delete("0.0",END)
            
    #Send my mesage to all others
    username = UserNameBox.get("1.0", "end-1c")
    s.sendall(username+': '+EntryText)

# GUI

#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create a Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Connecting to your partner..\n")
ChatLog.config(state=DISABLED)

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set



#Create the Button to send message
LeaveButton = Button(base, font=30, text="Leave", width="10", height=2,
                    bd=0, fg="white", justify=CENTER, bg="#3b5998", activebackground="#4e69a2",
                    command=LeaveAction)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

#Create entry box for port
PortBox = Text(base, bd=0, bg="white",width="6", height="1", font="Arial")
PortBox.insert(END, "PORT")
PortBox.bind("<Return>", DisableEntry)
PortBox.bind("<KeyRelease-Return>", PressAction)

#Create entry box for ip
IPBox = Text(base, bd=0, bg="white",width="11", height="1", font="Arial")
IPBox.insert(END, "IP ADDRESS")
IPBox.bind("<Return>", DisableEntry)
IPBox.bind("<KeyRelease-Return>", PressAction)

#Create entry box for username
UserNameBox = Text(base, bd=0, bg="white",width="13", height="1", font="Arial")
UserNameBox.insert(END, "USER NAME")
UserNameBox.bind("<Return>", DisableEntry)
UserNameBox.bind("<KeyRelease-Return>", PressAction)

#Create the Button to send message
username = UserNameBox.get("1.0", "end-1c")
SendButton = Button(base, font=30, text="Send", width="10", height=2,
                    bd=0, fg="white", justify=CENTER, bg="#3b5998", activebackground="#4e69a2",
                    command=ClickAction)

ConnectButton = Button(base, font=30, text="Connect", width="5", height=2,
                    bd=0, fg="white", justify=CENTER, bg="#3b5998", activebackground="#4e69a2",
                    command=ConnectAction)

# Place all components on the screen
IPBox.place(x=132,y=6, height=22)
PortBox.place(x=240,y=6, height=22)
UserNameBox.place(x=6,y=6, height=22)
scrollbar.place(x=376,y=35, height=357)
ChatLog.place(x=6,y=35, height=357, width=370)
EntryBox.place(x=6, y=401, height=90, width=265)
SendButton.place(x=271, y=401, height=45)
LeaveButton.place(x=271, y=446, height=45)
ConnectButton.place(x=310, y=6, height=25)






base.mainloop()
