import socket 
from threading import *
id = 1

ip = "127.0.0.1"
port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))

print("Listening on {}:{}".format(ip, str(port)))
while 1:
    server.listen()
    clientsocket, address = server.accept()
    connected = True
    
    print("Got a connection from:" + str(address))
    clientsocket.send(b"Welcome to the Server!\nYou can enter ? for help!")
    while connected:
        msg = clientsocket.recv(1024).decode()
        if msg == "?":
            clientsocket.send(b"Test\nexit")
        elif msg == "Test":
            clientsocket.send("This is a test!".encode())
        elif msg == "exit":
            clientsocket.send("Bye!".encode())
            clientsocket.close()
            connected = False
        else:
            msg = "Your msg: " + msg
            msg = msg.encode()
            clientsocket.send(msg)