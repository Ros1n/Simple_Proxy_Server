import socket
import threading
import urllib.request

class myThread(threading.Thread):
    def __init__(self, threadId, connectionSocket, clientAddress):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.connectionSocket = connectionSocket
        self.clientAddress = clientAddress

    def run(self):
        print('start socket'+str(self.threadId))
        keep_socket(self.connectionSocket, self.clientAddress)

def keep_socket(connectionSocket, clientAddress):
    #while connectionSocket.connect_ex(clientAddress) == 0:
    while True: 
        message = connectionSocket.recv(1024).decode("utf-8")
        method = message.split()[0]
        if method == 'GET':
            req = message[1]
            resp = urllib.request.urlopen(req).read() 
            connectionSocket.send(byte(resp)) #how to open the html page with this?
        elif method == 'POST':
            req = message[1]
            entity = message[2]

        if sentence == 'finish' or sentence == 'exit':
            connectionSocket.close()
        else:
            continue
    #else:
        #print(connectionSocket.connect_ex(clientAddress))




def main():
    serverName = ''
    serverPort = 12007
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverName,serverPort))
    serverSocket.listen(10)
    print('The server is ready to receive')


    count = 0
    while 1:
        try:
            connectionSocket, clientAddress = serverSocket.accept()
            t = myThread(count, connectionSocket, clientAddress)
            #t = threading.Thread(target=create_socket, args=connectionSocket)
            t.start()
            #thread.start_new_thread(create_socket, connectionSocket)
            count += 1
        except:
            print('connection socket doesn\' work')
            serverSocket.close()
    serverSocket.close()

if __name__ == '__main__':
    main()
