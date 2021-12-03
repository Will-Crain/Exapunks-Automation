import PIL
import copy as copy

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
				targets.append(target_number + suit)

			return targets

		if self.is_face():
			for face in faces:
				if not face == self.get_value():
					targets.append(face + self.get_suit())

			return targets

class Rank:
	def __init__(self, rank, cards):
		self.rank = rank
		self.cards = cards

	def get_rank(self):
		return self.rank
	def get_cards(self):
		return self.cards
	def get_card_ids(self):
		out_arr = []
		for card in self.cards:
			out_arr.append(card.get_id())
		
		return out_arr

	def remove_card(self, card_id):
		for card in self.cards:
			if card.get_id() == card_id:
				self.cards.remove(card)

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
		self.state_stack = []

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
			if len(rank.get_cards()) == 0:
				continue
			# Make sure we're not looking at the rank we're starting from
			if not rank.get_rank() == ref_rank.get_rank():
				top_card = rank.get_cards()[0]

				# Check if top card is a valid move for our stack
				if top_card.get_id() in rank_valid_moves:
					# {rank destination_rank, rank origin_rank, array cards_to_move, card target_card}
					move = [
						rank,
						ref_rank,
						rank_stack,
						top_card
					]
					moves.append(move)

		return moves

	def output(self):
		out_arr = []

		ranks_copy = copy.deepcopy(self.ranks)
		most_cards = 0
		for rank in ranks_copy:
			if len(rank.cards) > most_cards:
				most_cards = len(rank.cards)
		
		for num_cards in range(most_cards):
			out_arr.append([])

		for rank in ranks_copy:
			# to_append = []
			# rank.cards.reverse()

			for card_idx in range(most_cards):
				if len(rank.cards) > card_idx:
					out_arr[card_idx].append(rank.cards[card_idx].get_id() + ' ')
				else:
					out_arr[card_idx].append('   ')
		
		out_arr.reverse()
		out_str = ''
		for arr in out_arr:
			out_str += '\n'

			for card in arr:
				out_str += card + ' '

		out_str += '\n'
		print(out_str)

	def make_move(self, move):
		new_game = Game(copy.deepcopy(self.ranks))
		new_move = move.copy()

		dest_rank_id = move[0].get_rank()
		origin_rank_id = move[1].get_rank()

		new_game.ranks[dest_rank_id].cards.reverse()
		new_move[2].reverse()
		new_game.ranks[dest_rank_id].cards.extend(move[2])
		new_game.ranks[dest_rank_id].cards.reverse()

		for card in move[2]:
			new_game.ranks[origin_rank_id].remove_card(card.get_id())

		return new_game

	def solve(self):
		# Get all possible moves
		for rank in self.ranks:
			moves = self.get_rank_moves(rank)

			# Generate new gamestates and send them to the stack
			for move in moves:
				new_game = self.make_move(move)
				self.state_stack.append(new_game)


ranks = [
	Rank(0, [Card('8', 'S'), Card('9', 'S')]),
	Rank(1, [Card('6', 'S'), Card('7', 'H'), Card('9', 'H')]),
	Rank(2, [Card('9', 'H')]),
	Rank(3, [Card('Q', 'H'), Card('K', 'H')]),
	Rank(4, [Card('A', 'H'), Card('A', 'D'), Card('K', 'C')])
]

a = Game(ranks.copy())

a.solve()
print('\n\nORIGINAL')
a.output()
print('MOVES BELOW')
for state in a.state_stack:
	state.output()

print(a.get_rank_moves(a.ranks[3]))

# 1. Generate list of gamestates from each possible move
# 2. For each gamestate, repeat #1
# 3. If a gamestate's possible future gamestate list is empty, check if we've won
# 4a. If we've won, return the list of moves responsible for getting us there and iterate over them backwards
# 4b. If we haven't won, return and toss self out of parent (or have parent check if we're empty and losers?)
