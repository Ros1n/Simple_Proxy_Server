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
        print('start thread '+str(self.threadId))
        keep_socket(self.connectionSocket, self.clientAddress)


def proxy_server(webserver, port, conn, data, addr):
    try:
        print('start proxy')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        webserver = webserver.replace("www.", "", 1)
        s.connect((webserver, port))
        s.send(bytes(data.encode('utf8')))

        while 1:
            reply = s.recv(1024).decode('utf-8') #read reply or data from end web server
            if len(reply) > 0:
                conn.send(reply.encode('utf-8'))
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


def keep_socket(connectionSocket, clientAddress): #every connection keep a socket and received data
    #while connectionSocket.connect_ex(clientAddress) == 0:
    h = "Host:"
    while True: 
        data = connectionSocket.recv(1024).decode('utf-8')
        try:
            host = data.split(h)[1] if h in data else ''
            first_line = data.split('\n')[0]
            url = first_line.split(' ')[1]
            http_pos = url.find("://")
            tmp = url[1:] if http_pos == -1 else url[http_pos+3:]
            port_pos = tmp.find(":")

            webserver_pos = tmp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(tmp)
            webserver = ''
            port = -1
            if port == -1 or webserver_pos < port_pos:
                port = 80
                webserver = tmp[:port_pos]
            else:
                port = int((tmp[(port_pos+1):])[:webserver_pos-port_pos-1])
            
            proxy_server(host + webserver, port, connectionSocket, data, clientAddress)
        except:
            print("schew up in socket part")
    #else:
        #print(connectionSocket.connect_ex(clientAddress))




def main():
    serverName = ''
    serverPort = 8002 #listening port
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverName,serverPort))
    serverSocket.listen(5)
    print('The server is ready to receive')

    count = 0
    while True:
        try:
            connectionSocket, clientAddress = serverSocket.accept()
            t = myThread(count, connectionSocket, clientAddress)
            #t = threading.Thread(target=create_socket, args=connectionSocket)
            t.start()
            count += 1
            #thread.start_new_thread(create_socket, connectionSocket)
        except:
            print('connection socket doesn\'t work')
            serverSocket.close()
    serverSocket.close()

if __name__ == '__main__':
    main()
