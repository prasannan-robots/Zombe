import socket,os,subprocess,sys,time
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

file_path_to_read_and_write = os.path.abspath("data.DAT")
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
    return arr[0],arr[1]

try:
    os.rmdir("temp")
except:
    pass
    
host,recv_password = data_loader()
key = RSA.generate(1024)
private_key = key.export_key()
file_out = open("temp/private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("temp/receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

# Creates socket
def create_socket():
    s = socket.socket()
    s.connect((host, port))
    security(s)

# Encrypts content and send it
# Send data length and data
def sender(conn,data):
    encrypted_data = rsa.encrypt(data.encode(),public_key_server)
    encrypted_data_len = str(sys.getsizeof(encrypted_data.decode()))
    encrypted_data_len = rsa.encrypt(encrypted_data_len.encode(),public_key_server)
    conn.send(encrypted_data_len)
    time.sleep(0.1)
    conn.send(encrypted_data)

# Receives data and decrypt it
# Receive data length and data
def receiver(conn):
    data_len = conn.recv(10200)
    data_len = int(rsa.decrypt(data_len,private_key).decode())
    data = conn.recv(data_len)
    data = rsa.decrypt(data,private_key).decode()
    del data_len
    return data


# Process data and send the result to the server
# input s
def deptor(s):
    print("Starting ...")
    while True:
        data = input()
        if data == "stats":
            print("Private_key: ",private_key)
            print("Public_key: ",public_key)
            print("Server's_public_key: ", public_key_server)
            print("Server ip : ", host)

        if len(data) > 0:
            sender(s,data)
            print(receiver(s),end="")

# Security check for authentication
def security(s):
    sender(s,public_key)
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