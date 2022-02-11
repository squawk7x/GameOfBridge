import socket
import threading


class G_Client:
	is_active = True

	def __init__(self, host='127.0.0.1', port=54321):

		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.client.connect((host, port))

		self.nickname = input("Choose a nickname: ")
		self.client.send(self.nickname.encode())

	def receive(self):      # <= Server.broadcast
		while self.is_active:
			try:
				message = self.client.recv(2048).decode()
				print(message)
			except IOError:
				print("an IOError occurred!")
				self.stop()
				break

	def write(self, data=None):  # => Server.handle

		if not data:
			while self.is_active:
				message = f'{self.nickname}: {input("")}'
				self.client.send(message.encode())
		else:
			self.client.send(data)

	def run(self):
		receive_threat = threading.Thread(target=self.receive)
		receive_threat.start()

		write_thread = threading.Thread(target=self.write)
		write_thread.start()

	def stop(self):
		self.client.send('quit'.encode())
		self.is_active = False
		self.client.close()


if __name__ == '__main__':
	gc = G_Client()
	gc.run()


'''
class Client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	game_data = b''

	def __init__(self, host='127.0.0.1', port=54321):
		self.host = host
		self.port = port
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def start(self):
		self.sock.connect((self.host, self.port))
		c_thread = threading.Thread(target=self.upload_data, daemon=True)
		c_thread.start()

		while True:
			data = self.sock.recv(4096)
			self.game_data = data

			if data:
				data_from_server = pickle.loads(data)
				self.game_data = data
				deck.__dict__ = data_from_server[0]
				self.__dict__ = data_from_server[1]
				bridge.player_list[0].__dict__ = data_from_server[2]
				bridge.player_list[1].__dict__ = data_from_server[3]
				bridge.player_list[2].__dict__ = data_from_server[4]

			if not data:
				break

	def deliver_data(self):
		return self.game_data

	def upload_data(self, data=b''):
		self.sock.send)(data)

	def stop(self):
		self.sock.close()
'''
