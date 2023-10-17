# This Contains Server related functionality
import socket

import threading


class Client:
  def __init__(self, username, socket):
    self.username = username
    self.socket = socket

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

def handle_client(client_socket):
    # cname = client_socket.recv(1024).decode().split('NAME: ')[1]
    

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                remove_client(client_socket)
                break

            for client in clients:
                if client != client_socket:
                    client.send((message).encode())
        except:
            remove_client(client_socket)
            break

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

while True:
    client, _ = server.accept()
    clients.append(client)
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

