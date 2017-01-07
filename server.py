'''
Roinand Aguila
IT 238 Exercise 2
'''

import thread
from Tkinter import *
from socket import *
import re
import select



#Initiate socket and bind port to Server
WindowTitle = 'IT238 Chat v0.1 - Server'

SOCKET_LIST = []
RECV_BUFFER = 1024 


s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)



def ClickAction():
    
    thread.start_new_thread(GetConnected,())
    

    

def PressAction(event):
    PortBox.config(state=NORMAL)
    ClickAction()
def DisableEntry(event):
    PortBox.config(state=DISABLED)


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


# GUI

#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create a Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Waiting for Client Connections...\n")
ChatLog.config(state=DISABLED)

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create the Button to send message
SendButton = Button(base, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",
                    command=ClickAction)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

#Create entry box for port
PortBox = Text(base, bd=0, bg="white",width="10", height="1", font="Arial")
PortBox.insert(END, "PORT")
PortBox.bind("<Return>", DisableEntry)
PortBox.bind("<KeyRelease-Return>", PressAction)

StartButton = Button(base, font=30, text="Start Server", width="10", height=2,
                    bd=0, fg="white", justify=CENTER, bg="#3b5998", activebackground="#4e69a2",
                    command=ClickAction)


#Place all components on the screen
PortBox.place(x=100,y=6, height=22)
scrollbar.place(x=376,y=35, height=447)
ChatLog.place(x=6,y=35, height=447, width=370)
StartButton.place(x=200, y=6, height=25)



#---------------------------------------------------#
#----------------CONNECTION MANAGEMENT--------------#
#---------------------------------------------------#
def GetConnected():
    PORT = 9009
    HOST = '' 
    print "Port: %s"%(PortBox.get("1.0", "end-1c"))
    PORT = int(PortBox.get("1.0", "end-1c"))
    s.bind((HOST, PORT))
    s.listen(10)
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(s)

    
    while 1:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)



        for sock in ready_to_read:
            # a new connection request recieved
            if sock == s: 
                sockfd, addr = s.accept()
                SOCKET_LIST.append(sockfd)
                # print "Client (%s, %s) connected" % addr
                LoadConnectionInfo(ChatLog, '\n Connected with: ' + str(addr) + '\n---------------------------------------------------------------')
                
                broadcast(s, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(1024)
                    if data:
                        # there is something in the socket
                        broadcast(s, sock, data)
                        
                        LoadOtherEntry(ChatLog, data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(s, sock, "Client (%s, %s) is offline\n" % addr) 
                        # LoadConnectionInfo(ChatLog, "Client "+ str(addr) + "is offline")

                # exception 
                except:
                    broadcast(s, sock, "Client (%s, %s) is offline\n" % addr)
                    # LoadConnectionInfo(ChatLog, "Client "+ str(addr) + "is offline")
                    continue

    s.close()

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for s in SOCKET_LIST:
        # send the message only to peer
        if s != server_socket and s != sock :
            try :
                LoadConnectionInfo(ChatLog, message)
                s.send(message)
            except :
                # broken socket connection
                s.close()
                # broken socket, remove it
                if s in SOCKET_LIST:
                    SOCKET_LIST.remove(s)
    


base.mainloop()


