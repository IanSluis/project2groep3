"""
Module for managing platforms.
"""
import pygame
import constants
from os import path
from spritesheet_functions import SpriteSheet

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite
BLUETHING		= (17, 0, 16, 16)
GREENTHING		= (17, 17, 16, 16)
REDTHING		= (0, 17, 16, 16)
WHITETHING		= (0, 0, 16, 16)

SELECTED_SPRITESHEET = "things.png"


class Thing(pygame.sprite.Sprite):
	""" thing """

	def __init__(self, sprite_sheet_data):
		""" thing constructor. Assumes constructed with user passing in
			an array of 5 numbers like what's defined at the top of this
			code. """
		pygame.sprite.Sprite.__init__(self)
		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')
		sprite_sheet = SpriteSheet(path.join(img_dir, SELECTED_SPRITESHEET))
		# Grab the image for this thing
		self.image = sprite_sheet.get_image(sprite_sheet_data[0],
											sprite_sheet_data[1],
											sprite_sheet_data[2],
											sprite_sheet_data[3])

		self.rect = self.image.get_rect()	
		self.image.set_colorkey(constants.YELLOW)