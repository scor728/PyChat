# This Contains Server related functionality
import socket

import threading

serverAddress = "localhost"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverAddress, 1234))
server.listen()

client, _ = server.accept()

def send(m):
    while True:
        message = input("")
        m.send(message.encode())
        print("You: " + message)

def rec(m):
    while True:
        print("Partner: " + m.recv(1024).decode())

threading.Thread(target = send, args = (client,)).start()
threading.Thread(target = rec, args = (client,)).start()