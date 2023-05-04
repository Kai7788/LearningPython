import socket
import sys
ip = "127.0.0.1"
port = 9999

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))
    print("Connected!")
    connected = True
    while connected:
        print(s.recv(1024).decode())
        msg = input(">")
        if msg == "exit":
            connected = False
        msg = msg.encode()
        s.send(msg)
    print("Disconnected!")
except:
    print("Could not Connect to Host")
    sys.exit(1)
        