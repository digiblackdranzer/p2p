import socket
import pickle

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8080
# client.bind(('',port))
# client.listen(5)
peers = []
listOfSeeds = []
servercom = socket.socket()

servercom.connect(('sl2-27.cse.iitb.ac.in',port))
print(servercom.recv(1024).decode())
choice = int(input())
servercom.send(str(choice).encode())

if choice == 1 :
	peers = pickle.loads(servercom.recv(1024))
	print('Peers are loaded')

else :
	peers = pickle.loads(servercom.recv(1024))
	print("List of Seed Nodes : ",peers)	
	
print(servercom.recv(1024).decode())
servercom.close()

for peer in peers[:3] :
	try :
		servercom = socket.socket()
		servercom.connect((peer,port))	
		peersOfPeer = pickle.loads(servercom.recv(1024))
		print("List of Peers from ",peer," : ",peersOfPeer)
	except ConnectionRefusedError:
		print("Peer ",peer," is offline")
