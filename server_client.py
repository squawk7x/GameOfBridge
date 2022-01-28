import socket
import sys
import threading

host = '127.0.0.1'
port = 54321


class Server():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	data = b''
	
	def __init__(self):
		# self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((host, port))
		self.sock.listen(1)
		print(f'[{str(host)}:{str(port)}] Server waiting for connections ...')
	
	def handler(self, c, a):
		while True:
			data = c.recv(1024)
			if data and data == b'download':
				for connection in self.connections:
					connection.send(self.data)
				print('Server has sent data to client', data)
			elif data:
				self.data = data
				print('Server has received data from client', data)
				# for connection in self.connections:
				# 	connection.send(b'')
			elif not data:
				print(f'{str(a[0])}:{str(a[1])} disconnected')
				self.connections.remove(c)
				c.close()
				break
	
	def run(self):
		while True:
			c, a = self.sock.accept()
			
			s_thread = threading.Thread(target=self.handler, args=(c, a))
			s_thread.daemon = True
			s_thread.start()
			
			self.connections.append(c)
			print(f'{str(a[0])}:{str(a[1])} connected')
	
	def stop(self):
		self.sock.close()


class Client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	adress = None
	
	def __init__(self, adress='127.0.0.1'):
		self.adress = adress
		self.run()

	def exchange(self, data='data from client-exchange'):
		#self.sock.send(bytes(input(""), 'utf-8'))
		self.sock.send(data)
		while True:
			data = self.sock.recv(1024)
			print(data)
			if data:
				return data
			else:
				break
	
	def run(self):
		self.sock.connect((self.adress, 54321))
		
		c_thread = threading.Thread(target=self.exchange)
		c_thread.daemon = True
		c_thread.start()
	

if __name__ == "__main__":
	
	if (len(sys.argv) > 1):
		client = Client(sys.argv[1])
	else:
		server = Server()
		server.run()
