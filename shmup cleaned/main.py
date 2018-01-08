##imports
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialise game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption("kolor shmup")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def new(self):
        # start the game
        # make a groups for adding sprites in draw
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.ebullets = pg.sprite.Group()
        self.win = pg.sprite.Group()
        self.players = pg.sprite.Group()
        # spawn the player
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.players.add(self.player)
        #continually spawn backgroundstars
        for i in range (80):
            B = Backgroundstar(self)
            self.all_sprites.add(B)
        #spawn MRbossman
        self.mrbossman = MRbossman(self)
        self.all_sprites.add(self.mrbossman)
        self.enemy.add(self.mrbossman)
        # initiate run
        self.run()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        #load spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.Events()
            self.Update()
            self.Draw()
    def Update(self):
        # Game loop - Updates
        self.all_sprites.update()
    def Events(self):
        # Game loop - Events
        for event in pg.event.get():
            # check for window closing
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
        enemyhit = pg.sprite.groupcollide(self.bullets, self.enemy, True , False, pg.sprite.collide_circle)
        #check if a bullet hit MRbossman
        for hit in enemyhit:
            self.mrbossman.health -= 15
            if self.mrbossman.health < 0:
                self.mrbossman.health = 0
        # Check if a bullet hit the player
        playerhit = pg.sprite.groupcollide(self.ebullets, self.players, True , False, pg.sprite.collide_circle)
        for hit in playerhit:
            if self.player.invtimer > 1500:
                self.player.lives -= 1
                self.player.invincible()
                if self.player.lives == 0:
                    self.Show_GO_screen()
        # check if the player hit the green block
        colorhit = pg.sprite.groupcollide(self.win, self.players, True , False, pg.sprite.collide_circle)
        for hit in colorhit:
            kolorgreen = True
            pg.quit()

    def Draw(self):
        # Game loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # Draw MRbossmans hp bar
        def draw_Ehp_bar(surf, x, y, pct):
            if pct < 0:
                pct = 0
            Bar_length = 530
            Bar_height = 15
            fill = (self.mrbossman.health * 530) / self.mrbossman.maxhealth
            outline_rect = pg.Rect(x, y, Bar_length, Bar_height)
            fill_rect = pg.Rect(x, y, fill, Bar_height)
            pg.draw.rect(surf, GREEN, fill_rect)
            pg.draw.rect(surf, WHITE, outline_rect, 2)
        draw_Ehp_bar(self.screen, 5, 5, self.mrbossman.health)
        # Draw lives
        #def draw_lives(surf, x, y, lives, player_sprite_lives):
        #	for i in range(lives):
        #		self.player.image.rect = self.player.image.rect()
        #		self.player.image.rect.x = x + 25 * i
        #		self.player.image.rect.y = y
        #		surf.blit(player_sprite_lives, player_sprite_lives_rect)
        #draw_lives(self.screen, Width -150 , Height -30, self.player.lives, self.player.image)
        # After drawing flip the screen
        pg.display.flip()

    def Show_start_screen(self):
        # show the start screen
        pass

    def Show_GO_screen(self):
        # show the game over screen
        pg.quit()

g = Game()
g.Show_start_screen()
while g.running:
    g.new()
pg.quit()
