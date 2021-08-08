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

wow okay a lot of progress coming here, loading and saving are done, we have a log, and the
  tile menu is coming along nicely, still needs work on the UI but functionally were almost there

TILE MENU TO DO
===============
 []  GUI should highlight depth options
?[]  Show on level view?
 []  key map blacklist (no overriding special keys)

on the note of special keys, make a sort of cheat sheet help menu for the log maybe

still some crashes i think but were getting closer!
"""
import pygame
from pygame.locals import *

from ast import literal_eval
from pathlib import Path
import os

from src.tokens import tokens as tk
from src.tokens.tokens import KEYBOARD_MAP
from src.config.editor import *
from src.utils.input import expect_key

levelpath = Path(os.path.dirname(os.path.abspath(__file__))) / "bin"

DRAW_ZONES = {
    "tile menu"    : pygame.Surface((PW * 10, HEIGHT)),
    "enemy menu"   : pygame.Surface((PW * 10, HEIGHT)),
    "doors menu"   : pygame.Surface((PW * 10, HEIGHT)),
    "scene menu"   : pygame.Surface((PW * 10, HEIGHT)),
    "token editor" : pygame.Surface((PW * PW, PW * PW)),
    "level view"   : pygame.Surface((WIDTH, HEIGHT)),
    "log"          : pygame.Surface((PW * 20, HEIGHT)),
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
    "log"          : {},
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

def save(filename):
    try:
        with open(levelpath/filename, "w") as f:
            f.write(repr({
                "COLOR": COLOR,
                "TILES": TILES,
                "SPAWNS": SPAWNS,
                "DOORS": DOORS,
            }))
        return "Saved as "+filename+"."
    except IOError:
        return "IOError saving "+filename+"."


def load(filename):
    global COLOR, TILES, SPAWNS, DOORS
    try:
        with open(levelpath/filename, "r") as f:
            level_dict = literal_eval(f.read())
        COLOR = level_dict["COLOR"]
        TILES = level_dict["TILES"]
        SPAWNS = level_dict["SPAWNS"]
        DOORS = level_dict["DOORS"]
    except IOError:
        return "IOError "+filename+" not loadable."
    except SyntaxError:
        return "Corrupted level file "+filename+"." 

def run_editor(filename):
    global SCREEN
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    DRAW_ZONES["log"].fill((255, 255, 255))

    log(load(filename))
    while True:
        draw(SCREEN)
        resolve_input()
        pygame.display.update()


def log(string):
    if not string: return
    newlog = pygame.Surface((PW*20, PW*HEIGHT))
    newlog.fill((255, 255, 255))
    tk.draw_sentance(newlog, string, (0, 0), col1=(255, 255, 255), col2=(0, 0, 0), PW=1)
    newlog.blit(DRAW_ZONES["log"], (0, 16))
    DRAW_ZONES["log"] = newlog


def update_level_view():
    CX = MENU_STATES["level view"]["X"]
    CY = MENU_STATES["level view"]["Y"]
    dx = WIDTH / 2
    dy = HEIGHT / 2
    
    DRAW_ZONES["level view"].fill((180, 180, 180))
    for token in TILES:
        for position in TILES[token]:
            x, y = position
            x -= CX
            y -= CY
            tk.draw_token(DRAW_ZONES["level view"], token, (x*PW+dx, y*PW+dy), PW=PW//16)
    # draw cursor
    pygame.draw.line(DRAW_ZONES["level view"], (255, 0, 0), (dx, dy), (dx+PW, dy+PW), width=2)
    pygame.draw.line(DRAW_ZONES["level view"], (255, 0, 0), (dx, dy+PW), (dx+PW, dy), width=2)


def update_tile_menu():
    state = MENU_STATES["tile menu"]
    dest = DRAW_ZONES["tile menu"]
    dest.fill((160, 160, 160))
    for y, tile in enumerate(state["order"]):
        menu_segment = pygame.Surface((PW * 9, PW * 2))
        col = (50, 100, 50) if y == state["cursor"] else (50, 50, 50)
        menu_segment.fill(col)

        tk.draw_sentance(menu_segment, tile[:6], (PW//2, PW//2), PW=PW//16)
        tk.draw_token(menu_segment, tile, (PW*6+PW//2, PW//2), PW=PW//16)

        key_select = None
        for key in KEY_TILE_MAP:
            if state["order"][y] in KEY_TILE_MAP:
                key_select = key
                break

        if key_select:
            tk.draw_token(menu_segment, KEYBOARD_MAP[key_select], (PW*7+PW//2, PW//2), PW=PW//16)

        tk.draw_token(menu_segment, "x", (PW*8+PW//2, PW//2), PW=PW//16)

        dest.blit(menu_segment, (PW//2, (y*PW*2 + PW//2)))

    col = (50, 100, 50) if state["cursor"] == len(state["order"]) else (0, 0, 0)
    tk.draw_sentance(dest, "+",
                     (PW*2, len(state["order"])*PW*2+PW),
                     col1=col, PW=PW//16)


def draw(dest):
    dest.fill((255, 255, 255))
    update_level_view()
    update_tile_menu()
    dest.blit(DRAW_ZONES["level view"], (0, 0))
    if MENU not in ["level view", "log"]:
        dest.blit(DRAW_ZONES[MENU], (0, 0))
    dest.blit(DRAW_ZONES["log"], (WIDTH-PW*20, (HEIGHT-16) * (MENU != "log")))

def resolve_tile_events(e):
    state = MENU_STATES["tile menu"]
    name = state["order"][state["cursor"]] if state["order"] and state["cursor"] < len(state["order"]) else None

    if e.type != KEYDOWN: return
    # update curor
    if e.key == K_LEFT: state["depth"] = max(0, state["depth"] - 1)
    elif e.key == K_UP:state["cursor"] = max(0, state["cursor"] - 1)
    elif e.key == K_RIGHT: state["depth"] = min(3, state["depth"] + 1)
    elif e.key == K_DOWN: state["cursor"] = min(len(state["order"]), state["cursor"] + 1)
    
    elif e.key == K_SPACE:
        # check for add new
        if state["cursor"] == len(state["order"]):
            if inp := get_text_input():
                TILES[inp] = set()
                state["order"].append(inp)
                return "Create new tile " + inp +"."
        # check name
        elif state["depth"] == 0:
            if inp := get_text_input():
                TILES[inp] = TILES.pop(name)
                for key in KEY_TILE_MAP:
                    if KEY_TILE_MAP[key] == name:
                        KEY_TILE_MAP[key] = inp
                        break
                state["order"][state["order"].index(name)] = inp
                return "Change name "+name+" to "+inp+"."
        # check delete
        elif state["depth"] == 3:
            TILES.pop(name)
            state["order"].remove(name)
            return "Deleted tile "+name+"."
    else:
        # key select
        if state["depth"] == 2 and state["cursor"] < len(state["order"]):
            for key in KEY_TILE_MAP:
                if KEY_TILE_MAP[key] == state["order"][state["cursor"]]:
                   KEY_TILE_MAP.pop(key)
                   break
            KEY_TILE_MAP[e.key] = state["order"][state["cursor"]]
            return "Key "+KEYBOARD_MAP[e.key]+" set to "+state["order"][state["cursor"]]+"."

def resolve_view_events(e):
    if e.type != KEYDOWN: return
    state = MENU_STATES["level view"]
    if pygame.key.get_mods() & KMOD_SHIFT:
        if e.key == K_LEFT: state["X"] -= 4
        elif e.key == K_UP: state["Y"] -= 4
        elif e.key == K_RIGHT: state["X"] += 4
        elif e.key == K_DOWN: state["Y"] += 4

        elif e.key == K_s:
            tk.draw_sentance(SCREEN, "Save as?", (0, 0), PW=PW//16)
            pygame.display.update()
            if inp := get_text_input():
                log(save(inp))
    else:
        if e.key == K_LEFT: state["X"] -= 1
        elif e.key == K_UP: state["Y"] -= 1
        elif e.key == K_RIGHT: state["X"] += 1
        elif e.key == K_DOWN: state["Y"] += 1
        
        elif e.key in KEY_TILE_MAP:
            TILES[KEY_TILE_MAP[e.key]].add((state["X"], state["Y"]))
    

def get_text_input(pos=(PW*10, 0)):
    string = ""
    while True:
        tk.draw_sentance(SCREEN, " "*20, pos)
        tk.draw_sentance(SCREEN, string, pos)
        pygame.display.update()

        inp = expect_key()
        if inp == K_ESCAPE: return False
        if inp == K_BACKSPACE: string = string[:-1]
        if inp == K_RETURN: return string

        if inp in KEYBOARD_MAP:
            string = string + KEYBOARD_MAP[inp]
        


def resolve_input():
    global MENU
    for e in pygame.event.get():
        if (e.type == QUIT or e.type == KEYDOWN and
            pygame.key.get_mods() & KMOD_SHIFT and e.key == K_ESCAPE):
            quit()

        if MENU == "level view":
            log(resolve_view_events(e))
        elif MENU == "tile menu":
            log(resolve_tile_events(e))
            
        if e.type == KEYDOWN:
            if e.key == K_PERIOD:
                MENU = MENU_ORDER[(MENU_ORDER.index(MENU) + 1) % len(MENU_ORDER)]
            if e.key == K_COMMA:
                MENU = MENU_ORDER[(MENU_ORDER.index(MENU) - 1) % len(MENU_ORDER)]
