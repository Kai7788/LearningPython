import socket
import sys
import threading

ip = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip,port))
nickname = input("Please enter your nickname!\n")

def recive():
    nick_counter = 0
    while True:
        try:
            message = s.recv(1024).decode("utf-8")
            if message == "Nickname>" and nick_counter == 0:
                s.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print("Connection Closed!")
            s.close()
            break
    
def write():
    while True:
        message = "{}: {}".format(nickname, input(">"))
        s.send(message.encode("utf-8"))
            
            
            
recieve_thread = threading.Thread(target=recive)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()