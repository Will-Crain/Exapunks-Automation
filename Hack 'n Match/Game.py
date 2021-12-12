from collections import deque

from Rank import Rank
from Tile import Tile

class Game():

	columns = 7

	def __init__(self, rank_data):
		self.ranks = rank_data

		self.move_stack = deque([])

	def get_moves(self):
		for rank in self.ranks:

			# Single J move

			# Single K move

			# K + J ?
			# J + K ?

	def get_score(self):
		score = 0

		# One point for every continuous tile
		for rank in self.ranks:
			pass
		# Five points for every tile in a chain of length 4 or more

		return score


	def get_adjacent_tiles(self, rank_idx, tile_idx):
		adjacent_tiles = []

		ref_rank = self.ranks[rank_idx]
		ref_tile = ref_rank.tiles[tile_idx]

		# Check right
		if rank_idx + 1 >= 0 and rank_idx + 1 < len(self.ranks):
			rank = self.ranks[rank_idx+1]
			if tile_idx < len(rank.tiles):
				tile = rank.tiles[tile_idx]

				if Tile.is_equal(ref_tile, tile):
					adjacent_tiles.append((rank_idx+1, tile_idx))
		
		# Check left
		if rank_idx - 1 >= 0 and rank_idx - 1 < len(self.ranks):
			rank = self.ranks[rank_idx-1]
			if tile_idx < len(rank.tiles):
				tile = rank.tiles[tile_idx]

				if Tile.is_equal(ref_tile, tile):
					adjacent_tiles.append((rank_idx-1, tile_idx))

		# Check up
		if tile_idx + 1 >= 0 and tile_idx + 1 < len(ref_rank):
			tile = ref_rank.tiles[tile_idx+1]
			if Tile.is_equal(ref_tile, tile):
				adjacent_tiles.append((rank_idx, tile_idx+1))

		# Check down
		if tile_idx - 1 >= 0 and tile_idx - 1 < len(ref_rank):
			tile = ref_rank.tiles[tile_idx-1]
			if Tile.is_equal(ref_tile, tile):
				adjacent_tiles.append((rank_idx, tile_idx-1))


		return adjacent_tiles

	def get_Chain(self, rank_idx, tile_idx):
		tile_type = self.ranks[rank_idx].tiles[tile_idx].type
		
		# breadth-first search of every adjacent tile
		to_check = deque([])
		chain = [(rank_idx, tile_idx)]

		adjacent = self.get_adjacent_tiles(rank_idx, tile_idx)
		to_check.extend(adjacent)
		chain.extend(adjacent)

		while len(to_check) > 0:
			r_idx, t_idx = to_check.popleft()
			new_adjacent = self.get_adjacent_tiles(r_idx, t_idx)

			for c in new_adjacent:
				if not c in chain:
					chain.append(c)
					new_adjacent.append(c)
		

		

		