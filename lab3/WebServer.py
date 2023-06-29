from socket import *
#using the socket module
import sys

if not (len(sys.argv) < 3 and len(sys.argv) > 1):
    sys.exit()
    
serverPort = int(sys.argv[1])

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)

print ("The server is ready to receive, on port: " + str(serverPort))

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    if sentence:
        request = sentence.decode().split('\n')
        if ("GET" in request[0]):
            filename = request[0].split()[1][1:]
            try: 
                f = open(filename, "rb")
                outputdata = f.read()
                f.close()
                print("Sending file " + filename)
                # Send one HTTP header line into socket
                length = len(outputdata)
                if filename.endswith(".html"):
                    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + str(length) + "\r\n\r\n"           
                elif filename.endswith(".png"):
                    header = "HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length: " + str(length) + "\r\n\r\n"
                connectionSocket.send(header.encode())
                connectionSocket.sendall(outputdata)
                print("File sent")
                connectionSocket.close()
            except IOError:
                print("404 not found")
                error_html = "<html><head></head><body><h1>404 Not Found</h1><p>The requested file was not found on the server.</p></body></html>"
                header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: " + str(len(error_html)) + "\r\n\r\n"
                connectionSocket.send(header.encode())
                connectionSocket.sendall(error_html.encode())
                connectionSocket.close()
        else:
            print("Invalid request")
            connectionSocket.close()
    else:
        print("Empty request")
        connectionSocket.close()    