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
        self.recv_password = data_loader(file_path_to_read_and_write)
        
    
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
                self.sender(conn,self.recv_password)

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
    
    # Encrypts content and send it
    # Send data length and data
    def sender(self,client_object,data):
        key_path = client_object.public_key
        encrypted_data = rsa.encrypt(data.encode(),key_path) # Getting encrypted array from encrypt func
        encrypted_data_array = json.dumps({"result_array":encrypted_data}) # Dumping it to a json to be sent through sockets  
        conn.connection.send(str(sys.getsizeof(encrypted_data_array)).encode())
        time.sleep(0.1)
        conn.connection.send(encrypted_data_array.encode())


    # Receives data and decrypt it
    # Receive data length and data
    def receiver(self,conn):
        data_len = conn.connection.recv(10200)
        data_len = int(data_len.decode())
        data = conn.connection.recv(data_len)
        data = json.loads(data.decode())
        result_array = data.get("result_array")
        
        data = rsa.decrypt(result_array).decode()
        return data