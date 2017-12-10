import pygame
from pygame.locals import *

pygame.init()

screensize = (640, 320)

screen = pygame.display.set_mode(screensize)

clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)

def text_objects(text, font):
    textSurface = font.render(text, True, white, )
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('game_over.ttf, 100')
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screensize/2), (screensize/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()



class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize

        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        self.color = (black)

        self.direction = [1,1]

        self.speedx = 3
        self.speedy = 6

        self.hit_edge_left = False
        self.hit_edge_right = False


    def update(self, player_paddle, ai_paddle):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
        if self.rect.colliderect(ai_paddle):
            self.direction[0] = 1

    def render(self, screen):
      pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
      pygame.draw.circle(screen, (white), self.rect.center, self.radius, 2)

class AIPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = 5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (black)

        self.speed = 10

    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (white), self.rect, 2)

class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (black)

        self.speed = 3
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed
        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (white), self.rect, 2)


def pause():

    clock = pygame.time.Clock()

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

            screen.fill(black)

#        message_display("Paused", (white), -100, size ="large")

#        message_display("Press C to continue or Q to quit.",(white), 25)

        pygame.display.update()
        clock.tick(5)


def main():

    pong = Pong(screensize)
    ai_paddle = AIPaddle(screensize)
    player_paddle = PlayerPaddle(screensize)

    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_paddle.direction = -1
                elif event.key == K_DOWN:
                    player_paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and player_paddle.direction == -1:
                    player_paddle.direction = 0
                elif event.key == K_DOWN and player_paddle.direction == 1:
                    player_paddle.direction = 0

                elif event.key == pygame.K_p:
                    pause()


        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)

        if pong.hit_edge_right:
            main()
        elif pong.hit_edge_left:
            main()


        screen.fill(black)

        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)

        pygame.display.flip()

    pygame.quit()

main()