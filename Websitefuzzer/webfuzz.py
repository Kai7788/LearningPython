from bs4 import BeautifulSoup
import socket

url = socket.gethostbyname("www.bkbocholt-west.eu")
port = 443

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((url,port))
s.send("GET / HTTP/1.1\n".encode("utf-8"))
print(s.recv(4096))

