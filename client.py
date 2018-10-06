import socket
import pickle
import random
import threading
import time
import datetime
import hashlib

def logit(message):
	logger = open(myip+"_logs.txt","a")
	logger.write(message+"\n")
	logger.close()

# Utilities

def getHashes():
	return hashes

# Flooding Logic

def flood(peercons,client):
	
	while True :
		messages = client.recv(1024).decode()
		if len(messages) > 0 :
			print("Message Received : ",messages)
		sha1hash = hashlib.sha1()
		hashes = getHashes()
		sha1hash.update(messages.encode())
		msghash = sha1hash.hexdigest()
		if not(msghash in hashes) :
			logit(messages)
			print(messages)
			hashes.append(msghash)
			for peercon in peercons :
				try :
					peercon.send(messages.encode())
				except ConnectionRefusedError :
					print("Peer ",peer," is offline")	
			

def request(peercons):

	mycli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 8080
	mycli.bind(('',port))
	mycli.listen(5)
	seedNodes = []
	threads = []
	for i in range(20):
		threads.append(None)
	while True:
		b = True
		client,addr = mycli.accept()
		for i in range(20) : 
			if threads[i] == None :
				threads[i] = threading.Thread(target=flood,args=(peercons,client))
				threads[i].start()
				b = False
				break

		if b :
			client.send(("Peer is busy , unable to handle any request currently\n").encode())	



###################################################

# Initialization

port = 8080
peers = []
listOfSeeds = []
servercom = socket.socket()

###################################################

# Retrieval of Seed Nodes from Dedicated Directory Server

servercom.connect(('sl2-27.cse.iitb.ac.in',port))
response = servercom.recv(1024).decode()
myip = response.split(' ')[1]
print(response)
choice = 2
servercom.send(str(choice).encode())
peers = pickle.loads(servercom.recv(1024))
print("List of Seed Nodes : ",peers[:3])	
print(servercom.recv(1024).decode())
servercom.close()

##################################################

# Retrieval of Peers from Seed Nodes

for peer in peers[:3] :
	try :
		print("Peer : ",peer)
		servercom = socket.socket()
		servercom.connect((peer,8081))	
		peersOfPeer = pickle.loads(servercom.recv(1024))
		print("List of Peers from ",peer," : ",peersOfPeer)
		for newpeer in peersOfPeer :
			if not(newpeer in peers) :
				peers.append(newpeer)
		servercom.close()
	except ConnectionRefusedError:
		print("Peer ",peer," is offline")

################################################

# Establish Connections with Peers

if len(peers) > 4 :
	peerind = random.sample(range(len(peers)),4)
	newpeers = []
	for i in peerind :
		newpeers.append(peers[i])
	peers = newpeers


print("Chosen Peers for this Client are : ",peers)
peercons = []
if myip in peers :
	peers.remove(myip)
for peer in peers :
	try :
		servercom = socket.socket()
		servercom.connect((peer,port))
		peercons.append(servercom)
	except ConnectionRefusedError :
		print("Peer ",peer," is offline")

###############################################

# Create 2 Flows - i) For Listening and flooding  ii) For generating messages
# For this we use 1 thread

listenClient = threading.Thread(target=request,args=(peercons,))
listenClient.start()
hashes = []
while True :
	time.sleep(5)
	message  = str(datetime.datetime.now())+": "+myip+" pays "+str(random.randint(1,1000))+" BTC to "+peers[random.randint(0,len(peers)-1)]
	print("Generated Message : ",message)
	sha1hash = hashlib.sha1()
	sha1hash.update(message.encode())
	mhash = sha1hash.hexdigest()
	if mhash in hashes :
		continue
	logit(message)
	hashes.append(mhash)
	for peercon in peercons :
		try :
			peercon.send(message.encode())
		except ConnectionRefusedError :
			print("Peer ",peer," is offline")	






