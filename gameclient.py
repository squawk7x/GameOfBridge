#!/usr/bin/env python3
import socket


class Gameclient():

    def exchange_data(self, play_data_b=b''):
        host = '127.0.0.1'
        port = 54321

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csock:
            csock.connect((host, port))
            csock.sendall(play_data_b)
            print('Client says client data sent:\n', play_data_b)
            game_data_b = csock.recv(1024)
            print('Client says server data received:\n', game_data_b)

        return game_data_b


gameclient = Gameclient()

if __name__ == "__main__":
    gameclient.exchange_data()

