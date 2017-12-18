#sprite classes
import pygame as pg
import os
from settings import *

class Spritesheet:
    #utility class for loading sprites from spritesheet
    def __init__ (self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Get the part of the spritesheet with the image
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image
#player class
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image( 112, 0, 16, 16)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 16
        self.rect.centerx = Width / 2
        self.rect.bottom = Height - 60
        self.speedx = 0
        self.speedy = 0
        self.shot_delay = 300
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power_lvl = 1

    def update(self):
        self.speedx = 0
        self.speedy = 0
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (Width / 2, Height - 60)

        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.speedx = -5
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.speedx = 5
        if (keystate[pg.K_LEFT] or keystate[pg.K_a]) and (keystate[pg.K_RIGHT]or keystate[pg.K_d]):
            self.speedx = 0
        if keystate[pg.K_UP] or keystate[pg.K_w]:
            self.speedy = -5
        if keystate[pg.K_DOWN] or keystate[pg.K_s]:
            self.speedy = 5
        if (keystate[pg.K_UP] or keystate[pg.K_w]) and (keystate[pg.K_DOWN] or keystate[pg.K_s]):
            self.speedy = 0
        if keystate[pg.K_SPACE]:
            self.shoot()
        if keystate[pg.K_LSHIFT] or keystate[pg.K_RSHIFT]:
            self.rect.x += self.speedx / 2
            self.rect.y += self.speedy / 2
        else:
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Width:
            self.rect.right = Width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Height:
            self.rect.bottom = Height

    def hide(self):
		#hide the player while "dead"
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT - 3000)

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = self.game.spritesheet.get_image( 16, 0, 16, 16)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 17
        self.rect.x = -35
        self.rect.y = 20
        self.speedy = 0
        self.speedx = 5

    def update(self):
        while self.rect.top < HEIGHT - 100 :
            if self.rect.right > WIDTH - 30 :
                self.speedx = -5
                self.rect.top += -20
            if self.rect.left < 10 and self.rect.y > 21 :
                self.speedx = 5
                self.rect.top += -20

class Backgroundstar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = self.game.spritesheet.get_image( 0, 16, 16, 16)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speedy = 3
        self.rect.x = random.randrange (WIDTH - self.rect.width)
        self.rect.y = random.randrange (-1000, -10)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange (WIDTH - self.rect.width)
            self.rect.y = random.randrange (-1000, -10)
