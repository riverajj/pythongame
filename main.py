import pygame as pg
import sys
vec = pg.math.Vector2
from os import path
from settings import *
from sprites import *
from tilemap import *
import random
def draw_player_health(surf, x, y,pct):
    if pct <0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill, BAR_HEIGHT)
    if pct > 0.6:
        col= GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect,2)
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.level = 1
        self.load_data(self.level)
        self.game_started = False

        # self.squaregrid = SquareGrid(self.map.width, self.map.height)

    def load_data(self, level):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.monsA = pg.sprite.Group()
        self.level = level
        self.map_name = 'map' + str(self.level) + '.txt'
        self.map = Map(path.join(game_folder, self.map_name))
        self.title_font = path.join(img_folder, 'Roboto-Light.ttf')
        self.hud_font = path.join(img_folder, 'Roboto-Light.ttf')
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.monsA_img = pg.image.load(path.join(img_folder, MONSA_IMG)).convert_alpha()
        self.monsB_img = pg.image.load(path.join(img_folder, MONSB_IMG)).convert_alpha()
        self.monsC_img = pg.image.load(path.join(img_folder, MONSC_IMG)).convert_alpha()
        self.walls_img = pg.image.load(path.join(img_folder, WALLS_IMG)).convert_alpha()
        self.attack_right = []
        self.attack_right01 = pg.image.load(path.join(img_folder,'attack_right_01.png')).convert_alpha()
        self.attack_right02 = pg.image.load(path.join(img_folder,'attack_right_02.png')).convert_alpha()
        self.attack_right03 = pg.image.load(path.join(img_folder, 'attack_right_03.png')).convert_alpha()
        self.attack_right.append(self.attack_right01)
        self.attack_right.append(self.attack_right02)
        self.attack_right.append(self.attack_right03)
        self.attack_up = []
        self.attack_up01 = pg.image.load(path.join(img_folder,'attack_up_01.png')).convert_alpha()
        self.attack_up02 = pg.image.load(path.join(img_folder,'attack_up_02.png')).convert_alpha()
        self.attack_up03 = pg.image.load(path.join(img_folder, 'attack_up_03.png')).convert_alpha()
        self.attack_up.append(self.attack_up01)
        self.attack_up.append(self.attack_up02)
        self.attack_up.append(self.attack_up03)
        self.attack_left = []
        self.attack_left01 = pg.image.load(path.join(img_folder,'attack_left_01.png')).convert_alpha()
        self.attack_left02 = pg.image.load(path.join(img_folder,'attack_left_02.png')).convert_alpha()
        self.attack_left03 = pg.image.load(path.join(img_folder, 'attack_left_03.png')).convert_alpha()
        self.attack_left.append(self.attack_left01)
        self.attack_left.append(self.attack_left02)
        self.attack_left.append(self.attack_left03)
        self.attack_down = []
        self.attack_down01 = pg.image.load(path.join(img_folder,'attack_down_01.png')).convert_alpha()
        self.attack_down02 = pg.image.load(path.join(img_folder,'attack_down_02.png')).convert_alpha()
        self.attack_down03 = pg.image.load(path.join(img_folder, 'attack_down_03.png')).convert_alpha()
        self.attack_down.append(self.attack_down01)
        self.attack_down.append(self.attack_down02)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.non_enemy = pg.sprite.Group()
        self.non_player = pg.sprite.Group()
        # self.monsA = pg.sprite.Group()
        self.monsB = pg.sprite.Group()
        self.monsC = pg.sprite.Group()
        self.weapon_sprite = pg.sprite.Group()
        self.monster_hitbox = pg.sprite.Group()
        # g = SquareGrid(self.map.width, self.map.height)
        #agg
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                    # g.walls.append(vec(col,row))
                if tile == 'P':
                    self.player = Player(self, col, row)
                    # HealthBar(self,col,row)
                if tile == 'A':
                    MonsterA(self, col, row)
                if tile == "B":
                    MonsterB(self, col, row)
                if tile == "C":
                    MonsterC(self, col, row)
        # self.squaregrid = g
       
        self.camera = Camera(self.map.width, self.map.height)
        
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):

        pg.quit()
       

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player,self.monsters,False)
        for hit in hits:
            self.player.health -= 5
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        # if len(self.monsA) == 0:
        #     self.level += 1
        #     if self.level == 1:
        #         self.map = Map(path.join(path.dirname(__file__), 'map3.txt'))
        # if hits:
        #     if hits[0].rect.centerx < self.player.hit_rect.centerx:
        #         self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        #     if hits[0].rect.centerx > self.player.hit_rect.centerx:
        #         self.player.pos -= vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        if len(self.monsA) == 0 :
            if len(self.monsB) == 0 :
                if len(self.monsC) == 0: 
                    for sprite in self.all_sprites:
                        sprite.kill()
                    self.level += 1
                    if(self.level >= 6):
                        self.level = 6 
                    print(self.level)
                    self.load_data(self.level)
                    self.new()


    # def draw_grid(self):
    #     for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    #     for y in range(0, HEIGHT, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player),2)
        draw_player_health(self.screen,10,570,self.player.health / PLAYER_HEALTH)
        pg.display.flip()


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
    def show_start_screen(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.screen.fill(LIGHTGREY)
        self.menu_image = pg.image.load(path.join(img_folder,'menu_screen.png'))
        self.screen.blit(self.menu_image,(0,100))
        self.draw_text('WIZ KO LANG',self.title_font, 24, BLACK, WIDTH / 2,HEIGHT / 2, align="center")
        self.draw_text('Press any key to start',self.title_font,12,BLACK, WIDTH/2, HEIGHT * 3 / 4, align = "center")
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        self.draw_text('GAME OVER',self.title_font, 24, RED, WIDTH / 2,HEIGHT / 2, align="center")
        self.draw_text('Press a key to start again',self.title_font,12,WHITE, WIDTH/2, HEIGHT * 3 / 4, align = "center")
        self.level = 1
        self.new()
        self.load_data(self.level)
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
