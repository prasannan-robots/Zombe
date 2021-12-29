from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import sys,time,os,json,shutil


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
        return arr[0]

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

        public_key_file = open(f"./temp/client_key/{id}.pem","w").write(key)
        self.public_key = f"./temp/client_key/{id}.pem"
        del public_key_file
    
    def get_public_key(self):
        key = RSA.import_key(open(self.public_key).read())
        return key

    def delete_key_file(self):
        if os.path.exists(self.public_key):
            os.remove(self.public_key)



# To Manage encryption and decryption

class rsa:

    # To encrypt and decrypt using rsa opencryptdome
    # Uses a file to save the incoming data and opening it and decrypting it
    # All public_key of the clients are stored in file with unique no 
    def encrypt(data,public_key):
        result_array = [] # To store results in this array
        recipient_key = RSA.import_key(open(public_key).read())
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
        private_key = RSA.import_key(open("./temp/private.pem").read())

        print(cipher)
        enc_session_key, nonce, tag, ciphertext = cipher
        print(enc_session_key,type(enc_session_key))
        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode()
    
def cleanup():
    try:
        shutil.rmtree("temp/client_key")
        os.mkdir("temp/client_key")
    except:
        try:
            os.mkdir("temp/client_key")
        except:
            pass