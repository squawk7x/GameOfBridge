#!/usr/bin/env python3
import selectors
import socket


class Gameserver():
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
			#print('[Server] received from client:\n', self.sdata)
		elif sdata == b'request':
			conn.sendall(self.sdata)
			#print('[Server] sent to client:\n', self.sdata)
		
		self.sel.unregister(conn)
		print('[Server] unregister client\n', conn)
		conn.close()
	
	def start(self, host='localhost', port=54321):
		self.ssock.bind((host, port))
		
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


gameserver = Gameserver()

if __name__ == "__main__":
	gameserver.start()
