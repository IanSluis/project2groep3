import pygame, sys, random
from pygame.locals  import *

pygame.init()
pygame.font.init()

myFont_medium = pygame.font.SysFont("game_over.ttf", 50)
myFont_small = pygame.font.SysFont("game_over.ttf", 25)
myFont_large = pygame.font.SysFont("game_over.ttf", 100)

WINDOWWIDTH = 640
WINDOWHEIGHT = 320
LINETHICKNESS = 10

screensize = (640, 320)

screen = pygame.display.set_mode(screensize)

clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
grey = (210, 210, 210)

playerpoints = 0


def intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(black)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 100+100 > mouse[0] > 100 and 170+50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (100, 170, 100, 50))
            if click[0] == 1:
                main()
        else:
            pygame.draw.rect(screen, white, (100, 170, 100, 50))

        if 400 + 100 > mouse[0] > 400 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (400, 170, 100, 50))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, white, (400, 170, 100, 50))

        pong_text = myFont_large.render("Crazy Pong", False, white)
        start_text = myFont_medium.render("Play", False, black)
        quit_text = myFont_medium.render("Quit", False, black)

        screen.blit(pong_text, (100, 50))
        screen.blit(start_text, (115, 180))
        screen.blit(quit_text, (415, 180))

        pygame.display.update()
        clock.tick(30)


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

        self.direction = [- 1, 1]

        self.speedx = 6
        self.speedy = 4

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

        self.speed = 4

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

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 100 + 100 > mouse[0] > 100 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (100, 170, 100, 50))
            if click[0] == 1:
                paused = False
        else:
            pygame.draw.rect(screen, white, (100, 170, 100, 50))

        if 400 + 100 > mouse[0] > 400 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (400, 170, 100, 50))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, white, (400, 170, 100, 50))


        pause_text = myFont_large.render("Paused", False, white)
        go_text = myFont_medium.render("Go", False, black)
        quit_text = myFont_medium.render("Quit", False, black)

        screen.blit(pause_text, (190, 50))
        screen.blit(go_text, (125, 180))
        screen.blit(quit_text, (415, 180))


        pygame.display.update()
        clock.tick(30)


def gameover():

    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    main()

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 100 + 100 > mouse[0] > 100 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (100, 170, 185, 50))
            if click[0] == 1:
                main()
        else:
            pygame.draw.rect(screen, white, (100, 170, 185, 50))

        if 400 + 100 > mouse[0] > 400 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (400, 170, 100, 50))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, white, (400, 170, 100, 50))

        go_text = myFont_large.render("Game Over", False, white)
        try_text = myFont_medium.render("Try again", False, black)
        quit_text = myFont_medium.render("Quit", False, black)
        screen.blit(go_text, (150, 50))
        screen.blit(try_text, (115, 180))
        screen.blit(quit_text, (415, 180))

        pygame.display.update()
        clock.tick(30)


def won():

    while won:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    main()

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 100 + 100 > mouse[0] > 100 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (100, 170, 185, 50))
            if click[0] == 1:
                main()
        else:
            pygame.draw.rect(screen, white, (100, 170, 185, 50))

        if 400 + 100 > mouse[0] > 400 and 170 + 50 > mouse[1] > 170:
            pygame.draw.rect(screen, grey, (400, 170, 100, 50))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, white, (400, 170, 100, 50))

        go_text = myFont_large.render("You won!", False, white)
        try_text = myFont_medium.render("Try again", False, black)
        quit_text = myFont_medium.render("Quit", False, black)
        screen.blit(go_text, (150, 50))
        screen.blit(try_text, (115, 180))
        screen.blit(quit_text, (415, 180))

        pygame.display.update()
        clock.tick(30)


def main():

    pong = Pong(screensize)
    ai_paddle = AIPaddle(screensize)
    player_paddle = PlayerPaddle(screensize)

    running = True

    score = playerpoints

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

                elif event.key == pygame.K_ESCAPE:
                    pause()

        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)

        if pong.hit_edge_right:
                gameover()
                main()
        elif pong.hit_edge_left:
                won()
                # score = score + 1
                main()

        if score == 5:
            won()

        screen.fill(black)

        pygame.draw.line(screen, white, (320, 0), (320, 320), 3)

        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)

        pygame.display.flip()

    pygame.quit()


intro()
main()