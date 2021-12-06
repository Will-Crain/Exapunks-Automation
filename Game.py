import copy as copy
import time

from Move import Move
from Rank import Rank

class Game:
	def __init__(self, rank_info, hand=Rank(-1, [])):
		self.ranks = rank_info
		self.hand = hand

		self.move_stack = []
		self.winning_moves = []
		self.hashes = set(())

		self.done = False
		self.iter = 0

	def get_hand(self):
		return self.hand
	def get_rank(self, id):
		if id == -1:
			return self.hand
		
		return self.ranks[id]

	def get_ranks(self):
		rank_list = self.ranks.copy()
		rank_list.append(self.hand)

		return rank_list
	def get_rank_moves(self, ref_rank):
		moves = []

		if len(ref_rank.cards) == 0:
			return moves

		rank_stack = ref_rank.get_top_stack()
		rank_bot_card = rank_stack[0]
		rank_valid_moves = rank_bot_card.get_targets()

		for rank in self.get_ranks():

			# Can't move into own rank
			if rank.rank == ref_rank.rank:
				continue
			# Don't check empty ranks
			if len(ref_rank.cards) == 0:
				continue

			move = Move(rank.rank, ref_rank.rank, rank_stack)

			if len(rank.cards) == 0:
				if ref_rank.rank == -1:
					# move.output()
					moves.append(move)
				elif rank.rank == -1:
					if len(rank_stack) == 1:
						# move.output()
						moves.append(move)
				else:
					if len(rank_stack) < len(ref_rank.cards):
						# move.output()
						moves.append(move)
			elif len(rank.cards) > 0:
				top_card = rank.cards[-1]

				if ref_rank.rank == -1:
					if top_card.id in rank_valid_moves:
						# move.output()
						moves.append(move)
				elif rank.rank == -1:
					continue
				else:
					if top_card.id in rank_valid_moves:
						# move.output()
						moves.append(move)
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

			if len(rank_stack) < len(rank.cards):
				return False
			
			if len(rank.cards) == 0:
				points += 1
			elif len(rank.cards) == 4:
				if rank.cards[0].is_face():
					points += 1
			elif len(rank.cards) == 5:
				if rank.cards[0].is_number():
					points += 1

		if points == 9:
			return True
		
		return False
	def test_victory(self):
		if len(self.hand.cards) > 0:
			return False

		points = 0

		for rank in self.ranks:
			rank_stack = rank.get_top_stack()

			if len(rank.cards) == 0:
				points += 1
			elif len(rank.cards) == len(rank_stack):
				points += 1
			
		if points == len(self.ranks):
			return True

		return False

	def hash_exists(self, hash):
		if hash in self.hashes:
			return True

		return False
	
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
	def make_move(self, move):
		self.get_rank(move.dest_rank_id).cards.extend(move.stack)

		for _ in range(len(move.stack)):
			self.get_rank(move.from_rank_id).cards.pop()
				
	def iterate(self):
		new_move_stack = []
		
		for move_list in self.move_stack:
			new_game = self.make_copy()
		
			for move in move_list:
				new_game.make_move(move)


			if new_game.test_victory():
				# new_game.output()
				self.winning_moves.append(move_list)
			
			hash = new_game.hash()
			if self.hash_exists(hash):
				continue

			self.hashes.add(hash)

			for rank in new_game.get_ranks():
				moves_to_add = new_game.get_rank_moves(rank)
				for move in moves_to_add:
					move_list_copy = copy.copy(move_list)
					move_list_copy.append(move)
			
					new_move_stack.append(move_list_copy)

		del self.move_stack
		self.move_stack = new_move_stack.copy()

	def solve(self):
		for rank in self.get_ranks():
			moves = self.get_rank_moves(rank)
			for move in moves:
				self.move_stack.append([move])

		self.hashes.add(self.hash())

		iter = 1
		while len(self.move_stack) > 0:
			prev_time = time.time_ns()/1000
			self.iterate()

			new_time = time.time_ns()/1000
			new_size = len(self.move_stack)
			new_now = time.localtime()

			if new_size > 0:
				out_str = str(iter) + '\t'
				out_str += str(new_size)
				out_str += ' in '
				out_str += str(round((new_time-prev_time)/1000/1000, 2))
				out_str += 's\t('
				out_str += str(round((new_time-prev_time)/new_size, 3))
				out_str += 'ms per operation)\t'
				out_str += str(new_now.tm_hour) + ':' + str(new_now.tm_min) + '.' + str(new_now.tm_sec)

				iter += 1

				print(out_str)

		print('WINNING MOVES: %s' % len(self.winning_moves))
		if len(self.winning_moves) > 0:
			for move in self.winning_moves[0]:
				move.output()
