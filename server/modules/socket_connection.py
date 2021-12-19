# need to import tools send_password and recv_password
import socket
from modules.tools import clients,data_loader,rsa
import os
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
            c.delete_key_file()
            c = c.connection
            c.close()
            
        del self.array_of_client_objects[:]
        id_for_client = 0
        while True:
            try:
                conn, address = self.s.accept()
                self.s.setblocking(1)  # prevents timeout
                public_key = rsa.receiver(conn)
                self.sender(conn,self.send_password)

                client_obj = clients(conn,address)
                id_for_client = id_for_client + 1
                client_obj.save_public_key(public_key,id_for_client)
                self.array_of_client_objects.append(client_obj)

                print("D: Connection has been established :" + address[0])

            except Exception as msg:
                print("E: Error accepting connections", msg)
        
    # To remove clients in easy manner
    def remove_client(self,index_of_client_in_array_of_client_objects):
        object = self.array_of_client_objects[index_of_client_in_array_of_client_objects]   
        object.delete_key_file()
        del self.array_of_client_objects[index_of_client_in_array_of_client_objects],object 
    
    # Creating a proxy sender and receiver to call the one in tools.rsa
    def sender(self,client_object,data_to_be_sent):
        key_path = client_object.public_key
        rsa.sender(key_path,data_to_be_sent)

    def receiver(self,client_object):
        return rsa.receiver(client_object)