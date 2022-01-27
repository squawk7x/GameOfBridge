#!/usr/bin/env python3
import socket


class Gameclient():

	host = '127.0.0.1'
	port = 54321
	
	def upload_to_server(self, cdata=b'client data'):
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csock:
			csock.connect((self.host, self.port))
			csock.sendall(cdata)
			print(f'[Client] upload to server:\n', cdata)
	
	def download_from_server(self):
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csock:
			csock.connect((self.host, self.port))
			csock.send(b'request')
			cdata = csock.recv(1024)
			print(f'[Client] download from server:\n', cdata)
			return cdata
		

gameclient = Gameclient()

if __name__ == "__main__":
	gameclient.upload_to_server()
	gameclient.download_from_server()
	