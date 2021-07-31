# Code written by prasanna
import socket
import os
import subprocess
import sys
import time
from cryptography.fernet import Fernet
file_path_to_read_and_write = os.path.abspath(".0903e3ddsda334d3.dasd234342.;sfaf'afafaf[a]]fasd.one")
port = 1026

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
    return arr[0],arr[1],arr[2],arr[3]
send_password,recv_password,key,host = data_loader()
# Creates socket
def create_socket():
    s = socket.socket()
    s.connect((host, port))
    security(s)

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


# Process data and send the result to the server
# input s
def deptor(s):
    print("Starting ...")
    while True:
        data = input(">")
        if len(data) > 0:
            sender(s,data)
            print(receiver(s))

# Security check for authentication
def security(s):
    sender(s,send_password)
    rec = receiver(s)
    if rec == recv_password:
        deptor(s)
    else:
        s.close()
        del s
        create_socket()
while True:
    try:
        create_socket()
    except Exception as msf:
        print(msf)