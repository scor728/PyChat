# This Contains Server related functionality
import socket

import threading


class Client:
  def __init__(self, username, socket, password):
    self.username = username
    self.socket = socket
    self.password = password

serverAddress = "localhost"

print("Starting Server...")
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverAddress, 1234))
print("Server started on " + serverAddress + " on port " + "1234")
server.listen()

clients = []

#Client Object
#Usernames
#Socket

def handle_client(client):
    while True:
        try:
            socket = getattr(client, "socket")
            uname = getattr(client, "username")

            message = uname + ": " + socket.recv(1024).decode()

            if not message:
                remove_client(client)
                break

            for client1 in clients:
                if client1 != client:
                    socket1 = getattr(client1, "socket")
                    socket1.send((message).encode())
        except:
            remove_client(client_socket)
            break

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.socket.close()

def setup_client(client_socket):
    print("setup client")
    operation  = client_socket.recv(1024).decode()
    if operation == "R":
        print("register")
    elif operation == "L":
        print("login")
    else:
        exit()

    cname = client_socket.recv(1024).decode().split('NAME: ')[1]
    print(cname)
    password = client_socket.recv(1024).decode().split('PASSWORD: ')[1]
    print(password)

    client = Client(cname, client_socket, password)
    return client
    

while True:
    client_socket, _ = server.accept()
    client = setup_client(client_socket)
    clients.append(client)
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

