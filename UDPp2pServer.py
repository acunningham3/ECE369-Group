import socket
import select
import sys

IP = "127.0.0.1"
PORT = 1234

running = 1

# Creating a UDP server socket: (AF_INET for IPv4 protocols, SOCK_DGRAM for UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print ("Server runs on", IP, "at ", PORT)

server_socket.bind((IP, PORT))

# List of sockets for select.select()
client_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}


while running:
	print ("UDP Server is waiting on port ", PORT, "........")

	#read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
	new_client = False

	# Receive a message from the client
	# Adds client to list and checks if new client
	message, clientAddress =  server_socket.recvfrom(1024)

	message = message.decode('utf-8')

	client_list.append(clientAddress)

	num = client_list.count(clientAddress)
	if num > 1:
		client_list.remove(clientAddress)
	else:
		clients[clientAddress]=message
		new_client = True
		print("New connection from:", message, "Address:", clientAddress)

	# If not new client it passes the message to all other clients in list besides sender
	if new_client is True:
		continue
	else:
		if message == 'shutdown server':
			message = 'UDP server is now shutting down.....'
			
			message = message.encode('utf-8')

			for C_A in client_list:
				server_socket.sendto(message, C_A)
			running = 0

		else:
			print("Message from:", clientAddress, ":", message)
			message = message.encode('utf-8')

			#print(clientAddress)
			#server_socket.sendto(message, clientAddress)

			for C_A in client_list:
				
				#print(C_A)
				server_socket.sendto(message, C_A)

print ("UDP Server shuts down!")
server_socket.close()	
sys.exit(0)



    
