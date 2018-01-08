import os, sys, pygame

#execfile('file.py')
main_dir = os.path.split(os.path.abspath(__file__))[0]
platformer_dir = os.path.join(main_dir, 'platformer')
platformer_file = platformer_dir + "\platformer.py"
space_dir = os.path.join(main_dir, 'python game stuff')
space_file =  str(space_dir) + "\game.py"
pong_dir = os.path.join(main_dir, 'pong')
pong_file =  pong_dir + "\pong.py"
starjump_dir = os.path.join(main_dir, 'StarJump')
starjump_file =  starjump_dir + "\jumpstar.py"
selectablegames = [platformer_file,space_file,pong_file,starjump_file]

clock = pygame.time.Clock() 
SCREENRECT = pygame.Rect(0, 0, 640, 480)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SKYBLUE = (94,161,255)

#unlocks
KolorRed = False
KolorGreen = True
KolorBlue = False

def launch_game(name):
	print(name)
	os.system(name)
		
def main(winstyle = 0):	
	pygame.init()
	pygame.display.set_caption('Kolor')
	bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
	screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
	background = pygame.Surface(SCREENRECT.size)
	screen.fill(WHITE)
	background.fill(WHITE)
	screen.blit(background, (0,0))
	pygame.display.flip()
	
	SelectedGame = 0

#def draw_text(surf, text, size, x, y):
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("KOLOR", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=background.get_width()/2)
		background.blit(text, textpos)
		
	while 1:
		
		#input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
				if SelectedGame != 0:
					SelectedGame = SelectedGame - 1
					print("SelectedGame = " + str(SelectedGame))
				else:
					SelectedGame = 3
					print("Selectedgame reset to " + str(SelectedGame))
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
				if SelectedGame != 3:
					SelectedGame = SelectedGame + 1
					print("SelectedGame = " + str(SelectedGame))
				else:
					SelectedGame = 0
					print("Selectedgame reset to " + str(SelectedGame))
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				print("launching " + str(SelectedGame))
				chosengame = selectablegames [SelectedGame]
				launch_game(chosengame)
		#Draw Everything
		screen.blit(background, (0, 0))
		pygame.display.flip()
		
		
		clock.tick(60)	
		
		
if __name__ == '__main__':
	main()