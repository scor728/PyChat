# This Contains Server related functionality
import socket
import threading
import hashlib
import rsa
import signal
import select

public_key, private_key = rsa.newkeys(1024)

# Flag to indicate whether to continue the loop
running = True


class Client:
  def __init__(self, username, socket, password, receiver_name, logged_in, public_key):
    self.username = username
    self.socket = socket
    self.password = password
    self.receiver_name = receiver_name
    self.logged_in = logged_in
    self.public_key = public_key

serverAddress = "localhost"

def handle_client(client):
    while True:
        try:
            socket = getattr(client, "socket")
            uname = getattr(client, "username")
            rname = getattr(client, "receiver_name")
            clientkey = getattr(client, "public_key")

            message_val = rsa.decrypt(socket.recv(1024), private_key).decode()
            message = uname + ": " + message_val 

            if not message_val:
                remove_client(client)
                break

            for client1 in clients:
                if getattr(client1, "username") == rname and getattr(client1, "receiver_name") == uname:
                    socket1 = getattr(client1, "socket")
                    clientkey = getattr(client1, "public_key")
                    
                    socket1.send(rsa.encrypt((message).encode(), clientkey))
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        getattr(client, "socket").close()

def setup_client(client_socket):

    clientKey = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
    client_socket.send(public_key.save_pkcs1("PEM"))

    operation  = rsa.decrypt(client_socket.recv(1024), private_key).decode()
    if operation == "R":

        valid = False

        while valid == False:
            cname = rsa.decrypt(client_socket.recv(1024),private_key).decode().split('NAME: ')[1]

            found = False
            for client in clients:
                if getattr(client, "username") == cname:
                    found = True
                    break

            if found == False:
                valid = True
            else:
                client_socket.send(rsa.encrypt(("I").encode(), clientKey))

        client_socket.send(rsa.encrypt(("V").encode(), clientKey))
        
        password_input = rsa.decrypt(client_socket.recv(1024), private_key).decode().split('PASSWORD: ')[1]

        sha256 = hashlib.sha256()

        sha256.update(password_input.encode('utf-8'))
        password = sha256.hexdigest()



        rname = rsa.decrypt(client_socket.recv(1024), private_key).decode().split('RECEIVER: ')[1]


        client = Client(cname, client_socket, password, rname, True, clientKey)
        clients.append(client)
        return client
    
    elif operation == "L":

        logged_in = False

        while logged_in == False:        
            cname = rsa.decrypt(client_socket.recv(1024), private_key).decode().split('NAME: ')[1]
            
            supplied_password = rsa.decrypt(client_socket.recv(1024), private_key).decode().split('PASSWORD: ')[1]

            sha256 = hashlib.sha256()

            sha256.update(supplied_password.encode('utf-8'))
            password = sha256.hexdigest()

            current_client = False

            for client in clients:
                
                if getattr(client, "username") == cname and getattr(client, "password") == password:
                    current_client = client
                    
            if current_client == False:
                client_socket.send(rsa.encrypt(("I").encode(), clientKey))
            else:
                #Set Client Socket
                logged_in = True
                client_socket.send(rsa.encrypt(("V").encode(), clientKey))

        rname = rsa.decrypt(client_socket.recv(1024), private_key).decode().split('RECEIVER: ')[1]
        
        #Set Client Message Receiver
        setattr(current_client, "socket", client_socket)
        setattr(current_client, "receiver_name", rname)
        setattr(current_client, "public_key", clientKey)
    
        return current_client
    else:
        exit()

def signal_handler(signal, frame):
    global running

    print("Ctrl+C detected. Closing server and clients.")
    running = False
    for client in clients:
        sock = getattr(client, "socket")
        sock.close()
    server.close()
    exit()

# Register the Ctrl+C signal handler

signal.signal(signal.SIGINT, signal_handler)


def main():
    print("Starting Server...")
    global server, clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverAddress, 1234))

    print("Server Started on " + serverAddress + " on port " + "1234")
    server.listen()

    clients = []

    while running:
        sockets = [server]
            
        # Use select to wait for I/O activity with a timeout
        readable, _, _ = select.select(sockets, [], [], 0.25)
            
        if server in readable:
            client_socket, _ = server.accept()
            client = setup_client(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.start()

if __name__ == '__main__':
    main()