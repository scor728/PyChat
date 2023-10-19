# This Contains Client related functionality
import socket

import threading

serverAddress = "localhost"

def run(clientSocket):
    try:

        threading.Thread(target = send_message, args = (clientSocket,)).start()
        threading.Thread(target = rec_message, args = (clientSocket,)).start()
    except KeyboardInterrupt:
        clientSocket.close()
        exit()

def connect():
    
    print("Connecting to Server...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverAddress, 1234))
    print("Connected to Server " + serverAddress + " on port " + "1234")
    return client


def send_message(m):
    while True:
        message = input("")
        m.send(message.encode())
        
        print("You: " + message)

def rec_message(m):
    while True:
        print(m.recv(1024).decode())

def register():
    sock = connect()
    sock.send(("R").encode())
    username = input("Enter a Username: ")
    sock.send(("NAME: " + username).encode())
    password = input("Enter a Password: ")
    sock.send(("PASSWORD: " + password).encode())

    receiver = input("Partner Username: ")
    sock.send(("RECEIVER: " + receiver).encode())

    run(sock)

def login():
    sock = connect()
    sock.send(("L").encode())
    username1 = input("Username: ")
    sock.send(("NAME: " + username1).encode())
    password2 = input("Password: ")
    sock.send(("PASSWORD: " + password2).encode())
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