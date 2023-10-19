# This Contains Server related functionality
import socket

import threading


class Client:
  def __init__(self, username, socket, password, receiver_name):
    self.username = username
    self.socket = socket
    self.password = password
    self.receiver_name = receiver_name

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
            rname = getattr(client, "receiver_name")

            message = uname + ": " + socket.recv(1024).decode()

            if not message:
                remove_client(client)
                break

            for client1 in clients:
                if getattr(client1, "username") == rname and getattr(client1, "receiver_name") == uname:
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

        valid = False

        while valid == False:
            cname = client_socket.recv(1024).decode().split('NAME: ')[1]
            print(cname)

            found = False
            for client in clients:
                if getattr(client, "username") == cname:
                    found = True
                    break

            if found == False:
                valid = True
            else:
                client_socket.send(("I").encode())

        client_socket.send(("V").encode())
        
        password = client_socket.recv(1024).decode().split('PASSWORD: ')[1]
        print(password)

        rname = client_socket.recv(1024).decode().split('RECEIVER: ')[1]
        print(rname)

        client = Client(cname, client_socket, password, rname)
        return client
    
    elif operation == "L":
        print("login")

        cname = client_socket.recv(1024).decode().split('NAME: ')[1]
        print(cname)
        password = client_socket.recv(1024).decode().split('PASSWORD: ')[1]
        print(password)

        rname = client_socket.recv(1024).decode().split('RECEIVER: ')[1]
        print(rname)

        client = Client(cname, client_socket, password, rname)
        return client
    else:
        exit()
    
while True:
    client_socket, _ = server.accept()
    client = setup_client(client_socket)
    clients.append(client)
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

