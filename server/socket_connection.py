# need to import tools send_password and recv_password
import socket
from cryptography.fernet import Fernet
import tools
import os
import threading
# Socket tools class which is used as an object.
class socket_tools:

    # initialization of the class
    def __init__(self,host,port,file_path_to_read_and_write):
        self.host = host
        self.port = port
        self.all_connections = []
        self.all_address = []
        self.file_path_to_read_and_write = os.path.abspath(file_path_to_read_and_write)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind_socket()
        self.send_password, self.recv_password, self.key = tools.tool.data_loader(file_path_to_read_and_write)
        
    
    # this binds the socket
    def bind_socket(self):
        try:
            self.s.bind((self.host,self.port))
            self.s.listen(5)
        except:
            raise Exception("E: Error in binding the port")
    

    # To accept connections and append to list
    def accepting_connections(self):
        for c in self.all_connections:
            c.close()

        del self.all_connections[:]
        del self.all_address[:]

        while True:
            try:
                conn, address = self.s.accept()
                self.s.setblocking(1)  # prevents timeout
                received_password_from_client = self.receiver(conn)
                if received_password_from_client == self.send_password:
                    self.sender(conn,self.recv_password)
                self.all_connections.append(conn)
                self.all_address.append(address)

                print("D: Connection has been established :" + address[0])

            except:
                print("E: Error accepting connections")


    # Encrypts content and send it
    # Send data length and data
    def sender(self,conn,data):
        encryptor = Fernet(self.key)
        encrypted_data = encryptor.encrypt(data.encode())
        encrypted_data_len = str(sys.getsizeof(encrypted_data.decode()))
        encrypted_data_len = encryptor.encrypt(encrypted_data_len.encode())
        conn.send(encrypted_data_len)
        time.sleep(0.1)
        conn.send(encrypted_data)


    # Receives data and decrypt it
    # Receive data length and data
    def receiver(self,conn):
        data_len = conn.recv(10200)
        decryptor = Fernet(self.key)
        data_len = int(decryptor.decrypt(data_len).decode())
        data = conn.recv(data_len)
        data = decryptor.decrypt(data).decode()
        del data_len,decryptor
        return data