import socket
import pickle

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8080
# client.bind(('',port))
# client.listen(5)
# seedNodes = []
servercom = socket.socket()

servercom.connect(('sl2-27.cse.iitb.ac.in',8080))
print(servercom.recv(1024).decode())
choice = int(input())
servercom.send(str(choice).encode())

if choice == 1 :
	print(servercom.recv(1024).decode())
else :
	listOfSeeds = pickle.loads(servercom.recv(1024))
	print("List of Seed Node : ",listOfSeeds)	
	print(servercom.recv(1024).decode())
print(servercom.recv(1024).decode())
servercom.close()
	
