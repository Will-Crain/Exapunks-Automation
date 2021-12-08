class Card:
	
	numb_lookup = {
		'9':	'0',
		'8':	'9',
		'7':	'8',
		'6':	'7'
	}


	def __init__(self, value, suit):
		self.suit = suit
		self.value = value
		self.id = value + suit
	def __str__(self):
		return self.id

	def is_face(self):
		return self.value == 'F'
	def is_number(self):
		return not self.value == 'F'
	def is_red(self):
		return self.suit == 'R'
	# def get_targets(self):
	# 	targets = []

	# 	if self.is_number():
	# 		if self.value == '0':
	# 			return []

	# 		target_number = self.numb_lookup[self.value]

	# 		if self.is_red():
	# 			targets.append(target_number + 'B')
	# 		else:
	# 			targets.append(target_number + 'R')

	# 		return targets

	# 	else:
	# 		targets.append(self.value + self.suit)

	# 	return targets