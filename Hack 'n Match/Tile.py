import enum

class TileTypes(enum):
	R_ = 0
	B_ = 1
	Y_ = 2
	P_ = 3
	T_ = 4

	RB = 5
	BB = 6
	YB = 7
	PB = 8
	TB = 9


class Tile():
	def __init__(self, type):
		self.type = type