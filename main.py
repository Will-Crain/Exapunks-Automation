from PIL import ImageGrab, Image, ImageChops, ImageStat

import os
import pyautogui
import time

import cProfile as profiler

from Game import Game
from Card import Card
from Rank import Rank

CARD_IMAGES = r'res/'

class Board():

	default_delay = 0.1

	square_size = 15
	vertical_spacing_with_square = 15
	horizontal_spacing_with_square = 119

	vertical_spacing = vertical_spacing_with_square + square_size
	horizontal_spacing = horizontal_spacing_with_square + square_size

	left_offset = 369
	top_offset = 465

	card_width = 112
	card_height = 15

	hand_x = 1430
	hand_y = 245

	newgame_x = 1400
	newgame_y = 900

	values = ['H', '0', '9', '8', '7', '6']
	suits = ['H', 'D', 'C', 'S', 'R', 'B']


	def __init__(self):
		self.starting_rows = 4
		self.starting_cols = 9

		self.game = None

		self.bounding_box_list = []
		for c in range(self.starting_cols):
			self.bounding_box_list.append([])
			for r in range(self.starting_rows):
				new_bounding_box = (
					self.left_offset + self.horizontal_spacing*c, 
					self.top_offset + self.vertical_spacing*r, 
					self.left_offset + self.horizontal_spacing*c + self.square_size, 
					self.top_offset + self.vertical_spacing*r + self.square_size
				)
				self.bounding_box_list[c].append(new_bounding_box)

	def get_card(self, capture):
		dir = os.listdir(CARD_IMAGES)

		for image_os in dir:
			image_name = os.fsdecode(image_os)
			image = Image.open(CARD_IMAGES + image_os).convert('RGB')

			if list(image.getdata()) == list(capture.getdata()):
				card_value = image_name[0]
				card_suit = image_name[1]

				return Card(card_value, card_suit)

	def make_game(self):
		rank_cards = []
		for rank_idx in range(len(self.bounding_box_list)):
			rank_cards.append([])

			for card_box in self.bounding_box_list[rank_idx]:
				capture = ImageGrab.grab(card_box).convert('RGB')
				card = self.get_card(capture)
				rank_cards[rank_idx].append(card)

		for rank_idx in range(len(rank_cards)):
			rank = rank_cards[rank_idx]

			for card_idx in range(len(rank)):
				card = rank[card_idx]

		ranks = []
		for cards_idx in range(len(rank_cards)):
			ranks.append(Rank(cards_idx, rank_cards[cards_idx]))
		
		self.game = Game(ranks)
		return self.game

	def execute_move_list(self, move_list):

		# Tab into window
		pyautogui.mouseDown(200, 200, button='left')
		time.sleep(0.6)
		pyautogui.mouseUp()
		time.sleep(1)

		for move in move_list:
			from_position = self.get_back_stack_position(move.from_rank_id)
			dest_position = self.get_front_stack_position(move.dest_rank_id)

			pyautogui.moveTo(from_position[0], from_position[1], duration=self.default_delay)
			pyautogui.mouseDown(button='left')
			pyautogui.moveTo(dest_position[0], dest_position[1], duration=self.default_delay)
			pyautogui.mouseUp(button='left')

			self.game.make_move(move)


	def get_rank_x(self, rank_idx):
		return self.left_offset + rank_idx*self.horizontal_spacing + self.card_width/2
	
	def get_stack_front_y(self, rank_idx):
		if not self.game:
			return
		
		rank = self.game.get_rank(rank_idx)
		return self.top_offset + (len(rank.cards)-1 + 0.5)*self.vertical_spacing #+ self.vertical_spacing/2#+ self.card_height/2
	def get_stack_back_y(self, rank_idx):
		if not self.game:
			return
		
		rank = self.game.get_rank(rank_idx)
		rank_stack = rank.get_top_stack()

		return self.top_offset + (len(rank.cards)-len(rank_stack) + 0.5)*self.vertical_spacing

	def get_back_stack_position(self, rank_idx):
		if rank_idx == -1:
			return (self.hand_x, self.hand_y)
		else:
			return (self.get_rank_x(rank_idx), self.get_stack_back_y(rank_idx))
	def get_front_stack_position(self, rank_idx):
		if rank_idx == -1:
			return (self.hand_x, self.hand_y)
		else:
			return (self.get_rank_x(rank_idx), self.get_stack_front_y(rank_idx))

def main():
	board = Board()
	game = board.make_game()
	winning_moves = game.solve()

	board.execute_move_list(winning_moves)
	
profiler.run('main()')