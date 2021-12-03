import PIL

suits = ['H', 'D', 'C', 'S']
red_suits = ['H', 'D']
black_suits = ['C', 'S']

faces = ['K', 'Q', 'J', 'A']
numbs = ['0', '9', '8', '7', '6']
cards = ['K', 'Q', 'J', 'A', '0', '9', '8', '7', '6']

class Card:
	def __init__(self, value, suit):
		self.suit = suit
		self.value = value
		self.id = value + suit

	def get_suit(self):
		return self.suit
	def get_value(self):
		return self.value
	def get_id(self):
		return self.id

	def is_face(self):
		if self.value in faces:
			return True

		return False
	def is_number(self):
		if self.value in numbs:
			return True

		return False
	def is_red(self):
		if self.get_suit() == 'H' or self.get_suit() == 'D':
			return True

		return False

	def get_targets(self):
		targets = []

		if self.is_number():
			if self.get_value() == '0':
				return targets

			suits_to_iterate = []
			target_number = numbs[numbs.index(self.get_value())-1]

			if self.is_red():
				suits_to_iterate = black_suits
			else:
				suits_to_iterate = red_suits

			for suit in suits_to_iterate:
				targets.append(suit + target_number)

			return targets

		if self.is_face():
			for face in faces:
				if not face == self.get_value():
					targets.append(self.get_suit() + face)

			return targets

class Rank:
	def __init__(self, rank, cards):
		self.rank = rank
		self.cards = cards

	def get_rank(self):
		return self.rank
	def get_cards(self):
		return self.cards

	def get_top_stack(self):
		stack = []
		for card in self.get_cards():
			if len(stack) == 0:
				stack.append(card)
				continue

			if card.get_id() in stack[-1].get_targets():
				stack.append(card)
				continue

			break

		return stack


class Game:
	def __init__(self, rank_info):
		self.ranks = rank_info
		self.hand = []

	def get_hand(self):
		return self.hand

	def get_rank(self, id):
		return self.ranks[id]

	def get_rank_moves(self, ref_rank):
		moves = []

		# Rank stack is the largest front stack in our rank, and we want the bottom card in that stack
		rank_stack = ref_rank.get_top_stack()
		rank_top_card = rank_stack[-1]
		rank_valid_moves = rank_top_card.get_targets()

		for rank in self.ranks:
			# Make sure we're not looking at the rank we're starting from
			if not rank.get_rank() == ref_rank.get_rank():
				top_card = rank.get_cards()[0]

				# Check if top card is a valid move for our stack
				if top_card.get_id() in rank_valid_moves:
					moves.append([rank.get_rank(), top_card.get_id(), rank_top_card.get_id()])

		return moves

	def output(self):
		outArr = []

		for rank_idx, rank in enumerate(self.ranks):
			outArr.append([])

			for card_idx, card in enumerate(rank.get_cards()):

				outArr[rank_idx].append(card.get_id())

		outStr = ''
		for card in range(len(outArr[0])):
			card_idx = len(outArr[0]) - card - 1
			outStr += '\n'

			for rank in outArr:
				outStr += rank[card_idx] + ' ' 

		print(outStr)


ranks = [
	Rank(0, [Card('0', 'H'), Card('9', 'S'), Card('A', 'S'), Card('J', 'C')]),
	Rank(1, [Card('7', 'S'), Card('8', 'H'), Card('9', 'S'), Card('0', 'C')]),
	]

a = Game(ranks)
a.output()
b = a.get_rank(1)
c = a.get_rank_moves(b)
print(c)
# print(len(b.get_top_stack()))