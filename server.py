# This Contains Server related functionality
import socket

import threading


class Client:
  def __init__(self, username, socket, password, receiver_name, logged_in):
    self.username = username
    self.socket = socket
    self.password = password
    self.receiver_name = receiver_name
    logged_in = logged_in

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

            message_val = socket.recv(1024).decode()
            message = uname + ": " + message_val 

            if not message_val:
                remove_client(client)
                break

            for client1 in clients:
                if getattr(client1, "username") == rname and getattr(client1, "receiver_name") == uname:
                    socket1 = getattr(client1, "socket")
                    socket1.send((message).encode())
        except:

            remove_client(client_socket)
            break

def remove_client(client):
    if client in clients:
        getattr(client, "socket").close()

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

        client = Client(cname, client_socket, password, rname, True)
        clients.append(client)
        return client
    
    elif operation == "L":
        print("login")

        logged_in = False

        while logged_in == False:        
            cname = client_socket.recv(1024).decode().split('NAME: ')[1]
            # print(cname)
            password = client_socket.recv(1024).decode().split('PASSWORD: ')[1]
            # print(password)

            current_client = False

            for client in clients:
                if getattr(client, "username") == cname and getattr(client, "password") == password:
                    current_client = client
                    
            if current_client == False:
                client_socket.send(("I").encode())
            else:
                #Set Client Socket
                logged_in = True
                client_socket.send(("V").encode())

        print(password)

        rname = client_socket.recv(1024).decode().split('RECEIVER: ')[1]
        print(rname)
        #Set Client Message Receiver

        setattr(current_client, "socket", client_socket)
        setattr(current_client, "receiver_name", rname)

    
        return current_client
    else:
        exit()


print("About to enter loop")
# try:
#     while True:
#         print("Entered Loops")
#         client_socket, _ = server.accept()
#         client = setup_client(client_socket)
#         client_thread = threading.Thread(target=handle_client, args=(client,))
#         client_thread.start()
# except KeyboardInterrupt:
#     print("KBI")

# except Exception as e:
#     for client in clients:
#         sock = getattr(client, "socket")
#         sock.close()
#     exit()\


# Flag to indicate whether to continue the loop
running = True

def signal_handler(signal, frame):
    print("handling signal")
    global running
    print("Ctrl+C detected. Closing server and clients.")
    running = False
    for client in clients:
        sock = getattr(client, "socket")
        sock.close()
    server.close()
    exit()

# Register the Ctrl+C signal handler
import signal
signal.signal(signal.SIGINT, signal_handler)

import select
while running:
    sockets = [server]
        
    # Use select to wait for I/O activity with a timeout
    readable, _, _ = select.select(sockets, [], [], 0.25)
        
    if server in readable:
        client_socket, _ = server.accept()
        client = setup_client(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

    # print("Entered Loops")
    # client_socket, _ = server.accept()
    # print("Accepted")
    # client = setup_client(client_socket)
    # client_thread = threading.Thread(target=handle_client, args=(client,))
    # client_thread.start()

