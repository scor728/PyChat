# This Contains Client related functionality
import socket
import sys

import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
# import curses
# from curses import wrapper

print(private_key)

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
        exit()
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

def encryption(socket):
    print("Encrypting")
    socket.send(public_key.save_pkcs1("PEM"))
    global serverKey
    serverKey = rsa.PublicKey.load_pkcs1(socket.recv(1024))

def send_message(m):
    global stop
    while not stop:
        try: 

            print(">> ", end = "")
            message = input("")
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            
            if message == "EXIT":
                stop = True
                m.close()
                exit()
            
            m.send(rsa.encrypt(message.encode(), serverKey))
            # remove_line()
            print(CURSOR_UP_ONE + ERASE_LINE)
            # remove_line()
            print("You: " + message)
            
        except Exception:
            break

def welcome(rname):
    print("\n\n---------------------------------")
    print("Now Chatting with " + rname)
    print("---------------------------------")
    print("Type EXIT to exit the chat\n")

def remove_line():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

def rec_message(m):
    global stop
    while not stop:
        try:
            message = rsa.decrypt(m.recv(1024), private_key).decode()
            if not message:
                break
            else:
                remove_line()
                print("\n" + message)
                # print(">> ")
                print(">> ", end = "\r\033[3C")
                # print("\033[3C")
                # print('\x1b[1A')
               
        except Exception:
            break

def register():
    sock = connect()
    encryption(sock)
    sock.send(rsa.encrypt(("R").encode(), serverKey))

    while True:
        username = input("Enter a Username: ")
        sock.send(rsa.encrypt(("NAME: " + username).encode(), serverKey))

        valid = rsa.decrypt(sock.recv(1024), private_key).decode()

        if valid == "V":
            break
        else:
            print("User already exists with this Username!")


    password = input("Enter a Password: ")
    
    sock.send(rsa.encrypt(("PASSWORD: " + password).encode(), serverKey))

    receiver = input("Partner Username: ")
    sock.send(rsa.encrypt(("RECEIVER: " + receiver).encode(), serverKey))
    welcome(receiver)

    run(sock)

def login():
    sock = connect()
    encryption(sock)
    sock.send(rsa.encrypt(("L").encode(), serverKey))

    logged_in = False
    while not logged_in:
        username1 = input("Username: ")
        sock.send(rsa.encrypt(("NAME: " + username1).encode(), serverKey))
        password2 = input("Password: ")

        sock.send(rsa.encrypt(("PASSWORD: " + password2).encode(), serverKey))
        valid = rsa.decrypt(sock.recv(1024), private_key).decode()
        if valid == "I":
            print("Username and Password Do not Match!\nEnter them Again:")
        
        else:
            logged_in = True
        
    receiver = input("Partner Username: ")
    sock.send(rsa.encrypt(("RECEIVER: " + receiver).encode(), serverKey))

    welcome(receiver)

    run(sock)

print("Welcoming to the Encrypted Messaging Service!")

operation = input("I would like to Register (1) or Login (2):")

if operation == "1":
    register()
elif operation == "2":
    login()
else:
    exit()