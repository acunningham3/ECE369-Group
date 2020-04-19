# TCP Client (simple echo code in Python)

# Import socket module and system module
import socket
import sys

from PyQt5.QtCore import QThread


class Client(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('localhost', 8001))
        print("connected to localhost at port 8001")
        

    def send_drawing(self, data):
        """
        x0, y0 are first point of line to draw
        x1, y1 are second point
        """
        # for i in data:
        #     try:
        #         self.sendall(bytes(i))
        #     except ValueError:
        #         pass
        # self.connect(('localhost', 8001))

        print(data)
        packet = '[' + str(data) + ']'
        encoded_data = packet.encode()
        print(encoded_data)
        self.sendall(encoded_data)
        
        # need to receive reply from server

    def send_text(self, text):
        print(text)
        packet = '[' + text + ']'
        encoded_text = packet.encode()
        print(encoded_text)
        self.sendall(encoded_text)


class ClientThread(QThread):

    def __init__(self):
        super().__init__()

    def run(self):
        # if len(sys.argv) <= 2:
        #     print('Usage: "python TCPclient.py server_address server_port"')
        #     print('server_address = Visible Inside: "eng-svr-1" or 2 or "localhost" or "127.0.0.1"')
        #     print('                 Visible Outside: IP address or fully qualified doman name')
        #     print('server_port = server welcome socket port: #80GX')
        #     sys.exit(2)

        # Create a TCP client socket: (AF_INET for IPv4 protocols, SOCK_STREAM for TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Request a TCP connection to the TCP server welcome socket: host = argv[1] & port = argv[2]
        # clientSocket.connect((sys.argv[1], int(sys.argv[2])))
        clientSocket.connect(('localhost', 8001))

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

    
