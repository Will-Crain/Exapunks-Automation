from collections import deque
import copy as copy

import time
import sys

from Move import Move
from Rank import Rank
from Card import Card


class Game:
	def __init__(self, rank_info, hand=Rank(-1, [])):
		self.ranks = rank_info
		self.hand = hand

		self.move_stack = deque([])
		self.move_stack_len = 0

		self.winning_moves = []
		self.hashes = set(())

		self.done = False
		self.iter = 0

		self.check_hand = False

	def get_hand(self):
		return self.hand
	def get_rank(self, id):
		if id == -1:
			return self.hand
		
		return self.ranks[id]

	def get_ranks(self):
		rank_list = self.ranks.copy()
		if self.check_hand:
			rank_list.append(self.hand)

		return rank_list
	def get_rank_moves(self, ref_rank):
		moves = []
		hand_move = None

		if len(ref_rank.cards) == 0:
			return moves

		rank_stack = ref_rank.get_top_stack()
		rank_bot_card = rank_stack[0]
		rank_valid_moves = rank_bot_card.get_targets()

		ref_rank_len = len(ref_rank.cards)
		rank_stack_len = len(rank_stack)

		for rank in self.get_ranks():

			rank_len = len(rank.cards)

			# Can't move into own rank
			if rank.rank == ref_rank.rank:
				continue
			# Don't check empty ranks
			if ref_rank_len == 0:
				continue

			move = Move(rank.rank, ref_rank.rank, rank_stack)

			if rank_len == 0:
				if ref_rank.rank == -1:
					moves.append(move)
				elif rank.rank == -1:
					if rank_stack_len == 1:
						hand_move = move
				else:
					if rank_stack_len < ref_rank_len:
						moves.append(move)
			elif rank_len > 0:
				top_card = rank.cards[-1]

				if ref_rank.rank == -1:
					if top_card.id in rank_valid_moves:
						moves.append(move)
				elif rank.rank == -1:
					continue
				else:
					if top_card.id in rank_valid_moves:
						moves.append(move)

		# If we can move a card somewhere /and/ the hand, discard the hand move
		if len(moves) == 0 and hand_move:
			moves.append(hand_move)

		return moves

	def hash(self):
		hashes = []

		for rank in self.get_ranks():
			hashes.append('%s/' % rank.hash())

		hashes.sort()
		out_str = ''.join(hashes)

		return out_str

	def is_victory(self):
		points = 0

		if len(self.hand.cards) > 0:
			return False
		

		for rank in self.ranks:
			rank_stack = rank.get_top_stack()

			rank_len = len(rank.cards)

			if len(rank_stack) < rank_len:
				return False
			
			if rank_len == 0:
				points += 1
			elif rank_len == 4:
				if rank.cards[0].is_face():
					points += 1
			elif rank_len == 5:
				if rank.cards[0].is_number():
					points += 1

		if points == 9:
			return True
		
		return False

	def hash_exists(self, hash):
		return hash in self.hashes
	
	def output(self):
		out_arr = []

		ranks_copy = copy.copy(self.ranks)
		most_cards = 0
		for rank in ranks_copy:
			if len(rank.cards) > most_cards:
				most_cards = len(rank.cards)
		
		for _ in range(most_cards):
			out_arr.append([])

		for rank in ranks_copy:
			for card_idx in range(most_cards):
				if len(rank.cards) > card_idx:
					out_arr[card_idx].append(rank.cards[card_idx].id + ' ')
				else:
					out_arr[card_idx].append('   ')
		
		# out_arr.reverse()
		out_str = ''
		for arr in out_arr:
			out_str += '\n'

			for card in arr:
				out_str += card + ' '

		out_str += '\n'
		print(out_str)

	def make_copy(self):
		new_rank_array = []
		new_hand = Rank(-1, self.hand.cards.copy())

		for rank in self.ranks:
			new_card_array = rank.cards.copy()
			new_rank_array.append(Rank(rank.rank, new_card_array))
		
		return Game(new_rank_array, new_hand)

	def do_extend(self, rank, stack):
		for card in stack:
			rank.cards.append(card)
	def do_pop(self, rank, iter):
		for _ in range(iter):
			rank.cards.pop()

	def make_move(self, move):
		from_rank = self.get_rank(move.from_rank_id)
		dest_rank = self.get_rank(move.dest_rank_id)

		self.do_extend(dest_rank, move.stack)
		self.do_pop(from_rank, len(move.stack))
				
	def iterate(self):
		move_list = self.move_stack.popleft()
		self.move_stack_len -= 1
		new_game = self.make_copy()
	
		for move in move_list:
			new_game.make_move(move)

		if new_game.is_victory():
			self.winning_moves.append(move_list)
			return
		
		hash = new_game.hash()
		if self.hash_exists(hash):
			return

		self.hashes.add(hash)

		for rank in new_game.get_ranks():
			moves_to_add = new_game.get_rank_moves(rank)
			for move in moves_to_add:
				move_list_copy = copy.copy(move_list)
				move_list_copy.append(move)
		
				self.move_stack.append(move_list_copy)
				self.move_stack_len += 1

	def solve(self, with_hand=False):
		self.check_hand = with_hand

		for rank in self.get_ranks():
			moves = self.get_rank_moves(rank)
			for move in moves:
				self.move_stack.append([move])
				self.move_stack_len += 1

		self.hashes.add(self.hash())

		iter = 0
		time_start = time.time_ns()-10

		debug = False

		while self.move_stack:
			self.iterate()

			if debug:
				now_time = time.time_ns()
				time_since = now_time - time_start

				mean_time = iter/time_since*1e3

				out_str = '\r'
				out_str += str(iter) + ' iterations\t\t'
				out_str += str(self.move_stack_len) + ' items\t\t'
				out_str += str(round(time_since/1e9)) + 's\t\t'
				out_str += str(round(mean_time/1e3, 0)) + 'us\t\t'

				sys.stdout.write(out_str)
				sys.stdout.flush()

				iter += 1

		if len(self.winning_moves) > 0:
			return self.winning_moves[0]
		else:
			return None


# ranks = [
# 	Rank(0, [Card('7', 'R'), Card('F', 'C'), Card('F', 'C'), Card('F', 'C')]),
# 	Rank(1, [Card('8', 'B'), Card('0', 'B'), Card('F', 'D'), Card('F', 'D')]),
# 	Rank(2, [Card('F', 'S'), Card('9', 'R'), Card('6', 'R'), Card('7', 'B')]),
# 	Rank(3, [Card('6', 'B'), Card('9', 'R'), Card('F', 'H'), Card('6', 'R')]),
# 	Rank(4, [Card('9', 'B'), Card('F', 'S'), Card('F', 'S'), Card('F', 'H')]),
# 	Rank(5, [Card('7', 'B'), Card('0', 'R'), Card('F', 'S'), Card('F', 'D')]),
# 	Rank(6, [Card('F', 'C'), Card('9', 'B'), Card('F', 'D'), Card('F', 'H')]),
# 	Rank(7, [Card('7', 'R'), Card('F', 'H'), Card('0', 'B'), Card('6', 'B')]),
# 	Rank(8, [Card('8', 'B'), Card('8', 'R'), Card('0', 'R'), Card('8', 'R')])
# ]	############

