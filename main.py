import pygame
from pygame.locals import *
from pgu import engine
import conf
import numpy as np
import champ
import map
import time
class Joc(engine.Game):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        pygame.display.set_caption("Tremaux algorithm")
        self.crono = pygame.time.Clock()
        self._init_state_machine()

    def _init_state_machine(self):
        self.jugant = Jugant(self)

    def run(self):
        super().run(self.jugant, self.screen)

    def tick(self):
        self.crono.tick(conf.fps)

# Classe Jugant
class Jugant(engine.State):
    def init(self):
        self.gchamp = pygame.sprite.Group()
        self.champ = champ.Champ((0,0))
        self.gchamp.add(self.champ)
        self.map = map.Map(conf.maze_demo,conf.tile_size)
        self.champ.set_order((0,1))
        self.motor = Motor(self.map,self.champ,(12,14))
    def paint(self, screen):
        self.update(screen)

    def loop(self):
        self.gchamp.update()
        self.motor.update()

    def update(self, screen):
        screen.fill(conf.color_fons)
        screen.blit(self.map.image,self.map.rect)
        screen.blit(self.motor.make_mark_surface(),self.map.rect)
        self.gchamp.draw(screen)
        pygame.display.flip()
    

class Motor:
    def __init__(self,_map,champ,iend):
        print(conf.maze_demo.shape)
        self.map = _map
        self.iend = iend
        self.champ = champ
        self.matrix_marks = np.zeros(self.map.matrix_map.shape).astype(int)
        self.last_pos = self.champ.pos
        self.path = []
        self.finished = self.champ.pos == self.iend
        self.backtrack = False
        np.random.seed(int(time.time()))
    def update(self):
        if self.champ.waiting_order and self.champ.pos != self.iend:
            move = self.decide_next_move(self.champ.pos)
            self.last_pos = self.champ.pos
            self.champ.set_order(move)

    def decide_next_move(self,pos):
        c_adj = self.find_walkable(pos)
        if self.iend in c_adj:
            print("Iend:",self.iend,"at a touching pos")
            next_block = self.iend
        elif len(c_adj)>2:
            # is a junction
            print("We are in a junction")
            print(c_adj)
            marked = [i for i in c_adj if self.check_mark(i)>0]
            if len(marked)==0:
                # no visited
                print("Junction not visited, taking random way")
                next_block = [i for i in c_adj if i != self.last_pos][np.random.randint(0,len(c_adj)-1)]
            elif self.backtrack:
                # backtracking
                no_marked = [i for i in c_adj if self.check_mark(i)==0]
                if len(no_marked)>1:
                    next_block = no_marked[np.random.randint(0,len(no_marked))]
                    self.backtrack = False
                elif len(no_marked)==1:
                    next_block = no_marked[0]
                    self.backtrack = False
                else:
                    lessmarks = sorted(c_adj,key=lambda e: self.check_mark(e))
                    next_block = lessmarks[0]
            else:
                # visited
                next_block = self.last_pos
                print("Junction visited, backtracking")
                self.backtrack = True
            self.add_mark(self.last_pos)
            self.add_mark(next_block)
        elif len(c_adj)==1 and c_adj[0] == self.last_pos:
            # Closed path
            next_block = self.last_pos 
        else:
            # is a one-way path
            next_block = [i for i in c_adj if i != self.last_pos][0]
        return next_block
    def add_mark(self,pos):
        cols,fils = pos
        print("Adding mark to fila:",fils,"and column:",cols)
        self.matrix_marks[fils,cols] = self.matrix_marks[fils,cols] +1
    def check_mark(self,pos):
        cols,fils = pos
        return self.matrix_marks[fils,cols]
    def make_mark_surface(self):
        sur = pygame.Surface(self.map.size,pygame.SRCALPHA,32)
        sur = sur.convert_alpha()
        fils,cols = self.matrix_marks.shape
        for fil in range(fils):
            for col in range(cols):
                m = self.matrix_marks[fil,col]
                if m != 0:
                    x,y = tuple(np.multiply((col,fil),conf.tile_size))
                    x = x+conf.tile_size[0]-5
                    y = y+conf.tile_size[1]//2
                    pos = (x,y)
                    try:
                        pygame.draw.circle(sur,conf.mark_color[m],pos,5)
                    except:
                        print("M:",m)
        return sur

    def find_walkable(self,ind):
        adj = []
        x,y = ind
        poss = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
        for a,b in poss:
            if (a>=0 and a<self.map.ncols) and (b>=0 and b<self.map.nfils) and self.check_mark((a,b))<2 and self.map.matrix_map[b,a]==0:
                adj.append((a,b))
        return adj
def main():
    game = Joc()
    game.run()

if __name__=="__main__":
    main()