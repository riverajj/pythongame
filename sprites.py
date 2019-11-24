import pygame as pg
from settings import *
from collections import deque

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        pg.draw.rect(game.screen, (255,0,0))
        # self.squaregrid = game.squaregrid


    def get_keys(self, game):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        mousebuttons = pg.mouse.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        # if pg.mouse.get_pressed()[0]:
        #     mpos = vec(pg.mouse.get_pos())
        #     self.breadth_first_search(self.game.squaregrid, mpos, self.vel)

    def vec2int(self,v):
        return (int(v.x), int(v.y))

    # def breadth_first_search(self, graph, start, end):
    #     frontier2 = deque()
    #     frontier2.append(start)
    #     path = {}
    #     path[self.vec2int(start)] = None
    #     while len(frontier2) > 0:
    #         current = frontier2.popleft()
    #         if current == end :
    #             break
    #         for next in graph.find_neighbors(current):
    #             if vec2int(next) not in path:
    #                 frontier2.append(next)
    #                 path[vec2int(next)] = current - next
        
    #     current = start + path[self.vec2int(start)]
    #     while current != end:
    #         current = current + path[self.vec2int(current)]
    #         self.pos = current * TILESIZE

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys(self.game)
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


# class SquareGrid:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.walls = []
#         self.connections = [vec(1,0), vec(-1,0), vec(0,1), vec(0, -1)]
    
#     def in_bounds(self, node):
#         return 0 <= node.x < self.width and 0 <= node.y < self.height

#     def passable(self, node):
#         return node not in self.walls

#     def find_neighbors(self, node):
#         neighbors = [node + connection for connection in self.connections]
#         neighbors = filter(self.in_bounds, neighbors)
#         neighbors = filter(self.passable, neighbors)
#         print(list(neighbors))
#         return neighbors