import socket
import sys
import threading


class Server():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	
	def __init__(self, host='0.0.0.0', port=54321):
		self.host = host
		self.port = port
	
	def handler(self, c, a):
		while True:
			data = c.recv(1024)
			for connection in self.connections:
				connection.send(data)
			if not data:
				print(f'{str(a[0])}:{str(a[1])} disconnected')
				self.connections.remove(c)
				c.close()
				break
	
	def show_connections(self):
		for connection in self.connections:
			print(connection)
	
	def run(self):
		self.sock.bind((self.host, self.port))
		self.sock.listen(1)
		print(f'[{str(self.host)}:{str(self.port)}] Server waiting for connections...')
		
		while True:
			c, a = self.sock.accept()
			s_thread = threading.Thread(target=self.handler, args=(c, a))
			s_thread.daemon = True
			s_thread.start()
			self.connections.append(c)
			print(f'{str(a[0])}:{str(a[1])} connected')
	
	def stop(self):
		self.sock.close()


if __name__ == "__main__":

	server = Server()
	server.run()
