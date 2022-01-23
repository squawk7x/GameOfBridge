#!/usr/bin/env python3
import pickle
import socket
import Bridge




HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 54321        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'request blind')
    data = s.recv(1024)

cardset = pickle.loads(data)



cardset.show_blind()
cardset.show_stack()






