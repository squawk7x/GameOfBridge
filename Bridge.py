#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from datetime import date

import keyboard

suits = ['\u2666', '\u2665', '\u2660', '\u2663']
ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suit_colors = ['\033[95m', '\033[91m', '\033[93m', '\033[94m']
reset_color = '\033[0m'


class Card:
	# Represents a single playing card
	
	def __init__(self, suit, rank):
		if suit in suits and rank in ranks:
			self.suit = suit
			self.rank = rank
			self.value = self.set_value(self.rank)
	
	def __str__(self):
		card = None
		if self.suit == '\u2666':
			card = f'{suit_colors[0]}{self.suit}{self.rank}{reset_color} '
		elif self.suit == '\u2665':
			card = f'{suit_colors[1]}{self.suit}{self.rank}{reset_color} '
		elif self.suit == '\u2660':
			card = f'{suit_colors[2]}{self.suit}{self.rank}{reset_color} '
		elif self.suit == '\u2663':
			card = f'{suit_colors[3]}{self.suit}{self.rank}{reset_color} '
		return card
	
	def __eq__(self, other):
		if self.suit == other.suit and self.rank == other.rank:
			return True
		else:
			return False
		
	def __lt__(self, other):
		if self.get_value() < other.get_value():
			return True
		else:
			return False
	
	def __gt__(self, other):
		if self.get_value() > other.get_value():
			return True
		else:
			return False
	
	def get_suit(self):
		return self.suit
	
	def get_rank(self):
		return self.rank
	
	def set_value(self, rank):
		value = 0
		if rank in {'10', 'Q', 'K'}:
			value = 10
		if rank == 'A':
			value = 15
		if rank == 'J':
			value = 20
		return value
	
	def get_value(self):
		return self.value


class Jsuit:
	# Represents the suit to choose for 'J'
	def __init__(self, suit, color):
		self.suit = suit
		self.color = color
	
	def __str__(self):
		sign = f'{self.color}{self.suit}{self.suit}{reset_color} '
		return sign
	
	def __eq__(self, other):
		if self.suit == other.suit:
			return True
		else:
			return False
	
	def get_suit(self):
		return self.suit


class Jchoice:
	# array of suits for 'J'
	js = []
	j = None
	
	def __init__(self):
		self.js = [Jsuit('\u2666', '\033[95m'), Jsuit('\u2665', '\033[91m'), Jsuit('\u2660', '\033[93m'),
		           Jsuit('\u2663', '\033[94m')]
	
	def toggle_js(self):
		self.js.insert(0, self.js.pop())
	
	def set_j(self, color=None):
		if color:
			self.j = self.js[color]
		else:
			self.j = self.js[-1]
	
	def clear_j(self):
		self.j = None
	
	def get_j(self):
		if self.j:
			return self.j
		else:
			return ''
	
	def get_j_suit(self):
		if self.j:
			return self.j.suit
	
	def show_js(self):
		js = ''
		for j in self.js:
			js += str(j)
		print(11 * " " + js)


jchoice = Jchoice()


class Deck:
	# Represents a card deck with a blind and a stack
	
	def __init__(self):
		self.blind = []
		self.stack = []
		self.bridge_monitor = []
		self.evaluation = []
		self.shufflings = 1
		
		for suit in suits:
			for rank in ranks:
				self.blind.append(Card(suit, rank))
		self.shuffle_blind()
	
	# deck methods
	def show(self):
		self.show_blind(visible=True)
		self.show_cards_for_evaluation()
		self.show_bridge_monitor()
		self.show_stack(visible=True)
	
	# blind methods
	def show_blind(self, visible=False):
		blind = ''
		for card in self.blind:
			if visible:
				blind += str(card)
			else:
				blind += '## '
		print(f'\n{20 * " "}Blind ({len(self.blind)}) card(s):')
		print(f'{20 * " "}{blind}\n')
	
	def shuffle_blind(self):
		random.shuffle(self.blind)
	
	def card_from_blind(self):
		if len(self.blind) == 0:
			self.blind = self.stack
			self.stack = []
			self.stack.append(self.blind.pop())
			random.shuffle(self.blind)
			self.shufflings += 1
		if self.blind:
			return self.blind.pop()
		else:
			print('not enough cards available')
			exit()
	
	# stack methods
	def show_stack(self, visible=False):
		stack = ''
		if visible:
			for card in self.stack:
				stack = str(card) + stack
		else:
			for c in range(len(self.stack) - 1):
				stack += '## '
			stack = str(self.stack[-1]) + stack
		stack = f'{jchoice.get_j()}' + stack
		print(f'{20 * " "}Stack ({len(self.stack)}) card(s):')
		print(f'{20 * " "}{stack}\n')
	
	def put_card_on_stack(self, card):
		self.stack.append(card)
	
	def get_top_card_from_stack(self):
		if self.stack:
			return self.stack[-1]
	
	#  bridge monitor
	def update_bridge_monitor(self, card: Card):
		if deck.bridge_monitor and card.rank != deck.bridge_monitor[0].rank:
			deck.bridge_monitor.clear()
		deck.bridge_monitor.append(card)
	
	def show_bridge_monitor(self):
		bridge = ''
		for card in self.bridge_monitor:
			bridge += str(card)
		print(f'Bridge monitor ({len(self.bridge_monitor)}) card(s):')
		print(f'{bridge}')
	
	# evaluation monitor
	def append_card_for_evaluation(self, card: Card):
		if card.rank in {'7', '8', 'A'}:
			self.evaluation.append(card)
	
	def remove_card_from_evaluation(self, card):
		self.evaluation.remove(card)
	
	def show_cards_for_evaluation(self):
		evaluation = ''
		for card in self.evaluation:
			evaluation += str(card)
		print(f'Cards for evaluation ({len(self.evaluation)}) card(s):')
		print(f'{evaluation}')


deck = Deck()


class Handdeck:
	''' Represents the player's cards with some functionality '''
	
	def __init__(self):
		self.cards = []
		self.cards_drawn = []
		self.cards_played = []
		self.possible_cards = []
	
	def __len__(self):
		return len(self.cards)
	
	def count_points(self):
		points = 0
		for card in self.cards:
			points += card.value
		return points
	
	def remove_card_from_cards(self, c: Card):
		if self.cards:
			for card in self.cards:
				if card.suit == c.suit and card.rank == c.rank:
					self.cards.remove(card)
	
	def remove_card_from_possible_cards(self, c: Card):
		if self.possible_cards:
			for card in self.possible_cards:
				if card.suit == c.suit and card.rank == c.rank:
					self.possible_cards.remove(card)
	
	def get_possible_cards(self):
		
		self.possible_cards = []
		stack_card = deck.get_top_card_from_stack()
		
		'''
		1st move:
		---------
		suit    rank    J

		stack_card = '6' 3r
		suit    rank    J

		stack_card = 'J'
		suit            J

		2nd move:
		---------
				rank

		stack_card = '6'
		suit    rank    J

		stack_card 'J':
		suit            J

		'''
		
		if not self.cards_played:
			if stack_card.rank == 'J':
				for card in self.cards:
					if card.suit == jchoice.get_j_suit() or card.rank == 'J':
						self.possible_cards.append(card)
			else:
				for card in self.cards:
					if card.rank == stack_card.rank or card.suit == stack_card.suit or card.rank == 'J':
						self.possible_cards.append(card)
		if self.cards_played:
			if stack_card.rank == '6':
				for card in self.cards:
					if card.rank == stack_card.rank or card.suit == stack_card.suit or card.rank == 'J':
						self.possible_cards.append(card)
			elif stack_card.rank == 'J':
				for card in self.cards:
					if card.suit == jchoice.get_j_suit() or card.rank == 'J':
						self.possible_cards.append(card)
			else:
				for card in self.cards:
					if card.rank == stack_card.rank:
						self.possible_cards.append(card)
		return self.possible_cards


class Player:
	''' Represents a player with cards in hand '''
	name = None
	robot = False
	hand = None
	score = 0
	
	def __init__(self, name=None, robot=False):
		self.name = name
		self.robot = robot
		self.hand = Handdeck()
	
	def __lt__(self, other):
		if self.score < other.score:
			return True
		else:
			return False
	
	'''
	def __eq__(self, other):
		if self.score == other.score:
			return True
		else:
			return False
	'''
	
	def __gt__(self, other):
		if self.score > other.score:
			return True
		else:
			return False
	
	def draw_new_cards(self):
		self.hand.cards = []
		self.hand.cards_played = []
		self.hand.cards_drawn = []
		
		for _ in range(5):
			self.hand.cards.append(deck.blind.pop())
			
	def arrange_hand_cards(self):
		if self.hand.cards:
			self.hand.cards.sort()
			if self.hand.cards[-1].rank == 'J':
				self.hand.cards.insert(0, self.hand.cards.pop())
			# if self.hand.cards[0] != self.hand.cards[-1]:
			# 	while self.hand.cards[-1].rank == 'J':
			# 		self.hand.cards.insert(0, self.hand.cards.pop())
	
	def show(self):
		self.show_possible_cards()
		self.show_hand(visible=True)
	
	def show_hand(self, visible=False):
		self.arrange_hand_cards()
		cards = ''
		for card in self.hand.cards:
			if visible:
				cards += str(card)
			else:
				cards += '## '
		if visible:
			print(f'{self.name} holds ({len(self.hand.cards)}) card(s) [{self.hand.count_points()} points]:')
		else:
			print(f'{self.name} holds ({len(self.hand.cards)}) card(s):')
		print(cards)
	
	def show_possible_cards(self):
		cards = ''
		self.hand.possible_cards = self.hand.get_possible_cards()
		for card in self.hand.possible_cards:
			cards += str(card)
		print(f'{self.name} has played ({len(self.hand.cards_played)}) / drawn ({len(self.hand.cards_drawn)}) card(s)'
		      f' and can play ({len(self.hand.possible_cards)}) card(s):')
		print(cards)
	
	def toggle_possible_cards(self):
		if self.hand.possible_cards:
			card = self.hand.possible_cards.pop()
			self.hand.cards.remove(card)
			self.hand.cards.insert(0, card)
			self.hand.possible_cards.insert(0, card)
	
	def get_card_from_blind(self, cards=1):
		for card in range(cards):
			card = deck.card_from_blind()
			self.hand.cards.append(card)
			self.hand.cards_drawn.append(card)
	
	def must_draw_card(self):
		
		'''
		must draw card, if:
		---------------------------------
		 card   possible  card    pull
		played    card    drawn   card
			1       1       1       N
			1       1       0       N
			1       0       1       N
			1       0       0       N
			0       1       1       N
			0       1       0       N
			0       0       1       N
			0       0       0       Y       <--

		'6' on stack:
		-------------
			1		0		1		Y       <--
		'''
		
		stack_card = deck.get_top_card_from_stack()
		if stack_card.rank == '6' and not self.hand.possible_cards:
			self.get_card_from_blind()
		elif not self.hand.cards_played and not self.hand.possible_cards and not self.hand.cards_drawn:
			self.get_card_from_blind()
		else:
			pass
	
	def play_card(self, is_initial_card=False):
		if is_initial_card:# and not deck.stack:
			card = self.hand.cards.pop()
			deck.update_bridge_monitor(card)
			deck.put_card_on_stack(card)
			self.hand.cards_played.append(card)
			self.hand.get_possible_cards()
			deck.append_card_for_evaluation(card)
		if not is_initial_card and self.hand.possible_cards:
			card = self.hand.possible_cards.pop()
			self.hand.cards.remove(card)
			deck.update_bridge_monitor(card)
			deck.put_card_on_stack(card)
			self.hand.cards_played.append(card)
			deck.append_card_for_evaluation(card)
			jchoice.clear_j()
	
	def set_robot(self, robot=False):
		self.robot = robot
	
	def is_robot(self):
		return self.robot
	

class Bridge:
	'''
	Game of Bridge

	Rules Of The Game:
	------------------
	Bridge is played with 36 cards (4 suits and ranks from 6 to Ace) by 2-4 players.
	Each player starts with 5 cards from blind. First player puts a card onto the stack
	and can add more cards with same rank. The next player can play first card either
	same suit or same rank and can play more cards with same rank. First the cards on hand
	must be used and at least 1 card must be played or must be drawn from blind.
	No more than one card can be drawn from blind, except a '6' must be covered.

	Special Cards:
	--------------
	6   must be covered by same player, drawing cards until possible move
	7   next player must draw 1 card from blind
	8   next player must draw all cards (2 for each '8') from blind and will be passed over - or -
			following players must draw 2 cards and will be passed over
	J   can be played to any suit and player can choose which suit must follow
	A   next player will be passed over. With multiple 'A' the next players will be passed over

	Special Rule 'Bridge':
	----------------------
	If there are the same 4 cards in a row on the stack, the player of the 4th card can choose whether or not
	to finish the actual round.

	Counting:
	---------
	A round is over when one player has no more cards.
	The players note their points:

			6   0
			7   0
			8   0
			9   0
			10  10
			J   20  (-20)
			Q   10
			K   10
			A   15

	The points of several rounds will be added.
	If the blind was empty and the stack was reshuffeled, the points of this round are doubled, tripled, ...
	If a player finishes a round with a 'J' his score will be reduced by 20 for each 'J' of this last move.
	If a player reaches exactly 125 points, his score is back on 0!
	The player with the highest score starts the next round.

	The game is over once a player reaches more than 125 points.
	'''
	
	player = None
	number_of_players = 0
	player_list = []
	number_of_rounds = 0
	number_of_games = 0
	shuffler = None
	
	def __init__(self):
		
		while True:
			try:
				print("Enter number of players:")
				self.number_of_players = int(
					keyboard.read_hotkey(suppress=False))
			except ValueError:
				print('Valid number, please')
				continue
			if 2 <= self.number_of_players <= 4:
				break
			else:
				print('Please enter value between 2 and 4')
		
		try:
			os.remove(f'{date.today()}_scores.txt')
		except OSError as e:
			print('no scorelist found')
			
	def start_game(self):
		self.number_of_games += 1
		self.number_of_rounds = 0
		
		self.player_list.clear()
		
		for player in range(self.number_of_players):
			self.player_list.append(Player(f'Player-{player + 1}'))
	
		for player in self.player_list:
			if player.name != 'Player-1':
				player.set_robot(robot=True)
		
		self.start_round()
	
	def start_round(self):
		deck.__init__()
		
		for player in self.player_list:
			player.draw_new_cards()
		
		self.number_of_rounds += 1
		self.set_shuffler()
		self.player = self.shuffler
		self.player.play_card(is_initial_card=True)
	
	def set_shuffler(self):
		if self.shuffler == None:
			self.shuffler = self.player_list[0]
		else:
			self.shuffler = max(self.player_list)
			# self.shuffler = (sorted(self.player_list, key=lambda player: player.score)).pop()
	
	def activate_next_player(self):
		previous_player_was_robot = self.player.is_robot()
		aces = 0
		eights = 0
		
		self.player.hand.cards_played = []  # this player preparation for next turn
		self.player.hand.cards_drawn = []  # this player preparation for next turn
		self.player_list.append(self.player_list.pop(0))
		self.player = self.player_list[0]  # next player activated
		
		for card in deck.evaluation:
			if card.rank == '7':
				self.player.get_card_from_blind()
				self.player.hand.cards_drawn.clear()
			if card.rank == '8':
				eights += 1
			if card.rank == 'A':
				aces += 1
		deck.evaluation.clear()
		
		if eights == 1 or (eights and self.number_of_players == 2):
			for eight in range(eights):
				self.player.get_card_from_blind(2)
			self.player.hand.cards_drawn.clear()
			self.activate_next_player()
			
		elif eights >= 2:
			if previous_player_was_robot:
				key = random.choice(['a', 'n'])
				if key == 'a':
					print(f'\n{21 * " "}{self.player.name} said:')
					print(f"{22 * ' '}8's for all")
					print(f'{20 * " "}| SPACE |\n')
				elif key == 'n':
					print(f'\n{21 * " "}{self.player.name}:')
					print(f"{15 * ' '}All 8's for next player")
					print(f'{20 * " "}| SPACE |\n')
				keyboard.wait('space')
				
			else:
				print(f"\n{13 * ' '}? ? ? How to share the 8's ? ? ?\n")
				print(f'{13 * " "}| (n)ext player | (a)ll players |\n')
				key = keyboard.read_hotkey(suppress=False)
			
			if key == 'n':
				for eight in range(eights):
					self.player.get_card_from_blind(2)
				self.player.hand.cards_drawn.clear()
				self.activate_next_player()
			elif key == 'a':
				leap = 1
				while leap <= eights:
					if leap != self.number_of_players:
						self.player.get_card_from_blind(2)
						self.player.hand.cards_drawn.clear()
					else:
						eights += 1
					leap += 1
					self.activate_next_player()
		
		'''
		#Player/A	1	2	3	4

			2		1	3	1	3
			3		1	2	4	2
			4		1	2	3	5
			5		1	2	3	4
			6		1	2	3	4
		'''
		if aces > self.number_of_players:
			aces -= 2
		if aces == self.number_of_players:
			aces += 1
		for ace in range(aces):
			self.activate_next_player()
	
	def show_full_deck(self):
		print(f'\n{100 * "-"}')
		self.show_other_players(self.player)
		deck.show()
		self.player.show()
		print(
			'\n| TAB: toggle | SHIFT: put | ALT: draw | SPACE: next Player | (s)cores | (q)uit game |')
	
	def make_choice_for_J(self):
		if self.player.is_robot():
			jchoice.j = jchoice.js[random.randint(0, 3)]
		else:
			self.show_jcoice()
			while True:
				jkey = keyboard.read_hotkey(suppress=False)
				if jkey == 'tab':
					jchoice.toggle_js()
					deck.show()
					self.player.show()
					self.show_jcoice()
				if jkey == 'space':
					jchoice.set_j()
					break
	
	def show_jcoice(self):
		print(f'\n{20 * " "}\u2191\u2191')
		jchoice.show_js()
		print(f'{5 * " "}| TAB: toggle color | SPACE: set color / next player |')
	
	
	def show_other_players(self, player: Player):
		for p in self.player_list:
			if p != player:
				p.show_hand(visible=True)
	
	def finish_round(self):
		if deck.get_top_card_from_stack().rank == 'J':
			self.player.score -= 20 * len(deck.bridge_monitor) * deck.shufflings
		self.activate_next_player()  # evaluation of last round
		for player in self.player_list:
			player.score += player.hand.count_points() * deck.shufflings
			if player.score == 125:
				player.score = 0
			player.show_hand(visible=True)
		list = sorted(self.player_list, key=lambda player: player.name)
		try:
			f = open(f'{date.today()}_scores.txt')
		except IOError:
			f = open(f'{date.today()}_scores.txt', 'a')
			f.write(f'\n\nGame - Round   ')
			for player in list:
				f.write(f'{player.name} ')
			f.write('\n')
		finally:
			f.close()
			with open(f'{date.today()}_scores.txt', 'a') as f:
				f.write(
					f'  {self.number_of_games:2d} -{self.number_of_rounds:2d}{7 * " "}')
				for player in list:
					f.write("  {:3d}    ".format(player.score))
				f.write('\n')
		self.show_scores(wait_for_keyboard=False)
		self.set_shuffler()
		if self.shuffler.score <= 125:
			print(f'{15 * " "}{self.shuffler.name} will start next round\n')
			print(f'{22 * " "}| next (r)ound |\n')
			keyboard.wait('r')
			self.start_round()
		else:
			print(f'\nThe Winner is ...\n')
			print(f'{18 * " "}{min(self.player_list).name}\n')
			# winner = sorted(self.player_list, key=lambda player: player.score, reverse=True).pop()
			print(f'{27 * " "}+ + + G A M E  O V E R + + + \n')
			print(f'{34 * " "}| (n)ew game |\n')
			keyboard.wait('n')
			self.start_game()
			
	
	def show_scores(self, wait_for_keyboard=True):
		try:
			with open(f'{date.today()}_scores.txt') as f:
				print(f.read())
		except IOError:
			print(f'\n\nPlaying 1st round - No score list availabe yet\n')
		if wait_for_keyboard:
			print(f'{22 * " "}(r)eturn\n')
			keyboard.wait('r')
	
	def check_if_bridge(self):
		if len(deck.bridge_monitor) >= 4:
			print(f'\n{17 * " "}* * * B R I D G E * * *\n')
			
			if self.player.is_robot():
				key = random.choice(['n', 'y'])
				if key == 'n':
					print(f'{22 * " "}{self.player.name} said:')
					print(f"{17 * ' '}Let's continue this round")
					print(f'{24 * " "}| SPACE |\n')
					deck.bridge_monitor.clear()
					keyboard.wait('space')
					return False
				elif key == 'y':
					print(f'{22 * " "}{self.player.name} said:')
					print(f'{18 * " "}YES - count your points!')
					print(f'{24 * " "}| SPACE |\n')
					keyboard.wait('space')
					return True
			else:
				print(f'{24 * " "}| Y | N |\n')
				key = keyboard.read_hotkey(suppress=False)
			if key == 'n':
				deck.bridge_monitor.clear()
				return False
			if key == 'y':
				return True
		else:
			return False
	
	def is_next_player_possible(self):
		
		if self.check_if_bridge():
			self.finish_round()
			return False
		
		if deck.get_top_card_from_stack().rank == '6':
			return False
		
		if not self.player.hand.cards:
			self.finish_round()
			return False
		
		if deck.get_top_card_from_stack().rank == 'J':
			if self.player.hand.cards_played:
				self.make_choice_for_J()
				pass
		
		'''
		next player possible, (except 6 on stack) if:

			 card   possible  card    next
			played    card    drawn   player
				1       1       1       Y
				1       1       0       Y
				1       0       1       Y
				1       0       0       Y
				0       1       1       N
				0       1       0       N
				0       0       1       Y
				0       0       0       N       <-- must draw card
				
				                        N       <-- when '6'
		'''
		
		if self.player.hand.cards_played:
			return True
		
		elif not self.player.hand.cards_played:
			if not self.player.hand.possible_cards and self.player.hand.cards_drawn:
				return True
			else:
				return False
	
	def wait_for_keyboard(self):
		
		key = keyboard.read_hotkey(suppress=False)
		
		#Testing:
		if key == 'c':
			self.player.hand.cards.clear()
		if key == '6':
			for suit in suits:
				self.player.hand.cards.append(Card(suit, '6'))
		if key == '8':
			for suit in suits:
				self.player.hand.cards.append(Card(suit, '8'))
		if key == 'j':
			for suit in suits:
				self.player.hand.cards.append(Card(suit, 'J'))
		if key == 'a':
			for suit in suits:
				self.player.hand.cards.append(Card(suit, 'A'))
		#End Testing

		if key == 's':
			self.show_scores()

		if key == 'space':
			return key
	
	def play(self):
		
		self.start_game()
		
		while True:
			
			self.show_full_deck()
			
			if self.player.is_robot():
				
				while not self.is_next_player_possible():
					if self.player.hand.possible_cards:
						while self.player.hand.possible_cards:
							self.player.play_card()
							self.player.hand.get_possible_cards()
					else:
						self.player.get_card_from_blind()
						self.player.hand.get_possible_cards()
					self.show_full_deck()
				
				if self.wait_for_keyboard() == 'space':
					self.activate_next_player()
					continue
			
			key = keyboard.read_hotkey(suppress=False)
			
			if key == 'c':
				self.player.hand.cards.clear()
			if key == 't':
				self.start_round()
			if key == '6':
				for suit in suits:
					self.player.hand.cards.append(Card(suit, '6'))
			if key == '8':
				for suit in suits:
					self.player.hand.cards.append(Card(suit, '8'))
			if key == 'j':
				for suit in suits:
					self.player.hand.cards.append(Card(suit, 'J'))
			if key == 'a':
				for suit in suits:
					self.player.hand.cards.append(Card(suit, 'A'))
			if key == 'q':
				break
			elif key == 's':
				self.show_scores()
			elif key == 'tab':
				self.player.toggle_possible_cards()
			elif key == 'alt':
				self.player.must_draw_card()
			elif key == 'shift':
				self.player.play_card()
			elif key == 'space':
				if self.is_next_player_possible():
					self.activate_next_player()


if __name__ == "__main__":
	bridge = Bridge()
	bridge.play()
