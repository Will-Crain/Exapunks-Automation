
numbs = ['0', '9', '8', '7', '6']
colrs = ['R', 'B']

faces = ['F']
suits = ['H', 'D', 'C', 'S']


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