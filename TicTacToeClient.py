
import socket
import pickle


def printBoard():
	print('\n -----')
	print('|' + choices[0] + '|' + choices[1] + '|' + choices[2] + '|')
	print(' -----')
	print('|' + choices[3] + '|' + choices[4] + '|' + choices[5] + '|')
	print(' -----')
	print('|' + choices[6] + '|' + choices[7] + '|' + choices[8] + '|')
	print(' -----\n')


def checkWin():
	for x in range(0, 3):
		y = x * 3
		if (choices[y] == choices[(y + 1)] and choices[y] == choices[(y + 2)]):
			return True
			printBoard()
		if (choices[x] == choices[(x + 3)] and choices[x] == choices[(x + 6)]):
			return True
			printBoard()
	
	if ((choices[0] == choices[4] and choices[0] == choices[8]) or (
			choices[2] == choices[4] and choices[4] == choices[6])):
		return True
		printBoard()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = "localhost"
port = 12345

s.connect((ip, port))

choices = []

for x in range(0, 9):
	choices.append(str(x + 1))

playerOneTurn = False
winner = False
whoWins = 0
score1 = 0
score2 = 0
playing = True

data = pickle.dumps(choices)
s.send(data)

while not winner:
	recvd_data = s.recv(1024)
	choices = pickle.loads(recvd_data)
	winner = checkWin()
	if winner == True:
		whoWins = '1'
	playerOneTurn = not playerOneTurn
	
	if not winner and not playerOneTurn:
		choice = ''
		
		printBoard()
		
		print("Player 2:")
		
		while choice == '':
			try:
				choice = int(input(">> "))
			except:
				print("please enter a valid field")
				choice = ''
				continue
			if choices[choice - 1] == 'X' or choices[choice - 1] == 'O':
				choice = ''
				print("illegal move, plase try again")
				continue
		
		if playerOneTurn:
			choices[choice - 1] = 'X'
		else:
			choices[choice - 1] = 'O'
		
		winner = checkWin()
		if winner == True:
			whoWins = '2'
	
	data = pickle.dumps(choices)
	s.send(data)

print("Player " + whoWins + " wins!\n")

s.close()
