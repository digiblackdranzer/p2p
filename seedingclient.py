import socket
import pickle
import threading

def request(client,addr,peers):

	
	client.send(pickle.dumps(peers))
	client.send(("Terminating Connection\n").encode())
	client.close()
	

if __name__ == '__main__':
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 8080
	peers = []
	listOfSeeds = []
	threads = []
	servercom = socket.socket()
	servercom.connect(('sl2-27.cse.iitb.ac.in',8080))
	print(servercom.recv(1024).decode())
	choice = 1
	servercom.send(str(choice).encode())

	peers = pickle.loads(servercom.recv(1024))
	print('Peers are loaded')

	peerClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	peerClient.bind(('',port))
	peerClient.listen(5)
	for i in range(20):
		threads.append(None)
	while True:
		b = True
		client,addr = peerClient.accept()
		for i in range(20) : 
			if threads[i] == None :
				threads[i] = threading.Thread(target=request,args=(client,addr,peers))
				threads[i].start()
				b = False
				if not(addr[0] in peers) :
					peers.append(addr[0])
				break

		if b :
			client.send(("Peer is busy , unable to handle any request currently\n").encode())	

	
