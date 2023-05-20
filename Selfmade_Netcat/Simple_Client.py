import socket

ip = '127.0.0.1'
port = 9998

data = b"Test Data"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip,port))

client.send(data)

response = client.recv(4096)

print(response.decode('utf-8'))

client.close()