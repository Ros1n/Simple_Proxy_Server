from socket import *
serverName = 'localhost'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
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