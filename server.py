#!/usr/bin/env python3
import selectors
import socket
import sys


class Server():
	host = '0.0.0.0'
	port = 54321
	sdata = b''
	
	def __init__(self):
		self.sel = selectors.DefaultSelector()
		self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IP/TCP
	
	def accept(self, ssock, mask):
		conn, addr = ssock.accept()
		print('[Server] client accepted\n', conn, 'from', addr)
		conn.setblocking(False)
		self.sel.register(conn, selectors.EVENT_READ, self.share_data)
	
	def share_data(self, conn, mask):
		sdata = conn.recv(1024)
		
		if sdata and sdata != b'request':
			self.sdata = sdata
			print('[Server] received from client:\n', self.sdata)
		elif sdata == b'request':
			conn.sendall(self.sdata)
			print('[Server] sent to client:\n', self.sdata)
		
		self.sel.unregister(conn)
		print('[Server] unregister client\n', conn)
		conn.close()
	
	def run(self):
		self.ssock.bind((self.host, self.port))
		self.ssock.listen(4)
		self.ssock.setblocking(False)
		self.sel.register(self.ssock, selectors.EVENT_READ, self.accept)
		
		while True:
			print('\n[Server] is waiting for client...')
			events = self.sel.select()
			for key, mask in events:
				callback = key.data
				callback(key.fileobj, mask)
	
	def stop(self):
		self.sel.close()


#server = Server()


class Client():
	host = '127.0.0.1'
	port = 54321
	
	def __init__(self, host):
		self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.csock.connect((host, self.port))
	
	def upload_to_server(self, cdata=b'client data'):
		self.csock.sendall(cdata)
		print(f'[Client] upload to server:\n', cdata)
	
	def download_from_server(self):
		self.csock.connect((self.host, self.port))
		self.csock.send(b'request')
		cdata = self.csock.recv(1024)
		print(f'[Client] download from server:\n', cdata)
		return cdata


if __name__ == "__main__":
	
	if (len(sys.argv) > 1):
		client = Client(sys.argv[1])
		client.upload_to_server()
		client.download_from_server()
	else:
		server = Server()
		server.run()
