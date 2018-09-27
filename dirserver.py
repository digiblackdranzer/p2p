import socket
import pickle
import threading

def request(client,addr,seedNodes):

	client.send(("Hello "+str(addr)+" - Welcome to D-Torrent\nHere's list of Commands : \n1 - Register Yourself as Seed\n2 - Retrieve list of available Seed Nodes\n").encode())
	choice = int(client.recv(1024).decode())
	if choice == 1 :
		seedNodes.append(addr)
		client.send(pickle.dumps("Added as Seed Node Successfully\n"))#client.send(("Added as Seed Node Successfully\n").encode())
		client.send(pickle.dumps(seedNodes))
	else :
		client.send(pickle.dumps(seedNodes))
		client.send(("Available Seed Nodes Sent Successfully\n").encode())
	
	client.send(("Terminating Connection\n").encode())
	client.close()


if __name__ == '__main__':

	dirserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 8080
	dirserver.bind(('',port))
	dirserver.listen(5)
	seedNodes = []
	threads = []
	for i in range(20):
		threads.append(None)
	while True:
		b = True
		client,addr = dirserver.accept()
		for i in range(20) : 
			if threads[i] == None :
				threads[i] = threading.Thread(target=request,args=(client,addr,seedNodes))
				threads[i].start()
				b = False
				break

		if b :
			client.send(("Server is busy , unable to handle any request currently\n").encode())

	