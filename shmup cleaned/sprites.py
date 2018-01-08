##sprite classes
import pygame as pg
import os
import math
import random
from settings import *
#boss deathexplosion

class Spritesheet:
    # Utility class for loading sprites from spritesheet
    def __init__ (self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Get the part of the spritesheet with the image
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    #player class
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image( 112, 0, 16, 16)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 4
        if kolorgreen:
            pg.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        elif kolorgreen == False:
            pg.draw.circle(self.image, GRAY, self.rect.center, self.radius)
        self.rect.x = (Width / 2) - 8
        self.rect.y = Height - 60
        self.speedx = 0
        self.speedy = 0
        self.shot_delay = 50
        self.last_shot = pg.time.get_ticks()
        self.shots = 0
        self.lives = 3
        self.invtimer = pg.time.get_ticks()
        self.blinktimer = pg.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
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

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shot_delay:
            self.last_shot = now
            friendlybulletm = FriendlyBulletM(self.game, self.rect.x + 8, self.rect.top)
            self.game.all_sprites.add(friendlybulletm)
            self.game.bullets.add(friendlybulletm)
            if self.shots % 2 == 0:
                friendlybulletr = FriendlyBulletR(self.game, self.rect.x + 8, self.rect.top)
                self.game.all_sprites.add(friendlybulletr)
                self.game.bullets.add(friendlybulletr)
                friendlybulletl = FriendlyBulletL(self.game, self.rect.x + 8, self.rect.top)
                self.game.all_sprites.add(friendlybulletl)
                self.game.bullets.add(friendlybulletl)
                self.shots += 1
            else:
                self.shots += 1

    def invincible(self):
        self.invtimer = pg.time.get_ticks()
        self.blinktimer = pg.time.get_ticks()

class FriendlyBulletR(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image( 0, 0, 15, 15)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 4
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.xPos = 0
        self.startx = self.game.player.rect.x
        self.starty = self.game.player.rect.top
    def update(self):
        self.xPos = math.sin(0.03 * (self.rect.bottom - self.starty)) * 20
        self.rect.x = self.startx
        self.rect.x += self.xPos
        self.rect.y += self.speedy
        #kill the bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

class FriendlyBulletL(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image( 0, 0, 15, 15)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 4
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.xPos = 0
        self.startx = self.game.player.rect.x
        self.starty = self.game.player.rect.top
    def update(self):
        self.xPos = -math.sin(0.03 * (self.rect.bottom - self.starty)) * 20
        self.rect.x = self.startx
        self.rect.x += self.xPos
        self.rect.y += self.speedy
        #kill the bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

class FriendlyBulletM(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image( 20, 16, 8, 16)
        self.image.set_colorkey(BLACK)
        self.radius = 3
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15
    def update(self):
        self.rect.y += self.speedy
        #kill the bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

class Backgroundstar(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image( 4, 20, 4, 4)
        self.rect = self.image.get_rect()
        self.speedy = 3
        self.rect.x = random.randrange (Width - self.rect.width)
        self.rect.y = random.randrange (-1000, -10)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > Height + 10:
            self.rect.x = random.randrange (Width - self.rect.width)
            self.rect.y = random.randrange (-1000, -10)

class MRbossman(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(self.game.spritesheet.get_image(0, 32, 32, 28), (int(32*3), int(28*3)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 37
        self.rect.y = -42
        self.rect.x = (Width / 2) - 48
        self.maxhealth = 18000
        self.health = 18000
        self.speedx = 0
        self.speedy = 1
        self.i = 0
        # Phase 1 stuff
        self.phase1_cd = 100
        self.phase1_ls = pg.time.get_ticks()
        # Phase 2 stuff
        self.phase2_cd = 10
        self.phase2_ls = pg.time.get_ticks()
        self.circle = 0
        self.side = 1
        # Phase 3 stuff
        self.phase3_cd = 100
        self.phase3_ls = pg.time.get_ticks()
        self.movementcircle = 0
        # Phase 4 stuff
        self.phase4_cd = 40
        self.phase4_ls = pg.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.i == 0 and self.rect.y > 100:
            self.speedy = 0
            self.i += 1
            self.speedx = 3
        elif self.i == 1:
            self.phase1()
        if self.i == 1 and self.health < 16000:
            if self.rect.x > (Width / 2) - 43:
                self.speedx = -5
            if self.rect.x < (Width / 2) - 48:
                self.speedx = 5
            if self.rect.x >= (Width / 2) - 48 and self.rect.x <= (Width / 2) - 43:
                self.speedx = 0
            if self.rect.y < (Height / 2) - 48:
                self.speedy = 1
            else:
                self.speedy = 0
            if self.speedx == 0 and self.speedy == 0:
                self.i +=1
        elif self.i == 2:
            self.phase2()
        if self.i == 2 and self.health < 13000:
            self.speedx = 1
            if self.rect.x > Width - 148:
                self.speedx = 0
                self.i +=1
        elif self.i == 3:
            self.phase3()
        if self.i == 3 and self.health < 10500:
            if self.rect.x >= (Width / 2) - 48 and self.rect.x <= (Width / 2) - 43:
                self.rect.x = Width/2 - 48
            if self.rect.y > (Height / 2) - 48 and self.rect.y < (Height / 2) - 43:
                self.rect.y = Height/2 - 48
            if self.speedx == 0 and self.speedy == 0:
                self.i +=1
        elif self.i == 4:
            if self.rect.x > (Width / 2) - 42:
                self.speedx = -5
            elif self.rect.x < (Width / 2) - 48:
                self.speedx = 5
            if self.rect.x >= (Width / 2) - 48 and self.rect.x <= (Width / 2) - 42:
                self.speedx = 0
            if self.rect.y < (Height / 2) - 50:
                self.speedy = 3
            elif self.rect.y > (Height / 2) - 40:
                self.speedy = -3
            else:
                self.speedy = 0
            if self.speedx == 0 and self.speedy == 0:
                self.i +=1
        elif self.i == 5:
            self.phase4()
        if self.i == 5 and self.health < 6500:
            if self.rect.x > (Width / 2) - 42:
                self.speedx = -5
            elif self.rect.x < (Width / 2) - 48:
                self.speedx = 5
            if self.rect.x >= (Width / 2) - 48 and self.rect.x <= (Width / 2) - 42:
                self.speedx = 0
            if self.rect.y < (Height / 2) - 50:
                self.speedy = 3
            elif self.rect.y > (Height / 2) - 40:
                self.speedy = -3
            else:
                self.speedy = 0
            if self.speedx == 0 and self.speedy == 0:
                self.i +=1
        elif self.i == 6:
            self.phase5()
        if self.i == 6 and self.health < 2000:
            if self.rect.x > (Width / 2) - 43:
                self.speedx = -5
            if self.rect.x < (Width / 2) - 48:
                self.speedx = 5
            if self.rect.x >= (Width / 2) - 48 and self.rect.x <= (Width / 2) - 43:
                self.speedx = 0
            if self.speedx == 0:
                self.i +=1
        elif self.i == 7:
            self.phase6()
        if self.i == 7 and self.health == 0:
            self.speedy = -1
            if self.rect.y == 100:
                self.speedy = 0
                self.spawncolor()
                self.kill()

    def phase1(self):
        if self.rect.x > Width - 148:
            self.speedx = -3
        elif self.rect.x < 52:
            self.speedx = 3
        now = pg.time.get_ticks()
        if now - self.phase1_ls > self.phase1_cd:
            self.phase1_ls = now
            b1 = Bossmanbulletsp1(self.game, self.rect.x + 48, self.rect.y + 42)
            self.game.all_sprites.add(b1)
            self.game.ebullets.add(b1)

    def phase2(self):
        now = pg.time.get_ticks()
        if now - self.phase2_ls > self.phase2_cd:
            self.phase2_ls = now
            b2 = Bossmanbulletsp2(self.game, self.rect.x + 48, self.rect.y + 42)
            self.game.all_sprites.add(b2)
            self.game.ebullets.add(b2)
            self.circle += 0.015
            self.side += 1
            if self.side == 5:
                self.side = 1

    def phase3(self):
        now = pg.time.get_ticks()
        if now - self.phase3_ls > self.phase3_cd:
            self.phase3_ls = now
            b3 = Bossmanbulletsp3(self.game, self.rect.x + 48, self.rect.y + 42)
            self.game.all_sprites.add(b3)
            self.game.ebullets.add(b3)
        self.rect.x = math.cos(self.movementcircle) * 170 + 222
        self.rect.y = math.sin(self.movementcircle) * 170 + 340
        self.movementcircle += 0.0075 * math.pi

    def phase4(self):
        now = pg.time.get_ticks()
        if now - self.phase4_ls > self.phase4_cd:
            self.phase4_ls = now
            b4 = Bossmanbulletsp4(self.game, self.rect.x + 48, self.rect.y + 42)
            self.game.all_sprites.add(b4)
            self.game.ebullets.add(b4)
            self.speedx = random.randrange(-5,5)
            self.speedy = random.randrange(-5,5)
            if self.rect.x > Width/2 + 100:
                self.speedx += -5
            elif self.rect.x < Width/2 - 100:
                self.speedx += 5
            if self.rect.y > Height/2 + 100:
                self.speedy += -5
            if self.rect.y < Height/2 - 100:
                self.speedy += 5

    def phase5(self):
        pass
    def phase6(self):
        pass
    def spawncolor(self):
        color = Green(self.game, self.rect.x + 48, self.rect.y + 42)
        self.game.all_sprites.add(color)
        self.game.win.add(color)

class Bossmanbulletsp1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(self.game.spritesheet.get_image( 0, 16, 16, 16), (int(24), int(24)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.radius = 10
        self.speedx = 0
        self.speedy = 0
        self.speed = 7
        self.get_target()

    def get_target(self):

        xdiff = (self.game.player.rect.x + 8) - (self.game.mrbossman.rect.x + 48)
        ydiff = (self.game.player.rect.y + 8) - (self.game.mrbossman.rect.y + 42)

        magnitude = math.sqrt(float(xdiff**2 + ydiff**2))
        numframes = int(magnitude / self.speed)
        if numframes == 0:
            numframes = 1
        self.speedx = xdiff / numframes
        self.speedy = ydiff / numframes

        xtravel = self.speedx * numframes
        ytravel = self.speedy * numframes

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < -50 or self.rect.centerx < -50 or self.rect.bottom > Height + 50 or self.rect.centerx > Width + 50:
            self.kill()

class Bossmanbulletsp2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(self.game.spritesheet.get_image( 0, 16, 16, 16), (int(24), int(24)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.radius = 10
        self.speedx = 0
        self.speedy = 0
        self.get_target()

    def get_target(self):
        xdiff = (Width/2 + math.sin(self.game.mrbossman.circle)* 500) - (Width/2)
        ydiff = (Height/2 + math.cos(self.game.mrbossman.circle)* 500) - (Height/2)
        if self.game.mrbossman.side == 1:
            xdiff = (Width/2 + math.sin(self.game.mrbossman.circle)* 500) - (Width/2)
            ydiff = (Height/2 + math.cos(self.game.mrbossman.circle)* 500) - (Height/2)
        elif self.game.mrbossman.side == 2:
            xdiff = (Width/2 + -math.sin(self.game.mrbossman.circle)* 500) - (Width/2)
            ydiff = (Height/2 + -math.cos(self.game.mrbossman.circle)* 500) - (Height/2)
        elif self.game.mrbossman.side == 3:
            xdiff = (Width/2 + math.sin(self.game.mrbossman.circle + 0.5 * math.pi)* 500) - (Width/2)
            ydiff = (Height/2 + math.cos(self.game.mrbossman.circle + 0.5 * math.pi)* 500) - (Height/2)
        elif self.game.mrbossman.side == 4:
            xdiff = (Width/2 + -math.sin(self.game.mrbossman.circle + 0.5 * math.pi)* 500) - (Width/2)
            ydiff = (Height/2 + -math.cos(self.game.mrbossman.circle + 0.5 * math.pi)* 500) - (Height/2)
        numframes = 25

        self.speedx = xdiff / numframes
        self.speedy = ydiff / numframes

        xtravel = self.speedx * numframes
        ytravel = self.speedy * numframes

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < -50 or self.rect.centerx < -50 or self.rect.bottom > Height + 50 or self.rect.centerx > Width + 50:
            self.kill()

class Bossmanbulletsp3(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(self.game.spritesheet.get_image( 0, 16, 16, 16), (int(24), int(24)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.radius = 10
        self.speedx = 0
        self.speedy = 0
        self.speed = 5
        self.get_target()

    def get_target(self):

        xdiff = (self.game.player.rect.x + 8) - (self.game.mrbossman.rect.x + 48)
        ydiff = (self.game.player.rect.y + 8) - (self.game.mrbossman.rect.y + 42)

        magnitude = math.sqrt(float(xdiff**2 + ydiff**2))
        numframes = int(magnitude / self.speed)
        if numframes == 0:
            numframes = 1
        self.speedx = xdiff / numframes
        self.speedy = ydiff / numframes

        xtravel = self.speedx * numframes
        ytravel = self.speedy * numframes

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < -50 or self.rect.centerx < -50 or self.rect.bottom > Height + 50 or self.rect.centerx > Width + 50:
            self.kill()

class Bossmanbulletsp4(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(self.game.spritesheet.get_image( 0, 16, 16, 16), (int(24), int(24)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.radius = 10
        self.speedx = 0
        self.speedy = 0
        self.get_target()
        self.bulletdegrade = pg.time.get_ticks()
        self.bulletlife = 3000
    def get_target(self):
        xdiff = (Width/2 + math.sin(random.randrange(0, 500))* 500) - (Width/2) + 48
        ydiff = (Height/2 + math.cos(random.randrange(0, 500))* 500) - (Height/2)+ 42
        numframes = 120

        self.speedx = xdiff / numframes
        self.speedy = ydiff / numframes

        xtravel = self.speedx * numframes
        ytravel = self.speedy * numframes

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def update(self):
        now = pg.time.get_ticks()
        if now - self.bulletdegrade > self.bulletlife:
            self.bulletdegrade = now
            self.kill()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < -50 or self.rect.centerx < -50 or self.rect.bottom > Height + 50 or self.rect.centerx > Width + 50:
            self.kill()

class Bossmanbulletsp5(pg.sprite.Sprite):
    pass

class Green(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(self.game.spritesheet.get_image(14, 44, 4, 4), (int(48), int(48)))
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.centerx = x
        self.rect.bottom = y
