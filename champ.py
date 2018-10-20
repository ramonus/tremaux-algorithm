import pygame
import conf
import numpy as np

class Champ(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface(conf.champ_size,pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.topleft = tuple(np.add(np.multiply(conf.tile_size,pos),np.floor_divide(np.subtract(conf.tile_size,conf.champ_size),2)))
        self.pos = pos
        pygame.draw.circle(self.image,conf.color_champ,(self.rect.width//2,self.rect.width//2),15)
        self.waiting_order = True
        self.vel = (0,0)
        self.dest = None

    def set_order(self,nt):
        self.waiting_order = False
        self.vel = tuple(np.subtract(nt,self.pos))
        self.dest = nt
    def _buscarIndex(self,pos):
        return tuple(np.floor_divide(pos,conf.tile_size))
    def inside_tile(self,pos):
        r = np.multiply(pos,conf.tile_size)
    def update(self):
        self.pos = self._buscarIndex(self.rect.topleft)
        if self._in_pos():
            self.vel = (0,0)
            self.waiting_order = True
        else:
            self.rect = self.rect.move(self.vel)
            
    def _in_pos(self):
        r = pygame.Rect(np.multiply(conf.tile_size,self.dest),conf.tile_size)
        return r.contains(self.rect)
