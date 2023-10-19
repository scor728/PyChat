# This Contains Client related functionality
import socket

import threading

serverAddress = "localhost"
stop = False

def run(clientSocket):
    try:
        sending_thread =threading.Thread(target = send_message, args = (clientSocket,))
        
        receiving_thread = threading.Thread(target = rec_message, args = (clientSocket,))
        sending_thread.start()
        receiving_thread.start()

        sending_thread.join()
        receiving_thread.join()
    except KeyboardInterrupt:
        stop = True
        clientSocket.close()
        exit()

def connect():
    
    print("Connecting to Server...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverAddress, 1234))
    print("Connected to Server " + serverAddress + " on port " + "1234")
    return client


def send_message(m):
    while not stop:
        message = input("")
        m.send(message.encode())
        
        print("You: " + message)

def rec_message(m):
    while not stop:
        print(m.recv(1024).decode())

def register():
    sock = connect()
    sock.send(("R").encode())

    while True:
        username = input("Enter a Username: ")
        sock.send(("NAME: " + username).encode())

        valid = sock.recv(1024).decode()

        if valid == "V":
            break
        else:
            print("User already exists with this Username!")


    password = input("Enter a Password: ")
    sock.send(("PASSWORD: " + password).encode())

    receiver = input("Partner Username: ")
    sock.send(("RECEIVER: " + receiver).encode())

    run(sock)

def login():
    sock = connect()
    sock.send(("L").encode())

    logged_in = False
    while not logged_in:
        username1 = input("Username: ")
        sock.send(("NAME: " + username1).encode())
        password2 = input("Password: ")
        sock.send(("PASSWORD: " + password2).encode())
        valid = sock.recv(1024).decode()
        if valid == "I":
            print("Username and Password Do not Match!\nEnter them Again:")
        elif valid == 
        else:
            logged_in = True
        

    receiver = input("Partner Username: ")
    sock.send(("RECEIVER: " + receiver).encode())
    run(sock)

print("Welcoming to the Encrypted Messaging Service!")

operation = input("I would like to Register (1) or Login (2):")

if operation == "1":
    register()
elif operation == "2":
    login()
else:
    exit()