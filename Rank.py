class Rank:
	def __init__(self, rank, stacks):
		self.rank = rank
		self.stacks = stacks

	def remove_top_stack(self):
		self.stacks.pop(-1)
	def get_top_stack(self):
		return self.stacks[-1]
	def get_output(self):
		out_arr = []
		for stack in self.stacks:
			out_arr.push(stack.get_output())
			
		return out_arr
	
	def make_copy(self):
		new_stacks = []
		
		for stack in self.stacks:
			new_stacks.append(stack.make_copy())
		
		return Rank(self.rank, new_stacks)

	def get_total_cards(self):
		cards = 0
		for stack in self.stacks:
			cards += stack.length

		return cards
	def hash(self):
		out_str = ''
		if self.rank == -1:
			out_str += 'HAND_'
		else:
			out_str += 'COL_'
		
		for stack in self.stacks:
			out_str += stack.hash()

		return out_str