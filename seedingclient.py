import socket
import pickle
import threading
import hashlib
import time
import datetime
import random

def logit(message):
	logger = open(myip+"_logs.txt","a")
	logger.write(message)
	logger.close()

def peerupdate():
	while True :
		time.sleep(10)
		if len(peercons) == 4 :
			return


		if len(peercons) != len(peers) :
			try :
				servercom = socket.socket()
				servercom.connect((peers[len(peercons)],port))
				peercons.append(servercom)
			except ConnectionRefusedError :
				print("Peer ",peers[len(peercons)]," is offline")			

def getHashes():
	return hashes


def addPeer(addr):
	peers.append(addr)	

# Seed Logic
def seed(peers,client,addr):
	print("Peers in seed() : ",peers)
	addPeer(addr[0])
	client.send(pickle.dumps(peers))
	client.send(("Terminating Connection\n").encode())
	client.close()


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
			hashes.append(msghash)
			for peercon in peercons :
				try :
					peercon.send(messages.encode())
				except ConnectionRefusedError :
					print("Peer ",peer," is offline")	
		


def msgrequest(peercons):

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


def seedrequest(peers):

	mycli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	mycli.bind(('',8081))
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
				print("Argument to seed() : ",peers)
				threads[i] = threading.Thread(target=seed,args=(peers,client,addr))
				threads[i].start()
				b = False
				break

		if b :
			client.send(("Peer is busy , unable to handle any request currently\n").encode())
	

	
# Initialization

port = 8080
peers = []
listOfSeeds = []
servercom = socket.socket()

#################################

# Retrieve and register as seed node

servercom.connect(('sl2-27.cse.iitb.ac.in',port))
response = servercom.recv(1024).decode()
myip = response.split(' ')[1]
print(response)
choice = 1
servercom.send(str(choice).encode())
peers = pickle.loads(servercom.recv(1024))
print("List of Seed Nodes : ",peers[:3])	
print(servercom.recv(1024).decode())
servercom.close()	

##################################

# Establish Connection With peers

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

###################################

# Create 3 Flows : i) To act as seed server  ii) Message Generation iii) Flooding
print("Peercons : ",peercons)
print("Peers : ",peers)

listenClient = threading.Thread(target=msgrequest,args=(peercons,))
seedClient = threading.Thread(target=seedrequest,args=(peers,))
peerUpdateClient = threading.Thread(target=peerupdate)
listenClient.start()
seedClient.start()
peerUpdateClient.start()
hashes = []
while len(peers) < 1:
	pass
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