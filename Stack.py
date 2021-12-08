class Stack:

	numb_lookup = {
		'0':	None,
		'9':	'0',
		'8':	'9',
		'7':	'8',
		'6':	'7'
	}
	value_lookup = {
		'0': 10,
		'9': 9,
		'8': 8,
		'7': 7,
		'6': 6,
	}
	suit_swap = {
		'R': 'B',
		'B': 'R'
	}

	@staticmethod
	def get_combine(from_stack, to_stack):
		if from_stack.is_faces and to_stack.is_faces:
			suit_match = from_stack.back.suit == to_stack.front.suit
			if suit_match:
				new_stack = Stack(to_stack.back, from_stack.front, to_stack.length + from_stack.length)
				return new_stack

			return None

		elif not from_stack.is_faces and not to_stack.is_faces:
			value_match = Stack.numb_lookup[from_stack.back.value] == to_stack.front.value
			suit_match = not from_stack.back.suit == to_stack.front.suit

			if value_match and suit_match:
				new_stack = Stack(to_stack.back, from_stack.front, to_stack.length + from_stack.length)
				return new_stack
		
			return None

		else:
			return None

	@staticmethod
	def from_cards(cards):
		stacks = []

		# Create size 1 Stacks for every card
		for card in cards:
			stacks.append(Stack(card, card, 1))
		
		# Combine stacks now
		complete = False
		curr_idx = 0
		while not complete:
			if len(stacks) == 1:
				complete = True
				break
				
			if curr_idx >= len(stacks)-1:
				complete = True
				break

			can_combine = Stack.get_combine(stacks[curr_idx+1], stacks[curr_idx])
			if can_combine:
				stacks[curr_idx] = can_combine
				stacks.pop(curr_idx+1)
			else:
				curr_idx += 1

		return stacks

	def __init__(self, back, front, length):
		self.back = back
		self.front = front
		self.length = length

		self.is_faces = self.back.value == 'F'
	def __str__(self):
		return str(self.back) + ':' + str(self.front)

	def make_copy(self):
		return Stack(self.back, self.front, self.length)

	def get_output(self):
		out_arr = []
		for i in self.length:
			diff = int(self.back.value) - i
			suit = self.back.suit
			if diff%2 == 1:
				suit = self.suit_swap[suit]

			out_arr.push(str(diff) + suit)

		return out_arr
	def hash(self):
		return str(self)
