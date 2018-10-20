import pygame
import numpy as np
import conf

class Map:
    def __init__(self,matrix_map,tile_size):
        self.matrix_map = matrix_map
        self.tile_size = tile_size
        nfils, ncols = self.matrix_map.shape
        self.nfils = nfils
        self.ncols = ncols
        self.width = ncols*self.tile_size[0]
        self.height = nfils*self.tile_size[1]
        self.size = self.width,self.height
        self.image = self.generate_map()
        self.rect = self.image.get_rect()
    def generate_map(self):
        nfils,ncols = self.matrix_map.shape
        sur = pygame.Surface(self.size)
        sur.fill(conf.color_fons)
        for fila in range(nfils):
            for columna in range(ncols):
                tile = pygame.Surface(self.tile_size)
                tile.fill(conf.tile_color[self.matrix_map[fila,columna]])
                r = tile.get_rect()
                r.topleft = tuple(np.multiply(self.tile_size,(columna,fila)))
                sur.blit(tile,r)
        return sur
