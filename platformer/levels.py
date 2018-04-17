import pygame
from os import path
import constants
import platforms

BGRED = 0
BGGREEN = 0
BGBLUE = 0
if(constants.REDUNLOCKED):
	BGRED = constants.SKY[0]
if(constants.GREENUNLOCKED):
	BGGREEN = constants.SKY[1]
if(constants.BLUEUNLOCKED):
	BGBLUE = constants.SKY[2]

BGCOLOR = (BGRED,BGGREEN,BGBLUE)




class Level():
	""" This is a generic super-class used to define a level.
		Create a child class for each level with level-specific
		info. """

	# Lists of sprites used in all levels. Add or remove
	# lists as needed for your game. """
	platform_list = None
	enemy_list = None

	# Background image
	background = None

	# How far this world has been scrolled left/right
	world_shift = 0
	level_limit = -1000

	def __init__(self, player):
		""" Constructor. Pass in a handle to player. Needed for when moving platforms
			collide with the player. """
		self.platform_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player

	# Update everythign on this level
	def update(self):
		""" Update everything in this level."""
		self.platform_list.update()
		self.enemy_list.update()

	def draw(self, screen):
		""" Draw everything on this level. """

		# Draw the background
		# We don't shift the background as much as the sprites are shifted
		# to give a feeling of depth.
		screen.fill(BGCOLOR)
		screen.blit(self.background,(self.world_shift // 3,0))

		# Draw all the sprite lists that we have
		self.platform_list.draw(screen)
		self.enemy_list.draw(screen)

	def shift_world(self, shift_x):
		""" When the user moves left/right and we need to scroll everything: """

		# Keep track of the shift amount
		self.world_shift += shift_x

		# Go through all the sprite lists and shift
		for platform in self.platform_list:
			platform.rect.x += shift_x

		for enemy in self.enemy_list:
			enemy.rect.x += shift_x

# Create platforms for the level
class Level_01(Level):
	""" Definition for level 1. """

	def __init__(self, player):
		""" Create level 1. """

		# Call the parent constructor
		Level.__init__(self, player)
		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')
		self.background = pygame.image.load(path.join(img_dir, "background_01.png")).convert()
		self.background.set_colorkey(constants.RED)
		self.level_limit = -2500

		# Array with type of platform, and x, y location of the platform.
		level = [ 	
					#back wall
					[platforms.TEST_ONE, -100, 600],
					[platforms.TEST_ONE, -100, 543],
					[platforms.TEST_ONE, -100, 486],
					[platforms.TEST_ONE, -100, 429],
					[platforms.TEST_ONE, -100, 372],
					#first platform L shape
					[platforms.TEST_ONE, 570, 490],
					[platforms.TEST_ONE, 640, 490],
					[platforms.TEST_ONE, 710, 490],
					[platforms.TEST_ONE, 710, 433],
					[platforms.TEST_ONE, 710, 376],
					[platforms.TEST_ONE, 710, 319],
					
					#jump over it
					[platforms.TEST_ONE, 430, 386],

					#the second wall that requires the moving platform
					[platforms.TEST_ONE, 1300, 600],
					[platforms.TEST_ONE, 1300, 543],
					[platforms.TEST_ONE, 1300, 486],
					[platforms.TEST_ONE, 1300, 429],
					[platforms.TEST_ONE, 1300, 372],

					#jumping part
					[platforms.TEST_ONE, 1700, 231],
					[platforms.TEST_ONE, 1550, 436],
					[platforms.TEST_ONE, 1650, 324],
					[platforms.TEST_ONE, 1350, 541],
					
				  ]


		# Go through the array above and add platforms
		for platform in level:
			block = platforms.Platform(platform[0])
			block.rect.x = platform[1]
			block.rect.y = platform[2]
			block.player = self.player
			self.platform_list.add(block)
			
		# Add a custom moving platform
		block = platforms.MovingPlatform(platforms.TEST_TWO)
		block.rect.x = 1000
		block.rect.y = 280
		block.boundary_left = 800
		block.boundary_right = 1200
		block.change_x = 1
		block.player = self.player
		block.level = self
		self.platform_list.add(block)


# Create platforms for the level
class Level_02(Level):
	""" Definition for level 2. """

	def __init__(self, player):
		""" Create level 2. """

		# Call the parent constructor
		Level.__init__(self, player)

		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')
		self.background = pygame.image.load(path.join(img_dir, "background_02.png")).convert()
		self.background.set_colorkey(constants.RED)
		self.level_limit = -2500

		# Array with type of platform, and x, y location of the platform.
		level = [ 	[platforms.TEST_TWO, 570, 550],
					[platforms.TEST_TWO, 1190, 280],
				]


		# Go through the array above and add platforms
		for platform in level:
			block = platforms.Platform(platform[0])
			block.rect.x = platform[1]
			block.rect.y = platform[2]
			block.player = self.player
			self.platform_list.add(block)

		# Add a custom moving platform
		block = platforms.MovingPlatform(platforms.TEST_TWO)
		block.rect.x = 1500
		block.rect.y = 300
		block.boundary_top = 100
		block.boundary_bottom = 550
		block.change_y = -1
		block.player = self.player
		block.level = self
		self.platform_list.add(block)
