"""
Okay :) lets get to it

this will be a completely different flow from the game

There will me menues for 
[] Loading tokens and mapping them to keys
[] customizing enemies and setting spawn zones
[] setting doors and loading the level it leads to (or create new)
[] making event cutscenes


im thinking there will be one menu scoped at a time, with keys < > to switch scope

each menu will have a resolve inputs function and state dictionary

they will each all be drawn seperately and stored as Surfaces to be drawn to screen seperately 
"""
import pygame
from pygame.locals import *

from src.tokens import tokens as tk
from src.config.editor import *

DRAW_ZONES = {
    "tile menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "enemy menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "doors menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "scene menu"   : pygame.Surface((PW * 5, HEIGHT)),
    "token editor" : pygame.Surface((PW * PW, PW * PW)),
    "level view"   : pygame.Surface((WIDTH, HEIGHT)),
}
MENU = "level view"

MENU_STATES = {
    "tile menu"   : {
        "cursor": 0,
        "depth": 0,
        "order": [],
    },
    "enemy menu"   : {},
    "doors menu"   : {},
    "scene menu"   : {},
    "token editor" : {},
    "level view"   : {
        "X": 0,
        "Y": 0,
    },
}
MENU_ORDER = list(MENU_STATES.keys())

SCREEN = None

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
    if MENU != "level view":
        dest.blit(DRAW_ZONES[MENU], (0, 0))


def resolve_tile_events(e):
    state = MENU_STATES["tile menu"]
    name = None if not state["order"] else state["order"][state["cursor"]]

    if e.type != KEYDOWN: return
    # update curor
    if e.key == K_LEFT: state["depth"] = max(0, state["depth"] - 1)
    elif e.key == K_UP:state["cursor"] = min(len(state["order"]), state["cursor"] + 1)
    elif e.key == K_RIGHT: state["depth"] = min(3, state["depth"] + 1)
    elif e.key == K_DOWN: state["depth"] = min(len(state["order"]), state["cursor"] + 1)
    
    elif e.key == K_SPACE:
        # check for add new
        if state["cursor"] == len(state["order"]):
            if inp := get_text_input():
                TILES[inp] = set()
                state["order"].append(inp)                    
                # check name
        elif state["depth"] == 0:
            if inp := get_text_input():
                TILES[inp] = TILES.pop(name)
                state["order"][state["order"].index(name)] = inp
        # check delete
        elif state["depth"] == 3:
            TILES.pop(name)
            state["order"].remove(name)
    else:
        # key select
        if state["depth"] == 2 and state["cursor"] < len(state["order"]): 
            KEY_TILE_MAP[e.key] = state["order"][state["cursor"]]
            
def resolve_view_events(e):
    if e.type != KEYDOWN: return
    state = MENU_STATES["level view"]
    if pygame.key.get_mods() & KMOD_SHIFT:
        if e.key == K_LEFT: state["X"] -= 4
        elif e.key == K_UP: state["Y"] -= 4
        elif e.key == K_RIGHT: state["X"] += 4
        elif e.key == K_DOWN: state["Y"] -= 4
    else:
        if e.key == K_LEFT: state["X"] -= 1
        elif e.key == K_UP: state["Y"] -= 1
        elif e.key == K_RIGHT: state["X"] += 1
        elif e.key == K_DOWN: state["Y"] -= 1
        
        elif e.key in KEY_TILE_MAP:
            TILES[KEY_TILE_MAP[e.key]].add((state["X"], state["Y"]))
    

def get_text_input():
    return False


def resolve_input():
    global MENU
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            quit()

        if MENU == "level view":
            resolve_view_events(e)
        elif MENU == "tile menu":
            resolve_tile_events(e)
            
        if e.type == KEYDOWN:
            if e.key == K_PERIOD:
                MENU = MENU_ORDER[(MENU_ORDER.index(MENU) + 1) % len(MENU_ORDER)]
            if e.key == K_COMMA:
                MENU = MENU_ORDER[(MENU_ORDER.index(MENU) - 1) % len(MENU_ORDER)]
