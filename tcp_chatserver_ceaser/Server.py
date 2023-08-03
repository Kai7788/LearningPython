import socket
import threading
import sys
ip = "127.0.0.1"
port = 8081

clients = []
nicknames = []


def handle_con(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            broadcast(message)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            nickname = nicknames[index]
            print("{} has left the Room!".format(nickname))
            nicknames.remove(nickname)
            break

def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))

def recv_con():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip,port))
        server.listen()
    except:
        print("Could not bind to Address {}:{}".format(ip, str(port)))
        sys.exit(1)       
    
    print("Server is listening on {}:{}...".format(ip, str(port)))
    while True:
        client_socket, address = server.accept()
        print("Got a connection from {}".format(str(address)))
        client_socket.send("Nickname>".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        
        nicknames.append(nickname)
        clients.append(client_socket)
        
        broadcast("{} has joined the Room!".format(nickname))
        client_socket.send("Connected to the Server!".encode("utf-8"))
        
        thread = threading.Thread(target=handle_con, args=(client_socket,))
        thread.start()
        
print("Starting Server....")
recv_con()
        
        