import copy as copy

from Card import Card
from Move import Move
from Rank import Rank

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
			moves.append(Move(self.hand, ref_rank, rank_stack))
		
		# {rank destination_rank, rank origin_rank, array cards_to_move, card target_card}
		for rank in self.ranks:
			if len(rank.get_cards()) == 0:
				if not rank.get_rank() == ref_rank.get_rank() and len(rank_stack) < len(ref_rank.cards):
					moves.append(Move(rank, ref_rank, rank_stack))
					
				continue

			# Make sure we're not looking at the rank we're starting from
			if not rank.get_rank() == ref_rank.get_rank():
				top_card = rank.get_cards()[0]

				# Check if top card is a valid move for our stack
				if top_card.get_id() in rank_valid_moves:
					moves.append(Move(rank, ref_rank, rank_stack))

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

		dest_rank_id = move.dest_rank.get_rank()
		from_rank_id = move.from_rank.get_rank()

		# Check if going to hand
		if dest_rank_id == -1:
			self.hand.cards = move.stack

			for card in move.stack:
				self.ranks[from_rank_id].remove_card(card.get_id())

		elif from_rank_id == -1:
			self.ranks[dest_rank_id].cards.reverse()
			new_move.stack.reverse()
			self.ranks[dest_rank_id].cards.extend(new_move.stack)
			self.ranks[dest_rank_id].cards.reverse()

			for card in move.stack:
				self.hand.remove_card(card.get_id())
		
		else:
			self.ranks[dest_rank_id].cards.reverse()
			new_move.stack.reverse()
			self.ranks[dest_rank_id].cards.extend(new_move.stack)
			self.ranks[dest_rank_id].cards.reverse()

			for card in move.stack:
				self.ranks[from_rank_id].remove_card(card.get_id())
		

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
		if len(self.move_stack) > 0:
			self.iterate()

	def solve(self):
		for rank in self.ranks:
			moves = self.get_rank_moves(rank)

			for move in moves:
				self.move_stack.append([move])

		self.iterate()
		
		print(len(self.winning_moves))

			
		
			

ranks = [
	Rank(0, [Card('7', 'R'), Card('7', 'B'), Card('8', 'B')]),
	Rank(1, [Card('8', 'R')])
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