import platform
from socket import *

serverPort = 8001
clientSocket = socket(AF_INET, SOCK_STREAM)
serverName = platform.uname()[1]
clientSocket.connect((serverName,serverPort))
while True:
	sentence = input('Input lowercase sentence: ')
	if sentence == None or len(sentence) <= 1:
		print("cannot read from server")
	else:
		clientSocket.send(bytes(sentence,'utf-8'))
		modifiedSentence = clientSocket.recv(1024).decode("utf-8")
		print('From Server:', modifiedSentence)
clientSocket.close()