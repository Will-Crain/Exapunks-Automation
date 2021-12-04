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