import copy as copy
import time

suits = ['H', 'D', 'C', 'S']
red_suits = ['H', 'D']
black_suits = ['C', 'S']

faces = ['F']
suits = ['H', 'D', 'C', 'S']

numbs = ['0', '9', '8', '7', '6']
colrs = ['R', 'B']

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
		if self.get_suit() == 'R':
			return True

		return False

	def get_targets(self):
		targets = []

		if self.is_number():
			if self.get_value() == '0':
				return targets

			target_number = numbs[numbs.index(self.get_value())-1]

			if self.is_red():
				targets.append(target_number + 'B')
			else:
				targets.append(target_number + 'R')

			return targets

		if self.is_face():
			targets.append(self.get_value() + self.get_suit())

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
		self.hand = Rank(-1, [])

		self.move_stack = []
		self.winning_moves = []

		self.done = False
		self.iter = 0

	def get_hand(self):
		return self.hand
	def get_rank(self, id):
		return self.ranks[id]

	def get_rank_moves(self, ref_rank):
		moves = []

		if len(ref_rank.cards) == 0:
			return moves

		# Rank stack is the largest front stack in our rank, and we want the bottom card in that stack
		rank_stack = ref_rank.get_top_stack()
		rank_top_card = rank_stack[-1]
		rank_valid_moves = rank_top_card.get_targets()

		if len(rank_stack) == 1 and len(self.hand.cards) == 0 and len(ref_rank.cards) > 1:
			move = [
				self.hand,
				ref_rank,
				rank_stack
			]
			moves.append(move)
		
		# {rank destination_rank, rank origin_rank, array cards_to_move, card target_card}
		for rank in self.ranks:
			if len(rank.get_cards()) == 0:
				if not rank.get_rank() == ref_rank.get_rank() and len(rank_stack) < len(ref_rank.cards):
					move = [
						rank,
						ref_rank,
						rank_stack
					]

					moves.append(move)
				continue

			# Make sure we're not looking at the rank we're starting from
			if not rank.get_rank() == ref_rank.get_rank():
				top_card = rank.get_cards()[0]

				# Check if top card is a valid move for our stack
				if top_card.get_id() in rank_valid_moves:
					move = [
						rank,
						ref_rank,
						rank_stack
					]

					moves.append(move)

		return moves

	def is_victory(self):
		points = 0

		if len(self.hand.cards) > 0:
			return False
		

		for rank in self.ranks:
			rank_stack = rank.get_top_stack()

			# Check if completed face stack
			if len(rank_stack) == 4 and rank_stack[-1].is_face():
				points += 1
			
			# Check if completed number stack
			if len(rank_stack) == 5 and rank_stack[-1].is_number():
				points += 1

		if points == 8:
			return True
		
		return False
	def test_victory(self):
		points = 0

		if len(self.hand.cards) > 0:
			return False

		for rank in self.ranks:
			rank_stack = rank.get_top_stack()

			if len(rank_stack) == 2:
				points += 1
			
		if points == 2:
			return True

		return False

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
		new_move = copy.copy(move)

		dest_rank_id = move[0].get_rank()
		origin_rank_id = move[1].get_rank()

		# Check if going to hand
		if dest_rank_id == -1:
			self.hand.cards = move[2]

			for card in move[2]:
				self.ranks[origin_rank_id].remove_card(card.get_id())

		elif origin_rank_id == -1:
			self.ranks[dest_rank_id].cards.reverse()
			new_move[2].reverse()
			self.ranks[dest_rank_id].cards.extend(new_move[2])
			self.ranks[dest_rank_id].cards.reverse()

			for card in move[2]:
				self.hand.remove_card(card.get_id())
		
		else:
			self.ranks[dest_rank_id].cards.reverse()
			new_move[2].reverse()
			self.ranks[dest_rank_id].cards.extend(new_move[2])
			self.ranks[dest_rank_id].cards.reverse()

			for card in move[2]:
				self.ranks[origin_rank_id].remove_card(card.get_id())
		

	def iterate(self):
		new_move_stack = []
		
		for move_list in self.move_stack:
			new_game = Game(copy.deepcopy(self.ranks))
		
			for move in move_list:
				new_game.make_move(move)

			if new_game.test_victory():
				new_game.output()
				self.winning_moves.append(move_list)
			
			for rank in new_game.ranks:
				moves_to_add = new_game.get_rank_moves(rank)
				for move in moves_to_add:
					move_list_copy = copy.deepcopy(move_list)
					move_list_copy.append(move)
			
					new_move_stack.append(move_list_copy)
			
		self.move_stack = new_move_stack.copy()


	def solve(self):
		for rank in self.ranks:
			moves = self.get_rank_moves(rank)

			for move in moves:
				self.move_stack.append([move])

		while len(self.move_stack) > 0:
			self.iterate()
		
		print(len(self.winning_moves))

			
		
			

ranks = [
	Rank(0, [Card('7', 'B'), Card('8', 'B')]),
	Rank(1, [Card('7', 'R'), Card('8', 'R')])
]

# ranks = [
#     Rank(0, [Card('7', 'B'), Card('F', 'S'), Card('F', 'H'), Card('F', 'C')]),
#     Rank(1, [Card('8', 'B'), Card('7', 'B'), Card('F', 'D'), Card('F', 'S')]),
#     Rank(2, [Card('0', 'R'), Card('9', 'R'), Card('F', 'S'), Card('6', 'B')]),
#     Rank(3, [Card('F', 'H'), Card('9', 'B'), Card('8', 'R'), Card('7', 'R')]),
#     Rank(4, [Card('F', 'D'), Card('F', 'D'), Card('6', 'R'), Card('F', 'H')]),
#     Rank(5, [Card('8', 'B'), Card('0', 'R'), Card('8', 'R'), Card('7', 'R')]),
#     Rank(6, [Card('0', 'B'), Card('F', 'C'), Card('6', 'R'), Card('F', 'S')]),
#     Rank(7, [Card('9', 'R'), Card('9', 'B'), Card('F', 'D'), Card('F', 'H')]),
#     Rank(8, [Card('F', 'C'), Card('6', 'B'), Card('F', 'C'), Card('0', 'B')]),
# ]

a = Game(ranks.copy())

a.output()
solved_moves = a.solve()