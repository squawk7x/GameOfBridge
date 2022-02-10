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
		# client.close()
		print(f"now online: {self.nicknames}")
	
	def handle(self, client):
		while self.is_active:
			try:
				message = client.recv(1024).decode("utf-8")
				if message[-4:] == "quit":
					message = f"--- admin: " \
					          f"{self.get_nickname_of_client(client)} " \
					          f"left the chat ---"
					print(message)
					self.broadcast(message.encode("utf-8"))
					self.remove_client(client)
					break
				else:
					self.broadcast(message.encode("utf-8"))
			except:
				message = f"--- admin: " \
				          f"{self.get_nickname_of_client(client)} " \
				          f"not connected ---"
				print(message)
				self.broadcast(message.encode("utf-8"))
				self.remove_client(client)
				break
	
	def receive(self):
		while self.is_active:
			# Accept Connection
			client, address = self.server.accept()
			print("connected with {}".format(str(address)))
			client.send("--- admin: " \
			            "you are connected to the server! ---" \
			            "\n".encode("utf-8"))
			
			nickname = client.recv(1024).decode("utf-8")
			self.add_client(client, nickname)
			print("Nickname is {}".format(nickname))
			self.broadcast(f"--- broadcast: " \
			               f"{nickname} joined the chat! ---".encode("utf-8"))
			
			# Start Handling Thread For Client
			thread = threading.Thread(target=self.handle, args=(client,),
			                          daemon=True)
			thread.start()
	
	def run(self):
		print("Server is listening... ")
		self.receive()
	
	def stop(self):
		global is_active
		
		for client in self.clients:
			client.close()
		
		is_active = False
		self.server.close()
		print("Server stopped")


if __name__ == "__main__":
	gs = G_Server()
	gs.run()
