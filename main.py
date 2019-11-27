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
        self.load_data()
        # self.squaregrid = SquareGrid(self.map.width, self.map.height)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.monsA_img = pg.image.load(path.join(img_folder, MONSA_IMG)).convert_alpha()
        self.monsB_img = pg.image.load(path.join(img_folder, MONSB_IMG)).convert_alpha()
        self.monsC_img = pg.image.load(path.join(img_folder, MONSC_IMG)).convert_alpha()
        self.walls_img = pg.image.load(path.join(img_folder, WALLS_IMG)).convert_alpha()
        self.attack_img = pg.image.load(path.join(img_folder, ATTACK_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.non_enemy = pg.sprite.Group()
        self.non_player = pg.sprite.Group()
        self.monsA = pg.sprite.Group()
        self.monsB = pg.sprite.Group()
        self.monsC = pg.sprite.Group()
        self.weapon_sprite = pg.sprite.Group()
        self.monster_hitbox = pg.sprite.Group()
        # g = SquareGrid(self.map.width, self.map.height)
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
        # if hits:
        #     if hits[0].rect.centerx < self.player.hit_rect.centerx:
        #         self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        #     if hits[0].rect.centerx > self.player.hit_rect.centerx:
        #         self.player.pos -= vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

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
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
