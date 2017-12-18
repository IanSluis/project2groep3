#imports
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
        self.score = 0
        # make a groups for adding sprites in draw
        self.all_sprites = pg.sprite.Group()
        # spawn the player
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # initiate run
        self.run()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        #load highscore
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

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
        #see if a bullet hits an enemy
        bullethit = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_circle)
        for hit in bullethit:
            score += 10
            E1 = Enemy1()
            enemies.add(E1)
        #see if an enemy hits the player
        hit = pygame.sprite.spritecollide(player,enemies, True, pygame.sprite.collide_circle)
        if hit:
            death = Deathexplosion(player.rect.center, 'player')
            all_sprites.add(death)
            player.hide()
            player.lives -= 1
            player.power_lvl = 1

    def Draw(self):
        # Game loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # after drawing flip the screen
        pg.display.flip()

    def Show_start_screen(self):
        # show the start screen
        pass

    def Show_GO_screen(self):
        # show the game over screen
        pass

g = Game()
g.Show_start_screen()
while g.running:
    g.new()
    g.Show_GO_screen()

pg.quit()
