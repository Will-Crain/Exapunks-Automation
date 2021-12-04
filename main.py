import copy as copy

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
	def __init__(self, rank_info, hand=Rank(-1, []), move_list = []):
		self.ranks = rank_info
		self.hand = hand
		self.state_stack = []
		self.prev_moves = move_list
		self.winning_moves = []

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
				if len(rank.cards) == 0 and (len(rank_stack) < len(ref_rank.cards)):
					move = [
						rank,
						ref_rank,
						rank_stack
					]
					moves.append(move)

		return moves

	def is_victory(self):
		points = 0

		for rank in self.ranks:
			rank_stack = rank.get_top_stack()

			# Check if completed face stack
			if len(rank_stack) == 4 and rank_stack[-1].get_suit() in suits:
				points += 1
			
			# Check if completed number stack
			if len(rank_stack) == 5 and rank_stack[-1].get_value() == 0:
				points += 1
			
		# Check if hand is empty
		if len(self.hand.cards) > 0:
			return False

		if points == 8:
			return True
		
		return False

	def test_victory(self):
		points = 0

		if len(self.hand.cards) > 0:
			return False

		for rank in self.ranks:
			rank_stack = rank.get_top_stack()

			if len(rank_stack) == 3:
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
		prev_move_list = copy.deepcopy(self.prev_moves)
		prev_move_list.append(copy.deepcopy(move))

		new_game = Game(copy.deepcopy(self.ranks), copy.deepcopy(self.hand), prev_move_list)
		new_move = copy.deepcopy(move)
		new_ranks = copy.deepcopy(self.ranks)

		dest_rank_id = move[0].get_rank()
		origin_rank_id = move[1].get_rank()

		# Check if going to hand
		if dest_rank_id == -1:
			new_game.hand.cards.extend(move[2])

			for card in move[2]:
				new_game.ranks[origin_rank_id].remove_card(card.get_id())

		elif origin_rank_id == -1:
			new_game.ranks[dest_rank_id].cards.reverse()
			new_move[2].reverse()
			new_game.ranks[dest_rank_id].cards.extend(new_move[2])
			new_game.ranks[dest_rank_id].cards.reverse()

			for card in move[2]:
				new_game.hand.remove_card(card.get_id())
		
		else:
			new_ranks[dest_rank_id].cards.reverse()
			new_move[2].reverse()
			new_ranks[dest_rank_id].cards.extend(new_move[2])
			new_ranks[dest_rank_id].cards.reverse()

			new_game.ranks[dest_rank_id] = new_ranks[dest_rank_id]

			for card in move[2]:
				new_ranks[origin_rank_id].remove_card(card.get_id())
			
			new_game.ranks[origin_rank_id] = new_ranks[origin_rank_id]

		return new_game

	def generate_state_stack(self):
		for rank in self.ranks:
			moves = self.get_rank_moves(rank)
			if len(moves) == 0:
				continue
				
			for move in moves:
				new_game = self.make_move(move)
				self.state_stack.append(new_game)
		
		hand_moves = self.get_rank_moves(self.hand)
		for move in hand_moves:
			new_game = self.make_move(move)
			self.state_stack.append(new_game)

	def solve(self):
		if self.test_victory():
			self.output()

			out_str = ''
			for move in self.prev_moves:
				out_str += str(move[1].get_rank()) + ' -> ' + str(move[0].get_rank()) + '\n'

			print(out_str)

			return self.prev_moves

		else:
			self.generate_state_stack()

			for state in self.state_stack:
				win_moves = state.solve()

				if len(win_moves) > 0:
					return win_moves
			
			return []

ranks = [
	Rank(0, [Card('F', 'H'), Card('F', 'C')]),
	Rank(1, [Card('F', 'C'), Card('F', 'H')]),
	Rank(2, [Card('F', 'H'), Card('F', 'C')])
]

a = Game(ranks.copy())

a.output()
solved_moves = a.solve()

# out_str = ''
# for i, move in enumerate(solved_moves):
# 	out_str += str(i) + '\t' + str(move[1].get_rank()) + ' -> ' + str(move[0].get_rank()) + '\n'
# print(out_str)