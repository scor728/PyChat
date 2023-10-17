# This Contains Client related functionality
import socket

import threading

serverAddress = "localhost"

def run(clientSocket):
    try:

        threading.Thread(target = send_message, args = (clientSocket,)).start()
        threading.Thread(target = rec_message, args = (clientSocket,)).start()
    except:
        clientSocket.close()

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
        print("Partner: " + m.recv(1024).decode())

def register():
    sock = connect()
    username = input("Enter a Username: ")
    # sock.send("NAME: " + username)
    password = input("Enter a Password: ")
    run(sock)

def login():
    sock = connect()
    username1 = input("Username: ")
    password2 = input("Password: ")
    run(sock)

print("Welcoming to the Encrypted Messaging Service!")

operation = input("I would like to Register (1) or Login (2):")

if operation == "1":
    register()
elif operation == "2":
    login()
else:
    exit()







