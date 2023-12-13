import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 46960 # TODO: Change this to your expected port (defaultPort - 46960)
serverIP = 'localhost' #TODO: Change this to your instance IP (serverIP - `***.***.***.***`) (serverIP - `127.0.0.1`)

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcpPort = int(input("Please enter the TCP port of the host..."))
except:
    tcpPort = 0
if tcpPort == 0:
    tcpPort = defaultPort
tcpSocket.connect((serverIP, tcpPort))

clientMessage = ""
while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>")

    #TODO: Send the message to your server
    tcpSocket.send(clientMessage.encode())

    #TODO: Receive a reply from the server for the best highway to take
    response = tcpSocket.recv(1024).decode()

    #TODO: Print the best highway to take
    print(f"Message from Server {response}")

tcpSocket.close()

