#!/usr/bin/env python3
import socket


class Gameclient():

    def exchange_data(self, cdata=b'client data'):
        host = '127.0.0.1'
        port = 54321

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csock:
            csock.connect((host, port))
            csock.sendall(cdata)
            print('Client said client data sent:\n', cdata)
            data = csock.recv(1024)
            print('Client said server data received:\n', data)

        return data


gameclient = Gameclient()

if __name__ == "__main__":
    gameclient.exchange_data()

