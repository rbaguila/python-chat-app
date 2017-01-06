# Roinand Aguila
# IT 238 Exer 1
# chat_client.py
# Reference: NETWORK PROGRAMMING II - CHAT SERVER & CLIENT (http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php)

import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port username'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    username = str(sys.argv[3])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'You are now connected to remote host. You can start sending messages'
    sys.stdout.write('[' + username + '] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[' + username + '] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[' + username + '] '); sys.stdout.flush() 

if __name__ == "__main__":

    #sys.exit(chat_client())
    try:
        chat_client()
    except:
        print '\nChat Client Stopped by Ctrl + C'