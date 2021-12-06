from collections import deque

class Rank:
	def __init__(self, rank, cards):
		self.rank = rank
		self.cards = deque(cards)

	def get_card_ids(self):
		out_arr = []
		for card in self.cards:
			out_arr.append(card.id)
		
		return out_arr

	def remove_card(self, card):
		self.cards.remove(card)

	def get_top_stack(self):
		stack = []

		if len(self.cards) == 0:
			return stack
		
		stack = []
		for card in reversed(self.cards):
			if len(stack) == 0:
				stack.append(card)
			else:
				if card.id in stack[-1].get_targets():
					stack.append(card)
				else:
					break

		stack.reverse()
		return stack

	def hash(self):
		out_str = ''
		if self.rank == -1:
			out_str += 'HAND_'
		else:
			out_str += 'COL_'
		out_str += ''.join(self.get_card_ids())

		return out_str