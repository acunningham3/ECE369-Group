import socket
import select
import time
import sys


IP = "127.0.0.1"
PORT = 1234

# Create a UDP client socket: (AF_INET for IPv4 protocols, SOCK_DGRAM for UDP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Receive the server response function
def recve_data():
    recve_message, serverAddress = client_socket.recvfrom(1024)
    recve_message = recve_message.decode('utf-8')
    print(recve_message)


username = input("Username: ")
# Need to encode username to bytes before sending 
username = username.encode('utf-8')

client_socket.sendto(username, (IP, PORT))

#Decode username
username = username.decode('utf-8')
username = username +">"

while True:
    #Set timeout and start time
    timeout = 2
    timeout_start = time.time()
    #Input timer 
    while time.time() < timeout_start + timeout:   
        message = input(username)
    
    try:
        #Checking if user entered data and sending if true
        if message == username:
            message = None

        if message:
            
            #if user disconnects 
            if message == 'quit' or message == 'shutdown':
                print(username + "quits!")
                message = username + "quits!"
                message = message.encode('utf-8')
                client_socket.sendto(message , (IP, PORT))
                break
            if message == 'shutdown server':
                print("Server is shutting off")
            
            message = message.encode('utf-8')
            client_socket.sendto(message , (IP, PORT))
            recve_data()

        else:
            recve_data()

    except:
        # Server doesn't respond
        print("Time out! message is lost :( ")

client_socket.close()
sys.exit(0)