# Made by racteur 22/02/2024 ;-)

import time
from search import *

import pygame as pg

SQUARE_SIZE = 32

def decode(state):
    map = str(state).strip().split("\n")
    map = map[1:]
    
    for i in range(len(map)):
        map[i] = list(map[i])
    
    sizes = (len(map), len(map[0]))
    
    return sizes, map

WALL = pg.image.load("images/blue_stone.png")
PACMOZ = pg.image.load("images/pacmoz.png")

PACPOW = pg.image.load("images/pacpow.png")
PACMAN_LEFT = pg.image.load("images/pacman_left.png")
PACMAN_RIGHT = pg.image.load("images/pacman_right.png")
PACMAN_UP = pg.image.load("images/pacman_up.png")
PACMAN_DOWN = pg.image.load("images/pacman_down.png")

class Viewer:
    """
    To make visualisation during computation
    """
    
    def __init__(self, width, height, timing=0.01, use_pacmoz=False):
        self.app = pg.init()
        
        if use_pacmoz:
            pg.display.set_caption("!! PACMOZ !!")
        else:
            pg.display.set_caption("PACMAN")
    
        self.mode = pg.display.set_mode((width * SQUARE_SIZE, height * SQUARE_SIZE))
        self.positions = None
        self.timing = timing
        self.use_pacmoz = use_pacmoz
        
    def update(self, state):
        sizes, map = decode(state)
        
        self.mode.fill((0, 0, 0))
        
        for x in range(sizes[0]):
            for y in range(sizes[1]):
                if map[x][y] == "#":
                    self.mode.blit(WALL, (x * 32, y * 32))
                elif map[x][y] == "P":
                    if self.use_pacmoz:
                        self.mode.blit(PACMOZ, (x * 32, y * 32))
                    else:
                        if self.positions == None:
                            choice = PACMAN_UP
                        else:    
                            ox, oy = self.positions
                            
                            if x < ox:
                                choice = PACMAN_LEFT
                            elif ox < x:
                                choice = PACMAN_RIGHT
                            elif oy < y:
                                choice = PACMAN_DOWN
                            else:
                                choice = PACMAN_UP
                            
                        self.mode.blit(choice, (x * 32, y * 32))
                        
                        self.positions = (x, y)
                elif map[x][y] == "F":
                    self.mode.blit(PACPOW, (x * 32, y * 32))

        pg.display.flip()
        time.sleep(self.timing)
        
    def wait(self):
        working = True
        
        while working:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    working = False
                    break
            
            time.sleep(0.01)
        
def show(node, timing=0.5, use_pacmoz=False, viewer=None):
    """
    node is a Node of search.py or a list of nodes
    """
    
    if type(node) == Node:
        nodes = node.path()
    elif type(node) == list:
        nodes = []
        
        for n in node:
            nodes.extend(n.path())
    
    sizes, map = decode(nodes[0].state)
    
    if viewer == None:
        viewer = Viewer(sizes[0], sizes[1], use_pacmoz=use_pacmoz, timing=timing)
    
    for node in nodes:
        viewer.update(node.state)
    
    viewer.wait()