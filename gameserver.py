#!/usr/bin/env python3
import selectors
import socket


class Gameserver():

    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IP/TCP
        self.sdata = b'empty data'

    def accept(self, ssock, mask):
        conn, addr = ssock.accept()
        print('Server says client accepted\n', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        cdata = conn.recv(1024)
        if cdata:
            print('Server says client data received:\n', cdata)
            conn.sendall(cdata)                                 # echo back
            print('Server says server data sent :\n', cdata)
        else:
            self.sel.unregister(conn)
            print('Server says unregister client\n', conn)
            conn.close()

    def set_transfer_data(self, data):
        self.sdata = data

    def start(self, host='localhost', port=54321):
        self.ssock.bind((host, port))
        self.ssock.listen(4)
        self.ssock.setblocking(False)
        self.sel.register(self.ssock, selectors.EVENT_READ | selectors.EVENT_WRITE, self.accept)

        while True:
            print('Waiting for client...')
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def stop(self):
        self.sel.close()


gameserver = Gameserver()

if __name__ == "__main__":
    gameserver.start()
