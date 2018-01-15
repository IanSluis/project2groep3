##imports
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialise game window
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption("kolor shmup")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)

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
        #initiate the backgroundmusic
        pg.mixer.music.load(path.join(self.snd_dir, 'bg.wav'))
        pg.mixer.music.set_volume(0.03)
        #spawn MRbossman
        self.mrbossman = MRbossman(self)
        self.all_sprites.add(self.mrbossman)
        self.enemy.add(self.mrbossman)
        #initiate the game loop
        self.run()
    def load_data(self):
        self.dir = path.dirname(__file__)
        #load spritesheet images
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        #load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.shot_sound = pg.mixer.Sound(path.join(self.snd_dir,'shoot.wav'))
        self.shot_sound.set_volume(0.01)
        self.GO_sound = pg.mixer.Sound(path.join(self.snd_dir, 'GO.wav'))
        self.GO_sound.set_volume(0.5)
        self.start_sound = pg.mixer.Sound(path.join(self.snd_dir, 'start.wav'))
        self.start_sound.set_volume(0.1)
        self.boss_sound = pg.mixer.Sound(path.join(self.snd_dir, 'boss.wav'))
        self.boss_sound.set_volume(0.15)
        self.win_sound = pg.mixer.Sound(path.join(self.snd_dir, 'win.wav'))
        self.win_sound.set_volume(0.1)

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.Events()
            self.Update()
            self.Draw()
        pg.mixer.music.fadeout(500)
    def Update(self):
        # Game loop - Updates
        self.all_sprites.update()
        self.now = pg.time.get_ticks()
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
            if self.mrbossman.i > 0:
                self.mrbossman.health -= 50#
                if self.mrbossman.health < 0:
                    self.mrbossman.health = 0
        # Check if a bullet hit the player
        playerhit = pg.sprite.groupcollide(self.ebullets, self.players, True , False, pg.sprite.collide_circle)
        for hit in playerhit:
            if self.now - self.player.invtimer > 1500:
                self.player.lives -= 1
                self.player.invincible()
                if self.player.lives == 0:
                    self.GO_sound.play()
                    pg.time.wait(1447)
                    self.Show_GO_screen()
        # check if the player hit the green block
        colorhit = pg.sprite.groupcollide(self.win, self.players, True , False, pg.sprite.collide_circle)
        for hit in colorhit:
            kolorgreen = True
            self.win_sound.play()
            pg.time.wait(2400)
            pg.quit()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_Ehp_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        Bar_length = 530
        Bar_height = 15
        fill = (self.mrbossman.health * 530) / self.mrbossman.maxhealth
        outline_rect = pg.Rect(x, y, Bar_length, Bar_height)
        fill_rect = pg.Rect(x, y, fill, Bar_height)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_lives(self, surf, x, y, lives, image):
        self.image = image
        self.rect = self.image.get_rect()
        for i in range(lives):
            self.rect.x = x + 25 * i
            self.rect.y = y
            surf.blit(self.image, self.rect)

    def Draw(self):
        # Game loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # Draw MRbossmans hp bar
        self.draw_Ehp_bar(self.screen, 5, 5, self.mrbossman.health)
        # Draw lives
        self.draw_lives(self.screen, Width -150 , Height -30, self.player.lives, self.player.image)
        # After drawing flip the screen
        pg.display.flip()

    def Show_start_screen(self):
        # show the start screen
        self.screen.fill(BLACK)
        self.draw_text('kolorshmup', 48, WHITE, Width/2, Height/5)
        self.draw_text('wasd or arrow keys to move, space to shoot', 25, WHITE, Width/2, Height/2.5)
        self.draw_text('hold shift to move slowly', 25, WHITE, Width/2, Height/2)
        self.draw_text('press any key to start or quit to go back to the menu', 20, WHITE, Width/2, Height/1.5)
        pg.display.flip()
        self.wait_for_key()

    def Show_GO_screen(self):
        # show the game over screen
        self.screen.fill(BLACK)
        self.draw_text('Game over', 48, WHITE, Width/2, Height/4)
        self.draw_text('press any key to start again', 20, WHITE, Width/2, Height/2)
        self.draw_text('quit to go back to the main menu', 20, WHITE, Width/2, Height/1.5)
        pg.display.flip()
        self.wait_for_key()
        self.new()
    def wait_for_key(self):
        waiting = True
        keystate = pg.key.get_pressed()
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.KEYUP:
                    waiting = False
        self.start_sound.play()

g = Game()
g.Show_start_screen()
while g.running:
    g.new()
pg.quit()
