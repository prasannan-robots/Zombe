# need to import tools send_password and recv_password
import socket
import rsa
from modules.tools import clients,data_loader
import os, sys, time
import threading
# Socket tools class which is used as an object.
class socket_tools:

    # initialization of the class
    def __init__(self,host,port,file_path_to_read_and_write):
        self.host = host
        self.port = port
        self.array_of_client_objects = []
        self.file_path_to_read_and_write = os.path.abspath(file_path_to_read_and_write)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind_socket()
        self.public_key_server, self.private_key, self.recv_password = data_loader(file_path_to_read_and_write)
        
    
    # this binds the socket
    def bind_socket(self):
        try:
            self.s.bind((self.host,self.port))
            self.s.listen(5)
        except:
            raise Exception("E: Error in binding the port")
    

    # To accept connections and append to list
    def accepting_connections(self):
        for c in self.array_of_client_objects:
            c = c.connection
            c.close()

        del self.array_of_client_objects[:]

        while True:
            try:
                conn, address = self.s.accept()
                self.s.setblocking(1)  # prevents timeout
                public_key = self.receiver(conn)
                self.sender(conn,self.send_password)
                client_obj = clients(conn,address,public_key)
                self.array_of_client_objects.append(client_obj)
                print("D: Connection has been established :" + address[0])

            except Exception as msg:
                print("E: Error accepting connections", msg)


    # Encrypts content and send it
    # Send data length and data
    def sender(self,conn,data):
        encrypted_data = rsa.encrypt(data.encode(),self.public_key)
        encrypted_data_len = str(sys.getsizeof(encrypted_data.decode()))
        encrypted_data_len = rsa.encrypt(encrypted_data_len.encode())
        conn.connection.send(encrypted_data_len)
        time.sleep(0.1)
        conn.connection.send(encrypted_data)


    # Receives data and decrypt it
    # Receive data length and data
    def receiver(self,conn):
        data_len = conn.connection.recv(10200)
        data_len = int(rsa.decrypt(data_len,self.private_key).decode())
        data = conn.connection.recv(data_len)
        data = rsa.decrypt(data,self.private_key).decode()
        del data_len
        return data