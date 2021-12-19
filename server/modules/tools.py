from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import sys,time,os,json


def data_loader(file_path_to_read_and_write):
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

# Just to create a single object instead of whole array :)
class clients:
    def __init__(self,connection,address,public_key=None,id=None):
        self.connection = connection # Stores the connection par of the clients
        self.address = address # Stores the ip address of the clients
        self.public_key = public_key # Stores the path of client's public key
        self.id = id # Stores object's id
    
    def save_public_key(self,key,id=None):
        if id == None:
            id = self.id

        file = open(f"./temp/{id}.pem").write(key)
        self.public_key = file.name
        file.close()
    
    def get_public_key(self):
        key = RSA.import_key(open(self.public_key).read())
        return key

    def delete_key_file(self):
        if os.path.exists(self.public_key):
            os.remove(self.public_key)



# To Manage encryption and decryption

class rsa:
    def __init__(self):
        pass

    # To encrypt and decrypt using rsa opencryptdome
    # Uses a file to save the incoming data and opening it and decrypting it
    # All public_key of the clients are stored in file with unique no 
    def encrypt(data,public_key):
        file_out = open("./temp/encrypted_data.bin", "wb")

        recipient_key = RSA.import_key(open("./temp/receiver.pem").read())
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
        file_out.close()
        return file_out.name

    def decrypt(cipher,private_key):
        file_in = open("./temp/encrypted_data.bin", "rb")

        private_key = RSA.import_key(open("./temp/private.pem").read())

        enc_session_key, nonce, tag, ciphertext = \
        [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode()
    
    # Encrypts content and send it
    # Send data length and data
    def sender(self,conn,data):
        encrypted_data_file = rsa.encrypt(data.encode(),self.public_key)
        file = open(encrypted_data_file,"rb")
        file_array = []
        for i in file.readlines():
            file_array.append(i)
        
        file_array_string = json.dumps({"file_array":file_array})
        conn.connection.send(str(sys.getsizeof(file_array)).encode())
        time.sleep(0.1)
        conn.connection.send(file_array_string.encode())
        del file_array


    # Receives data and decrypt it
    # Receive data length and data
    def receiver(self,conn):
        data_len = conn.connection.recv(10200)
        data_len = int(data_len.decode())
        data = conn.connection.recv(data_len)
        data = json.loads(data.decode())
        file_array = data.get("file_array")
        
        data = rsa.decrypt(file_array,self.private_key).decode()
        del data_len
        return data