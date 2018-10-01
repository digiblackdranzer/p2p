import socket
import pickle
import random


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8080
# client.bind(('',port))
# client.listen(5)
peers = []
listOfSeeds = []
servercom = socket.socket()

servercom.connect(('sl2-27.cse.iitb.ac.in',port))
print(servercom.recv(1024).decode())
choice = 2
servercom.send(str(choice).encode())


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
		for newpeer in peersOfPeer :
			if not(newpeer in peers) :
				peers.append(newpeer)
		servercom.close()
	except ConnectionRefusedError:
		print("Peer ",peer," is offline")

peers.remove()
if len(peers) > 4 :
	peerind = random.sample(range(len(peers)),4)
	newpeers = []
	for i in peerind :
		newpeers.append(peers[i])
	peers = newpeers


print("Chosen Peers for this Client are : ",peers)
peercon = []
for peer in peers :
	try :
		servercom = socket.socket()
		servercom.connect((peer,port))
		peercon.append(servercom)
	except ConnectionRefusedError :
		print("Peer ",peer," is offline")	




