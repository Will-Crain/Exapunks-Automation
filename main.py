from Game import Game
from Card import Card
from Rank import Rank


ranks = [
	Rank(0, [Card('7', 'R'), Card('F', 'C'), Card('F', 'C'), Card('F', 'C')]),
	Rank(1, [Card('8', 'B'), Card('0', 'B'), Card('F', 'D'), Card('F', 'D')]),
	Rank(2, [Card('F', 'S'), Card('9', 'R'), Card('6', 'R'), Card('7', 'B')]),
	Rank(3, [Card('6', 'B'), Card('9', 'R'), Card('F', 'H'), Card('6', 'R')]),
	Rank(4, [Card('9', 'B'), Card('F', 'S'), Card('F', 'S'), Card('F', 'H')]),
	Rank(5, [Card('7', 'B'), Card('0', 'R'), Card('F', 'S'), Card('F', 'D')]),
	Rank(6, [Card('F', 'C'), Card('9', 'B'), Card('F', 'D'), Card('F', 'H')]),
	Rank(7, [Card('7', 'R'), Card('F', 'H'), Card('0', 'B'), Card('6', 'B')]),
	Rank(8, [Card('8', 'B'), Card('8', 'R'), Card('0', 'R'), Card('8', 'R')])
]	############



a = Game(ranks.copy())

a.output()
a.solve()