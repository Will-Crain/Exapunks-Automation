
numbs = ['0', '9', '8', '7', '6']
numb_lookup = {
	'9':	'0',
	'8':	'9',
	'7':	'8',
	'6':	'7'
}
colrs = ['R', 'B']

faces = ['F']
suits = ['H', 'D', 'C', 'S']


class Card:
	def __init__(self, value, suit):
		self.suit = suit
		self.value = value
		self.id = value + suit

	def is_face(self):
		if self.value == 'F':
			return True

		return False
	def is_number(self):
		if not self.value == 'F':
			return True

		return False
	def is_red(self):
		if self.suit == 'R':
			return True

		return False

	def get_targets(self):
		targets = []

		if self.is_number():
			if self.value == '0':
				return []

			target_number = numb_lookup[self.value]

			if self.is_red():
				targets.append(target_number + 'B')
			else:
				targets.append(target_number + 'R')

			return targets

		else:
			targets.append(self.value + self.suit)

		return targets