import socket
import threading

host = '127.0.0.1'
port = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((host, port))
sock.listen(1)

connections = []


def handler(c, a):
	while True:
		data = c.recv(1024)
		for connection in connections:
			connection.send(bytes(data))
		if not data:
			connections.remove(c)
			c.close()
			break


while True:
	c, a = sock.accept()
	cThread = threading.Thread(target=handler, args=(c, a))
	cThread.daemon = True
	cThread.start()
	connections.append(c)
	print(connections)
