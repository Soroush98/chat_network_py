import socket
import time
import random
import sys
from threading import *
def receive2(s):
    while True:
        try:
            data = s.recv(1024).decode("utf8")
        except ConnectionResetError:
            sys.exit()
        if (data == "exit"):
            return
        print("Got message "+data )

def receive(s):
    while True:
        try:
            data = s.recv(1024).decode("utf8")
        except ConnectionResetError:
            sys.exit()
        if (data == "exit"):
            return
        print("Got message "+data)

def tcp_recieve(port):


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        conn, addr = s.accept()
        print("Connected to user with ip "+addr[0]+" on port "+str(port))
        t1 = Thread(target = receive2,args=(conn,))
        t1.daemon = True
        t1.start()
        while True:
            data = input("Enter a message \n")
            if (data == "exit"):
                print("Closing connection")
                sys.exit()
            try:
                conn.send(bytes(data,'utf8'))
            except ConnectionResetError:
                sys.exit()
        conn.close()
        return
def tcp_send(address,data):
    temp = data.decode()
    port = int(temp)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((address[0], port))
    print("Connected to user with ip "+address[0]+" on port "+str(port))
    t1 = Thread(target = receive,args=(s,))
    t1.daemon = True
    t1.start()
    while True:
        data = input("Enter a message \n")
        if (data == "exit"):
            print("Closing connection")
            sys.exit()
        try:
            s.send(bytes(data,'utf8'))
        except ConnectionResetError:
            sys.exit()



    return
def udp_recieve():

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 37020))
    message = b"hello"
    state = 0
    client.settimeout(3)
    try:
        data, addr = client.recvfrom(1024)
        print("received message: %s"%data)
        if (data == message):
            state = -1
        time.sleep(1)
        client.close()
        return addr,state,data
    except socket.timeout:
        print("Time out , resending broadcast")
        state = -2
        client.close()
        return 0,state,0


def udp_send():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    server.bind(("", 44444))
    message = b"hello"
    server.sendto(message, ('<broadcast>', 37020))
    print("broadcast message sent!")
    time.sleep(1)
    server.close()
    return
def udp_send2(addr):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.settimeout(0.2)
    server.bind(("", 44444))
    port = random.randrange(5000,50000)
    message = str(port)
    server.sendto(message.encode(), (addr[0], 37020))
    print("port message sent!")
    time.sleep(1)
    server.close()
    return port
while True:
    udp_send()
    addr,state,data = udp_recieve()
    if (state != -2 ):
        break
if (state == -1):
    port = udp_send2(addr)
    tcp_recieve(port)
else:
    tcp_send(addr,data)


