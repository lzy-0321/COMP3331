#coding: utf-8
from socket import *
import sys 
import os 

serverPort = sys.argv[1]
if int(serverPort) < 1024 or int(serverPort) > 8080:
    print("a non-standard port") 
    sys.exit() 

serverSocket = socket(AF_INET, SOCK_STREAM)


serverSocket.bind(('localhost', int(serverPort)))

serverSocket.listen(1)
#The serverSocket then goes in the listen state to listen 
# for client connection requests. 

print("The server is ready to receive")

while 1:
    connectionSocket, addr = serverSocket.accept()
#When a client knocks on this door, the program invokes the accept( ) method for serverSocket, which creates a new socket in the server, called connectionSocket, dedicated to this particular client. The client and server then complete the handshaking, creating a TCP connection between the client’s clientSocket and the server’s connectionSocket. With the TCP connection established, the client and server can now send bytes to each other over the connection. With TCP, all bytes sent from one side not are not only guaranteed to arrive at the other side but also guaranteed to arrive in order

    sentence = connectionSocket.recv(1024)
#wait for data to arrive from the client
    file = sentence.split()[1][1:]
    print(file)
    if os.path.exists(file):
        file_conten = open(file, 'rb').read()
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')
        connectionSocket.sendall(file_conten)
    else:
        connectionSocket.send(b'HTTP/1.1 400 Not Foung\r\n')

    connectionSocket.close()
#close the connectionSocket. Note that the serverSocket is still alive waiting for new clients to connect, we are only closing the connectionSocket.