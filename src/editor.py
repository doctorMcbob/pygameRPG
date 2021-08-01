"""
Okay :) lets get to it

this will be a completely different flow from the game

There will me menues for 
[] Loading tokens and mapping them to keys
[] customizing enemies and setting spawn zones
[] setting doors and loading the level it leads to (or create new)
[] making event cutscenes

"""
import pygame
from pygame.locals import *

from src.tokens import tokens as tk
from src.config.editor import *

DRAW_ZONES = {
    "token menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "enemy menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "doors menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "scene menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "token editor" : pygame.Surface((PW * PW, PW * PW)),
    "level view"   : pygame.Surface((WIDTH, HEIGHT)),
}
MENU = "token menu"

SCREEN = None
CX, CY = 0, 0

KEY_TILE_MAP = {}

COLOR = {}
TILES = {}
SPAWNS = []
DOORS = {}

def run_editor(filename):
    global SCREEN
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    while True:
        draw(SCREEN)
        resolve_input()
        pygame.display.update()


def update_level_view():
    DRAW_ZONES["level view"].fill((180, 180, 180))
    for token in TILES:
        for position in TILES[token]:
            x, y = position
            x -= CX * PW
            Y -= CY * PW
            tk.draw_token(DRAW_ZONES["level view"], token, (x*PW, y*PW))
    # draw cursor
    x = WIDTH / 2
    y = HEIGHT / 2
    pygame.draw.line(DRAW_ZONES["level view"], (255, 0, 0), (x, y), (x+PW, y+PW), width=2)
    pygame.draw.line(DRAW_ZONES["level view"], (255, 0, 0), (x, y+PW), (x+PW, y), width=2)


def draw(dest):
    dest.fill((255, 255, 255))
    update_level_view()
    dest.blit(DRAW_ZONES["level view"], (0, 0))
    dest.blit(DRAW_ZONES[MENU], (0, 0))
    
    
def resolve_input():
    global CX, CY
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
        if e.type == KEYDOWN:
            if pygame.key.get_mods() & KMOD_SHIFT:
                if e.key == K_LEFT: CX -= 4
                elif e.key == K_UP: CY -= 4
                elif e.key == K_RIGHT: CX += 4
                elif e.key == K_DOWN: CY -= 4
            else:
                if e.key == K_LEFT: CX -= 1
                elif e.key == K_UP: CY -= 1
                elif e.key == K_RIGHT: CX += 1
                elif e.key == K_DOWN: CY -= 1

                elif e.key in KEY_TILE_MAP:
                    TILES[KEY_TILE_MAP].add((CX, CY))
    
