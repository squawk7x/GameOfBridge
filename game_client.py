import socket
import sys
import threading


class Client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def __init__(self, host='127.0.0.1'):
		self.host = host
	
	def run(self):
		self.sock.connect((self.host, 54321))
		c_thread = threading.Thread(target=self.exchange)
		c_thread.daemon = True
		c_thread.start()
		
		while True:
			data = self.sock.recv(1024)
			print(str(data, 'utf-8'))
			if not data:
				break
	
	def exchange(self):
		self.sock.send(bytes(input(""), 'utf-8'))
		
	def stop(self):
		self.sock.close()

if __name__ == "__main__":
	
	if (len(sys.argv) > 1):
		client = Client(sys.argv[1])
	else:
		client = Client()
	client.run()
	