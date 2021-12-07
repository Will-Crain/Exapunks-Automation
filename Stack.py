from Card import Card

class Stack:

	numb_lookup = {
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

	@classmethod
	def get_combine(from_stack, to_stack):
		if from_stack.is_faces and to_stack.is_faces:
			suit_match = from_stack.back.suit == to_stack.front.suit
			if suit_match:
				return Stack(to_stack.back, from_stack.front)

			return None

		elif not from_stack.is_faces and not to_stack.is_faces:
			value_match = Stack.numb_lookup[from_stack.back.value] == to_stack.front.value
			suit_match = not from_stack.back.suit == to_stack.front.suit

			if value_match and suit_match:
				return Stack(to_stack.back, from_stack.front)
		
			return None

		else:
			return None

	def __init__(self, back, front):
		self.back = back
		self.front = front

		self.is_faces = self.back.value == 'F'

		# self.len = self.value_lookup(self.back.value) - self.value_lookup(self.front.value) + 1
		
# Win condition is if every rank has either 0 or 1 stacks?