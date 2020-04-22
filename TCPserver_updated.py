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
client_list = []

def client_connect(accept_tuple):
    #s.accept() returns a tuple
    connection_socket = accept_tuple[0]
    global client_list
    client_list.append(connection_socket)
    print(client_list)
    address = accept_tuple[1]
    with connection_socket:
        while True:
            try:
                message = connection_socket.recv(1024)
                print(message)
                # if message.decode('utf-8') == "shutdown":
                    
                if not message or message.decode('utf-8') == "shutdown":
                    global running
                    running = False
                    client_list.remove(connection_socket)
                    connection_socket.close()
                    break
                for client in client_list:
                    if client != connection_socket:
                        client.sendall(message)
            except (ConnectionResetError, OSError):
                print("client disconnected")
                connection_socket.close()
                running = False
                break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Server runs on {HOST} at {socket.gethostbyname(HOST)}, port {PORT}")
        s.bind((HOST, PORT))
        
        while running:
            s.listen(5)
            client_thread = threading.Thread(target=client_connect, args=(s.accept(),))
            client_thread.start()
            # print(running)
        s.shutdown(socket.SHUT_RDWR)
        s.close()

if __name__ == "__main__":
    main()
