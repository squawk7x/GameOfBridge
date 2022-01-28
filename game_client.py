import socket
import sys
import threading


class Client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	game_data = b''
	
	def __init__(self, host='127.0.0.1'):
		self.host = host
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	def run(self):
		self.sock.connect((self.host, 54321))
		c_thread = threading.Thread(target=self.upload_data)
		c_thread.daemon = True
		c_thread.start()
		
		while True:
			data = self.sock.recv(1024)
			self.game_data = data
			#print('received data', data)
			if not data:
				break
	
	def deliver_data(self):
		#print('deliver data:\n', self.game_data)
		return self.game_data
	
	def upload_data(self, data=b''):
		#print('upload data:\n', data)
		self.sock.send(data)
		
	def stop(self):
		self.sock.close()

if __name__ == "__main__":
	
	if (len(sys.argv) > 1):
		client = Client(sys.argv[1])
	else:
		client = Client()
	client.run()
	