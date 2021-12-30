import socket,os,subprocess,sys,time,shutil,json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

file_path_to_read_and_write = os.path.abspath("data.DAT")
port = 1026

# rsa class to encrypt and decrypt data
class rsa:

    # To encrypt and decrypt using rsa opencryptdome
    # Uses a file to save the incoming data and opening it and decrypting it
    # All public_key of the clients are stored in file with unique no 
    def encrypt(data,public_key):
        result_array = [] # To store results in this array
        key_file = open(public_key)
        recipient_key = RSA.import_key(key_file.read())
        key_file.close()
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        result_array = [ x for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
        return result_array

    def decrypt(cipher):
        private_key = RSA.import_key("./temp/private.pem".read())

        enc_session_key, nonce, tag, ciphertext = cipher

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode()

# Encrypts content and send it
# Send data length and data
def sender(client_object,data):
    key_path = "receiver.pem"
    encrypted_data = rsa.encrypt(data.encode(),key_path) # Getting encrypted array from encrypt func
    for i in encrypted_data:
        print(sys.getsizeof(i))
        client_object.send(str(sys.getsizeof(i)).encode())
        time.sleep(0.2)
        client_object.send(i)
        time.sleep(0.5)


# Receives data and decrypt it
# Receive data length and data
def receiver(conn):
    result_array = []
    for i in range(4):
        data_len = conn.recv(10200)
        data_len = int(data_len.decode())
        data = conn.recv(data_len)
        result_array.append(data)
    data = rsa.decrypt(result_array).decode()
    return data


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

def change_key():
    try:
        shutil.rmtree("temp")
    except:
        pass
    os.mkdir("temp")
    key = RSA.generate(2048)
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
    key_file = open("temp/receiver.pem")
    public_key = key_file.read()
    key_file.close()
    sender(s,public_key)
    #rec = receiver(s)
    #print(rec)
    #rec = recv_password
    #if rec == recv_password:
    deptor(s)
    #else:
     #   s.close()
     #   del s
     #   create_socket()

# Start of the program
change_key()
host,recv_password = data_loader()
while True:
    try:
        create_socket()
    except Exception as msf:
        print(msf)