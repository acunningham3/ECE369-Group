# TCP Server Multithread (simple echo multithread code in Python)
# run on "eng-svr-2" x-term ssh at 134.88.53.55

# Import socket, system, & thread modules
import socket
import sys
import threading

global running

HOST = '127.0.0.1'
PORT = 8001

running = True

def client_connect(accept_tuple):
    #s.accept() returns a tuple
    connection_socket = accept_tuple[0]
    address = accept_tuple[1]
    with connection_socket:
        while True:
            message = connection_socket.recv(1024)
            print(message)
            # if message.decode('utf-8') == "shutdown":
                
            if not message or message.decode('utf-8') == "shutdown":
                global running
                running = False
                break
            connection_socket.sendall(message)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server runs on", HOST, "at", socket.gethostbyname(HOST))
        s.bind((HOST, PORT))
        
        while running:
            s.listen(5)
            client_thread = threading.Thread(target=client_connect, args=(s.accept(),))
            client_thread.start()
            # print(running)

if __name__ == "__main__":
    main()
