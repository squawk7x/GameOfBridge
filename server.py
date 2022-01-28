import socket
import sys
import threading

host = '0.0.0.0'
port = 54321


class Server():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	
	def __init__(self):
		# self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((host, port))
		self.sock.listen(1)
	
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
	
	def run(self):
		while True:
			c, a = self.sock.accept()
			sThread = threading.Thread(target=self.handler, args=(c, a))
			sThread.daemon = True
			sThread.start()
			self.connections.append(c)
			print(f'{str(a[0])}:{str(a[1])} connected')


class Client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def __init__(self, adress):
		self.sock.connect((adress, 54321))
		cThread = threading.Thread(target=self.exchange)
		cThread.daemon = True
		cThread.start()
		
		while True:
			data = self.sock.recv(1024)
			print(str(data, 'utf-8'))
			if not data:
				break
	
	def exchange(self):
		self.sock.send(bytes(input(""), 'utf-8'))



if __name__ == "__main__":
	
	if (len(sys.argv) > 1):
		client = Client(sys.argv[1])
	else:
		server = Server()
		server.run()
