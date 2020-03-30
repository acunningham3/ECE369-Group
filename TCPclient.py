# TCP Client (simple echo code in Python)

# Import socket module and system module
import socket
import sys

if len(sys.argv) <= 2:
	print('Usage: "python TCPclient.py server_address server_port"')
	print('server_address = Visible Inside: "eng-svr-1" or 2 or "localhost" or "127.0.0.1"')
	print('                 Visible Outside: IP address or fully qualified doman name')
	print('server_port = server welcome socket port: #80GX')
	sys.exit(2)

# Create a TCP client socket: (AF_INET for IPv4 protocols, SOCK_STREAM for TCP)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Request a TCP connection to the TCP server welcome socket: host = argv[1] & port = argv[2]
clientSocket.connect((sys.argv[1], int(sys.argv[2])))

# Client takes message from user input, sends it to the server, and receives its echo
print('Type "quit" to exit the client or "shutdown" to turnoff the server')
while True:
	message = input("Type a message: ")
	msg_byte = message.encode()
	print(message)
	clientSocket.send(msg_byte)
	modifiedMessage = clientSocket.recv(1024)
	print('Received echo:', modifiedMessage)
	if message == 'quit' or message == 'shutdown' or message == "":
		print('TCP Client quits!')
		break

# Close the client socket
clientSocket.close()
sys.exit(0)
