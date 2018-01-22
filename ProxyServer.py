import socket
import threading
import sys

config = { "BLACKLIST_DOMAINS":[],
			"HOST_NAME":'/',
			"BIND_PORT": 80,
			"CONNECTION_TIMEOUT":100
		}

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
        print('start the proxy server with host ', host, " and port ", port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        webserver = webserver.replace("www.", "", 1)
        s.settimeout(config["CONNECTION_TIMEOUT"])
        s.connect((webserver, port))
        s.send(bytes(data.encode('utf8')))

        while True:
            reply = s.recv(1024).decode('utf-8') #read reply or data from end web server
            if len(reply) > 0:
            	#check if the host:port is blacklisted
            	for i in range(0, len(config["BLACKLIST_DOMAINS"])):
            		if config["BLACKLIST_DOMAINS"][i] in webserver:
            			conn.close()
                conn.send(reply.encode('utf-8')) #suppose to send to browser
                dar = float(len(reply))
                dar = "%s KB" % ("%.3s" % str(float(dar / 1024)))
                print("[*] Request Done: %s => %s <= " % (str(addr[0]), str(dar)))
            else:
                break

        s.close()
        conn.close()
    except Exception as inst:
    	if s:
        	s.close()
       	if conn:
        	conn.close()
        print(type(inst))
        sys.exit(1)


def keep_socket(connectionSocket, clientAddress): 
	#every connection keep a socket and received data
    #while connectionSocket.connect_ex(clientAddress) == 0:
    h = "Host:"
    while True: 
        data = connectionSocket.recv(1024).decode('utf-8')
        try:
            host = data.split(h)[1] if h in data else ''
            first_line = data.split('\n')[0] #parse the first line
            url = first_line.split(' ')[1] 	 #get url
            http_pos = url.find("://")		 #find pos of ://
            tmp = url[1:] if http_pos == -1 else url[http_pos+3:]
            port_pos = tmp.find(":")		 #find port pos if any

            webserver_pos = tmp.find("/")	 #find end of web server
            if webserver_pos == -1:
                webserver_pos = len(tmp)

            webserver = ''
            port = -1
            if port_pos == -1 or webserver_pos < port_pos:
                port = 80					#default port
                webserver = tmp[:webserver_pos]
            else:
                port = int((tmp[(port_pos + 1):])[:webserver_pos- port_pos - 1])
                webserver = tmp[:port_pos]
            
            proxy_server(host + webserver, port, connectionSocket, data, clientAddress)
        except:
            print("schew up in socket part")
            pass        

def main():
    serverName = ''
    serverPort = 8003 #listening port
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #re-use the socket
    serverSocket.bind((serverName,serverPort))
    serverSocket.listen(5)
    print('The server is ready to receive')

    count = 0
    while True:
        try:
            connectionSocket, clientAddress = serverSocket.accept()
            t = myThread(count, connectionSocket, clientAddress)
            #t.setDaemon(True)
            t.start()
            count += 1
        except:
            print('connection socket doesn\'t work')
            serverSocket.close()
    serverSocket.close()

if __name__ == '__main__':
    main()


