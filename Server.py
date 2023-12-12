import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys

maxPacketSize = 1024
defaultPort = 46960 #TODO: Set this to your preferred port (defaultPort - 46960)
exitSignal = True

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port", i)
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i))
                potentialPort.close()
                print("Server listening on port", i)
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port", i, "already in use. Checking next...")
                else:
                    print("An exotic error occurred:", e)

def GetServerData() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase()


def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    count91 = 0
    sum91 = 0
    count92 = 0
    sum92 = 0
    count93 = 0
    sum93 = 0

    print("tcp server listening...")

    while True:
        dataClient = tcpSocket.recv(1024)
        if not dataClient:
            continue
        msgClient = "Message from client: {}".format(dataClient)
        print(msgClient)
        payloads = GetServerData()

        for payload in payloads:
            if "Traffic Sensor 91" in payload.keys():
                count91 += 1
                sum91 += payload.get("Traffic Sensor 91")
            elif "Traffic Sensor 92" in payload.keys():
                count92 += 1
                sum92 += payload.get("Traffic Sensor 92")
            elif "Traffic Sensor 93" in payload.keys():
                count93 += 1
                sum93 += payload.get("Traffic Sensor 93")
        avg91 = sum91/count91
        avg92 = sum92/count92
        avg93 = sum93/count93

        fasthwy = min(avg91, avg92, avg93)
        print(fasthw)
        print(avg91, avg92, avg93)

        message2Client = ""

        if fasthwy == avg91:
            message2Client = "The fastest is Freeway 91"
        if fasthwy == avg92:
            message2Client = "The fastest is  Freeway 92"
        if fasthwy == avg93:
            message2Client = "The fastest is Freeway 93"

        bytes2send = str.encode(message2Client)
        tcpSocket.sendall(bytes2send)
    #pass; #TODO: Implement TCP Code, use GetServerData to query the database.

def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpPort = defaultPort
    print("TCP Port:", tcpPort)
    tcpSocket.bind(('localhost', tcpPort))
    return tcpSocket

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket()
    tcpSocket.listen(5)
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept()
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress])
        connectionThread.start()

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads)
    tcpThread.start()

    while not exitSignal:
        time.sleep(1)
    print("Ending program by exit signal...")
