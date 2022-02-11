import threading
import socket


class G_Server:
	is_active = True
	clients = []
	nicknames = []

	def __init__(self, host="127.0.0.1", port=54321):

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((host, port))
		self.server.listen()

	def broadcast(self, message):
		for client in self.clients:
			client.send(message)

	def add_client(self, client, nickname):
		self.clients.append(client)
		self.nicknames.append(nickname)
		print(f"now online: {self.nicknames}")

	def get_nickname_of_client(self, client):
		index = self.clients.index(client)
		nickname = self.nicknames[index]
		return nickname

	def remove_client(self, client):
		index = self.clients.index(client)
		nickname = self.nicknames[index]
		self.nicknames.remove(nickname)
		self.clients.remove(client)
		client.close()
		print(f"now online: {self.nicknames}")

	def handle(self, client):
		while self.is_active:
			try:
				message = client.recv(2048)
				if message.decode()[-4:] == "quit":
					advice = f"--- broadcast: " \
					          f"{self.get_nickname_of_client(client)} " \
					          f"left ---"
					print(advice)
					self.broadcast(advice.encode())
					self.remove_client(client)
					break
				else:
					self.broadcast(message)

			except Exception:
				advice = f"--- admin: " \
				          f"{self.get_nickname_of_client(client)} " \
				          f"not connected ---"
				print(advice)
				self.remove_client(client)
				break


	def receive(self):
		while self.is_active:
			# Accept Connection
			client, address = self.server.accept()  # Waiting for new client
			print("connected with {}".format(str(address)))

			client.send("--- admin: you are connected to the server! ---\n"
			               .encode())

			nickname = client.recv(1024).decode()
			self.add_client(client, nickname)
			print("Nickname is {}".format(nickname))
			self.broadcast(f"--- broadcast: {nickname} joined! ---"
			               .encode())

			thread = threading.Thread(target=self.handle, args=(client,), daemon=True)
			thread.start()

	def run(self):
		print("Server is listening... ")
		self.receive()

	def stop(self):

		for client in self.clients:
			client.close()

		self.is_active = False
		self.server.close()
		print("Server stopped")


if __name__ == "__main__":
	gs = G_Server()
	gs.run()
