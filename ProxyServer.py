import socket
import threading
import sys

class myThread(threading.Thread):
    def __init__(self, threadId, connectionSocket, clientAddress):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.connectionSocket = connectionSocket
        self.clientAddress = clientAddress

    def run(self):
        print('start thread'+str(self.threadId))
        keep_socket(self.connectionSocket, self.clientAddress)


def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(bytes(data.encode('utf8')))

        while 1:
            reply = s.recv(1024).decode('utf-8')
            if len(reply) > 0:
                conn.send(reply)
                dar = float(len(reply))
                dar = "%s KB" % ("%.3s" % str(float(dar / 1024)))
                print("[*] Request Done: %s => %s <= " % (str(addr[0]), str(dar)))
            else:
                break

        s.close()
        #conn.close()
    except:
        s.close()
        conn.close()
        sys.exit(1)


def keep_socket(connectionSocket, clientAddress):
    #while connectionSocket.connect_ex(clientAddress) == 0:
    while True: 
        data = connectionSocket.recv(1024).decode("utf-8")
        try:
            first_line = data.split('\n')[0]
            url = first_line.split(' ')[1]
            http_pos = url.find("://")
            tmp = url if http_pos == -1 else url[http_pos+3:]
            port_pos = tmp.find(":")

            webserver_pos = tmp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(tmp)
            webserver = ''
            port = -1
            if port == -1 or webserver_pos < port_pos:
                port = 80
                webserver = tmp[:port_pos]

            proxy_server(webserver, port, connectionSocket, data, clientAddress)
        except:
            print("schew up in socket part")
    #else:
        #print(connectionSocket.connect_ex(clientAddress))




def main():
    serverName = ''
    serverPort = 8080
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverName,serverPort))
    serverSocket.listen(10)
    print('The server is ready to receive')


    count = 0
    while True:
        try:
            connectionSocket, clientAddress = serverSocket.accept()
            t = myThread(count, connectionSocket, clientAddress)
            #t = threading.Thread(target=create_socket, args=connectionSocket)
            t.start()
            #thread.start_new_thread(create_socket, connectionSocket)
            count += 1
        except:
            print('connection socket doesn\'t work')
            serverSocket.close()
    serverSocket.close()

if __name__ == '__main__':
    main()
